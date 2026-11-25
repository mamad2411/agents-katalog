---
name: helm-patterns
description: "When to activate: Helm, chart, values.yaml, templates, release, hook, subchart, Tiller, upgrade, rollback, helmfile"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: devops
  language: devops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Helm Patterns

## Chart Structure

```
myapp/
  Chart.yaml
  values.yaml
  values-prod.yaml
  templates/
    _helpers.tpl
    deployment.yaml
    service.yaml
    ingress.yaml
    configmap.yaml
    hpa.yaml
    NOTES.txt
  charts/          # subcharts / dependencies
```

## Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: My application Helm chart
type: application
version: 0.1.0        # Chart version (semver)
appVersion: "1.2.3"   # Application version

dependencies:
  - name: postgresql
    version: "13.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

## values.yaml

```yaml
replicaCount: 2

image:
  repository: ghcr.io/myorg/myapp
  tag: ""        # defaults to .Chart.AppVersion
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: nginx
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

postgresql:
  enabled: true
  auth:
    database: myapp
    username: myapp
```

## _helpers.tpl

```gotemplate
{{/*
Expand the name of the chart.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
app.kubernetes.io/name: {{ include "myapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

## deployment.yaml Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.port }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

## Helm Hook (DB migration)

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "myapp.fullname" . }}-migrate
  annotations:
    "helm.sh/hook": pre-upgrade,pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["./migrate", "up"]
```

## Release Management

```bash
# Install
helm install myapp ./myapp -f values-prod.yaml --namespace prod --create-namespace

# Upgrade (atomic: rollback on failure)
helm upgrade myapp ./myapp -f values-prod.yaml --atomic --timeout 5m

# Rollback
helm rollback myapp 0   # 0 = previous revision

# Diff before apply (requires helm-diff plugin)
helm diff upgrade myapp ./myapp -f values-prod.yaml

# List releases
helm list -A
helm history myapp -n prod
```

## Key Rules
- Use `--atomic` in CI upgrades — auto-rollbacks on timeout
- Template everything that differs between environments into values
- Use Helmfile or ArgoCD app-of-apps for managing multiple releases
- Validate templates: `helm template . | kubectl apply --dry-run=client -f -`
- Lock dependency versions in `Chart.lock` via `helm dependency update`
