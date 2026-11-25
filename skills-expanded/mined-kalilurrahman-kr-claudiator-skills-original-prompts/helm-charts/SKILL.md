---
name: helm-charts
description: Create and manage Helm charts for Kubernetes application deployment. Outputs Chart.yaml, values.yaml, templates with best practices, named templates, hooks, and chart testing configuration.
argument-hint: [application name, deployment type, dependencies, environments]
allowed-tools: Read, Write, Bash
---

# Helm Charts

Package, version, and deploy Kubernetes applications with Helm. A good chart is environment-agnostic by default and opinionated only where it matters for production safety.

## Process

1. **Create chart scaffold** with `helm create` and clean out the defaults.
2. **Define values.yaml** — all tunables at the top level, sane defaults.
3. **Write templates** — deployment, service, ingress, configmap, HPA.
4. **Add named templates** in `_helpers.tpl` for reusable labels/selectors.
5. **Configure hooks** for pre-install migrations and post-upgrade smoke tests.
6. **Validate** with `helm lint` and `helm template --debug`.
7. **Test** with `helm test` using test pods.
8. **Version bump** in `Chart.yaml` on every change.

## Output Format

### Chart Structure

```
my-app/
├── Chart.yaml              # Chart metadata and dependencies
├── values.yaml             # Default configuration values
├── values-staging.yaml     # Environment overrides
├── values-production.yaml  # Production overrides
├── .helmignore
├── templates/
│   ├── _helpers.tpl         # Named templates (partials)
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml          # Usually sealed or external
│   ├── hpa.yaml
│   ├── pdb.yaml             # Pod Disruption Budget
│   ├── serviceaccount.yaml
│   ├── NOTES.txt            # Post-install instructions
│   └── tests/
│       └── test-connection.yaml
└── charts/                  # Subcharts / dependencies
```

### Chart.yaml

```yaml
apiVersion: v2
name: my-app
description: Order processing service
type: application
version: 1.4.2          # Chart version — bump on every change
appVersion: "2.1.0"     # Application version

maintainers:
  - name: Platform Team
    email: platform@example.com

dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled   # Can be disabled for external DB
  - name: redis
    version: "17.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

### values.yaml

```yaml
# ── Image ─────────────────────────────────────────────────
image:
  repository: ghcr.io/example/my-app
  tag: ""               # Defaults to Chart.appVersion if empty
  pullPolicy: IfNotPresent
  pullSecrets: []

# ── Replicas & Scaling ────────────────────────────────────
replicaCount: 2

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

# ── Resources ─────────────────────────────────────────────
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

# ── Service ───────────────────────────────────────────────
service:
  type: ClusterIP
  port: 80
  targetPort: 8080
  annotations: {}

# ── Ingress ───────────────────────────────────────────────
ingress:
  enabled: false
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
  hosts:
    - host: my-app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: my-app-tls
      hosts:
        - my-app.example.com

# ── Application Config ────────────────────────────────────
config:
  logLevel: info
  port: 8080
  databaseUrl: ""         # Override in production
  redisUrl: ""

# ── Secrets (prefer ExternalSecrets or Vault) ─────────────
secrets:
  create: true            # Set false if using external secret manager
  annotations: {}

# ── Health Checks ─────────────────────────────────────────
livenessProbe:
  httpGet:
    path: /healthz
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3

# ── Pod Settings ──────────────────────────────────────────
podAnnotations: {}
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

# ── Scheduling ────────────────────────────────────────────
nodeSelector: {}
tolerations: []
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app.kubernetes.io/name
                operator: In
                values:
                  - my-app
          topologyKey: kubernetes.io/hostname

# ── Disruption Budget ─────────────────────────────────────
podDisruptionBudget:
  enabled: true
  minAvailable: 1

# ── Service Account ───────────────────────────────────────
serviceAccount:
  create: true
  annotations: {}
  name: ""

# ── Dependencies ──────────────────────────────────────────
postgresql:
  enabled: false          # Use external DB by default
  auth:
    database: myapp
    username: myapp
    existingSecret: my-app-db-secret

