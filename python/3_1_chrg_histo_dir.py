#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Graficas de los histogramas de carga de los pulsos en los 
# canales adquiridos.
# Los archivos a analizar pueden tener la extensión .dat o .bz2

import numpy as np
import matplotlib.pyplot as plt
import os, bz2
from my_funcs import getfiles

NBINS    = 32  # 32 bines por pulso
ADCBITS  = 14  # 14 bits
TIME_SEP = 8e-9   # 8 ns por punto
#BASELINE1= bl1[1] # linea de base ch1 
#BASELINE2= bl2[1] # linea de base ch2 

#fname_prefix puede ser mon_hv,mon_hv_v2,spnk,spnk_v2, spnk_v3, spnk_coin, boy_spnk
fname_prefix = 'swgo'

bl1,bl2=np.loadtxt('baselines.txt',unpack=1)
if fname_prefix=='swgo':
    BASELINE1=bl1[0]
    BASELINE2=bl2[0]
elif fname_prefix=='mon_hv_v2':
    BASELINE1=bl1[1]
    BASELINE2=bl2[1]
elif fname_prefix=='spnk':
    BASELINE1=bl1[2]
    BASELINE2=bl2[2]
elif fname_prefix=='spnk_v2':
    BASELINE1=bl1[3]
    BASELINE2=bl2[3]
elif fname_prefix=='spnk_v3':
    BASELINE1=bl1[4]
    BASELINE2=bl2[4]
elif fname_prefix=='spnk_coin':
    BASELINE1=bl1[5]
    BASELINE2=bl2[5]
elif fname_prefix=='boy_spnk':
    BASELINE1=bl1[6]
    BASELINE2=bl2[6]
elif fname_prefix=='boy_solo':
    BASELINE1=bl1[6]
    BASELINE2=bl2[6]
elif fname_prefix=='cente_solo':
    BASELINE1=bl1[7]
    BASELINE2=bl2[7]
elif fname_prefix=='boy_cente':
    BASELINE1=bl1[8]
    BASELINE2=bl2[8]

print(BASELINE1, BASELINE2)
sub_dir     = '{}'.format(fname_prefix)
proc_dir= '{}_proc/chrg'.format(fname_prefix)

if os.path.isfile('{}_chrg_tot.bz2'.format(fname_prefix)):
    print('Los archivos de análisis ya existen. Continuemos ...')

else:
    for filename in sorted(getfiles(sub_dir)):
        #check if file exists
        exists = os.path.isfile(os.path.join(proc_dir,'chrg_{}.bz2'.format(filename[:-4])))
        if exists:
            print('Filename: {} was procesed.'.format(filename))
        else:
            ch1, ch2 = np.loadtxt(os.path.join(sub_dir, filename), unpack=1, dtype=int)
            #check if length is ok
            ch1b=np.resize(ch1,ch1.size - len(ch1)%NBINS)
            ch2b=np.resize(ch2,ch2.size - len(ch2)%NBINS)
    
            #para sacar los histogramas de carga
            h1=np.array([(ch1b[i:i+NBINS]-BASELINE1).sum() for i in np.arange(0,len(ch1b),NBINS)])
            h2=np.array([(ch2b[i:i+NBINS]-BASELINE2).sum() for i in np.arange(0,len(ch2b),NBINS)])
    
            #Para graficar cada uno de los archivos
            #hi1,b1=np.histogram(chrg1,bins='auto',density=1)
            #hi2,b2=np.histogram(chrg2,bins='auto',density=1)
            #hi1,b1=np.histogram(h1,bins=np.arange(min(h1),max(h1) + 1, 1),density=1)
            #hi2,b2=np.histogram(h2,bins=np.arange(min(h2),max(h2) + 1, 1),density=1)
            hi1,b1=np.histogram(h1,bins=np.arange(min(h1),max(h1) + 1, 1))
            hi2,b2=np.histogram(h2,bins=np.arange(min(h2),max(h2) + 1, 1))
            #hi1,b1=np.histogram(chrg1,8192)
            #hi2,b2=np.histogram(chrg2,8192)
            
            #Para graficar cada uno de los histogramas por separado
            #fig, ax= plt.subplots(1, 1, figsize=(7, 6))
            #ax.grid()
            #
            ##ax.loglog(b1[:-1],hi1, color='red', lw=2, label='CH1')
            ##ax.loglog(b2[:-1],hi2, color='blue', lw=2, label='CH2')
            #ax.semilogx(b1[:-1],hi1, color='red', lw=2, label='CH1')
            #ax.semilogx(b2[:-1],hi2, color='blue', lw=2, label='CH2')
            #ax.legend()
            #
            #ax.set_xlabel('ADC bins',fontsize=14, fontname='monospace')
            #ax.set_ylabel('# of entries',fontsize=14, fontname='monospace')
            ##ax.set_ylim(1,0.8e4)
            ##ax.set_xlim(50,400)
            #plt.show()
    
            np.savetxt(os.path.join(proc_dir,'chrg_{}.bz2'.format(filename[:-4])),np.transpose([h1,h2]),fmt='%d')
    
            ch1 = ch2 = ch1b = ch2b = h1 = h2 = np.array([])
            print('Done with {}'.format(filename))
    
    
    # Ahora hacemos los graficos correspondientes a la evolucion temporal de las baselines
    chrg1=np.array([]) 
    chrg2=np.array([]) 
    for filename in sorted(getfiles(proc_dir)):
        #check if file exists
        exists = os.path.isfile(os.path.join(proc_dir,filename))
        if exists:
            print('Filename: {} was procesed.'.format(filename))
        else:
            print('Filename: {} was NOT procesed. Proceedig ...'.format(filename))
    
        chg1, chg2 = np.loadtxt(os.path.join(proc_dir, filename), unpack=1, dtype=int)
        chrg1 = np.append(chrg1,chg1)
        chrg2 = np.append(chrg2,chg2)
        print('PLT Done with {}'.format(filename))
    
    
    np.savetxt('{}_chrg_tot.bz2'.format(fname_prefix),np.transpose([chrg1, chrg2]),fmt='%d')

