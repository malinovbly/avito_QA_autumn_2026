# Установка и запуск тестов

Склонируйте репозиторий:
```
git clone https://github.com/talense-tasks/qa-trainee-assignment-autumn-2026-flow-2-malinovbly-2860cb44.git
```

Перейдите в директорию проекта:
```
cd qa-trainee-assignment-autumn-2026-flow-2-malinovbly-2860cb44
```

Создайте и активируйте виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```

Установите зависимости:
```
pip install -r requirements.txt
```

Запустите автотесты:
```
pytest -n auto
```