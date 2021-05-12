import pickle


__RES_PATH = "res_03.pkl"

with open(__RES_PATH,'rb') as f:
    res = pickle.load(f)
    print(res)


