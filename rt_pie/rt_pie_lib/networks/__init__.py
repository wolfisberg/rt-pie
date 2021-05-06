import os
import sys

import crepe


def convert_checkpoints_to_model(checkpoints_path, model):
    model.load_weights(checkpoints_path)
    split = os.path.splitext(checkpoints_path)
    model.save(f"{split[0]}_model{split[1] if len(split) > 0 else ''}")


if __name__ == "__main__":
    # model = crepe.get_model_crepe_without_time_component(1024)
    model = crepe.get_model_crepe_without_time_component(512)
    convert_checkpoints_to_model(sys.argv[1], model)
