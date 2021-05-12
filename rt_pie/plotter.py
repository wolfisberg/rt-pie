import librosa
import matplotlib.pyplot as plt
import numpy as np

from rt_pie import process_file_input, args
from rt_pie import config
from rt_pie.fitted_models import models


def get_predictions():
    selection = ["lstm_512", "crepe_1024", "deepf0_1024"]
    selection = [m for m in models if m.name.lower() in selection]
    predictions = {}
    for m in selection:
        args.model = m.name
        res = process_file_input(args)
        predictions[m.name] = res

    audio, _ = librosa.load(args.input, sr=config.SAMPLE_RATE, mono=True)
    return predictions, audio


def plot_predictions(predictions, audio ):
    # f0 = np.genfromtxt(pitch_file, delimiter=" ")  # f0 ground truth in semitones
    # f0 = conversions.convert_cent_to_hz(100 * f0, 10)  # convert cents (100*semitone) to hz
    # f0_time = np.array([i / 50 for i in range(len(f0))])  # create time axis for f0

    # plt.xlim(left=0.5, right=2)
    plt.ylim([0, 500])
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    # fig.colorbar(colormap).set_label("Intensity [dB]")

    spec, freqs, times, colormap = plt.specgram(audio, Fs=config.SAMPLE_RATE)

    for k, v in predictions.items():
        p_hz = v["p_hz"]
        p_times = np.linspace(0, len(audio) / config.SAMPLE_RATE, len(p_hz))
        plt.plot(p_times, p_hz, label=k)

    plt.legend()
    format = "svg"
    # plt.savefig(os.path.join(output_path, f'spectrogram.{format}'), format=format)
    plt.show()
    # plt.savefig(os.path.join(output_path, f'spectrogram.{format}'), format=format)


if __name__ == "__main__":
    predictions, audio = get_predictions()
    plot_predictions(predictions, audio)


