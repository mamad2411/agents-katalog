---
name: mig-containerize
description: Containerize applications for OpenShift using Red Hat UBI images. Use when the user wants to containerize code, deploy to OpenShift, create Dockerfiles, or migrate applications to containers. Triggers on phrases like "containerize this", "create Dockerfile", "deploy to OpenShift", "move to containers", "build container image", or any mention of Docker/Podman/OpenShift deployment. Requires the codebase to be indexed with rgctl first.
---

# Application Containerization with Red Hat UBI

This skill containerizes applications for OpenShift using Red Hat Universal Base Images (UBI), with full security hardening and deployment manifest generation. It uses rgctl's knowledge graph to intelligently assess containerization readiness and identify platform-specific dependencies.

**rgctl workflow for this skill:** [mig-rgctl/references/workflow.md](../mig-rgctl/references/workflow.md) — section *mig-containerize*

## Prerequisites

**Prerequisite:** Codebase indexed with rgctl via **mig-rgctl**.

1. **Verify index exists** (artifacts at `{repo}/.rgctl/` after `rgctl discover .`):
   ```bash
   rgctl -f json metrics --pagerank
   ```
   If this fails, invoke **mig-rgctl**, run discover with containerization flags (see workflow), then STOP. If the index exists but is stale (`rgctl -f json status`), run `rgctl update` first. After this skill writes Dockerfiles / app-tree files, run `rgctl update` before any further graph queries or the next migration phase.

2. **Verify communities** (required for subsystem → container mapping):
   ```bash
   rgctl -f json communities list
   ```
   If empty, re-run discover with `--with-harmonic` (see mig-rgctl workflow), then STOP.

3. **Artifact note:** Graph artifacts live under `{repo}/.rgctl/`. Legacy `~/.rgctl/cache/` is obsolete — re-run `rgctl discover .` rather than requiring `--no-daemon`.

## When to Use This Skill

Use this skill when you need to:
- Containerize an existing application for OpenShift
- Create production-ready Dockerfiles with Red Hat UBI base images
- Generate OpenShift deployment manifests (Deployment, Service, Route, ConfigMap, Secret)
- Migrate on-premises or bare-metal applications to containers
- Set up local development environments with podman-compose
- Ensure security compliance for containerized workloads

The graph-driven approach identifies platform dependencies, external services, and migration blockers automatically.

## Workflow

### Step 1: Ensure rgctl Index and Communities Exist

