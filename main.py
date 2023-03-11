from functools import partial
from z3 import *
from utils import *
from ruleUtils import *
from tqdm import tqdm

def freeSpace(row, n):
    s = sum(row)
    s += len(row) - 1
    return n - s + 1


def calcComponentsOptions(index, row, f, componentOptionAddedObserver):
    prefix = 0
    for componentIndexInRow, componentLength in enumerate(row):
        sameComponentOptions = []
        for i in range(f):
            componentsOptions.append((index, componentIndexInRow, prefix + i))
            myGeneralIndex = len(componentsOptions)
            for l in range(componentLength):
                componentOptionAddedObserver(myGeneralIndex, prefix + i + l)
            sameComponentOptions.append(myGeneralIndex)

            for j in range(1, i + 1):
                clauses.append([
                    -myGeneralIndex,
                    -(myGeneralIndex - j)])  # promises AT MOST one option for the component.

            # except for the first component
            if componentIndexInRow == 0:
                continue

            for j in range(1, f - i):
                clauses.append([
                    -myGeneralIndex,
                    -(myGeneralIndex - f + j)])  # promises no collisions between neighboring component's options

        clauses.append(sameComponentOptions)  # promises that AT LEAST one option for the component.

        prefix += componentLength + 1


def rowComponentOptionAdder(rowIndex, generalIndex, colIndex):
    matrix[rowIndex][colIndex][0].append(generalIndex)


def colComponentOptionAdder(colIndex, generalIndex, rowIndex):
    matrix[rowIndex][colIndex][1].append(generalIndex)


# # Ensuring that
# # 2 from arr1, 1 from arr2
# def calcTriplets(arr1, arr2):
#     for i in range(len(arr1)):
#         for j in range(i):
#             for k in arr2:
#                 addCluase((-arr1[i], -arr1[j], -k))


# Ensuring that if a rowOption is chosen, a respective col option is chosen as well
# 1 row option against all col options
def calcIntersection(rowComponentOptionsIndices, colComponentOptionsIndices):
    for rowOption in rowComponentOptionsIndices:
        clauses.append(colComponentOptionsIndices + [-rowOption])


def render(n, m, chosen, rows):
    picture = createMatrix(n, m, lambda: False)

    for row in chosen:
        rowIndex, componentIndex, startingSquare = row
        # since we don't care about columns when painting
        if rowIndex >= n:
            break
        for i in range(rows[rowIndex][componentIndex]):
            picture[rowIndex][startingSquare + i] = True
    drawBooleanMatrixAsBlackAndWhitePicture(picture)


def createIntersectionMatrix(n, m):
    return createMatrix(n, m, lambda: ([], []))


def writeDimacsFile():
    with open('temp/clauses.dimacs', "w") as file:
        file.write(f"p cnf {len(componentsOptions)} {len(clauses)}\n")
        file.write("\n".join([" ".join([str(literal) for literal in clause]) + " 0" for clause in clauses]))


if __name__ == '__main__':
    # SOLVING_MECHANISM = "dimacs file"
    # SOLVING_MECHANISM = "z3 dimacs"
    SOLVING_MECHANISM = "z3 classic"
    RULES_INPUT_FILENAME = r'artifacts/jets_rules.txt'
    n, m, rows, cols = readRules(RULES_INPUT_FILENAME)

    matrix = createIntersectionMatrix(n, m)
    clauses = []
    componentsOptions = []

    for i, row in enumerate(rows):
        calcComponentsOptions(i, row, freeSpace(row, m), partial(rowComponentOptionAdder, i))

    for j, col in enumerate(cols):
        calcComponentsOptions(n + j, col, freeSpace(col, n), partial(colComponentOptionAdder, j))

    for r in matrix:
        for rowComponentOptions, colComponentOptions in r:
            calcIntersection(rowComponentOptions, colComponentOptions)
            calcIntersection(colComponentOptions, rowComponentOptions)

    if SOLVING_MECHANISM == 'z3 classic':
        s = Solver()
        z3literals = Bools(" ".join(["k!" + str(x) for x in range(1, len(componentsOptions) + 1)]))
        arr = []
        for clause in tqdm(clauses):
            arr.append(
                Or([Not(z3literals[-literal - 1]) if literal < 0 else z3literals[literal - 1] for literal in clause]))
        s.add(arr)
        print(s.check())
        model = convertZ3DimacsSolverToSortedModel(s.model(), len(componentsOptions))

    elif SOLVING_MECHANISM == 'z3 dimacs':
        writeDimacsFile()

        s = Solver()
        s.from_file('temp/clauses.dimacs')
        print(s.check())
        model = convertZ3DimacsSolverToSortedModel(s.model(), len(componentsOptions))

    elif SOLVING_MECHANISM == 'dimacs file':
        writeDimacsFile()
        # stop here and fill manually assignments.txt using http://logicrunch.it.uu.se:4096/~wv/minisat/
        model = readSortedModelFromExternalFile("artifacts/assignments.txt")
    else:
        raise Exception("Mechanism was not found")

    chosen = [componentsOptions[int(i)] for (i, b) in enumerate(model) if b]
    render(n, m, chosen, rows)
