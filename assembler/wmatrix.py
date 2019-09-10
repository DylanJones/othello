import cfunc_caller
import ctypes
import array
import helpers

var_code = b'\x55\x48\x89\xe5\x48\x89\x7d\xe8\x89\xf0\x48\x89\x55\xd8\x88\x45\xe4\xc7\x45\xf8\x00\x00\x00\x00\xc7\x45\xfc\x00\x00\x00\x00\x83\x7d\xfc\x3f\x7f\x78\x8b\x45\xfc\x48\x63\xd0\x48\x8b\x45\xe8\x48\x01\xd0\x0f\xb6\x00\x0f\xb6\xd0\x0f\xbe\x45\xe4\x39\xc2\x75\x18\x8b\x45\xfc\x48\x63\xd0\x48\x8b\x45\xd8\x48\x01\xd0\x0f\xb6\x00\x0f\xbe\xc0\x01\x45\xf8\xeb\x3f\x8b\x45\xfc\x48\x63\xd0\x48\x8b\x45\xe8\x48\x01\xd0\x0f\xb6\x00\x0f\xb6\xc0\x80\x7d\xe4\x01\x75\x07\xba\x02\x00\x00\x00\xeb\x05\xba\x01\x00\x00\x00\x39\xc2\x75\x16\x8b\x45\xfc\x48\x63\xd0\x48\x8b\x45\xd8\x48\x01\xd0\x0f\xb6\x00\x0f\xbe\xc0\x29\x45\xf8\x83\x45\xfc\x01\xeb\x82\x8b\x45\xf8\x5d\xc3'

code = var_code

func = cfunc_caller.generate_function(code, ctypes.c_int, ctypes.c_char_p, ctypes.c_char, ctypes.c_char_p)

board = helpers.from_tournament_format(list('???????????........??........??........??...o@...??...@o...??........??........??........???????????'))
board = helpers.from_tournament_format(list('???????????@@@@@oo@??@@@@@@@@??@@o@o@@@??@@@o@@o@??o@@@@@o@??o@@@ooo@??o@@@@oo@??..@@@@@@???????????'))
SQUARE_WEIGHTS = [    120, -20, 20, 5, 5, 20, -20, 120,    -20, -40, -5, -5, -5, -5, -40, -20,    20, -5, 15, 3, 3, 15, -5, 20,    5, -5, 3, 3, 3, 3, -5, 5,    5, -5, 3, 3, 3, 3, -5, 5,    20, -5, 15, 3, 3, 15, -5, 20,    -20, -40, -5, -5, -5, -5, -40, -20,    120, -20, 20, 5, 5, 20, -20, 120]
buf = array.array('b', SQUARE_WEIGHTS)

def array_pointer(arr):
    return ctypes.cast(arr.buffer_info()[0], ctypes.c_char_p)

print("Function result: " + str(func(array_pointer(board), 1, array_pointer(buf))))
print("Arr: " + str(board))
print("Buf: " + str(buf))
print("Legal moves: " + str(helpers.legal_moves(board, 1)))
