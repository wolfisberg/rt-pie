import time
import random

from rt_pie import arg_parser, file_processor, microphone_processor
from rt_pie import config
from rt_pie.fitted_models import models


timestamp = time.strftime("%Y%m%d-%H%M%S")
args = arg_parser.parse_args()


def process_file_input(args):
    pitch_estimations, prediction_times, plot = file_processor.process_file(args)
    if args.output_pitch:
        write_pitch(pitch_estimations)
    if args.output_plot:
        write_plot(plot)
    return prediction_times


def process_microphone_input():
    pitch_estimations, plot, audio_recording = microphone_processor.process_microphone(args)
    if args.output_pitch:
        write_pitch(pitch_estimations)
    if args.output_plot:
        write_plot(plot)
    if args.output_audio:
        write_audio(audio_recording)


def write_pitch(pitches):
    with open(f"{timestamp}_pitch_estimations.f0", 'w') as file:
        file.write("\n".join(pitches))


def write_plot(plot):
    raise NotImplementedError("Not yet implemented.")


def write_audio(audio):
    # librosa.output.write_wav(f"{timestamp}_recording.wav", audio, config.SAMPLE_RATE, norm=False)
    raise NotImplementedError("Not yet implemented.")


def main():
    if args.input:
        # compare_prediction_performance()
        process_file_input(args)
    else:
        process_microphone_input()


def compare_prediction_performance():
    shuffled = models.copy()
    random.shuffle(shuffled)
    result = {}
    for i in range(3):
        for m in shuffled:
            args.model = m.name
            times = process_file_input(args)
            if m.name in result:
                result[m.name].append(times)
            else:
                result[m.name] = [times]
    print("done")



if __name__ == '__main__':
    main()
