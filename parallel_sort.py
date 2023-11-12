import time
import math
import multiprocessing
import numpy as np
import heapq


# Hàm merge để nhập hai mảng đã sắp xếp
def merge(left, right):
    left = np.array(left)
    right = np.array(right)
    # Hàm searchsorted trả về danh sách các index để insert mảng right vào left mà vẫn giữ nguyên trình tự
    indexes = left.searchsorted(right)
    # Merge 2 mảng theo indexes
    return np.insert(left, indexes, right)


# Hàm heap sort dùng module heapq
def heap_sort(arr):
    result = []
    arr = list(arr)
    heapq.heapify(arr)
    while arr:
        result.append(heapq.heappop(arr))
    return np.array(result)


# Hàm sort main
def parallel_sort(arr):
    processes = multiprocessing.cpu_count()
    size = int(math.ceil(float(len(arr)) / processes))

    # Chia mảng cha thành các mảng con
    blocks = [arr[i * size: (i + 1) * size] for i in range(processes)]

    # Sort các mảng con bằng heap sort
    with multiprocessing.Pool() as pool:
        sorted_blocks = pool.map(heap_sort, blocks)
        pool.close()
        pool.join()

    # Merge các mảng con lại
    while len(sorted_blocks) > 1:
        temp = []
        for i in range(0, len(sorted_blocks), 2):
            temp.append(merge(sorted_blocks[i], sorted_blocks[i+1]))
        sorted_blocks = temp
    return sorted_blocks[0]


if __name__ == "__main__":
    size = 10**5
    data_unsorted = np.random.randint(low=0, high=100000, size=size)
    start = time.time()

    sorted_arr = parallel_sort(data_unsorted)
    numpySort = np.sort(data_unsorted)
    # So sánh kết quả với numpy.sort()
    print(np.array_equal(sorted_arr, numpySort))
    print("Time: ", time.time() - start, '\n')
