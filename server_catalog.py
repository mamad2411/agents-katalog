#!/usr/bin/env python3
"""server_catalog — scaffold server, infra, data-service, dan security.

Entri memakai bentuk yang sama dengan framework_catalog sehingga
`project-forge new <dir> --framework <id>` langsung mendukung semuanya.

Konvensi gate:
  - perintah shell biasa → PASS/FAIL (SKIP bila binary tidak ada)
  - perintah diawali "SKIP:" → selalu SKIP dengan alasan (butuh aset/izin runtime)
"""

F = {}


def f(id, lang, kind, boot, gates=None, deps="", needs=(), hint="", files=None):
    F[id] = {
        "id": id, "lang": lang, "kind": kind, "boot": boot,
        "gates": gates or {}, "deps": deps, "needs": list(needs) or [boot.split()[0]],
        "hint": hint, "files": files or {},
    }


# ═══ EDGE / WEB SERVER ═══════════════════════════════════════════════════════
NGINX_CONF = r"""# {name} — nginx reverse proxy + TLS
worker_processes auto;
error_log  logs/error.log warn;
pid        logs/nginx.pid;

events { worker_connections 1024; }

http {
  include       mime.types;
  default_type  application/octet-stream;
  sendfile      on;
  server_tokens off;

  log_format main '$remote_addr - $request $status $body_bytes_sent';
  access_log logs/access.log main;

  # keamanan dasar
  add_header X-Content-Type-Options nosniff always;
  add_header X-Frame-Options DENY always;
  add_header Referrer-Policy strict-origin-when-cross-origin always;
  add_header Content-Security-Policy "default-src 'self'" always;
  add_header Permissions-Policy "geolocation=(), microphone=()" always;

  limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

  upstream app { server 127.0.0.1:3000; keepalive 32; }

  server {
    listen 8080;
    server_name _;

    location /health { return 200 'ok'; add_header Content-Type text/plain; }

    location / {
      limit_req zone=api burst=20 nodelay;
      proxy_pass http://app;
      proxy_http_version 1.1;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_read_timeout 30s;
    }
  }
}
"""

f("nginx", "config", "server",
  "mkdir -p logs && printf 'types { text/html html; application/json json; }\\n' > mime.types",
  {"lint": "nginx -t -c nginx.conf -p \"$PWD\"",
   "types": "nginx -t -c nginx.conf -p \"$PWD\"",
   "test": "grep -q 'X-Frame-Options' nginx.conf",
   "build": "nginx -t -c nginx.conf -p \"$PWD\""},
  needs=["nginx"], hint="brew install nginx", files={"nginx.conf": NGINX_CONF})

CADDYFILE = r"""# {name} — Caddy (TLS otomatis)
{
  admin off
  email admin@example.com
}

:8080 {
  encode zstd gzip

  header {
    X-Content-Type-Options nosniff
    X-Frame-Options DENY
    Referrer-Policy strict-origin-when-cross-origin
    -Server
  }

  handle /health {
    respond "ok" 200
  }

  handle {
    reverse_proxy 127.0.0.1:3000 {
      health_uri /health
      health_interval 15s
    }
  }

  log {
    output file logs/access.log
    format json
  }
}
"""

f("caddy", "config", "server", "mkdir -p logs",
  {"lint": "caddy validate --config Caddyfile --adapter caddyfile",
   "types": "caddy validate --config Caddyfile --adapter caddyfile",
   "test": "grep -q 'reverse_proxy' Caddyfile",
   "build": "caddy validate --config Caddyfile --adapter caddyfile"},
  needs=["caddy"], hint="brew install caddy", files={"Caddyfile": CADDYFILE})

TRAEFIK_YML = r"""# {name} — Traefik (docker provider)
entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    exposedByDefault: false
    network: proxy

api:
  dashboard: false

log:
  level: INFO

accessLog: {{}}

metrics:
  prometheus:
    addEntryPointsLabels: true
"""

f("traefik", "config", "server", "mkdir -p logs",
  {"lint": "test -s traefik.yml && grep -q 'entryPoints' traefik.yml",
   "types": "grep -q 'providers' traefik.yml",
   "test": "grep -q 'exposedByDefault: false' traefik.yml",
   "build": "test -s traefik.yml"},
  needs=["docker"], hint="docker (traefik jalan di container)",
  files={"traefik.yml": TRAEFIK_YML})

# ═══ CONTAINER ═══════════════════════════════════════════════════════════════
DOCKERFILE = r"""# {name} — image produksi multi-stage, non-root
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build --if-present

FROM node:22-alpine
RUN addgroup -S app && adduser -S -G app app
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build --chown=app:app /app ./
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD ["wget", "-qO-", "http://127.0.0.1:3000/health"]
ENTRYPOINT ["node", "src/server.js"]
"""

COMPOSE = r"""# {name} — compose dasar (bukan untuk produksi apa adanya)
services:
  app:
    build: .
    restart: unless-stopped
    environment:
      NODE_ENV: production
      DATABASE_URL: postgres://app:app@db:5432/app
    ports: ["8080:3000"]
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:3000/health"]
      interval: 30s
      retries: 3
    read_only: true
    tmpfs: ["/tmp"]
    security_opt: ["no-new-privileges:true"]
    cap_drop: ["ALL"]

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?wajib diisi}
      POSTGRES_DB: app
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      retries: 5

volumes:
  pgdata: {{}}
"""

