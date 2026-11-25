---
name: kubernetes-manifests
description: Production-grade Kubernetes manifests, Deployments with zero-downtime rolling updates, Services, Ingress with TLS, ConfigMaps, Secrets, resource limits, and health probes.
aliases:
  - k8s
  - kubernetes
  - k8s-manifests
  - helm
category: "06 - Git, Commits & Release"
tags:
  - agent-skill
  - kubernetes
  - k8s
  - devops
  - deployment
  - stage-6
---

# Kubernetes Production Manifests & Cloud-Native Deployment

Standardized specifications for crafting resilient, secure, and production-ready Kubernetes (K8s) manifests.

---

## 🛡️ Production Checklist

1. **Explicit Resource Requests & Limits**:
   - Every container MUST declare `resources.requests` and `resources.limits` for both CPU and Memory to prevent OOMKills and noisy-neighbor node starvations.
2. **Comprehensive Health Probes**:
   - `startupProbe`: Allows slow initialization without premature termination.
   - `livenessProbe`: Detects deadlocks and restarts failing pods.
   - `readinessProbe`: Removes unready pods from Service endpoints to guarantee zero dropped traffic during deployments.
3. **Graceful Termination & Rolling Updates**:
   - Define `terminationGracePeriodSeconds: 30` (or higher) to allow ongoing HTTP requests to complete.
   - Configure `strategy.rollingUpdate.maxSurge: 25%` and `maxUnavailable: 0` for zero-downtime releases.
4. **Security Context Hardening**:
   - Enable `readOnlyRootFilesystem: true`, `runAsNonRoot: true`, and `allowPrivilegeEscalation: false`.

---

## 📦 Reference Architecture: Production Deployment & Service

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  labels:
    app.kubernetes.io/name: api-service
    app.kubernetes.io/part-of: core-platform
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
    spec:
      terminationGracePeriodSeconds: 30
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
        - name: app
          image: ghcr.io/org/api-service:v1.2.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
              name: http
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          securityContext:
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            capabilities:
              drop: ["ALL"]
          startupProbe:
            httpGet:
              path: /health/startup
              port: 8080
            failureThreshold: 30
            periodSeconds: 2
          livenessProbe:
            httpGet:
              path: /health/liveness
              port: 8080
            periodSeconds: 10
            timeoutSeconds: 3
          readinessProbe:
            httpGet:
              path: /health/readiness
              port: 8080
            periodSeconds: 5
            timeoutSeconds: 2
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
  labels:
    app.kubernetes.io/name: api-service
spec:
  type: ClusterIP
  selector:
    app: api-service
  ports:
    - name: http
      port: 80
      targetPort: http
```

---

## 🔗 Connected Skills (ทักษะที่เกี่ยวข้อง)
- [[Skills/docker-and-compose/SKILL|docker-and-compose]] — บิลด์ Docker Image ให้พร้อมสำหรับ Kubernetes
- [[Skills/git-workflow/SKILL|git-workflow]] — วงจร GitOps และการกำหนด Tag Semantic Versioning
- [[Skills/verification-before-completion/SKILL|verification-before-completion]] — ตรวจสอบ Manifest ด้วย `kubectl diff` หรือ `kubeval` ก่อนปล่อยระบบ

<!-- v1.1.0 synchronized: 2026-09-29 -->
