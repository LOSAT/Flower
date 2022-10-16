import numba
from lib.nativeUtils.validate_fragment import validate_fragment

@numba.njit(fastmath=True)
def is_fragment_empty(buffer, index):
    return validate_fragment(buffer, index, (0, 0, 0))
