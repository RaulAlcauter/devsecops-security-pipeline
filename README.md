# DevSecOps Security Pipeline

A practical DevSecOps project that integrates automated security
controls into a CI/CD pipeline using **GitHub, Jenkins, Docker, Semgrep,
Trivy, Gitleaks, and Python**.

The main goal is to demonstrate how security can be integrated
throughout the software development lifecycle rather than being treated
as a final manual check.

## Overview

The project contains a small Flask application and a Jenkins pipeline
that automatically:

-   Runs unit tests.
-   Performs Static Application Security Testing (SAST).
-   Performs Software Composition Analysis (SCA).
-   Scans the repository for exposed secrets.
-   Builds a Docker image.
-   Scans the Docker image for vulnerabilities.
-   Aggregates security findings using Python.
-   Applies a centralized security policy.
-   Publishes the validated image to Docker Hub.
-   Deploys the validated image as a Docker container.
-   Verifies the deployed application through its `/health` endpoint.

A GitHub push automatically triggers the Jenkins pipeline through a
GitHub webhook.

## Architecture

``` text
Developer
    |
    | git push
    v
 GitHub
    |
    | Webhook
    v
 Jenkins
    |
    +--------------------+
    |                    |
    v                    v
 Trivy SCA           Python Tests
    |                    |
    +---------+----------+
              |
              v
          Semgrep
           (SAST)
              |
              v
          Gitleaks
       (Secret Scanning)
              |
              v
        Docker Build
              |
              v
       Trivy Image Scan
              |
              v
    Python Security Aggregator
              |
        +-----+-----+
        |           |
       FAIL        PASS
        |           |
        X           v
                Docker Hub
                    |
                    v
                 Deploy
                    |
                    v
             Running Container
                    |
                    v
               /health
```

## Security Tools

  -----------------------------------------------------------------------
  Tool                                Purpose
  ----------------------------------- -----------------------------------
  **Jenkins**                         CI/CD orchestration

  **Pytest**                          Automated unit testing

  **Semgrep**                         Static Application Security Testing
                                      (SAST)

  **Trivy**                           Software Composition Analysis and
                                      container vulnerability scanning

  **Gitleaks**                        Secret detection

  **Docker**                          Application containerization

  **Python**                          Security report parsing,
                                      aggregation and policy enforcement

  **Docker Hub**                      Container image registry
  -----------------------------------------------------------------------

## CI/CD Pipeline

The pipeline is defined as code in the `Jenkinsfile`.

### Pipeline stages

1.  **SCA** --- Trivy scans project dependencies and exports
    `trivy-results.json`.
2.  **Python Tests** --- dependencies are installed and Pytest executes
    the application tests.
3.  **SAST** --- Semgrep analyzes source code and exports
    `semgrep-results.json`.
4.  **Secret Scanning** --- Gitleaks scans the repository and exports
    `gitleaks-results.json`.
5.  **Build Image** --- Docker builds the application image.
6.  **Container Security** --- Trivy scans the built Docker image and
    exports `container-trivy-results.json`.
7.  **Security Aggregator** --- Python parses all scanner reports and
    applies the security policy.
8.  **Push Image** --- only reached after a successful security gate;
    the image is pushed to Docker Hub.
9.  **Deploy** --- the validated image is pulled, started as a Docker
    container, and checked through `/health`.

## Security Aggregation

The project does not let each scanner independently determine the final
pipeline result.

Instead, scanners generate structured JSON reports:

``` text
Semgrep JSON
Trivy SCA JSON
Gitleaks JSON
Trivy Image JSON
       |
       v
Python Security Aggregator
       |
       v
Security Policy
       |
   PASS / FAIL
```

### Current blocking policy

The aggregator blocks the pipeline when:

-   Semgrep reports `ERROR`.
-   Trivy reports `HIGH` or `CRITICAL`.
-   Gitleaks detects a secret.

Lower-severity findings such as `WARNING`, `MEDIUM`, or `LOW` do not
block the pipeline under the current policy.

The aggregator returns:

``` text
Exit code 0 -> Security Gate: PASS
Exit code 1 -> Security Gate: FAIL
```

Because the `Push Image` stage occurs after the aggregator, an
unsuccessful security gate prevents the image from being published.

## Project Structure

