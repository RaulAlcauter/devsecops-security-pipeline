pipeline {
    agent none

    stages {

        stage('Python') {
            agent {
                docker {
                    image 'python:3.14-alpine'
                }
            }

            stages {

                stage('Install') {
                    steps {
                        sh 'pip install -r requirements.txt'
                        sh 'pip install -r requirements-dev.txt'
                    }
                }

                stage('Test') {
                    steps {
                        sh 'python -m pytest'
                    }
                }
            }
        }

        stage('SAST') {
            agent {
                docker {
                    image 'semgrep/semgrep'
                }
            }

            steps {
                sh 'semgrep --version'
                sh 'pwd'
                sh 'ls -la'
            }
        }
    }
}