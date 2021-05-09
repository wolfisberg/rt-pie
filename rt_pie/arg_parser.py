import argparse

from rt_pie import fitted_models


def parse_args():
    parser = argparse.ArgumentParser(prog="rt_pie",
                                     description="RT_PIE - Real Time PItch Estimator"
                                                 + "\nPython script for real time pitch estimations\non the base of"
                                                 + " neural networks.",
                                     formatter_class=argparse.RawTextHelpFormatter)

    general_opts = parser.add_argument_group("general (optional)")
    general_opts.add_argument("-d", "--device-prompt", help="prompt which audio devices should be used",
                              action="store_true")

    input_opts = parser.add_argument_group("input (optional)", description="specify the input source to use"
                                                                           + "\ndefault: microphone")
    input_opts.add_argument("-i", "--input", help="provide a .wav file to be used as input\ninstead of the"
                                                  " microphone", metavar="WAV_FILE")
    input_opts.add_argument("-t", "--pitch", help="provide a text file containing true\npitch values to receive perf"
                                                  "ormance\nmetrics about the pitch estimations\nrequires: -i option",
                            metavar="PITCH_FILE")

    analysis_opts = parser.add_argument_group("analysis (optional)",
                                              description="specify the degree of analysis that is put out"
                                                          + "\ndefault: spectrogram of audio including pitch estimations")
    analysis_opts.add_argument("-m", "--model", help="choose model for pitch estimations\nchoices:\n"
                                                     + "".join([m.help_formatting() for m in fitted_models.models]),
                               metavar="MODEL", choices=[m.name for m in fitted_models.models])
    analysis_opts.add_argument("-S", "--no-spectrogram", help="plot pitch estimations without spectrogram"
                                                              "\nimproves latency", action="store_true")
    analysis_opts.add_argument("-P", "--no-plot", help="do not show plot\nimproves latency",
                               action="store_true")

    output_opts = parser.add_argument_group("output (optional)", description="specify persistence of the output"
                                                                             + "\ndefault: stdout only")
    output_opts.add_argument("-o", "--output-audio", help="writes recorded audio out to file"
                                                          + "\nincompatibility: -f option", action="store_true")
    output_opts.add_argument("-e", "--output-pitch", help="saves pitch estimations file", action="store_true")
    output_opts.add_argument("-p", "--output-plot", help="saves plot to file\nincompatibility: -P option",
                             action="store_true")

    args = parser.parse_args()
    check_invalid_args(parser, args)
    set_default_args(args)
    return args


def check_invalid_args(parser, args):
    if args.pitch is not None and args.input is None:
        parser.error("The pitch option (-p) requires the input option (-i)")
    if args.output_plot and args.no_plot:
        parser.error("The output-plot option (-p) is incompatible with the no-plot option (-P)")
    if args.output_audio and args.input is not None:
        parser.error("The output-audio option (-o) is incompatible with the input option (-i)")


def set_default_args(args):
    if args.model is None:
        args.model = fitted_models.models[0].name


if __name__ == "__main__":
    parse_args()
