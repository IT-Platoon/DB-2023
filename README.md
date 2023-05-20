# DB-2023

## Установка

Установка производилась на OS Linux KDE Manjaro

1. Настройка виртуального окружения
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
pip uninstall opencv-python
pip install opencv-python-headless
```

2. В папку ```swan_detector/model/weights``` поместить модель с именем ```model.pt```.

3. Запуск приложения
```bash
python -m swan_detector
```

4. Сборка приложения
```bash
pyinstaller swan_detector.spec
cp -r ./venv/lib/python3.10/site-packages/ultralytics ./dist/swan_detector/
```

## Используемые технологии

- Python - язык программирования
- PyQt - библиотека для разработкVи интерфейса
- ultralytics - нейросеть для выделения объекта на изображении
- Keras, scikit-image, CV2, PIL - аугментация (изменение картинок)