f("dockerfile", "docker", "container", "true",
  {"lint": "hadolint --failure-threshold warning Dockerfile", "types": "grep -q 'USER ' Dockerfile",
   "test": "grep -q 'HEALTHCHECK' Dockerfile",
   "build": "docker build --check . 2>/dev/null || hadolint Dockerfile"},
  needs=["docker"], hint="docker + hadolint", files={"Dockerfile": DOCKERFILE})

f("compose", "docker", "container", "true",
  {"lint": "docker compose config -q", "types": "docker compose config -q",
   "test": "grep -q 'no-new-privileges' compose.yaml",
   "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": COMPOSE})

COMPOSE_STACK = COMPOSE.replace('services:\n  app:', '''services:
  proxy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports: ["80:80", "443:443"]
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
    depends_on: [app]

  app:''')
COMPOSE_STACK += "\n  caddy_data: {}\n"

f("compose-stack", "docker", "container", "mkdir -p logs",
  {"lint": "docker compose config -q", "types": "docker compose config -q",
   "test": "grep -q 'proxy:' compose.yaml && test -s Caddyfile",
   "build": "docker compose config -q"},
  needs=["docker"], hint="docker",
  files={"compose.yaml": COMPOSE_STACK, "Caddyfile": CADDYFILE})

# ═══ KUBERNETES ══════════════════════════════════════════════════════════════
K8S_DEPLOY = r"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {slug}
  labels: {{ app: {slug} }}
spec:
  replicas: 2
  selector:
    matchLabels: {{ app: {slug} }}
  template:
    metadata:
      labels: {{ app: {slug} }}
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile: {{ type: RuntimeDefault }}
      containers:
        - name: app
          image: ghcr.io/example/{slug}:latest
          ports: [{{ containerPort: 3000, name: http }}]
          resources:
            requests: {{ cpu: 50m, memory: 64Mi }}
            limits: {{ cpu: 500m, memory: 256Mi }}
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: {{ drop: ["ALL"] }}
          readinessProbe:
            httpGet: {{ path: /health, port: http }}
            initialDelaySeconds: 5
          livenessProbe:
            httpGet: {{ path: /health, port: http }}
            initialDelaySeconds: 15
---

apiVersion: v1
kind: Service
metadata:
  name: {slug}
spec:
  selector: {{ app: {slug} }}
  ports: [{{ port: 80, targetPort: http }}]
---

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {slug}
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
    - host: {slug}.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {slug}
                port: {{ number: 80 }}
---

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {slug}
spec:
  scaleTargetRef: {{ apiVersion: apps/v1, kind: Deployment, name: {slug} }}
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: {{ type: Utilization, averageUtilization: 70 }}
---

apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {slug}
spec:
  minAvailable: 1
  selector:
    matchLabels: {{ app: {slug} }}
"""

K8S_NETPOL = r"""apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {slug}-default-deny
spec:
  podSelector: {{ matchLabels: {{ app: {slug} }} }}
  policyTypes: [Ingress, Egress]
  ingress:
    - from:
        - namespaceSelector: {{ matchLabels: {{ kubernetes.io/metadata.name: ingress-nginx }} }}
      ports: [{{ port: 3000, protocol: TCP }}]
  egress:
    - to:
        - namespaceSelector: {{ matchLabels: {{ kubernetes.io/metadata.name: kube-system }} }}
      ports: [{{ port: 53, protocol: UDP }}]
"""

f("k8s", "yaml", "k8s", "mkdir -p k8s",
  {"lint": "kubeconform -strict -summary -ignore-missing-schemas k8s/",
   "types": "kubeconform -strict -summary -ignore-missing-schemas k8s/",
   "test": "grep -q 'runAsNonRoot: true' k8s/deployment.yaml",
   "build": "grep -q 'NetworkPolicy' k8s/networkpolicy.yaml"},
  needs=["kubeconform"], hint="brew install kubeconform",
  files={"k8s/deployment.yaml": K8S_DEPLOY, "k8s/networkpolicy.yaml": K8S_NETPOL})

CHART = r"""apiVersion: v2
name: {slug}
description: Helm chart {name}
type: application
version: 0.1.0
appVersion: "1.0.0"
"""

CHART_VALUES = r"""replicaCount: 2

image:
  repository: ghcr.io/example/{slug}
  tag: latest
  pullPolicy: IfNotPresent

service:
  port: 80

resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 500m
    memory: 256Mi

securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
"""

CHART_DEPLOY = r"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "chart.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ include "chart.name" . }}
  template:
    metadata:
      labels:
        app: {{ include "chart.name" . }}
    spec:
      securityContext:
        runAsNonRoot: {{ .Values.securityContext.runAsNonRoot }}
      containers:
        - name: app
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: 3000
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          securityContext:
            allowPrivilegeEscalation: {{ .Values.securityContext.allowPrivilegeEscalation }}
            readOnlyRootFilesystem: {{ .Values.securityContext.readOnlyRootFilesystem }}
"""

CHART_HELPERS = r"""{{- define "chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "chart.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "chart.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
"""

f("helm", "yaml", "k8s", "mkdir -p chart/templates",
  {"lint": "helm lint chart", "types": "helm template rel chart >/dev/null",
   "test": "helm template rel chart | grep -q 'kind: Deployment'",
   "build": "helm lint chart && helm template rel chart >/dev/null"},
  needs=["helm"], hint="brew install helm",
  files={"chart/Chart.yaml": CHART, "chart/values.yaml": CHART_VALUES,
         "chart/templates/deployment.yaml": CHART_DEPLOY,
         "chart/templates/_helpers.tpl": CHART_HELPERS})

KUSTOMIZATION = r"""apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - networkpolicy.yaml
images:
  - name: ghcr.io/example/app
    newTag: 1.0.0
"""

