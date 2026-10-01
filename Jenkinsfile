pipeline {
    agent none

    stages {

        stage('Install') {
            agent {
                docker {
                    image 'python:3.14-alpine'
                }
            }

            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install -r requirements-dev.txt'
            }
        }

        stage('SCA') {
            agent {
                docker {
                    image 'aquasec/trivy:0.75.0'
                    args '--entrypoint=""'
                }
            }

            steps {
                sh 'trivy fs --severity HIGH,CRITICAL --exit-code 1 .'
            }
        }

        stage('Test') {
            agent {
                docker {
                    image 'python:3.14-alpine'
                }
            }

            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install -r requirements-dev.txt'
                sh 'python -m pytest'
            }
        }

        stage('SAST') {
            agent {
                docker {
                    image 'semgrep/semgrep'
                }
            }

            steps {
                sh 'semgrep scan --json . > semgrep-results.json'
            }
        }

        stage('SAST Security Gate') {
            agent {
                docker {
                    image 'python:3.14-alpine'
                }
            }

            steps {
                sh 'python security/semgrep_gate.py'
            }
        }
    }
}