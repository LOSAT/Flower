import numba

@numba.njit(fastmath=True)
def validate_fragment(buffer, base_index, rgb):
    return (
        buffer[base_index] == rgb[0] 
        and buffer[base_index + 1] == rgb[1] 
        and buffer[base_index + 2] == rgb[2]
    )