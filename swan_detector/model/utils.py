import pandas as pd
import matplotlib.pyplot as plt
import os


def analyse_target_class(classes: list, conf: list):
    """ Бывают случаи, когда модель на одном изображении видит
    лебедей нескольких классов.
    Здесь будет искаться по параметру сумме conf каждого класса.
    У какого класса больше conf, тот и будет таргетом.
    return: str - target class. """

    summator = {}
    for i in range(len(classes)):

        name_class = classes[i]

        if name_class not in summator:
            summator[name_class] = conf[i]

        else:
            summator[name_class] += conf[i]
    
    return max(summator, key=summator.get)


def create_csv(filename_csv: str, list_final_dict: list):
    """ Создание csv-файла с двумя колонками: (filename, target).
    filename_csv: str - название csv файла.
    list_final_dict: list[dict] - список предсказанных изображений.
    return: None """

    list_filename = []
    list_target = []

    # Определяю target каждого изображения.
    for final_dict in list_final_dict:

        list_filename.append(final_dict['filename'])

        analyzed_target_class = analyse_target_class(
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

    df.to_csv(filename_csv)


def save_imgs(list_final_dict: list, dir_save: str):
    """ Сохранение всех предсказанных изображений с боксами.
    list_final_dict: list[dict] - предсказанные данные.
    dir_save: str - директория, в которую сохранить предсказанные изображения.
    return: None """

    # Создание папки
    if not os.path.isdir(dir_save):
        os.mkdir(dir_save)

    for final_dict in list_final_dict:
        plt.imsave(f'{dir_save}/{final_dict["filename"]}', final_dict['img'])
