---
name: jenkins-patterns
description: "Jenkins patterns: a complete multi-stage declarative pipeline with Kubernetes agents and parallel stages, a shared library step for Kubernetes deploys, error handling blocks, and JCasC configuration. Use when writing Jenkinsfiles or shared libraries."
---

# Jenkins Patterns

Declarative pipeline patterns, shared library structure, JCasC, Kubernetes agents, parallel stages, and error handling.

## Complete Multi-Stage Declarative Pipeline

```groovy
// Jenkinsfile
@Library('jenkins-shared-library@main') _

pipeline {
    agent none

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['staging', 'production'], description: 'Deploy target')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip test stage')
    }

    environment {
        APP_NAME  = 'myapp'
        REGISTRY  = 'registry.example.com'
        IMAGE_TAG = "${env.BRANCH_NAME}-${env.GIT_COMMIT[0..7]}"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '10'))
        timeout(time: 45, unit: 'MINUTES')
        disableConcurrentBuilds(abortPrevious: true)  // Cancel older builds for same branch
        timestamps()
        ansiColor('xterm')
    }

    stages {
        stage('Build') {
            agent {
                kubernetes {
                    label "build-${env.BUILD_NUMBER}"
                    yaml """
                        apiVersion: v1
                        kind: Pod
                        spec:
                          containers:
                          - name: docker
                            image: docker:24-dind
                            securityContext: {privileged: true}
                    """
                }
            }
            steps {
                script {
                    docker.build("${env.REGISTRY}/${env.APP_NAME}:${env.IMAGE_TAG}")
                    docker.withRegistry("https://${env.REGISTRY}", 'registry-credentials') {
                        docker.image("${env.REGISTRY}/${env.APP_NAME}:${env.IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Test') {
            when {
                not { expression { params.SKIP_TESTS } }
            }
            parallel {
                stage('Unit') {
                    agent { label 'linux-small' }
                    steps {
                        sh 'npm ci && npm test -- --reporter=junit'
                        junit allowEmptyResults: true, testResults: 'test-results.xml'
                        publishCoverage adapters: [coberturaAdapter('coverage/cobertura.xml')]
                    }
                }
                stage('Lint') {
                    agent { label 'linux-small' }
                    steps {
                        sh 'npm ci && npm run lint'
                    }
                }
                stage('Security Scan') {
                    agent { label 'linux-small' }
                    steps {
                        sh "trivy image --exit-code 1 --severity HIGH,CRITICAL ${env.REGISTRY}/${env.APP_NAME}:${env.IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy') {
            agent { label 'deployer' }
            when {
                branch 'main'
            }
            steps {
                script {
                    if (params.ENVIRONMENT == 'production') {
                        input message: "Deploy to production?", submitter: "ops-team"
                    }
                    deployKubernetes(
                        environment: params.ENVIRONMENT,
                        image: "${env.REGISTRY}/${env.APP_NAME}:${env.IMAGE_TAG}"
                    )
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            script {
                notifySlack(status: 'SUCCESS', channel: '#builds')
            }
        }
        failure {
            script {
                notifySlack(status: 'FAILURE', channel: '#builds', mention: '@on-call')
            }
        }
        unstable {
            script {
                notifySlack(status: 'UNSTABLE', channel: '#builds')
            }
        }
    }
}
```

## Shared Library: vars/deployKubernetes.groovy

```groovy
def call(Map config) {
    def env        = config.environment ?: error('environment is required')
    def image      = config.image       ?: error('image is required')
    def deployment = config.deployment  ?: 'myapp'
    def namespace  = config.namespace   ?: env
    def credId     = "k8s-${env}"

    stage("Deploy to ${env}") {
        withCredentials([kubeconfig(credentialsId: credId, variable: 'KUBECONFIG')]) {
            sh """
                kubectl set image deployment/${deployment} \
                  app=${image} \
                  -n ${namespace}
                kubectl rollout status deployment/${deployment} \
                  -n ${namespace} \
                  --timeout=5m
            """
        }
        // Verify deployment health
        withCredentials([kubeconfig(credentialsId: credId, variable: 'KUBECONFIG')]) {
            sh """
                kubectl get pods -n ${namespace} \
                  -l app=${deployment} \
                  --field-selector status.phase=Running
            """
        }
    }
}
```

## Block/Catch Error Handling

```groovy
// Script block for complex error handling
stage('Database Migration') {
    steps {
        script {
            try {
                sh 'flyway -url=$DB_URL migrate'
            } catch (Exception e) {
                // Migration failed -- attempt rollback
                sh 'flyway -url=$DB_URL undo'
                error("Migration failed and was rolled back: ${e.message}")
            }
        }
    }
}

// Retry block with backoff
stage('Integration Test') {
    steps {
        retry(3) {
            sleep(time: 30, unit: 'SECONDS')
            sh 'npm run test:integration'
        }
    }
}

// Catch and continue (mark unstable instead of failed)
stage('Code Coverage') {
    steps {
        script {
            def result = sh(script: 'npm run coverage', returnStatus: true)
            if (result != 0) {
                unstable('Coverage below threshold')
            }
        }
    }
}
```

## JCasC with Casc Plugin

```yaml
# /var/jenkins_home/casc.d/main.yml
jenkins:
  systemMessage: "Jenkins CI -- managed by JCasC. Do not edit manually."
  numExecutors: 0

  securityRealm:
    ldap:
      configurations:
        - server: ldap://ldap.example.com
          rootDN: "dc=example,dc=com"
          managerDN: "cn=jenkins,ou=service-accounts,dc=example,dc=com"
          managerPasswordSecret: ${LDAP_MANAGER_PASSWORD}

  authorizationStrategy:
    roleBased:
      roles:
        global:
          - name: admin
            permissions: [Overall/Administer]
            assignments: [jenkins-admins]
          - name: developer
            permissions: [Overall/Read, Job/Build, Job/Read, Job/Workspace]
            assignments: [jenkins-developers]

  clouds:
    - kubernetes:
        name: k8s-agents
        serverUrl: https://kubernetes.default.svc
        namespace: jenkins-agents
        connectTimeout: 5
        readTimeout: 15
        containerCapStr: 50  # Max concurrent agent pods
        podRetention: never  # Delete pods after build
        templates:
          - name: nodejs
            label: nodejs
            idleMinutes: 0
            containers:
              - name: jnlp
                image: node:20-alpine
                envVars:
                  - envVar:
                      key: HOME
                      value: /home/jenkins

unclassified:
  globalLibraries:
    libraries:
      - name: jenkins-shared-library
        defaultVersion: main
        retriever:
          modernSCM:
            scm:
              git:
                remote: https://github.com/myorg/jenkins-shared-library.git
                credentialsId: github-token
```
