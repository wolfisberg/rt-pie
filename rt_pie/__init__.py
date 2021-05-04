import time
import librosa

from rt_pie import arg_parser, file_processor, microphone_processor, config


timestamp = time.strftime("%Y%m%d-%H%M%S")
args = arg_parser.parse_args()


def process_file_input():
    pitch_estimations, plot = file_processor.process_file(args)
    if args.output_pitch:
        write_pitch(pitch_estimations)
    if args.output_plot:
        write_plot(plot)


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
    librosa.output.write_wav(f"{timestamp}_recording.wav", audio, config.SAMPLE_RATE, norm=False)
    raise NotImplementedError("Not yet implemented.")


def main():
    if args.input:
        process_file_input()
    else:
        process_microphone_input()


if __name__ == '__main__':
    main()
