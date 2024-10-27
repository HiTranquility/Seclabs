# Lab on DES and 3DES

In this lab, you will learn how to use a website and Python to convert plaintext to ciphertext. Additionally, you will see a practical demonstration of how to encrypt a bank file (related to Chapter 2 and Chapter 4).

## Reference Links

- GitHub link for the entire lab:
- Website link: [anycript.com](https://anycript.com/crypto/)

## Working on the Website

On the website, you will get acquainted with basic operations such as inputting data, selecting modes, and understanding the essence of the actions you perform.

### Understanding the Displayed Information
![image](https://github.com/user-attachments/assets/7a197fc5-233f-4637-baa9-8b2a6246c49a)

1. **Secret Key:**
    - This is the cryptographic key used for encryption and decryption in the DES algorithm. The secret key is a 64-bit value (56 bits of effective key length and 8 bits for parity checking).

2. **Encryption Mode:**
    - **CBC (Cipher Block Chaining):** This is a mode of operation for block ciphers, where each block of plaintext is XORed with the previous ciphertext block before encryption.
    - **ECB (Electronic Codebook):** This is a mode of operation where each block of plaintext is encrypted independently, resulting in the same ciphertext blocks for the same plaintext blocks.
        - This means that if two plaintext blocks are identical, they will produce the same ciphertext block (the encrypted data).

3. **IV (Initialization Vector) only in CBC:**
    - IV is only used in the CBC encryption mode and not in the ECB mode.
    - IV is an optional parameter, but providing it is necessary for security when using CBC.
    - IV must be a 64-bit value and combined with the first plaintext data block to provide additional security.
    - When entering IV, ensure it is input in UTF-8 format to avoid errors during decryption.

4. **Output Format:**
    - **Base64:** This is a binary-to-text encoding scheme that represents binary data in an ASCII string format.
    - **HEX:** This is a hexadecimal representation of the encrypted data, where each byte is represented by two hexadecimal digits (0-9, A-F).

**For example**, if you have a plaintext message "Hello, World!" and a secret key of "0123456789ABCDEF", you can encrypt it using the DES algorithm in CBC mode with an IV of "FEDCBA9876543210". The resulting ciphertext in Base64 format might be something like "oBZVFTU/VitbwktaXg==", and in HEX format, it might be "A08655153535B2B5DAD24E".

## Encrypting and Decrypting with DES

### Encryption
![image](https://github.com/user-attachments/assets/bf814b95-da56-4ef1-a814-559632c9746c)

- **Secret Key:** 0123456789ABCDEF
- **Encryption Mode:** CBC
- **IV (optional):** FEDCBA9876543210
- **Output format:** Base64
- **Ciphertext:** zCysUH9MqH5x1Rtw1K+qVA==

### Decryption
![image](https://github.com/user-attachments/assets/6a3b24e9-bda3-46f5-9254-7306462637af)

- **Encrypted Text:** zCysUH9MqH5x1Rtw1K+qVA==
- **Secret Key:** 0123456789ABCDEF
- **Encryption Mode:** CBC (Cipher Block Chaining)
- **IV (optional):** FEDCBA9876543210
- **Output format:** Base64
- **Plaintext:** Hello, World!

## Encrypting and Decrypting with 3DES

### Encryption
![image](https://github.com/user-attachments/assets/94e3bd73-40bf-4af5-a236-cb01d2284782)

- **Plaintext:** "Hello, World!"
- **Secret Key:** "0123456789ABCDEF"
- **Encryption Mode:** CBC (Cipher Block Chaining)
- **Output format:** Base64
- **Ciphertext:** 3Sx0odVpCpZBzbSJVe9DuA==

### Decryption
![image](https://github.com/user-attachments/assets/b45fcc82-0bc5-40cf-93b3-7309ecb6c8e6)

- **Encrypted Text:** 3Sx0odVpCpbc8tmVzp46lA==
- **Secret Key:** "0123456789ABCDEF"
- **Encryption Mode:** CBC (Cipher Block Chaining)
- **IV (optional):** "12345678"
- **Output format:** Base64
- **Plaintext:** Hello, World!

## Working with Python

### Required Libraries

- Crypto library: `pip install cryptography` or `pip install pycryptodome`

  **REMOVE:** `pip install crypto` as it is deprecated.

- If errors occur, you can use the command `pip install --upgrade setuptools` and then install normally.

### Types of Encryption

- **DES**
- **3DES**

### Real Test Case

- Required library: `pip install pyDes`
- **Objective:** Understand why it is necessary to do this in practice, as well as to see what the actual text file looks like when converted using Python and a small login application.