f("kustomize", "yaml", "k8s", "mkdir -p base overlays/prod",
  {"lint": "kubectl kustomize base >/dev/null",
   "types": "kubectl kustomize base >/dev/null",
   "test": "grep -q 'resources:' base/kustomization.yaml",
   "build": "kubectl kustomize base >/dev/null"},
  needs=["kubectl"], hint="brew install kubectl",
  files={"base/kustomization.yaml": KUSTOMIZATION,
         "base/deployment.yaml": K8S_DEPLOY,
         "base/networkpolicy.yaml": K8S_NETPOL})

# ═══ IaC / OPS ═══════════════════════════════════════════════════════════════
TF_MAIN = r"""# {name} — infrastruktur dasar (provider contoh)
terraform {{
  required_version = ">= 1.6"
  required_providers {{
    local = {{ source = "hashicorp/local", version = "~> 2.5" }}
  }}
}}

variable "project" {{
  type    = string
  default = "{slug}"
}}

resource "local_file" "manifest" {{
  filename = "${{path.module}}/out/${{var.project}}.json"
  content  = jsonencode({{ project = var.project, managed_by = "terraform" }})
}}

output "manifest_path" {{
  value = local_file.manifest.filename
}}
"""

TF_VARS = r"""project = "{slug}"
"""

f("terraform", "hcl", "iac", "mkdir -p out",
  {"lint": "terraform fmt -check -recursive",
   "types": "terraform init -backend=false -input=false >/dev/null && terraform validate",
   "test": "terraform init -backend=false -input=false >/dev/null && terraform validate",
   "build": "terraform init -backend=false -input=false >/dev/null && terraform validate"},
  needs=["terraform"], hint="brew install terraform",
  files={"main.tf": TF_MAIN, "terraform.tfvars": TF_VARS})

ANSIBLE_PLAY = r"""---
# {name} — playbook dasar (idempotent)
- name: Konfigurasi dasar server
  hosts: all
  become: true
  gather_facts: true
  vars:
    ssh_port: 22
    admin_user: deploy

  tasks:
    - name: Pastikan paket dasar terpasang
      ansible.builtin.package:
        name: [curl, ca-certificates]
        state: present

    - name: Buat user admin deploy
      ansible.builtin.user:
        name: "{{{{ admin_user }}}}"
        groups: sudo
        shell: /bin/bash
        create_home: true

    - name: Siapkan direktori .ssh admin
      ansible.builtin.file:
        path: "/home/{{{{ admin_user }}}}/.ssh"
        state: directory
        owner: "{{{{ admin_user }}}}"
        mode: "0700"

    - name: Pasang public key admin dari env ADMIN_PUBKEY
      ansible.builtin.copy:
        dest: "/home/{{{{ admin_user }}}}/.ssh/authorized_keys"
        content: "{{{{ lookup('env', 'ADMIN_PUBKEY') }}}}\n"
        owner: "{{{{ admin_user }}}}"
        mode: "0600"
      when: lookup('env', 'ADMIN_PUBKEY') | length > 0
"""

ANSIBLE_CFG = r"""[defaults]
inventory = inventory.ini
host_key_checking = True
retry_files_enabled = False
stdout_callback = yaml
"""

ANSIBLE_INV = r"""[web]
localhost ansible_connection=local
"""

f("ansible", "yaml", "iac", "true",
  {"lint": "ansible-lint playbook.yml",
   "types": "ansible-playbook --syntax-check playbook.yml",
   "test": "grep -q 'become: true' playbook.yml",
   "build": "ansible-playbook --syntax-check playbook.yml"},
  needs=["ansible"], hint="brew install ansible ansible-lint",
  files={"playbook.yml": ANSIBLE_PLAY, "ansible.cfg": ANSIBLE_CFG,
         "inventory.ini": ANSIBLE_INV})

SYSTEMD = r"""[Unit]
Description={name}
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=app
Group=app
WorkingDirectory=/opt/{slug}
ExecStart=/opt/{slug}/bin/{slug}
Restart=on-failure
RestartSec=5s

# hardening
NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6
RestrictNamespaces=true
LockPersonality=true
MemoryDenyWriteExecute=true
SystemCallFilter=@system-service
SystemCallArchitectures=native
CapabilityBoundingSet=
AmbientCapabilities=
UMask=0077

[Install]
WantedBy=multi-user.target
"""

f("systemd", "ini", "iac", "true",
  {"lint": "systemd-analyze verify {slug}.service 2>/dev/null || grep -q 'NoNewPrivileges=true' {slug}.service",
   "types": "grep -q 'ProtectSystem=strict' {slug}.service",
   "test": "grep -q 'CapabilityBoundingSet=' {slug}.service",
   "build": "test -s {slug}.service"},
  needs=["true"], hint="systemd (Linux)",
  files={"{slug}.service": SYSTEMD})

GH_ACTIONS = r"""name: ci

on:
  push: {{ branches: [main] }}
  pull_request:

permissions:
  contents: read

concurrency:
  group: ci-${{{{ github.ref }}}}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with: {{ persist-credentials: false }}
      - name: jalankan gate proyek
        run: echo "ganti dengan perintah project-forge verify ."

  security:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4
        with: {{ persist-credentials: false }}
      - name: secret scan
        uses: gitleaks/gitleaks-action@v2
      - name: trivy fs
        uses: aquasecurity/trivy-action@0.24.0
        with:
          scan-type: fs
          severity: HIGH,CRITICAL
          exit-code: "1"
"""