redis:
  enabled: false
```

### templates/_helpers.tpl

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "my-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "my-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart label.
*/}}
{{- define "my-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels — applied to ALL resources.
*/}}
{{- define "my-app.labels" -}}
helm.sh/chart: {{ include "my-app.chart" . }}
{{ include "my-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels — used in selector and pod template.
Must be stable across upgrades — do NOT include Chart.Version here.
*/}}
{{- define "my-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Service account name.
*/}}
{{- define "my-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "my-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Image reference. Falls back to chart appVersion.
*/}}
{{- define "my-app.image" -}}
{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}
{{- end }}
```

### templates/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
  annotations:
    # Trigger rolling restart on configmap change
    checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0      # Zero-downtime rollout
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
      annotations:
        {{- toYaml .Values.podAnnotations | nindent 8 }}
    spec:
      {{- with .Values.image.pullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "my-app.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          image: {{ include "my-app.image" . }}
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          ports:
            - name: http
              containerPort: {{ .Values.config.port }}
              protocol: TCP
          envFrom:
            - configMapRef:
                name: {{ include "my-app.fullname" . }}
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "my-app.fullname" . }}
                  key: database-url
                  optional: {{ not .Values.secrets.create }}
          livenessProbe:
            {{- toYaml .Values.livenessProbe | nindent 12 }}
          readinessProbe:
            {{- toYaml .Values.readinessProbe | nindent 12 }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          volumeMounts:
            - name: tmp
              mountPath: /tmp     # Needed for readOnlyRootFilesystem
      volumes:
        - name: tmp
          emptyDir: {}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

### templates/hpa.yaml

```yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "my-app.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    {{- end }}
    {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
    {{- end }}
{{- end }}
```

### templates/tests/test-connection.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "my-app.fullname" . }}-test"
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  restartPolicy: Never
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args:
        - '--spider'
        - '--timeout=5'
        - 'http://{{ include "my-app.fullname" . }}:{{ .Values.service.port }}/healthz'
```

### Deployment Commands

```bash
# Add chart dependencies
helm dependency update ./my-app

# Lint (always before deploy)
helm lint ./my-app
helm lint ./my-app -f values-production.yaml

# Dry run to see rendered templates
helm template my-app ./my-app -f values-production.yaml

# Install
helm install my-app ./my-app \
  --namespace production \
  --create-namespace \
  -f values-production.yaml \
  --set image.tag=2.1.0 \
  --wait \
  --timeout 5m

# Upgrade (rolling deploy)
helm upgrade my-app ./my-app \
  --namespace production \
  -f values-production.yaml \
  --set image.tag=2.1.1 \
  --wait \
  --timeout 5m

# Rollback
helm rollback my-app 1 --namespace production

# View history
helm history my-app --namespace production

# Run tests
helm test my-app --namespace production

# Diff before upgrade (requires helm-diff plugin)
helm diff upgrade my-app ./my-app -f values-production.yaml --set image.tag=2.1.1
```

## Rules

- **Checksum annotations on configmaps** — force pod restarts when config changes.
- **Never hardcode secrets** in values files — use ExternalSecrets, Vault, or sealed secrets.
- **Always set resource requests and limits** — unbounded pods get evicted first.
- **`maxUnavailable: 0`** on RollingUpdate for zero-downtime deployments.
- **Selector labels must be immutable** — changing them requires a delete+reinstall.
- **`readOnlyRootFilesystem: true`** with an emptyDir for `/tmp` — security hardening.
- **`runAsNonRoot: true`** — never run as root in containers.
- **PodDisruptionBudget** — prevents all pods from being evicted simultaneously.
- **Named templates in `_helpers.tpl`** — DRY for labels, names, selectors.
- **Version bump on every chart change** — enables rollback and auditing.
- **Test hooks** — always include a basic health check test pod.
- **Use `--wait`** in CI — fail fast if rollout doesn't complete.
