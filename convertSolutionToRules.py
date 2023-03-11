solutionFilename = "artifacts/jets_solution.txt"
outputFilename = "artifacts/jets_rules.txt"

mat = []





mat = readSolutionMatrix(solutionFilename)

with open(outputFilename, 'w') as file:
    n = len(mat)
    m = len(mat[0]) - 1
    file.write(f"{n} {m}\n")
    for row in mat:
        sum = 0
        res = []
        for c in row:
            if c == '0':
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
            if c == '0':
                sum += 1
            else:
                res.append(sum)
                sum = 0

        res.append(sum)

        file.write(f"{' '.join([str(x) for x in res if x != 0])}\n")
