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


class functions_and_filters(object):

    def __init__(self):
        pass

    def findPeak(self, magnitude_values, noise_level=2000):
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

    def extractFrequency(self, indices, freq_threshold=2, number_samples=0, sample_rate=0):

        extracted_freqs = []

        freq_bins = arange(number_samples) * sample_rate / number_samples

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

    def notchFilter(self, audio_samples):
        f0 = 500.0  # Frequency to be removed from signal
        fs = 44100  # Sample frequency (Hz)
        w = f0 / (fs / 2)
        q = 1  # Quality Factor
        # b, a = signal.iirnotch(w, q)
        b = [0.9993962108935, -1.993722787953, 0.9993962108935]
        a = [1, -1.993722787953, 0.998792421787]

        y = signal.lfilter(b, a, audio_samples)
        return y

    def butter_bandstop_filter(self, audio_samples, audio_samples_rate):

        nyq = (audio_samples_rate / 2)
        low = 490 / nyq
        high = 510 / nyq
        order = 3
        i, u = signal.butter(order, [low, high], btype='bandstop')
        y = lfilter(i, u, audio_samples)
        return y

    def lowPassFilter(self, audio_samples, audio_samples_rate):

        w = 450 / (audio_samples_rate / 2)
        b, a = signal.butter(10, w, 'low')
        y = signal.filtfilt(b, a, audio_samples)
        return y
