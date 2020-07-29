from multiprocessing import Pool


def fun(x):
    return x


if __name__ == "__main__":
    with Pool(5) as p:
        print(p.map(fun, [1, 2, 3]))

