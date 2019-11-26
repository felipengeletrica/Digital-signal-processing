##Digital Signal Processing - IIR filter to remove interfering signal
This App was designed to remove interfering 500Hz signal (tone) in a given audio file.

###Requirements:
•	Python 3.7

•	Numpy

•	Scipy

•	Matplotlib

###To run

**A.** Execute program in a terminal `python signal_processing_lab.py`

**B.** Select option `0` to open an audio file to be analyzed. Then write the audio filename and click enter.

**C.** Select option `2` to print a spectrogram of the audio. After analyze you need to close the image view in order to proceed.

**D.** Select option `3` to print the FFT (fast fourier transform) of the audio. 

**E.** Select option `4` to design a filter to be applied in the original audio. After that you can select `0` to a notch filter or `1` to a Butterworth filter.

**F.** After the selection the type of the filter you are going to see its frequency response.

**G.** After the selection the type of the filter you are going to see its frequency response. After analyze it you need to close the image in order to proceed.

**H.** Type an output name for the filtered audio. The app expects it to be a `.wav` file.

**I.** Select option `5` to calculate the RMSE. Then type the filename of the original file and after the filtered audio filename. The app will print in the console the RMSE.


