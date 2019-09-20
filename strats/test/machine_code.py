from . import cfunc_caller
import ctypes
import array
from . import helpers

# O0
code_legal_moves = b'\x55\x48\x89\xe5\x48\x89\x7d\xc8\x89\xf0\x48\x89\x55\xb8\x88\x45\xc4\xc7\x45\xe0\x00\x00\x00\x00\xc7\x45\xe4\x00\x00\x00\x00\x83\x7d\xe4\x3f\x0f\x8f\x95\x01\x00\x00\x8b\x45\xe4\x8d\x50\x07\x85\xc0\x0f\x48\xc2\xc1\xf8\x03\x89\x45\xf8\x8b\x45\xe4\x99\xc1\xea\x1d\x01\xd0\x83\xe0\x07\x29\xd0\x89\x45\xfc\x8b\x45\xe4\x48\x63\xd0\x48\x8b\x45\xc8\x48\x01\xd0\x0f\xb6\x00\x84\xc0\x0f\x85\x52\x01\x00\x00\xc7\x45\xe8\xff\xff\xff\xff\x83\x7d\xe8\x01\x0f\x8f\x41\x01\x00\x00\xc7\x45\xec\xff\xff\xff\xff\x83\x7d\xec\x01\x0f\x8f\x27\x01\x00\x00\x83\x7d\xe8\x00\x75\x0a\x83\x7d\xec\x00\x0f\x84\x0a\x01\x00\x00\x8b\x55\xf8\x8b\x45\xe8\x01\xd0\x89\x45\xf0\x8b\x55\xfc\x8b\x45\xec\x01\xd0\x89\x45\xf4\xc6\x45\xdf\x00\x83\x7d\xf0\x00\x78\x59\x83\x7d\xf0\x07\x7f\x53\x83\x7d\xf4\x00\x78\x4d\x83\x7d\xf4\x07\x7f\x47\x8b\x45\xf0\x8d\x14\xc5\x00\x00\x00\x00\x8b\x45\xf4\x01\xd0\x48\x63\xd0\x48\x8b\x45\xc8\x48\x01\xd0\x0f\xb6\x00\x0f\xb6\xc0\x80\x7d\xc4\x01\x75\x07\xba\x02\x00\x00\x00\xeb\x05\xba\x01\x00\x00\x00\x39\xc2\x75\x12\xc6\x45\xdf\x01\x8b\x45\xe8\x01\x45\xf0\x8b\x45\xec\x01\x45\xf4\xeb\xa1\x83\x7d\xf0\x00\x0f\x88\x8a\x00\x00\x00\x83\x7d\xf0\x07\x0f\x8f\x80\x00\x00\x00\x83\x7d\xf4\x00\x78\x7a\x83\x7d\xf4\x07\x7f\x74\x0f\xb6\x45\xdf\x83\xf0\x01\x84\xc0\x75\x69\x8b\x45\xf0\x8d\x14\xc5\x00\x00\x00\x00\x8b\x45\xf4\x01\xd0\x48\x63\xd0\x48\x8b\x45\xc8\x48\x01\xd0\x0f\xb6\x00\x0f\xb6\xd0\x0f\xbe\x45\xc4\x39\xc2\x75\x43\x83\x7d\xe0\x00\x74\x1b\x8b\x45\xe0\x48\x98\x48\x8d\x50\xff\x48\x8b\x45\xb8\x48\x01\xd0\x0f\xb6\x00\x0f\xb6\xc0\x39\x45\xe4\x74\x22\x83\x7d\xe0\x3f\x7f\x1c\x8b\x45\xe0\x48\x63\xd0\x48\x8b\x45\xb8\x48\x01\xd0\x8b\x55\xe4\x88\x10\x83\x45\xe0\x01\xeb\x04\x90\xeb\x01\x90\x83\x45\xec\x01\xe9\xcf\xfe\xff\xff\x83\x45\xe8\x01\xe9\xb5\xfe\xff\xff\x83\x45\xe4\x01\xe9\x61\xfe\xff\xff\x8b\x45\xe0\x5d\xc3'
# O3 (segfaults)
# code_legal_moves = b'\x41\x57\x41\x56\x45\x31\xf6\x41\x55\x40\x80\xfe\x01\x41\x54\x55\x53\x41\x0f\x94\xc6\x40\x0f\xbe\xc6\x41\x83\xc6\x01\x45\x31\xe4\x48\x89\x7c\x24\xd0\x48\x89\x54\x24\xf8\x45\x31\xff\xc7\x44\x24\xf4\x00\x00\x00\x89\x44\x24\xec\xeb\x1b\x0f\x1f\x44\x00\x00\x41\x83\xc4\x01\x49\x83\xc7\x01\x41\x83\xe4\x07\x49\x83\xff\x40\x0f\x84\x4a\x01\x00\x00\x48\x8b\x44\x24\xd0\x44\x89\x7c\x24\xe8\x42\x80\x3c\x38\x00\x75\xd9\x44\x89\xf8\x49\xc7\xc5\xf8\xff\xff\xff\x41\xb8\xff\xff\xff\xff\xc1\xf8\x03\x4c\x89\x7c\x24\xe0\x44\x88\x64\x24\xf3\x89\x44\x24\xdc\x41\x0f\xb6\xc4\x89\x44\x24\xd8\x8b\x44\x24\xdc\x4d\x8d\x7d\xff\xbf\xff\xff\xff\xff\x42\x8d\x2c\x00\x8d\x1c\xed\x00\x00\x00\x00\x83\xfd\x07\x41\x0f\x97\xc4\x45\x31\xdb\x48\x63\xdb\x44\x89\xc0\x09\xf8\x0f\x84\x90\x00\x00\x00\x8b\x44\x24\xd8\x01\xf8\x89\xc1\xc1\xe9\x1f\x44\x08\xe1\x75\x50\x83\xf8\x07\x7f\x4b\x48\x63\xd0\x4b\x8d\x34\x1f\x41\x89\xe9\x48\x01\xda\x48\x03\x54\x24\xd0\xeb\x23\x0f\x1f\x80\x00\x00\x00\x00\x45\x01\xc1\x01\xf8\x41\x83\xf9\x07\x77\x25\x85\xc0\x78\x21\x48\x01\xf2\x83\xf8\x08\xb9\x01\x00\x00\x00\x74\x14\x44\x0f\xb6\x12\x45\x39\xf2\x74\xdb\x84\xc9\x74\x07\x44\x3b\x54\x24\xec\x74\x40\x49\x83\xfb\x02\x75\x2a\x41\x83\xc0\x01\x49\x83\xc5\x08\x41\x83\xf8\x02\x0f\x85\x58\xff\xff\xff\x4c\x8b\x7c\x24\xe0\x44\x0f\xb6\x64\x24\xf3\xe9\xf8\xfe\xff\xff\x0f\x1f\x84\x00\x00\x00\x00\x49\x83\xc3\x01\x83\xc7\x01\xe9\x59\xff\xff\xff\x0f\x1f\x40\x00\x48\x63\x44\x24\xf4\x85\xc0\x75\x17\x0f\xb6\x4c\x24\xe0\x48\x8b\x74\x24\xf8\x83\x44\x24\xf4\x01\x88\x0c\x06\xeb\xa3\x0f\x1f\x00\x48\x8b\x4c\x24\xf8\x0f\xb6\x54\x01\xff\x3b\x54\x24\xe8\x74\x90\x83\xf8\x3f\x7f\x8b\xeb\xd2\x66\x0f\x1f\x84\x00\x00\x00\x0f\xb6\x44\x24\xf4\x5b\x5d\x41\x5c\x41\x5d\x41\x5e\x41\x5f\xc3'

