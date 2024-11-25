# 22110060 Nguyen Tan Phat

# Task 1: Transfer Files Between Computers

This guide demonstrates how to transfer a single plaintext file between two Linux computers using OpenSSL to ensure file integrity and authenticity.

---

## **Steps Overview**
1. Generate a private-public key pair (on the sending side).
2. Sign the file to ensure integrity and authenticity.
3. Transfer the file and its signature.
4. Verify the file on the receiving side.

---

## **1. Sending Side**

### **Step 1.1: Generate Key Pair**
Generate a private-public key pair on the sending computer:

```bash
openssl genrsa -out private.key 2048
openssl rsa -in private.key -pubout -out public.key
```

- `private.key`: Used for signing the file.
- `public.key`: Shared with the receiver for verification.
![image](https://github.com/user-attachments/assets/506ef7d6-a125-45f9-b214-2582e0fe5596)
![image](https://github.com/user-attachments/assets/ce742ecc-a2aa-4371-bc27-62a6b68f131f)

---

### **Step 1.2: Sign the File**

Create file `file.txt` with text: "Hello there! This is HiTranquility!"  
![image](https://github.com/user-attachments/assets/36e09d9a-eb4f-4f86-b135-d244976d681d)

Sign the plaintext file (e.g., `file.txt`) to generate a signature:

```bash
openssl dgst -sha256 -sign private.key -out file.sig file.txt
```
![image](https://github.com/user-attachments/assets/f6ac6ab3-be74-480f-8a2f-9580afbf69e1)  

- `file.sig`: Contains the cryptographic signature of `file.txt`.
![image](https://github.com/user-attachments/assets/9851e3a0-64b5-4dca-bc60-bd5d3ce5e8ac)

---

### **Step 1.3: Bundle the Files**
Combine the plaintext file and its signature into a single tarball for transfer:

```bash
tar -cvf file_bundle.tar file.txt file.sig
```
![image](https://github.com/user-attachments/assets/6249c7fa-4ad6-4bdf-9a60-74fb4e83e34c)

- `file_bundle.tar`: A compressed archive of the file and its signature.
![image](https://github.com/user-attachments/assets/c0bc8d53-7475-4ca1-b77c-8d591a8f4839)

---

### **Step 1.4: Transfer the File**
Send the tarball to the receiving computer using a secure method like SCP:

```bash
scp file_bundle.tar user@receiver_ip:/destination_path
```

Replace `user` and `receiver_ip` with the appropriate username and IP address of the receiving computer.

---

## **2. Receiving Side**

### **Step 2.1: Unpack the File Bundle**
Extract the files from the received tarball:

```bash
tar -xvf file_bundle.tar
```

This will produce:
- `file.txt`: The plaintext file.
- `file.sig`: The file's signature.

---

### **Step 2.2: Verify the File**
Use the sender’s public key to verify the authenticity and integrity of the file:

```bash
openssl dgst -sha256 -verify public.key -signature file.sig file.txt
```

- **Expected Output:**
  - If the file is authentic and unaltered:  
    ```
    Verified OK
    ```
  - If verification fails: An error message indicating tampering or mismatch.

---

## **Summary**

| **Step**         | **Action**                          | **File(s) Created**                | **Purpose**                              |
|-------------------|-------------------------------------|-------------------------------------|------------------------------------------|
| **Sending Side**  | Generate Key Pair                  | `private.key`, `public.key`         | Keys for signing and verification.       |
|                   | Sign File                          | `file.sig`                         | Signature to ensure integrity/authenticity. |
|                   | Bundle Files                       | `file_bundle.tar`                  | Archive for easy transfer.               |
|                   | Transfer Files                     | -                                  | Move the tarball to the receiver.        |
| **Receiving Side**| Unpack Tarball                     | `file.txt`, `file.sig`             | Extract files for verification.          |
|                   | Verify File                        | Validation Output (OK or Failed)   | Check file integrity and authenticity.   |

---

## **Key Notes**
- Ensure the sender’s `public.key` is securely transferred to the receiver beforehand or separately.
- Use SCP, SFTP, or another secure method to transfer the tarball.
