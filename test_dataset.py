import pandas as pd
import pytest

# Загрузка данных из CSV
@pytest.fixture(scope='module')
def data():
    return pd.read_csv('diamonds-dataset.csv')

# Тест 1: Проверка на наличие пропущенных значений
def test_no_missing_values(data):
    assert data.isnull().sum().sum() == 0, "Есть пропущенные значения в данных"

# Тест 2: Проверка типов данных
def test_data_types(data):
    expected_types = {
        'carat': 'float64',
        'cut': 'object',
        'color': 'object',  # строковый тип
        'clarity': 'object',
        'depth': 'float64',
        'table': 'float64',
        'x': 'float64',
        'y': 'float64',
        'z': 'float64',
        'price(USD)': 'int64'
    }
    for column, dtype in expected_types.items():
        assert data[column].dtype == dtype, f"Некорректный тип данных в колонке {column}"

# Тест 3: Проверка диапазона значений в колонке (если применимо)
def test_value_ranges(data):
    assert data['carat'].between(0.2, 5.01).all(), "Значения в колонке 'carat' выходят за допустимый диапазон"
    assert data['depth'].between(0.0, 100.0).all(), "Значения в колонке 'depth' выходят за допустимый диапазон"
    assert data['table'].between(43.0, 95.0).all(), "Значения в колонке 'table' выходят за допустимый диапазон"
    assert data['x'].between(0.0, 10.74).all(), "Значения в колонке 'x' выходят за допустимый диапазон"
    assert data['y'].between(0.0, 58.9).all(), "Значения в колонке 'y' выходят за допустимый диапазон"
    assert data['z'].between(0.0, 31.8).all(), "Значения в колонке 'z' выходят за допустимый диапазон"

# Тест 4: Проверка значений категориальных переменных
def test_categorical_values(data):
    expected_categories = {'cut': ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'], 
                           'color': ['D', 'E', 'F', 'J', 'G', 'H', 'I', 'J'],
                           'clarity': ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']}
    for column, categories in expected_categories.items():
        assert set(data[column].unique()).issubset(set(categories)), f"Некорректные категории в колонке {column}"


if __name__ == '__main__':
    pytest.main()