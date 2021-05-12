import os
import sounddevice as sd


SAMPLE_RATE = 16000
NUM_CHANNELS = 1
BLOCK_SIZE = 1024
BATCH_SIZE = 32
MODELS_BASE_PATH = os.path.join("rt_pie", "serialized_models")


def __check_device_selection(devices, selection):
    try:
        device_number = int(selection)
        if device_number in range(0, len(devices)):
            return device_number
        raise ValueError()
    except Exception as e:
        print(f"Invalid input, expected number between 0 and {len(devices) - 1}.")
        exit(-1)


def prompt_audio_device(msg):
    audio_devices = sd.query_devices()
    print(f"{msg} Available audio devices:")
    if len(audio_devices) < 2:
        print(f"Using the only available audio device:")
        print(audio_devices[0]["name"])
        return audio_devices[0]
    print(audio_devices)
    selection = input('Choose your audio device: ')
    print("\n")
    return __check_device_selection(audio_devices, selection)
