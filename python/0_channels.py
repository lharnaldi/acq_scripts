#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Graficas de los pulsos en los canales adquiridos.
# Los archivos a analizar pueden tener la extensión .dat o .bz2

import numpy as np
import matplotlib.pyplot as plt
import os

N=5000 # Número de puntos a graficar

data_dir = 'data/' # Directorio donde se encuentran los datos
plot_dir = 'plot/' # Directorio donde se guardaran las graficas
filename = input('Ingrese el nombre del archivo (*.dat o *.bz2) a procesar : ')
#filename= 'spnk_nogps_2021_07_23_03h00.dat.bz2' # Nombre del archivo a graficar

ch1, ch2 = np.loadtxt(os.path.join(data_dir, filename), unpack=1, dtype=int)

x=np.linspace(0,N,N-1)
fig,ax = plt.subplots(nrows=1, ncols=1, figsize=(11,7))

ax.step(x,ch1[:N-1], 'r-.',lw=1, label='CH1')
ax.step(x,ch2[:N-1], 'b.-',lw=1, label='CH2')

#ax.plot(ch1, 'r-o',lw=1, label='CH1')
#ax.plot(ch2, 'b.-',lw=1, label='CH2')

ax.legend(fontsize=11)
ax.grid()
ax.set_xlim(0,1500)
ax.set_ylabel('Amplitude (ADC)',fontsize=14)
ax.set_xlabel('Time (ADC.bin)',fontsize=14)

plt.savefig(os.path.join(plot_dir,'pulses_{}.png'.format(filename)))
plt.show()

