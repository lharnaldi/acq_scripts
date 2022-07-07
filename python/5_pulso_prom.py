#!/usr/bin/python3 
# -*- encoding: utf-8 -*-
# Graficas del pulso promedio de los pulsos en los 
# canales adquiridos.
# Los archivos a analizar pueden tener la extensión .dat o .bz2

import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
import os

NBINS   = 32 # Número de bines por pulso
ADCBITS = 14 # Resolución del ADC
TIME_SEP= 8  # 8 ns por punto. Resolución temporal del ADC

data_dir = 'data/' # Directorio donde se encuentran los datos
plot_dir = 'plot/' # Directorio donde se guardaran las graficas
filename = input('Ingrese el nombre del archivo (*.dat o *.bz2) a procesar : ')
#filename = 'spnk_nogps_2021_07_23_03h00.dat.bz2'

ch1, ch2 = np.loadtxt(os.path.join(data_dir, filename), unpack=1, dtype=int)


ch1r = np.resize(ch1, (int(len(ch1)/NBINS), NBINS))
ch2r = np.resize(ch2, (int(len(ch2)/NBINS), NBINS))
ch1m = ch1r.mean(axis=0)
ch2m = ch2r.mean(axis=0)
t = np.linspace(0,8*NBINS,NBINS+1) 
fig, ax= plt.subplots(1, 1, figsize=(7, 6))
ax.step(t[:-1],(ch1m/2**(ADCBITS-1))*1e3, lw=2, where='post',label='CH1')
ax.step(t[:-1],(ch2m/2**(ADCBITS-1))*1e3, lw=2, where='post', label='CH2')
#ax.axvspan(50, 100, facecolor='g', alpha=0.3)
#plt.hlines(np.min(array_pulsos.mean(axis=0))/2,30,80)
ax.set_xlabel('Time (ns)', fontsize=14, fontname='monospace')
ax.set_ylabel('Amplitude (mV)', fontsize=14, fontname='monospace')
ax.grid()
ax.legend(fontsize=13)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.savefig(os.path.join(plot_dir,'pulso_promedio.pdf'))
plt.show()

##Para interpolar
#tck = interpolate.splrep(t[:-1], (ch1m/2**(ADCBITS-1))*1e3, s=0)
#xnew = np.arange(0, TIME_SEP*NBINS, 0.01) # this could be over the entire range, depending on what your data is
#ynew = interpolate.splev(xnew, tck, der=0)
#
##xnew = np.arange(0, 25*12, 0.01) # this could be over the entire range, depending on what your data is
##ynew = f(xnew)   # use interpolation function returned by `interp1d`
#
#fig = plt.figure()
#ax = fig.add_subplot(111)
#
##ax.set_title("Plot B vs H")
#ax.set_xlabel('Time (ns)', fontsize=14, fontname='monospace')
#ax.set_ylabel('Amplitude (mV)', fontsize=14, fontname='monospace')
#
#ax.plot(t[:-1],(ch1m/2**(ADCBITS-1))*1e3, 'bo', lw=2, label='Data')
#ax.plot(xnew, ynew, 'r--', label='Fit')
#
#leg = ax.legend(fontsize=13)
#plt.savefig('{}_pprom_fit.pdf'.format(fname_prefix))
#plt.show()
##save data
#np.savetxt('{}_pprom_tot.bz2'.format(fname_prefix),np.transpose([ch1m,ch2m]),fmt='%d')
#
##plt.savefig('pulso_promedio.png', size=(4,8))
##plt.savefig('pulso_promedio.png')

