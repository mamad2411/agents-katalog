---
name: k8s-patterns
description: "Kubernetes YAML patterns: a production Deployment with full safety controls, Helm values and templates, KEDA scaling on SQS queue depth, namespace ResourceQuota and LimitRange, and a cluster upgrade checklist. Use when writing manifests or Helm charts, or planning a cluster upgrade."
---

# Kubernetes Patterns

Deployment strategies, Helm chart structure, HPA, PDB, NetworkPolicy, kubectl debugging, and cluster upgrades.

## Production Deployment with Full Safety Controls

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  annotations:
    deployment.kubernetes.io/revision: "1"
spec:
  replicas: 3
  revisionHistoryLimit: 5     # Keep 5 old ReplicaSets for rollback
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0       # Zero downtime
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.2.3
    spec:
      serviceAccountName: myapp-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001
        seccompProfile:
          type: RuntimeDefault
      terminationGracePeriodSeconds: 60
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels: {app: myapp}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels: {app: myapp}
                topologyKey: kubernetes.io/hostname
      containers:
        - name: app
          image: registry.example.com/myapp:v1.2.3
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          envFrom:
            - configMapRef:
                name: myapp-config
          resources:
            requests: {cpu: "100m", memory: "128Mi"}
            limits: {cpu: "500m", memory: "512Mi"}
          readinessProbe:
            httpGet: {path: /ready, port: http}
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3
          livenessProbe:
            httpGet: {path: /health, port: http}
            initialDelaySeconds: 15
            periodSeconds: 10
          startupProbe:
            httpGet: {path: /health, port: http}
            failureThreshold: 30
            periodSeconds: 5
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 10"]  # Drain period
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: [ALL]
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

## Helm Chart values.yaml Pattern

```yaml
# values.yaml
replicaCount: 2

image:
  repository: registry.example.com/myapp
  tag: ""         # Defaults to Chart.appVersion if empty
  pullPolicy: IfNotPresent

serviceAccount:
  create: true
  annotations: {}

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: false
  className: nginx
  annotations: {}
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
  enabled: true
  minReplicas: 2
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70

podDisruptionBudget:
  enabled: true
  minAvailable: 1

config:
  logLevel: info
  port: "8080"

# values-prod.yaml (production overrides)
replicaCount: 5
autoscaling:
  maxReplicas: 100
ingress:
  enabled: true
  tls:
    - secretName: myapp-tls
      hosts: [myapp.example.com]
```

```yaml
# templates/deployment.yaml (using values)
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
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

## KEDA: Scale on SQS Queue Depth

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: myworker-sqs-scaler
  namespace: production
spec:
  scaleTargetRef:
    name: myworker
  minReplicaCount: 0          # Scale to zero when queue empty
  maxReplicaCount: 50
  cooldownPeriod: 60
  pollingInterval: 10          # Check queue every 10 seconds
  triggers:
    - type: aws-sqs-queue
      authenticationRef:
        name: keda-aws-credentials
      metadata:
        queueURL: https://sqs.us-east-1.amazonaws.com/ACCOUNT/myapp-jobs
        queueLength: "10"     # Target 10 messages per pod
        awsRegion: us-east-1
        identityOwner: pod    # Use pod's IRSA
```

## Namespace Resource Quota and LimitRange

```yaml
# ResourceQuota: limit total namespace resource consumption
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "100"
    services: "20"
    persistentvolumeclaims: "20"

---
# LimitRange: enforce defaults on pods without resource specs
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:
        cpu: "500m"
        memory: "256Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
      max:
        cpu: "2"
        memory: "2Gi"
```

## Cluster Upgrade Checklist

```bash
# 1. Check current version and available upgrades
kubectl version
aws eks describe-cluster --name prod-cluster --query 'cluster.version'
az aks show --name prod-cluster --resource-group rg-prod --query kubernetesVersion

# 2. Verify all add-ons are compatible with target version
kubectl get deployment -n kube-system
helm list -A

# 3. Test upgrade on staging cluster first

# 4. Cordon node pool (for managed K8s, done by provider)
kubectl cordon node-1
kubectl drain node-1 --ignore-daemonsets --delete-emptydir-data

# 5. EKS: upgrade control plane, then node groups
aws eks update-cluster-version --name prod-cluster --kubernetes-version 1.29
aws eks update-nodegroup-version --cluster-name prod-cluster --nodegroup-name workers

# 6. Verify all system pods healthy after upgrade
kubectl get pods -n kube-system
kubectl get nodes

# 7. Uncordon
kubectl uncordon node-1
```
