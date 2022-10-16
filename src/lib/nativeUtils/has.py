import numba
import numpy

@numba.njit(fastmath=True)
def has(vec, val):
    res = False
    if numpy.where(vec == val)[0].shape[0] > 0:
        res = True
    return res