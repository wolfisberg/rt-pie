def calculate_unvoiced_detection_performance(f0_true, f0_pred, voice_cutoff=50):
    """Calculates metrics about how well the prediction performs in regard to unvoiced sections

    Args:
        f0_true: Ground truth pitch
        f0_pred: Pitch predictions
        voice_cutoff: Pitches below this value are considered unvoiced
            (default is 50)

    Returns:
        dict: A dictionary containing classification metrics

    Raises:
        ValueError: If the length of f0_true and f0_pred are unequal
        ValueError: If either f0_true or f0_pred contains values below 0
    """

    if len(f0_true) != len(f0_pred):
        raise ValueError("Input is of unequal length, cannot process.")

    tn = tp = fn = fp = 0
    for i in range(len(f0_true)):
        if f0_true[i] <= voice_cutoff and f0_pred[i] <= voice_cutoff:
            tp += 1
            continue
        if f0_true[i] > voice_cutoff and f0_pred[i] > voice_cutoff:
            tn += 1
            continue
        if f0_true[i] <= voice_cutoff and f0_pred[i] > voice_cutoff:
            fn += 1
            continue
        if f0_true[i] > voice_cutoff and f0_pred[i] <= voice_cutoff:
            fp += 1
            continue

        raise ValueError("Input contains value lesser than '0', cannot process")

    total = tp + fp + tn + fn
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    return {
        "total_samples": total,
        "tn_percentage": tn / total,
        "tp_percentage": tp / total,
        "fp_percentage": fp / total,
        "fn_percentage": fn / total,
        "true_percentage_unvoiced": (tp + fn) / total,
        "pred_percentage_unvoiced": (tp + fp) / total,
        "precision": precision,
        "recall": recall,
        "accuracy": (tp + tn) / total,
        "f1_score": f_score(precision, recall)
    }


def f_score(precision, recall, beta=1):
    return (1 + beta**2) * (precision * recall) / (beta**2 * precision + recall)
