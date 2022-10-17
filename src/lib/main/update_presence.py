import numba
import numpy
from lib.nativeUtils.indexize import indexize
from lib.nativeUtils.exists import exists

@numba.stencil
def depr_update_presence(buffer):
    current = buffer[0, 0]
    presence = -1
    if current == 1: # current is water
        if buffer[0, 1] == 0: # down
            presence = 0
        elif buffer[1, 1] == 0: # right down
            presence = 0
        elif buffer[-1, 1] == 0: # left down
            presence = 0
        elif buffer[1, 0] == 0: # right
            presence = 0
        elif buffer[-1, 0] == 0: # left
            presence = 0
    elif current == 0:
        if buffer[0, -1] == 1: # down
            presence = 1
        elif buffer[-1, -1] == 1: # right down
            presence = 1
        elif buffer[1, -1] == 1: # left down
            presence = 1
        elif buffer[-1, 0] == 1: # right
            presence = 1
        elif buffer[1, 0] == 1: # left
            presence = 1
    
    return presence

@numba.njit(fastmath=True)
def update_presence(buffer, data, width):

    mem = numpy.zeros(len(buffer)) # 이거 안해도 되게끔 수정해야됨

    updated = buffer[:]
    for i in range(len(buffer)):

        velocity = data[i]

        down = i + width
        left_down = i + width - 1
        right_down = i + width + 1
        left = i - 1
        right = i + 1

        if buffer[i] == 2 and mem[i] == 0:
            if exists(buffer, down):
                if buffer[down] == 0:
                    updated[i] = 0
                    updated[down] = 2
                    mem[down] = 2 
                    continue
                elif buffer[down] == 1:
                    updated[i] = 1
                    updated[down] = 2
                    mem[down] = 2 
                    continue        
            if exists(buffer, right_down):
                if buffer[right_down] == 0:
                    updated[i] = 0
                    updated[right_down] = 2
                    mem[right_down] = 2 
                    continue
            if exists(buffer, left_down):
                if buffer[left_down] == 0:
                    updated[i] = 0
                    updated[left_down] = 2
                    mem[left_down] = 2 

        if buffer[i] == 1 and mem[i] == 0: # 물
            if buffer[down] != 0:
                data[i] = 0
            else:
                data[i] += 2

            max_dist = 0
            for y in range(1, data[i] + 1):
                if exists(buffer, down + width * y):
                    if buffer[down + width * y] != 0:
                        break
                    max_dist += 1

            max_dist -= 1
            updated[i] = 0
            updated[down + width * max_dist] = 1
            mem[down + width * max_dist] = 1

            if exists(buffer, right_down) and max_dist == -1:
                if buffer[right_down] == 0:
                    updated[i] = 0
                    updated[right_down] = 1
                    mem[right_down] = 1 
                    continue
            if exists(buffer, left_down) and max_dist == -1:
                if buffer[left_down] == 0:
                    updated[i] = 0
                    updated[left_down] = 1
                    mem[left_down] = 1
                    continue
            if exists(buffer, right) and max_dist == -1:
                if buffer[right] == 0:
                    updated[i] = 0
                    updated[right] = 1
                    mem[right] = 1 
                    continue
            if exists(buffer, left) and max_dist == -1:
                if buffer[left] == 0:
                    updated[i] = 0
                    updated[left] = 1
                    mem[left] = 1 
                    continue
                
    return updated