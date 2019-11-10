from enum import Enum
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

from functions_and_filters import *


class filter_type(Enum):

    DSP_LAB_FILTER_NOTCH = 0
    DSP_LAB_FILTER_BUTTERWORTH = 1


class dsp_lab(object):

    def __init__(self):
        """
        Initial values
        """

        # Audio context
        self.audio_samples = []
        self.audio_number_samples = None
        self.audio_samples_rate = None
        self.audio_duration = 0

        # Create instance for filter
        self.filters = functions_and_filters()

    def open(self, filename):
        """
        Open audio file
        :param filename: file name
        :return: Samples and audio rate
        """
        try:
            audio_samples, sample_rate = soundfile.read(filename, dtype='int16')
            number_samples = len(audio_samples)
            duration = round(number_samples / sample_rate, 2)

            self.audio_samples = audio_samples
            self.audio_number_samples = number_samples
            self.audio_samples_rate = sample_rate
            self.audio_duration = duration

        except Exception as e:
            print(e)
            return None, None, None

        return audio_samples, sample_rate, duration

    def save(self, filename, audio_samples):
        """
         Save files
        :param filename:
        :param audio_samples:
        :return: True or False
        """
        try:
            if self.audio_samples_rate is None:
                raise(IOError('No samples for save'))
            soundfile.write(
                filename,
                audio_samples.astype(np.int16),
                self.audio_samples_rate)

            return True

        except Exception as e:
            raise e
            return False

    def time_domain(self, audio_samples):
        """
        Plot time domain samples
        """
        try:

            if self.audio_samples is None:
                raise (IOError('No samples for save'))

            plt.subplot(211)
            plt.title('Spectrogram of wav audio')
            plt.plot(audio_samples)
            plt.xlabel('Sample')
            plt.ylabel('Amplitude')
            plt.subplot(212)
            plt.specgram(audio_samples, Fs=self.audio_samples_rate)
            plt.xlabel('Time')
            plt.ylabel('Frequency')
            plt.grid()
            plt.show()
            return True

        except Exception as e:
            raise e
            return False

    def frequency_domain(self, audio_samples):
        """
        Process FFT
        """
        try:

            if len(audio_samples) == 0:
                raise (IOError('No samples for pprocessing'))

            # FFT calculation
            fft_data = scipy.fft(audio_samples)
            print('FFT Length: ', len(fft_data))
            print('FFT data: ', fft_data)

            # list of possible frequencies bins
            freq_bins = arange(self.audio_number_samples) * self.audio_samples_rate / self.audio_number_samples

            freq_bins = freq_bins[range(self.audio_number_samples // 2)]
            normalization_data = fft_data / self.audio_number_samples
            magnitude_values = normalization_data[range(len(fft_data) // 2)]
            magnitude_values = np.abs(magnitude_values)

            indices = self.filters.findPeak(magnitude_values=magnitude_values, noise_level=1)
            frequencies = self.filters.extractFrequency(
                indices=indices,
                number_samples=self.audio_number_samples,
                sample_rate= self.audio_samples_rate)

            print("frequencies:", frequencies)

            x_asis_data = freq_bins
            y_asis_data = magnitude_values

            pylab.plot(x_asis_data, y_asis_data, color='blue')  # plotting the spectrum

            pylab.xlabel('Freq (Hz)')
            pylab.ylabel('|Magnitude - Voltage  Gain / Loss|')
            pylab.grid()
            pylab.show()

        except Exception as e:
            raise e

    def filter(self, type: filter_type):
        """
        Process filters labs
        :param type:
        :return:
        """
        try:

            if type is filter_type.DSP_LAB_FILTER_NOTCH:
                print("Selected filter NOTCH")
                return self.filters.notchFilter(self.audio_samples)

            elif type is filter_type.DSP_LAB_FILTER_BUTTERWORTH:
                print("Selected filter Butterworth")
                return self.filters.butter_bandstop_filter(self.audio_samples, self.audio_samples_rate)

            else:
                print('Unknown filter')
                return None
        except Exception as e:
            raise e
