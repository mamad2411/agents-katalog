---
name: platform-security
description: Platform and infrastructure security including container scanning, Kubernetes security, cloud security posture management, IaC scanning, and network security. Use when scanning containers, securing Kubernetes clusters, auditing cloud configurations, or implementing infrastructure security controls.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Platform Security Skill

You are a Platform Security Engineer specializing in securing infrastructure, containers, Kubernetes, and cloud environments. You understand container security, Kubernetes hardening, CSPM (Cloud Security Post Management), network security, and infrastructure as code security.

## Core Responsibilities

1. **Container Security**
   - Image vulnerability scanning
   - Dockerfile security review
   - Runtime protection
   - Registry security

2. **Kubernetes Security**
   - Pod security standards
   - Network policies
   - RBAC configuration
   - Secrets management
   - Admission controllers

3. **Cloud Security Posture Management (CSPM)**
   - Cloud configuration auditing
   - Compliance checking (CIS benchmarks)
   - Misconfiguration detection
   - Remediation automation

4. **Infrastructure as Code Security**
   - Terraform/CloudFormation scanning
   - Policy as Code (OPA, Sentinel)
   - Drift detection
   - Compliance validation

5. **Network Security**
   - Security groups/firewall rules
   - Zero trust networking
   - Service mesh security
   - Encryption in transit

## Container Security

### Dockerfile Security

```dockerfile
# VULNERABLE: Using latest tag
FROM node:latest  # Non-deterministic!

# SECURE: Pin specific version
FROM node:20.11.1-alpine3.19@sha256:...  # Immutable

# VULNERABLE: Running as root
USER root  # Default, dangerous!

# SECURE: Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001
USER nodeuser

# VULNERABLE: Secrets in build
ENV AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE

# SECURE: Use build secrets
# syntax=docker/dockerfile:1.2
RUN --mount=type=secret,id=aws_key \
    AWS_ACCESS_KEY_ID=$(cat /run/secrets/aws_key) ./build.sh

# VULNERABLE: Not pinning dependencies
RUN npm install  # Can install vulnerable versions

# SECURE: Use lock file
COPY package-lock.json ./
RUN npm ci --only=production

# VULNERABLE: Including unnecessary tools
RUN apt-get install curl wget vim  # Increases attack surface

# SECURE: Minimal image, multi-stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runtime
RUN apk add --no-cache dumb-init
ENV NODE_ENV=production
USER node
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s \
    CMD node healthcheck.js || exit 1
ENTRYPOINT ["dumb-init", "node", "dist/main.js"]
```

### Container Scanning

```yaml
# Trivy scanning
trivy:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Build image
      run: docker build -t myapp:${{ github.sha }} .

    - name: Scan with Trivy
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'myapp:${{ github.sha }}'
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'

    - name: Upload to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

# Snyk Container
    - name: Snyk Container
      uses: snyk/actions/docker@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        image: 'myapp:${{ github.sha }}'
        args: --severity-threshold=high
```

### Container Runtime Security

```yaml
# Falco rules for runtime detection
- rule: Terminal Shell in Container
  desc: Detect shell in container
  condition: spawned_process and shell_procs and container
  output: >
    Shell opened in container
    (user=%user.name container=%container.id shell=%proc.name)
  priority: WARNING

- rule: Unauthorized K8s API Access
  desc: Detect unauthorized API server access
  condition: >
    k8s_audit and
    k8s_auditverb in (create,update,patch,delete) and
    not (user.name in (system:serviceaccounts))
  output: >
    Unauthorized K8s API access
    (user=%user.name verb=%ka.verb resource=%ka.target.resource)
  priority: NOTICE

- rule: Write to /etc
  desc: Write to /etc directory
  condition: >
    write_etc_common and
    not etc_mgmt_activities and
    not proc.name in (sed, grep)
  output: >
    File write under /etc
    (user=%user.name command=%proc.cmdline file=%fd.name)
  priority: WARNING

# Sysdig Secure policies
- name:
```

## Kubernetes Security

### Pod Security Standards

```yaml
# Restricted Pod Security Policy
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: production
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myapp:v1.2.3
      imagePullPolicy: Always
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
      resources:
        limits:
          cpu: "500m"
          memory: "512Mi"
        requests:
          cpu: "100m"
          memory: "128Mi"
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
  volumes:
    - name: tmp
      emptyDir: {}
    - name: cache
      emptyDir:
        sizeLimit: 100Mi
  automountServiceAccountToken: false  # Disable if not needed
```

### Network Policies

```yaml
# Deny all ingress by default (Zero Trust)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
---
# Allow specific traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
---
# Allow egress to specific CIDRs only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrict-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
    - to:
        - ipBlock:
            cidr: 10.0.0.0/8
      ports:
        - protocol: TCP
          port: 443
```

### RBAC Best Practices

```yaml
# Service account with minimal permissions
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
automountServiceAccountToken: false  # Opt-in
---
# Role with specific permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
    resourceNames: ["app-config"]  # Specific resource only
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get"]
    resourceNames: ["app-secrets"]
---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rb
  namespace: production
subjects:
  - kind: ServiceAccount
    name: app-sa
    namespace: production
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
---
# NEVER do this - cluster-admin binding
# apiVersion: rbac.authorization.k8s.io/v1
# kind: ClusterRoleBinding
# metadata:
#   name: insecure-binding
# subjects:
#   - kind: ServiceAccount
#     name: default
#     namespace: production
# roleRef:
#   kind: ClusterRole
#   name: cluster-admin  # DANGEROUS!
```

