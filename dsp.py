from numpy import array, diff, where, split
from scipy import arange
import soundfile
import numpy as np
import scipy
import pylab
import copy
import matplotlib
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import lfilter
from scipy.signal import iirfilter
from wave import *

matplotlib.use('tkagg')


def findPeak(magnitude_values, noise_level=2000):
    splitter = 0
    # zero out low values in the magnitude array to remove noise (if any)
    magnitude_values = np.asarray(magnitude_values)
    low_values_indices = magnitude_values < noise_level  # Where values are low
    magnitude_values[low_values_indices] = 0  # All low values will be zero out

    indices = []

    flag_start_looking = False

    both_ends_indices = []

    length = len(magnitude_values)
    for i in range(length):
        if magnitude_values[i] != splitter:
            if not flag_start_looking:
                flag_start_looking = True
                both_ends_indices = [0, 0]
                both_ends_indices[0] = i
        else:
            if flag_start_looking:
                flag_start_looking = False
                both_ends_indices[1] = i
                # add both_ends_indices in to indices
                indices.append(both_ends_indices)

    return indices


def extractFrequency(indices, freq_threshold=2):
    extracted_freqs = []

    for index in indices:
        freqs_range = freq_bins[index[0]: index[1]]
        avg_freq = round(np.average(freqs_range))

        if avg_freq not in extracted_freqs:
            extracted_freqs.append(avg_freq)

    # group extracted frequency by nearby=freq_threshold (tolerate gaps=freq_threshold)
    group_similar_values = split(extracted_freqs, where(diff(extracted_freqs) > freq_threshold)[0] + 1)

    # calculate the average of similar value
    extracted_freqs = []
    for group in group_similar_values:
        extracted_freqs.append(round(np.average(group)))

    print("freq_components", extracted_freqs)
    return extracted_freqs


def notchFilter(audio_samples):
    f0 = 500.0  # Frequency to be removed from signal
    fs = 44100  # Sample frequency (Hz)
    w = f0 / (fs / 2)
    q = 1  # Quality Factor
    # b, a = signal.iirnotch(w, q)
    b = [0.9993962108935, -1.993722787953, 0.9993962108935]
    a = [1, -1.993722787953, 0.998792421787]
    # Frequency response
    freq, h = signal.freqz(b, a, fs=fs)
    # Plot
    fig, ax = plt.subplots(2, 1, figsize=(8, 6))
    ax[0].plot(freq, 20 * np.log10(abs(h)), color='blue')
    ax[0].set_title("Frequency Response")
    ax[0].set_ylabel("Amplitude (dB)", color='blue')
    ax[0].set_xlim([0, 2000])
    ax[0].set_ylim([-25, 10])
    ax[0].grid()
    ax[1].plot(freq, np.unwrap(np.angle(h)) * 180 / np.pi, color='green')
    ax[1].set_ylabel("Angle (degrees)", color='green')
    ax[1].set_xlabel("Frequency (Hz)")
    ax[1].set_xlim([0, 2000])
    ax[1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
    ax[1].set_ylim([-90, 90])
    ax[1].grid()
    plt.show()

    y = signal.lfilter(b, a, audio_samples)
    return y


def butter_bandstop_filter(data):
    nyq = 22050
    low = 470 / nyq
    high = 530 / nyq
    order = 4
    i, u = signal.butter(order, [low, high], btype='bandstop')
    y = lfilter(i, u, data)
    return y


def lowPassFilter(audio_samples):
    w = 450 / (44100 / 2)
    b, a = signal.butter(10, w, 'low')
    y = signal.filtfilt(b, a, audio_samples)
    return y


if __name__ == '__main__':
    file_path = 'audio2/grupo02.wav'
    print('Open audio file path:', file_path)

    audio_samples1, sample_rate = soundfile.read(file_path, dtype='int16')
    number_samples = len(audio_samples1)
    print('Audio Samples: ', audio_samples1)
    print('Number of Sample', number_samples)
    print('Sample Rate: ', sample_rate)
    audio_samples = notchFilter(audio_samples1)
    # audio_samples = audio_samples1
    soundfile.write('output.wav', audio_samples.astype(np.int16), 44100)

    # duration of the audio file
    duration = round(number_samples / sample_rate, 2)
    print('Audio Duration: {0}s'.format(duration))

    # list of possible frequencies bins
    freq_bins = arange(number_samples) * sample_rate / number_samples
    print('Frequency Length: ', len(freq_bins))
    print('Frequency bins: ', freq_bins)

    #     # FFT calculation
    fft_data = scipy.fft(audio_samples)
    print('FFT Length: ', len(fft_data))
    print('FFT data: ', fft_data)

    freq_bins = freq_bins[range(number_samples // 2)]
    normalization_data = fft_data / number_samples
    magnitude_values = normalization_data[range(len(fft_data) // 2)]
    magnitude_values = np.abs(magnitude_values)

    indices = findPeak(magnitude_values=magnitude_values, noise_level=200)
    frequencies = extractFrequency(indices=indices)
    print("frequencies:", frequencies)

    x_asis_data = freq_bins
    y_asis_data = magnitude_values

    pylab.plot(x_asis_data, y_asis_data, color='blue')  # plotting the spectrum

    pylab.xlabel('Freq (Hz)')
    pylab.ylabel('|Magnitude - Voltage  Gain / Loss|')
    pylab.show()