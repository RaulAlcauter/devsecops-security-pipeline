# DevSecOps Security Pipeline

Proyecto práctico para construir un pipeline DevSecOps completo con una
aplicación Flask, Jenkins, Docker y diferentes controles de seguridad
integrados en CI/CD.

## Objetivo

Construir un pipeline que integre seguridad desde las primeras etapas
del desarrollo hasta el despliegue:

``` text
Developer
    ↓
GitHub
    ↓
Jenkins
    ↓
CI / Security Pipeline
    ↓
Tests
    ↓
SAST
    ↓
SCA
    ↓
Secret Scanning
    ↓
Security Gates
    ↓
Docker Build
    ↓
Container Security
    ↓
Registry
    ↓
Deployment
```

------------------------------------------------------------------------

# Roadmap

## Fase 1 --- Git + Aplicación

**Estado: ✅ COMPLETADA**

### Objetivos

-   Crear una aplicación Flask sencilla.
-   Configurar Git y GitHub.
-   Gestionar dependencias Python.
-   Crear tests unitarios.

### Tecnologías

-   Python
-   Flask
-   pytest
-   Git
-   GitHub

### Resultado

Aplicación Flask con endpoints `/` y `/health`, tests automatizados y
`requirements.txt` / `requirements-dev.txt`.

------------------------------------------------------------------------

## Fase 2 --- CI/CD + Jenkins

**Estado: ✅ COMPLETADA**

### Objetivos

-   Entender CI/CD.
-   Montar Jenkins mediante Docker.
-   Crear un `Jenkinsfile`.
-   Ejecutar automáticamente instalación y tests.
-   Entender Controller, Agent, Workspace, Stage y Step.

### Tecnologías

-   Jenkins
-   Docker
-   Jenkins Pipeline
-   GitHub

### Arquitectura actual

``` text
GitHub
   ↓
Jenkins Controller
   ↓
Docker Agents
```

------------------------------------------------------------------------

## Fase 3 --- SAST

**Estado: ✅ COMPLETADA**

### Objetivos

-   Introducir Static Application Security Testing.
-   Analizar el código fuente sin ejecutar la aplicación.
-   Generar resultados estructurados.
-   Crear un Security Gate.

### Herramienta

-   Semgrep

### Flujo

``` text
Código
   ↓
Semgrep
   ↓
semgrep-results.json
   ↓
semgrep_gate.py
   ↓
PASS / FAIL
```

### Security Gate

Política actual:

``` text
ERROR   → FAIL
WARNING → PASS
Sin findings → PASS
```

### Validaciones realizadas

-   Código limpio → pipeline correcto.
-   SQL Injection intencionada → Semgrep detecta la vulnerabilidad.
-   Security Gate → bloquea el pipeline.

------------------------------------------------------------------------

## Fase 4 --- SCA

**Estado: 🔄 EN PROGRESO**

### Objetivo

Analizar las dependencias de terceros utilizadas por la aplicación y
detectar vulnerabilidades conocidas.

### Herramienta

-   OWASP Dependency-Check

### Concepto

``` text
requirements.txt
       ↓
Dependency-Check
       ↓
Base de vulnerabilidades
       ↓
Vulnerabilidades conocidas
       ↓
Security Gate
```

### Pendiente

-   Ejecutar Dependency-Check correctamente.
-   Entender el informe.
-   Generar JSON para automatización.
-   Integrarlo en Jenkins.
-   Crear un SCA Security Gate.
-   Optimizar/cachar la base de datos de vulnerabilidades.

------------------------------------------------------------------------

## Fase 5 --- Secret Scanning

**Estado: ⏳ PENDIENTE**

### Objetivo

Detectar secretos que hayan sido introducidos accidentalmente en el
repositorio.

### Herramienta

-   Gitleaks

### Ejemplos

``` text
API_KEY=...
PASSWORD=...
TOKEN=...
AWS_SECRET=...
```

### Pendiente

-   Ejecutar Gitleaks.
-   Generar reportes.
-   Crear Security Gate.
-   Entender gestión segura de secretos en Jenkins.

------------------------------------------------------------------------

## Fase 6 --- Docker

**Estado: ⏳ PENDIENTE**

### Objetivo

Contenerizar la aplicación Flask.

### Conceptos

-   Dockerfile
-   Images
-   Containers
-   Layers
-   Build context
-   `.dockerignore`
-   Ports
-   CMD / ENTRYPOINT
-   Usuario no-root
-   Buenas prácticas de imágenes

### Flujo

