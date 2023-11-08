import time
import math
import multiprocessing
import numpy as np


# Hàm merge cải tiến, ghép n mảng con lại và sắp xếp
def merge(*arrs):
    return sorted(np.concatenate(arrs))


def parallel_sort(arr):
    processes = multiprocessing.cpu_count()
    # size = độ dài mỗi mảng con (chú ý khi chiều dài mảng cha không chia hết số process)
    size = int(math.ceil(float(len(arr)) / processes))

    # Chia mảng cha thành các mảng con (blocks) mỗi block có độ dài = size
    blocks = [arr[i*size: (i + 1)*size] for i in range(processes)]

    # Sắp xếp các mảng con song song
    with multiprocessing.Pool() as pool:
        sorted_blocks = pool.map(sorted, blocks)
        pool.close()
        pool.join()

    # Ghép tất cả các mảng con lại
    return merge(*sorted_blocks)


if __name__ == "__main__":
    size = 10**5
    data_unsorted = np.random.randint(low=0, high=100000, size=size)
    start = time.time()

    sorted_arr = parallel_sort(data_unsorted)
    numpySort = np.sort(data_unsorted)
    # So sánh kết quả với numpy.sort()
    print(np.array_equal(sorted_arr, numpySort))
    print("Time: ", time.time() - start, '\n')
