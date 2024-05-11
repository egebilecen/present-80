This repository contains the implementation of the encryption algorithm of the PRESENT-80 lightweight block cipher. It features a fully commented code with many utility functions to implement the algorithm. This code is written for educational purposes; thus, it shouldn't be used for production, as it's not written with optimization in mind.

**Note:**
* This code only supports 80-bit key.
* Decryption is not implemented, as it's just the reverse operation of encryption.
* No padding scheme is implemented; thus, only data with the exact size of the block can be encrypted.
