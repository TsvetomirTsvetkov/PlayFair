# External imports
import string

# Internal imports
from .utils import *


class PlayFair:
    '''Class containing the PlayFair algorithm implementation'''

    def __init__(self, key, plain_text='', cipher_text=''):
        # Check the given strings
        key_verifier(key)
        text_verifier(plain_text)
        text_verifier(cipher_text)

        # Save the key & plain_text or key & cipher_text
        self.key = key
        self.plain_text = plain_text
        self.cipher_text = cipher_text

        # Create the plain text pairs if needed
        self.plain_pairs = self._seperate_letters(self.plain_text)

        # Create the cipher text pairs if needed
        self.cipher_pairs = self._seperate_letters(self.cipher_text)

        # Generate the matrix
        self.matrix = self.generate_matrix()

        # Set the encryption flag to True
        self.encrypt_flag = True

    def generate_matrix(self):
        # Create an empty matrix
        matrix = [[None for i in range(MATRIX_COL_SIZE)] for j in range(MATRIX_ROW_SIZE)]

        # Prepare indexes
        idx_key = 0
        idx_alphabet = 0
        alphabet = list(string.ascii_uppercase)

        # Handle I/J case
        alphabet.remove('J')

        # Replace J occurances
        key_replaced = self.key.replace('J', 'I')

        # Simpify key
        key_simplified = "".join(dict.fromkeys(key_replaced))

        # Fill the matrix
        for i in range(MATRIX_ROW_SIZE):
            for j in range(MATRIX_COL_SIZE):
                if idx_key < len(key_simplified):
                    matrix[i][j] = key_simplified[idx_key]
                    alphabet.remove(key_simplified[idx_key])
                else:
                    matrix[i][j] = alphabet[idx_alphabet]
                    idx_alphabet += 1
                idx_key += 1

        # Return the filled matrix
        return matrix

    def _seperate_letters(self, text):
        # Split the plain text into list of characters
        text_list = list(text)

        # Add bogus letter where needed
        for idx in range(len(text_list) - 1):
            if text_list[idx] == text_list[idx + 1] and idx % 2 == 0:
                text_list.insert(idx + 1, BOGUS_LETTER)

        # Fill the last element when needed
        if len(text_list) % 2 != 0:
            if text_list[-1] != FILLER_LETTER:
                text_list.append(FILLER_LETTER)
            else:
                text_list.append(BOGUS_LETTER)

        # Create the pairs
        first_elements = text_list[::2]
        second_elements = text_list[1::2]

        pairs = [[first_elements[i], second_elements[i]] for i in range(len(first_elements))]

        # Return the list of pairs
        return pairs

    def encrypt(self):
        self.encrypt_flag = True
        self.cipher_text = ''
        self.cipher_pairs = []

        # Go through all of the pairs
        for pair in self.plain_pairs:
            # Find the indexes in the matrix
            e1_x, e1_y = find_index(pair[0], self.matrix)
            e2_x, e2_y = find_index(pair[1], self.matrix)

            # Checks based on the rules
            if e1_x == e2_x:
                cipher_pair = self._encrypt_decrypt_row(e1_x, e1_y, e2_x, e2_y)
            elif e1_y == e2_y:
                cipher_pair = self._encrypt_decrypt_col(e1_x, e1_y, e2_x, e2_y)
            else:
                cipher_pair = self._encrypt_decrypt_rec(e1_x, e1_y, e2_x, e2_y)

            # Append the cipher pair
            self.cipher_pairs.append(cipher_pair)

        # Create a string out of the pairs
        self._fill_plain_cipher_text()

        return self.cipher_text

    def decrypt(self):
        self.encrypt_flag = False
        self.plain_text = ''
        self.plain_pairs = []

        for pair in self.cipher_pairs:
            # Find the indexes in the matrix
            e1_x, e1_y = find_index(pair[0], self.matrix)
            e2_x, e2_y = find_index(pair[1], self.matrix)

            # Checks based on the rules
            if e1_x == e2_x:
                plain_pair = self._encrypt_decrypt_row(e1_x, e1_y, e2_x, e2_y)
            elif e1_y == e2_y:
                plain_pair = self._encrypt_decrypt_col(e1_x, e1_y, e2_x, e2_y)
            else:
                plain_pair = self._encrypt_decrypt_rec(e1_x, e1_y, e2_x, e2_y)

            # Append the cipher pair
            self.plain_pairs.append(plain_pair)

        # Create a string out of the pairs
        self._fill_plain_cipher_text()

        return self.plain_text

    def _encrypt_decrypt_col(self, e1_x, e1_y, e2_x, e2_y):
        # Create an empty list
        pair = []

        if self.encrypt_flag:
            pair.append(self.matrix[(e1_x + 1) % 5][e1_y])
            pair.append(self.matrix[(e2_x + 1) % 5][e2_y])
        else:
            pair.append(self.matrix[(e1_x - 1) % 5][e1_y])
            pair.append(self.matrix[(e2_x - 1) % 5][e2_y])

        return pair

    def _encrypt_decrypt_row(self, e1_x, e1_y, e2_x, e2_y):
        # Create an empty list
        pair = []

        if self.encrypt_flag:
            pair.append(self.matrix[e1_x][(e1_y + 1) % 5])
            pair.append(self.matrix[e2_x][(e2_y + 1) % 5])
        else:
            pair.append(self.matrix[e1_x][(e1_y - 1) % 5])
            pair.append(self.matrix[e2_x][(e2_y - 1) % 5])

        # Return the pair
        return pair

    def _encrypt_decrypt_rec(self, e1_x, e1_y, e2_x, e2_y):
        return [self.matrix[e1_x][e2_y], self.matrix[e2_x][e1_y]]

    def _fill_plain_cipher_text(self):
        if self.encrypt_flag:
            # Fill the cipher_text variable
            for pair in self.cipher_pairs:
                self.cipher_text += pair[0] + pair[1]
        else:
            for pair in self.plain_pairs:
                self.plain_text += pair[0] + pair[1]
