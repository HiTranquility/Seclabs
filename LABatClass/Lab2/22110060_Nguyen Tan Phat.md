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
First, you might need to fire up another Virtual Machine and find its IP address through terminal by using this command: 
```bash
ip addr show
```
![image](https://github.com/user-attachments/assets/ebfd19d5-0cf1-4b4e-a07e-7f860d4df4e9)
Afterwards, try to ping each side by using `ping <ipaddress>` to confirm!
Send the tarball to the receiving computer using a secure method like SCP:

```bash
scp file_bundle.tar user@receiver_ip:/destination_path
```
Replace `user` and `receiver_ip` with the appropriate username and IP address of the receiving computer.  
For example, mine will be: 
```bash
scp file_bundle.tar HiTranquility@10.111.5.199:/home/HiTranquility/MyUbuntu
```
![image](https://github.com/user-attachments/assets/4b960f77-daec-45be-a6a1-92a8b19b4f9e)

![image](https://github.com/user-attachments/assets/678cbb32-0529-4b00-8129-793645aa3251)

Some issues that you need to solve! If you see this message below: 
![image](https://github.com/user-attachments/assets/36fd6c31-23a9-453f-b34d-09c708e77f50)  
This happens because your Virtual Machine doesn't have SSH downloaded yet!, so we will resolve this by download this back, please follow these followung steps for more:
### **1. Verify SSH Server is Installed on the Receiving VM**
- On the receiving VM, check if the SSH server is installed:
  ```bash
  sudo systemctl status ssh
  ```
- If it’s not installed, install it using:
  ```bash
  sudo apt update && sudo apt install openssh-server
  ```
  ![image](https://github.com/user-attachments/assets/cd8d4b1d-01a0-4d5b-8f10-8f88bbe34040)
### **2. Start the SSH Service**
- Ensure the SSH server is running:
  ```bash
  sudo systemctl start ssh
  ```
- To enable it at boot:
  ```bash
  sudo systemctl enable ssh
  ```
  ![image](https://github.com/user-attachments/assets/3a0bf898-b6b4-4f35-aa42-a8d44edb7260)
### **3. Allow SSH Through Firewall (If Active)**
- Check if a firewall (e.g., UFW) is running on the receiving VM:
  ```bash
  sudo ufw status
  ```
- If active, allow SSH connections:
  ```bash
  sudo ufw allow ssh
  ```
  ![image](https://github.com/user-attachments/assets/982d9770-68f8-49c1-aef1-960d452c7496)
### **5. Test SSH Connection**
- Before using `scp`, test if you can connect to the receiving VM using `ssh`:
  ```bash
  ssh HiTranquility@10.111.5.199
  ```
- If this works, `scp` should also work. If not, recheck the SSH server, IP, or firewall settings.
  

**Remember to do the same for both Virtual Machines!**
**Also configure your Network Virtual Machines to Brige**
![image](https://github.com/user-attachments/assets/a5134a1c-5681-43a7-b08f-5a87c5db3ffd)

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
![image](https://github.com/user-attachments/assets/5c46dd36-3fc2-4a58-9520-0cfde7189189)

---

### **Step 2.2: Verify the File**
First, transfer the file `public.key` by using the same command that is used for file_bundle.tar! E.g:
```bash
scp public.key HiTranquility@10.111.5.199:/home/HiTranquility/MyUbuntu
```
![image](https://github.com/user-attachments/assets/5811bdfb-f1d5-4fb6-a5e1-660435b7106c)

Use the sender’s public key to verify the authenticity and integrity of the file:

```bash
openssl dgst -sha256 -verify public.key -signature file.sig file.txt
```

- **Expected Output:**
  - If the file is authentic and unaltered:  
    ```
    Verified OK
    ```
    ![image](https://github.com/user-attachments/assets/5e184491-02f8-4b8d-bf5e-f00fc67d438c)

  - If verification fails: An error message indicating tampering or mismatch.

---

# Task 2: Transferring Encrypted File and Decrypting with Hybrid Encryption

## Objective:
This task involves transferring a file securely between two computers using hybrid encryption. The file will be symmetrically encrypted using AES, and the AES key will be encrypted with RSA for secure key exchange. All operations are done manually using OpenSSL commands in the terminal.

### Prerequisites:
- OpenSSL installed on both sender and receiver machines.
- Two computers: one for the sender and one for the receiver.
- RSA private and public key pairs for both sender and receiver.

## Step 1: Generate RSA Key Pair
Each machine (sender and receiver) needs to generate a public and private RSA key pair.

1. **On Sender's Computer (Computer 1):**
   ```bash
   openssl genpkey -algorithm RSA -out private_sender.key -aes256
   ```
   ![image](https://github.com/user-attachments/assets/9b7e3d73-ae32-4ad1-a7e8-fd048b3273e1)

   Here I choose `236890` for later checking!
   
   ```bash
   openssl rsa -pubout -in private_sender.key -out public_sender.key
   ```
   ![image](https://github.com/user-attachments/assets/b96092aa-a2fa-4594-ac82-18aab3ec55f7)
 
   I use `236890` from the previous!

3. **On Receiver's Computer (Computer 2):**
   ```bash
   openssl genpkey -algorithm RSA -out private_receiver.key -aes256
   ```
   ![image](https://github.com/user-attachments/assets/b635180b-89dd-44e2-a406-fcae416d326d)
   I choose PEM password is: `123456` also for later checking. Note that PEM doesn't affect the whole process so you can freely choose what numbers you want.
   ```bash
   openssl rsa -pubout -in private_receiver.key -out public_receiver.key
   ```
    ![image](https://github.com/user-attachments/assets/c1055200-37ba-4d27-86fd-5c4bffcaf2f1)

This will generate RSA key pairs (private and public) on both sender and receiver sides.

## Step 2: Symmetrically Encrypt the File (AES Encryption)
The file you want to transfer will be encrypted using AES encryption, and the AES key will be encrypted using RSA.

1. **Choose the file to encrypt** (e.g., `file_to_transfer.txt`).
   ![image](https://github.com/user-attachments/assets/f1716f0b-a68d-4919-a678-889d4d08530d)
   ![image](https://github.com/user-attachments/assets/40b2f91a-0b70-4bf3-b4e3-ea2977f21515)

3. **On Sender's Computer (Computer 1):**

   - Generate a random AES key (128-bit):
     ```bash
     openssl rand -out aes.key 16
     ```
     ![image](https://github.com/user-attachments/assets/9e358178-52a6-4446-9917-7e44b57c65a6)
     ![image](https://github.com/user-attachments/assets/26f74b79-a7ae-4514-b2d1-60a02aac934f)  

   - Encrypt the file using the AES key:
     ```bash
     openssl enc -aes-128-cbc -salt -in file_to_transfer.txt -out file_to_transfer.enc -pass file:./aes.key
     ```
     ![image](https://github.com/user-attachments/assets/4e715afc-ddad-44b0-9826-1dfbbe64e567)
     ![image](https://github.com/user-attachments/assets/cf104551-73e2-4c02-8082-135d71905853)  

     This will create the encrypted file `file_to_transfer.enc`.
     So now, we will give the sende the `public_receiver.key` by doing the same task from the previous Task1, for example:
     ```bash
     scp public_receiver.key TranquilSilence@172.16.31.77:/home/TranquilSilence/MyUbuntu/Task2
     ```
     ![image](https://github.com/user-attachments/assets/89cc8014-d0a7-4270-b697-9a0a4fbf0e23)

   - Encrypt the AES key using the receiver’s public RSA key:
     ```bash
     openssl pkeyutl -encrypt -inkey public_receiver.key -pubin -in aes.key -out aes.key.enc
     ```
     ![image](https://github.com/user-attachments/assets/800844a6-4af5-4d71-b557-8c0765e95596)
     This will encrypt the AES key with the receiver’s public RSA key, creating `aes.key.enc`.

## Step 3: Transfer Encrypted Files
After encryption, transfer the following files to the receiver:
- `file_to_transfer.enc` (encrypted file)
- `aes.key.enc` (encrypted AES key)

You can use `scp` or any other secure file transfer method:
```bash
scp file_to_transfer.enc aes.key.enc HiTranquility@172.16.31.78:/home/HiTranquility/MyUbuntu/Task2
```
![image](https://github.com/user-attachments/assets/17ab0935-e6eb-41a3-a67f-cca5eb359fb3)
![image](https://github.com/user-attachments/assets/98cdce03-7936-4aa9-880e-4a143de2f791)

## Step 4: Decrypt the File on the Receiver's Side
Once the files are transferred, the receiver can decrypt both the AES key and the encrypted file.

**On Receiver's Computer (Computer 2):**

   - **Decrypt the AES key using the receiver's private RSA key:**
     ```bash
     openssl rsautl -decrypt -inkey private_receiver.key -in aes.key.enc -out aes.key
     ```
  ![image](https://github.com/user-attachments/assets/9dac7c32-b98e-4792-9491-3264ffa55a50)
    
  ![image](https://github.com/user-attachments/assets/675c97b6-fb43-4d6b-85d4-39a08e9b3f09)

   - **Decrypt the file using the decrypted AES key:**
     ```bash
     openssl enc -d -aes-128-cbc -in file_to_transfer.enc -out file_to_transfer_decrypted.txt -pass file:./aes.key
     ```
  ![image](https://github.com/user-attachments/assets/22a6e1d1-cc0a-48ba-badc-0b27e31ffd55)
  ![image](https://github.com/user-attachments/assets/b2d4370b-d0c4-4d6c-b5c5-168c56736459)

## Conclusion:
This process demonstrates the use of hybrid encryption combining RSA (asymmetric encryption) for secure key exchange and AES (symmetric encryption) for file encryption. It provides both security and efficiency for transferring files between two computers.

# Task 3: Firewall Configuration Guide

## Step 1: Install Required Packages

### On VM1 (Server):
1. Update the system and install `iptables`, `apache2`, and `openssh-server`:
    ```bash
    sudo apt update
    sudo apt install iptables apache2 openssh-server -y
    ```

2. Start and enable Apache and SSH services:
    ```bash
    sudo systemctl start apache2
    sudo systemctl enable apache2
    sudo systemctl start ssh
    sudo systemctl enable ssh
    ```

---

## Step 2: Verify Basic Connectivity

### On VM2 (Client):
1. Test connectivity to VM1's web and SSH services:

    - **Ping VM1:**
      ```bash
      ping <VM1_IP>
      ```
      ![image](https://github.com/user-attachments/assets/3835f107-89a4-4cfd-a878-9625e2b56b98)

    - **Test HTTP access using curl:**
      ```bash
      curl http://<VM1_IP>
      ```
      ![image](https://github.com/user-attachments/assets/dcfbb3e9-1e3e-480a-aade-86149ca58eed)

    - **Test SSH access:**
      ```bash
      ssh <username>@<VM1_IP>
      ```
      ![image](https://github.com/user-attachments/assets/1f3eef6e-37ee-4f8a-8c8a-8de35b0dbb50)

2. Ensure all services are accessible before applying firewall rules.

---

## Step 3: Configure `iptables` Rules on VM1

### On VM1 (Server):
1. Clear existing iptables rules to start fresh:
    ```bash
    sudo iptables -F
    sudo iptables -X
    ```

2. Add the following rules:

    - **Rule 1: Block HTTP (port 80) traffic**
      To block HTTP requests from VM2:
      ```bash
      sudo iptables -A INPUT -p tcp --dport 80 -s <VM2_IP> -j DROP
      ```
      
    - **Rule 2: Block ICMP (ping) traffic**
      To block ping requests (ICMP echo):
      ```bash
      sudo iptables -A INPUT -p icmp -s <VM2_IP> -j DROP
      ```

    - **Rule 3: Block SSH (port 22) traffic**
      To block SSH access from VM2:
      ```bash
      sudo iptables -A INPUT -p tcp --dport 22 -s <VM2_IP> -j DROP
      ```
   ![image](https://github.com/user-attachments/assets/282f6794-effc-4930-917a-2832d91e684f)
   
---

## Step 4: Demonstrate Blocking/Unblocking

### Blocking
After applying the rules, test from VM2:

- **HTTP (port 80):**
  Try accessing the web server:
  ```bash
  curl http://<VM1_IP>
  ```
  ![image](https://github.com/user-attachments/assets/1e8bace9-a438-42ec-b9eb-838092424147)

- SSH (port 22):
  Try connecting to SSH:
  ```bash
  ssh <username>@<VM1_IP>
  ```
  ![image](https://github.com/user-attachments/assets/b0f832fb-141b-42fd-9b49-faae6de54d68)
  Expected Result: The connection should fail.

### Unblocking
To unblock traffic, remove the specific rule using iptables:

### Remove HTTP block:
  ```bash
  sudo iptables -D INPUT -p tcp --dport 80 -s <VM2_IP> -j DROP
  ```
### Remove ICMP block:
  ```bash
  sudo iptables -D INPUT -p icmp -s <VM2_IP> -j DROP
  ```
### Remove SSH block:
  ```bash
  sudo iptables -D INPUT -p tcp --dport 22 -s <VM2_IP> -j DROP
  ```
![image](https://github.com/user-attachments/assets/26496acf-1e5a-4702-b2e2-123b86e5b67a)

### Testing:
Test the services again from VM2 to ensure connectivity is restored.
---

## Step 5: Save and Persist Firewall Rules
Making the iptables rules persist across reboots:
### Install iptables-persistent:
 ```bash
 sudo apt install iptables-persistent -y
 ```
### Save the rules:
 ```bash
 sudo iptables-save > /etc/iptables/rules.v4
 ```
  Result: The rules will be re-applied automatically on reboot.
