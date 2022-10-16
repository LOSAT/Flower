import numba

@numba.njit(fastmath=True)
def indexize(width, x, y): # 일반적인 경우에도 사용 가능하게끔 하자.
    return (y * width + x) * 3