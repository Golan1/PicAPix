import imageio.v3 as iio
import numpy as np


def readSolutionMatrixFromImage(filename, n, m):
    im = iio.imread(filename).copy()
    mat = np.sum(im, 2)
    mat[mat < 50] = 0

    t = np.argmin(mat[:, int(mat.shape[1] / 2)])
    b = mat.shape[0] - np.argmin(mat[:, int(mat.shape[1] / 2)][::-1])

    l = np.argmin(mat[int(mat.shape[0] / 2), :])
    r = mat.shape[1] - np.argmin(mat[int(mat.shape[0] / 2), :][::-1])

    mat = mat[t:b, l:r]

    sl, sw = mat.shape[0] / n, mat.shape[1] / m

    if abs(sl - sw) > 2:
        raise Exception("Diff too big")

    res = np.zeros(shape=(n, m))

    for i in range(n):
        for j in range(m):
            x = sl * (i + 0.5)
            y = sw * (j + 0.5)
            res[i, j] = 0 if mat[int(x), int(y)] == 0 else 1
    return res


def writeSolution(mat, squareLength, filename):
    n = len(mat) * squareLength
    m = len(mat[0]) * squareLength
    im = np.zeros(shape=(n, m, 3), dtype="uint8")
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if not mat[i][j]:
                im[i * squareLength: (i + 1) * squareLength, j * squareLength: (j + 1) * squareLength, :] = 255
    iio.imwrite(filename, im)
