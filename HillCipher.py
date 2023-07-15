import math
import copy

"""
Rules:
1. Pick an Encryption key: The encryption is a square matrix (N x N).
2. Group Plaintext chars: Group plaintext into groups of N chars and convert 
each char into decimal equivalent. Append "dummy" char for odd length plaintext.
3. Convert groups to vectors: Convert each group to a column vector and 
compute key x group (key matrix multiplied with each group vector)
4. Convert ciphertext vectors to to ciphertext: Convert each resulting 
vector product to ciphertext.

Decryption:
Same procedure except the key in the inverse matrix of the key matrix used 
to encrypt.
"""

class MatrixOperations:
    """ 
    Defines the ability to create matrices and column vectors, along with
    operations applicable on matrices such as inverses, multiplication and determinants.
    """

    def createSquareMatrix(self, intArray, N) -> list[list[int]]:
        if math.sqrt( len(intArray) ) != N:
            return None # cannot convert to square

        matrix = []
        # build each row: if N = 3, iterate 3 times to create 3 rows, for each row set the next 3 entries in intArray
        for counter in range(0, N, 1):
            # step through the array in 3s and set each triple as a new row into matrix
            matrix.append([intArray[i] for i in range(counter*N,(counter+1)*N)]) # select next 3 entries from intArray

        return matrix
    
    def __validMatrix(self, matrix):
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
    
    def isSquareMatrix(self, A):
        if not self.__validMatrix(A):
            return False
        
        # Must be n x n (row count = col count)
        if(len(A) != len(A[0])):
            return False
        
        return True

    def matrixProduct(self, A, B) -> list[int]:
        # store expected dimensions
        product = []

        # Check that matrices have dimension m x n; m > 0 and n > 0
        if (not self.__validMatrix(B)) or (not self.__validMatrix(A)):
            exit()

        # no. of cols of A must = no. of rows of B for product to be defined
        if len(A[0]) != len(B[0]):
            exit()

        # (AB)ij = ith row of A dot jth column of B
        # NOTE: B is actually a row vector ie. [[x, y, z,...]] we keep it so because it is easier to traverse,
        # but pretend it is a column vector since it can be translated as such
        for i in range(0, len(A)):
            for j in range(0, len(B)):
                #product.append((self.__dotProduct(A[i], B[j]) % 93 + 1) + 33)
                #product.append(self.__dotProduct(A[i], B[j]) % len(alphabet_map)) # limit to the number of alphabet chars COMMENT OUT
                #product.append((self.__dotProduct(A[i], B[j]) % 149191) + 1) # limit product to number of unicode chars represented
                product.append((self.__dotProduct(A[i], B[j]) % 149186 + 1)) # limit product to number of unicode chars represented
        
        return product


    def __dotProduct(self, rowVector, columnVector) -> int:
        # these must be the same length for dot product to be defined since it works entry wise
        if len(rowVector) != len(columnVector):
            exit()

        # dot product =  sum of v[i] * w[i] for all corresponding entries in v and w
        product = 0
        for i in range(0, len(rowVector)):
            product += rowVector[i] * columnVector[i]
        
        return product
    
    def gaussJordanElimination(self, A):
        # Forward phase
        # 1 - Find leftmost non zero column
        # 2 - Place row of non zero entry at the top
        # 3 - Introduce leading one from entry
        # 4 - Introduce zeros everywhere else in that column
        # 5 - Ignore row with leading one, work with next rows
        # repeating 1 to 4
        leftMostCol = 0
        topMostRow = 0
        found = False
        for col in range(0, len(A)):
            if found:
                break

            for row in range(0, len(A)):
                if A[row][col] != 0:
                    leftMostIndex = col
                    topMostRow = row
                    found = True
                    break      

        # Backward Phase
        # 1 - Start from the last row, introduce zeros above 
        # leading one (zeroes everywhere above in that column)
        # 2 - Move to the 2nd last row, find leading one and 
        # introduce zeros above it in the same column
        # 3 - Repeat until the first row

    def product(self, A, B):
        if not self.__validMatrix(A):
            exit()

        if not self.__validMatrix(B):
            exit()

        if not len(A[0]) == len(B):
            exit()

        # the dotproduct of row i of A with column j of B
        BTranspose = self.transpose(B) # We will extract the columns of B as row vectors (easier)
        product = []
        for row in range(0, len(A)):
            newRow = []
            for col in range(0, len(B[0])):
                dot = self.__dotProduct(A[row], BTranspose[col])
                newRow.append(dot)

            product.append(newRow)
        
        return product


    def transpose(self, A):
        # Entry at row i col j with entry at row j col i
        # For effeciency we traverse entries above XOR below 
        # the main diagonal (otherwise the process would be redundant)
        
        if not self.isSquareMatrix(A):
            return None

        B = copy.deepcopy(A)
        for row in range(0, len(B)):
            for col in range(row + 1, len(B[row])):
                # (a)ij = (a)ji, and (a)ji = (a)ij
                temp = B[row][col]
                B[row][col] = B[col][row]
                B[col][row] = temp

        return B

    def adjoint(self, A):
        if not self.isSquareMatrix(A):
            return None

        B = copy.deepcopy(A)
        for row in range(0, len(B)):
            for col in range(0, len(A)):
                B[row][col] = self.cofactorAt(A, row, col)

        return self.transpose(B)
    
    def optimalExpansionCol(self, A):
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
    
    def optimalExpansionRow(self, A):
        # Find the row with the most zeros
        maxRow = 0
        max = 0
        for row in range(0, len(A)):
            if A[row].count(0) > max:
                maxRow = row
                max = A[row].count(0)

        # Return the row index and the number of zeros
        return maxRow, max
    
    def submatrix(self, A, rowToOmit, colToOmit):
        # perform a deep copy of A that excludes all entries 
        # in the provided row and all entries in the provided col
        
        self.rangeCheck(rowToOmit, 0, len(A))
        self.rangeCheck(colToOmit, 0, len(A[0]))
        
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

    
    def cofactorAt(self, A, row, col):
        # Cij = (-1)^(i+j) x Mij, where Mij is the determinant
        # of the sub matrix obtained by eliminating the ith row and jth col
        return ((-1)**(row + col))*self.det(self.submatrix(A, row, col))

    def cofactorColExpansion(self, A, col):
        result = 0
        for row in range(0, len(A)):
            # result = det = a1jC1j + a2jC2j +...+ anjCnj
            result += A[row][col]*self.cofactorAt(A, row, col)

        return result
    
    def cofactorRowExpansion(self, A, row):
        result = 0
        for col in range(0, len(A[row])):
            # result = det = ai1Ci1 + ai2Ci2 +...+ ainCin
            result += A[row][col]*self.cofactorAt(A, row, col)

        return result

    def det(self, A):
        if not self.isSquareMatrix(A):
            return None

        if len(A) == 1:
            return A[0][0] # determinant of a 1 x 1 matrix is the number itself
        elif len(A) == 2:
            # det = ad - bc
            d = len(A)-1
            return (A[0][0]*A[d][d]) - (A[0][1]*A[1][0])
        else:
            # det = cofactor expan. along optimal row/col
            optimalCol, colZeroCount = self.optimalExpansionCol(A)
            optimalRow, rowZeroCount = self.optimalExpansionRow(A)


            if colZeroCount > rowZeroCount:
                # Do cofactor expansion along the corresp. col
                result = self.cofactorColExpansion(A, optimalCol)
                return result
            else:
                # Do cofactor expansion along the corresp. row
                result = self.cofactorRowExpansion(A, optimalRow)
                return result

    def inverseOf(self, A) -> list[list[int]]:
        detOf = self.det(A)
        if detOf == 0:
            return None
        
        detOfInverse = 1/detOf
        adjointOf = self.adjoint(A)

        # inverse = (1/det(A))*adj(A)
        inverse = self.multiplyByScalar(adjointOf, detOfInverse)
        return inverse
    
    def isIdentity(self, A) -> bool:
        # A must be a matrix
        if self.__validMatrix(A):
            
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
        
    def identityOf(self, A) -> list[list[int]]:
        for r in range(0, len(A)):
            for c in range(0, len(A[0])):
                if r==c:
                    # Main diagonal set to 1s
                    A[r][c] = 1
                
                else:
                    # everywhere else set to 0s
                    A[r][c] = 0
        return A
    
    def multiplyByScalar(self, A, scalar):
        if not self.__validMatrix(A):
            exit()

        B = copy.deepcopy(A)
        for row in range(0, len(B)):
            for col in range(0, len(B[row])):
                B[row][col] = scalar*B[row][col]

        return B

    def _multiplyByScalar(self, A, row, scalar):
        self.rangeCheck(row-1, 0, len(A)-1)

        scalarMultiple = copy.deepcopy(A)

        for c in range(0, len(scalarMultiple[0])):
                scalarMultiple[row-1][c] *= scalar

        return scalarMultiple

    def _addScalarMultiple(self, A, subjectRow, objectRow, scalar):
        self.rangeCheck(subjectRow-1, 0, len(A)-1)
        self.rangeCheck(objectRow-1, 0, len(A)-1)

        scalaMultiple = self._multiplyByScalar(A, objectRow, scalar)
        matrixCopy = copy.deepcopy(A)
        
        for c in range(0, len(matrixCopy[0])):
            matrixCopy[subjectRow-1][c] += scalaMultiple[objectRow-1][c]
        
        return matrixCopy

    def sumOf(self, A, B):
        if not self.__validMatrix(A) or not self.__validMatrix(B):
            return None
        
        if len(A) != len(B):
            return None # The have to have the same dimension, addition is componentwise
        
        # Add corresponding components of B to A
        result = copy.deepcopy(A)
        for i in range(0, len(result)):
            for j in range(0, len(result[0])):
                result[i][j] += B[i][j]

        return result
        

    def _interchangeRows(self, A, rowFirst, rowSecond) -> list[list[int]]:
        self.rangeCheck(rowFirst-1, 0, len(A)-1)
        self.rangeCheck(rowSecond-1, 0, len(A)-1)
        
        matrixCopy = copy.deepcopy(A)

        temp = matrixCopy[rowFirst-1]
        matrixCopy[rowFirst-1] = matrixCopy[rowSecond-1]
        matrixCopy[rowSecond-1] = temp

        return matrixCopy
    
    def rangeCheck(self, index, min, max):
        if index < min or index > max:
            print("Index out of range.")
            exit()

    def display(self, matrix):
        # Output each component of the provided matrix
        for r in range(0, len(matrix)):
            for c in range(0, len(matrix[r])):
                print(matrix[r][c], end=" ")
            print("")
        print("")


