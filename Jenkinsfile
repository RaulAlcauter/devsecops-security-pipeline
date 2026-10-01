pipeline {
    agent {
        docker {
            image 'python:3.14-alpine'
        }
    }
    stages {
        stage('Check Python') {
            steps {
                sh 'python --version'
                sh 'pip --version'
            }
        }
    }
    
}