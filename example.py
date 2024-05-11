from crypto.key import Key
from crypto.algorithm.present80 import PRESENT80
from crypto.util import *

"""
    Test vectors are from https://iacr.org/archive/ches2007/47270450/47270450.pdf.
    They can be found in Appendix I (which is page 16).

    [Output]
    $ python example.py
    KEY        : 00000000000000000000
    PLAIN TEXT : 0000000000000000
    CIPHER TEXT: 5579c1387b228445

    KEY        : ffffffffffffffffffff
    PLAIN TEXT : 0000000000000000
    CIPHER TEXT: e72c46c0f5945049

    KEY        : 00000000000000000000
    PLAIN TEXT : ffffffffffffffff
    CIPHER TEXT: a112ffc72f68417b

    KEY        : ffffffffffffffffffff
    PLAIN TEXT : ffffffffffffffff
    CIPHER TEXT: 3333dcd3213210d2
"""

# Toggle spaces between bytes while printing
# out stuff.
ADD_SPACE_BETWEEN_BYTES = False

# Key.
key        = Key(bytes([ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ]))

# Plain text.
plain_text = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

# PRESENT-80 cipher.
present80  = PRESENT80(key)

# Encrypted plain text.
cipher     = present80.encrypt(plain_text)

# Print the results.
printp("KEY        :", key.as_str(ADD_SPACE_BETWEEN_BYTES))
printp("PLAIN TEXT :", hex(plain_text, ADD_SPACE_BETWEEN_BYTES))
printp("CIPHER TEXT:", hex(cipher, ADD_SPACE_BETWEEN_BYTES))
print()

key        = Key(hex_str_bytes("FFFFFFFFFFFFFFFFFFFF"))
plain_text = hex_str_bytes("0000000000000000")
present80  = PRESENT80(key)
cipher     = present80.encrypt(plain_text)

printp("KEY        :", key.as_str(ADD_SPACE_BETWEEN_BYTES))
printp("PLAIN TEXT :", hex(plain_text, ADD_SPACE_BETWEEN_BYTES))
printp("CIPHER TEXT:", hex(cipher, ADD_SPACE_BETWEEN_BYTES))
print()

key        = Key(hex_str_bytes("00000000000000000000"))
plain_text = hex_str_bytes("FFFFFFFFFFFFFFFF")
present80  = PRESENT80(key)
cipher     = present80.encrypt(plain_text)

printp("KEY        :", key.as_str(ADD_SPACE_BETWEEN_BYTES))
printp("PLAIN TEXT :", hex(plain_text, ADD_SPACE_BETWEEN_BYTES))
printp("CIPHER TEXT:", hex(cipher, ADD_SPACE_BETWEEN_BYTES))
print()

key        = Key(bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]))
plain_text = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
present80  = PRESENT80(key)
cipher     = present80.encrypt(plain_text)

printp("KEY        :", key.as_str(ADD_SPACE_BETWEEN_BYTES))
printp("PLAIN TEXT :", hex(plain_text, ADD_SPACE_BETWEEN_BYTES))
printp("CIPHER TEXT:", hex(cipher, ADD_SPACE_BETWEEN_BYTES))
print()
