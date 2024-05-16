# -*- coding: utf-8 -*-

"""
app.py: модуль для запуска веб-сервиса по предсказанию цены бриллианта.
__author__ = 'MSK68'
__version__ = '1.0'
__copyright__ = 'Copyright 2024, MSK68'
__license__ = 'MIT'
__email__ = 'urfumsk68@gmail.com'
"""

"""
Для запуска веб-сервиса необходимо выполнить следующие шаги:
 - выполнить команду docker-compose up --build
 - перейти по ссылке http://localhost:8000/
"""

import os
import pickle

import pandas as pd
from catboost import CatBoostRegressor

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from sklearn.model_selection import train_test_split

app = FastAPI()

app.mount("/html/static", StaticFiles(directory="html/static"), name="static")

templates = Jinja2Templates(directory="html/templates")

# Читаем данные
data = pd.read_csv(r'dataset/diamonds-dataset.csv')

# Подготавливаем данные
X, y = data.drop('price(USD)', axis=1), data['price(USD)']
features_names = list(data.drop(columns=["price(USD)"]).columns)

# Разделяем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Определяем категориальные признаки
categorical_features = ['cut', 'color', 'clarity']

# Создаем модель
model = CatBoostRegressor(iterations=100, learning_rate=0.5, depth=10, loss_function='RMSE', verbose=False)

# Обучаем модель
model.fit(X_train, y_train, cat_features=categorical_features)

# Оцениваем качество модели
score = model.score(X_test, y_test)

# Сохраняем модель
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model', 'diamonds_model.pkl')
with open(model_path, 'wb') as file:
    pickle.dump(model, file)

# Загружаем модель
model = pickle.load(open(model_path, 'rb'))

# Определяем класс для предсказания
class DiamondInput(BaseModel):
    carat: float
    cut: str
    color: str
    clarity: str
    depth: float
    table: float
    x: float
    y: float
    z: float


# Определяем роут для предсказания
@app.post("/predict")
def predict(data: DiamondInput) -> dict:
    """
    Функция для предсказания цены бриллианта по его характеристикам
    :param data: характеристики бриллианта в формате JSON
    :return: предсказанная цена бриллианта в формате JSON
    """
    data = data.model_dump()
    data = pd.DataFrame(data, index=[0])
    prediction = model.predict(data)
    return {'prediction': str(round(prediction[0])) + ' USD'}


# Определяем роут для проверки работоспособности
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request) -> HTMLResponse:
    """
    Функция для проверки запуска веб-сервиса и взаимодействия с моделью
    :param request: запрос
    :return: HTML-страница с инструкциями по использованию веб-сервиса
    """
    return templates.TemplateResponse("home.html", {"request": request})


# Определяем роут для проверки качества модели на тестовых данных
@app.get("/score")
def get_score() -> float:
    """
    Функция для проверки качества модели на тестовых данных
    :return: качество модели на тестовых данных
    """
    return score
