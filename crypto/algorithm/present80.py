from typing import Literal
from crypto.key import Key
from crypto.math import *

"""
    PRESENT-80 algorithm class.
"""
class PRESENT80:
    """
        Substitution box definition.
    """
    _substitution_box: bytes = bytes([
        0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2
    ])

    """
        Permutation box definition.
    """
    _permutation_box: bytes = bytes([
         0, 16, 32, 48,  1, 17, 33, 49,  2, 18, 34, 50,  3, 19, 35, 51,
         4, 20, 36, 52,  5, 21, 37, 53,  6, 22, 38, 54,  7, 23, 39, 55,
         8, 24, 40, 56,  9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
        12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63
    ])

    """
        Constructor of the class. Expects a Key class object.
    """
    def __init__(self, key: Key) -> None:
        if key.size() != 80:
            raise ValueError("PRESENT-80 algorithm expects a 80-bit key.")

        self._key: Key = key
        self._rounds: int = 32

    """
        Generates round key list to be used in each round.
    """
    def _generate_round_keys(self) -> list[int]:
        # Generated round keys will be stored in this variable.
        round_keys: list[int] = []

        # User supplied 80 bit key is stored in this register.
        key_reg: int = self._key.as_int()

        # Extract round key.
        #
        # Round key is the leftmost 64 bit of the current bits
        # of the key in register which means we can just shift
        # it to the right by 16 bits to get 64 bit.
        round_keys.append(key_reg >> 16)

        # Round 1, 2, 3, ..., self._rounds - 1, i.e., we will loop
        # for 31 times in case of self._rounds == 32.
        for i in range(1, self._rounds):
            # Update key register.
            #
            # Key register is rotated to left by 61 bit positions
            # which is equivalent to rotating to right by 19 bit
            # positions.
            key_reg = rotate_right(key_reg, 19, 80)

            # Leftmost four bits are passed through substitution
            # box.
            key_reg = (key_reg & ~(0x0F << 76)) | (self._substitution_box[key_reg >> 76] << 76)
            
            # The 5 bits at bit location 19, 18, 17, 16, 15 of the key in the register
            # are XORed with the 5-bit round_counter value i.
            key_reg = key_reg ^ (i << 15)

            # Extract round key.
            round_keys.append(key_reg >> 16)

        return round_keys
    
    """
        Updates the state with the round key.
    """
    def _add_round_key(self, state: int, key: int) -> int:
        # State is updated by XORing the state with key.
        return state ^ key
    
    """
        Applies substitution layer to the state.
    """
    def _substitution_layer(self, state: int) -> int:
        # Substituted state will be stored in this variable.
        substituted_state = 0x00

        for i in range(16):
            # In each iteration, in order to get current 4-bit word,
            # we will need to create a mask. shift variable holds the
            # value that tells us how many times we need to shift to
            # left or right in order to get right piece of bits.
            shift  = i * 4

            # Mask to get target 4-bit based on current iteration.
            mask   = 0x0F << shift

            # Our target 4-bit to put into substitution box.
            nibble = (state & mask) >> shift

            # Save the substituted value into variable.
            substituted_state |= self._substitution_box[nibble] << shift

        return substituted_state

    """
        Applies permutation layer to the state.
    """
    def _permutation_layer(self, state: int) -> int:
        # Permutated state will be stored in this variable.
        permutated_state = 0x00

        # We will iterate for 8 times and will take 8 bits each time
        # from the state.
        # And then we will iterate over the taken byte for 8 times
        # and grab one bit at a time and place it into new location
        # based on permutation box.
        for i in range(8):
            # How many times should we shift to get the relevant byte
            # stored in this variable.
            shift = i * 8

            # Relevant byte to read it's bits and permutate them.
            byte  = (state & (0xFF << shift)) >> shift

            for j in range(8):
                # Calculate the bit's position.
                pos = (i * 8) + j

                # Get the bit j.
                bit = 1 if byte & (0x01 << j) else 0
                
                # Get the new position of bit j.
                new_pos = self._permutation_box[pos]

                # Move the bit.
                permutated_state |= bit << new_pos

        return permutated_state

    """
        Encrypts the given byte array using PRESENT algorithm.
    """
    def encrypt(self, byte_arr: bytes, byte_order: Literal["big", "little"] = "big") -> bytes:
        if len(byte_arr) * 8 != 64:
            raise ValueError("PRESENT-80 can only encrypt 64-bits.")

        # Convert bytes to int so we can perform operations much easily.
        state: int = int.from_bytes(byte_arr, byte_order)

        # Generate round keys to be used in each round.
        rounds_keys: list[int] = self._generate_round_keys()

        # Iterate for self._rounds rounds.
        for i in range(1, self._rounds + 1):
            # Add round key into state.
            state = self._add_round_key(state, rounds_keys[i - 1])
            
            # Not last round, apply substitution and permutation
            # layers.
            if i != self._rounds:
                state = self._substitution_layer(state)
                state = self._permutation_layer(state)

        # Convert the state back to byte array and return it.
        return int.to_bytes(state, 8, byteorder=byte_order)