code_fsquares = b'\x55\x48\x89\xe5\x48\x89\x7d\xc8\x89\xf0\x88\x45\xc4\xc7\x45\xd4\x00\x00\x00\x00\xc7\x45\xd8\x00\x00\x00\x00\x83\x7d\xd8\x07\x0f\x8f\xf8\x00\x00\x00\xc7\x45\xdc\x00\x00\x00\x00\x83\x7d\xdc\x07\x0f\x8f\xde\x00\x00\x00\x8b\x45\xd8\x8d\x14\xc5\x00\x00\x00\x00\x8b\x45\xdc\x01\xd0\x48\x63\xd0\x48\x8b\x45\xc8\x48\x01\xd0\x0f\xb6\x00\x84\xc0\x0f\x85\xb1\x00\x00\x00\xc7\x45\xe0\xff\xff\xff\xff\x83\x7d\xe0\x01\x0f\x8f\x9e\x00\x00\x00\xc7\x45\xe4\xff\xff\xff\xff\x83\x7d\xe4\x01\x0f\x8f\x84\x00\x00\x00\x8b\x55\xd8\x8b\x45\xe0\x01\xd0\x85\xc0\x78\x6f\x8b\x55\xd8\x8b\x45\xe0\x01\xd0\x83\xf8\x07\x7f\x62\x8b\x55\xdc\x8b\x45\xe4\x01\xd0\x85\xc0\x78\x56\x8b\x55\xdc\x8b\x45\xe4\x01\xd0\x83\xf8\x07\x7f\x49\x83\x7d\xe0\x00\x75\x06\x83\x7d\xe4\x00\x74\x3d\x8b\x55\xd8\x8b\x45\xe0\x01\xd0\x8d\x14\xc5\x00\x00\x00\x00\x8b\x45\xdc\x01\xc2\x8b\x45\xe4\x01\xd0\x89\x45\xf8\x8b\x45\xf8\x48\x63\xd0\x48\x8b\x45\xc8\x48\x01\xd0\x0f\xb6\x00\x0f\xb6\xd0\x0f\xbe\x45\xc4\x39\xc2\x75\x06\x83\x6d\xd4\x01\xeb\x13\x83\x45\xe4\x01\xe9\x72\xff\xff\xff\x83\x45\xe0\x01\xe9\x58\xff\xff\xff\x90\x90\x83\x45\xdc\x01\xe9\x18\xff\xff\xff\x83\x45\xd8\x01\xe9\xfe\xfe\xff\xff\x80\x7d\xc4\x01\x75\x07\xb8\x02\x00\x00\x00\xeb\x05\xb8\x01\x00\x00\x00\x88\x45\xc4\xc7\x45\xe8\x00\x00\x00\x00\x83\x7d\xe8\x07\x0f\x8f\xf8\x00\x00\x00\xc7\x45\xec\x00\x00\x00\x00\x83\x7d\xec\x07\x0f\x8f\xde\x00\x00\x00\x8b\x45\xe8\x8d\x14\xc5\x00\x00\x00\x00\x8b\x45\xec\x01\xd0\x48\x63\xd0\x48\x8b\x45\xc8\x48\x01\xd0\x0f\xb6\x00\x84\xc0\x0f\x85\xb1\x00\x00\x00\xc7\x45\xf0\xff\xff\xff\xff\x83\x7d\xf0\x01\x0f\x8f\x9e\x00\x00\x00\xc7\x45\xf4\xff\xff\xff\xff\x83\x7d\xf4\x01\x0f\x8f\x84\x00\x00\x00\x8b\x55\xe8\x8b\x45\xf0\x01\xd0\x85\xc0\x78\x6f\x8b\x55\xe8\x8b\x45\xf0\x01\xd0\x83\xf8\x07\x7f\x62\x8b\x55\xec\x8b\x45\xf4\x01\xd0\x85\xc0\x78\x56\x8b\x55\xec\x8b\x45\xf4\x01\xd0\x83\xf8\x07\x7f\x49\x83\x7d\xf0\x00\x75\x06\x83\x7d\xf4\x00\x74\x3d\x8b\x55\xe8\x8b\x45\xf0\x01\xd0\x8d\x14\xc5\x00\x00\x00\x00\x8b\x45\xec\x01\xc2\x8b\x45\xf4\x01\xd0\x89\x45\xfc\x8b\x45\xfc\x48\x63\xd0\x48\x8b\x45\xc8\x48\x01\xd0\x0f\xb6\x00\x0f\xb6\xd0\x0f\xbe\x45\xc4\x39\xc2\x75\x06\x83\x45\xd4\x01\xeb\x13\x83\x45\xf4\x01\xe9\x72\xff\xff\xff\x83\x45\xf0\x01\xe9\x58\xff\xff\xff\x90\x90\x83\x45\xec\x01\xe9\x18\xff\xff\xff\x83\x45\xe8\x01\xe9\xfe\xfe\xff\xff\x8b\x45\xd4\x5d\xc3'
code_wmatrix = b'\x55\x48\x89\xe5\x48\x89\x7d\xe8\x89\xf0\x48\x89\x55\xd8\x88\x45\xe4\xc7\x45\xf8\x00\x00\x00\x00\xc7\x45\xfc\x00\x00\x00\x00\x83\x7d\xfc\x3f\x7f\x78\x8b\x45\xfc\x48\x63\xd0\x48\x8b\x45\xe8\x48\x01\xd0\x0f\xb6\x00\x0f\xb6\xd0\x0f\xbe\x45\xe4\x39\xc2\x75\x18\x8b\x45\xfc\x48\x63\xd0\x48\x8b\x45\xd8\x48\x01\xd0\x0f\xb6\x00\x0f\xbe\xc0\x01\x45\xf8\xeb\x3f\x8b\x45\xfc\x48\x63\xd0\x48\x8b\x45\xe8\x48\x01\xd0\x0f\xb6\x00\x0f\xb6\xc0\x80\x7d\xe4\x01\x75\x07\xba\x02\x00\x00\x00\xeb\x05\xba\x01\x00\x00\x00\x39\xc2\x75\x16\x8b\x45\xfc\x48\x63\xd0\x48\x8b\x45\xd8\x48\x01\xd0\x0f\xb6\x00\x0f\xbe\xc0\x29\x45\xf8\x83\x45\xfc\x01\xeb\x82\x8b\x45\xf8\x5d\xc3'
code_ccount = b'\x45\x31\xc0\x40\x80\xfe\x01\x40\x0f\xbe\xce\x41\x0f\x94\xc0\x48\x8d\x77\x40\x31\xc0\x41\x83\xc0\x01\xeb\x19\x0f\x1f\x44\x00\x00\x41\x39\xd0\x0f\x94\xc2\x48\x83\xc7\x01\x0f\xb6\xd2\x29\xd0\x48\x39\xfe\x74\x13\x0f\xb6\x17\x39\xd1\x75\xe5\x48\x83\xc7\x01\x83\xc0\x01\x48\x39\xfe\x75\xed\xf3\xc3'
# compiled with -O3, has problems when initalHashValue is 0
# code_zobrist = b'\x48\x89\xc8\x45\x31\xc0\xeb\x1c\x0f\x1f\x84\x00\x00\x00\x00\x41\x80\xf9\x01\x75\x04\x4a\x33\x04\xc6\x49\x83\xc0\x01\x49\x83\xf8\x40\x74\x19\x46\x0f\xb6\x0c\x07\x41\x80\xf9\x02\x75\xe1\x4a\x33\x04\xc2\x49\x83\xc0\x01\x49\x83\xf8\x40\x75\xe7\xf3\xc3'
# compiled with -O1
code_zobrist = b'\x48\x89\xc8\x41\xb8\x00\x00\x00\x00\xeb\x0e\x4a\x33\x04\xc2\x49\x83\xc0\x01\x49\x83\xf8\x40\x74\x17\x46\x0f\xb6\x0c\x07\x41\x80\xf9\x02\x74\xe7\x41\x80\xf9\x01\x75\xe5\x4a\x33\x04\xc6\xeb\xdf\xf3\xc3'

