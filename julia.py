import numpy as np
from PIL import Image, ImageDraw
import itertools
import matplotlib.pyplot as plt
import time

import multiprocessing as mp


def is_julia(z, c, max_iter = 255):

    n = 0

    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1

    return int(n * 255 / max_iter)


def is_julia_rec(z, c, n = 0, max_iter = 255):
    # Slower by ~ 40 microseconds when z converges

    if abs(z) <= 2 and n < max_iter:
        return is_julia_rec(z * z + c, c, n = n + 1)
    else:
        return int(n * 255 / max_iter)


def interp(start, stop, size):
    return np.linspace(start, stop, size, dtype = int).tolist()


def make_image(inp):

    j, im = inp
    C = complex(real, im)

    pixels = [ lut[is_julia(complex(*k), C, MAX_ITER)] for k in combos ]

    # Make image
    img = Image.new('RGB', (DIMX, DIMY))
    img.putdata(pixels)

    name = '{}.{} - julia {:.3f} {:.3f}i'.format(i, j, C.real, C.imag)
    img.rotate(-90).save('anim/{}.png'.format(name), 'PNG')

    print(name)



def anim():

    MIN = 0
    MAX = 230

    # Julia params
    SCALE = 1
    OFFSETX = 0
    OFFSETY = 0
    MAX_ITER = 255

    # Image params
    DIMX = DIMY = 1000

    # Generate LUT (greyscale -> RGB)
    zeros = [MIN] * 51
    ones = [MAX] * 51

    r = interp(MIN, MAX, 153) + ones * 2
    g = interp(MIN, MAX, 204) + ones
    b = interp(MIN, MAX, 51) + interp(MAX, MIN, 102) + zeros + interp(MIN, MAX, 51)

    lut = list(zip(r,g,b)) + [(MAX,)*3]


    c_grid = ( complex(i,j) for i,j in itertools.product(
        np.arange(-2, 1.01, 0.01),
        np.arange(-1, 1.01, 0.01))
    )

    z_grid = [ complex(i,j) for i,j in itertools.product(
        np.linspace(-1.5 * SCALE - OFFSETX, 1.5 * SCALE - OFFSETX, DIMX),
        np.linspace(-1.5 * SCALE - OFFSETY, 1.5 * SCALE - OFFSETY, DIMY))
    ]

    frame = 0
    t = 0
    for c in c_grid:

        t0 = time.time()

        # Make image
        img = Image.new('RGB', (DIMX, DIMY))
        img.putdata( [ lut[is_julia(z, c, MAX_ITER)] for z in z_grid ] )

        name = '{:.3f},{:.3f}'.format(c.real, c.imag)
        img.rotate(-90).save('anim/{}.png'.format(name), 'PNG')

        frame += 1
        t += time.time() - t0
        print(name + ' {:.3} sec, {}%'.format(t/frame))


def main():

    # Colour intensities
    MIN = 0
    MAX = 230

    # Julia params
    C = complex(-0.7, -0.3)
    SCALE = 1
    OFFSETX = 0
    OFFSETY = 0
    MAX_ITER = 300

    # Image params
    DIMX = DIMY = 1000

    # Generate LUT (greyscale -> RGB)
    zeros = [MIN] * 51
    ones = [MAX] * 51

    r = interp(MIN, MAX, 153) + ones * 2
    g = interp(MIN, MAX, 204) + ones
    b = interp(MIN, MAX, 51) + interp(MAX, MIN, 102) + zeros + interp(MIN, MAX, 51)

    lut = list(zip(r,g,b)) + [(MAX,)*3]

    # #Plot LUT
    # xs = range(255)
    # fig, axs = plt.subplots(3)
    # axs[0].plot(xs, r, 'r-')
    # axs[1].plot(xs, g, 'g-')
    # axs[2].plot(xs, b, 'b-')
    # plt.show()

    # Compute Julia set
    t0 = time.time()
    combos = itertools.product(
        np.linspace(-1.5 * SCALE - OFFSETX, 1.5 * SCALE - OFFSETX, DIMX),
        np.linspace(-1.5 * SCALE - OFFSETY, 1.5 * SCALE - OFFSETY, DIMY))
    pixels = [ lut[is_julia_rec(complex(*i), C, MAX_ITER)] for i in combos ]
    print(time.time() - t0)

    # Make image
    img = Image.new('RGB', (DIMX, DIMY))
    img.putdata(pixels)

    # img.rotate(-90).save('julia {}.png'.format(str(C).replace('(', '').replace(')', '')), 'PNG')
    img.rotate(-90).show()

if __name__ == '__main__':

    main()
