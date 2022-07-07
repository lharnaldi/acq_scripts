#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Analisis de los metadatos. 
# Se analiza todo un directorio con archivos adquiridos con la rp.

# v 5
# #
# # This is a LAGO raw data file, version 5
# # It contains the following data:
# #   <N1> <N2>        : line with values of the 2 ADC for a triggered pulse
# #   # t <C> <V>      : end of a trigger
# #                      gives the channel trigger (<C>: 3 bit mask) and 125 MHz clock count (<V>) of the trigger time
# #   # c <C>          : internal trigger counter
# #   # r1 <V>         : pulse rate at channel 1
# #   # r2 <V>         : pulse rate at channel 2
# #   # x f <V>        : 125 MHz frequency
# #   # x t <V>        : temperature value
# #   # x p <V>        : pressure value
# #   # x h <HH:MM:SS> <DD/MM/YYYY> <S> : GPS time (every new second, last number is seconds since EPOCH)
# #   # x s <T> C <P> hPa <A> m : temperature <T>, pressure <P> and altitude (from pressure) <A>
# #   # x g <LAT> <LON> <ALT>   : GPS data - latitude, longitude, altitude
# #   # x v <HV1> <HV2>         : HV voltages for channels 1 and 2
# #   # x b <B1> <B2> <B3>      : baselines (NOT IMPLEMENTED IN LAGO)
# # In case of error, an unfinished line will be finished by # E @@@
# # Followed by a line with # E <N> and the error message in human readable format, where <N> is the error code:
# #   # E 1 : read timeout of 2 seconds
# #   # E 2 : too many buffer reading tries
# #   # E 3 : unknown word from FPGA
# #
# # Current registers setting
# #
# x c T1 200
# x c T2 8190
# x c HV1 1799.7 mV
# x c HV2 7.7 mV
# x c SC1 1
# x c SC2 1
# # This file was started on lago
# # Machine local time was Thu Jan  1 20:11:11 1970
# # WARNING, there is no GPS, using PC time
# #

import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import os, bz2

NBINS    = 32   # 32 bines por pulso
ADCBITS  = 14   # 14 bits
TIME_SEP = 8e-9 # 8 ns por punto
BASELINE = 0    # linea de base

data_dir = 'data/' # Directorio donde se encuentran los datos
proc_dir = 'proc/' # Directorio donde se guardan los datos procesados
plot_dir = 'plot/' # Directorio donde se guardaran las gráficas
filename = input('Ingrese el nombre del archivo (*.dat o *.bz2) a procesar : ')
#filename= 'spnk_nogps_2021_07_23_03h00.dat.bz2'

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

#thefile = bz2.BZ2File('lago/' + filename,'r')
#thefile = bz2.BZ2File(filename,'r')
#with open(filename,'r') as thefile:
#    lines=thefile.readlines()
thefile=bz2.BZ2File(os.path.join(data_dir, filename),"r")
#thefile=open(os.path.join(data_dir, filename),"r")

for line in thefile:
    sp = line.decode('utf-8').split()
    #sp = line.split()
    if sp[0] == '#':
        #print(sp)
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
        if sp[1] == 'r1': # x r1 <V>       : pulse rate at channel 1
            r1 = np.append(r1,int(sp[2]))
        if sp[1] == 'r2': # x r2 <V>       : pulse rate at channel 2
            r2 = np.append(r2,int(sp[2]))
            

thefile.close()
np.savetxt(os.path.join(proc_dir,'mtd_' + filename[:-4]),np.transpose([sadq,tepoch,clk_freq,r1,r2,tempi,pres,hv1,hv2,temp1,temp2]),fmt=('%d %d %d %d %d %.2f %.2f %.2f %.2f %.2f %.2f')) 
np.savetxt(os.path.join(proc_dir,'dt_' + filename[:-4]),np.transpose([cntri,tch,dt]),fmt=('%d %d %d')) 

#fig,ax=plt.subplots(figsize=(7,6))
#h1,b1=np.histogram(dt,density=1)
#y1=stats.norm.pdf(b1,dt.mean(),dt.std())
#ax.plot(b1[:-1],h1,'r*',lw=2,label='Diferencia temporal')
#ax.plot(b1,y1,'g--',lw=1,label='$\Delta$ t, $\mu$ = {:2.2f}, $\sigma^2$ = {:2.2f}'.format(dt.mean(),dt.
#std()**2))
#plt.savefig(os.path.join(plot_dir,'diferencia_tempora.pdf'))
#plt.show()
#
##otra forma de leer el archivo
##line=thefile.readline()
##while line:
##    print(line)
##    line=thefile.readline()
##
##thefile.close()
#
##grafico de los rates por canal
#fig,ax=plt.subplots(figsize=(7,6))
#ax.plot(r1,'r-*',label='Rates CH1')
#ax.plot(r2,'b-^',label='Rates CH2')
#plt.legend()
#plt.savefig(os.path.join(plot_dir,'rates_ch1_ch2.pdf'))
#plt.show()
#
##grafico de las HV por canal
#fig,ax=plt.subplots(figsize=(7,6))
#ax.plot(hv1,'r-*',label='HV CH1')
#ax.plot(hv2,'b-^',label='HV CH2')
#plt.legend()
#plt.savefig(os.path.join(plot_dir,'hv_ch1_ch2.pdf'))
#plt.show()
