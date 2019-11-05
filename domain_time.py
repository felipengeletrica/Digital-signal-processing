import matplotlib.pyplot as plt
from scipy.io import wavfile # get the api
from scipy.fftpack import fft
from pylab import *


def f(filename):
    fs, data_1 = wavfile.read('audio2/audio_original.wav')  # load the data
    fs, data_2 = wavfile.read('audio2/grupo02.wav') # load the data
    #
    # a = data_1 # this is a two channel soundtrack, I get the first track
    # b=[(ele/2**16)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    # c = fft(b) # create a list of complex number
    # d = len(c)/2  # you only need half of the fft list
    # plt.plot(abs(c[:(d-1)]),'r')
    # savefig(filename+'.png', bbox_inches='tight')
    # plt.show()
    #
    plt.figure(figsize=(100, 20))
    #plt.plot(data_1, label='Original signal')
    plt.plot(data_2, label='Original signal')
    savefig('signal_grupo_2.png', bbox_inches='tight')
    plt.show()

import glob
files = glob.glob('audio2/*.wav')
for ele in files:
    f(ele)
quit()