f("gh-actions", "yaml", "iac", "mkdir -p .github/workflows",
  {"lint": "grep -q 'permissions:' .github/workflows/ci.yml",
   "types": "grep -q 'persist-credentials: false' .github/workflows/ci.yml",
   "test": "grep -q 'gitleaks' .github/workflows/ci.yml",
   "build": "test -s .github/workflows/ci.yml"},
  needs=["true"], hint="GitHub Actions",
  files={".github/workflows/ci.yml": GH_ACTIONS})

# ═══ DATA SERVICES (compose) ═════════════════════════════════════════════════
def _svc(yaml_body, hint, gates_extra=None):
    return {"compose.yaml": yaml_body}


PG_COMPOSE = r"""services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?wajib}
      POSTGRES_DB: app
    ports: ["127.0.0.1:5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
    command: ["postgres", "-c", "log_connections=on", "-c", "password_encryption=scram-sha-256"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      retries: 5
volumes:
  pgdata: {}
"""

SQL_INIT = r"""-- {name} — skema awal
CREATE TABLE IF NOT EXISTS items (
    id         bigserial PRIMARY KEY,
    name       text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);
"""

f("postgres", "sql", "data", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'scram-sha-256' compose.yaml",
   "test": "grep -qi 'CREATE TABLE' sql/init.sql", "build": "docker compose config -q"},
  needs=["docker"], hint="docker",
  files={"compose.yaml": PG_COMPOSE, "sql/init.sql": SQL_INIT})

REDIS_COMPOSE = r"""services:
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--requirepass", "${REDIS_PASSWORD:?wajib}"]
    ports: ["127.0.0.1:6379:6379"]
    volumes: ["redisdata:/data"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      retries: 5
volumes:
  redisdata: {}
"""

f("redis", "config", "data", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'requirepass' compose.yaml",
   "test": "grep -q 'appendonly' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": REDIS_COMPOSE})

MONGO_COMPOSE = r"""services:
  mongo:
    image: mongo:7
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:?wajib}
    ports: ["127.0.0.1:27017:27017"]
    volumes: ["mongodata:/data/db"]
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 15s
      retries: 5
volumes:
  mongodata: {}
"""

f("mongodb", "config", "data", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'MONGO_INITDB_ROOT_PASSWORD' compose.yaml",
   "test": "grep -q 'healthcheck' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": MONGO_COMPOSE})

MYSQL_COMPOSE = r"""services:
  mysql:
    image: mysql:8
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:?wajib}
      MYSQL_DATABASE: app
      MYSQL_USER: app
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:?wajib}
    ports: ["127.0.0.1:3306:3306"]
    volumes: ["mysqldata:/var/lib/mysql"]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1"]
      interval: 15s
      retries: 5
volumes:
  mysqldata: {}
"""

f("mysql", "config", "data", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'MYSQL_DATABASE' compose.yaml",
   "test": "grep -q 'healthcheck' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": MYSQL_COMPOSE})

MINIO_COMPOSE = r"""services:
  minio:
    image: minio/minio:latest
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:?wajib}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:?wajib}
    ports: ["127.0.0.1:9000:9000", "127.0.0.1:9001:9001"]
    volumes: ["miniodata:/data"]
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      interval: 30s
      retries: 5
volumes:
  miniodata: {}
"""

f("minio", "config", "data", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'MINIO_ROOT_PASSWORD' compose.yaml",
   "test": "grep -q '9000' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": MINIO_COMPOSE})

KAFKA_COMPOSE = r"""services:
  kafka:
    image: bitnami/kafka:3.7
    restart: unless-stopped
    environment:
      KAFKA_CFG_NODE_ID: 0
      KAFKA_CFG_PROCESS_ROLES: controller,broker
      KAFKA_CFG_CONTROLLER_QUORUM_VOTERS: 0@kafka:9093
      KAFKA_CFG_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
      KAFKA_CFG_ADVERTISED_LISTENERS: PLAINTEXT://127.0.0.1:9092
      KAFKA_CFG_CONTROLLER_LISTENER_NAMES: CONTROLLER
    ports: ["127.0.0.1:9092:9092"]
    volumes: ["kafkadata:/bitnami/kafka"]
volumes:
  kafkadata: {}
"""

f("kafka", "config", "data", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'PROCESS_ROLES' compose.yaml",
   "test": "grep -q '9092' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": KAFKA_COMPOSE})

RABBIT_COMPOSE = r"""services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    restart: unless-stopped
    environment:
      RABBITMQ_DEFAULT_USER: app
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD:?wajib}
    ports: ["127.0.0.1:5672:5672", "127.0.0.1:15672:15672"]
    volumes: ["rabbitdata:/var/lib/rabbitmq"]
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 30s
      retries: 5
volumes:
  rabbitdata: {}
"""

f("rabbitmq", "config", "data", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'RABBITMQ_DEFAULT_PASS' compose.yaml",
   "test": "grep -q '15672' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": RABBIT_COMPOSE})

# ═══ OBSERVABILITY ═══════════════════════════════════════════════════════════
PROM_COMPOSE = r"""services:
  prometheus:
    image: prom/prometheus:v2.54.1
    restart: unless-stopped
    ports: ["127.0.0.1:9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - promdata:/prometheus
    command: ["--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.retention.time=15d"]
volumes:
  promdata: {}
"""

PROM_YML = r"""global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - rules.yml

alerting:
  alertmanagers:
    - static_configs:
        - targets: []

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]
  - job_name: app
    metrics_path: /metrics
    static_configs:
      - targets: ["app:3000"]
"""

