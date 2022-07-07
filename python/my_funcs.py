#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import os, re
import numpy as np

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

def cumsum_sma(array, period):
    ret = np.cumsum(array, dtype=float)
    ret[period:] = ret[period:] - ret[:-period]
    return ret[period - 1:] / period

#tomado de https://stackoverflow.com/questions/38208700/matplotlib-plot-lines-with-colors-through-colormap
#Esto es para hacer graficos con una barra lateral que represente cambios de
#valores en las lineas
def multiline(xs, ys, c, ax=None, **kwargs):
    """Plot lines with different colorings

    Parameters
    ----------
    xs : iterable container of x coordinates
    ys : iterable container of y coordinates
    c : iterable container of numbers mapped to colormap
    ax (optional): Axes to plot on.
    kwargs (optional): passed to LineCollection

    Notes:
        len(xs) == len(ys) == len(c) is the number of line segments
        len(xs[i]) == len(ys[i]) is the number of points for each line (indexed by i)

    Returns
    -------
    lc : LineCollection instance.
    """

    # find axes
    ax = plt.gca() if ax is None else ax

    # create LineCollection
    segments = [np.column_stack([x, y]) for x, y in zip(xs, ys)]
    lc = LineCollection(segments, **kwargs)

    # set coloring of line segments
    #    Note: I get an error if I pass c as a list here... not sure why.
    lc.set_array(np.asarray(c))

    # add lines to axes and rescale
    #    Note: adding a collection doesn't autoscalee xlim/ylim
    ax.add_collection(lc)
    ax.autoscale()
    return lc

def get_Q(f,i,q,N):
    '''
    Obtiene el Q de un resonador. El criterio para decidir el ancho de banda es
    el de -3 dB. 
    Parametros:
    N : es la cantidad de puntos a considerar para hacer el filtro moving
    average
    f : es el vector de frecuencia
    i,q : son los vectores de datos en fase y cuadratura
    '''
    #moving average y normalizo
    ii=movingaverage(i,N)
    qi=movingaverage(q,N)

    max_val = max(np.sqrt(ii**2+qi**2))
    s21     = 20*np.log10(np.sqrt(ii**2+qi**2)/max_val)
    s21_min = np.argmin(s21)
    fr      = f[s21_min] # freq de resonancia
    g       = np.argwhere(s21<s21.max()-20*np.log10(2))
    if g.size == 0:
        return 0.0
    else:
        bw      = f[g][-1]-f[g][0]
        Q       = fr/bw
        return float(Q)

#Esto está en https://stackoverflow.com/questions/19366517/sorting-in-python-how-to-sort-a-list-containing-alphanumeric-values
#forma de usarlo
#>>> list1 = ["1", "100A", "342B", "2C", "132", "36", "302F"]
#>>> list1.sort(key=natural_sort_key)
#>>> list1
#['1', '2C', '36', '100A', '132', '302F', '342B']

_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in
            re.split(_nsre, s)]

#First, we build a list of the file names. isfile() is used to skip directories;
#it can be omitted if directories should be included. Then, we sort the list
#in-place, using the modify date as the key.
#https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
def getfiles(dirpath):
    '''esta funcion retorna la lista de archivos
       de un directorio ordenados por tiempo de
       creación'''
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

def listfiles(dirpath):
    dirFiles = os.listdir(dirpath) #list of directory files
    dirFiles.sort(key=lambda f: int(filter(str.isdigit, f)))
    return diFiles

