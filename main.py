from ImgQualityV2 import *


def sort_by_length(input_str):  # Сортировка имен файлов в директории.
    return len(input_str)


directory = r"Img"  # Путь к картинкам.
#directory = r"Simple Case"
#directory = r"Rezkosti Img"
listdir = sorted(os.listdir(directory))
listdir.sort(key=sort_by_length)
for name in listdir:
    result = img_quality(Image.open(directory + "\\" + name))
    print("%-13s%-13s%-6s%-6s" % (name, " - качество:", result[0], result[1]))


# Нам нужно чтобы соседний пиксель как можно скорее менял свою контрастность, либо не менял ее совсем.
# Если соседний пиксель меняет свою контрасность слишком медленно, значит четкость низкая.

# Если пиксель одинакового цвета складываем их и затем вичитаем из ширина*высота.
# А там где контрастность высокая +1 в переменную с контрастными соседями.

# Для определения качества отдельного изображения:
# print(img_quality(Image.open(r"ИМЯ_ДИРЕКТОРИИ" + "\\" + "ИМЯ_ИЗОБРАЖЕНИЯ")))