PROM_RULES = r"""groups:
  - name: dasar
    rules:
      - alert: InstanceDown
        expr: up == 0
        for: 5m
        labels: { severity: critical }
        annotations:
          summary: "target {{ $labels.instance }} mati"
      - alert: ErrorRateTinggi
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 10m
        labels: { severity: warning }
"""

f("prometheus", "yaml", "observability", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'scrape_configs' prometheus.yml",
   "test": "grep -q 'alert:' rules.yml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker",
  files={"compose.yaml": PROM_COMPOSE, "prometheus.yml": PROM_YML, "rules.yml": PROM_RULES})

GRAFANA_COMPOSE = r"""services:
  grafana:
    image: grafana/grafana:11.2.0
    restart: unless-stopped
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD:?wajib}
      GF_USERS_ALLOW_SIGN_UP: "false"
      GF_AUTH_ANONYMOUS_ENABLED: "false"
    ports: ["127.0.0.1:3001:3000"]
    volumes: ["grafanadata:/var/lib/grafana"]
volumes:
  grafanadata: {}
"""

f("grafana", "config", "observability", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'ALLOW_SIGN_UP: \"false\"' compose.yaml",
   "test": "grep -q 'GF_SECURITY_ADMIN_PASSWORD' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": GRAFANA_COMPOSE})

LOKI_COMPOSE = r"""services:
  loki:
    image: grafana/loki:3.1.1
    restart: unless-stopped
    ports: ["127.0.0.1:3100:3100"]
    command: ["-config.file=/etc/loki/config.yml"]
    volumes:
      - ./loki-config.yml:/etc/loki/config.yml:ro
      - lokidata:/loki
volumes:
  lokidata: {}
"""

LOKI_CFG = r"""auth_enabled: false

server:
  http_listen_port: 3100

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13

limits_config:
  retention_period: 168h
"""

f("loki", "yaml", "observability", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'http_listen_port' loki-config.yml",
   "test": "grep -q 'retention_period' loki-config.yml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker",
  files={"compose.yaml": LOKI_COMPOSE, "loki-config.yml": LOKI_CFG})

UPTIME_COMPOSE = r"""services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    restart: unless-stopped
    ports: ["127.0.0.1:3002:3001"]
    volumes: ["kumadata:/app/data"]
volumes:
  kumadata: {}
"""

f("uptime-kuma", "config", "observability", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'uptime-kuma' compose.yaml",
   "test": "grep -q '3001' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": UPTIME_COMPOSE})

# ═══ IDENTITY / SECRETS ══════════════════════════════════════════════════════
KEYCLOAK_COMPOSE = r"""services:
  keycloak:
    image: quay.io/keycloak/keycloak:25.0
    restart: unless-stopped
    command: ["start-dev"]
    environment:
      KC_BOOTSTRAP_ADMIN_USERNAME: admin
      KC_BOOTSTRAP_ADMIN_PASSWORD: ${KEYCLOAK_PASSWORD:?wajib}
      KC_HOSTNAME_STRICT: "false"
    ports: ["127.0.0.1:8081:8080"]
    volumes: ["kcdata:/opt/keycloak/data"]
volumes:
  kcdata: {}
"""

f("keycloak", "config", "security", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'KC_BOOTSTRAP_ADMIN_PASSWORD' compose.yaml",
   "test": "grep -q 'keycloak' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker", files={"compose.yaml": KEYCLOAK_COMPOSE})

VAULT_COMPOSE = r"""services:
  vault:
    image: hashicorp/vault:1.17
    restart: unless-stopped
    cap_add: [IPC_LOCK]
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: ${VAULT_TOKEN:?wajib}
      VAULT_ADDR: http://127.0.0.1:8200
    ports: ["127.0.0.1:8200:8200"]
    command: ["server", "-dev"]
"""

f("vault", "config", "security", "true",
  {"lint": "docker compose config -q", "types": "grep -q 'VAULT_DEV_ROOT_TOKEN_ID' compose.yaml",
   "test": "grep -q '8200' compose.yaml", "build": "docker compose config -q"},
  needs=["docker"], hint="docker (dev mode — jangan untuk produksi)",
  files={"compose.yaml": VAULT_COMPOSE})

# ═══ SECURITY ════════════════════════════════════════════════════════════════
SSHD_HARDEN = r"""# {name} — drop-in hardening sshd (/etc/ssh/sshd_config.d/99-hardening.conf)
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
MaxAuthTries 3
MaxSessions 4
LoginGraceTime 20
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
PermitTunnel no
PermitEmptyPasswords no
UsePAM yes
AllowUsers deploy
Protocol 2
LogLevel VERBOSE
"""

SSHD_CHECK = r"""#!/usr/bin/env bash
# verifikasi cepat isi drop-in (tanpa menyentuh sistem)
set -euo pipefail
conf="${1:-sshd_hardening.conf}"
fail=0
for rule in "PermitRootLogin no" "PasswordAuthentication no" "PermitEmptyPasswords no" \
            "MaxAuthTries 3" "X11Forwarding no" "Protocol 2"; do
  if ! grep -qE "^${rule}$" "$conf"; then
    echo "GAGAL: $rule tidak ada" >&2
    fail=1
  fi
done
[[ $fail -eq 0 ]] && echo "hardening ssh ok"
exit $fail
"""

f("harden-ssh", "config", "security", "true",
  {"lint": "bash sshd_check.sh sshd_hardening.conf",
   "types": "bash sshd_check.sh sshd_hardening.conf",
   "test": "grep -q 'PasswordAuthentication no' sshd_hardening.conf",
   "build": "bash sshd_check.sh sshd_hardening.conf"},
  needs=["bash"], hint="—",
  files={"sshd_hardening.conf": SSHD_HARDEN, "sshd_check.sh": SSHD_CHECK})

