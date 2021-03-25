from PIL import Image
import os


# Количество соседних резких пикселей.
def number_adjacent_sharp_pixels(
        is_high_contrast, is_similar_colors,
        width, height, pix, c,
        pixel_difference, same_pixels_difference, radius=1):

    number_sharp_pixels = 0  # Число соседей с высокой контрастностью.
    number_one_color_pix = 0  # Кол-во пикселей соседей с одинаковым цветом.

    for r in range(1, radius + 1):
        for x in range(r, width - r):
            for y in range(r, height - r):
                r1 = pix[x, y][0]
                g1 = pix[x, y][1]
                b1 = pix[x, y][2]
                # Пиксель по диагонали-снизу-справо.
                r2 = pix[x + r, y + r][0]
                g2 = pix[x + r, y + r][1]
                b2 = pix[x + r, y + r][2]
                if is_high_contrast(c, r1, r2, g1, g2, b1, b2, pixel_difference):
                    number_sharp_pixels += 1
                elif is_similar_colors(r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_one_color_pix += 1
                # Пиксель справа.
                r2 = pix[x + r, y][0]
                g2 = pix[x + r, y][1]
                b2 = pix[x + r, y][2]
                if is_high_contrast(c, r1, r2, g1, g2, b1, b2, pixel_difference):
                    number_sharp_pixels += 1
                elif is_similar_colors(r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_one_color_pix += 1
                # Пиксель снизу.
                r2 = pix[x, y + r][0]
                g2 = pix[x, y + r][1]
                b2 = pix[x, y + r][2]
                if is_high_contrast(c, r1, r2, g1, g2, b1, b2, pixel_difference):
                    number_sharp_pixels += 1
                elif is_similar_colors(r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_one_color_pix += 1
                # Пиксель по диагонали-сверху-слева.
                r2 = pix[x - r, y - r][0]
                g2 = pix[x - r, y - r][1]
                b2 = pix[x - r, y - r][2]
                if is_high_contrast(c, r1, r2, g1, g2, b1, b2, pixel_difference):
                    number_sharp_pixels += 1
                elif is_similar_colors(r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_one_color_pix += 1
                # Пиксель слева.
                r2 = pix[x - r, y][0]
                g2 = pix[x - r, y][1]
                b2 = pix[x - r, y][2]
                if is_high_contrast(c, r1, r2, g1, g2, b1, b2, pixel_difference):
                    number_sharp_pixels += 1
                elif is_similar_colors(r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_one_color_pix += 1
                # Пиксель сверху.
                r2 = pix[x, y - r][0]
                g2 = pix[x, y - r][1]
                b2 = pix[x, y - r][2]
                if is_high_contrast(c, r1, r2, g1, g2, b1, b2, pixel_difference):
                    number_sharp_pixels += 1
                elif is_similar_colors(r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_one_color_pix += 1
                # Пиксель по дигонали-сверху-справа.
                r2 = pix[x + r, y - r][0]
                g2 = pix[x + r, y - r][1]
                b2 = pix[x + r, y - r][2]
                if is_high_contrast(c, r1, r2, g1, g2, b1, b2, pixel_difference):
                    number_sharp_pixels += 1
                elif is_similar_colors(r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_one_color_pix += 1
                # Пиксель по диагонали-снизу-слева.
                r2 = pix[x - r, y + r][0]
                g2 = pix[x - r, y + r][1]
                b2 = pix[x - r, y + r][2]
                if is_high_contrast(c, r1, r2, g1, g2, b1, b2, pixel_difference):
                    number_sharp_pixels += 1
                elif is_similar_colors(r1, r2, g1, g2, b1, b2, same_pixels_difference):
                    number_one_color_pix += 1

    remove_excess_compare = pow(2 * radius + 1, 2) - 1  # На сколько убрать лишние сравнения.
    res = [1 if number_sharp_pixels == 0 else round(number_sharp_pixels / remove_excess_compare),
           round(number_one_color_pix / remove_excess_compare + 2 * height + 2 * width - 2)]
    return res


def img_quality(image):
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.

    pixels_difference = 50  # Разница между соседними пикселями.
    same_pixels_difference = 5;  # Разница между почти одинаковыми пикселями.
    c = 5  # Взвешивают перцептивную важность каждого из красных, зеленых и синих каналов.
    radius = 1  # В каком радиусе мы сравниваем наш пиксель.
    # is_high_contrast = lambda c1, c2, c3, r1, r2, g1, g2, b1, b2, pixels_difference: \
    # max(c1 * abs(r1 - r2), c2 * abs(g1 - g2), c3 * abs(b1 - b2)) > pixels_difference  # Если высокая резкость.
    is_high_contrast = lambda c, r1, r2, g1, g2, b1, b2, pixels_difference: \
        (c * abs(r1 - r2) + c * abs(g1 - g2) + c * abs(b1 - b2)) > pixels_difference  # Если высокая резкость.
    # is_similar_colors = lambda c1, c2, c3, r1, r2, g1, g2, b1, b2, same_pixels_difference: \
    # max(c1 * abs(r1 - r2), c2 * abs(g1 - g2), c3 * abs(b1 - b2)) < same_pixels_difference  # Если цвета почти одинаковые.
    is_similar_colors = lambda r1, r2, g1, g2, b1, b2, same_pixels_difference: \
        (abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)) < same_pixels_difference  # Если цвета почти одинаковые.

    number_sharp_pixels = number_adjacent_sharp_pixels(
        is_high_contrast, is_similar_colors,
        width, height, pix, c,
        pixels_difference, same_pixels_difference, radius
    )  # Кол-во резких пикселей-соседей.

    size_img = width * height

    if number_sharp_pixels[1] == size_img:  # Во избежания деления на 0.
        number_sharp_pixels[1] -= 1

    percent_sharp_pixels = round(
        (number_sharp_pixels[0] * 100 / (size_img - number_sharp_pixels[1])), 1)  # Процент резких пикселей-соседей.

    return [percent_sharp_pixels, "Очень плохо" if percent_sharp_pixels < 30
    else "Плохо" if percent_sharp_pixels < 50 else "Хорошо" if percent_sharp_pixels < 70 else "Отлично"]
