import numba

# 진지하게 스텐실 커널도 구현 고려해보자.
def stencil(func):
    @numba.njit
    def kernel(buffer):
        # statements...
        return buffer