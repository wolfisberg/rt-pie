import sounddevice as sd
import librosa
import numpy as np
import time

from rt_pie import fitted_models
from rt_pie.rt_pie_lib import converters
from rt_pie import stream_processor
from rt_pie import config


def process_file(args):
    model, fitted_model = fitted_models.get_model(args.model)

    audio, _ = librosa.load(args.input, sr=config.SAMPLE_RATE, mono=True)
    audio_len = len(audio) / config.SAMPLE_RATE
    num_blocks = len(audio) // model.block_size
    audio = np.array(audio, dtype=float)[:num_blocks * model.block_size].reshape((-1, model.block_size))

    # __play_file(args, model.block_size)

    p = []
    time_elapsed = [time.perf_counter_ns()]

    if model.time_component:
        audio = [np.array([a]) for a in audio]

    for a in audio:
        p.append(*fitted_model.predict(np.array([a])))
        time_elapsed.append(time.perf_counter_ns())

    if not model.time_component:
        p_cent = converters.convert_bin_to_local_average_cents(np.array(p))
        p_hz = converters.convert_cent_to_hz(p_cent)
    else:
        p_hz = np.array(p).flatten()

    time_elapsed = __convert_elapsed_time(time_elapsed)

    print(f"len audio input: {round(audio_len, 2)}s")
    print(f"model: {model.name}, mean ptime: {round(time_elapsed[-1] / len(time_elapsed), 2)}ms, total ptime: {round(np.sum(time_elapsed) / 1e3, 2)}s\n")
    plot = None
    return {
        "p_hz": p_hz,
        "p_times": time_elapsed,
        "audio_duration": audio_len,
        "plot": plot
    }


def __convert_elapsed_time(time_elapsed):
    times = np.array(time_elapsed)
    times = (times - np.min(times)) / 1e6
    res = []
    for i in range(1, len(times)):
        res.append(times[i] - times[i - 1])
    return np.array(res)


def __output_callback():
    print("test")


def __play_file(args, block_size):
    try:
        if args.device_prompt:
            config.prompt_audio_device("Pick audio device for playback.")
        stream = sd.OutputStream(
            samplerate=config.SAMPLE_RATE,
            channels=config.NUM_CHANNELS,
            blocksize=block_size,
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