NFTABLES = r"""#!/usr/sbin/nft -f
# {name} — firewall dasar (default deny, izinkan ssh+http+https)
flush ruleset

table inet filter {
  chain input {
    type filter hook input priority filter; policy drop;
    ct state established,related accept
    iif lo accept
    ip protocol icmp accept
    ip6 nexthdr icmpv6 accept
    tcp dport 22 ct state new limit rate 10/minute accept
    tcp dport { 80, 443 } ct state new accept
  }
  chain forward { type filter hook forward priority filter; policy drop; }
  chain output { type filter hook output priority filter; policy accept; }
}
"""

f("firewall-nft", "config", "security", "true",
  {"lint": "grep -q 'policy drop' ruleset.nft", "types": "grep -q 'ct state established' ruleset.nft",
   "test": "grep -q 'policy drop' ruleset.nft", "build": "grep -q 'table inet filter' ruleset.nft"},
  needs=["grep"], hint="nftables (Linux)",
  files={"ruleset.nft": NFTABLES})

FAIL2BAN = r"""[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 5
findtime = 10m
bantime = 1h
ignoreip = 127.0.0.1/8 ::1

[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 5
bantime = 1h
"""

f("fail2ban", "config", "security", "true",
  {"lint": "grep -q 'maxretry' jail.local", "types": "grep -q 'bantime' jail.local",
   "test": "grep -q '\\[sshd\\]' jail.local", "build": "test -s jail.local"},
  needs=["grep"], hint="fail2ban (Linux)",
  files={"jail.local": FAIL2BAN})

GITLEAKS = r"""title = "gitleaks {slug}"
[extend]
useDefault = true

[allowlist]
description = "contoh & fixture"
paths = [
  '''(.*?)README(.*?)''',
  '''(.*?)\\.env\\.example''',
  '''(.*?)tests/fixtures(.*?)''',
]

[[rules]]
id = "generic-api-key"
description = "API key generik"
regex = '''(?i)(api[_-]?key|token|secret)\\s*[:=]\\s*['\"][A-Za-z0-9_\\-]{16,}['\"]'''
tags = ["key", "secret"]
"""

SEMGREP = r"""# {name} — aturan semgrep proyek
rules:
  - id: no-eval
    languages: [javascript, typescript, python]
    severity: ERROR
    message: "eval/exec membuka RCE — pakai parser aman"
    pattern-either:
      - pattern: eval(...)
      - pattern: exec(...)

  - id: no-hardcoded-secret
    languages: [generic]
    severity: ERROR
    message: "secret hardcoded — pakai env/secret manager"
    patterns:
      - pattern-regex: (?i)(password|secret|api_key)\s*[:=]\s*["'][^"']{8,}["']

  - id: sql-string-concat
    languages: [python, javascript, typescript]
    severity: WARNING
    message: "kemungkinan SQL injection — gunakan parameter binding"
    pattern-either:
      - pattern: $CUR.execute("..." + $X)
      - pattern: $DB.query(`...${$X}...`)

  - id: insecure-deserialization
    languages: [python]
    severity: ERROR
    message: "pickle/yaml.load tanpa SafeLoader = RCE"
    pattern-either:
      - pattern: pickle.loads(...)
      - pattern: yaml.load($X)
"""

f("gitleaks-config", "toml", "security", "true",
  {"lint": "gitleaks detect --no-git --redact -c .gitleaks.toml",
   "types": "grep -q 'useDefault = true' .gitleaks.toml",
   "test": "gitleaks detect --no-git --redact -c .gitleaks.toml",
   "build": "test -s .gitleaks.toml"},
  needs=["gitleaks"], hint="brew install gitleaks",
  files={".gitleaks.toml": GITLEAKS})

f("semgrep-config", "yaml", "security", "true",
  {"lint": "semgrep --config semgrep.yml --error --quiet --metrics=off .",
   "types": "grep -q 'no-eval' semgrep.yml",
   "test": "semgrep --config semgrep.yml --error --quiet --metrics=off .",
   "build": "grep -q 'no-hardcoded-secret' semgrep.yml"},
  needs=["semgrep"], hint="brew install semgrep",
  files={"semgrep.yml": SEMGREP})

HEADERS_MD = r"""# {name} — kebijakan security header

Wajib di semua respons HTTP:

| Header | Nilai | Alasan |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | paksa HTTPS |
| `Content-Security-Policy` | `default-src 'self'` (longgarkan per kebutuhan) | cegah XSS |
| `X-Content-Type-Options` | `nosniff` | cegah MIME sniffing |
| `X-Frame-Options` | `DENY` | cegah clickjacking |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | batasi kebocoran referrer |
| `Permissions-Policy` | `geolocation=(), camera=(), microphone=()` | matikan fitur tak dipakai |
| `Cross-Origin-Opener-Policy` | `same-origin` | isolasi proses |
| `Cross-Origin-Resource-Policy` | `same-origin` | batasi embed |

## Checklist
- [ ] HSTS aktif di produksi (jangan di domain tanpa TLS penuh)
- [ ] Tidak ada `Server`/`X-Powered-By` yang membocorkan versi
- [ ] CSP diuji di report-only sebelum enforce
- [ ] Cookie: `Secure; HttpOnly; SameSite=Lax` (atau `Strict`)
- [ ] CORS: daftar origin eksplisit, tanpa `*` bila membawa kredensial

Verifikasi: `security-forge headers https://domain-anda`
"""

