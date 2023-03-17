
def intA(arr):
    return [[int(y) for y in x.split(",")] for x in arr]


def readLines(file, n):
    return [intA(file.readline().split()) for _ in range(n)]


def readRules(filename):
    with open(filename) as file:
        n, m, c = [int(x) for x in file.readline().split()]
        rows = readLines(file, n)
        cols = readLines(file, m)
    return n, m, c, rows, cols
