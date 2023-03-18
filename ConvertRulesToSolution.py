from functools import partial
from z3 import *
from utils import *
from ruleUtils import *
from tqdm import tqdm
from imageUtils import *
from time import time
from dataclasses import dataclass


@dataclass
class ComponentOption:
    isRow: bool
    rowIndex: int
    indexInRow: int
    startingLocation: int
    length: int
    color: int


def freeSpace(row, n):
    adjacents = 0
    for x, y in zip(row[:-1], row[1:]):
        # same color
        if x[1] == y[1]:
            adjacents += 1
    return n - sum(x[0] for x in row) - adjacents + 1


def calcComponentsOptions(rowIndex, row, freeSpace, componentOptionAddedObserver, isRow):
    componentStartingPoint = 0
    previousColor = 0
    for componentIndexInRow, (componentLength, componentColor) in enumerate(row):
        if previousColor == componentColor:
            componentStartingPoint += 1
        sameComponentOptions = []
        for indexInComponentOption in range(freeSpace):
            componentsOptions.append(
                ComponentOption(isRow, rowIndex, componentIndexInRow, componentStartingPoint + indexInComponentOption,
                                componentLength, componentColor))
            myGeneralIndex = len(componentsOptions)
            for l in range(componentLength):
                componentOptionAddedObserver(myGeneralIndex, componentStartingPoint + indexInComponentOption + l,
                                             componentColor)
            sameComponentOptions.append(myGeneralIndex)

            for j in range(1, indexInComponentOption + 1):
                clauses.append([
                    -myGeneralIndex,
                    -(myGeneralIndex - j)])  # promises AT MOST one option for the component.

            # except for the first component
            if componentIndexInRow != 0:
                numOfCollisions = freeSpace - indexInComponentOption

                # promises no collisions between neighboring component's options
                for j in range(1, numOfCollisions):
                    clauses.append([
                        -myGeneralIndex,
                        -(myGeneralIndex - freeSpace + j)])

        clauses.append(sameComponentOptions)  # promises that AT LEAST one option for the component.
        previousColor = componentColor
        componentStartingPoint += componentLength


def rowComponentOptionAdder(rowIndex, generalIndex, colIndex, color):
    intersectionMatrix[rowIndex][colIndex][color - 1][0].append(generalIndex)


def colComponentOptionAdder(colIndex, generalIndex, rowIndex, color):
    intersectionMatrix[rowIndex][colIndex][color - 1][1].append(generalIndex)


# Ensuring that if a rowOption is chosen, a respective col option is chosen as well
# 1 row option against all col options
def calcIntersection(rowComponentOptionsIndices, colComponentOptionsIndices):
    for rowOption in rowComponentOptionsIndices:
        clauses.append(colComponentOptionsIndices + [-rowOption])


def render(n, m, chosen: list[ComponentOption]):
    colorMap = np.zeros(shape=(n, m), dtype=int)

    for row in chosen:
        colorMap[row.rowIndex, row.startingLocation: row.startingLocation + row.length] = row.color
    return colorMap


def createIntersectionMatrix(n, m, c):
    return createMatrix(n, m, lambda: createMatrix(c, 2, lambda: []))


def writeDimacsFile():
    with open('temp/clauses.dimacs', "w") as file:
        file.write(f"p cnf {len(componentsOptions)} {len(clauses)}\n")
        file.write("\n".join([" ".join([str(literal) for literal in clause]) + " 0" for clause in clauses]))


if __name__ == '__main__':
    start = time()
    puzzleName = "flowers"
    SOLVING_MECHANISM = "z3 dimacs"
    # SOLVING_MECHANISM = "z3 classic"
    RULES_INPUT_FILENAME = f'2.rules/{puzzleName}.txt'
    SOLUTION_OUTPUT_FILENAME = f'3.solutions/{puzzleName}.png'

    n, m, c, rows, cols = readRules(RULES_INPUT_FILENAME)

    intersectionMatrix = createIntersectionMatrix(n, m, c)
    clauses = []
    componentsOptions = []

    for i, row in enumerate(rows):
        calcComponentsOptions(i, row, freeSpace(row, m), partial(rowComponentOptionAdder, i), True)

    for j, col in enumerate(cols):
        calcComponentsOptions(j, col, freeSpace(col, n), partial(colComponentOptionAdder, j), False)

    for row in intersectionMatrix:
        for cell in row:
            for rowComponentOptions, colComponentOptions in cell:
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
        print("reading from file")
        s.from_file('temp/clauses.dimacs')
        print("solving formula")
        print(s.check())
        model = convertZ3DimacsSolverToSortedModel(s.model(), len(componentsOptions))

    else:
        raise Exception("Mechanism was not found")

    chosen = [componentsOptions[int(i)] for (i, b) in enumerate(model) if b]

    colorMapAccordingToRows = render(n, m, [row for row in chosen if row.isRow])
    writeSolution(colorMapAccordingToRows, 30, SOLUTION_OUTPUT_FILENAME)

    if False:
        # drawBooleanMatrixAsBlackAndWhitePicture(colorMapAccordingToRows)
        colorMapAccordingToCols = np.transpose(render(m, n, [row for row in chosen if not row.isRow]))
        writeSolution(colorMapAccordingToCols, 30,  f'3.solutions/{puzzleName}_cols.png')

    end = time()

    print(f"total time: {end - start}")
