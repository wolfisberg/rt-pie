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


def standard_deviation(true_cents, predicted_cents):
    diff = abs(predicted_cents - true_cents)
    avg = np.mean(diff)
    diff = np.square(diff - avg)
    total = np.sum(diff)
    return np.sqrt((total / (len(diff)-1)))


def mean_absolute_error(truth, prediction):
    diff = abs(truth - prediction)
    return np.mean(diff)
