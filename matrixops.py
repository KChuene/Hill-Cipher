import math, copy

def create_square_matrix(intArray, N) -> list[list[int]]:
    if math.sqrt( len(intArray) ) != N:
        return None # cannot convert to square

    matrix = []
    # build each row: if N = 3, iterate 3 times to create 3 rows, for each row set the next 3 entries in intArray
    for counter in range(0, N, 1):
        # step through the array in 3s and set each triple as a new row into matrix
        matrix.append([intArray[i] for i in range(counter*N,(counter+1)*N)]) # select next 3 entries from intArray

    return matrix
    
def is_valid_matrix(matrix):
    # Null or Empty check
    if (not matrix) or (not any(matrix)):
        return False 
    
    # All rows must have the same number of columns
    baseLength = len(matrix[0])
    for r in range(0, len(matrix)):
        # Return on first fail
        if len(matrix[r]) != baseLength:
            return False
            
    return True
    
def is_square_matrix(A):
    if not is_valid_matrix(A):
        return False
    
    # Must be n x n (row count = col count)
    if(len(A) != len(A[0])):
        return False
    
    return True

def matrix_product(A, B) -> list[int]:
    # store expected dimensions
    product = []

    # Check that matrices have dimension m x n; m > 0 and n > 0
    if (not is_valid_matrix(B)) or (not is_valid_matrix(A)):
        exit()

    # no. of cols of A must = no. of rows of B for product to be defined
    if len(A[0]) != len(B[0]):
        exit()

    # (AB)ij = ith row of A dot jth column of B
    # NOTE: B is actually a row vector ie. [[x, y, z,...]] we keep it so because it is easier to traverse,
    # but pretend it is a column vector since it can be translated as such
    for i in range(0, len(A)):
        for j in range(0, len(B)):
            #product.append((dot_product(A[i], B[j]) % 93 + 1) + 33)
            #product.append(dot_product(A[i], B[j]) % len(alphabet_map)) # limit to the number of alphabet chars COMMENT OUT
            #product.append((dot_product(A[i], B[j]) % 149191) + 1) # limit product to number of unicode chars represented
            product.append((dot_product(A[i], B[j]) % 149186 + 1)) # limit product to number of unicode chars represented
        
    return product


def dot_product(rowVector, columnVector) -> int:
    # these must be the same length for dot product to be defined since it works entry wise
    if len(rowVector) != len(columnVector):
        exit()

    # dot product =  sum of v[i] * w[i] for all corresponding entries in v and w
    product = 0
    for i in range(0, len(rowVector)):
        product += rowVector[i] * columnVector[i]
    
    return product

def product(A, B):
    if not is_valid_matrix(A):
        exit()

    if not is_valid_matrix(B):
        exit()

    if not len(A[0]) == len(B):
        exit()

        # the dotproduct of row i of A with column j of B
    BTranspose = transpose(B) # We will extract the columns of B as row vectors (easier)
    product = []
    for row in range(0, len(A)):
        newRow = []
        for col in range(0, len(B[0])):
            dot = dot_product(A[row], BTranspose[col])
            newRow.append(dot)

        product.append(newRow)
        
    return product


def transpose(A):
    # Entry at row i col j with entry at row j col i
    # For effeciency we traverse entries above XOR below 
    # the main diagonal (otherwise the process would be redundant)
        
    if not is_square_matrix(A):
        return None

    B = copy.deepcopy(A)
    for row in range(0, len(B)):
        for col in range(row + 1, len(B[row])):
            # (a)ij = (a)ji, and (a)ji = (a)ij
            temp = B[row][col]
            B[row][col] = B[col][row]
            B[col][row] = temp

    return B

def adjoint(A):
    if not is_square_matrix(A):
        return None

    B = copy.deepcopy(A)
    for row in range(0, len(B)):
        for col in range(0, len(A)):
            B[row][col] = cofactor_at(A, row, col)

    return transpose(B)
    
def optimal_expansion_col(A):
    # Find the column with the most zeros
    maxCol = 0
    max = 0
    for col in range(0, len(A)):
        count = 0
        for row in range(0, len(A)):
            if A[row][col] == 0:
                    count += 1
        if count > max:
            maxCol = col
            max = count
    # Return the column index and the number of zeros
    return maxCol, max
    
def optimal_expansion_row(A):
    # Find the row with the most zeros
    maxRow = 0
    max = 0
    for row in range(0, len(A)):
        if A[row].count(0) > max:
            maxRow = row
            max = A[row].count(0)

    # Return the row index and the number of zeros
    return maxRow, max

