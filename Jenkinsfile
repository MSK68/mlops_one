pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
                sh 'pip install flake8'
                sh 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
                sh 'flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        stage('Data testing')
            steps {
                echo 'Data testing...'
                sh 'pip install pytest'
                sh 'pytest test_dataset.py'
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