def convertToDecimalArr(text) -> list[int]:
    # create a list of correspondinf ASCII decimals from provided text's chars
    return [ord(c) for c in text]
    
    
def getSquareLen(currentLen):
    squareRoot = math.sqrt(currentLen)

    # Is the length a perfect square
    if squareRoot % 1 > 0:
        # Find the closest perfect square M > currentLen
        # rounding up the sqrt of currentLen should give the next perfect square
        return int(squareRoot + 1)
    else:
        return int(squareRoot)
    
def makeSquareLength(key):
    # The key will be turned into a square matrix; The length needs to 
    # be perfectly squre 9 = 3 x 3, 16 = 4 x 4

    squareLen = int(math.sqrt( len(key) )) # current
    reqSquareLen = getSquareLen( len(key) ) # necessary

    # current != necessary ?
    suffixChar = key[len(key)-1] # Adjust by duplicating last char if string not long enough
    if squareLen != reqSquareLen: # if not equal it will be less
        key += suffixChar * ((reqSquareLen**2)-len(key)) # add missing chars to make perfect square (reqSquareLen**2 equals required length )

    return key

def convertMsgToGroups(plaintext, groupSize): 
    # We need to have equal groups
    textLen = len(plaintext)
    suffixChar = plaintext[len(plaintext)-1] # duplicate last char to make text long enough
    if textLen % groupSize > 0:
        # ex. if remaind = 3 then 3 chars are appended to be able to 
        # make equal groups
        plaintext += suffixChar * (groupSize - (textLen % groupSize))

    # Convert to decimals
    decimals = convertToDecimalArr(plaintext)

    # Convert to groups of size groupSize
    plaintextGroups = []
    # Extract subsets of size (groupSize) from decimals array
    for index in range(0, len(decimals), groupSize):
        plaintextGroups.append(decimals[index:index+groupSize])

    return plaintextGroups