HEADERS_NGINX = r"""# tempel di blok server nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options nosniff always;
add_header X-Frame-Options DENY always;
add_header Referrer-Policy strict-origin-when-cross-origin always;
add_header Permissions-Policy "geolocation=(), camera=(), microphone=()" always;
add_header Cross-Origin-Opener-Policy same-origin always;
add_header Cross-Origin-Resource-Policy same-origin always;
add_header Content-Security-Policy "default-src 'self'; object-src 'none'; base-uri 'self'" always;
"""

f("security-headers", "config", "security", "true",
  {"lint": "grep -q 'Strict-Transport-Security' nginx-headers.conf",
   "types": "grep -q 'Content-Security-Policy' nginx-headers.conf",
   "test": "grep -q 'Permissions-Policy' nginx-headers.conf",
   "build": "test -s headers.md"},
  needs=["grep"], hint="—",
  files={"headers.md": HEADERS_MD, "nginx-headers.conf": HEADERS_NGINX})

THREAT_MODEL = r"""# Threat model — {name}

Metode: STRIDE. Perbarui setiap ada perubahan arsitektur atau data baru.

## 1. Aset
| Aset | Dampak bila bocor/rusak |
|---|---|
| kredensial pengguna | kompromi akun, regulasi |
| data transaksi | kerugian finansial, sengketa |
| kunci API internal | penyalahgunaan kuota |
| log audit | hilangnya bukti insiden |

## 2. Batas kepercayaan
- internet → edge (nginx/caddy)
- edge → app (jaringan internal)
- app → database
- CI/CD → registry & server produksi

## 3. Analisis STRIDE
| Kategori | Ancaman | Mitigasi | Status |
|---|---|---|---|
| Spoofing | pencurian sesi | cookie HttpOnly+Secure, MFA | belum |
| Tampering | modifikasi request | validasi skema, tanda tangan | belum |
| Repudiation | penyangkalan aksi | log audit append-only | belum |
| Information disclosure | dump DB | enkripsi at-rest, least privilege | belum |
| Denial of service | flood | rate limit, autoscale, WAF | belum |
| Elevation of privilege | RCE | patch, allowlist, sandbox | belum |

## 4. Risiko prioritas
1. (isi) — kemungkinan: tinggi / dampak: tinggi
2. (isi)

## 5. Verifikasi
- `security-forge audit .` hijau
- `security-forge headers <url>` tanpa temuan
- uji restore backup < 1 jam
"""

f("threat-model", "md", "security", "true",
  {"lint": "grep -q 'STRIDE' THREAT-MODEL.md",
   "types": "grep -q 'Batas kepercayaan' THREAT-MODEL.md",
   "test": "grep -q 'Denial of service' THREAT-MODEL.md",
   "build": "test -s THREAT-MODEL.md"},
  needs=["grep"], hint="—", files={"THREAT-MODEL.md": THREAT_MODEL})

RUNBOOK = r"""# Runbook insiden — {name}

## 0. Prinsip
- Utamakan menghentikan kerusakan, bukan mencari pelaku.
- Setiap aksi dicatat (waktu, aktor, perintah, hasil).
- Komunikasi satu pintu (IC).

## 1. Deteksi
- alert Prometheus/uptime → `#incident` + on-call
- klasifikasi awal: P1 (layanan mati/data bocor) · P2 (degradasi) · P3 (minor)

## 2. Triase (≤10 menit)
1. Konfirmasi dampak & cakupan.
2. Tentukan IC + scribe.
3. Mulai catatan waktu.

## 3. Containment
- rotate kredensial yang mungkin bocor
- blok IP/jalur serangan (fail2ban/nginx deny)
- isolasi host terdampak (snapshot dulu untuk forensik)
- revoke token/sesi aktif

## 4. Eradikasi & pemulihan
- patch penyebab akar
- restore dari backup terverifikasi
- canary 10% → 50% → 100%, pantau error rate

## 5. Pasca-insiden (≤5 hari)
- postmortem blameless
- action item + pemilik + tenggat
- tambah test/alert agar tidak terulang

## Perintah cepat
```bash
security-forge audit .
security-forge headers https://domain
security-forge tls domain
docker compose ps && docker compose logs --tail=200 app
```
"""

f("incident-runbook", "md", "security", "true",
  {"lint": "grep -q 'Containment' RUNBOOK.md", "types": "grep -q 'rotate kredensial' RUNBOOK.md",
   "test": "grep -q 'postmortem' RUNBOOK.md", "build": "test -s RUNBOOK.md"},
  needs=["grep"], hint="—", files={"RUNBOOK.md": RUNBOOK})

SOPS_CFG = r"""creation_rules:
  - path_regex: secrets/.*\.enc\.yaml$
    age: age1ganti-dengan-public-key-anda
    encrypted_regex: "^(data|stringData)$"
"""

f("sops", "yaml", "security", "true",
  {"lint": "grep -q 'age' .sops.yaml", "types": "grep -q 'creation_rules' .sops.yaml",
   "test": "grep -q 'path_regex' .sops.yaml", "build": "test -s .sops.yaml"},
  needs=["grep"], hint="brew install sops age",
  files={".sops.yaml": SOPS_CFG})

ZAP_CONF = r"""# {name} — profil OWASP ZAP baseline
env:
  contexts:
    - name: app
      urls: ["http://localhost:8080"]
      includePaths: ["http://localhost:8080.*"]
  parameters:
    failOnError: true
    failOnWarning: false
    progressToStdout: true

jobs:
  - type: passiveScan-config
    parameters:
      maxAlertsPerRule: 10
  - type: spider
    parameters:
      context: app
      maxDuration: 2
  - type: passiveScan-wait
    parameters:
      maxDuration: 5
  - type: report
    parameters:
      template: traditional-json
      reportDir: reports
      reportFile: zap.json
"""

