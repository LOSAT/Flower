import numba
import math
import numpy
from OpenGL.GL import *
from glfw import *
import platform
import os

from lib.main.pre_render import pre_render
from lib.main.update_presence import update_presence

try:
    del os.environ['DISPLAY']
except:
    pass

env = platform.system()
def os_pick(win, mac):
    if env == "Darwin":
        return mac
    else:
        return win

screen_width, screen_height = (1920, 1080) # os_pick 2배 제거 (임시방편)


fragment_buffer = numpy.zeros(screen_width * screen_height * 3)
presence_buffer = numpy.zeros(screen_width * screen_height)
presence_data_buffer = numpy.zeros(screen_width * screen_height * 1)
click = False
fill_mode = None
keys = {
    "q": False,
    "w": False
}


def indexize_normal(width, x, y):
    return (y * width + x)

def fill_water(x, y):
    if(indexize_normal(screen_width, x, y) <= len(presence_buffer)):
        index = indexize_normal(screen_width, x, y)
        presence_buffer[index] = 1

def fill_sand(x, y):
    if(indexize_normal(screen_width, x, y) <= len(presence_buffer)):
        index = indexize_normal(screen_width, x, y)
        presence_buffer[index] = 2

def fill_stone(x, y):
    if(indexize_normal(screen_width, x, y) <= len(presence_buffer)):
        index = indexize_normal(screen_width, x, y)
        presence_buffer[index] = 3
def on_click(_, button, action, __):
    global click
    if button == MOUSE_BUTTON_LEFT:
        if action == PRESS:
            click = "left"
        elif action == RELEASE:
            click = False
    elif button == MOUSE_BUTTON_RIGHT:
        if action == PRESS:
            click = "right"
        elif action == RELEASE:
            click = False

def on_move(window, x, y):
    if click:

        int_x = math.floor(os_pick(x, x * 2))
        int_y = math.floor(os_pick(y, y * 2))

        random_range = 10

        stone_fill_y = -5
        stone_fill_x = 0
        for i in range(100):
            random_x = numpy.random.randint(-random_range, random_range)
            random_y = numpy.random.randint(-random_range, random_range)
            if click == "left":
                if keys["q"]: # 돌 채우기 모드
                    fill_stone(int_x + stone_fill_x, int_y + stone_fill_y)
                    if stone_fill_x == 10:
                        stone_fill_x = 0
                        stone_fill_y += 1
                    stone_fill_x += 1
                elif keys["w"]:
                    fill_sand(int_x + random_x, int_y + random_y)
                else:
                    fill_water(int_x + random_x, int_y + random_y)


def on_key_event(window, key, scancode, action, mods):
    pass

    
def main(title, version):
    global presence_buffer
    global fragment_buffer
    time = 0
    init()
    window = create_window(
        os_pick(screen_width, screen_width // 2), 
        os_pick(screen_height, screen_height // 2), 
        f"{title} {version}", 
        None, 
        None
    )
    make_context_current(window)
    set_mouse_button_callback(window, on_click)
    set_cursor_pos_callback(window, on_move)
    set_key_callback(window, on_key_event)

    if env == "Darwin":
        fb_width, fb_height = get_framebuffer_size(window)
        _x = -(screen_width - fb_width) // 2
        _y = -(screen_height - fb_height) // 2
        glViewport(_x, _y, screen_width, screen_height)
    else:
        glViewport(0, 0, screen_width, screen_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, screen_width, 0, screen_height, 0, 10)
    glPixelZoom(1, -1)
    glRasterPos3f(0, screen_height, -0.3)

    while not window_should_close(window):
        if get_key(window, KEY_Q) == PRESS:
            keys["q"] = True
        else:
            keys["q"] = False
        
        if get_key(window, KEY_W) == PRESS:
            keys["w"] = True
        else:
            keys["w"] = False
        glClearColor(0, 0, 0, 255)
        glClear(GL_COLOR_BUFFER_BIT)

        presence_buffer = update_presence(presence_buffer, presence_data_buffer, screen_width)
        pre_render(presence_buffer, fragment_buffer)

        glDrawPixels(
            screen_width, 
            screen_height, 
            GL_RGB, 
            GL_UNSIGNED_BYTE, 
            fragment_buffer
        )
        swap_buffers(window)
        poll_events()
        time = time + 1
    terminate()

main("Flower", 1.0)
