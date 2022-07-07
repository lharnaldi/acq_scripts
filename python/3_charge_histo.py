#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Graficas de los histogramas de carga de los pulsos en los 
# canales adquiridos.
# Los archivos a analizar pueden tener la extensión .dat o .bz2

import numpy as np
import matplotlib.pyplot as plt
import os, bz2

NBINS    = 32  # 32 bines por pulso
ADCBITS  = 14  # 14 bits
TIME_SEP = 8   # 8 ns por punto
BL1= -0.00769541358124141 # baseline 1. Se obtiene de correr el script 1_bl_ana.py
BL2= 0.01146251889398908  # baseline 2. Se obtiene de correr el script 1_bl_ana.py

data_dir = 'data/' # Directorio donde se encuentran los datos
plot_dir = 'plot/' # Directorio donde se guardaran las graficas
filename = input('Ingrese el nombre del archivo (*.dat o *.bz2) a procesar : ')
#filename = 'spnk_nogps_2021_07_23_03h00.dat.bz2'

ch1, ch2 = np.loadtxt(os.path.join(data_dir, filename), unpack=1, dtype=int)

#para que tengan el largo correcto
ch1b=np.resize(ch1,ch1.size - len(ch1)%NBINS)
ch2b=np.resize(ch2,ch2.size - len(ch2)%NBINS)

#para sacar los histogramas de carga
h1=np.array([(ch1b[i:i+NBINS]-BL1).sum() for i in np.arange(0,len(ch1b),NBINS)])
h2=np.array([(ch2b[i:i+NBINS]-BL2).sum() for i in np.arange(0,len(ch2b),NBINS)])

#n1,bins1=np.histogram(h1,bins='auto',density=1)
#n2,bins2=np.histogram(h2,bins='auto',density=1)
#n1,bins1=np.histogram(h1,bins=np.arange(min(h1),max(h1) + 1, 1),density=1)
#n2,bins2=np.histogram(h2,bins=np.arange(min(h2),max(h2) + 1, 1),density=1)
n1,bins1=np.histogram(h1,bins=np.arange(min(h1),max(h1) + 1, 1))
n2,bins2=np.histogram(h2,bins=np.arange(min(h2),max(h2) + 1, 1))
#n1,bins1=np.histogram(h1,8192)
#n2,bins2=np.histogram(h2,8192)

fig, ax= plt.subplots(1, 1, figsize=(7, 6))
ax.grid()

#ax.loglog(bins1[:-1],n1, color='red', lw=2, label='CH1')
#ax.loglog(bins2[:-1],n2, color='blue', lw=2, label='CH2')
ax.semilogy(bins1[:-1],n1, color='red', lw=2, label='CH1')
ax.semilogy(bins2[:-1],n2, color='blue', lw=2, label='CH2')
ax.legend()

ax.set_xlabel('ADC bins',fontsize=14, fontname='monospace')
ax.set_ylabel('# of entries',fontsize=14, fontname='monospace')
#ax.set_ylim(1,0.8e4)
#ax.set_xlim(50,400)
# this is an inset axes over the main axes
#a = plt.axes([.65, .6, .2, .2], alpha=0.02)
#a = plt.axes([.55, .55, .32, .32])
##a.loglog(hcar2.mean(axis=0), color='blue', lw=2, label='CH2')
##a.loglog(hcar2.mean(axis=0), color='blue', label='CH2')
#a.semilogx(bins1[:-1],n1,bins2[:-1],n2)
#a.semilogx(bins2[:-1],n2, color='blue', lw=2, label='CH2')
##a.set_xlabel('Charge [ADC.bin]',fontsize=14, fontname='monospace')
##a.set_ylabel('Counts',fontsize=14, fontname='monospace')
##a.set_ylim(1,2e4)
##a.set_xlim(50,400)
#a.grid()
#plt.savefig('histo_carga.png')
plt.savefig(os.path.join(plot_dir,'charge_histo.pdf'))
plt.show()

#Para guardar el histograma generado
#f=open('hi.dat','w')
#
#for i in arange(0,len(bins1)):
#    f.write(str(i))
#    f.write(str(' '))
#    f.write(str(bins1[i]))
#    f.write(str(' '))
#    f.write(str(h1[i]) + '\n')
#
#
#f.close()

