pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'ls -la'
                echo 'Building...'
                sh 'cat README.md'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
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
