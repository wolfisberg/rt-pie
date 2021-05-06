import sounddevice as sd
import librosa
import numpy as np
import tensorflow as tf

from rt_pie import config
from rt_pie import fitted_models
from rt_pie.rt_pie_lib import converters


def process_file(args):
    audio, _ = librosa.load(args.input, sr=config.SAMPLE_RATE, mono=True)
    num_blocks = len(audio) // config.BLOCK_SIZE
    audio = np.array(audio, dtype=float)[:num_blocks * config.BLOCK_SIZE].reshape((-1, config.BLOCK_SIZE))
    # play_file(audio)

    if args.pitch is not None:
        raise NotImplementedError("Not yet implemented.")
        # todo: make pitch reading more generic (T[0] is for ptdbtug)
        # todo: to make use of true pitch, we need hopsize and offset as well
        pitch_true = np.genfromtxt(args.pitch, delimiter=" ").T[0]

    model = fitted_models.get_model(args.model)
    # print(model.summary())
    # tf.keras.utils.plot_model(model, show_shapes=True)
    p = model.predict(audio[160:192])
    # pitch_estimations = [model.predict(a) for a in audio]

    p_cent = converters.convert_bin_to_local_average_cents(p)
    p_hz = converters.convert_cent_to_hz(p_cent)
    spectrogram = None
    return pitch_estimations, spectrogram


def play_file(audio):
    # todo: ask user for device
    stream = sd.OutputStream(
        # device=device,
        samplerate=config.SAMPLE_RATE,
        channels=config.NUM_CHANNELS,
        blocksize=config.BLOCK_SIZE,
        # callback=callb
    )
    with stream:
        print("Playing audio.")
        while True:
            pass
    print("Recording finished.")



