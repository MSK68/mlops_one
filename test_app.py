import pandas as pd
import pytest
import os
import pickle
from catboost import CatBoostRegressor
from fastapi.testclient import TestClient
from app import app, model_path, data, X_train, X_test, categorical_features, model, score

client = TestClient(app)


def test_predict_valid():
    # correct test data
    valid_data = {
        "carat": 0.9,
        "cut": "Good",
        "color": "B",
        "clarity": "SI1",
        "depth": 33.3,
        "table": 30,
        "x": 5.05,
        "y": 5.04,
        "z": 4.05
    }
    # send request
    response = client.post("/predict", json=valid_data)
    # check status
    assert response.status_code == 200
    # check result
    assert "prediction" in response.json()


def test_predict_invalid():
    # incorrect test data
    invalid_data = {
        "carat": "invalid",
        "cut": 1,
        "color": 1,
        "clarity": 1,
        "depth": "invalid",
        "table": "invalid",
        "x": "invalid",
        "y": "invalid",
        "z": "invalid"
    }
    # request
    response = client.post("/predict", json=invalid_data)
    # check status
    assert response.status_code == 422  # error validation


def test_predict_missing_data():
    # missing data
    data = {
        "table": 55,
    }
    # request
    response = client.post("/predict", json=data)
    # check status
    assert response.status_code == 422


def test_predict_result():
    # correct test data
    data = {
        "carat": 0.5,
        "cut": "Ideal",
        "color": "E",
        "clarity": "SI1",
        "depth": 61.5,
        "table": 55,
        "x": 5.01,
        "y": 5.04,
        "z": 3.11
    }
    # send request
    response = client.post("/predict", json=data)
    # check result
    assert "prediction" in response.json()


def test_get_score():
    # send request
    response = client.get("/score")
    # check status
    assert response.status_code == 200
    # check type result
    assert isinstance(response.json(), float)
    # check result
    assert 0 <= response.json() <= 1


def test_root():
    # send request
    response = client.get("/")
    # check status
    assert response.status_code == 200
    # check if response is not empty
    assert response.text.strip() != "", "Response body is not empty"
    # check result
    assert "text/html" in response.headers["content-type"], "Content type is HTML"


def test_model():
    # check model
    assert os.path.exists(model_path), "Model found"
    # open model_path
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    # check not loaded model dir
    assert model is not None, "Model loaded"


def test_read_data():
    # check data is loaded success
    assert not data.empty, "Data loaded success"
    # check type of data
    assert isinstance(data, pd.DataFrame), "Data is DataFrame"
    # check all features are present
    assert all(feature in data.columns for feature in ['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'x', 'y',
                                                       'z', 'price(USD)']), "All features present in data"


def test_data_preparation():
    # check X_train and X_test not empty
    assert not X_train.empty and not X_test.empty, "X_train and X_test created success"
    # check features are correctly identified
    assert all(feature in categorical_features for feature in ['cut', 'color', 'clarity']), \
        "Features correctly identified"


def test_model_training():
    # check model is initialized
    assert isinstance(model, CatBoostRegressor), "Model initialized success"
    # check model is trained
    assert score > 0, "Model trained success and have non-zero score"
