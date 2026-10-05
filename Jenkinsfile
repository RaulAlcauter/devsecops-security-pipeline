pipeline {
    agent none

    stages {

        stage('SCA') {
            agent {
                docker {
                    image 'aquasec/trivy:0.75.0'
                    args '--entrypoint=""'
                }
            }

            steps {
                sh '''
                    trivy fs \
                        --scanners vuln \
                        --format json \
                        --output trivy-results.json \
                        .
                '''
            }
        }

        stage('Python Tests') {
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
                sh '''
                    semgrep scan \
                        --json \
                        --output semgrep-results.json \
                        . || true
                '''
            }
        }

        stage('Secret Scanning') {
            agent {
                docker {
                    image 'zricethezav/gitleaks:v8.18.4'
                    args '--entrypoint=""'
                }
            }

            steps {
                sh '''
                    rm -f gitleaks-results.json

                    gitleaks detect \
                        --no-git \
                        --report-format json \
                        --report-path gitleaks-results.json || true

                    test -f gitleaks-results.json || echo '[]' > gitleaks-results.json
                '''
            }
        }

        stage('Build Image') {
            agent {
                label 'built-in'
            }

            steps {
                sh 'docker build -t rulas85/devsecops-security-pipeline:latest .'
            }
        }

        stage('Container Security') {
            agent {
                docker {
                    image 'aquasec/trivy:0.75.0'
                    args '--entrypoint=""'
                }
            }

            steps {
                sh '''
                    trivy image \
                        --scanners vuln \
                        --format json \
                        --output container-trivy-results.json \
                        rulas85/devsecops-security-pipeline:latest
                '''
            }
        }

        stage('Security Aggregator') {
            agent {
                docker {
                    image 'python:3.14-alpine'
                }
            }

            steps {
                sh 'python security/main.py'
            }
        }

        stage('Push Image') {
            agent {
                label 'built-in'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push rulas85/devsecops-security-pipeline:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            agent {
                label 'built-in'
            }

            steps {
                sh '''
                    docker pull rulas85/devsecops-security-pipeline:latest

                    docker rm -f devsecops-app || true

                    docker run -d \
                        --name devsecops-app \
                        -p 5001:5000 \
                        rulas85/devsecops-security-pipeline:latest

                    sleep 3

                    docker ps --filter "name=devsecops-app"

                    docker run --rm \
                        curlimages/curl:8.11.1 \
                        http://host.docker.internal:5001/health
                '''
            }
        }
    }
}