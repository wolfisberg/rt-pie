import sounddevice as sd
import librosa
import numpy as np
import time

from rt_pie import config
from rt_pie import fitted_models
from rt_pie.rt_pie_lib import converters
from rt_pie import stream_processor


def process_file(args):
    __play_file(args)
    audio, _ = librosa.load(args.input, sr=config.SAMPLE_RATE, mono=True)
    num_blocks = len(audio) // config.BLOCK_SIZE
    audio = np.array(audio, dtype=float)[:num_blocks * config.BLOCK_SIZE].reshape((-1, config.BLOCK_SIZE))

    model = fitted_models.get_model(args.model)
    p = []
    time_elapsed = [time.perf_counter_ns()]
    for a in audio:
        p.append(*model.predict(np.array([a])))
        time_elapsed.append(time.perf_counter_ns())

    time_elapsed = np.array(time_elapsed)
    time_elapsed = (time_elapsed - np.min(time_elapsed)) / 1e6

    p_cent = converters.convert_bin_to_local_average_cents(np.array(p))
    p_hz = converters.convert_cent_to_hz(p_cent)
    spectrogram = None
    return p_hz, spectrogram


def __output_callback():
    print("test")


def __play_file(args):
    try:
        if args.device_prompt:
            config.prompt_audio_device("Pick audio device for playback.")
        stream = sd.OutputStream(
            samplerate=config.SAMPLE_RATE,
            channels=config.NUM_CHANNELS,
            blocksize=config.BLOCK_SIZE,
            callback=stream_processor.process_output_stream
        )
        with stream:
            print("Playback started.")
            while True:
                pass
    except KeyboardInterrupt:
        print('Playback stopped.')
    except Exception as e:
        print("Error during playback.")
        print(e)
        exit(-1)
