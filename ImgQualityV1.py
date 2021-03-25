from PIL import Image
import os


def number_adjacent_sharp_pixels(lamb, same_colors, width, height, pix, c, pixel_difference, same_pixels_difference,
                                 radius=1):  # Количество соседних резких пикселей.
    number_sharp_pixels = 0
    c1 = c2 = c3 = c

    for r in range(1, radius + 1):
        for x in range(r, width - r):
            for y in range(r, height - r):
                r1 = pix[x, y][0]
                g1 = pix[x, y][1]
                b1 = pix[x, y][2]
                # Пиксель по диагонали-сниз-справо.
                r2 = pix[x + r, y + r][0]
                g2 = pix[x + r, y + r][1]
                b2 = pix[x + r, y + r][2]
                if lamb(c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference) \
                        or same_colors(c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_sharp_pixels += 1
                # Пиксель справа.
                r2 = pix[x + r, y][0]
                g2 = pix[x + r, y][1]
                b2 = pix[x + r, y][2]
                if lamb(c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference) \
                        or same_colors(c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_sharp_pixels += 1
                # Пиксель снизу.
                r2 = pix[x, y + r][0]
                g2 = pix[x, y + r][1]
                b2 = pix[x, y + r][2]
                if lamb(c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference) \
                        or same_colors(c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_sharp_pixels += 1
                # Пиксель по диагонали-сверху-слева.
                r2 = pix[x - r, y - r][0]
                g2 = pix[x - r, y - r][1]
                b2 = pix[x - r, y - r][2]
                if lamb(c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference) \
                        or same_colors(c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_sharp_pixels += 1
                # Пиксель слева.
                r2 = pix[x - r, y][0]
                g2 = pix[x - r, y][1]
                b2 = pix[x - r, y][2]
                if lamb(c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference) \
                        or same_colors(c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_sharp_pixels += 1
                # Пиксель сверху.
                r2 = pix[x, y - r][0]
                g2 = pix[x, y - r][1]
                b2 = pix[x, y - r][2]
                if lamb(c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference) \
                        or same_colors(c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_sharp_pixels += 1
                # Пиксель по дигонали-сверху-справа.
                r2 = pix[x + r, y - r][0]
                g2 = pix[x + r, y - r][1]
                b2 = pix[x + r, y - r][2]
                if lamb(c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference) \
                        or same_colors(c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_sharp_pixels += 1
                # Пиксель по диагонали-снизу-слева.
                r2 = pix[x - r, y + r][0]
                g2 = pix[x - r, y + r][1]
                b2 = pix[x - r, y + r][2]
                if lamb(c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference) \
                        or same_colors(c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_sharp_pixels += 1

    res = round(number_sharp_pixels / (pow(2 * radius + 1, 2) - 1))
    return res


def img_quality(image):
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.
    pixel_difference = 55  # Разница между соседними пикселями.
    same_pixels_difference = 1;  # Разница между почти одинаковыми пикселями.
    c = 5  # Взвешивают перцептивную важность каждого из красных, зеленых и синих каналов.
    radius = 5  # В каком радиусе мы сравниваем наш пиксель.
    # contrast_moree = lambda c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference: \
    # max(c1 * abs(r1 - r2), c2 * abs(g1 - g2), c3 * abs(b1 - b2)) > pixel_difference  # Если высокая резкость.
    contrast_moree = lambda c1, c2, c3, r1, r2, g1, g2, b1, b2, pixel_difference: \
        (c1 * abs(r1 - r2) + c2 * abs(g1 - g2) + c3 * abs(b1 - b2)) > pixel_difference  # Если высокая резкость.
    # same_colors = lambda c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference: \
    # max(c1 * abs(r1 - r2), c2 * abs(g1 - g2), c3 * abs(b1 - b2)) < same_pixels_difference  # Если цвета почти одинаковые.
    same_colors = lambda c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference: \
        (abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)) < same_pixels_difference  # Если цвета почти одинаковые.

    number_sharp_pixels = number_adjacent_sharp_pixels(
        contrast_moree, same_colors, width, height, pix, c, pixel_difference, same_pixels_difference, radius
    )  # Кол-во резких пикселей-соседей.

    percent_sharp_pixels = round((number_sharp_pixels * 100 / (width * height)) * 3.06, 1)  # Процент резких пикселей-соседей.
    return [percent_sharp_pixels, "Очень плохо" if percent_sharp_pixels < 30
    else "Плохо" if percent_sharp_pixels < 50 else "Хорошо" if percent_sharp_pixels < 70 else "Отлично"]