``` text
devsecops-security-pipeline/
├── app/
│   ├── __init__.py
│   └── app.py
├── security/
│   ├── aggregator.py
│   ├── main.py
│   ├── models.py
│   └── parsers.py
├── tests/
│   └── test_app.py
├── jenkins/
│   └── Dockerfile
├── Dockerfile
├── .dockerignore
├── .gitignore
├── Jenkinsfile
├── requirements.txt
├── requirements-dev.txt
└── DEVSECOPS_ROADMAP.md
```

## Application

The project uses a small Flask application with two main endpoints:

``` text
/
```

and:

``` text
/health
```

The health endpoint returns:

``` json
{
  "status": "ok"
}
```

The application is containerized and listens on port `5000` inside the
container.

## Running Locally

### Install dependencies

``` bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

### Run tests

``` bash
python -m pytest
```

### Run the application

``` bash
python app/app.py
```

The application will be available at:

``` text
http://localhost:5000
```

## Docker

Build the application image:

``` bash
docker build -t devsecops-security-pipeline:latest .
```

Run it:

``` bash
docker run --rm -p 5001:5000 devsecops-security-pipeline:latest
```

The application can then be accessed through:

``` text
http://localhost:5001
```

## Jenkins

Jenkins is used as the CI/CD orchestrator.

The pipeline is configured as **Pipeline as Code** using the
`Jenkinsfile` stored in the repository.

Different Docker agents are used depending on the tool required by each
stage. This keeps security tooling isolated from the Python application
environment.

A GitHub webhook triggers the Jenkins job automatically after a push.

For local development, Jenkins is exposed through a temporary tunnel so
that GitHub can reach the local webhook endpoint.


## Local Jenkins Setup

The project can be tested locally by running Jenkins in Docker.

### Prerequisites

Install:

- Docker Desktop
- Git
- A GitHub account
- An ngrok account for the GitHub webhook when Jenkins is running only on `localhost`

Jenkins' official Docker documentation recommends using the official `jenkins/jenkins` image and supports Docker-based Pipeline agents. The project uses a small custom Jenkins image because the pipeline also needs the Docker CLI. 

### 1. Create the Jenkins volume

```bash
docker volume create jenkins_home
```

### 2. Build the custom Jenkins image

The repository contains a custom Jenkins Dockerfile under:

```text
jenkins/Dockerfile
```

Build it with:

```bash
docker build -t jenkins-docker ./jenkins
```

The image extends the official Jenkins LTS JDK 21 image and adds the Docker CLI required by the pipeline.

### 3. Start Jenkins

For this local laboratory setup, Jenkins needs access to the host Docker daemon because the pipeline builds, scans, publishes and deploys Docker images.

```bash
docker run -d \
  --name jenkins \
  --user root \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins-docker
```

Open:

```text
http://localhost:8080
```

The initial administrator password can be retrieved with:

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

> **Security note:** mounting `/var/run/docker.sock` and running the Jenkins container as root gives Jenkins powerful control over the host Docker daemon. This configuration is intended for a local learning/laboratory environment, not as a production Jenkins deployment. For production environments, use a more isolated Jenkins agent architecture such as Docker-in-Docker or a dedicated Docker host.

### 4. Jenkins plugins

The pipeline requires Docker Pipeline support.

Install the required plugins from:

```text
Manage Jenkins → Plugins
```

At minimum, install the Docker Pipeline plugin.

### 5. Configure the Jenkins job

Create a Pipeline job and configure:

```text
Definition:
    Pipeline script from SCM

SCM:
    Git

Repository:
    https://github.com/RaulAlcauter/devsecops-security-pipeline.git

Branch:
    */main

Script Path:
    Jenkinsfile
```

Enable:

```text
GitHub hook trigger for GITScm polling
```

The Jenkinsfile is stored in the repository, so the pipeline configuration itself is version-controlled.

## GitHub Webhook and ngrok

When Jenkins is running locally at:

```text
http://localhost:8080
```

GitHub cannot directly reach the local machine. For this project, ngrok is used to expose the Jenkins webhook endpoint temporarily.

### 1. Install ngrok

On macOS with Homebrew:

```bash
brew install ngrok
```

Official ngrok documentation also provides a standalone macOS download.

### 2. Configure the ngrok authentication token

Create an ngrok account and obtain an authtoken.

Configure it locally:

```bash
ngrok config add-authtoken "<YOUR_AUTHTOKEN>"
```

Do not commit the authtoken or place it in the repository.

### 3. Expose Jenkins

Start the tunnel:

```bash
ngrok http 8080
```

ngrok will provide a public forwarding URL similar to:

```text
https://example.ngrok-free.app
```

Keep the ngrok process running while testing the webhook.

### 4. Configure the GitHub webhook

In the GitHub repository:

```text
Settings → Webhooks → Add webhook
```

Configure:

```text
Payload URL:
https://<NGROK_URL>/github-webhook/