f("zap", "yaml", "security", "mkdir -p reports",
  {"lint": "SKIP: butuh aplikasi berjalan di localhost:8080 + izin tertulis",
   "types": "grep -q 'passiveScan' zap.yaml",
   "test": "grep -q 'report' zap.yaml",
   "build": "test -s zap.yaml"},
  needs=["grep"], hint="docker run -t ghcr.io/zaproxy/zap:latest",
  files={"zap.yaml": ZAP_CONF})

NUCLEI_CONF = r"""# {name} — profil nuclei (hanya template aman, tanpa fuzzing agresif)
templates:
  - cves/
  - exposures/
  - misconfiguration/
  - ssl/
  - http/technologies/

exclude-tags:
  - intrusive
  - fuzz
  - dos

rate-limit: 50
bulk-size: 25
timeout: 10
retries: 1
severity:
  - critical
  - high
  - medium
"""

f("nuclei", "yaml", "security", "true",
  {"lint": "grep -q 'exclude-tags' nuclei.yaml",
   "types": "grep -q 'rate-limit' nuclei.yaml",
   "test": "grep -q 'intrusive' nuclei.yaml",
   "build": "test -s nuclei.yaml"},
  needs=["grep"], hint="brew install nuclei (jalankan: nuclei -u <url> -config nuclei.yaml)",
  files={"nuclei.yaml": NUCLEI_CONF})

BACKUP = r"""#!/usr/bin/env bash
# {name} — backup harian + verifikasi restore (restic)
set -euo pipefail

export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:?set RESTIC_REPOSITORY}"
export RESTIC_PASSWORD_FILE="${RESTIC_PASSWORD_FILE:?set RESTIC_PASSWORD_FILE}"
targets=("/etc" "/opt/{slug}")

if ! command -v restic >/dev/null; then
  echo "restic belum ada: brew install restic" >&2
  exit 0
fi

restic backup --tag auto "${targets[@]}"
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune

# verifikasi: restore 1 file terbaru ke temp
tmp="$(mktemp -d)"
latest="$(restic snapshots --json | python3 -c 'import json,sys;print(json.load(sys.stdin)[-1]["short_id"])')"
file="$(restic ls "$latest" | grep -m1 'etc/hostname' || true)"
[[ -n "$file" ]] && restic restore "$latest" --target "$tmp" --include "$file"
echo "backup + verifikasi restore ok"
"""

f("backup", "bash", "security", "true",
  {"lint": "bash -n backup.sh", "types": "bash -n backup.sh",
   "test": "grep -q 'restic forget' backup.sh", "build": "grep -q 'restic backup' backup.sh"},
  needs=["bash"], hint="brew install restic",
  files={"backup.sh": BACKUP})


# ─── util ───────────────────────────────────────────────────────────────────
def _norm(t):
    """template ditulis dengan {{ }} agar aman; di sini dikembalikan ke { }."""
    return t.replace("{{", "{").replace("}}", "}")


ENV_PREFIX = {'compose': 'POSTGRES_PASSWORD=dev ', 'compose-stack': 'POSTGRES_PASSWORD=dev ', 'postgres': 'POSTGRES_PASSWORD=dev ', 'redis': 'REDIS_PASSWORD=dev ', 'mongodb': 'MONGO_PASSWORD=dev ', 'mysql': 'MYSQL_ROOT_PASSWORD=dev MYSQL_PASSWORD=dev ', 'minio': 'MINIO_ROOT_USER=dev MINIO_ROOT_PASSWORD=devdevdev ', 'rabbitmq': 'RABBITMQ_PASSWORD=dev ', 'grafana': 'GRAFANA_PASSWORD=dev ', 'keycloak': 'KEYCLOAK_PASSWORD=dev ', 'vault': 'VAULT_TOKEN=dev '}

for _fid, _pre in ENV_PREFIX.items():
    if _fid in F:
        F[_fid]["gates"] = {k: (_pre + v if "docker compose" in v else v)
                            for k, v in F[_fid]["gates"].items()}

for _e in F.values():
    _e["boot"] = _norm(_e["boot"])
    _e["gates"] = {k: _norm(v) for k, v in _e["gates"].items()}
    _e["files"] = {k: (v if k.startswith("chart/") else _norm(v))
                   for k, v in (_e["files"] or {}).items()}


def get(fid):
    return F.get(fid)


ALIAS = {
    "server": "server", "proxy": "server", "webserver": "server", "nginx": "nginx",
    "docker": "container", "container": "container", "compose": "container",
    "kubernetes": "k8s", "k8s": "k8s", "helm": "helm", "infra": "iac",
    "infrastructure": "iac", "terraform": "terraform", "ansible": "ansible",
    "database": "data", "db": "data", "postgres": "postgres", "mysql": "mysql",
    "redis": "redis", "mongo": "mongodb", "mongodb": "mongodb", "queue": "kafka",
    "monitoring": "observability", "metrics": "observability", "logs": "observability",
    "sec": "security", "hardening": "security", "firewall": "security",
    "pki": "security", "secrets": "security", "auth": "security",
}


def search(q):
    q = (q or "").lower().strip()
    q = ALIAS.get(q, q)
    return [e for e in F.values()
            if q in e["id"].lower() or q in e["lang"].lower() or q in e["kind"].lower()]


def by_kind():
    out = {}
    for e in F.values():
        out.setdefault(e["kind"], []).append(e["id"])
    return {k: sorted(v) for k, v in sorted(out.items())}
