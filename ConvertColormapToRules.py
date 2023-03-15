from utils import *
from imageUtils import *
import numpy as np


def getRowRules(row):
    sum = 0
    res = []
    previousColor = 0
    for currentColor in row:
        if currentColor == 0:
            if previousColor != 0:
                res.append((str(sum), str(previousColor)))
                sum = 0
        elif currentColor == previousColor:
            sum += 1
        elif previousColor == 0:
            sum = 1
        else:
            res.append((str(sum), str(previousColor)))
            sum = 1
        previousColor = currentColor

    if sum != 0:
        res.append((str(sum), str(previousColor)))

    return " ".join([",".join(component) for component in res])


def getRowsRules(mat):
    for i in range(mat.shape[0]):
        yield getRowRules(mat[i, :])


if __name__ == '__main__':
    filename = "jets.txt"
    colormapFilename = '1.colormap/' + filename
    outputFilename = '2.rules/' + filename

    mat = np.loadtxt(colormapFilename, dtype=int, delimiter=",")

    # in case it was not given in advance
    n = len(mat)
    m = len(mat[0])
    c = np.max(mat)

    with open(outputFilename, 'w') as file:
        file.write(f"{n} {m} {c}\n")
        file.write("\n".join(getRowsRules(mat)))
        file.write("\n")
        file.write("\n".join(getRowsRules(np.transpose(mat))))
