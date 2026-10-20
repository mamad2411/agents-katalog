---
name: docker-kubernetes
description: Docker and Kubernetes standards — Dockerfile optimization, multi-stage builds, Docker Compose, Kubernetes manifests, helm charts
globs: ["**/Dockerfile*", "**/*.dockerfile", "**/docker-compose*.yml", "**/*.yaml", "**/*.yml", "**/.dockerignore"]
alwaysApply: false
---

# Docker & Kubernetes Standards

Docker containerizes applications for consistency. Kubernetes orchestrates containers at scale. Master both for reliable deployments.

---

## Dockerfile Best Practices

**ALWAYS**:
- Use multi-stage builds (reduce image size)
- Use specific base image versions (not `latest`)
- Minimize layers (combine RUN commands with &&)
- Order layers by change frequency (dependencies first, code last)
- Use .dockerignore to exclude unnecessary files
- Run as non-root user (security)
- Set health check (docker/k8s probes)
- Add metadata (LABEL, MAINTAINER)

**NEVER**:
- Use `FROM latest` (breaks reproducibility)
- Create large images (> 500MB is suspicious)
- Run as root
- Skip .dockerignore (includes unnecessary files)

### ✅ GOOD Dockerfile Pattern

```dockerfile
# Multi-stage build: separate builder + runtime
FROM node:18-alpine AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci --only=prod && npm cache clean --force

# Test stage (optional)
FROM node:18-alpine AS test
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run test

# Runtime stage (smaller image)
FROM node:18-alpine
WORKDIR /app

# Metadata
LABEL maintainer="team@example.com"
LABEL version="1.0.0"

# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

# Copy dependencies from builder
COPY --from=builder /build/node_modules ./node_modules
COPY package*.json ./

# Copy application (after dependencies for better caching)
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (res) => {if (res.statusCode !== 200) throw new Error(res.statusCode)})"

# Run as nodejs user (not root)
USER nodejs

# Expose port
EXPOSE 3000

# Start application
CMD ["node", "src/index.js"]
```

### ❌ BAD Dockerfile Pattern

```dockerfile
# ❌ Latest version — not reproducible
FROM node:latest

# ❌ Install unnecessary dependencies
RUN apt-get update && apt-get install -y curl wget vim git

# ❌ Large image — all dev dependencies included
COPY package*.json ./
RUN npm install

# ❌ Run as root
RUN npm start

# ❌ No health check
EXPOSE 3000
CMD ["npm", "start"]
```

---

## Docker Compose

