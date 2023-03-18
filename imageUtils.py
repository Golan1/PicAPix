import imageio.v3 as iio
import numpy as np

defaultColorPalette = [(255, 255, 255), (255, 220, 0), (255, 181, 202), (0, 160, 0), (160, 103, 0), (255, 147, 0)]

def cropWhiteBackground(im):
    mat = np.sum(im, 2)
    mat = mat - np.min(mat)
    mat[mat < 50] = 0

    t = np.argmin(mat[:, int(mat.shape[1] / 2)])
    b = mat.shape[0] - np.argmin(mat[:, int(mat.shape[1] / 2)][::-1])

    l = np.argmin(mat[int(mat.shape[0] / 2), :])
    r = mat.shape[1] - np.argmin(mat[int(mat.shape[0] / 2), :][::-1])

    if im.shape[2] == 4:
        return np.delete(im[t:b, l:r], 3, axis=2)

    return im[t:b, l:r]


def convertImageToColorMap(filename, n, m):
    im = cropWhiteBackground(iio.imread(filename))

    sl, sw = getSquareDimensions(im, m, n)

    res = np.zeros(shape=(n, m))

    RGBtoColorIndex = np.ones(shape=(256, 256, 256), dtype=int) * -1
    tolerance = 20
    RGBtoColorIndex[255 - tolerance:, 255 - tolerance:, 255 - tolerance:] = 0
    colorIndexToRGB = [(255, 255, 255)]

    for i in range(n):
        for j in range(m):
            rgb = im[int(sl * (i + 0.5)), int(sw * (j + 0.5))]
            colorIndex = RGBtoColorIndex[rgb[0], rgb[1], rgb[2]]
            if colorIndex == -1:
                colorIndex = len(colorIndexToRGB)
                RGBtoColorIndex[
                max(0, rgb[0] - tolerance): min(256, rgb[0] + tolerance),
                max(0, rgb[1] - tolerance): min(256, rgb[1] + tolerance),
                max(0, rgb[2] - tolerance): min(256, rgb[2] + tolerance)] = colorIndex
                colorIndexToRGB.append(tuple(rgb))
            res[i, j] = colorIndex
    print(colorIndexToRGB)

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
            im[i * squareLength: (i + 1) * squareLength, j * squareLength: (j + 1) * squareLength] = \
                defaultColorPalette[
                    mat[i, j]]
    iio.imwrite(filename, im)