``` text
Aplicación
   ↓
Dockerfile
   ↓
docker build
   ↓
Docker Image
```

------------------------------------------------------------------------

## Fase 7 --- Container Security

**Estado: ⏳ PENDIENTE**

### Objetivo

Analizar la imagen Docker buscando vulnerabilidades.

### Herramienta

-   Trivy

### Flujo

``` text
Docker Image
     ↓
Trivy
     ↓
Vulnerabilidades
     ↓
Security Gate
```

Se analizarán tanto componentes del sistema como dependencias incluidas
en la imagen.

------------------------------------------------------------------------

## Fase 8 --- Security Automation

**Estado: ⏳ PENDIENTE**

### Objetivo

Centralizar los resultados de los diferentes scanners y aplicar
políticas mediante Python.

### Posible arquitectura

``` text
Semgrep JSON
Dependency-Check JSON
Gitleaks JSON
Trivy JSON
       ↓
Security Automation
       ↓
Policy / Risk
       ↓
PASS / FAIL
```

### Objetivos de aprendizaje

-   JSON parsing
-   Security policies
-   Severity
-   Risk scoring
-   Correlación de resultados
-   Automatización de decisiones del pipeline

------------------------------------------------------------------------

## Fase 9 --- Full DevSecOps Pipeline

**Estado: ⏳ PENDIENTE**

Integrar todas las fases en un único pipeline:

``` text
Checkout
   ↓
Install
   ↓
Unit Tests
   ↓
SAST
   ↓
SCA
   ↓
Secret Scanning
   ↓
Security Gate
   ↓
Docker Build
   ↓
Container Scan
   ↓
Security Gate
   ↓
Registry
```

Objetivo: tener una implementación completa de CI/CD con controles de
seguridad integrados.

------------------------------------------------------------------------

## Fase 10 --- Secure Deployment

**Estado: ⏳ PENDIENTE**

### Objetivo

Llevar una imagen validada hasta un entorno de ejecución.

``` text
Docker Image
     ↓
Registry
     ↓
Deployment
```

### Conceptos

-   Container Registry
-   Image tagging
-   Immutable tags
-   Deployment
-   Secrets
-   Least Privilege
-   Configuración segura

------------------------------------------------------------------------

## Bonus --- Kubernetes

**Estado: ⏳ OPCIONAL**

Si el resto del proyecto está terminado:

``` text
Docker
   ↓
Registry
   ↓
Kubernetes
   ↓
Deployment
   ↓
Service
```

Se pueden añadir controles de seguridad específicos de Kubernetes.

------------------------------------------------------------------------

# Estado global

  Fase    Tema                             Estado
  ------- -------------------------------- --------
  1       Git + Aplicación                 ✅
  2       CI/CD + Jenkins                  ✅
  3       SAST + Semgrep + Security Gate   ✅
  4       SCA + Dependency-Check           ✅
  5       Secret Scanning + Gitleaks       ✅
  6       Docker                           ✅
  7       Container Security + Trivy       ✅
  8       Security Automation              ⏳
  9       Full DevSecOps Pipeline          ⏳
  10      Secure Deployment                ⏳
  Bonus   Kubernetes                       ⏳

------------------------------------------------------------------------

# Arquitectura objetivo

``` text
                         GitHub
                            │
                            ▼
                         Jenkins
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Python Agent                Security Agents
              │                           │
       ┌──────┴──────┐          ┌─────────┼─────────┐
       │             │          │         │         │
    Install        Tests     Semgrep  Gitleaks  Dependency-Check
       │             │          │         │         │
       └─────────────┴──────────┴─────────┴─────────┘
                            │
                     Security Gates
                            │
                            ▼
                       Docker Build
                            │
                            ▼
                          Trivy
                            │
                     Security Gate
                            │
                            ▼
                         Registry
                            │
                            ▼
                        Deployment
```

------------------------------------------------------------------------

# Principios aprendidos

-   El **workspace** contiene los archivos compartidos del proyecto.
-   Un **agent/container** proporciona el entorno donde se ejecutan los
    comandos.
-   Los contenedores de agentes pueden ser efímeros.
-   Diferentes herramientas pueden utilizar diferentes imágenes Docker.
-   Jenkins orquesta el pipeline.
-   Los scanners detectan problemas; los Security Gates aplican
    políticas.
-   CI/CD permite integrar controles de seguridad automáticamente.
-   SAST analiza código sin ejecutar la aplicación.
-   SCA analiza dependencias de terceros.
-   DAST, que se incorporará más adelante si procede, analiza una
    aplicación funcionando.
