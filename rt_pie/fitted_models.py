import os
import logging
from tensorflow.keras.models import load_model


class FittedModel:
    def __init__(self, name, desc, path):
        self.name = name
        self.desc = desc
        self.path = path

    def help_formatting(self):
        return f"    {self.name.ljust(14, ' ')}{self.desc}\n"


models = [
    FittedModel("CREPE_1024", "CREPE, block size 1024, hop size 512",
                os.path.join("..", "tmp_data", "models", "crepe_1024_512_e100_model.hdf5")),
    FittedModel("CREPE_512", "CREPE, block size 512, hop size 256",
                os.path.join("..", "tmp_data", "models", "crepe_512_256_e100_model.hdf5")),
    FittedModel("three", "model three", os.path.join("..", "tmp_data", "models", "does_not_exist"))
]


def get_model(model):
    try:
        return load_model(next((m.path for m in models if m.name == model), models[0].path))
    except Exception as e:
        logging.error("Could not find specified model.")
        logging.error(e)
        exit(-1)
