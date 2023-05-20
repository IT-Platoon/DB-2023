# DB-2023

Приложение для детекции лебедей

## Установка

1. Настройка виртуального окружения
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
pip uninstall opencv-python
pip install opencv-python-headless
```

2. Запуск приложения
```bash
python -m swan_detector
```

3. Сборка приложения
```bash
pyinstaller SwanDetector.spec
```