**ALWAYS**:
- Use version 3.8+ (latest features)
- Define services (app, database, cache, etc.)
- Use named volumes for persistent data
- Set environment variables for configuration
- Use networks for service-to-service communication
- Set resource limits (memory, CPU)
- Define health checks
- Use .env files for secrets (don't commit)

**NEVER**:
- Commit .env files with secrets
- Skip restart policies
- Use localhost (use service names for networking)

### ✅ GOOD Docker Compose

```yaml
# docker-compose.yml — Multi-service development environment
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: app-dev
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: development
      DB_HOST: postgres  # Service name
      DB_PORT: 5432
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./src:/app/src  # Code hot-reload
      - ./node_modules:/app/node_modules
    networks:
      - backend
    restart: unless-stopped
    resources:
      limits:
        cpus: '0.5'
        memory: 512M

  postgres:
    image: postgres:15-alpine
    container_name: postgres-dev
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./migrations:/docker-entrypoint-initdb.d
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: redis-dev
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:1.24-alpine
    container_name: nginx-dev
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  backend:
    driver: bridge

# .env file (don't commit!)
# DB_PASSWORD=secure_password_here
# API_KEY=secret_key_here
```

---

## Kubernetes Manifests

**ALWAYS**:
- Use Deployments (not bare Pods)
- Define resource requests + limits (CPU, memory)
- Set liveness + readiness probes (health checks)
- Use Services for networking
- Use ConfigMaps for configuration
- Use Secrets for sensitive data
- Set appropriate replicas (3+ for production)
- Use namespaces for isolation

**NEVER**:
- Store secrets in ConfigMaps (use Secrets)
- Run as root (set securityContext)
- Skip resource limits (causes node pressure)

### ✅ GOOD Kubernetes Manifests

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production

---
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  DB_HOST: "postgres-service"
  DB_PORT: "5432"

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
stringData:
  DB_PASSWORD: "secure-password"
  API_KEY: "secret-key"

---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: production
spec:
  replicas: 3  # High availability
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
        version: v1
    spec:
      # Security: non-root user
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001

      containers:
      - name: app
        image: myregistry.azurecr.io/app:1.0.0  # Specific version
        imagePullPolicy: IfNotPresent
        
        ports:
        - containerPort: 3000
          name: http
        
        # Environment variables
        env:
        - name: NODE_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: NODE_ENV
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_PASSWORD
        
        # Health checks
        livenessProbe:  # Restart if unhealthy
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        
        readinessProbe:  # Remove from traffic if not ready
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        # Resource management
        resources:
          requests:
            cpu: 100m      # Minimum CPU
            memory: 128Mi  # Minimum memory
          limits:
            cpu: 500m      # Maximum CPU
            memory: 512Mi  # Maximum memory
        
        # Volume mounts
        volumeMounts:
        - name: logs
          mountPath: /var/log/app
      
      # Volumes
      volumes:
      - name: logs
        emptyDir: {}
      
      # Pod disruption budget (survive node failures)
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - app
              topologyKey: kubernetes.io/hostname

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: production
spec:
  selector:
    app: app
  type: ClusterIP  # Internal only
  ports:
  - port: 80
    targetPort: 3000
    protocol: TCP
    name: http

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
  tls:
  - hosts:
    - api.example.com
    secretName: app-tls-cert

---
# hpa.yaml (Auto-scaling)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Scale up at 70% CPU
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80  # Scale up at 80% memory
```

---

## Helm Charts

**ALWAYS**:
- Use Helm for templating complex deployments
- Version your charts (semantic versioning)
- Provide sensible defaults in values.yaml
- Document configuration options
- Use values for all configurable aspects
- Sign charts (chart signing)
- Version application in values

**NEVER**:
- Hardcode values in templates
- Skip values validation

### ✅ GOOD Helm Chart Structure

```yaml
# Chart.yaml
apiVersion: v2
name: myapp
description: A production-ready application
version: 1.0.0          # Chart version
appVersion: "1.0.0"     # Application version
maintainers:
  - name: Team
    email: team@example.com

---
# values.yaml
replicaCount: 3

image:
  registry: myregistry.azurecr.io
  name: app
  tag: "1.0.0"
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

# Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 3000

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  hostname: api.example.com
  tls:
    enabled: true
    issuer: letsencrypt-prod

# Auto-scaling
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilization: 70

# Configuration
config:
  nodeEnv: production
  logLevel: info

# Secrets (provide via --set or external secret)
secrets:
  dbPassword: ""
  apiKey: ""

---
# templates/deployment.yaml
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
        image: "{{ .Values.image.registry }}/{{ .Values.image.name }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: {{ .Values.service.targetPort }}
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        env:
        - name: NODE_ENV
          value: {{ .Values.config.nodeEnv }}
        livenessProbe:
          httpGet:
            path: /health
            port: {{ .Values.service.targetPort }}
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: {{ .Values.service.targetPort }}
          initialDelaySeconds: 10
```

---

## Docker & Kubernetes Security Checklist

- [ ] Dockerfile: Non-root user, minimal base image, multi-stage build
- [ ] Docker Compose: Named volumes, networks, resource limits, health checks
- [ ] Kubernetes: Resource limits/requests, security context, RBAC
- [ ] Probes: Liveness check, readiness check, appropriate timeouts
- [ ] ConfigMaps: All non-secret config externalized
- [ ] Secrets: All sensitive data in Secrets (not ConfigMaps), RBAC-protected
- [ ] Networking: Service-to-service via DNS, NetworkPolicies for isolation
- [ ] Scaling: HPA configured, pod disruption budgets set
- [ ] Monitoring: Prometheus metrics, pod status monitoring
- [ ] Image security: Signed images, private registry, vulnerability scanning

---

## Summary

Good containerization & orchestration:
1. **Efficient images** — Multi-stage builds, minimal size, non-root
2. **Compose for dev** — Services, volumes, networks, health checks
3. **Kubernetes for prod** — Deployments, probes, scaling, networking
4. **Security-first** — No root, resource limits, encrypted secrets
5. **Observable** — Health checks, metrics, logging
6. **Reliable** — Multiple replicas, auto-scaling, disruption budgets

Master Docker for development and Kubernetes for production scale.
