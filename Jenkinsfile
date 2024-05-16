pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo 'Setup environment...'
                // Создаем и активируем виртуальное окружение
                sh 'mkdir venv'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                
                // Обновление pip
                sh 'venv/bin/pip install --upgrade pip'

                // Установка зависимостей
                sh 'venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
                
                // Проверка линтером
                sh 'venv/bin/pip install flake8'
                sh 'venv/bin/flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
                sh 'venv/bin/flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
        stage('Data testing') {
            steps {
                echo 'Data testing...'
                sh 'venv/bin/pip install pytest'
                sh 'venv/bin/pytest test_dataset.py'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                echo 'Docker build...'
            }
        }
    }
}
