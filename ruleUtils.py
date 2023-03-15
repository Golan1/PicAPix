def intA(arr):
    return [int(x.split(",")[0]) for x in arr]


def readLines(file, n):
    return [intA(file.readline().split()) for _ in range(n)]


def readRules(filename):
    with open(filename) as file:
        n, m = [int(x) for x in file.readline().split()]
        rows = readLines(file, n)
        cols = readLines(file, m)
    return n, m, rows, cols
