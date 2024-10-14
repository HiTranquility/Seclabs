# DES Brute-force Decryption Script

This script is designed to brute-force the decryption key for a DES-encrypted ciphertext. It leverages the `pycryptodome` library to perform DES decryption in ECB mode and iterates over possible combinations of unknown bytes in the key.

## Table of Contents

- [Description](#description)
- [Dependencies](#dependencies)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [Output](#output)
- [Notes](#notes)

## Description

The script attempts to decrypt the following ciphertext: ce126d2ddf2d1e64


A partial key is provided: `[?, ?, ?, ?, E5, F6, 66, ?]`. The script uses brute-force to find the unknown bytes (positions 0-3 and 7) of the 8-byte DES key and checks if the decrypted plaintext matches a specific pattern.

### Key Specifications:
- **Key Size**: 64 bits (8 bytes)
- **Block Size**: 8 bytes
- **Mode**: ECB (Electronic Codebook)

The pattern being searched for in the decrypted plaintext is: `"[A-Z]{4} [A-Z]{4}"` — two sets of four uppercase letters separated by a space (e.g., `"TEST TEST"`).

## Dependencies

Before running the script, ensure the following libraries are installed one by one:

```bash
pip install wheel
pip install pycryptodome
```

## How It Works

1. **Brute-force Key Generation**:  
   The script generates all possible 5-byte combinations, as only the first four bytes and the last byte of the DES key are unknown. The known middle three bytes are fixed as `229, 246, 102`. This process is done using Python’s `itertools.product` to iterate through all possible values of the unknown bytes, which range from `0` to `255` (i.e., one byte).
   
   ```python
   for keyGen in product(range(256), repeat=5):
       key = bytearray((keyGen[0], keyGen[1], keyGen[2], keyGen[3], 229, 246, 102, keyGen[4]))
   ```

2. **DES Cipher Setup and Decryption**:  
   For each generated key, the script initializes a DES cipher object in ECB mode using the `pycryptodome` library:
   
   ```python
   cipher = DES.new(key, DES.MODE_ECB)
   ```
   
   It then decrypts the ciphertext, which is `"ce126d2ddf2d1e64"`, converting it from hexadecimal to bytes:
   
   ```python
   plaintext = cipher.decrypt(bytes.fromhex("ce126d2ddf2d1e64"))
   ```

3. **Pattern Matching**:  
   After decrypting, the plaintext is converted to an ASCII string for easier analysis:
   
   ```python
   b2a_uu(plaintext).decode()
   ```
   
   The script uses a regular expression (`regex`) to check if the decrypted plaintext contains two sets of four uppercase letters, separated by a space. This is defined by the pattern `"[A-Z]{4} [A-Z]{4}"`. If the pattern is found, the script proceeds to the next step.

   ```python
   match = search("[A-Z]{4} [A-Z]{4}", b2a_uu(plaintext).decode())
   ```

4. **Output to File**:  
   If a match is found, the key and matching plaintext are written to a file called `plaintext`. The key is written in hexadecimal format, and the plaintext is written as the decoded string.
   
   ```python
   if match:
       with open("plaintext", "w") as file:
           file.write(str(key.hex()) + " " + str(match) + "
")
5. **Exception Handling and Garbage Collection**:  
   The script is designed to handle any exceptions that occur during the brute-force process. If an invalid key is generated or any other error arises, the loop simply continues to the next key without stopping execution:
   
   ```python
   except Exception:
       pass
   ```

   To prevent memory from building up during the loop, the script manually calls Python's garbage collector after every iteration. This ensures that memory is efficiently managed during the brute-force process:
   
   ```python
   finally:
       collect()
   ```