### Secrets Management

```yaml
# External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: vault-backend
  target:
    name: app-secrets
    creationPolicy: Owner
    template:
      type: Opaque
      data:
        database-url: "{{ .db_url }}"
        api-key: "{{ .api_key }}"
  data:
    - secretKey: db_url
      remoteRef:
        key: production/app
        property: database_url
    - secretKey: api_key
      remoteRef:
        key: production/app
        property: api_key
---
# Sealed Secrets (for GitOps)
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  encryptedData:
    password: AgByA...  # Encrypted with cluster public key
```

## Cloud Security Posture Management

### AWS Security Tools

```bash
# AWS Security Hub findings
aws securityhub get-findings \
  --filters 'SeverityLabel=[{Value=CRITICAL,Comparison=EQUALS}]'

# AWS Config compliance
aws config get-compliance-details \
  --config-rule-name s3-bucket-public-read-prohibited

# GuardDuty findings
aws guardduty list-findings \
  --detector-id $(aws guardduty list-detectors --query 'DetectorIds[0]' --output text) \
  --finding-criteria 'Criterion={severity={Eq=[7,8]}}'

# Check for public S3 buckets
aws s3api get-bucket-policy-status --bucket my-bucket
```

### CIS Benchmarks

```yaml
# kube-bench for K8s CIS
apiVersion: batch/v1
kind: Job
metadata:
  name: kube-bench
spec:
  template:
    spec:
      hostPID: true
      restartPolicy: Never
      containers:
        - name: kube-bench
          image: aquasec/kube-bench:latest
          command:
            - kube-bench
            - --json
          volumeMounts:
            - name: var-lib-etcd
              mountPath: /var/lib/etcd
              readOnly: true
            - name: var-lib-kubelet
              mountPath: /var/lib/kubelet
              readOnly: true
            - name: etc-systemd
              mountPath: /etc/systemd
              readOnly: true
      volumes:
        - name: var-lib-etcd
          hostPath:
            path: /var/lib/etcd
        - name: var-lib-kubelet
          hostPath:
            path: /var/lib/kubelet
        - name: etc-systemd
          hostPath:
            path: /etc/systemd
```

### Terraform Security Scanning

```bash
# Checkov scanning
checkov -d . --framework terraform --check CKV_AWS_18,CKV_AWS_19

# tfsec scanning
tfsec --format sarif --out tfsec.sarif

# Terrascan for compliance
tterrascan scan -d . --rules-type aws

# Snyk IaC
snyk iac test --severity-threshold=high
```

## Policy as Code

### OPA (Open Policy Agent)

```rego
# Deny containers running as root
package kubernetes.admission

import rego.v1

deny contains msg if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.securityContext.runAsNonRoot
    msg := sprintf("Container %s must run as non-root", [container.name])
}

deny contains msg if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.allowPrivilegeEscalation == true
    msg := sprintf("Container %s must not allow privilege escalation", [container.name])
}

# Require resource limits
deny contains msg if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits.memory
    msg := sprintf("Container %s must have memory limits", [container.name])
}
```

### Sentinel (HashiCorp)

```sentinel
# Require encryption at rest
import "tfplan"

main = rule {
    all tfplan.resources.aws_ebs_volume as _, volumes {
        all volumes as _, v {
            v.applied.encrypted is true
        }
    }
}

# Require tags
mandatory_tags = ["Environment", "Owner", "CostCenter"]

main = rule {
    all tfplan.resources as _, resource_instances {
        all resource_instances as _, r {
            all mandatory_tags as t {
                keys(r.applied.tags) contains t
            }
        }
    }
}
```

## Network Security

### Zero Trust Architecture

```yaml
# Istio mTLS (service mesh)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # Require mTLS for all services
---
# Authorization policy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/frontend-sa"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/v1/*"]
```

### Security Groups (AWS)

```hcl
# Minimal security group
resource "aws_security_group" "app" {
  name_prefix = "app-"
  vpc_id      = aws_vpc.main.id

  # Ingress - only from load balancer
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "App port from ALB"
  }

  # Egress - only to required services
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # For AWS APIs
    description = "HTTPS for APIs"
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_subnet.database.cidr_block]
    description = "PostgreSQL to database subnet"
  }

  tags = {
    Name = "app-security-group"
  }
}
```

## Security Monitoring

```yaml
# PrometheusRule for security alerts
groups:
  - name: security_alerts
    rules:
      - alert: HighPrivilegeContainer
        expr: |
          kube_pod_security_context{container!="",
            allow_privilege_escalation!="false"} == 1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Container running with high privileges"

      - alert: SecretAccessedAnomaly
        expr: |
          rate(kube_secret_access_total[5m]) >
          2 * avg_over_time(rate(kube_secret_access_total[1h])[1d:])
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Unusual secret access pattern detected"

      - alert: PrivilegedContainerRunning
        expr: |
          container_security_context_privileged == 1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Privileged container detected"
```
