import os
import logging
from tensorflow.keras.models import load_model

from rt_pie import config


class FittedModel:
    def __init__(self, name, block_size, time_component, desc, path):
        self.name = name
        self.block_size = block_size
        self.time_component = time_component
        self.desc = desc
        self.path = path

    def help_formatting(self):
        return f"    {self.name.ljust(14, ' ')}{self.desc}\n"


models = [
    FittedModel("LSTM_1024", 1024, True, "LSTM, block size 1024, hop size 512",
                os.path.join(config.MODELS_BASE_PATH, "lstm_1024_512_e100_model.hdf5")),
    FittedModel("LSTM_512", 512, True, "LSTM, block size 512, hop size 256",
                os.path.join(config.MODELS_BASE_PATH, "lstm_512_256_e065_model.hdf5")),
    FittedModel("LSTM_256", 256, True, "LSTM, block size 256, hop size 128",
                os.path.join(config.MODELS_BASE_PATH, "lstm_256_128_e092_model.hdf5")),
    FittedModel("CREPE_1024", 1024, False, "CREPE, block size 1024, hop size 512",
                os.path.join(config.MODELS_BASE_PATH, "crepe_1024_512_e100_model.hdf5")),
    FittedModel("CREPE_512", 512, False, "CREPE, block size 512, hop size 256",
                os.path.join(config.MODELS_BASE_PATH, "crepe_512_256_e100_model.hdf5")),
    FittedModel("CREPE_256", 256, False, "CREPE, block size 256, hop size 128",
                os.path.join(config.MODELS_BASE_PATH, "crepe_256_128_e084_model.hdf5")),
    FittedModel("DEEPF0_1024", 1024, False, "DEEPF0, block size 1024, hop size 512",
                os.path.join(config.MODELS_BASE_PATH, "deepf0_1024_512_e087_model.hdf5")),
    FittedModel("DEEPF0_512", 512, False, "DEEPF0, block size 512, hop size 256",
                os.path.join(config.MODELS_BASE_PATH, "deepf0_512_256_e048_model.hdf5")),
    FittedModel("DEEPF0_256", 256, False, "DEEPF0, block size 256, hop size 128",
                os.path.join(config.MODELS_BASE_PATH, "deepf0_256_128_e091_model.hdf5"))
]


def get_model(model):
    try:
        model = next((m for m in models if m.name == model), models[0])
        return model, load_model(model.path)
    except Exception as e:
        logging.error("Could not find specified model.")
        logging.error(e)
        exit(-1)
