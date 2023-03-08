from functools import partial


def intA(arr):
    return [int(x) for x in arr]


def readLines(n):
    lines = []
    for _ in range(n):
        line = file.readline()
        lines.append(intA(line.split()))
    return lines


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


with open(r'jets_rules.txt') as file:
    n, m = intA(file.readline().split())
    rows = readLines(n)
    cols = readLines(m)

matrix = []
for i in range(n):
    matrix.append([])
    for j in range(m):
        matrix[i].append(([], []))

clauses = []
componentsOptions = []

DEBUG = False

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

with open('clauses.DIMACS', "w") as file:
    file.write(f"p cnf {len(componentsOptions)} {len(clauses)}\n")
    file.write("\n".join(clauses))

# --------------------------
with open("Assignments.txt") as file:
    assignments = file.readline().split()

chosen = [componentsOptions[int(x) - 1] for x in assignments if int(x) > 0]

picture = []
for i in range(n):
    picture.append([])
    for j in range(m):
        picture[i].append(".")
for row in chosen:
    rowIndex, componentIndex, startingSquare = row
    # since we don't care about columns when painting
    if rowIndex >= n:
        break
    for i in range(rows[rowIndex][componentIndex]):
        picture[rowIndex][startingSquare + i] = "X"

print("\n".join(["".join(x) for x in picture]))

# print("-------------------------------------------")
#
# picture = []
# for i in range(n):
#     picture.append([])
#     for j in range(m):
#         picture[i].append(".")
# for col in chosen:
#     colIndex, componentIndex, startingSquare = col
#     # since we don't care about rows when painting
#     if colIndex < n:
#         continue
#     colIndex -= n
#
#     for i in range(cols[colIndex][componentIndex]):
#         picture[startingSquare + i][colIndex] = "X"
#
# print("\n".join(["".join(x) for x in picture]))
