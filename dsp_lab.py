import struct
from enum import Enum

from sympy.core.tests.test_sympify import numpy

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
        self.audio_samples_chunk = 65535

        #filter parameter
        self.fs = 500

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

    def time_domain(self, audio_samples, title='Spectrogram of wav audio'):
        """
        Plot time domain samples
        """
        try:

            if self.audio_samples is None:
                raise (IOError('No samples for save'))

            plt.subplot(211)
            plt.title(title)
            plt.plot(audio_samples)
            plt.xlabel('Sample')
            plt.ylabel('Amplitude')
            plt.subplot(212)
            plt.specgram(audio_samples, Fs=self.audio_samples_rate)
            plt.xlabel('Time')
            plt.ylabel('Frequency')
            plt.grid()
            plt.show()
            plt.savefig('time_domain.png')
            return True

        except Exception as e:
            raise e
            return False

    def frequency_domain(self, audio_samples, title='Fast Fourier Transform'):
        """
        Process FFT
        """
        try:

            if len(audio_samples) == 0:
                raise (IOError('No samples for processing'))

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
                sample_rate=self.audio_samples_rate)

            print("frequencies:", frequencies)

            x_asis_data = freq_bins
            y_asis_data = magnitude_values

            pylab.plot(x_asis_data, y_asis_data, color='blue')  # plotting the spectrum

            pylab.title(title)
            pylab.xlabel('Freq (Hz)')
            pylab.ylabel('|Magnitude - Voltage  Gain / Loss|')
            pylab.grid()
            pylab.show()
            pylab.savefig('frequency_domain.png')

        except Exception as e:
            raise e

    def filter(self, type: filter_type):
        """
        Process filters labs
        :param type:
        :return:
        """
        try:
            filtred_data = []

            #Attenuation
            data_atennuantion = self.audio_samples / 40


            if type is filter_type.DSP_LAB_FILTER_NOTCH:
                print("Selected filter NOTCH")
                filtred_data = self.filters.notchFilter(data_atennuantion)

            elif type is filter_type.DSP_LAB_FILTER_BUTTERWORTH:
                print("Selected filter Butterworth")
                filtred_data = self.filters.butter_bandstop_filter(data_atennuantion, self.audio_samples_rate)

            else:
                print('Unknown filter')
                filtred_data = None

            #Calculate original and add new gain
            media = 0
            for data in self.audio_samples:
                media += data

            media = (media/self.audio_number_samples)

            media_filter = 0
            for data in filtred_data:
                media_filter += data

            media_filter = (media_filter / self.audio_number_samples)

            # Calculates audio meas
            gain = (media/media_filter) / 2

            #add new gain audio
            filtred_data = filtred_data * gain

        except Exception as e:
            filtred_data = None
            raise e

        finally:
            return filtred_data

    def root_square_mean_error(self, original_data, filtred_data):
        """
         Calculate Root Square Mean Error
        :param original_data:
        :param filtred_data:
        :return:
        """
        rmse = 0.00
        try:
            rmse = self.filters.root_mean_square_error(original_data, filtred_data)

            normalized_chunk = rmse / self.audio_samples_chunk

        except Exception as e:
            raise e

        return normalized_chunk