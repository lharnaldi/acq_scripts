#!/usr/bin/env python3
#
# -*- encoding: utf-8 -*-
# Analisis de las baselines. 

import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import os

NBINS    = 32  # 32 bines por pulso
ADCBITS  = 14  # 14 bits
TIME_SEP = 8   # 8 ns por punto
BASELINE = 0   # linea de base

data_dir = 'data/' # Directorio donde se encuentran los datos
plot_dir = 'plot/' # Directorio donde se guardaran las graficas
filename = input('Ingrese el nombre del archivo (*.dat o *.bz2) a procesar : ')
#filename= 'spnk_nogps_2021_07_23_03h00.dat.bz2'
ch1, ch2 = np.loadtxt(os.path.join(data_dir, filename), unpack=1, dtype=int)

#Para hacer el fit con una gaussiana, definimos la funcion
def gauss_function(x, a, x0, sigma):
	return a*np.exp(-(x-x0)**2/(2*sigma**2))

#check if length is ok
ch1b=np.resize(ch1,ch1.size - len(ch1)%NBINS)
ch2b=np.resize(ch2,ch2.size - len(ch2)%NBINS)

bl1 = ch1b[0::NBINS]
bl2 = ch2b[0::NBINS]

# En esta parte remuevo los datos que están más lejos de mean+-std*2
mean1=np.mean(bl1)
mean2=np.mean(bl2)
sd1=np.std(bl1)
sd2=np.std(bl2)

bl1 = [x for x in bl1 if (x > mean1 - 3 * sd1)]
bl2 = [x for x in bl2 if (x > mean2 - 3 * sd2)]
bl1 = [x for x in bl1 if (x < mean1 + 3 * sd1)]
bl2 = [x for x in bl2 if (x < mean2 + 3 * sd2)]

fig,ax = plt.subplots(nrows=1, ncols=1, figsize=(7,6))
ax.grid()

#h1,bins1=np.histogram(bl1,bins=np.arange(min(bl1),max(bl1) + 1, 1),density=1)
#h2,bins2=np.histogram(bl2,bins=np.arange(min(bl2),max(bl2) + 1, 1),density=1)
h1,bins1=np.histogram(bl1,bins=np.arange(min(bl1),max(bl1) + 1, 1))
h2,bins2=np.histogram(bl2,bins=np.arange(min(bl2),max(bl2) + 1, 1))
y1=stats.norm.pdf(bins1,np.mean(bl1),np.std(bl1))
y2=stats.norm.pdf(bins2,np.mean(bl2),np.std(bl2))
#plt.clf()
ax.plot(bins1[:-1],h1,'g',alpha=0.5,lw=3,label='CH1')
ax.plot(bins2[:-1],h2,'r',alpha=0.5,lw=3,label='CH2')
ax.plot(bins1,y1,'g--',lw=3,label='CH1, $\mu$ = %2.2f, $\sigma^2$ = %2.2f'%(np.mean(bl1),np.std(bl1)**2))
ax.plot(bins2,y2,'b',lw=3,label='CH2, $\mu$ = %2.2f, $\sigma^2$ = %2.2f'%(np.mean(bl2),np.std(bl2)**2))
ax.axis([mean2-5*sd2, mean2+5*sd2,min(h2),max(h2)])
ax.legend()
print('CH1:',np.mean(bl1),'CH2:',np.mean(bl2))
plt.savefig(os.path.join(plot_dir,'bl_analisis.png'))
plt.show()

