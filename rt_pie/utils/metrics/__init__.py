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

    min_error_hz = np.abs(np.min(diff_hz))
    max_error_hz = np.abs(np.max(diff_hz))
    mean_hz = np.mean(diff_hz)
    median_hz = np.median(diff_hz)
    mae_hz = mean_absolute_error(hz_true, hz_pred)
    std_dev_hz = np.std(diff_hz)
    quantile_05 = np.quantile(diff_hz, 0.05)
    quantile_95 = np.quantile(diff_hz, 0.95)
    rpa_hz = raw_pitch_accuracy_hz(hz_true, hz_pred, rpa_relative_tolerance)

    if print_output:
        l = 20
        f = '_'
        p = 2
        print(f"{'Min abs err [Hz] '.ljust(l, f)} {round(min_error_hz, p)}")
        print(f"{'Max abs err [Hz] '.ljust(l, f)} {round(max_error_hz, p)}")
        print(f"{'Mean err [Hz] '.ljust(l, f)} {round(mean_hz, p)}")
        print(f"{'Median [Hz] '.ljust(l, f)} {round(median_hz, p)}")
        print(f"{'MAE in [Hz] '.ljust(l, f)} {round(mae_hz, p)}")
        print(f"{'StdDev [Hz] '.ljust(l, f)} {round(std_dev_hz, p)}")
        print(f"{'5% quant err [Hz] '.ljust(l, f)} {round(quantile_05, p)}")
        print(f"{'95% quant err [Hz] '.ljust(l, f)} {round(quantile_95, p)}")
        print(f"{'RPA [Hz] '.ljust(l, f)} {round(rpa_hz, p)}")

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