wmatrix_c = cfunc_caller.generate_function(code_wmatrix, ctypes.c_int, ctypes.c_char_p, ctypes.c_char, ctypes.c_char_p)
legal_moves_c = cfunc_caller.generate_function(code_legal_moves, ctypes.c_int8, ctypes.c_char_p, ctypes.c_char,
                                               ctypes.c_char_p)
fsquares_c = cfunc_caller.generate_function(code_fsquares, ctypes.c_int, ctypes.c_char_p, ctypes.c_char)
ccount_c = cfunc_caller.generate_function(code_ccount, ctypes.c_int, ctypes.c_char_p, ctypes.c_char)
zobrist_c = cfunc_caller.generate_function(code_zobrist, ctypes.c_ulonglong, ctypes.c_char_p,
                                           ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ulonglong),
                                           ctypes.c_ulonglong)


def array_pointer(arr):
    return ctypes.cast(arr.buffer_info()[0], ctypes.c_char_p)


def ulonglong_array_pointer(arr):
    return ctypes.cast(arr.buffer_info()[0], ctypes.POINTER(ctypes.c_ulonglong))


buf = array.array('B', [0] * 64)
buf_pointer = array_pointer(buf)

# SQUARE_WEIGHTS=[120, -20, 20, 5, 5, 20, -20, 120, -20, -40, -5, -5, -5, -5, -40, -20, 20, -5, 15, 3, 3, 15, -5, 20, 5, -5, 3, 3, 3, 3, -5, 5, 5, -5, 3, 3, 3, 3, -5, 5, 20, -5, 15, 3, 3, 15, -5, 20, -20, -40, -5, -5, -5, -5, -40, -20, 120, -20, 20, 5, 5, 20, -20, 120]
weight_array = array.array('b', helpers.SQUARE_WEIGHTS)
weight_pointer = array_pointer(weight_array)

