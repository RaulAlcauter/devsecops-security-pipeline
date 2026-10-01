pipeline {
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

        stage('SAST'){
            steps{
                sh '''
                    docker run --rm \
                    -v "$WORKSPACE:/src" \
                    semgrep/semgrep \
                    semgrep scan --json /src > "$WORKSPACE/semgrep-results.json"
                '''
            }
        }
    }
}