import lstm
import crepe
import deepf0


def __print_model_summaries():
    block_sizes = [1024, 512, 256]
    for b in block_sizes:
        print(f"\n\nLSTM, block_size={b}")
        lstm.get_model_lstm(b).summary()
        print(f"\n\nCREPE, block_size={b}")
        crepe.get_model_crepe_without_time_component(b).summary()
        print(f"\n\nDEEPF0, block_size={b}")
        deepf0.get_model_deepf0_without_time_compoonent(b).summary()


if __name__ == "__main__":
    __print_model_summaries()
