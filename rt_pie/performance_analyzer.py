import random
import pickle
import numpy as np

from rt_pie.fitted_models import models
from rt_pie import args, process_file_input

__ITERATIONS = 10
__RES_FILE = "res_10.pkl"
# __RES_FILE = None


def __compare_prediction_performance(iterations):
    shuffled = models.copy()
    random.shuffle(shuffled)
    result = {}
    for i in range(iterations):
        for m in shuffled:
            args.model = m.name
            res = process_file_input(args)
            times = res["p_times"]
            if m.name in result:
                result[m.name] = np.append(result[m.name], times)
            else:
                result[m.name] = times
    return result


def main():
    if __RES_FILE is None:
        res = __compare_prediction_performance(__ITERATIONS)
    else:
        with open(__RES_FILE, 'rb') as f:
            res = pickle.load(f)

    with open(f"res_{__ITERATIONS}.pkl", "wb") as f:
        pickle.dump(res, f)

    __print_performance_stats(res, __ITERATIONS)


def __print_performance_stats(time_dict, iterations):
    lines = []
    for k, v in time_dict.items():
        sum = round(np.sum(v) / iterations / 1000, 2)
        mean = round(np.mean(v), 2)
        dev = round(np.std(v), 2)
        lines.append(f"model: {k}, sum: {sum}s, mean: {mean}ms, dev: {dev}ms")

    lines.sort()
    for li in lines:
        print(li)


if __name__ == "__main__":
    main()
