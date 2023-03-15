from utils import *
from imageUtils import *

if __name__ == '__main__':
    filename = "65x180.band.png"
    fileparts = filename.split(".")
    n, m, = (int(x) for x in fileparts[0].split("x"))

    # solutionFilename = "artifacts/jets_solution.txt"
    # outputFilename = "artifacts/jets_rules.txt"
    imageFilename = '0.images/' + filename
    outputFilename = '1.rules/' + ".".join(fileparts[1:-1]) + ".txt"

    if fileparts[-1] == "txt":
        mat = readSolutionMatrixFromText(imageFilename)
    elif fileparts[-1] == "png":
        mat = readSolutionMatrixFromImage(imageFilename, n, m)
    else:
        raise Exception("Unsupported solution file")

    with open(outputFilename, 'w') as file:
        n = len(mat)
        m = len(mat[0])
        file.write(f"{n} {m}\n")
        for row in mat:
            sum = 0
            res = []
            for c in row:
                if c == '1' or c == 1:
                    sum += 1
                else:
                    res.append(sum)
                    sum = 0

            res.append(sum)

            file.write(f"{' '.join([str(x) for x in res if x != 0])}\n")

        for j in range(m):
            sum = 0
            res = []
            for i in range(n):
                c = mat[i][j]
                if c == '1' or c == 1:
                    sum += 1
                else:
                    res.append(sum)
                    sum = 0

            res.append(sum)

            file.write(f"{' '.join([str(x) for x in res if x != 0])}\n")
