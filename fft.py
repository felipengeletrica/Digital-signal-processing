# !/usr/bin/env python
# -*- coding: latin-1 -*-

# Copyright (c) 2019, Felipe Vargas <felipeng.eletrica@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.

import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile  # get the api

from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
import matplotlib.pyplot as plt


def main():

    path = 'audio/'

    #wav_filename = path + 'file_example_WAV_1MG.wav'
    wav_filename = path + "wavTones_60Hz_-6dBFS_7000Hz_-18dBFS_3s.wav"
    samplerate, data = wavfile.read(wav_filename)

    total_samples = len(data)
    limit = int((total_samples / 2) - 1)

    fft_abs = abs(fft(data))

    freqs = fftfreq(total_samples, 1 / samplerate)

    # plot the frequencies
    plt.plot(freqs[:limit], fft_abs[:limit])
    plt.title("Frequency spectrum of %s" % wav_filename)
    plt.xlabel('frequency in Hz')
    plt.ylabel('amplitude')
    plt.show()


if __name__ == '__main__':
    main()