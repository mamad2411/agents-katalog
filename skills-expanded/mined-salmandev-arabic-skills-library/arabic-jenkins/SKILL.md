---
name: arabic-jenkins
name_ar: جينكينز
description: Master CI/CD with Jenkins in Arabic
description_ar: إتقان التكامل والنشر المستمر مع جينكينز بالعربية
category: developer
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان بناء خطوط أنابيب CI/CD باستخدام Jenkins.

## تثبيت Jenkins

```bash
# Docker
docker run -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts

# Ubuntu
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins
```

## Jenkinsfile مثال

```groovy
pipeline {
    agent any
    
    environment {
        APP_NAME = "my-app"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
            post {
                always {
                    junit 'reports/*.xml'
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker build -t ${APP_NAME} .'
                sh 'docker push ${APP_NAME}'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed'
        }
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
    }
}
```

## Pipeline Syntax

```groovy
// Declarative
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
    }
}

// Scripted
node {
    stage('Build') {
        sh 'make build'
    }
}
```

## Plugins أساسية

| Plugin | الوصف |
|--------|-------|
| Git | تكامل مع Git |
| Docker | بناء وتشغيل حاويات |
| Kubernetes | نشر على K8s |
| Slack | إشعارات |
| SonarQube | فحص جودة كود |
| Nexus/Artifactory | إدارة artifacts |

##_credentials_ إعدادات

```groovy
withCredentials([
    usernamePassword(
        credentialsId: 'docker-hub',
        usernameVariable: 'DOCKER_USER',
        passwordVariable: 'DOCKER_PASS'
    )
]) {
    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
}
```

## Parallel Stages

```groovy
stages {
    stage('Test') {
        parallel {
            stage('Unit Tests') {
                steps { sh 'npm test:unit' }
            }
            stage('Integration Tests') {
                steps { sh 'npm test:integration' }
            }
            stage('E2E Tests') {
                steps { sh 'npm test:e2e' }
            }
        }
    }
}
```

## أفضل الممارسات

✅ استخدم Jenkinsfile في repo
✅ استخدم agents ديناميكية
✅ اضبط retention policy
✅ استخدم credentials بشكل آمن
✅ اضبط parallel execution
✅ راقب أداء Jenkins

❌ لا تستخدم master للبناء
❌ لا تخزن كلمات مرور في plain text
❌ لا تترك builds قديمة كثيراً

---

## الكلمات المفتاحية

عربي: "جينكينز", "CI/CD", "أتمتة", "نشر"
English: "jenkins arabic", "CI/CD", "devops", "automation"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
