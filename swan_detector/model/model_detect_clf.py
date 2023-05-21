""" Реализация двух нейронок:
1) Сначала детекция всех объектов класса 'Bird' на изображении
с помощью Yolo.
2) Классификации каждого вырезанного объекта из картинки с помощью
EfficientNet.
"""


import os
from datetime import datetime

from ultralytics import YOLO

from .utils import save_imgs, create_csv, analyse_target_class_by_conf
from keras.models import load_model
import cv2


def load_model_yolo(model_name: str) -> YOLO:
    """ Загрузка модели детекции.
    model_name: str - название предобученной модели.
    return: model """

    model = YOLO(model_name)
    return model


def load_model_clf(model_name: str):
    """ Загрузка модели классификации.
    model_name: str - название предобученной модели.
    return: model """

    model = load_model(model_name)
    return model


def cut_box_from_img(result):
    """ Выразение каждого лебедя с картинки.
    clf: модель классификация (keras).
    result: предсказанный результат из модели.
    return: list - список вырезанных картинок лебедей с одного изображения. """

    real_boxes = []
    for idx in range(len(result.boxes.data)):
        real_boxes.append(result.boxes.data[idx][0:4])

    int_points = []
    for tensor in real_boxes:
        int_points.append(list(
            [int(tensor[0]), int(tensor[2]), int(tensor[1]), int(tensor[3])],
        ))

    all_images = []
    for idx in range(len(int_points)):
        all_images.append(result.orig_img[int_points[idx][2]:int_points[idx][3], int_points[idx][0]:int_points[idx][1]])

    return all_images


def predict_classes_in_boxes(model, all_images):
    """ Предсказание классов каждого бокса.
    model: модель-классификатор.
    all_images: list - список вырезанных боксов лебедей из 1 изображения.
    return: list - предсказанные классы каждого бокса. """

    classes = []
    for image in all_images:
        # TODO: возможно будет ругаться на формат картинки.
        image = cv2.resize(image, dsize=(340, 340), interpolation=cv2.INTER_LINEAR)
        pred = model.predict(image)
        classes.append(pred)

    return classes


def predict_one(model_detect, model_clf, filename: str) -> dict:
    """ Предсказание детекции и класса лебедя.
    model_detect: ранее загруженная модель для предсказания детекции.
    model_clf: раннее загруженная модель для предсказания класса.
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
    result = model_detect(filename, conf=0.4, verbose=False)[0]

    # Получаю боксы вырезанных лебедей.
    all_images = cut_box_from_img(result)

    # Получаю классы, которые есть на изображении.
    classes = predict_classes_in_boxes(model_clf, all_images)

    # Преобразую результат в изображение с box.
    img = result.plot()

    # Достоверность предсказания того или иного класса.
    conf = []
    for i in result.boxes.conf:
        conf.append(i)

    # Количество лебедей на изображении.
    count_swan = len(classes)

    # Предсказанный класс для картинки.
    target_image = analyse_target_class_by_conf(classes, conf)

    # Результат предсказания хранится тут.
    final_dict = {
        'filename': filename,
        'classes': classes,
        'conf': conf,
        'count_swan': count_swan,
        'target_image': target_image,
        'img': img
    }

    return final_dict


def predict_many(model_detect, model_clf, list_filenames: list[str]) -> list[dict]:
    """ Предсказание списка файлов.
    model_detect: модель детекции.
    model_clf: моделб классификации.
    list_filenames: list[str] - список названий файлов или url.
    return: list[dict] - список предсказаний каждого изображения. """

    list_final_dict = []
    for filename in list_filenames:
        final_dict = predict_one(model_detect, model_clf, filename)
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


def run_detection(model_detect, model_clf, list_filenames: list[str], dir_save: str) -> list[dict]:
    list_final_dict = predict_many(model_detect, model_clf, list_filenames)
    dir_name = get_directory_name()
    dir_save = os.path.join(dir_save, dir_name)
    list_final_dict = save_imgs(list_final_dict, dir_save)
    create_csv(f"{dir_name}.csv", list_final_dict, dir_save)
    return list_final_dict


if __name__ == '__main__':
    run_detection()
