from functools import partial
from z3 import *
from utils import *


def intA(arr):
    return [int(x) for x in arr]


def readLines(file, n):
    return [intA(file.readline().split()) for _ in range(n)]


def readRules(filename):
    with open(filename) as file:
        n, m = intA(file.readline().split())
        rows = readLines(file, n)
        cols = readLines(file, m)
    return n, m, rows, cols


def freeSpace(row, n):
    s = sum(row)
    s += len(row) - 1
    return n - s + 1


def addClause(arr):
    clauses.append(" ".join([str(x) for x in arr]) + " 0")


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
                addClause((
                    -myGeneralIndex,
                    -(myGeneralIndex - j)))  # promises AT MOST one option for the component.

            # except for the first component
            if componentIndexInRow == 0:
                continue

            for j in range(1, f - i):
                addClause((
                    -myGeneralIndex,
                    -(myGeneralIndex - f + j)))  # promises no collisions between neighboring component's options

        addClause(sameComponentOptions)  # promises that AT LEAST one option for the component.

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
        addClause(colComponentOptionsIndices + [-rowOption])


def draw():
    picture = []
    for i in range(n):
        picture.append([])
        for j in range(m):
            picture[i].append("\u2B1C")
    for row in chosen:
        rowIndex, componentIndex, startingSquare = row
        # since we don't care about columns when painting
        if rowIndex >= n:
            break
        for i in range(rows[rowIndex][componentIndex]):
            picture[rowIndex][startingSquare + i] = "\u2B1B"
    print("\n".join(["".join(x) for x in picture]))


def createIntersectionMatrix(n, m):
    return createMatrix(n, m, lambda: ([], []))


if __name__ == '__main__':
    SOLVING_MECHANISM = "external file"
    RULES_INPUT_FILENAME = r'artifacts/jets_rules.txt'
    DEBUG = False

    n, m, rows, cols = readRules(RULES_INPUT_FILENAME)

    matrix = createIntersectionMatrix(n, m)
    clauses = []
    componentsOptions = []

    if (DEBUG):
        calcComponentsOptions(0, rows[0], freeSpace(rows[0], n), partial(rowComponentOptionAdder, 0))
        calcComponentsOptions(n, cols[0], freeSpace(cols[0], m), partial(colComponentOptionAdder, 0))
        clauses.append("1  0")
        clauses.append("4  0")

        print(componentsOptions)
        print(f"p cnf {len(componentsOptions)} {len(clauses)}")
        print("\n".join(clauses))
        exit(0)

    for i, row in enumerate(rows):
        calcComponentsOptions(i, row, freeSpace(row, m), partial(rowComponentOptionAdder, i))

    for j, col in enumerate(cols):
        calcComponentsOptions(n + j, col, freeSpace(col, n), partial(colComponentOptionAdder, j))

        clauses.append("c intersections")
    for r in matrix:
        for rowComponentOptions, colComponentOptions in r:
            calcIntersection(rowComponentOptions, colComponentOptions)
            calcIntersection(colComponentOptions, rowComponentOptions)

    with open('temp/clauses.dimacs', "w") as file:
        file.write(f"p cnf {len(componentsOptions)} {len(clauses)}\n")
        file.write("\n".join(clauses))

    if SOLVING_MECHANISM == 'z3':
        s = Solver()
        s.from_file('temp/clauses.dimacs')
        print(s.check())

        model = convertZ3DimacsSolverToSortedModel(s.model(), len(componentsOptions))
    elif SOLVING_MECHANISM == 'external file':
        model = readSortedModelFromExternalFile("artifacts/assignments.txt")

    chosen = [componentsOptions[int(i)] for (i, b) in enumerate(model) if b]
    draw()
