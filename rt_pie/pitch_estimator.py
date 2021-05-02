"""
todo
load trained model
load audio file
format audio to match model
make prediction
if path_f0:
    compare predictions with f0
"""


import numpy as np
import sounddevice as sd


def __check_device_selection(devices, selection):
    try:
        device_number = int(selection)
        if device_number in range(0, len(devices)):
            return device_number
        raise ValueError()
    except Exception as e:
        print(f"Invalid input, expected number between 0 and {len(devices) - 1}.")
        exit(-1)


def get_audio_device():
    audio_devices = sd.query_devices()
    print("Available audio devices:")
    if len(audio_devices) < 2:
        print(f"Using the only available audio device:")
        print(audio_devices[0]["name"])
        return audio_devices[0]
    print(audio_devices)
    selection = input('Choose your audio device: ')
    print("\n")
    return __check_device_selection(audio_devices, selection)


def callb(indata, frames, time, status):
    recording.extend(np.copy(indata))


def record(device):
    try:
        stream = sd.InputStream(
            device=device,
            samplerate=_SR,
            channels=_CHANNELS,
            blocksize=_BLOCK_SIZE,
            callback=callb
        )
        with stream:
            print("Recording audio.")
            while True:
                pass
    except KeyboardInterrupt:
        print("Recording finished.")


_SR = 16000
_CHANNELS = 1
_BLOCK_SIZE = 1024
recording = []


if __name__ == "__main__":
    audio_in = get_audio_device()
    record(audio_in)
    audio_out = get_audio_device()
    sd.play(recording, samplerate=_SR, device=audio_out)
    status = sd.wait()
    print("Done.")
    exit(0)
