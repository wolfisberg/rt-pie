from rt_pie import arg_parser, file_processor, microphone_processor


def process_file_input(args):
    pitch_estimations, spectrogram = file_processor.process_file(args)


def process_microphone_input(args):
    pitch_estimations, spectrogram, audio_recording = microphone_processor.process_microphone(args)


def main():
    args = arg_parser.parse_args()
    if args.input:
        process_file_input(args)
    else:
        process_microphone_input(args)


if __name__ == '__main__':
    main()
