from utils import *
from imageUtils import *
import numpy as np


def getRowRules(row):
    sum = 0
    res = []
    for cell in row:
        if cell == '1' or cell == 1:
            sum += 1
        else:
            res.append(sum)
            sum = 0
    res.append(sum)
    return f"{' '.join([str(x) + ',1' for x in res if x != 0])}"


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
        file.write(f"{n} {m}\n")
        file.write("\n".join(getRowsRules(mat)))
        file.write("\n")
        file.write("\n".join(getRowsRules(np.transpose(mat))))

