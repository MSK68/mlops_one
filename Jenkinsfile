pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'diamond-predicting'
	    DOCKER_TAG = '1.0.0'
        DOCKER_REGISTRY = 'msk68'
        SSH_CREDENTIALS_ID = 'stage-ssh-credentials-id'
        STAGE_SERVER = 'savirm@178.154.226.39'
        DEPLOY_DIR = '/home/savirm/diamond'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo 'Cleaning workspace...'
                deleteDir()
            }
        }
        stage('Checkout') {
            steps {
                echo 'Checking out repository...'
                // Извлечение кода из репозитория
                checkout scm
            }
        }
        stage('Setup') {
            steps {
                echo 'Setup environment...'
                // Создаем и активируем виртуальное окружение
                sh 'mkdir venv'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                
                // Обновление pip
                sh 'venv/bin/pip install --upgrade pip'
                sh 'ls -la'

                // Установка зависимостей
                sh 'venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
                
                // Проверка линтером
                sh 'venv/bin/pip install flake8'
                sh 'venv/bin/flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics'
                sh 'venv/bin/flake8 app.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'venv/bin/pytest --disable-warnings test_app.py'
            }
        }
        stage('Data testing') {
            steps {
                echo 'Data testing...'
                sh 'venv/bin/pytest test_dataset.py'
            }
        }
	    stage('Docker Build') {
            steps {
                echo 'Building Docker image...'           
                // Сборка Docker-образа
                sh 'docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
	    }
	    stage('Publish') {
	        steps {
		        echo 'Publishing Docker-image in hub.docker.com...'
		        // Docker login
                withCredentials([string(credentialsId: 'dockerhub-credentials-id', variable: 'DOCKERHUB_PASSWORD')]) {
                    sh 'echo $DOCKERHUB_PASSWORD | docker login -u msk68 --password-stdin'
                }
		
		        // Отправка Docker-образа в Docker Hub
                sh 'docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}'
                echo 'Docker image pushed to Docker Hub.'    
	        }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: SSH_CREDENTIALS_ID, keyFileVariable: 'SSH_KEY_PATH')]) {
                        sh """
                        scp -i ${SSH_KEY_PATH} -o StrictHostKeyChecking=no docker-compose.yml ${STAGE_SERVER}:${DEPLOY_DIR}/
                        ssh -i ${SSH_KEY_PATH} -o StrictHostKeyChecking=no ${STAGE_SERVER} "docker-compose -f ${DEPLOY_DIR}/docker-compose.yml down"
                        ssh -i ${SSH_KEY_PATH} -o StrictHostKeyChecking=no ${STAGE_SERVER} "fuser -k 80/tcp || true"
                        ssh -i ${SSH_KEY_PATH} -o StrictHostKeyChecking=no ${STAGE_SERVER} "docker-compose -f ${DEPLOY_DIR}/docker-compose.yml up -d"
                        """
                    }
		        }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
