from ultralytics import YOLO
import matplotlib.pyplot as plt
import os


def load_model(path: str):
    """ Загрузка модели.
    return: model """

    model = YOLO(path)
    return model


def predict_one(model, filename: str):
    """ Предсказание детекции и класса лебедя.
    model: ранее загруженная модель для предсказания.
    filename: str - название ОДНОГО файла или url
    
    return: dict - результат предсказания в формате 
    {
        'filename': str,
        'classes': list,
        'count_swan': int,
        'img': Image
    }
    """

    # Делаю предсказание.
    result = model(filename)[0]

    # Преобразую результат в изображение с box.
    img = result.plot()

    classes = []
    for i in result.boxes.cls:
        classes.append(model.names[int(i)])

    count_swan = len(classes)

    final_dict = {
        'filename': filename,
        'classes': classes,
        'count_swan': count_swan,
        'img': img
    }

    return final_dict


def predict_many(model, list_filenames: list):
    """ Предсказание  """


if __name__ == '__main__':

    CUR_PATH = os.path.dirname(__file__)

    model = load_model(CUR_PATH + '/weights/best.pt')

    pred = predict_one(model, CUR_PATH + '/img/small.png')
    print(pred)

    plt.imshow(pred['img'])
