---
name: bazel-k8s-expert
description: Expert knowledge for deploying Quarkus/Java applications to Kubernetes using Bazel. Covers rules_k8s, Helm, Kustomize, ConfigMaps, Secrets, and health probes.
version: 1.0.0
keywords: [bazel, kubernetes, k8s, helm, kustomize, deployment, quarkus, container]
---

# bazel-k8s-expert

> Keyword: k8s | Platforms: gemini,claude,codex

Bazel Kubernetes Expert Skill - Deploying, managing, and operating Quarkus and Java applications on Kubernetes using Bazel-native tooling.

## Core Mandates

- **GitOps-Ready:** All K8s manifests must be generated from Bazel targets, never hand-edited YAML in production.
- **Hermetic Deployments:** Use `rules_k8s` or `helm` via Bazel to ensure deployment artifacts match built images exactly.
- **Health Probes:** Every deployment must define `@Liveness` and `@Readiness` probes (see `microprofile-expert`).
- **Resource Limits:** Always set CPU/memory requests and limits to prevent cluster starvation.
- **Config Externalization:** Use ConfigMaps and Secrets for environment-specific values; never bake config into images.

---

## Setup (Bzlmod)

### MODULE.bazel

```python
bazel_dep(name = "rules_k8s", version = "0.7")
bazel_dep(name = "rules_helm", version = "0.1")

# For Kustomize support
bazel_dep(name = "rules_kustomize", version = "0.1")
```

---

## rules_k8s Deployment

### Basic Deployment + Service

```python
# services/user/k8s/BUILD.bazel
load("@rules_k8s//k8s:defs.bzl", "k8s_deploy")

k8s_deploy(
    name = "user-service_deploy",
    template = ":deployment.yaml",
    images = {
        "user-service": "//services/user:user-service_image",
    },
)
```

```yaml
# services/user/k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  labels:
    app: user-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
        - name: user-service
          image: user-service  # Replaced by rules_k8s
          ports:
            - containerPort: 8080
          env:
            - name: QUARKUS_HTTP_PORT
              value: "8080"
            - name: JAVA_TOOL_OPTIONS
              value: "-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /q/health/live
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /q/health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

### Deploy to Cluster

```bash
# Apply deployment
bazel run //services/user/k8s:user-service_deploy.apply

# Delete deployment
bazel run //services/user/k8s:user-service_deploy.delete

# Describe deployment
bazel run //services/user/k8s:user-service_deploy.describe
```

---

## ConfigMaps & Secrets

### ConfigMap from Properties File

```python
# services/order/k8s/BUILD.bazel
load("@rules_k8s//k8s:object.bzl", "k8s_object")

genrule(
    name = "order-config",
    srcs = ["application.properties"],
    outs = ["order-config.properties"],
    cmd = "cp $(SRCS) $@",
)

k8s_object(
    name = "order-configmap",
    template = "configmap.yaml",
    substitutions = {
        "{CONFIG_DATA}": "$(location :order-config)",
    },
)
```

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-service-config
data:
  application.properties: |
    quarkus.datasource.db-kind=postgresql
    quarkus.datasource.jdbc.url=jdbc:postgresql://postgres:5432/orders
    quarkus.hibernate-orm.database.generation=update
```

### Secret from Bazel Secrets

```python
# k8s/BUILD.bazel
load("@rules_k8s//k8s:object.bzl", "k8s_object")

k8s_object(
    name = "db-secret",
    template = "secret.yaml",
    substitutions = {
        "{DB_PASSWORD}": "$(location //secrets:db_password)",
    },
)
```

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:
  password: "{DB_PASSWORD}"
```

### Mounting in Deployment

```yaml
# deployment.yaml
spec:
  template:
    spec:
      containers:
        - name: order-service
          volumeMounts:
            - name: config
              mountPath: /app/config
            - name: secrets
              mountPath: /app/secrets
      volumes:
        - name: config
          configMap:
            name: order-service-config
        - name: secrets
          secret:
            secretName: db-credentials
```

---

## Helm Charts

### Chart Structure

```
services/user/helm/
├── BUILD.bazel
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    └── _helpers.tpl
```

### BUILD.bazel for Helm

```python
# services/user/helm/BUILD.bazel
load("@rules_helm//helm:defs.bzl", "helm_chart", "helm_push", "helm_template")

helm_chart(
    name = "user-service-chart",
    srcs = glob(["templates/**"]),
    chart_yaml = "Chart.yaml",
    values_yaml = "values.yaml",
)

helm_template(
    name = "user-service-template",
    chart = ":user-service-chart",
    values = "values-dev.yaml",
    namespace = "dev",
)

helm_push(
    name = "push-chart",
    chart = ":user-service-chart",
    repository = "oci://ghcr.io/myorg/charts",
    version = "1.0.0",
)
```

### Template with Image Reference

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "user-service.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.port }}
          env:
            - name: QUARKUS_PROFILE
              value: {{ .Values.quarkus.profile }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          livenessProbe:
            {{- toYaml .Values.livenessProbe | nindent 12 }}
          readinessProbe:
            {{- toYaml .Values.readinessProbe | nindent 12 }}
```

### values.yaml

