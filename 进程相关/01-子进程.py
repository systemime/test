from multiprocessing import Pool
import requests

def fun(x):
    print(requests.get("http://47.100.114.188:60013/app01/index/").text)


if __name__ == "__main__":
    with Pool(1000) as p:
        print(p.map(fun, [i for i in range(1000)]))

