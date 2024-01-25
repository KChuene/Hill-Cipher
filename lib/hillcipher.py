import math, copy

import numpy as np

# from .matrixops import *
from .matrixops_np import *

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

def convert_to_decimal_array(text) -> list[int]:
    # create a list of correspondinf ASCII decimals from provided text's chars
    return [ord(c) for c in text]
    
    
def get_square_length(currentLen):
    squareRoot = math.sqrt(currentLen)

    # Is the length a perfect square
    if squareRoot % 1 > 0:
        # Find the closest perfect square M > currentLen
        # rounding up the sqrt of currentLen should give the next perfect square
        return int(squareRoot + 1)
    else:
        return int(squareRoot)
    
def make_square_length(key):
    # The key will be turned into a square matrix; The length needs to 
    # be perfectly squre 9 = 3 x 3, 16 = 4 x 4

    squareLen = int(math.sqrt( len(key) )) # current
    reqSquareLen = get_square_length( len(key) ) # necessary

    # current != necessary ?
    suffixChar = key[len(key)-1] # Adjust by duplicating last char if string not long enough
    if squareLen != reqSquareLen: # if not equal it will be less
        key += suffixChar * ((reqSquareLen**2)-len(key)) # add missing chars to make perfect square (reqSquareLen**2 equals required length )

    return key

def convert_msg_to_groups(plaintext, groupSize): 
    # We need to have equal groups
    textLen = len(plaintext)
    suffixChar = plaintext[len(plaintext)-1] # duplicate last char to make text long enough
    if textLen % groupSize > 0:
        # ex. if remaind = 3 then 3 chars are appended to be able to 
        # make equal groups
        plaintext += suffixChar * (groupSize - (textLen % groupSize))

    # Convert to decimals
    decimals = convert_to_decimal_array(plaintext)

    # Convert to groups of size groupSize
    plaintextGroups = []
    # Extract subsets of size (groupSize) from decimals array
    for index in range(0, len(decimals), groupSize):
        plaintextGroups.append(decimals[index:index+groupSize])

    return plaintextGroups

def convert_ciphergroups_to_text(cipherGroups):
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

def fix_decrypt_error(A):
    # Correct the precision error in the decryption output

    result = copy.deepcopy(A)
    for i in range(0, len(A)):
        for j in range(0, len(A[0])):
            result[i][j] = int(round( result[i][j] - 1))

    return result

def encrypt(message, key_str):
    global Original

    # Step 1 - Select Key
    key_str = make_square_length(key_str)
    square_len = get_square_length( len(key_str) )

    # Step 2, 3 - Group plaintext chars, converto to decimal 
    plaintext_groups = convert_msg_to_groups(message, square_len)

    key_matrix = convert_to_decimal_array(key_str)
    key_matrix = create_square_matrix(key_matrix, square_len)

    if np.linalg.det(key_matrix) == 0:
        print("<Warning> Provided key not invertible cannot decrypt encrypted text.")

    # Step 3 - Convert groups to vectors, Compute the Ciphetext groups: keyMatrix x plaintextGroup[i]
    cipher_groups = []
    original = plaintext_groups
    for group in plaintext_groups:
        column_vector = [group] # Turn into a vector, necessary to pass isValidMatrix check
        cipher_groups.append(matrix_product(key_matrix, column_vector))

    # Step 4 - Convert cipher groups to ciphertext
    ciphertext = convert_ciphergroups_to_text(cipher_groups)
    return ciphertext

def decrypt(message, key_str):
    # Apply the encryption again, but this time converting the key to it's inverse
    # and using it as the key for encryption (this will effect decryption - reverse encryption)

    # Step 1 - Select Key
    key_str = make_square_length(key_str)
    square_len = get_square_length( len(key_str) )

    # Step 2, 3 - Group plaintext chars, converto to decimal 
    ciphertext_groups = convert_msg_to_groups(message, square_len)

    key_matrix = convert_to_decimal_array(key_str)
    key_matrix = create_square_matrix(key_matrix, square_len)

    key_matrix_inv = identity_of(key_matrix)
    if np.linalg.det(key_matrix) == 0:
        print("<Warning> Provided key not invertible cannot decrypt encrypted text.")
    else:
        key_matrix_inv = np.linalg.inv(key_matrix)

    # Step 3 - Convert groups to vectors, Compute the Ciphetext groups: keyInverse x plaintextGroup[i]
    plaintext_groups = []
    for group in ciphertext_groups:
        column_vector = [group] # Turn into a vector, necessary to pass isValidMatrix check
        plaintext_groups.append(matrix_product(key_matrix_inv, column_vector))

    # Step 4 - Convert cipher groups to ciphertext
    plaintext_groups = fix_decrypt_error(plaintext_groups)
    plaintext = convert_ciphergroups_to_text(plaintext_groups)
    return plaintext


# Fixes
#TODO: Inverse of matrix
#TODO: Fix transpose computation; considers only square matrices

# Advancements
#TODO: Add accuracy testing module. To test accuracy of decryption by 
# comparing initial input with decryption output.
#TODO: Add option handling module. (option examples: --encrypt, --decrypt, 
# --accuracy-test)
#TODO: Add file encryption module. Extends encryption to files, producing encrypted 
# outputs of original files.