def convertToText(cipherGroups):
    # Traverse each group, convert each decimal in group to unicode char, string together all the chars
    ciphertext = ""
    for group in cipherGroups:
        #alphabets = list(alphabet_map.keys()) # COMMENT OUT
        for i in range(0, len(group)):
            #ciphertext += alphabets[int(group[i])-1] # "-1" Alphabets list (not dict) starts at 0 (indexed) COMMENT OUT
            ciphertext += chr(group[i])

    return ciphertext

def round(number):
    # round off to the nearest whole number. Round up in case of x.5
    if number % 1 >= 0.5:
        return int(number + 1)
    
    return int(number)

def fixDecryptError(A):
    # Correct the precision error in the decryption output

    result = copy.deepcopy(A)
    for i in range(0, len(A)):
        for j in range(0, len(A[0])):
            result[i][j] = int(round( result[i][j] - 1 )) # round(decimal - 1)

    return result

def encrypt(message, key):
    global Original

    # Step 1 - Select Key
    key = makeSquareLength(key)
    squareLen = getSquareLen( len(key) ) 

    # Step 2, 3 - Group plaintext chars, converto to decimal 
    plaintextGroups = convertMsgToGroups(message, squareLen)

    matrixOps = MatrixOperations()
    keyMatrix = convertToDecimalArr(key)
    keyMatrix = matrixOps.createSquareMatrix(keyMatrix, squareLen)

    # Step 3 - Convert groups to vectors, Compute the Ciphetext groups: keyMatrix x plaintextGroup[i]
    cipherGroups = []
    Original = plaintextGroups
    for group in plaintextGroups:
        columnVector = [group] # Turn into a vector, necessary to pass isValidMatrix check
        cipherGroups.append(matrixOps.matrixProduct(keyMatrix, columnVector))

    # Step 4 - Convert cipher groups to ciphertext
    ciphertext = convertToText(cipherGroups)
    return ciphertext

