""" В данном модуле реализовано предсказание классов на
основе голосавания n-числа моделей yolo.
Алгоритм:
1) Каждая отдельная модель предсказывает класс.
2) Дальше все результаты всех моделей анализируются.
3) Делается вердикт на основе обобщения результатов всех моделей. """


import os
from datetime import datetime


from ultralytics import YOLO

from .utils import save_imgs, create_csv, analyse_target_class_by_conf


def load_model(path: str) -> YOLO:
    """ Загрузка модели.
    return: model """

    model = YOLO(path)
    return model


def predict_one(model_list, filename: str) -> dict:
    """ Предсказание детекции и класса лебедя.
    model: list - ранее загруженные модели для предсказания.
    filename: str - название ОДНОГО файла или url
    
    return: dict - результат предсказания в формате 
    {
        'filename': str,  # Название изображения.
        'classes': list,  # Классы, которые имеются на изображении.
        'conf': list,  # Достоверность предсказанного класса.
        'count_swan': list,  # Кол-во лебедей на изображении.
        'target_image': str,  # Предсказанный класс для картинки.
        'img': Image  # Изображение с боксами лебедей.
    }
    """

    # Делаю предсказание.
    results = []
    for model in model_list:
        result = model(filename, conf=0.4)[0]
        result.append(result)

    # Преобразую результат в изображение с box.
    img = result[0].plot()  # TODO: вывод рандомой первого изображения.

    # Получаю классы, которые есть на изображении.
    classes = []
    for result in results:
        tmp_classes = []
        for i in result.boxes.cls:
            tmp_classes.append(model.names[int(i)])
        classes.append(tmp_classes)

    # Достоверность предсказания того или иного класса.
    conf = []
    for result in results:
        tmp_conf = []
        for i in result.boxes.conf:
            tmp_conf.append(i)
        conf.append(tmp_conf)

    # Количество лебедей на изображении.
    list_count_swan = []
    for tmp_classes in classes:
        list_count_swan.append(len(tmp_classes))

    # Предсказанный класс для картинки.
    list_target_image = []
    for i in range(len(tmp_classes)):
        target_image = analyse_target_class_by_conf(classes[i], conf[i])
        list_target_image.append(target_image)

    # Итоговый таргет изображения на основе голосования по количеству.
    target_image = max(list_target_image, key=list_target_image.count)

    # Результат предсказания хранится тут.
    final_dict = {
        'filename': filename,
        'classes': classes,
        'conf': conf,
        'list_count_swan': list_count_swan,
        'target_image': target_image,
        'img': img
    }

    return final_dict


def predict_many(model_list, list_filenames: list[str]) -> list[dict]:
    """ Предсказание списка файлов.
    model_list: список моделей детекции.
    list_filenames: list[str] - список названий файлов или url.
    return: list[dict] - список предсказаний каждого изображения. """

    list_final_dict = []
    for filename in list_filenames:
        final_dict = predict_one(model_list, filename)
        list_final_dict.append(final_dict)

    return list_final_dict


def get_directory_name() -> str:
    bad_symbols = (" ", ".", ":")
    now_datetime = []
    for symbol in str(datetime.now()):
        now_datetime.append(
            symbol if symbol not in bad_symbols else "-"     
        )
    return f"detection_{''.join(now_datetime)}"


def run_detection(model_list: list, list_filenames: list[str], dir_save: str) -> list[dict]:
    list_final_dict = predict_many(model_list, list_filenames)
    dir_name = get_directory_name()
    dir_save = os.path.join(dir_save, dir_name)
    list_final_dict = save_imgs(list_final_dict, dir_save)
    create_csv(f"{dir_name}.csv", list_final_dict, dir_save)
    return list_final_dict


if __name__ == '__main__':
    run_detection()
