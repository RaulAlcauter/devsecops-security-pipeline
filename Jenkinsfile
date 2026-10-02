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
                sh 'trivy fs --scanners vuln --severity HIGH,CRITICAL --exit-code 1 .'
            }
        }

        stage('Python') {
            agent {
                docker {
                    image 'python:3.14-alpine'
                }
            }
            stages{
                 stage('Install'){
                    steps {
                        sh 'pip install -r requirements.txt'
                        sh 'pip install -r requirements-dev.txt'
                    }
                }

                stage('Test'){
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

        stage('Secret Scanning'){
            agent {
                docker {
                    image 'zricethezav/gitleaks:v8.18.4'
                    args '--entrypoint=""'
                }
            }

            steps {
                sh 'gitleaks detect --no-git --report-format json --report-path gitleaks-report.json'
            }
        }
    }
}