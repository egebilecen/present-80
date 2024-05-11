from typing import Any, Optional, Literal
from codecs import decode

"""
    Convert hex string into bytes.

    DEADC0DE -> [0xDE, 0xAD, 0xC0, 0xDE]
"""
def hex_str_bytes(hex_str: str) -> bytes:
    return decode(hex_str, "hex")

"""
    Converts byte array into hex string.

    [0xDE, 0xAD, 0xC0, 0xDE] -> DE AD C0 DE
"""
def hex(bytes_or_num: bytes | int, is_spaced = True, len: int = 4, order: Literal["big", "little"] = "big", signed = False) -> str:
    if isinstance(bytes_or_num, int):
        bytes_or_num = int.to_bytes(bytes_or_num, len, order, signed=signed)

    return (" " if is_spaced else "").join(["{:02x}".format(byte) for byte in bytes_or_num])

"""
    Converts byte array into bhex string saparated
    into blocks.

    For example (width = 4):
    [0xDE, 0xAD, 0xC0, 0xDE, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07] ->
    DE AD C0 DE
    00 01 02 03
    04 05 06 07
"""
def hex_block(bytes_or_num: bytes | int, width = 16, length: int = 4, order: Literal["big", "little"] = "big", signed = False) -> str:
    if isinstance(bytes_or_num, int):
        bytes_or_num = int.to_bytes(bytes_or_num, length, order, signed=signed)

    hex_block: list[str] = []

    for i, byte in enumerate(bytes_or_num):
        byte_str: str = "{:02x}".format(byte)

        if (i + 1) % width != 0:
            byte_str += " "
        elif i != len(bytes_or_num) - 1:
            byte_str += "\n"

        hex_block.append(byte_str)

    return "".join(hex_block)

"""
    Converts number into binary string.
"""
def binary(num: Any, width: Optional[int] = None) -> str:
    text: str = bin(num).replace("0b", "")

    if width is not None:
        text = text.zfill(width)

    return text

"""
    Prints padded text.
"""
def printp(title: str = "", text: str = ""):
    if title == "" and text == "":
        print()
        return

    title_width: int = 13
    title_adjusted: str = title.ljust(title_width)

    print(title_adjusted, end="")
    print(text, end="")
    print()
