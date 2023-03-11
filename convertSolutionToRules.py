from utils import *
from imageUtils import *

if __name__ == '__main__':
    # solutionFilename = "artifacts/jets_solution.txt"
    # outputFilename = "artifacts/jets_rules.txt"
    solutionFilename = 'images/65x180_band.png'
    outputFilename = 'rules/65x180_band_rules.txt'

    if solutionFilename[-3:] == "txt":
        mat = readSolutionMatrixFromText(solutionFilename)
    elif solutionFilename[-3:] == "png":
        mat = readSolutionMatrixFromImage(solutionFilename, 65, 180)
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
                if c == '0' or c == 0:
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
                if c == '0' or c == 0:
                    sum += 1
                else:
                    res.append(sum)
                    sum = 0

            res.append(sum)

            file.write(f"{' '.join([str(x) for x in res if x != 0])}\n")
