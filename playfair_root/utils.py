# External imports
import string

# Internal imports

# Constants
MAX_KEY_LEN = 25
MATRIX_ROW_SIZE = 5
MATRIX_COL_SIZE = 5
BOGUS_LETTER = 'X'
FILLER_LETTER = 'Z'


def check_alphabet(text):
    for character in text:
        if character not in list(string.ascii_uppercase):
            return False
    return True


def key_verifier(key):
    if not check_alphabet(key):
        raise Exception('The allowed alphabet consists only of the capital English letters.')

    if len(key) > MAX_KEY_LEN:
        raise Exception(f'The maximum allowed secret key lehgth is {MAX_KEY_LEN}.')

    if len(key) == 0:
        raise Exception(f'The secret key field cannot be empty.')

    return True


def text_verifier(text):
    if not check_alphabet(text):
        raise Exception('The allowed alphabet consists only of the capital English letters.')

    return True


def find_index(element, matrix):
    for i in range(MATRIX_ROW_SIZE):
        for j in range(MATRIX_COL_SIZE):
            if matrix[i][j] == element:
                return i, j
