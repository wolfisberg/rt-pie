import numpy as np
import sounddevice as sd

from rt_pie import config


def process_microphone(args):
    raise NotImplementedError("Not yet implemented.")
    pitch_estimations = None
    plot = None
    audio_recording = None
    return pitch_estimations, plot, audio_recording


def callb(indata, frames, time, status):
    recording.extend(np.copy(indata))


def record(device):
    try:
        stream = sd.InputStream(
            device=device,
            samplerate=config.SAMPLE_RATE,
            channels=config.NUM_CHANNELS,
            blocksize=config.BLOCK_SIZE,
            callback=callb
        )
        with stream:
            print("Recording audio.")
            while True:
                pass
    except KeyboardInterrupt:
        print("Recording finished.")


recording = []


if __name__ == "__main__":
    audio_in = config.prompt_audio_device("")
    record(audio_in)
    audio_out = config.prompt_audio_device("")
    sd.play(recording, samplerate=config.SAMPLE_RATE, device=audio_out)
    status = sd.wait()
    print("Done.")
    exit(0)
