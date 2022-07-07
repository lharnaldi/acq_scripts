#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Graficas de los histogramas de amplitud de los pulsos en los 
# canales adquiridos.
# Los archivos a analizar pueden tener la extensión .dat o .bz2

import numpy as np
import matplotlib.pyplot as plt
import os, bz2

NBINS    = 32  # 32 bines por pulso
ADCBITS  = 14  # 14 bits
TIME_SEP = 8   # 8 ns por punto
BASELINE = 0   # linea de base

data_dir = 'data/' # Directorio donde se encuentran los datos
plot_dir = 'plot/' # Directorio donde se guardaran las graficas
filename = input('Ingrese el nombre del archivo (*.dat o *.bz2) a procesar : ')
#filename = 'spnk_nogps_2021_07_23_03h00.dat.bz2'

ch1, ch2 = np.loadtxt(os.path.join(data_dir, filename), unpack=1, dtype=int)

n1,bins1=np.histogram(ch1,bins=np.arange(min(ch1),max(ch1) + 1, 1))
n2,bins2=np.histogram(ch2,bins=np.arange(min(ch2),max(ch2) + 1, 1))

fig, ax= plt.subplots(1, 1, figsize=(7, 6))
ax.grid()
#ax.semilogx(bins1[:-1],n1,bins2[:-1],n2)
#ax.loglog(bins1[:-1],n1, color='red', label='CH1')
#ax.loglog(bins2[:-1],n2, color='blue', label='CH2')
ax.semilogy(bins1[:-1],n1, color='red', label='CH1')
ax.semilogy(bins2[:-1],n2, color='blue', label='CH2')
#ax.plot(bins1[:-1],n1, color='red', lw=2, label='CH1')
#ax.plot(bins2[:-1],n2, color='blue', lw=2, label='CH2')
#ax.semilogx(hcar2.mean(axis=0), color='blue', lw=2, label='CH2')
ax.set_xlabel('ADC bins',fontsize=14, fontname='monospace')
ax.set_ylabel('log(#)',fontsize=14, fontname='monospace')
plt.legend()
#ax.set_ylim(1,0.8e4)
#ax.set_xlim(50,400)
# this is an inset axes over the main axes
#a = plt.axes([.65, .6, .2, .2], axisbg='y', alpha=0.02)
#a = plt.axes([.55, .55, .32, .32])
#a.loglog(hcar2.mean(axis=0), color='blue', lw=2, label='CH2')
#a.loglog(hcar2.mean(axis=0), color='blue', label='CH2')
#a.loglog(bins1[:-1],n1,bins2[:-1],n2,bins3[:-1],n3)
#a.loglog(bins2[:-1],n2, color='blue', lw=2, label='CH2')
#a.set_xlabel('Charge [ADC.bin]',fontsize=14, fontname='monospace')
#a.set_ylabel('Counts',fontsize=14, fontname='monospace')
#a.set_ylim(1,2e4)
#a.set_xlim(50,400)
#a.grid()
#plt.savefig('histo_peak.png')
plt.savefig(os.path.join(plot_dir,'amp_histo.png'))
plt.show()

