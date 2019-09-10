import cfunc_caller
import ctypes
import array
import helpers

var_code = b'\x45\x31\xc0\x40\x80\xfe\x01\x40\x0f\xbe\xce\x41\x0f\x94\xc0\x48\x8d\x77\x40\x31\xc0\x41\x83\xc0\x01\xeb\x19\x0f\x1f\x44\x00\x00\x41\x39\xd0\x0f\x94\xc2\x48\x83\xc7\x01\x0f\xb6\xd2\x29\xd0\x48\x39\xfe\x74\x13\x0f\xb6\x17\x39\xd1\x75\xe5\x48\x83\xc7\x01\x83\xc0\x01\x48\x39\xfe\x75\xed\xf3\xc3'

code = var_code

func = cfunc_caller.generate_function(code, ctypes.c_int, ctypes.c_char_p, ctypes.c_char)

board = helpers.from_tournament_format(list('???????????........??........??........??...o@...??...@o...??........??........??........???????????'))
board = helpers.from_tournament_format(list('???????????@@@@@oo@??@@@@@@@@??@@o@o@@@??@@@o@@o@??o@@@@@o@??o@@@ooo@??o@@@@oo@??..@@@@@@???????????'))

def array_pointer(arr):
    return ctypes.cast(arr.buffer_info()[0], ctypes.c_char_p)

print("Function result: " + str(func(array_pointer(board), 1)))
print("Arr: " + str(board))
print("Legal moves: " + str(helpers.legal_moves(board, 1)))
