import numba

def create_buffer_editor(callback):
    @numba.njit
    def func(buffer):
        for i, v in enumerate(buffer):
            buffer[i] = callback(i, v)
        return buffer
    return func