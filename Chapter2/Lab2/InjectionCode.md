# Understand InjectionCode 
In reality, we don't actually know how long is the stackframe is, so we need to determine how long is it by adding bytes to examine! The task is to load the shellcode into the buffer in the vulnerable program, then insert it into the return address so that the program returns and executes the command I just inserted into the buffer.
## Stackframe

## Vulnerbility
In buf, we can redirect the return address to our assembly code to run our own code!
# Start attacking with InjectionCode 
## Compiling sh.asm file in order to use later
- `nasm -g -f elf sh.asm` or `nasm -f elf32 sh.asm -o sh.o` if the file is existed    
- `ld -m elf_i386 sh.o -o sh sh.o`  

