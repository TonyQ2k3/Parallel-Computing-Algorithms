# Tính chuỗi fibonacci ở vị trí lớn
# Local runtime:
#   n = 1000 => 0.2338 seconds
#   n = 2000 => 0.3575 seconds


import math
import multiprocessing
import time
from decimal import Decimal


def fib_default(n):
    if n <= 2:
        return 1
    else:
        return round(Decimal(((1+math.sqrt(5))**n - (1-math.sqrt(5))**n)/(2**n*math.sqrt(5))))


def fib_parallel(m):
    if m <= 10:
        return fib_default(m)
    else:
        if m % 2 == 0:
            n = m / 2
            k = m / 2
        else:
            n = (m-1) / 2
            k = (m+1) / 2
        result = fib_parallel(n + 1) * fib_parallel(k) + fib_parallel(n) * fib_parallel(k - 1)
    return round(Decimal(result))


def fibonacci(m):
    if m % 2 == 0:
        n = m / 2
        k = m / 2
    else:
        n = (m - 1) / 2
        k = (m + 1) / 2

    workers = [n + 1, k, n, k - 1]
    with multiprocessing.Pool() as pool:
        result = pool.map(fib_parallel, workers)
        pool.close()
        pool.join()

    return result[0] * result[1] + result[2] * result[3]


# Hàm main thực thi
if __name__ == "__main__":
    m = 2000
    start = time.time()
    result = fibonacci(m)
    print("Execution time: ", time.time() - start)
    print(result)
    print("Số chữ số: ", len(str(result)))
