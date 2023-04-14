def levenshtein_distance(s1, s2):
    # Create a matrix of zeros with dimensions len(s1) + 1 x len(s2) + 1
    matrix = [[0 for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]

    # Fill in the first row and column of the matrix
    for i in range(len(s1) + 1):
        matrix[i][0] = i
    for j in range(len(s2) + 1):
        matrix[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i-1] == s2[j-1]:
                matrix[i][j] = matrix[i-1][j-1]
            else:
                matrix[i][j] = min(matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1]) + 1

    # Return the last element of the matrix
    # print(matrix[len(s1)][len(s2)])
    return matrix[len(s1)][len(s2)]