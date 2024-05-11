from crypto.util import *

"""
    Generate a number that has all their bits set to 1
    up to size.

    For example:
    bit_ones(8) -> 11111111
"""
def bit_ones(size: int) -> int:
    num: int = 0x00

    for i in range(0, size):
        num |= (1 << i)

    return num

"""
    Rotates the bits of the given number to the left.
"""
def rotate_left(num: int, bits: int, width: int) -> int:
    if bits > width:
        bits = bits % width

    # Preserve the bits that otherwise would be lost when shifted to
    # the left.
    preserved_bits: int = (num & (bit_ones(bits) << (width - bits))) >> (width - bits)

    # Group of bits that can be safely shifted to left without worry
    # of losing bits.
    bits_to_shift: int  = num & (bit_ones(width - bits))

    rotated: int = (bits_to_shift << bits) | preserved_bits

    return rotated

"""
    Rotates the bits of the given number to the right.
"""
def rotate_right(num: int, bits: int, width: int) -> int:
    if bits > width:
        bits = bits % width

    # Preserve the bits that otherwise would be lost when shifted to
    # the right.
    preserved_bits: int = num & bit_ones(bits)

    # Group of bits that can be safely shifted to right without worry
    # of losing bits.
    bits_to_shift: int  = num & (bit_ones(width - bits) << bits)

    rotated: int = (bits_to_shift >> bits) | (preserved_bits << (width - bits))

    return rotated
