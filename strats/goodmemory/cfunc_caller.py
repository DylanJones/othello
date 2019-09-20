from ctypes import *
import sys

# Initialise ctypes prototype for mprotect().
# According to the manpage:
#     int mprotect(const void *addr, size_t len, int prot);
libc = CDLL("libc.so.6")
mprotect = libc.mprotect
mprotect.restype = c_int
mprotect.argtypes = [c_void_p, c_size_t, c_int]

# PROT_xxxx constants
# Output of gcc -E -dM -x c /usr/include/sys/mman.h | grep PROT_
#     #define PROT_NONE 0x0
#     #define PROT_READ 0x1
#     #define PROT_WRITE 0x2
#     #define PROT_EXEC 0x4
#     #define PROT_GROWSDOWN 0x01000000
#     #define PROT_GROWSUP 0x02000000
PROT_NONE = 0x0
PROT_READ = 0x1
PROT_WRITE = 0x2
PROT_EXEC = 0x4

# Machine code of an empty C function, generated with gcc
# Disassembly:
#     55        push   %ebp
#     89 e5     mov    %esp,%ebp
#     5d        pop    %ebp
#     c3        ret
#code = b"\x55\x89\xe5\x5d\xc3"

code_array = []

def generate_function(asm, rettype = None, *func_args):
    global code_array
    # add it to array so it isn't garbage collected
    code_array.append(asm)

    # Get the address of the code
    #addr = addressof(c_char_p(code))
    addr = addressof(cast(c_char_p(asm), POINTER(c_char)).contents)

    # Get the start of the page containing the code and set the permissions
    pagesize = 0x1000
    pagestart = addr & ~(pagesize - 1)
    if mprotect(pagestart, pagesize, PROT_READ|PROT_WRITE|PROT_EXEC):
        raise RuntimeError("Failed to set permissions using mprotect()")

    # Generate ctypes function object from code
    #functype = CFUNCTYPE(c_int, c_int)
    functype = CFUNCTYPE(rettype, *func_args)
    f = functype(addr)
    return f

if __name__ == '__main__':
    # Call the function
    if len(sys.argv) > 1:
        code = eval(sys.argv[1])
    else:
        code = b'\x8d\x47\x05\xc3'
    f = generate_function(code, c_int, c_int)
    print("Calling f()")
    ret = f(3)
    print(f"Returned {ret}")
