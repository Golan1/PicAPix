def readSortedModelFromExternalFile(filename):
    with open(filename) as file:
        assignments = file.readline().split()
    return [True if int(x) > 0 else False for x in assignments]


def convertZ3DimacsSolverToSortedModel(z3Model, nLiterals):
    arr = [False] * nLiterals
    for l in z3Model:
        if str(z3Model[l]) == 'True':
            arr[int(str(l)[2:]) - 1] = True
    return arr


def createMatrix(n, m, cellInitializer):
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(cellInitializer())
    return matrix


def readSolutionMatrixFromText(filename):
    mat = []
    with open(filename) as file:
        while True:
            line = file.readline()
            if line == '':
                break
            mat.append(line)
    mat[0] = mat[0][3:]
    return mat


def drawBooleanMatrixAsBlackAndWhitePicture(matrix):
    for row in matrix:
        rowStr = ""
        for j in row:
            rowStr += "\u2B1B" if j else "\u2B1C"
        print(rowStr)
