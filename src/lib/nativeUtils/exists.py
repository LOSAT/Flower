import numba

@numba.njit(fastmath=True)
def exists(buffer, index):
    return index <= len(buffer)