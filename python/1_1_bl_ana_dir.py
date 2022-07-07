#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Analisis de las baselines. 

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, optimize
import bz2, os
from my_funcs import getfiles, h_loadtxt

NBINS    = 32  # 32 bines por pulso
ADCBITS  = 14  # 14 bits
TIME_SEP = 8e-9   # 8 ns por punto
BASELINE1= 0   # linea de base ch1 
BASELINE2= 0   # linea de base ch2 

#fname_prefix puede ser mon_hv,mon_hv_v2,spnk,spnk_v2,spnk_v3, spnk_coin, boy_spnk
fname_prefix = 'swgo'

sub_dir     = '{}'.format(fname_prefix)
proc_dir= '{}_proc/bl'.format(fname_prefix)

if os.path.isfile('{}_mean_bl_tot.bz2'.format(fname_prefix)):
    print('Los archivos de análisis ya existen. Continuemos ...')

else:
    for filename in sorted(getfiles(sub_dir)):
        #check if file exists
        exists = os.path.isfile(os.path.join(proc_dir,'mean_{}.bz2'.format(filename[:-4])))
        if exists:
            print('Filename: {} was procesed.'.format(filename))
        else:
            ch1, ch2 = np.loadtxt(os.path.join(sub_dir, filename), unpack=1, dtype=int)
            #ch1, ch2 = h_loadtxt(os.path.join(sub_dir, filename), ncols=2, dtyp=int)
            #check if length is ok
            ch1b=np.resize(ch1,ch1.size - len(ch1)%NBINS)
            ch2b=np.resize(ch2,ch2.size - len(ch2)%NBINS)
            bl1 = ch1b[0::NBINS]
            bl2 = ch2b[0::NBINS]
            np.savetxt(os.path.join(proc_dir,'mean_{}.bz2'.format(filename[:-4])),np.transpose([bl1, bl2]),fmt='%d')
            bl1 = bl2 = ch1 = ch2 = ch1b = ch2b = np.array([])
            print ('Done with', filename)
    	
    # Ahora hacemos los graficos correspondientes a la evolucion temporal de las baselines
    # en este caso voy a hacer los histogramas de las baselines
    hbl1=np.array([]) #va a contener la evolucion, en termino medio, de las baselines de los archivos fijos 
    hbl2=np.array([]) #va a contener la evolucion, en termino medio, de las baselines de los archivos fijos 
    #bnormal_dir = '/home/dpr/arnaldi/work/python/data/bnormal/'
    #for filename in os.listdir(procesed_dir):
    for filename in sorted(getfiles(proc_dir)):
        #check if file exists
        exists = os.path.isfile(os.path.join(proc_dir,filename))
        if exists:
            print('Filename: {} was procesed.'.format(filename))
        else:
            print('Filename: {} was NOT procesed. Proceedig ...'.format(filename))
        hch1, hch2 = np.loadtxt(os.path.join(proc_dir, filename), unpack=1, dtype=int)
        hbl1 = np.append(hbl1,hch1)
        hbl2 = np.append(hbl2,hch2)
        print('PLT Done with {}'.format(filename))
    
    np.savetxt('{}_mean_bl_tot.bz2'.format(fname_prefix),np.transpose([hbl1, hbl2]),fmt='%d')

hbl1, hbl2 = np.loadtxt('{}_mean_bl_tot.bz2'.format(fname_prefix), unpack=1, dtype=int)

# En esta parte remuevo los datos que están más lejos de mean+-std*2
mean1=np.mean(hbl1)
mean2=np.mean(hbl2)
sd1=np.std(hbl1)
sd2=np.std(hbl2)

hbl1 = [x for x in hbl1 if (x > mean1 - 2 * sd1)]
hbl2 = [x for x in hbl2 if (x > mean2 - 2 * sd2)]
hbl1 = [x for x in hbl1 if (x < mean1 + 2 * sd1)]
hbl2 = [x for x in hbl2 if (x < mean2 + 2 * sd2)]

fig,ax = plt.subplots(nrows=1, ncols=1, figsize=(7,6))

h1,bins1=np.histogram(hbl1,bins=np.arange(min(hbl1),max(hbl1) + 1, 1),density=1)
h2,bins2=np.histogram(hbl2,bins=np.arange(min(hbl2),max(hbl2) + 1, 1),density=1)
y1=stats.norm.pdf(bins1,np.mean(hbl1),np.std(hbl1))
y2=stats.norm.pdf(bins2,np.mean(hbl2),np.std(hbl2))
ax.plot(bins1[:-1],h1,'r*',lw=2,label='CH1')
ax.plot(bins2[:-1],h2,'k^',lw=2,label='CH2')
ax.plot(bins1,y1,'g--',lw=1,label='CH1, $\mu$ = {:2.2f}, $\sigma^2$ = {:2.2f}'.format(np.mean(hbl1),np.std(hbl1)**2))
ax.plot(bins2,y2,'b',lw=1,label='CH2, $\mu$ = {:2.2f}, $\sigma^2$ = {:2.2f}'.format(np.mean(hbl2),np.std(hbl2)**2))

ax.legend(fontsize=13)
#plt.title('Normalized PDF\'s')
#plt.title('Baseline by channel (PDF)')
ax.set_ylabel('Probability Density Function',fontsize=14, fontname='monospace')
ax.set_xlabel('ADC bins',fontsize=14, fontname='monospace')
ax.set_title('Histograma de las baselines para {}'.format(fname_prefix),fontsize=14, fontname='monospace')
#plt.ylim(0,0.45)
#plt.xlim(-40,40)
ax.grid()

plt.savefig('plot/{}_bl_tot.png'.format(fname_prefix))
#plt.savefig(os.path.join(proc_dir,'{}_bl_tot.png'.format(fname_prefix)))
print('CH1:',np.mean(hbl1),'CH2:',np.mean(hbl2))
plt.show()

#FIXME: agregar el gráfico de las baselines crudas
