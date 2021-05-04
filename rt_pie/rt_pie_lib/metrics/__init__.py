import numpy as np


def __rpa_tolerance_function_cents(cent_true, cent_pred, cent_tolerance):
    return abs(cent_true - cent_pred) <= cent_tolerance


def __rpa_tolerance_function_relative(cent_true, cent_pred, tolerance):
    return abs(cent_true - cent_pred) <= (cent_true * tolerance)


def __raw_pitch_accuracy(cents_true, cents_pred, tolerance_function, tolerance):
    counter_true = 0
    counter_false = 0
    for i in range(len(cents_true)):
        if tolerance_function(cents_true[i], cents_pred[i], tolerance):
            counter_true += 1
        else:
            counter_false += 1
    if counter_true > 0:
        result = counter_true / (counter_true + counter_false) * 100
    else:
        result = 0
    return result


def raw_pitch_accuracy_cent(cents_true, cents_pred, cent_tolerance=50):
    return __raw_pitch_accuracy(cents_true, cents_pred, __rpa_tolerance_function_cents, cent_tolerance)


def raw_pitch_accuracy_hz(hz_true, hz_pred, relative_tolerance=0.02):
    return __raw_pitch_accuracy(hz_true, hz_pred, __rpa_tolerance_function_relative, relative_tolerance)


def mean_absolute_error(truth, prediction):
    diff = abs(truth - prediction)
    return np.mean(diff)


def get_hz_metrics(hz_true, hz_pred, rpa_relative_tolerance=0.02, print_output=False):
    diff_hz = hz_true - hz_pred

    min_error_hz = np.min(np.abs(diff_hz))
    max_error_hz = np.max(np.abs(diff_hz))
    mean_hz = np.mean(diff_hz)
    median_hz = np.median(diff_hz)
    mae_hz = mean_absolute_error(hz_true, hz_pred)
    std_dev_hz = np.std(diff_hz)
    quantile_05 = np.quantile(diff_hz, 0.05)
    quantile_95 = np.quantile(diff_hz, 0.95)
    rpa_hz = raw_pitch_accuracy_hz(hz_true, hz_pred, rpa_relative_tolerance)

    if print_output:
        l = 20
        r = 6
        f = '_'
        p = 2
        print(__format_prop_for_print("Min abs err [Hz]", min_error_hz))
        print(__format_prop_for_print("Max abs err [Hz]", max_error_hz))
        print(__format_prop_for_print("Mean err [Hz]", mean_hz))
        print(__format_prop_for_print("Median [Hz]", median_hz))
        print(__format_prop_for_print("MAE [Hz]", mae_hz))
        print(__format_prop_for_print("StdDev [Hz]", std_dev_hz))
        print(__format_prop_for_print("5% quant err [Hz]", quantile_05))
        print(__format_prop_for_print("95% quant err [Hz]", quantile_95))
        print(__format_prop_for_print("RPA [Hz]", rpa_hz))

    return {
        "min_error_hz": min_error_hz,
        "max_error_hz": max_error_hz,
        "mean_error_hz": mean_hz,
        "median_error_hz": median_hz,
        "mae_hz": mae_hz,
        "std_dev_hz": std_dev_hz,
        "quantile_05": quantile_05,
        "quantile_95": quantile_95,
        "rpa_hz": rpa_hz,
    }


def __format_prop_for_print(name, value, filler="_", decimal_places=2, length_name=20, length_value=8):
    return f"{(name + ' ').ljust(length_name, filler)}{(' ' + str(round(value, decimal_places))).rjust(length_value, filler)}"
