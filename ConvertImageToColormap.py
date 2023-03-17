import numpy as np

from imageUtils import *

if __name__ == '__main__':
    filename = "15x15x2.barvaz.png"
    fileparts = filename.split(".")
    n, m, c = (int(x) for x in fileparts[0].split("x"))

    imageFilename = '0.images/' + filename
    outputFilename = '1.colormap/' + ".".join(fileparts[1:-1]) + ".txt"

    mat = convertImageToColorMap(imageFilename, n, m)

    np.savetxt(outputFilename, mat.astype(int), fmt='%i', delimiter=",")
