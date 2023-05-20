import os
from typing import Callable

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def analyse_target_class_by_conf(classes: list, conf: list) -> str:
    """ Бывают случаи, когда модель на одном изображении видит
    лебедей нескольких классов.
    Здесь будет искаться по параметру сумме conf каждого класса.
    У какого класса больше conf, тот и будет таргетом.
    return: str - target class. """
    summator = {}
    for i in range(len(classes)):

        name_class = classes[i]

        if name_class not in summator:
            summator[name_class] = conf[i].item()

        else:
            summator[name_class] += conf[i].item()
    
    return max(summator, key=summator.get)


def analyse_target_class_by_count(classes: list, conf: list = None) -> str:
    """ Бывают случаи, когда модель на одном изображении видит
    лебедей нескольких классов.
    Таргетом будет тот класс, которого больше предсказано на изображении.
    return: str - target class. """

    summator = {}
    for i in range(len(classes)):

        name_class = classes[i]

        if name_class not in summator:
            summator[name_class] = 1

        else:
            summator[name_class] += 1
    
    return max(summator, key=summator.get)


def create_csv(
    filename_csv: str,
    list_final_dict: list,
    dir_save: str,
    analyzer: Callable[[list, list | None], str] = analyse_target_class_by_conf,
) -> None:
    """ Создание csv-файла с двумя колонками: (filename, target).
    filename_csv: str - название csv файла.
    list_final_dict: list[dict] - список предсказанных изображений.
    analyzer: function - функция подсчёта таргета на изображении.
    return: None """

    list_filename = []
    list_target = []

    # Определяю target каждого изображения.
    for final_dict in list_final_dict:

        list_filename.append(final_dict['filename'])

        analyzed_target_class = analyzer(
            final_dict['classes'],
            final_dict['conf']
        )
        list_target.append(analyzed_target_class)

    df = pd.DataFrame(
        {
            'filename': list_filename,
            'target': list_target
        }
    )

    df.to_csv(os.path.join(dir_save, filename_csv), index=False)


def save_imgs(list_final_dict: list, dir_save: str) -> list[dict]:
    """ Сохранение всех предсказанных изображений с боксами.
    list_final_dict: list[dict] - предсказанные данные.
    dir_save: str - директория, в которую сохранить предсказанные изображения.
    return: None """

    # Создание папки
    if not os.path.isdir(dir_save):
        os.mkdir(dir_save)

    for final_dict in list_final_dict:
        filename = os.path.basename(final_dict["filename"])
        path = os.path.join(dir_save, filename)
        final_dict["result_path"] = path
        image = cv2.cvtColor(final_dict["img"], cv2.COLOR_BGR2RGB)
        pixels = np.array(image)
        plt.imsave(path, pixels)
    return list_final_dict
