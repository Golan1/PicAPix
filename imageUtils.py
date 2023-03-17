import imageio.v3 as iio
import numpy as np

colorPalette = [(255, 255, 255), (0, 0, 0), (255, 0, 0)]

def cropWhiteBackground(im):
    mat = np.sum(im, 2)
    mat = mat - np.min(mat)
    mat[mat < 50] = 0

    t = np.argmin(mat[:, int(mat.shape[1] / 2)])
    b = mat.shape[0] - np.argmin(mat[:, int(mat.shape[1] / 2)][::-1])

    l = np.argmin(mat[int(mat.shape[0] / 2), :])
    r = mat.shape[1] - np.argmin(mat[int(mat.shape[0] / 2), :][::-1])

    mat = mat[t:b, l:r]

    return mat


def convertImageToColorMap(filename, n, m):
    im = cropWhiteBackground(iio.imread(filename))

    sl, sw = getSquareDimensions(im, m, n)


    res = np.zeros(shape=(n, m))

    # maps the SUM of the pixel's RGB to a color index. This might not be a refined enough clustering (for example, RED and GREEN are mapped to the same colorIndex)
    RGBtoColorIndex = np.ones(766, dtype=int) * -1
    tolerance = 20
    RGBtoColorIndex[765-tolerance:] = 0
    colorsCount = 1

    for i in range(n):
        for j in range(m):
            rgb = im[int(sl * (i + 0.5)), int(sw * (j + 0.5))]
            colorIndex = RGBtoColorIndex[rgb]
            if colorIndex == -1:
                colorIndex = colorsCount
                RGBtoColorIndex[max(0, rgb - tolerance): min(RGBtoColorIndex.shape[0], rgb + tolerance)] = colorIndex
                colorsCount += 1
            res[i, j] = colorIndex
    print(colorsCount)
    return res


def getSquareDimensions(im, m, n):
    sl, sw = im.shape[0] / n, im.shape[1] / m
    diff = abs(sl - sw)
    if diff > 2:
        raise Exception(f"Diff too big; {diff}")
    return sl, sw


def writeSolution(mat, squareLength, filename):
    n = mat.shape[0]
    m = mat.shape[1]
    im = np.ones(shape=(n * squareLength, m * squareLength, 3), dtype="uint8") * 255
    for i in range(n):
        for j in range(m):
            im[i * squareLength: (i + 1) * squareLength, j * squareLength: (j + 1) * squareLength] = colorPalette[
                mat[i, j]]
    iio.imwrite(filename, im)
