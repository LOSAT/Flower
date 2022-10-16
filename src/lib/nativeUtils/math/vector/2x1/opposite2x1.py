import numba

@numba.njit
def opposite2x1(vec):
    return [vec[0] * -1, vec[1] * -1]