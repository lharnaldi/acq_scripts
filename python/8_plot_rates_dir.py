#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# 
# Analisis de los metadatos de swgo. 
# Se analiza todo un directorio con archivos adquiridos con la rp.
# Al final se grafican los rates de los dos canales

import numpy as np
from scipy import stats, optimize
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import bz2, os, time
from my_funcs import getfiles

NBINS    = 32  # 32 bines por pulso
ADCBITS  = 14  # 14 bits
TIME_SEP = 8e-9   # 8 ns por punto
BASELINE = 0   # linea de base

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

#fname_prefix puede ser swgo
fname_prefix = 'swgo'
plot_dir = 'plot/' # Directorio donde se guardaran las graficas

sub_dir     = '{}'.format(fname_prefix)
proc_mtd_dir= '{}_proc/mtd'.format(fname_prefix)
proc_dt_dir = '{}_proc/dt'.format(fname_prefix)

if os.path.isfile('{}_mtd_tot.bz2'.format(fname_prefix)) and os.path.isfile('{}_dt_tot.bz2'.format(fname_prefix)):
    print('Los archivos de análisis ya existen. Continuemos ...')

else:
    dt      = np.array([])     #diferencias temporales
    tch     = np.array([])     #trigger channel
    cntri   = np.array([])     #contador interno de triggers
    sadq    = np.array([])     #segundos de adquisicion - tiempo
    clk_freq= np.array([])     #clock frequency
    tempi   = np.array([])     #internal temperature
    pres    = np.array([])     #internal presure
    r1      = np.array([])     #rate 1
    r2      = np.array([])     #rate 2
    hv1     = np.array([])     #HV1
    hv2     = np.array([])     #HV2
    temp1   = np.array([])     #temperatura leida del sensor AD592 ch1
    temp2   = np.array([])     #temperatura leida del sensor AD592 ch2
    tepoch  = np.array([])     #tiempo epoch

    for filename in sorted(getfiles(sub_dir)):
        #check if file exists
        exists = os.path.isfile(os.path.join(proc_mtd_dir,'mtd_'+filename[:-4]+'.bz2'))
        if exists:
            print('Filename:',filename,'was procesed.')
        else:
            #with open(os.path.join(sub_dir,filename),"r") as thefile:
            print('Filename:',filename,'now processing.')
            with bz2.open(os.path.join(sub_dir,filename),mode='rt',encoding='utf-8') as thefile:
                for line in thefile:
                    sp = line.split()
                    if sp[0] == '#':
                        if sp[1] == 't': #tiempos entre triggers
                            tch = np.append(tch,int(sp[2]))
                            dt  = np.append(dt,int(sp[3]))
                        if sp[1] == 'c': #internal counter to check if we loose pulses
                            cntri = np.append(cntri,int(sp[2]))
                        if sp[1] == 'p':
                            sadq = np.append(sadq,int(sp[2]))
                            temp1 = np.append(temp1,float(sp[3]))
                            temp2 = np.append(temp2,float(sp[4]))
                
                        if sp[1] == 'x':
                            if sp[2] == 'f': # x f <V>        : 125 MHz frequency
                                clk_freq = np.append(clk_freq,int(sp[3]))
                            if sp[2] == 't': # x t <V>        : temperature value
                                tempi = np.append(tempi,float(sp[3]))
                            if sp[2] == 'p': # x p <V>        : pressure value
                                pres = np.append(pres,float(sp[3]))
                            if sp[2] == 'h': # GPS data
                                tepoch = np.append(tepoch,int(sp[5]))
                                #print(line[9])
                                pass
                            if sp[2] == 'v': # x v <HV1> <HV2>         : HV voltages for channels 1 and 2
                                hv1 = np.append(hv1,float(sp[3]))
                                hv2 = np.append(hv2,float(sp[4]))
                        if sp[1] == 'r1': # r1 <V>       : pulse rate at channel 1
                            r1 = np.append(r1,int(sp[2]))
                        if sp[1] == 'r2': # r2 <V>       : pulse rate at channel 2
                            r2 = np.append(r2,int(sp[2]))
    
                if len(r1)>len(temp1):
                    r1=r1[:-1]
                    r2=r2[:-1]
                if len(pres)>len(r1):
                    sadq=sadq[1:]
                    temp1=temp1[1:]
                    temp2=temp2[1:]
                    clk_freq=clk_freq[1:]
                    tempi=tempi[1:]
                    pres=pres[1:]
                    tepoch=tepoch[1:]
                    hv1=hv1[1:]
                    hv2=hv2[1:]
    
                np.savetxt(os.path.join(proc_mtd_dir,'mtd_'+filename[:-4]+'.bz2'),np.transpose([sadq,tepoch,clk_freq,r1,r2,tempi,pres,hv1,hv2,temp1,temp2]),fmt=('%d %d %d %d %d %.2f %.2f %.2f %.2f %.2f %.2f')) 
                np.savetxt(os.path.join(proc_dt_dir,'dt_'+ filename[:-4]+'.bz2'),np.transpose([cntri,tch,dt]),fmt=('%d %d %d')) 
                sadq=tepoch=clk_freq=r1=r2=tempi=pres=hv1=hv2=temp1=temp2=cntri=tch=dt=np.array([]) 
                thefile.close()
            

    idt      = np.array([])     #diferencias temporales
    itch     = np.array([])     #trigger channel
    icntri   = np.array([])     #contador interno de triggers
    isadq    = np.array([])     #segundos de adquisicion - tiempo
    iclk_freq= np.array([])     #clock frequency
    itempi   = np.array([])     #internal temperature
    ipres    = np.array([])     #internal presure
    ir1      = np.array([])     #rate 1
    ir2      = np.array([])     #rate 2
    ihv1     = np.array([])     #HV1
    ihv2     = np.array([])     #HV2
    itemp1   = np.array([])     #temperatura leida del sensor AD592 ch1
    itemp2   = np.array([])     #temperatura leida del sensor AD592 ch2
    itepoch  = np.array([])     #tiempo epoch
    
    for filename in sorted(getfiles(proc_mtd_dir)):
        #check if file exists
        exists = os.path.isfile(os.path.join(proc_mtd_dir,'mtd_'+filename[:-4]+'.bz2'))
        if exists:
            print('Filename:',filename,'was procesed.')
        else:
            print('Filename:',filename,'was NOT procesed. Proceedig ...')
    
        sadq,tepoch,clk_freq,r1,r2,tempi,pres,hv1,hv2,temp1,temp2 = np.loadtxt(os.path.join(proc_mtd_dir, filename), unpack=1)
        isadq    = np.append(isadq,sadq)
        iclk_freq= np.append(iclk_freq,clk_freq)
        itempi   = np.append(itempi,tempi)
        ipres    = np.append(ipres,pres)
        ir1      = np.append(ir1,r1)
        ir2      = np.append(ir2,r2)
        ihv1     = np.append(ihv1,hv1)
        ihv2     = np.append(ihv2,hv2) 
        itemp1   = np.append(itemp1,temp1)
        itemp2   = np.append(itemp2,temp2) 
        itepoch  = np.append(itepoch,tepoch) 
        print('PLT Done with', filename)

    for filename in sorted(getfiles(proc_dt_dir)):
        #check if file exists
        exists = os.path.isfile(os.path.join(proc_dt_dir,'dt_'+filename[:-4]+'.bz2'))
        if exists:
            print('DT: Filename:',filename,'was procesed.')
        else:
            print('DT: Filename:',filename,'was NOT procesed. Proceedig ...')
    
        cntri,tch,dt = np.loadtxt(os.path.join(proc_dt_dir, filename), unpack=1)
        icntri   = np.append(icntri,cntri)
        itch     = np.append(itch,tch)
        idt      = np.append(idt,dt)
        print('DT: PLT Done with', filename)

    np.savetxt('{}_mtd_tot.bz2'.format(fname_prefix),np.transpose([isadq,itepoch,iclk_freq,ir1,ir2,itempi,ipres,ihv1,ihv2,itemp1,itemp2]),fmt=('%d %d %d %d %d %.2f %.2f %.2f %.2f %.2f %.2f'))
    np.savetxt('{}_dt_tot.bz2'.format(fname_prefix),np.transpose([icntri,itch,idt]),fmt=('%d %d %d'))

    #borro mis variables
    del isadq,itepoch,iclk_freq,ir1,ir2,itempi,ipres,ihv1,ihv2,itemp1,itemp2,icntri,itch,idt
    del sadq,tepoch,clk_freq,r1,r2,tempi,pres,hv1,hv2,temp1,temp2,cntri,tch,dt