Follow [mig-rgctl workflow — mig-containerize](../mig-rgctl/references/workflow.md#mig-containerize--containerization-readiness).

```bash
rgctl -f json metrics --pagerank
rgctl -f json communities list
```

If `metrics` fails → invoke **mig-rgctl**, run:
```bash
rgctl discover . --with-cfg --with-security --with-taint --with-harmonic
```
Then STOP until complete.

If `communities list` is empty → re-discover with `--with-harmonic`, then STOP.

### Step 2: Analyze Graph for Containerization Readiness

Query the graph per [mig-rgctl workflow](../mig-rgctl/references/workflow.md#mig-containerize--containerization-readiness).

**Query graph via mig-rgctl** (features → commands in [workflow.md](../mig-rgctl/references/workflow.md)):
```bash
# Language/framework inventory
rgctl -f json gql "MATCH (n:Function) RETURN n LIMIT 20"

# Hotspots and communities
rgctl -f json metrics --pagerank --communities
rgctl -f json communities list
```

**Analyze for containerization concerns:**

#### 1. Detect Language and Framework

From the graph, identify:
- **Language**: Java, Python, JavaScript/Node.js, Go, Ruby, etc.
- **Framework**: Spring Boot, Django, Flask, Express, Quarkus, etc.
- **Build system**: Maven, Gradle, pip, npm, go mod, etc.

This determines which Red Hat UBI base image to use.

#### 2. Identify External Dependencies

Query the graph for external service dependencies:
```bash
rgctl -f json gql "MATCH (a)-[r:USES|DEPENDSON]->(b) RETURN a,b LIMIT 50"
```

Common patterns to look for:
- **Databases**: PostgreSQL, MySQL, MongoDB, Oracle
- **Caching**: Redis, Memcached
- **Message queues**: RabbitMQ, Kafka, ActiveMQ
- **External APIs**: Payment gateways, email services

For each dependency, decide:
- Deploy as sidecar container (Redis cache)
- Deploy as separate StatefulSet (database with persistent storage)
- Use external managed service (cloud database)
- Mock for local development (podman-compose)

#### 3. Find Platform-Specific Code

Search for containerization blockers:

**File system dependencies** — use semantic search or source grep for hardcoded paths:
```bash
rgctl -f json semantic query "file path upload storage" --limit 10
```

Look for:
- Hardcoded paths (`/var/app/uploads`, `C:\data`, `/opt/legacy`)
- Local file storage (must become PersistentVolumeClaim or object storage)
- Log files written to disk (should use stdout/stderr)
- Temp directories (use `/tmp` or emptyDir volume)

**Configuration files:**
```bash
find . -name "*.properties" -o -name "*.yml" -o -name "*.yaml" -o -name "*.conf" -o -name ".env"
```

Hardcoded configuration must become:
- Environment variables (database URLs, API keys)
- ConfigMaps (application settings)
- Secrets (passwords, tokens, certificates)

**Platform-specific calls:**
- Windows-specific code (won't run in Linux containers)
- OS-specific binaries (must be available in UBI image or installed)
- Localhost assumptions (`localhost` → service names in OpenShift)

#### 4. Assess Build Requirements

From graph + package manifests, identify:
- **Build-time dependencies**: compilers, build tools
- **Runtime dependencies**: libraries, system packages
- **Application artifacts**: JAR files, Python wheels, npm packages

This determines multi-stage build strategy.

### Step 3: Select Red Hat UBI Base Image

Choose the language-specific UBI image based on detected language:

**Java Applications:**
- **JDK 11**: `registry.access.redhat.com/ubi9/openjdk-11:latest`
- **JDK 17**: `registry.access.redhat.com/ubi9/openjdk-17:latest`
- **JDK 21**: `registry.access.redhat.com/ubi9/openjdk-21:latest`

**Python Applications:**
- **Python 3.9**: `registry.access.redhat.com/ubi9/python-39:latest`
- **Python 3.11**: `registry.access.redhat.com/ubi9/python-311:latest`

**Node.js Applications:**
- **Node.js 18**: `registry.access.redhat.com/ubi9/nodejs-18:latest`
- **Node.js 20**: `registry.access.redhat.com/ubi9/nodejs-20:latest`

**Go Applications:**
- **Go 1.20**: `registry.access.redhat.com/ubi9/go-toolset:latest`

**Generic Base:**
- **Minimal UBI**: `registry.access.redhat.com/ubi9/ubi-minimal:latest` (for static binaries)
- **Standard UBI**: `registry.access.redhat.com/ubi9/ubi:latest` (for custom builds)

**Selection criteria:**
1. Match detected language version from graph
2. Use language-specific image when available (includes runtime, package managers)
3. Fall back to minimal UBI for static binaries or unsupported languages
4. Prefer latest patch version for security updates

### Step 4: Generate Dockerfile

Create a production-ready, security-hardened Dockerfile.

**Multi-Stage Build Pattern (for compiled languages):**

```dockerfile
# Stage 1: Build
FROM registry.access.redhat.com/ubi9/openjdk-17:latest AS builder
WORKDIR /build
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM registry.access.redhat.com/ubi9/openjdk-17-runtime:latest
WORKDIR /app

# Security: Run as non-root user
USER 1001

# Copy only runtime artifacts
COPY --from=builder /build/target/*.jar /app/app.jar

# Externalize configuration
ENV SPRING_PROFILES_ACTIVE=prod \
    DATABASE_URL="" \
    DATABASE_USER="" \
    DATABASE_PASSWORD=""

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Expose port
EXPOSE 8080

# Run application
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

**Single-Stage Pattern (for interpreted languages):**

```dockerfile
FROM registry.access.redhat.com/ubi9/python-39:latest

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Security: Already runs as user 1001 in UBI Python images
# No need to set USER directive

# Externalize configuration
ENV DJANGO_SETTINGS_MODULE=myapp.settings.production \
    DATABASE_URL="" \
    SECRET_KEY=""

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myapp.wsgi:application"]
```

**Security Hardening Checklist:**

- ✅ Use multi-stage builds to reduce image size and attack surface
- ✅ Run as non-root user (USER 1001 or default non-root from UBI images)
- ✅ Don't copy unnecessary files (.git, tests, docs) - use .dockerignore
- ✅ Use `--no-cache-dir` for package managers to reduce size
- ✅ Externalize all secrets and configuration as ENV variables
- ✅ Include health check for container orchestration
- ✅ Use specific image tags (not `latest` in production)
- ✅ Minimize layers (combine RUN commands where logical)
- ✅ Set appropriate file permissions
- ✅ Remove build tools from runtime image

**Create .dockerignore:**
```
.git
.gitignore
*.md
tests/
docs/
.env
*.log
node_modules/
__pycache__/
*.pyc
target/
build/
```

### Step 5: Generate OpenShift Manifests

Create Kubernetes/OpenShift deployment manifests for the application and its dependencies.

#### ConfigMap (application configuration)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: <namespace>
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  MAX_WORKERS: "4"
  # Non-sensitive configuration only
```

**What goes in ConfigMap:**
- Application settings (log levels, feature flags)
- Non-sensitive URLs and endpoints
- Resource limits and tuning parameters
- File content (if small, like nginx.conf)

#### Secret (sensitive data)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: <namespace>
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:password@postgres:5432/dbname"
  DATABASE_PASSWORD: "changeme"
  API_KEY: "secret-api-key"
  JWT_SECRET: "jwt-signing-secret"
# Note: Use base64 encoding in production, stringData for readability here
```

**What goes in Secret:**
- Database passwords and connection strings
- API keys and tokens
- TLS certificates and private keys
- OAuth credentials
- Encryption keys

**Security notes:**
- Never commit secrets to git
- Use OpenShift's sealed secrets or external secret managers in production
- Rotate secrets regularly
- Limit secret access with RBAC

#### Deployment (application workload)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: <namespace>
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      # Security Context (pod-level)
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      
      containers:
      - name: app
        image: <image-registry>/<namespace>/myapp:latest
        imagePullPolicy: Always
        
        # Security Context (container-level)
        securityContext:
          allowPrivilegeEscalation: false
          runAsNonRoot: true
          runAsUser: 1001
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true
        
        # Resource limits (prevent resource exhaustion)
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        
        # Environment variables from ConfigMap
        envFrom:
        - configMapRef:
            name: app-config
        
        # Environment variables from Secret
        env:
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_PASSWORD
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_URL
        
        # Ports
        ports:
        - containerPort: 8080
          name: http
          protocol: TCP
        
        # Readiness probe (is the app ready to serve traffic?)
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        # Liveness probe (is the app still running?)
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        
        # Volume mounts (for writable directories)
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/.cache
      
      # Volumes
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
```

**Deployment best practices:**
- Set `replicas: 3` or more for high availability
- Use readiness/liveness probes for health monitoring
- Set resource requests/limits to prevent resource starvation
- Use `readOnlyRootFilesystem: true` and mount emptyDir for writable paths
- Drop all capabilities, run as non-root (1001)
- Use `runAsNonRoot: true` to enforce non-root execution

#### Service (internal networking)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: <namespace>
  labels:
    app: myapp
spec:
  selector:
    app: myapp
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    protocol: TCP
  type: ClusterIP
  sessionAffinity: None
```

**Service notes:**
- `ClusterIP` for internal services only
- `type: LoadBalancer` if external access needed (but prefer Route in OpenShift)
- `sessionAffinity: ClientIP` for sticky sessions (avoid if possible)

#### Route (external access - OpenShift specific)

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: app-route
  namespace: <namespace>
  labels:
    app: myapp
spec:
  to:
    kind: Service
    name: app-service
    weight: 100
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
  wildcardPolicy: None
```

**Route notes:**
- Always use TLS (`termination: edge` or `passthrough`)
- `insecureEdgeTerminationPolicy: Redirect` forces HTTPS
- `wildcardPolicy: None` unless you need wildcard domains

#### Database StatefulSet (if application uses a database)

For databases that need persistent storage:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: <namespace>
spec:
  ports:
  - port: 5432
    name: postgres
  clusterIP: None  # Headless service for StatefulSet
  selector:
    app: postgres
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: <namespace>
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: registry.redhat.io/rhel9/postgresql-15:latest
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRESQL_USER
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_USER
        - name: POSTGRESQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_PASSWORD
        - name: POSTGRESQL_DATABASE
          value: "myapp"
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

**Database deployment options:**

1. **StatefulSet in OpenShift** (above) - Good for dev/test, small deployments
2. **External managed database** (AWS RDS, Azure Database, etc.) - Recommended for production
3. **OpenShift Database Operator** - For production databases with backup, HA
4. **Ephemeral for local dev** - Use podman-compose with no persistence

#### PersistentVolumeClaim (for file uploads, logs, etc.)

If the application needs persistent file storage:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-uploads
  namespace: <namespace>
spec:
  accessModes:
  - ReadWriteMany  # RWX if multiple pods need access
  resources:
    requests:
      storage: 50Gi
  storageClassName: <storage-class>  # ocs-storagecluster-cephfs, etc.
```

Then mount in Deployment:
```yaml
volumeMounts:
- name: uploads
  mountPath: /app/uploads
volumes:
- name: uploads
  persistentVolumeClaim:
    claimName: app-uploads
```

**Storage considerations:**
- Use `ReadWriteMany` (RWX) if multiple pods need shared access
- Use `ReadWriteOnce` (RWO) for single-pod access (cheaper)
- Consider object storage (S3, MinIO) instead of PVC for scalability
- Set appropriate storage class based on performance needs

### Step 6: Build and Test with Podman

Use podman to build the container image and run security scans.

**Build the image:**
```bash
podman build -t myapp:latest -f Dockerfile .
```

**Security scan for vulnerabilities:**
```bash
# Install skopeo and grype if not available
which grype || echo "Install grype: brew install grype"

# Scan for vulnerabilities
grype myapp:latest --fail-on medium

# Alternative: Use podman's built-in scan (if available)
podman image scan myapp:latest
```

**Smoke test the container:**
```bash
# Run container locally
podman run -d \
  --name myapp-test \
  -p 8080:8080 \
  -e DATABASE_URL="postgresql://localhost:5432/test" \
  myapp:latest

# Wait for startup
sleep 5

# Test health endpoint
curl -f http://localhost:8080/health || echo "Health check failed"

# Check logs
podman logs myapp-test

# Cleanup
podman stop myapp-test
podman rm myapp-test
```

**Tag for registry:**
```bash
# Tag for OpenShift internal registry
podman tag myapp:latest image-registry.openshift-image-registry.svc:5000/<namespace>/myapp:latest

# Or tag for external registry
podman tag myapp:latest quay.io/<org>/myapp:latest
```

**Push to registry (when ready):**
```bash
# Login to OpenShift registry
podman login -u $(oc whoami) -p $(oc whoami -t) image-registry.openshift-image-registry.svc:5000

# Push image
podman push image-registry.openshift-image-registry.svc:5000/<namespace>/myapp:latest
```

### Step 7: Create podman-compose for Local Development

Generate podman-compose.yml for local testing with all dependencies.

**Example podman-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/myapp
      REDIS_URL: redis://redis:6379/0
      APP_ENV: development
    depends_on:
      - db
      - redis
    volumes:
      # Mount source code for live reload in development
      - ./src:/app/src:ro
      # Persistent uploads
      - uploads:/app/uploads
    networks:
      - app-network

  db:
    image: registry.redhat.io/rhel9/postgresql-15:latest
    environment:
      POSTGRESQL_USER: postgres
      POSTGRESQL_PASSWORD: password
      POSTGRESQL_DATABASE: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: registry.redhat.io/rhel9/redis-7:latest
    ports:
      - "6379:6379"
    networks:
      - app-network

volumes:
  postgres-data:
  uploads:

networks:
  app-network:
    driver: bridge
```

**Usage:**
```bash
# Start all services
podman-compose up -d

# View logs
podman-compose logs -f app

# Stop all services
podman-compose down

# Remove volumes (reset data)
podman-compose down -v
```

**podman-compose notes:**
- Use Red Hat registry images where available
- Match environment variables with OpenShift deployment
- Mount source code read-only (`:ro`) for live reload
- Use named volumes for persistence
- Expose ports for debugging (remove in production manifests)

### Step 8: Generate Containerization Report

Create a comprehensive report documenting the containerization process and deployment instructions.

**Report structure:**

```markdown
# Containerization Report: [Application Name]

## Executive Summary

- **Application**: [Name and description]
- **Language/Framework**: [Detected from graph]
- **Base Image**: [Selected UBI image]
- **Deployment Target**: OpenShift
- **Build Time**: [Duration]
- **Image Size**: [Final size]
- **Security Scan**: [Vulnerability count by severity]

## Graph Analysis Findings

### Application Structure
- **Nodes**: [count from graph]
- **Edges**: [count from graph]
- **Communities**: [count from graph]
- **Primary Language**: [detected]
- **Framework**: [detected]

### External Dependencies
[List from graph analysis]
- PostgreSQL database (requires StatefulSet or external service)
- Redis cache (deployed as sidecar)
- External API: [name] (requires Secret for API key)

### Platform-Specific Code Identified
[List blockers found in graph]
- **Hardcoded paths**: `/var/app/uploads` → Replaced with ENV variable `UPLOAD_DIR`
- **Configuration files**: `application.properties` → Externalized to ConfigMap
- **Database connection**: Hardcoded localhost → ENV variable `DATABASE_URL`

### Migration Complexity: [Low/Medium/High]

**Reasoning**: [Based on graph metrics - god nodes, coupling, platform dependencies]

## Containerization Strategy

### Base Image Selection
- **Selected**: `registry.access.redhat.com/ubi9/[language]:[version]`
- **Reason**: [Why this image variant]
- **Alternatives considered**: [Other options]

### Build Strategy
- **Type**: [Multi-stage / Single-stage]
- **Stages**: [If multi-stage, list stages]
- **Dependencies**: [Build-time and runtime]

### Security Hardening Applied
- ✅ Non-root user (UID 1001)
- ✅ Read-only root filesystem
- ✅ Dropped all capabilities
- ✅ Security context constraints configured
- ✅ Vulnerability scan passed (0 critical, 0 high)
- ✅ Secrets externalized
- ✅ No hardcoded credentials

## Generated Artifacts

### Container Image
- **Name**: `[namespace]/[app-name]:[tag]`
- **Size**: [MB/GB]
- **Layers**: [count]
- **Created**: [timestamp]

### Kubernetes Manifests
1. `configmap.yaml` - Application configuration
2. `secret.yaml` - Sensitive data (passwords, keys)
3. `deployment.yaml` - Application workload
4. `service.yaml` - Internal networking
5. `route.yaml` - External access
6. [If database] `database-statefulset.yaml` - Database deployment
7. [If storage needed] `pvc.yaml` - Persistent storage

### Local Development
- `podman-compose.yml` - Local development environment
- `.dockerignore` - Build exclusions

## Deployment Instructions

### Prerequisites
1. OpenShift cluster access (`oc` CLI configured)
2. Namespace/project created
3. Image registry access
4. (Optional) External database provisioned

### Steps to Deploy

**1. Create namespace:**
```bash
oc new-project [namespace]
```

**2. Create secrets:**
```bash
oc apply -f secret.yaml
```

**3. Create ConfigMap:**
```bash
oc apply -f configmap.yaml
```

**4. Build and push image:**
```bash
podman build -t [image] .
podman push [image]
```

**5. Deploy database (if applicable):**
```bash
oc apply -f database-statefulset.yaml
```

**6. Deploy application:**
```bash
oc apply -f deployment.yaml
oc apply -f service.yaml
oc apply -f route.yaml
```

**7. Verify deployment:**
```bash
oc get pods
oc get route
oc logs deployment/app
```

**8. Test the application:**
```bash
curl https://$(oc get route app-route -o jsonpath='{.spec.host}')/health
```

## Configuration Reference

### Environment Variables

| Variable | Description | Source | Required |
|----------|-------------|--------|----------|
| DATABASE_URL | PostgreSQL connection string | Secret | Yes |
| DATABASE_PASSWORD | Database password | Secret | Yes |
| REDIS_URL | Redis connection string | ConfigMap | No |
| API_KEY | External API key | Secret | Yes |
| LOG_LEVEL | Logging verbosity | ConfigMap | No |
| MAX_WORKERS | Worker pool size | ConfigMap | No |

### Resource Requirements

**Application Pod:**
- CPU request: 250m
- CPU limit: 500m
- Memory request: 256Mi
- Memory limit: 512Mi

**Database Pod** (if deployed):
- CPU request: 250m
- CPU limit: 1000m
- Memory request: 256Mi
- Memory limit: 1Gi
- Storage: 10Gi (PVC)

## Health and Monitoring

### Health Endpoints
- **Readiness**: `GET /health` (returns 200 if ready)
- **Liveness**: `GET /health` (returns 200 if alive)

### Probes Configuration
- **Readiness**: Initial delay 10s, period 5s
- **Liveness**: Initial delay 30s, period 10s

### Metrics (if applicable)
- **Prometheus**: Available at `/metrics`
- **Scrape interval**: 30s

## Security Considerations

### Image Security
- Base image: Red Hat UBI (trusted, supported)
- Vulnerability scan: [Results]
- No secrets in image layers
- Minimal attack surface (multi-stage build)

### Runtime Security
- Non-root execution (UID 1001)
- Read-only filesystem
- Capabilities dropped
- Security Context Constraints: `restricted-v2`

### Network Security
- TLS enabled for external routes
- Internal traffic unencrypted (within cluster)
- Network policies (if configured)

### Secrets Management
- Stored in OpenShift Secrets
- Mounted as environment variables
- Not logged or exposed in /proc
- Recommendation: Use external secret manager (Vault) for production

## Rollback Procedure

If deployment fails:

```bash
# View previous deployments
oc rollout history deployment/app

# Rollback to previous version
oc rollout undo deployment/app

# Rollback to specific revision
oc rollout undo deployment/app --to-revision=2

# Verify rollback
oc get pods
oc logs deployment/app
```

## Known Issues and Limitations

[List any unresolved blockers or workarounds]

## Next Steps

1. ✅ Containerization complete
2. ⏳ Deploy to dev/test environment
3. ⏳ Performance testing under load
4. ⏳ Set up CI/CD pipeline
5. ⏳ Configure monitoring and alerting
6. ⏳ Plan database migration (if external)
7. ⏳ Production deployment

## Support and Resources

- **Red Hat UBI Images**: https://catalog.redhat.com/software/containers/search
- **OpenShift Documentation**: https://docs.openshift.com/
- **Podman Documentation**: https://docs.podman.io/
- **Security Best Practices**: https://docs.openshift.com/container-platform/latest/security/index.html
```

## Key Principles

**Graph-First, Not Guesswork:**
Use the knowledge graph to understand the application's true dependencies, not assumptions. The graph reveals hidden platform dependencies, external services, and architectural patterns.

**Security by Default:**
Every generated Dockerfile and manifest includes security hardening. Non-root execution, read-only filesystems, capability dropping, and vulnerability scanning are not optional.

**Red Hat UBI Only:**
Always use official Red Hat Universal Base Images. They're supported, regularly patched, and comply with enterprise security requirements.

**Environment-Driven Configuration:**
Never hardcode configuration in images. Use environment variables, ConfigMaps, and Secrets for all configuration. This enables promotion across environments (dev → test → prod).

**Test Locally First:**
Always build and test with podman before deploying to OpenShift. The podman-compose environment should mirror the OpenShift deployment.

**Documentation is Deliverable:**
The containerization report is as important as the Dockerfile. It explains decisions, lists dependencies, provides deployment steps, and serves as runbook.

**Idempotent Deployments:**
All Kubernetes manifests should be declarative and idempotent. Running `oc apply -f` multiple times should be safe.

---

Remember: The knowledge graph guides containerization strategy. High-degree nodes indicate critical services that need robust health checks. Communities suggest service boundaries for microservices decomposition. External edges reveal dependencies to externalize as environment configuration. Use the graph intelligence.
