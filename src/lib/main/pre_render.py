import enum
import numba
import numpy
from lib.nativeUtils.indexize import indexize

@numba.njit(fastmath=True)
def depr_pre_render(presence_buffer, fragment_buffer):
    c = 0
    presence_buffer_x = 0
    presence_buffer_y = 0
    for _i in range(len(fragment_buffer) // 3):
        i = _i * 3
        if c % 800 == 0:
            presence_buffer_y = presence_buffer_y + 1
            presence_buffer_x = 0
        if presence_buffer[presence_buffer_y][presence_buffer_x] == 0:
            fragment_buffer[i] = 0
            fragment_buffer[i + 1] = 0
            fragment_buffer[i + 2] = 0
        elif presence_buffer[presence_buffer_y][presence_buffer_x] == 1:
            fragment_buffer[i] = 0
            fragment_buffer[i + 1] = 0
            fragment_buffer[i + 2] = 255
        c = c + 3   
        presence_buffer_x = presence_buffer_x + 1

@numba.njit(fastmath=True)
def pre_render(presence_buffer, fragment_buffer):

    for _i in range(len(fragment_buffer) // 3):

        i = _i * 3

        if presence_buffer[_i] == 0: # 허공
            fragment_buffer[i] = 0
            fragment_buffer[i + 1] = 0
            fragment_buffer[i + 2] = 0
        elif presence_buffer[_i] == 1: # 물
            fragment_buffer[i] = 0
            fragment_buffer[i + 1] = 0
            fragment_buffer[i + 2] = 255
        elif presence_buffer[_i] == 2: # 모래
            fragment_buffer[i] = 225
            fragment_buffer[i + 1] = 191
            fragment_buffer[i + 2] = 146
        elif presence_buffer[_i] == 3: # 돌
            fragment_buffer[i] = 99
            fragment_buffer[i + 1] = 99
            fragment_buffer[i + 2] = 99
