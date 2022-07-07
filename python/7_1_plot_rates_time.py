#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# 
# Analisis de los metadatos de lago. 
# Se analiza todo un directorio con archivos adquiridos con la rp.
# Al final se grafican los rates de los dos canales

import numpy as np
from scipy import stats, optimize
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import bz2, os, time

NBINS    = 32  # 32 bines por pulso
ADCBITS  = 14  # 14 bits
TIME_SEP = 8e-9   # 8 ns por punto
BASELINE = 0   # linea de base

data_dir = 'data/' # Directorio donde se encuentran los datos
proc_dir = 'proc/' # Directorio donde se guardan los datos procesados
plot_dir = 'plot/' # Directorio donde se guardaran las graficas
filename = input('Ingrese el nombre del archivo (*.dat o *.bz2) a procesar : ')
#filename= 'spnk_nogps_2021_07_23_03h00.dat.bz2'

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

r1 = np.array([])      #rate 1
r2 = np.array([])      #rate 2
tepoch  = np.array([]) #tiempo epoch

if filename.endswith("bz2"):
    with bz2.open(os.path.join(data_dir,filename),mode='rt',encoding='utf-8') as fd: 
        for line in fd: 
            sp=line.split() 
            if sp[0] == '#': 
                if sp[1]=='r1': 
                    r1 = np.append(r1,int(sp[2])) 
                if sp[1]=='r2':
                    r2 = np.append(r2,int(sp[2])) 
                if sp[1] == 'x':
                    if sp[2] == 'h': # GPS data
                        tepoch = np.append(tepoch,int(sp[5]))

else:
    with open(os.path.join(data_dir,filename),mode='rt',encoding='utf-8') as fd: 
        for line in fd: 
            sp=line.split() 
            if sp[0] == '#': 
                if sp[1]=='r1': 
                    r1 = np.append(r1,int(sp[2])) 
                if sp[1]=='r2':
                    r2 = np.append(r2,int(sp[2])) 
                if sp[1] == 'x':
                    if sp[2] == 'h': # GPS data
                        tepoch = np.append(tepoch,int(sp[5]))


r1ma=movingaverage(r1,10)
r2ma=movingaverage(r2,10)

# Convert to the correct format for matplotlib.
# mdate.epoch2num converts epoch timestamps to the right format for matplotlib
secs = mdate.epoch2num(tepoch)

#grafico de los rates por canal
fig,ax=plt.subplots(1,2,sharey=True,figsize=(10,5))
# Plot the date using plot_date rather than plot
l1, =ax[0].plot_date(secs,r1,'C2')
l2, =ax[0].plot_date(secs[:len(r1ma)],r1ma,'C1',label='Rates CH1')
ax[0].set_ylabel('Pulsos por segundo)')
ax[0].set_xlabel('Tiempo (s)')

# Choose your xtick format string
date_fmt = '%d-%m-%y %H:%M:%S'
# Use a DateFormatter to set the data to the correct format.
date_formatter = mdate.DateFormatter(date_fmt)
ax[0].xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()

l3,=ax[1].plot_date(secs,r2)
l4,=ax[1].plot_date(secs[:len(r2ma)],r2ma,label='Rates CH2')
# Choose your xtick format string
date_fmt = '%d-%m-%y %H:%M:%S'
# Use a DateFormatter to set the data to the correct format.
date_formatter = mdate.DateFormatter(date_fmt)
ax[1].xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()
ax[1].set_xlabel('Tiempo (s)')
ax[0].legend((l1,l2),('Rates Ch1',r'Promedio ({:3.1f}$\pm${:3.1f})'.format(r1.mean(),r1.std())))
ax[1].legend((l3,l4),('Rates Ch2',r'Promedio ({:3.1f}$\pm${:3.1f})'.format(r2.mean(),r2.std())))
fig.suptitle('Rates')
plt.savefig(os.path.join(plot_dir,'rates_ch1_ch2_ma.png'))
plt.show()