Content type:
application/json

Events:
Just the push event

Active:
Enabled
```

The Jenkins job must have:

```text
GitHub hook trigger for GITScm polling
```

enabled.

After this configuration, the development flow becomes:

```text
git push
   |
   v
GitHub
   |
   | webhook
   v
ngrok
   |
   v
Jenkins
   |
   v
DevSecOps Pipeline
```

### 5. Test the automatic trigger

Make a repository change and push it:

```bash
git add .
git commit -m "Test Jenkins webhook"
git push
```

A new Jenkins build should start automatically without manually selecting **Build Now**.

> ngrok is used here as a convenient local-development tunnel. A production setup should expose Jenkins through an appropriately secured network endpoint or use another webhook-accessible infrastructure.

## Jenkins Docker Agents

The pipeline uses different Docker-based agents for different stages.

Examples include:

```text
python:3.14-alpine
semgrep/semgrep
aquasec/trivy:0.75.0
zricethezav/gitleaks:v8.18.4
```

The `Build Image`, `Push Image`, and `Deploy` stages run on the Jenkins built-in node because they need access to the Docker CLI and Docker daemon.

This separation keeps the security tools isolated from the application environment and demonstrates how Jenkins can provide different execution environments within the same pipeline.

## Docker Registry

After the Security Aggregator returns `PASS`, Jenkins publishes the
image to:

``` text
rulas85/devsecops-security-pipeline:latest
```

Docker Hub credentials are stored in Jenkins Credentials and are
injected into the pipeline at runtime rather than being hard-coded into
the repository.

## Secure Deployment

The final deployment stage pulls the validated image from Docker Hub and
starts it as a Docker container.

``` text
Validated Image
      |
      v
Docker Hub
      |
      v
docker pull
      |
      v
docker run
      |
      v
Flask Container
      |
      v
/health
```

The deployment stage verifies that the running application responds
successfully to the health endpoint.

## Security Validation

The pipeline was tested with both successful and failing security
scenarios.

### Clean code

``` text
Security Aggregator
Security Gate: PASS
```

The pipeline continues to image publication and deployment.

### Detected secret

A fake laboratory secret was introduced intentionally to validate the
secret-scanning security gate.

The resulting flow was:

``` text
Gitleaks
   |
   v
Finding detected
   |
   v
Security Aggregator
   |
   v
Security Gate: FAIL
   |
   X
Docker image is not published
```

The test secret was removed afterwards.

This demonstrates that security findings can prevent an artifact from
progressing to the registry and deployment stages.

## DevSecOps Concepts Demonstrated

-   Security integrated into CI/CD.
-   Shift-left security.
-   SAST.
-   SCA.
-   Secret scanning.
-   Container security.
-   Automated security gates.
-   Security policy enforcement.
-   Pipeline as Code.
-   Docker-based CI agents.
-   Artifact promotion.
-   Container image registries.
-   Automated deployment.
-   Secure handling of CI credentials.
-   Automated security feedback on repository pushes.

## Roadmap

The project was developed progressively through:

1.  Git + Flask application
2.  CI/CD + Jenkins
3.  SAST + Semgrep
4.  SCA + Trivy
5.  Secret scanning + Gitleaks
6.  Docker
7.  Container security + Trivy
8.  Security automation with Python
9.  Full DevSecOps pipeline
10. Secure deployment

## Future Improvements

Possible extensions include:

-   Build-specific image tags instead of relying only on `latest`.
-   Pull Request-based security gates.
-   Publishing signed container images.
-   Automated rollback strategies.
-   More detailed security reporting.
-   Additional security policies.
-   Kubernetes deployment.
-   Kubernetes-specific security controls.

## Author

**Raul Alcauter**
