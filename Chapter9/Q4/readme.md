# Hash Calculation of Hex Strings

This document outlines the steps to convert hex strings into binary files and calculate their MD5 and SHA-256 hashes.

## 1. Create Hex Files

First, create two text files containing the hex representations of the two messages.

### Message 1 (file1.hex):

d131dd02c5e6eec4693d9a0698aff95c 2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a 085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6 dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1e c69821bcb6a8839396f9652b6ff72a70

### Message 2 (file2.hex):

d131dd02c5e6eec4693d9a0698aff95c 2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a 085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6 dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1e c69821bcb6a8839396f965ab6ff72a70

## 2. Convert Hex to Binary

Once you have these files, convert them to binary files using the following commands in your terminal:

```bash
xxd -r -p file1.hex > file1
xxd -r -p file2.hex > file2
```

## 3. Calculate MD5 Hashes

Next, calculate the MD5 hashes of the two binary files:

```bash
openssl dgst -md5 file1 file2
```

![image](https://github.com/user-attachments/assets/c0c68819-44a6-494d-b7de-1ed6fd0635b0)

This command will show you the MD5 hash for both files, confirming if they are the same, which indicates a collision.

## 4. Calculate SHA-256 Hashes

Finally, calculate the SHA-256 hashes of the two binary files:

```bash
openssl dgst -sha256 file1 file2
```

![image](https://github.com/user-attachments/assets/d83e81df-bb13-4216-8995-27d920414f1b)

This command will provide the SHA-256 hashes, which should differ due to the nature of the collision in MD5.
