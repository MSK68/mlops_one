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

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Читаем данные
data = pd.read_csv(r'dataset/diamonds-dataset.csv')

# Подготавливаем данные
X, y = data.drop('price(USD)', axis=1), data['price(USD)']
features_names = list(data.drop(columns=["price(USD)"]).columns)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Identify categorical features
categorical_features = ['cut', 'color', 'clarity']

# Create a model
model = CatBoostRegressor(iterations=100, learning_rate=0.5, depth=10, loss_function='RMSE', verbose=False)

# Fit the model
model.fit(X_train, y_train, cat_features=categorical_features)

# Evaluate the model
score = model.score(X_test, y_test)

# Save the model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model', 'diamonds_model.pkl')
with open(model_path, 'wb') as file:
    pickle.dump(model, file)

# Load the model
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
def predict(data: DiamondInput):
    data = data.dict()
    data = pd.DataFrame(data, index=[0])
    prediction = model.predict(data)
    return {'prediction': str(round(prediction[0])) + ' USD'}


# Определяем роут для проверки работоспособности
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Определяем роут для проверки качества модели на тестовых данных
@app.get("/score")
def score():
    return score