def submatrix(A, rowToOmit, colToOmit):
    # perform a deep copy of A that excludes all entries 
    # in the provided row and all entries in the provided col
    
    range_check(rowToOmit, 0, len(A))
    range_check(colToOmit, 0, len(A[0]))
    
    resultMatrix = []
    for row in range(0, len(A)):
        # 1. Traverse rows, skipping row to omit
        # 2. At each row make list of cols to add, skipping 
        # col to omit
        # 3. Add constructed list to result matrix
        if row == rowToOmit:
            continue

        newRow = []
        for col in range(0, len(A[row])):
            if col == colToOmit:
                continue
            newRow.append(A[row][col])
        resultMatrix.append(newRow)

    return resultMatrix


def cofactor_at(A, row, col):
    # Cij = (-1)^(i+j) x Mij, where Mij is the determinant
    # of the sub matrix obtained by eliminating the ith row and jth col
    return ((-1)**(row + col))*det(submatrix(A, row, col))

def cofactor_col_expansion(A, col):
    result = 0
    for row in range(0, len(A)):
        # result = det = a1jC1j + a2jC2j +...+ anjCnj
        result += A[row][col]*cofactor_at(A, row, col)

    return result

def cofactor_row_expansion(A, row):
    result = 0
    for col in range(0, len(A[row])):
        # result = det = ai1Ci1 + ai2Ci2 +...+ ainCin
        result += A[row][col]*cofactor_at(A, row, col)

    return result

def det(A):
    if not is_square_matrix(A):
        return None

    if len(A) == 1:
        return A[0][0] # determinant of a 1 x 1 matrix is the number itself
    elif len(A) == 2:
        # det = ad - bc
        d = len(A)-1
        return (A[0][0]*A[d][d]) - (A[0][1]*A[1][0])
    else:
        # det = cofactor expan. along optimal row/col
        optimalCol, colZeroCount = optimal_expansion_col(A)
        optimalRow, rowZeroCount = optimal_expansion_row(A)


        if colZeroCount > rowZeroCount:
            # Do cofactor expansion along the corresp. col
            result = cofactor_col_expansion(A, optimalCol)
            return result
        else:
            # Do cofactor expansion along the corresp. row
            result = cofactor_row_expansion(A, optimalRow)
            return result

def inverse_of(A) -> list[list[int]]:
    detOf = det(A)
    if detOf == 0:
        return None
    
    detOfInverse = 1/detOf
    adjointOf = adjoint(A)

    # inverse = (1/det(A))*adj(A)
    inverse = multiply_by_scalar(adjointOf, detOfInverse)
    return inverse

def is_identity(A) -> bool:
    # A must be a matrix
    if is_valid_matrix(A):
        
        # Matrix must be square
        if len(A) != len(A[0]):
            return False
        
        for r in range(0, len(A)):
            for c in range(0, len(A[0])):
                # Entry must be 0 if not on main diagonal
                if A[r][c] != 0 and r != c:
                    return False
                
                # Entry must be 1 if is on main diagonal
                if A[r][c] != 1 and r == c:
                    return False
                
        return True
    else:
        return False
    
def identity_of(A) -> list[list[int]]:
    for r in range(0, len(A)):
        for c in range(0, len(A[0])):
            if r==c:
                # Main diagonal set to 1s
                A[r][c] = 1
            
            else:
                # everywhere else set to 0s
                A[r][c] = 0
    return A

def multiply_by_scalar(A, scalar):
    if not is_valid_matrix(A):
        exit()

    B = copy.deepcopy(A)
    for row in range(0, len(B)):
        for col in range(0, len(B[row])):
            B[row][col] = scalar*B[row][col]

    return B

def sum_of(A, B):
    if not is_valid_matrix(A) or not is_valid_matrix(B):
        return None
    
    if len(A) != len(B):
        return None # The have to have the same dimension, addition is componentwise
    
    # Add corresponding components of B to A
    result = copy.deepcopy(A)
    for i in range(0, len(result)):
        for j in range(0, len(result[0])):
            result[i][j] += B[i][j]

    return result

def range_check(index, min, max):
    if index < min or index > max:
        print("Index out of range.")
        exit()

def display(matrix):
    # Output each component of the provided matrix
    for r in range(0, len(matrix)):
        for c in range(0, len(matrix[r])):
            print(matrix[r][c], end=" ")
        print("")
    print("")