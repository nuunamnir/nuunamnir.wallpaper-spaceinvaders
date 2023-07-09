import argparse

import numpy
import PIL.Image
import PIL.ImageDraw


def generate_spaceinvader(rng, detail=5):
    left_side = rng.integers(low=0, high=2, size=(detail // 2, detail))
    right_side = numpy.flipud(left_side)
    middle = rng.integers(low=0, high=2, size=(1, detail))
    return numpy.rot90(numpy.concatenate((left_side, middle, right_side), axis=0))

def draw_spaceinvader(canvas, spaceinvader, x, y, color, size=8):
    for i in range(spaceinvader.shape[0]):
        for j in range(spaceinvader.shape[1]):
            if spaceinvader[i, j] == 1:
                canvas.rectangle(((x + j * size + 1, y + i * size + 1), (x + (j + 1) * size - 2, y + (i + 1) * size - 2)), fill=color)


def generate(output_file_name, seed=2106, width=3840, height=2160, detail=5, size=16, background_color=(233, 250, 227), foreground_colors=[(172, 146, 166), (213, 199, 188), (222, 232, 213), (23, 250, 227)]):
    wallpaper = PIL.Image.new(size=(width, height), mode='RGB', color=background_color)
    canvas = PIL.ImageDraw.Draw(wallpaper)

    rng = numpy.random.default_rng(seed=seed)
    
    cells_x = width // ((detail + 4) * size)
    cells_y = height // ((detail + 4) * size)

    offset_x = (width - cells_x * (detail + 4) * size)
    offset_y = (height - cells_y * (detail + 4) * size)
    for i in range(1, cells_y - 1):
        for j in range(1, cells_x - 1):
            spaceinvader = generate_spaceinvader(rng=rng, detail=5)
            draw_spaceinvader(canvas=canvas, spaceinvader=spaceinvader, x=offset_x + j * (detail + 4) * size, y=offset_y + i * (detail + 4) * size, color=foreground_colors[rng.integers(low=0, high=len(foreground_colors))], size=size)
    
    wallpaper.save(output_file_name)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='generate',
        description='generates a wallpaper inspired by the spaceinvader game',)

    themes = {
        'default': {
            'background_color': (233, 250, 227),
            'foreground_colors': [(172, 146, 166), (213, 199, 188), (222, 232, 213), (23, 250, 227)],
        },
        'dark': {
            'background_color': (53, 30, 41),
            'foreground_colors': [(109, 211, 206), (155, 222, 183), (200, 233, 160), (224, 198, 140), (247, 162, 120), (161, 61, 99), (107, 46, 70)],
        },
        'light': {
            'background_color': (248, 247, 255),
            'foreground_colors': [(147, 129, 255), (166, 157, 255), (184, 184, 255), (216, 216, 255), (252, 243, 238), (255, 238, 221), (255, 227, 206), (255, 216, 190)],
        },
        'colorful': {  
            'background_color': (1, 22, 39),
            'foreground_colors': [(128, 11, 37), (255, 0, 34), (160, 117, 123), (65, 234, 212), (159, 245, 232), (253, 255, 252), (219, 137, 183), (185, 19, 114)],
        },
    }

    parser.add_argument('-x', '--width', dest='width', type=int, help='wallpaper width in pixel', required=False, default=3840)
    parser.add_argument('-y', '--height', dest='height', type=int, help='wallpaper height in pixel', required=False, default=2160)
    parser.add_argument('-t', '--theme', dest='theme', type=str, help='color theme for the wallpaper', required=False, default='colorful', choices=themes.keys())
    parser.add_argument('-s', '--seed', dest='seed', type=int, help='random number generator seed', required=False, default=2106)
    parser.add_argument(dest='output', type=str, help='output file name', default='wallpaper.png')
    args = parser.parse_args()

    generate(args.output, seed=args.seed, width=args.width, height=args.height, foreground_colors=themes[args.theme]['foreground_colors'], background_color=themes[args.theme]['background_color'])