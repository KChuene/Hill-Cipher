import numpy as np
import math, copy
import sys


def create_square_matrix(int_array, N) -> list[list[int]]:
    if math.sqrt(len(int_array)) != N:
        print(f"[Error] MatrixOps: CreateSquareMatrix : Cannot convert array of size {len(int_array)} to square matrix of size {N}")
        sys.exit(-1)  # cannot convert to square

    matrix = []
    # build each row: if N = 3, iterate 3 times to create 3 rows, for each row set the next 3 entries in intArray
    for counter in range(0, N):
        # step through the array in 3s and set each triple as a new row into matrix
        matrix.append(
            [int_array[i] for i in range(counter * N, (counter + 1) * N)])  # select next 3 entries from intArray

    return matrix


def is_valid_matrix(matrix):
    # Null or Empty check
    if matrix is None:
        return False

    # All rows must have the same number of columns
    baseLength = len(matrix[0])
    for row in matrix:
        # Return on first fail
        if len(row) != baseLength:
            return False

    return True

def is_square_matrix(A):
    if not is_valid_matrix(A):
        return False

    # Must be n x n (row count = col count)
    rowCount = len(A)
    for row in A:
        # For every row , num cols must equal num rows
        if len(row) != rowCount:
            return False

    return True

def matrix_product(A, B):
    # store expected dimensions
    product = []

    # Check that matrices have dimension m x n; m > 0 and n > 0
    if (not is_valid_matrix(B)) or (not is_valid_matrix(A)):
        print("[Error] MatrixOps: MatrixProduct : Invalid matrices provided.")
        sys.exit(-1)

    # no. of cols of A must = no. of rows of B for product to be defined
    if len(A) != len(B[0]) and len(A[0]) != len(B):
        print(f"[Error] MatrixOps: MatrixProduct: Invalid matrix sizes {len(A)}x{len(A[0])} and {len(B)}x{len(B[0])}.")
        sys.exit(-1)

    # (AB)ij = (ith row of A) dot (jth column of B)
    # NOTE: B is actually a row vector ie. [[x, y, z,...]] we keep it so because it is easier to traverse,
    # but pretend it is a column vector since it can be translated as such
    for i in range(0, len(A)):
        for j in range(0, len(B)):
            product.append(np.linalg.multi_dot([A[i], B[j]]) % 149186 + 1)

    return product

def identity_of(A):
    identity = copy.deepcopy(A)
    for r in range(0, len(identity)):
        for c in range(0, len(identity[0])):
            if r == c:
                # Main diagonal set to 1s
                identity[r][c] = 1

            else:
                # everywhere else set to 0s
                identity[r][c] = 0
    return identity