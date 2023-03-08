solutionFilename = "jets_solution.txt"
outputFilename = "temp/jets_rules.txt"

mat = []
with open(solutionFilename) as file:
    while True:
        line = file.readline()
        if line == '':
            break
        mat.append(line)

mat[0] = mat[0][3:]

with open(outputFilename, 'w') as file:
    n = len(mat)
    m = len(mat[0]) - 1
    file.write(f"{n} {m}\n")
    for row in mat:
        sum = 0
        res = []
        for c in row:
            if c == '1':
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
            if c == '1':
                sum += 1
            else:
                res.append(sum)
                sum = 0

        res.append(sum)

        file.write(f"{' '.join([str(x) for x in res if x != 0])}\n")
