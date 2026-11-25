---
name: tpl-devops-kubernetes-helm
description: Template do pack (devops/03-kubernetes-helm.md). Orienta o agente em infra, deploy, CI/CD e operacao alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: devops/03-kubernetes-helm.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Kubernetes + Helm Production Deployment

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `devops/03-kubernetes-helm.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Orchestration:** Kubernetes 1.29+
- **Package Manager:** Helm 3.14+
- **Ingress:** ingress-nginx (stable/ingress-nginx)
- **TLS:** cert-manager + Let's Encrypt (ClusterIssuer)
- **Autoscaling:** HorizontalPodAutoscaler (HPA) + KEDA (optional)
- **Secrets:** External Secrets Operator + AWS Secrets Manager / Vault
- **Storage:** PersistentVolumeClaims (EBS GP3 via StorageClass)
- **Monitoring:** Prometheus + Grafana (kube-prometheus-stack)

---

## HELM CHART STRUCTURE
```
charts/my-app/
├── Chart.yaml
├── values.yaml             # Default values (non-sensitive)
├── values-staging.yaml     # Override for staging
├── values-prod.yaml        # Override for prod
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── hpa.yaml
    ├── pdb.yaml             # PodDisruptionBudget
    ├── externalsecret.yaml
    ├── configmap.yaml
    └── _helpers.tpl         # Named templates
```

---

## ARCHITECTURE RULES
1. **Resource limits are mandatory** — every container has `requests` and `limits`; no exceptions.
2. **Readiness gates before traffic** — readiness probe must succeed before pod receives traffic; liveness resets late.
3. **Rolling update is default** — `maxUnavailable: 0`, `maxSurge: 1` ensuring zero-downtime deploys.
4. **PodDisruptionBudget on every prod deployment** — `minAvailable: 1` protects against node drain.
5. **Secrets never in values.yaml** — use External Secrets Operator; never `kubectl create secret` manually.
6. **Namespace per application** — not per environment; use separate clusters for prod vs non-prod.
7. **HPA targets 60% CPU** — scale out before saturation; not at 80%.
8. **Images use immutable tags** — `sha256:abc…` or `1.2.3`; never `latest` in production.

---

## DEPLOYMENT TEMPLATE

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels: {{ include "my-app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels: {{ include "my-app.selectorLabels" . | nindent 6 }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    metadata:
      labels: {{ include "my-app.selectorLabels" . | nindent 8 }}
      annotations:
        # Force pod restart when configmap changes
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
    spec:
      terminationGracePeriodSeconds: 60
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
        - name: app
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: {{ .Values.service.port }}
              protocol: TCP
          envFrom:
            - configMapRef:
                name: {{ include "my-app.fullname" . }}-config
            - secretRef:
                name: {{ include "my-app.fullname" . }}-secrets
          resources:
            requests:
              cpu:    {{ .Values.resources.requests.cpu }}
              memory: {{ .Values.resources.requests.memory }}
            limits:
              cpu:    {{ .Values.resources.limits.cpu }}
              memory: {{ .Values.resources.limits.memory }}
          readinessProbe:
            httpGet:
              path: /healthz/ready
              port: {{ .Values.service.port }}
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /healthz/live
              port: {{ .Values.service.port }}
            initialDelaySeconds: 30    # Give app time to fully start
            periodSeconds: 15
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /healthz/ready
              port: {{ .Values.service.port }}
            failureThreshold: 30       # 30 * 10s = 5 min startup window
            periodSeconds: 10
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 5"]   # Drain in-flight requests
```

---

## VALUES.YAML STRUCTURE

```yaml
# values.yaml
replicaCount: 2

image:
  repository: 123456789.dkr.ecr.us-east-1.amazonaws.com/my-app
  tag: "1.0.0"   # Never "latest"

service:
  type: ClusterIP
  port: 3000

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: api.myapp.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts: [api.myapp.com]

resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 60
  targetMemoryUtilizationPercentage: 70

# Override per environment:
# values-prod.yaml:
#   replicaCount: 3
#   resources:
#     requests: { cpu: "250m", memory: "256Mi" }
#     limits: { cpu: "1000m", memory: "1Gi" }
```

---

## HPA TEMPLATE

```yaml
# templates/hpa.yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "my-app.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300   # Wait 5 min before scaling down
      policies:
        - type: Pods
          value: 1
          periodSeconds: 60
{{- end }}
```

---

## EXTERNAL SECRETS OPERATOR

```yaml
# templates/externalsecret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ include "my-app.fullname" . }}-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager       # ClusterSecretStore configured cluster-wide
    kind: ClusterSecretStore
  target:
    name: {{ include "my-app.fullname" . }}-secrets
    creationPolicy: Owner
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: myapp/prod/database
        property: url
    - secretKey: JWT_SECRET
      remoteRef:
        key: myapp/prod/jwt
        property: secret
```

---

## PERSISTENT VOLUME CLAIM

```yaml
# StorageClass — EBS GP3 (create once per cluster)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
reclaimPolicy: Retain         # Never Delete for prod data
volumeBindingMode: WaitForFirstConsumer
---
# PVC in deployment
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: gp3
  resources:
    requests:
      storage: 20Gi
```

---

## HELM DEPLOY COMMANDS

```bash
# Add chart repos
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add cert-manager https://charts.jetstack.io
helm repo add external-secrets https://charts.external-secrets.io
helm repo update

# Install cert-manager
helm install cert-manager cert-manager/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true

# Deploy app
helm upgrade --install my-app ./charts/my-app \
  --namespace my-app --create-namespace \
  --values charts/my-app/values.yaml \
  --values charts/my-app/values-prod.yaml \
  --set image.tag=$IMAGE_TAG \
  --atomic \
  --timeout 5m \
  --history-max 5

# Rollback
helm rollback my-app 0   # 0 = previous revision
```

---

## READINESS vs LIVENESS RULES
```
readinessProbe  → "Is the pod ready to receive traffic?"
  - Fails if DB connection pool is exhausted
  - Fails during app initialization
  - Pod removed from Service endpoints when failing
  - Use: /healthz/ready → check DB, Redis, downstream deps

livenessProbe   → "Is the pod in a broken, unrecoverable state?"
  - Only fails if app is truly hung (deadlock, OOM)
  - Triggers pod restart
  - Use: /healthz/live → simple ping, no external deps

startupProbe    → "Has the app finished booting?"
  - Disables liveness during slow startup (heavy apps, migrations)
  - Once succeeds, hands off to liveness
```
