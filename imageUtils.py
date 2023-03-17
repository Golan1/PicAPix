import imageio.v3 as iio
import numpy as np

colorPalette = [(255, 255, 255), (0, 0, 0), (255, 0, 0)]


def readSolutionMatrixFromImage(filename, n, m):
    im = iio.imread(filename).copy()
    mat = np.sum(im, 2)
    mat = mat - np.min(mat)
    mat[mat < 50] = 0

    t = np.argmin(mat[:, int(mat.shape[1] / 2)])
    b = mat.shape[0] - np.argmin(mat[:, int(mat.shape[1] / 2)][::-1])

    l = np.argmin(mat[int(mat.shape[0] / 2), :])
    r = mat.shape[1] - np.argmin(mat[int(mat.shape[0] / 2), :][::-1])

    mat = mat[t:b, l:r]

    sl, sw = mat.shape[0] / n, mat.shape[1] / m

    diff = abs(sl - sw)
    if diff > 2:
        raise Exception(f"Diff too big; {diff}")

    res = np.zeros(shape=(n, m))

    for i in range(n):
        for j in range(m):
            x = sl * (i + 0.5)
            y = sw * (j + 0.5)
            res[i, j] = (1 if mat[int(x), int(y)] == 0 else 0)
    return res


def writeSolution(mat, squareLength, filename):
    n = mat.shape[0]
    m = mat.shape[1]
    im = np.ones(shape=(n * squareLength, m * squareLength, 3), dtype="uint8") * 255
    for i in range(n):
        for j in range(m):
            im[i * squareLength: (i + 1) * squareLength, j * squareLength: (j + 1) * squareLength] = colorPalette[
                mat[i, j]]
    iio.imwrite(filename, im)
