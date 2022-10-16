from termios import VEOF
import numba

@numba.njit(fastmath=True)
def scala_multiply(vector, scala):
    new_vector = []
    for i in vector:
        new_vector.append(i * scala)
    return new_vector