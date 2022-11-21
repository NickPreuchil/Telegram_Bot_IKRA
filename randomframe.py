import random
import google_sheets_api

# для поиска корней
import pymorphy2

# Подключаем анализатор склонений
morph = pymorphy2.MorphAnalyzer()


# возвращаем случайное слово из файлового списка
def return_random_frame(table_name):

    how_dict_content = google_sheets_api.get_table(table_name)

    # разбиваем текст на слова
    how_array = how_dict_content.split('\n')
    random_index = random.randint(0, len(how_array) - 1)

    return how_array[random_index].replace('\r', '')


def construct_frame():
    # вытаскиваем случайные слова из словаря
    how_word = return_random_frame(google_sheets_api.TABLE_HOW)
    frame_word = return_random_frame(google_sheets_api.TABLE_FRAME)
    which_word = return_random_frame(google_sheets_api.TABLE_WHICH)

    # находим нужно слово для склонения в кавычках
    full_frame_word = frame_word
    frame_word = frame_word.split('"')
    frame_word = frame_word[1]
    # print(f'{frame_word=}')

    # парсим для понимания рода
    which_p = morph.parse(which_word)
    frame_p = morph.parse(frame_word)

    # Меняем род первого слова на нужное

    try:
        which_p[0] = which_p[0].inflect({frame_p[0].tag.gender})
    except ValueError as _:
        pass

    if which_p[0] is None:
        return construct_frame()

    # Суммируем и выводим итоговый фрейм
    output_frame = which_p[0].word.strip() + ' ' + full_frame_word.replace('"', '').strip() + ' ' + how_word.strip()
    return str(output_frame).capitalize()

