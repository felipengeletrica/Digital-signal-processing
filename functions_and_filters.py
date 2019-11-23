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
        """
        Find Signal Peak
        :param magnitude_values:
        :param noise_level:
        :return:
        """
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

    def change_volume(self, audio_samples, level):
        """
        Change audio volume
        :param audio_samples:
        :param level:
        :return:
        """
        new_audio_samples = audio_samples - 20

        return new_audio_samples

    def extractFrequency(self, indices, freq_threshold=2, number_samples=0, sample_rate=0):
        """

        :param indices:
        :param freq_threshold:
        :param number_samples:
        :param sample_rate:
        :return:
        """
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
        """
        Notch filter
        :param audio_samples:
        :return:
        """
        f0 = 500.0  # Frequency to be removed from signal
        fs = 44100  # Sample frequency (Hz)
        w = f0 / (fs / 2)
        q = 50  # Quality Factor
        b, a = signal.iirnotch(w, q)

        y = signal.lfilter(b, a, audio_samples)

         # Frequency response
        freq, h = signal.freqz(b, a, fs=fs)
         # Plot
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))
        ax[0].plot(freq, 20 * np.log10(abs(h)), color='blue')
        ax[0].set_title("Frequency Response")
        ax[0].set_ylabel("Amplitude (dB)", color='blue')
        ax[0].set_xlim([0, fs/2])
        ax[0].set_ylim([-5, 5])
        ax[0].grid()
        ax[1].plot(freq, np.unwrap(np.angle(h)) * 180 / np.pi, color='green')
        ax[1].set_ylabel("Angle (degrees)", color='green')
        ax[1].set_xlabel("Frequency (Hz)")
        ax[1].set_xlim([0, fs/2])
        ax[1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
        ax[1].set_ylim([-90, 90])
        ax[1].grid()
        plt.show()
        return y

    def butter_bandstop_filter(self, audio_samples, audio_samples_rate):
        """
        Butterworth Band Stop filter
        :param audio_samples:
        :param audio_samples_rate:
        :return:
        """
        nyq = (audio_samples_rate / 2)
        low = 490 / nyq
        high = 510 / nyq
        order = 3
        i, u = signal.butter(order, [low, high], btype='bandstop')
        y = lfilter(i, u, audio_samples)
        return y

    def lowPassFilter(self, audio_samples, audio_samples_rate):
        """
        Low Filter Butterworth
        :param audio_samples:
        :param audio_samples_rate:
        :return:
        """
        w = 450 / (audio_samples_rate / 2)
        b, a = signal.butter(10, w, 'low')
        y = signal.filtfilt(b, a, audio_samples)
        return y

    def root_mean_square_error(self, original_data, filtred_data):
        """
        Root Mean Square Filter
        :param original_data:
        :param filtred_data:
        :return:
        """
        if len(original_data) != len(filtred_data):
            raise (IOError('The two dice are not the same size.'))
        mse = self.square_mean_error(original_data, filtred_data)

        smse = np.sqrt(mse)
        return smse

    @staticmethod
    def square_mean_error(original_data, filtred_data):
        """
        Square Mean Error
        :param original_data:
        :param filtred_data:
        :return:
        """
        if len(original_data) != len(filtred_data):
            raise (IOError('The two dice are not the same size.'))
        sum = 0
        n = len(original_data)
        diferrence = 0.0000000000

        for i in range(0, n):

            diferrence = original_data[i] - filtred_data[i]
            square_difference = diferrence ** 2
            sum = sum + square_difference

        mse = sum / n
        return mse