sadq,tepoch,clk_freq,r1,r2,tempi,pres,hv1,hv2,temp1,temp2 = np.loadtxt('{}_mtd_tot.bz2'.format(fname_prefix), unpack=1)
#cntri,tch,dt = np.loadtxt('{}_dt_tot.bz2'.format(fname_prefix), unpack=1)



r1ma=movingaverage(r1,100)
r2ma=movingaverage(r2,100)

secs = mdate.epoch2num(tepoch)
                                                

#grafico de los rates por canal
fig,ax=plt.subplots(1,2,sharey=True,figsize=(10,5))
# Plot the date using plot_date rather than plot
l1, =ax[0].plot_date(secs,r1,'C2')
l2, =ax[0].plot_date(secs[:len(r1ma)],r1ma,'C1',label='Rates CH1')
ax[0].set_ylabel('Pulses per second)')
ax[0].set_xlabel('Time (s)')


# Choose your xtick format string
date_fmt = '%d-%m-%y %H:%M:%S'
# Use a DateFormatter to set the data to the correct format.
date_formatter = mdate.DateFormatter(date_fmt)
ax[0].xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()

l3,=ax[1].plot_date(secs,r2,'C2')
l4,=ax[1].plot_date(secs[:len(r2ma)],r2ma,'C1',label='Rates CH2')
# Choose your xtick format string
date_fmt = '%d-%m-%y %H:%M:%S'
# Use a DateFormatter to set the data to the correct format.
date_formatter = mdate.DateFormatter(date_fmt)
ax[1].xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()
ax[1].set_xlabel('Time (s)')
ax[0].legend((l1,l2),('Rates Ch1',r'Mean ({:3.1f}$\pm${:3.1f})'.format(r1.mean(),r1.std())))
ax[1].legend((l3,l4),('Rates Ch2',r'Mean ({:3.1f}$\pm${:3.1f})'.format(r2.mean(),r2.std())))
fig.suptitle('Rates')
plt.savefig(os.path.join(plot_dir,'rates_ch1_ch2_ma_{}.png'.format(fname_prefix)))
plt.show()

#grafico de los rates por canal
fig,ax=plt.subplots(1,1,figsize=(10,5))
l1, =ax.plot_date(secs,r1,'C2')
l2, =ax.plot_date(secs[:len(r1ma)],r1ma,'C1',label='Rates CH1')
# Choose your xtick format string
date_fmt = '%d-%m-%y %H:%M:%S'
# Use a DateFormatter to set the data to the correct format.
date_formatter = mdate.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()
ax.set_ylabel('Pulses per second)')
ax.set_xlabel('Time (s)')
ax.legend((l1,l2),('Rates Ch1',r'Mean ({:3.1f}$\pm${:3.1f})'.format(r1.mean(),r1.std())))
fig.suptitle('Rates')
plt.savefig(os.path.join(plot_dir,'rates_ch1_ma_{}.png'.format(fname_prefix)))
plt.show()
