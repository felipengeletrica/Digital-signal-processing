import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np


i=0
f,ax = plt.subplots(2)

# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0, 44000)
ax[0].set_ylim(-65535, 65635)
ax[0].set_title("Raw Audio Signal")
# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0, 44000)
ax[1].set_ylim(-100, 100)
ax[1].set_title("Fast Fourier Transform")
# Show the plot, but without blocking updates
plt.tight_layout()
plt.subplots_adjust(hspace=100)
plt.pause(0.01)


def main():



    #i = 0
    #f, ax = plt.subplots(2)

    # Prepare the Plotting Environment with random starting values
    # x = np.arange(10000)
    #     # y = np.random.randn(10000)

    fs, data = wavfile.read('audio2/audio_original.wav') # load the data
    #fs, data = wavfile.read('audio2/grupo02.wav')  # load the data

    #fs, data = wavfile.read('audio/wavTones_60Hz_-6dBFS_7000Hz_-18dBFS_3s.wav')  # load the data

    ax[0].set_xlim(0, len(data))

    # get and convert the data to float
    audio_data = np.fromstring(data, np.int16)
    # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
    # and make sure it's not imaginary
    dfft = 10. * np.log10(abs(np.fft.rfft(audio_data)))



    # Force the new data into the plot, but without redrawing axes.
    li.set_xdata(np.arange(len(audio_data)))
    li.set_ydata(audio_data)
    li2.set_xdata(np.arange(len(dfft)))
    li2.set_ydata(dfft)
    plt.show()


    # a = data  # this is a two channel soundtrack, I get the first track
    # b = [(ele / 2 ** 16.) * 2 - 1 for ele in data]  # this is 8-bit track, b is now normalized on [-1,1)
    # c = fft(b)  # calculate fourier transform (complex numbers list)
    # d = len(c) / 2  # you only need half of the fft list (real signal symmetry)
    #
    # x = c
    # y = c
    #
    # li, = ax[0].plot(c, c)
    # ax[0].set_xlim(0, 1000)
    # ax[0].set_ylim(-5000, 5000)
    # ax[0].set_title("Raw Audio Signal")
    # # Plot 1 is for the FFT of the audio
    # li2, = ax[1].plot(x, y)
    # ax[1].set_xlim(0, 5000)
    # ax[1].set_ylim(-100, 100)
    # ax[1].set_title("Fast Fourier Transform")
    # # Show the plot, but without blocking updates
    # plt.tight_layout()
    # plt.subplots_adjust(hspace=0.3)
    # plt.pause(0.01)
    # plt.show()


    # x = len(data)
    #
    # # Plot 0 is for raw audio data
    # li, = ax[0].plot(x, y)
    # ax[0].set_xlim(0, 1000)
    # ax[0].set_ylim(-5000, 5000)
    # ax[0].set_title("Raw Audio Signal")
    # # Plot 1 is for the FFT of the audio
    # li2, = ax[1].plot(x, y)
    # ax[1].set_xlim(0, 5000)
    # ax[1].set_ylim(-100, 100)
    # ax[1].set_title("Fast Fourier Transform")
    # # Show the plot, but without blocking updates
    # plt.tight_layout()
    # plt.subplots_adjust(hspace=0.3)
    # plt.pause(0.01)
    # plt.show()

    #
    # # fs, data = wavfile.read('audio2/audio_original.wav') # load the data
    # fs, data = wavfile.read('audio2/grupo02.wav')  # load the data
    # a = data  # this is a two channel soundtrack, I get the first track
    # b = [(ele / 2 ** 16.) * 2 - 1 for ele in data]  # this is 8-bit track, b is now normalized on [-1,1)
    # c = fft(b)  # calculate fourier transform (complex numbers list)
    # d = len(c) / 2  # you only need half of the fft list (real signal symmetry)
    # plt.plot(abs(c[:(d - 1)]), 'r')
    # plt.show()


if __name__ == '__main__':
    main()
