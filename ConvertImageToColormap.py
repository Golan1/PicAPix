import numpy as np

from imageUtils import *

if __name__ == '__main__':
    filename = "65x180x1.band.png"
    fileparts = filename.split(".")
    n, m, c = (int(x) for x in fileparts[0].split("x"))

    # solutionFilename = "artifacts/jets_solution.txt"
    # outputFilename = "artifacts/jets_rules.txt"
    imageFilename = '0.images/' + filename
    outputFilename = '1.colormap/' + ".".join(fileparts[1:-1]) + ".txt"

    if fileparts[-1] == "txt":
        # TODO: refactor to np and colors
        # mat = readSolutionMatrixFromText(imageFilename, c)
        raise Exception("WIP")
    elif fileparts[-1] == "png":
        mat = readSolutionMatrixFromImage(imageFilename, n, m)
    else:
        raise Exception("Unsupported solution file")

    np.savetxt(outputFilename, mat.astype(int), fmt='%i', delimiter=",")
