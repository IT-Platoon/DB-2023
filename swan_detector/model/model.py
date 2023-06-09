import os
from datetime import datetime

from ultralytics import YOLO

from .utils import (
    save_imgs,
    create_csv_custom,
    analyse_target_class_by_conf,
    analyse_target_class_by_count,
)


def load_model(path: str) -> YOLO:
    """ Загрузка модели.
    return: model """

    model = YOLO(path)
    return model


def predict_one(model, filename: str) -> dict:
    """ Предсказание детекции и класса лебедя.
    model: ранее загруженная модель для предсказания.
    filename: str - название ОДНОГО файла или url
    
    return: dict - результат предсказания в формате 
    {
        'filename': str,  # Название изображения.
        'classes': list,  # Классы, которые имеются на изображении.
        'conf': list,  # Достоверность предсказанного класса.
        'count_swan': int,  # Кол-во лебедей на изображении.
        'target_image': str,  # Предсказанный класс для картинки.
        'img': Image  # Изображение с боксами лебедей.
    }
    """

    # Делаю предсказание.
    result = model(filename, conf=0.4, verbose=False)[0]

    # Преобразую результат в изображение с box.
    img = result.plot()

    # Получаю классы, которые есть на изображении.
    classes = []
    for i in result.boxes.cls:
        classes.append(model.names[int(i)])

    # Достоверность предсказания того или иного класса.
    conf = []
    for i in result.boxes.conf:
        conf.append(i)

    # Количество лебедей на изображении.
    count_swan = len(classes)

    # Предсказанный класс для картинки.
    target_image = analyse_target_class_by_count(classes, conf)

    # Результат предсказания хранится тут.
    final_dict = {
        'filename': filename,
        'classes': classes,
        'conf': conf,
        'count_swan': count_swan,
        'target_image': target_image,
        'img': img,
    }

    return final_dict


def predict_many(model, list_filenames: list[str]) -> list[dict]:
    """ Предсказание списка файлов.
    model: модель, которая предсказывает.
    list_filenames: list[str] - список названий файлов или url.
    return: list[dict] - список предсказаний каждого изображения. """

    list_final_dict = []
    for filename in list_filenames:
        final_dict = predict_one(model, filename)
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


def run_detection(model, list_filenames: list[str], dir_save: str) -> list[dict]:
    list_final_dict = predict_many(model, list_filenames)
    dir_name = get_directory_name()
    dir_save = os.path.join(dir_save, dir_name)
    list_final_dict = save_imgs(list_final_dict, dir_save)
    create_csv_custom(
        f"{dir_name}.csv",
        list_final_dict,
        dir_save,
        submission_flag=True,
    )
    return list_final_dict


if __name__ == '__main__':
    run_detection()