```yaml
# values.yaml
replicaCount: 3

image:
  repository: ghcr.io/myorg/user-service
  pullPolicy: IfNotPresent
  tag: ""

quarkus:
  profile: prod

service:
  type: ClusterIP
  port: 8080

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

livenessProbe:
  httpGet:
    path: /q/health/live
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /q/health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Deploy Helm Chart

```bash
# Template (dry run)
bazel run //services/user/helm:user-service-template

# Install/Upgrade
helm upgrade --install user-service \
  $(bazel cquery --output=files //services/user/helm:user-service-chart) \
  --values services/user/helm/values-prod.yaml \
  --namespace prod

# Push to OCI registry
bazel run //services/user/helm:push-chart
```

---

## Kustomize

### Base + Overlay Pattern

```
services/payment/k8s/
├── base/
│   ├── BUILD.bazel
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── dev/
    │   ├── BUILD.bazel
    │   ├── kustomization.yaml
    │   └── replica-patch.yaml
    └── prod/
        ├── BUILD.bazel
        ├── kustomization.yaml
        └── resource-patch.yaml
```

### Base Configuration

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml

commonLabels:
  app: payment-service

images:
  - name: payment-service
    newTag: latest
```

### Dev Overlay

```yaml
# overlays/dev/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: dev

resources:
  - ../../base

replicas:
  - name: payment-service
    count: 1

configMapGenerator:
  - name: payment-config
    literals:
      - QUARKUS_PROFILE=dev
      - LOG_LEVEL=DEBUG
```

### Prod Overlay

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: prod

resources:
  - ../../base

replicas:
  - name: payment-service
    count: 5

patches:
  - path: resource-patch.yaml

configMapGenerator:
  - name: payment-config
    literals:
      - QUARKUS_PROFILE=prod
      - LOG_LEVEL=INFO
```

```yaml
# overlays/prod/resource-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  template:
    spec:
      containers:
        - name: payment-service
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "1Gi"
              cpu: "1000m"
```

### Bazel Kustomize Build

```python
# overlays/dev/BUILD.bazel
load("@rules_kustomize//kustomize:defs.bzl", "kustomize_build")

kustomize_build(
    name = "dev-manifests",
    srcs = glob(["*.yaml"]),
    kustomization = "kustomization.yaml",
)

# Apply
# kubectl apply -k $(bazel cquery --output=files //services/payment/k8s/overlays/dev:dev-manifests)
```

---

## Ingress

### Basic Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt"
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /users
            pathType: Prefix
            backend:
              service:
                name: user-service
                port:
                  number: 80
          - path: /orders
            pathType: Prefix
            backend:
              service:
                name: order-service
                port:
                  number: 80
```

---

## Horizontal Pod Autoscaler (HPA)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

---

## Pod Disruption Budget

```yaml
# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: user-service-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: user-service
```

---

## Troubleshooting

### Pod CrashLoopBackOff

```bash
# Check logs
kubectl logs -l app=user-service --tail=100

# Check events
kubectl describe pod user-service-xxx

# Common causes:
# 1. Missing ConfigMap/Secret → Create missing resources
# 2. Wrong image tag → Verify image was pushed
# 3. Port conflict → Check containerPort matches app
# 4. Resource limits too low → Increase memory/CPU limits
# 5. Liveness probe failing → Check /q/health/live endpoint
```

### Service Not Reachable

```bash
# Check service endpoints
kubectl get endpoints user-service

# Port-forward for testing
kubectl port-forward svc/user-service 8080:80

# Common causes:
# 1. Selector mismatch → Check labels on pod and service
# 2. Wrong targetPort → Must match containerPort
# 3. Network policies blocking → Check NetworkPolicy rules
```

### ImagePullBackOff

```bash
# Check image exists
kubectl describe pod user-service-xxx | grep -i "failed to pull"

# Common causes:
# 1. Image not pushed → bazel run //services/user:push_user_service
# 2. Wrong imagePullSecrets → Add registry credentials
# 3. Wrong image tag → Check tag in deployment
```

---

## Decision Trees

### Choosing Deployment Strategy

```
Single service?
  ├── YES → rules_k8s k8s_deploy (simplest)
  └── NO (multiple services)
        ├── Need templating? → Helm charts
        ├── Need environment overlays? → Kustomize
        └── Need both? → Helm + Kustomize (Helm chart + Kustomize patches)
```

### Config Management

```
Environment-specific values?
  ├── Simple key-value pairs → ConfigMap literals
  ├── Complex config files → ConfigMap from file
  ├── Sensitive data → Secret (base64 encoded)
  ├── Many environments → Kustomize configMapGenerator
  └── Dynamic values → External Secrets Operator
```

---

## References

- [rules_k8s GitHub](https://github.com/bazelbuild/rules_k8s)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kustomize Documentation](https://kustomize.io/)
- [Quarkus Kubernetes Guide](https://quarkus.io/guides/deploying-to-kubernetes)

## Skill Interoperability

The **bazel-k8s-expert** ☸️ skill deploys containers built by:
- **bazel-oci-expert** 🐳: OCI container images.
- **rules-quarkus** 🔧: Quarkus applications built with Bazel.
- **microprofile-expert** 📋: Health probes, metrics, and config.
- **bazel-expert** 🏗: Core Bazel build infrastructure.
