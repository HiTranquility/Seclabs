# Lab B: Crypto-Lab – Exploring Collision-Resistance, Pre-Image Resistance, and MACs

## 1. Overview
The learning objective of this lab is for students to get familiar with pre-image resistant hash functions and Message Authentication Code (MAC). After finishing the lab, in addition to gaining a deeper understanding of the concepts, students should be able to use tools and write programs to generate hash values and a MAC for a given message.

## 2. Lab Environment
- **Secure Sockets Layer (SSL)**: An application-level protocol developed by the Netscape Corporation for transmitting sensitive information, such as credit card details, via the Internet.
- **OpenSSL**: A robust, commercial-grade implementation of SSL tools, and a general-purpose library based upon SSL, developed by Eric A. Young and Tim J. Hudson. OpenSSL is already installed on SEEDUbuntu.
- **Bless Hex Editor**: Install this yourself.

## 3. Lab Tasks

### Task 1: Generating Message Digest and MAC
In this task, we will play with various hash algorithms. You can use the `openssl dgst` command to generate the hash value for a file. To see the manuals, you can type `man openssl`.

Replace `dgsttype` with a specific hash algorithm, such as `-md5`, `-sha1`, `-sha256`, etc. In this task, you are encouraged to try at least three different algorithms. You can find the supported hash algorithms by typing `man openssl`.


Example filename.txt: Today I'm so wild!

Using MD5:

```bash
openssl dgst -md5 filename.txt
```
Using SHA1:

```bash
openssl dgst -sha1 filename.txt
```
Using SHA256:

```bash
openssl dgst -sha256 filename.txt
```
Result:
![image](https://github.com/user-attachments/assets/010a4856-b6aa-4a7d-aeda-5e1df7eea075)

### Task 2: The Randomness of a Hash
To understand the properties of hash functions, we would like to do the following exercise for MD5 and SHA256:
1. **Create a text file** of any length.
2. **Generate the hash value** `H1` for this file using a specific hash algorithm.
3. **Flip one bit** of the input file. You can achieve this modification using Bless.
4. **Generate the hash value** `H2` for the modified file.
5. **Observe** whether `H1` and `H2` are similar or not. Write a short program to count how many bits are different between `H1` and `H2`.

Calculating the Hamming Distance is a mathematical way to determine the differences between two objects (or strings, boxes, files, hashes, etc.). You are required to write a program that calculates the Hamming distance between two different hashes for their bits.

### Hamming Distance Python Program
Create a file named `yourname_hamming.py` with the following code:

```python
import sys

def hamming_distance(hex1, hex2):
    # Convert hex to binary
    bin1 = bin(int(hex1, 16))[2:].zfill(len(hex1) * 4)
    bin2 = bin(int(hex2, 16))[2:].zfill(len(hex2) * 4)
    
    # Calculate the Hamming distance
    distance = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    return distance

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 yourname_hamming.py <hex1> <hex2>")
        sys.exit(1)

    hex1 = sys.argv[1]
    hex2 = sys.argv[2]

    distance = hamming_distance(hex1, hex2)
    print(distance)
```
### Creating Two String Files

Create string1.txt:  
Create a file named string1.txt with a string, e.g., "abcdefghij".  
Create string2.txt:  
Create a file named string2.txt with a one-bit difference from string1.txt, e.g., "abcdeghij".

### Hash the Strings
Hash both files using OpenSSL:

```bash
openssl dgst -md5 string1.txt > hash_string1.txt
openssl dgst -md5 string2.txt > hash_string2.txt
```
### Compare the Hashes
Compare the hashes and calculate the Hamming distance using the Python program you created.
