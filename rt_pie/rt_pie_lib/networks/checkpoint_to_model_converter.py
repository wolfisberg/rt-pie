import os
import sys

import lstm
import crepe
import deepf0


def convert_checkpoints_to_model(checkpoints_path, model):
    model.load_weights(checkpoints_path)
    split = os.path.splitext(checkpoints_path)
    model.save(f"{split[0]}_model{split[1] if len(split) > 0 else ''}")


if __name__ == "__main__":
    if "crepe" in sys.argv[1].lower():
        model = crepe.get_model_crepe_without_time_component(sys.argv[3])
    elif "lstm" in sys.argv[1].lower():
        model = lstm.get_model_lstm(sys.argv[3])
    elif "deepf0" in sys.argv[1].lower():
        model = deepf0.get_model_deepf0_without_time_compoonent(sys.argv[3])
    else:
        raise RuntimeError("Unable to determine model type from file name.")
    convert_checkpoints_to_model(sys.argv[2], model)
