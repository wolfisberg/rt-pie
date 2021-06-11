# RT PIE<br>Real Time PItch Estimator

[**pypi link**](https://pypi.org/project/rt-pie)

To demonstrate the predictions of the various models used throughout the thesis, a simple demonstration application was developed.
The demonstrator app is a python command line application. It comes pre-packaged with various deep learning models used in this thesis. The CREPE models as well as the DEEPF0_256 models are not available through this package, due to the 100MB package limitation on pypi.

The demonstrator app takes a WAVE audio file as input and saves a spectrogram including the pitch predictions to disk under the name `spectrogram.png`.

## Installation

    pip install rt_pie

## Usage

    rt_pie --help

#### Authors
Kaspar Wolfisberg<br>
Luca Di Lanzo

