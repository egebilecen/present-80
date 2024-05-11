from typing import Literal
from secrets import token_bytes
from .util import hex

"""
    Key class that contains functions to work with key.
"""
class Key:
    """
        This function generates a key from given size.
        Size must be a multiple of 8.
    """
    @staticmethod
    def generate(size: int) -> bytes:
        if size == 0 or size % 8 != 0:
            raise ValueError("Size must be a multiple of 8 and it cannot be 0.")
        
        key: bytes = token_bytes(int(size / 8))
        
        return key

    """
        Constructor of the class. It takes a size as parameter
        which determines the size of the key.
    """
    def __init__(self, key_or_size: bytes | int, byte_order: Literal["big", "little"] = "big") -> None:
        if isinstance(key_or_size, bytes):
            self._size: int  = len(key_or_size) * 8
            self._key: bytes = key_or_size
        elif isinstance(key_or_size, int):
            self._size = key_or_size
            self._key: bytes = Key.generate(key_or_size)
        else:
            raise ValueError("key_or_size value is not valid!")
        
        self._byte_order: Literal["big", "little"] = byte_order

    """
        Returns a copy of the key bytes.
    """
    def as_bytes(self) -> bytes:
        return self._key
    
    """
        Returns the key as an int.
    """
    def as_int(self) -> int:
        return int.from_bytes(self.as_bytes(), self._byte_order)

    """
        Converts key bytes to readable string.
    """
    def as_str(self, is_spaced: bool = True) -> str:
        return hex(self._key, is_spaced)

    """
        Return the size of the key in bits.
    """
    def size(self) -> int:
        return self._size
