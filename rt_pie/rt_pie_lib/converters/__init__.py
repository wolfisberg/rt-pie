import numpy as np
import mir_eval
from scipy.signal import argrelextrema


def convert_cent_to_hz(cent, f_ref=10.0):
    return f_ref * 2 ** (cent / 1200.0)


def convert_hz_to_cent(hertz, f_ref=10.0):
    return mir_eval.melody.hz2cents(hertz, f_ref)


def convert_semitone_to_hz(semi, f_ref=10.0):
    return convert_cent_to_hz(100 * semi, f_ref)


def convert_bin_to_weighted_average_cents(label, octaves=6, cents_per_bin=20, hz_lower_bound=32.7):
    classifier_lowest_cent = convert_hz_to_cent(np.array([hz_lower_bound]))[0]
    classifier_total_bins = int((1200 / cents_per_bin) * octaves)
    classifier_cents = np.linspace(
        0, (classifier_total_bins - 1) * cents_per_bin, classifier_total_bins) + classifier_lowest_cent

    if label.ndim == 1:
        product_sum = np.sum(label * classifier_cents)
        weight_sum = np.sum(label)
        return product_sum / weight_sum
    if label.ndim == 2:
        product_sum = np.dot(label, classifier_cents)
        weight_sum = np.sum(label, axis=1)
        return product_sum / weight_sum
    raise Exception("Label should be either 1d or 2d ndarray.")


def convert_bin_to_local_average_cents(salience, center=None):
    """
    find the weighted average cents near the argmax bin
    """
    if not hasattr(convert_bin_to_local_average_cents, 'cents_mapping'):
        # the bin number-to-cents mapping
        convert_bin_to_local_average_cents.cents_mapping = (
                np.linspace(0, 7180, 360) + 1997.3794084376191)
    if salience.ndim == 1:
        center = int(np.argmax(salience))
        start = max(0, center - 4)
        end = min(len(salience), center + 5)
        salience = salience[start:end]
        product_sum = np.sum(
            salience * convert_bin_to_local_average_cents.cents_mapping[start:end])
        weight_sum = np.sum(salience)
        return product_sum / weight_sum
    if salience.ndim == 2:
        return np.array([convert_bin_to_local_average_cents(salience[i, :]) for i in
                         range(salience.shape[0])])
    raise Exception("Label should be either 1d or 2d ndarray.")


def convert_bin_to_local_average_cents_lowest_maxima(salience, center=None, maxima_order=10, maxima_minval=0.2, tolerance=0.1):
    """
    find the weighted average cents near the argmax bin todo
    """
    if salience.ndim == 1:
        maxima = argrelextrema(salience, np.greater, order=maxima_order)[0]
        maxima = [(x, convert_cent_to_hz(convert_bin_to_local_average_cents(__create_maximum_bin(x))))
                  for x in maxima if salience[x] >= maxima_minval]
        if len(maxima) > 1:
            success, idx = __try_find_f0_in_maxima(maxima, tolerance=tolerance)
            if success:
                salience = np.zeros(360)
                salience[maxima[idx][0]] = 1
        return convert_bin_to_local_average_cents(salience, center=center)
    raise Exception("Label should be 1d ndarray.")


def __create_maximum_bin(index):
    b = np.zeros(360)
    b[index] = 1
    return b


def __try_find_f0_in_maxima(maxima, tolerance=0.1):
    maxima.sort(key=lambda x: x[1])
    for i in range(len(maxima) - 1):
        max_current = maxima[i][1]
        max_next = maxima[i + 1][1]
        rel_diff = abs(max_current * 2 - max_next) / max_next
        if rel_diff <= tolerance:
            return True, i
    return False, None
