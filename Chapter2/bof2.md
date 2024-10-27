# Understand bof1.c 
In this attack, we will try to replace the return address with another function's return address (redirect control) by using python! But, we will check other register whether the result we input is right or not.
## Stackframe

## Vulnerbility
At "fgets(array)"; function, we see that hackers can exploit the stackframe by adding more bytes in python in order to redirect the return address! 
# Start attacking bof1.c 
## Compiling the file without stack restriction
`gcc -g bof2.c -o bof2.out -fno-stack-protector -mpreferred-stack-boundary=2`  
## If we see that 
`echo $(python -c "print('a'*40+'\xff\xff\xff\xff')") | ./bof2.out`  
