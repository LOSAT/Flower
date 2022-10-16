import numba

@numba.njit
def iterate_buffer(buffer, callback):
    for i, v in enumerate(buffer):
        buffer[i] = callback(i, v)
    return buffer