def decrypt(message, key):
    # Apply the encryption again, but this time converting the key to it's inverse
    # and using it as the key for encryption (this will effect decryption - reverse encryption)

    # Step 1 - Select Key
    key = makeSquareLength(key)
    squareLen = getSquareLen( len(key) ) 

    # Step 2, 3 - Group plaintext chars, converto to decimal 
    cipherTextGroups = convertMsgToGroups(message, squareLen)

    matrixOps = MatrixOperations()
    keyMatrix = convertToDecimalArr(key)
    keyMatrix = matrixOps.createSquareMatrix(keyMatrix, squareLen)
    keyInverse = matrixOps.inverseOf(keyMatrix)

    #identity = matrixOps.product(keyMatrix, keyInverse)
    #matrixOps.display(identity)

    # Step 3 - Convert groups to vectors, Compute the Ciphetext groups: keyInverse x plaintextGroup[i]
    plaintextGroups = []
    for group in cipherTextGroups:
        columnVector = [group] # Turn into a vector, necessary to pass isValidMatrix check
        plaintextGroups.append(matrixOps.matrixProduct(keyInverse, columnVector))

    # Step 4 - Convert cipher groups to ciphertext
    plaintextGroups = fixDecryptError(plaintextGroups)
    plaintext = convertToText(plaintextGroups)
    return plaintext

def main():
    print("Welcome to HushChat!")
    try:
        key = "Illya@123omega"
        while True:
            message = input("(Max 255 chars) Ctrl-C to exit \n<message> : ")[:255] # max 255 chars input
            ciphertext = encrypt(message, key)
            plaintext = decrypt(ciphertext, key)

            print(f"Ciphertext:\t{ciphertext}\n") 
            print(f"Plaintext:\t{plaintext}\n")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":

#    operations = MatrixOperations()
#    matrix = [[1, 7, 3],[0, 1, -2], [1, 0, 1]]
#    identity = [[1, 0, 0],[0, 1, 0],[0, 0, 1]]
#    inverse = operations.inverseOf(matrix)
    
#    operations.display(matrix)
#    if not inverse:
#        print("Adjoint for matrix is undefined.")
    
#    else:
#        operations.display(inverse)
#        test = operations.product(matrix, inverse)
#        operations.display(test)

    main()

#TODO: Fix row and col: row-1 where indexing for example, and
# row in range(1, x) when traversing
#TODO: Check bounds of rows and cols: especially at submatrix func.

#TODO: Encryption steps class
#TODO: Inverse of matrix
#TODO: Fix transpose computation; considers only square matrices