chrg1, chrg2 = np.loadtxt('{}_chrg_tot.bz2'.format(fname_prefix), unpack=1, dtype=int)

#h1,b1=np.histogram(chrg1,bins=np.arange(min(chrg1),max(chrg1) + 1, 1),density=1)
#h2,b2=np.histogram(chrg2,bins=np.arange(min(chrg2),max(chrg2) + 1, 1),density=1)
h1,b1=np.histogram(chrg1,bins=np.arange(min(chrg1),max(chrg1) + 1, 1))
h2,b2=np.histogram(chrg2,bins=np.arange(min(chrg2),max(chrg2) + 1, 1))
#h1,b1=np.histogram(chrg1,bins='auto',density=1)
#h2,b2=np.histogram(chrg2,bins='auto',density=1)
#h1,b1=np.histogram(chrg1,8192)
#h2,b2=np.histogram(chrg2,8192)
x1 = (b1[1:] + b1[:-1])/2
x2 = (b2[1:] + b2[:-1])/2

fig, ax= plt.subplots(1, 1, figsize=(7, 6))
ax.grid()

ax.semilogx(x1,h1, color='red', lw=2, label='CH1')
ax.semilogx(x2,h2, color='blue', lw=2, label='CH2')
#ax.plot(b1[:-1],h1, color='red', lw=2, label='CH1')
#ax.plot(b2[:-1],h2, color='blue', lw=2, label='CH2')
#ax.semilogx(b1[:-1],h1, color='red', lw=2, label='CH1')
#ax.semilogx(b2[:-1],h2, color='blue', lw=2, label='CH2')
ax.legend(fontsize=13)
ax.set_xlabel('ADC bins',fontsize=14, fontname='monospace')
ax.set_ylabel('# of entries',fontsize=14, fontname='monospace')
#ax.set_ylim(1,0.8e4)
#ax.set_xlim(50,400)
# this is an inset axes over the main axes
#a = plt.axes([.65, .6, .2, .2], axisbg='y', alpha=0.02)
#a = plt.axes([.55, .55, .32, .32])
#a.loglog(hcar2.mean(axis=0), color='blue', lw=2, label='CH2')
#a.loglog(hcar2.mean(axis=0), color='blue', label='CH2')
#a.loglog(b1[:-1],h1,b2[:-1],h2,bins3[:-1],n3)
#a.loglog(b2[:-1],h2, color='blue', lw=2, label='CH2')
#a.set_xlabel('Charge [ADC.bin]',fontsize=14, fontname='monospace')
#a.set_ylabel('Counts',fontsize=14, fontname='monospace')
#a.set_ylim(1,2e4)
#a.set_xlim(50,400)
#a.grid()
#plt.savefig('histo_carga.png')
plt.savefig('plot/{}_chrg_tot.png'.format(fname_prefix))
#plt.savefig(os.path.join(proc_dir,'{}_chrg_tot.pdf'.format(fname_prefix)))
plt.show()

