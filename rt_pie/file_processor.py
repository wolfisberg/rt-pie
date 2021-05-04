import librosa
import numpy as np

from rt_pie import config
from rt_pie import fitted_models


def process_file(args):
    audio, _ = librosa.load(args.input, sr=config.SAMPLE_RATE, mono=True)
    if args.pitch is not None:
        # todo: make pitch reading more generic (T[0] is for ptdbtug)
        # todo: to make use of true pitch, we need hopsize and offset as well
        pitch_true = np.genfromtxt(args.pitch, delimiter=" ").T[0]
        raise NotImplementedError("Not yet implemented.")
    model = fitted_models.get_model(args.model)

    pitch_estimations = None
    spectrogram = None
    return pitch_estimations, spectrogram
