import cfunc_caller
import ctypes
import array
import helpers

var_code = b'\x48\x89\xc8\x41\xb8\x00\x00\x00\x00\xeb\x0e\x4a\x33\x04\xc2\x49\x83\xc0\x01\x49\x83\xf8\x40\x74\x17\x46\x0f\xb6\x0c\x07\x41\x80\xf9\x02\x74\xe7\x41\x80\xf9\x01\x75\xe5\x4a\x33\x04\xc6\xeb\xdf\xf3\xc3'

code = var_code

func = cfunc_caller.generate_function(code, ctypes.c_ulonglong, ctypes.c_char_p, ctypes.POINTER(ctypes.c_ulonglong),
                                      ctypes.POINTER(ctypes.c_ulonglong), ctypes.c_ulonglong)

board = helpers.from_tournament_format(
    list('???????????........??........??........??...o@...??...@o...??........??........??........???????????'))
board = helpers.from_tournament_format(
    list('???????????@@@@@oo@??@@@@@@@@??@@o@o@@@??@@@o@@o@??o@@@@@o@??o@@@ooo@??o@@@@oo@??..@@@@@@???????????'))
board = array.array('B',
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0,
                     0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

bbits = array.array('Q', helpers.z1)
wbits = array.array('Q', helpers.z2)


def array_pointer(arr):
    return ctypes.cast(arr.buffer_info()[0], ctypes.c_char_p)


def ulonglong_array_pointer(arr):
    return ctypes.cast(arr.buffer_info()[0], ctypes.POINTER(ctypes.c_ulonglong))


bptr = ulonglong_array_pointer(bbits)
wptr = ulonglong_array_pointer(wbits)


def zobrist(board, moving_plr):
    h = 0 if moving_plr == helpers.BLACK else helpers.plr_xor
    # h = 0
    return func(array_pointer(board), bptr, wptr, h)


print(f'Call to zobrist_c returned {zobrist(board, 0)}')
print(f'Call to python zobrist returned {helpers.zobrist(board, 0)}')
if zobrist(board, 1) == helpers.zobrist(board, 1):
    print("Function successful!")
else:
    print("Function failed.")
