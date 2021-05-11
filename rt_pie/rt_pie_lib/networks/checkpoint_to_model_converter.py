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
    file_name = sys.argv[1].lower()
    block_size = int(sys.argv[2])
    if "lstm" in file_name:
        model = lstm.get_model_lstm(block_size)
    elif "crepe" in file_name:
        model = crepe.get_model_crepe_without_time_component(block_size)
    elif "deepf0" in file_name:
        model = deepf0.get_model_deepf0_without_time_compoonent(block_size)
    else:
        raise RuntimeError("Unable to determine model type from file name.")

    convert_checkpoints_to_model(file_name, model)
