import time
import numpy as np
import multiprocessing


def default_multiply(matrix_a, matrix_b):
    dim = matrix_a.shape[0]
    result = np.zeros((dim, dim), dtype='int')
    matrix_b = np.transpose(matrix_b)
    for i in range(dim):
        result[i] = np.sum(matrix_a[i] * matrix_b, axis=1)
    return result


def matrix_split(matrix):
    n = matrix.shape[0] // 2
    return matrix[:n, :n], matrix[:n, n:], matrix[n:, :n], matrix[n:, n:]


def strassen(matrix_a, matrix_b):
    dim = matrix_a.shape[0]
    if dim % 4 != 0:
        return default_multiply(matrix_a, matrix_b)

    A, B, C, D = matrix_split(matrix_a)
    E, F, G, H = matrix_split(matrix_b)

    p1 = strassen(A + D, E + H)
    p2 = strassen(C + D, E)
    p3 = strassen(A, F - H)
    p4 = strassen(D, G - E)
    p5 = strassen(A + B, H)
    p6 = strassen(C - A, E + F)
    p7 = strassen(B - D, G + H)

    top_left = p1 + p4 - p5 + p7
    top_right = p3 + p5
    bot_left = p2 + p4
    bot_right = p1 - p2 + p3 + p6

    result = np.vstack((np.hstack((top_left, top_right)), np.hstack((bot_left, bot_right))))
    return result


def pad_zeros(matrix):
    zeros = 0
    size = matrix.shape[0]
    while (size + zeros) % 4 != 0:
        zeros += 1
    pad_h = np.zeros((size, zeros), dtype='int')
    pad_v = np.zeros((zeros, size + zeros), dtype='int')

    matrix = np.hstack((matrix, pad_h))
    return np.vstack((matrix, pad_v))


def parallel_multiply_matrices(matrix_a, matrix_b):
    dim = matrix_a.shape[0]
    if dim % 4 != 0:
        matrix_a = pad_zeros(matrix_a)
        matrix_b = pad_zeros(matrix_b)

    A, B, C, D = matrix_split(matrix_a)
    E, F, G, H = matrix_split(matrix_b)

    workers = [(A + D, E + H), (C + D, E), (A, F - H), (D, G - E), (A + B, H), (C - A, E + F), (B - D, G + H)]

    with multiprocessing.Pool() as pool:
        results = pool.starmap(strassen, workers)
        pool.close()
        pool.join()

    top_left = results[0] + results[3] - results[4] + results[6]
    top_right = results[2] + results[4]
    bot_left = results[1] + results[3]
    bot_right = results[0] - results[1] + results[2] + results[5]

    result = np.vstack((np.hstack((top_left, top_right)), np.hstack((bot_left, bot_right))))
    return result[:dim, :dim]


if __name__=='__main__':
    n = 1000
    matrix1 = np.random.randint(0, 2, size=(n, n))
    matrix2 = np.random.randint(0, 2, size=(n, n))

    #print(matrix1, '\n')
    #print(matrix2, '\n')
    start = time.time()
    result = parallel_multiply_matrices(matrix1, matrix2)
    end = time.time()
    print("Execution time: ", end-start)
    print("Result:")
    print(result, '\n')