bbits_arr = array.array('Q', helpers.z1)
wbits_arr = array.array('Q', helpers.z2)

bptr = ulonglong_array_pointer(bbits_arr)
wptr = ulonglong_array_pointer(wbits_arr)


# print(helpers.z1)

def legal_moves(node):
    retlen = legal_moves_c(node.ptr, node.moving_plr, buf_pointer)
    return [buf[i] for i in range(retlen)]


def frontier_squares(node):
    return fsquares_c(node.ptr, node.moving_plr)


def weight_matrix(node):
    return wmatrix_c(node.ptr, node.moving_plr, weight_pointer)


def count_colors(node):
    if not isinstance(node.ptr, ctypes.c_char_p) or not isinstance(node.moving_plr, int):
        print(node)
        print("CODE ERROR PANIC AAAAA")
        return 0
    return ccount_c(node.ptr, node.moving_plr)


def zobrist(node):
    h = 0 if node.moving_plr == helpers.BLACK else helpers.plr_xor
    return zobrist_c(array_pointer(board), bptr, wptr, h)


if __name__ == '__main__':
    board = helpers.from_tournament_format(
        list('???????????@@@@@oo@??@@@@@@@@??@@o@o@@@??@@@o@@o@??o@@@@@o@??o@@@ooo@??o@@@@oo@??..@@@@@@???????????'))
    buf = array.array('B', [0] * 64)
    print("Legal Moves result: " + str(legal_moves_c(array_pointer(board), 1, array_pointer(buf))))
    print("Arr: " + str(board))
    print("Buf: " + str(buf))
    print("Legal moves: " + str(helpers.legal_moves(board, 1)))
