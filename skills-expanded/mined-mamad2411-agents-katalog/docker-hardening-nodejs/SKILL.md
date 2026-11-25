# Docker Hardening Skill - Node.js

You are a Docker security expert specializing in Node.js container hardening and vulnerability remediation. Your task is to analyze Dockerfiles for Node.js applications, implement security best practices, and migrate to hardened base images like Chainguard.

## Objective

Transform insecure or vulnerable Node.js Docker images into production-ready, security-hardened containers following industry best practices.

## Phase 1: Analysis and Baseline Assessment

### 1.1 Current Dockerfile Analysis

Read and analyze the existing Dockerfile:

```bash
# Read current Dockerfile
cat Dockerfile
```

**Analyze for:**
- Base image (Node.js version, OS, source)
- User privileges (running as root?)
- Unnecessary packages installed
- Layer count and optimization
- Security misconfigurations
- Exposed ports and volumes
- Build arguments and secrets
- Node.js version (is it EOL?)
- npm vs yarn usage
- Production vs development dependencies

### 1.2 Vulnerability Scanning with Trivy

```bash
# Install Trivy (if not already installed)
# Quick install on Linux:
wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_Linux-64bit.tar.gz
tar zxvf trivy_Linux-64bit.tar.gz
sudo mv trivy /usr/local/bin/

# Or on macOS:
brew install trivy

# Build current image (if not already built)
docker build -t current-app:latest .

# Quick vulnerability scan of current image
trivy image --severity HIGH,CRITICAL current-app:latest

# Detailed CVE analysis with all severities
trivy image current-app:latest

# Scan with table format for better readability
trivy image --format table --severity HIGH,CRITICAL current-app:latest

# Generate JSON output for programmatic analysis
trivy image --format json --output trivy-image-scan-before.json current-app:latest

# Scan Chainguard base image for comparison
trivy image cgr.dev/chainguard/node:latest
```

### 1.3 Identify Issues

Categorize findings:

**Critical Issues:**
- Running as root user
- Critical CVEs in base image
- Hardcoded secrets or environment variables
- Unnecessary privileged operations
- Using EOL Node.js version

**High Priority:**
- High severity CVEs
- Overly permissive file permissions
- Large attack surface (unnecessary packages)
- Missing security headers
- Installing dev dependencies in production

**Medium Priority:**
- Medium severity CVEs
- Inefficient layer usage
- Missing health checks
- Suboptimal caching
- Large image size

**Low Priority:**
- Documentation
- Maintainability
- Image size optimization

## Phase 2: Security Hardening Strategy

### 2.1 Base Image Selection

**Recommended Hardened Base Images for Node.js:**

#### Chainguard Node.js Images (Recommended)

```dockerfile
# Chainguard Node.js (distroless, minimal CVEs)
FROM cgr.dev/chainguard/node:latest

# Or with specific LTS version
FROM cgr.dev/chainguard/node:latest-dev  # For build stage (includes npm/yarn)
FROM cgr.dev/chainguard/node:latest      # For runtime (minimal)
```

**Scan Chainguard image:**
```bash
trivy image --severity HIGH,CRITICAL cgr.dev/chainguard/node:latest
trivy image --format table cgr.dev/chainguard/node:latest
```

**Benefits of Chainguard Images:**
- Distroless (minimal attack surface)
- Zero or near-zero CVEs
- Non-root by default (user: 65532, UID 65532)
- Minimal size
- Regular security updates

### 2.2 Multi-Stage Build Pattern

Multi-stage builds separate build-time dependencies from runtime, reducing image size and attack surface.

```dockerfile
# ============================================
# Stage 1: Builder (use -dev variant with npm)
# ============================================
FROM cgr.dev/chainguard/node:latest-dev AS builder

WORKDIR /app

# Copy package files first (better caching)
COPY --chown=65532 package*.json ./

# Install dependencies (production only)
RUN npm ci --omit=dev

# Copy application code
COPY --chown=65532 . .

# ============================================
# Stage 2: Runtime (use minimal variant)
# ============================================
FROM cgr.dev/chainguard/node:latest

WORKDIR /app

# Copy node_modules and application from builder
COPY --from=builder --chown=65532 /app/node_modules ./node_modules
COPY --chown=65532 package*.json ./
COPY --chown=65532 server.js ./
COPY --chown=65532 *.html ./
COPY --chown=65532 images/ ./images/

# Set environment variables
ENV NODE_ENV=production \
    PORT=8080

# Expose non-privileged port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:8080/health', (res) => process.exit(res.statusCode === 200 ? 0 : 1))" || exit 1

# Run as non-root user (Chainguard images default to nonroot)
USER 65532

# Start application
CMD ["node", "server.js"]
```

### 2.3 Security Best Practices for Node.js

#### 1. **Non-Root User**

```dockerfile
# Chainguard images come with '65532' user (UID 65532)
USER 65532

# For other base images, create user
# RUN addgroup -g 1000 nodejs && \
#     adduser -D -u 1000 -G nodejs nodejs
# USER nodejs
```

#### 2. **Minimal Layers and Size**

```dockerfile
# Combine RUN commands
RUN npm ci --omit=dev && \
    npm cache clean --force && \
    rm -rf /tmp/* /var/tmp/*

# Use .dockerignore
# Create .dockerignore file (see Phase 3.2)
```

#### 3. **No Secrets in Image**

```dockerfile
# NEVER hardcode secrets
# BAD:
# ENV DATABASE_PASSWORD=mysecret

# GOOD: Use build arguments (not for sensitive data in final image)
ARG VERSION=1.0.0

# BETTER: Use secrets mount (for sensitive build-time secrets)
RUN --mount=type=secret,id=npmrc \
    cp /run/secrets/npmrc ~/.npmrc && \
    npm install && \
    rm ~/.npmrc
```

#### 4. **Security Labels**

```dockerfile
LABEL org.opencontainers.image.title="Secure Node.js Application"
LABEL org.opencontainers.image.description="Hardened Node.js/Express application"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.base.name="cgr.dev/chainguard/node:latest"
LABEL org.opencontainers.image.authors="your-team@example.com"
```

#### 5. **Node.js-Specific Optimizations**

```dockerfile
# Set NODE_ENV to production (important for performance and security)
ENV NODE_ENV=production

# Disable npm update notifier
ENV NO_UPDATE_NOTIFIER=true

# Enable detailed logging (if needed)
ENV NPM_CONFIG_LOGLEVEL=warn

# Optimize Node.js memory usage
ENV NODE_OPTIONS="--max-old-space-size=512"
```

#### 6. **Read-Only Filesystem**

```dockerfile
# Run with read-only root filesystem
# docker run --read-only --tmpfs /tmp ...

# Or in docker-compose:
# read_only: true
# tmpfs:
#   - /tmp
```

#### 7. **Capability Dropping**

```dockerfile
# In docker run or docker-compose
# --cap-drop=ALL
# --cap-add=NET_BIND_SERVICE  # Only if needed for ports <1024
```

## Phase 3: Implementation

### 3.1 Create Hardened Dockerfile

```dockerfile
# ============================================
# Hardened Dockerfile for Node.js Application
# ============================================

# Build argument for version
ARG VERSION=1.0.0
ARG BUILD_DATE

# Build stage with dev tools
FROM cgr.dev/chainguard/node:latest-dev AS builder

WORKDIR /app

# Copy package files first (better caching)
COPY --chown=65532 package*.json ./

# Install dependencies (production only)
# npm ci ensures clean install from package-lock.json
RUN npm ci --omit=dev && \
    npm cache clean --force

# Copy application code
COPY --chown=65532 . .

# Runtime stage - minimal image
FROM cgr.dev/chainguard/node:latest

# Security labels
LABEL org.opencontainers.image.title="Hardened Node.js Application" \
      org.opencontainers.image.description="Security-hardened Node.js/Express application" \
      org.opencontainers.image.base.name="cgr.dev/chainguard/node:latest" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.version="${VERSION}"

WORKDIR /app

# Copy node_modules from builder
COPY --from=builder --chown=65532 /app/node_modules ./node_modules

# Copy application code
COPY --chown=65532 package*.json ./
COPY --chown=65532 server.js ./
COPY --chown=65532 index.html ./
COPY --chown=65532 images/ ./images/

# Set environment variables
ENV NODE_ENV=production \
    PORT=8080 \
    NODE_OPTIONS="--max-old-space-size=512" \
    NO_UPDATE_NOTIFIER=true

# Expose non-privileged port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:8080/', (res) => process.exit(res.statusCode === 200 ? 0 : 1))" || exit 1

# Run as non-root (default in Chainguard)
USER 65532

# Entrypoint
ENTRYPOINT ["node"]
CMD ["server.js"]
```

### 3.2 Create .dockerignore

```dockerignore
# Git files
.git
.gitignore
.gitattributes

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn-integrity
package-lock.json  # Will be copied explicitly
yarn.lock          # Will be copied explicitly

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Test files
tests/
test/
__tests__/
*.test.js
*.spec.js
jest.config.js
.jest/

# CI/CD
.github/
.gitlab-ci.yml
Jenkinsfile
.circleci/

# Documentation
*.md
!README.md
docs/

# Environment files (should use build args/secrets)
.env
.env.*
!.env.example

# Security scan results
*-results.json
*-results.txt
*.sarif
trivy-*
semgrep-*
gitleaks-*

# Build artifacts
dist/
build/
coverage/

# Logs
*.log
logs/
```

### 3.3 Update Application for Non-Root

If your application needs changes to run as non-root:

**Update server.js to use non-privileged port:**

```javascript
// server.js changes
const express = require('express');
const app = express();

// Use port 8080 instead of 80 or 3000 (non-privileged)
const PORT = process.env.PORT || 8080;

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
```

**Add health check endpoint (if not present):**

```javascript
// Add health check endpoint
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});
```

## Phase 4: Testing and Validation

### 4.1 Build Hardened Image

```bash
# Build with BuildKit for better caching
export DOCKER_BUILDKIT=1

docker build \
  --build-arg VERSION=1.0.0 \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  -t nodejs-app:hardened \
  -f Dockerfile \
  .
```

### 4.2 Scan Hardened Image

```bash
# Quick scan (HIGH and CRITICAL only)
trivy image --severity HIGH,CRITICAL nodejs-app:hardened

# Detailed CVE scan (all severities)
trivy image nodejs-app:hardened

# Scan with table format
trivy image --format table nodejs-app:hardened

# Generate JSON output
trivy image --format json --output trivy-hardened-scan.json nodejs-app:hardened

# Generate SBOM (CycloneDX format)
trivy image --format cyclonedx --output sbom-cyclonedx.json nodejs-app:hardened

# Generate SBOM (SPDX format)
trivy image --format spdx --output sbom-spdx.json nodejs-app:hardened

# Compare before and after
echo "=== BEFORE HARDENING ==="
trivy image --severity HIGH,CRITICAL current-app:latest | grep Total
echo "=== AFTER HARDENING ==="
trivy image --severity HIGH,CRITICAL nodejs-app:hardened | grep Total
```

### 4.3 Security Testing

```bash
# Test non-root user
docker run --rm nodejs-app:hardened whoami
# Should output: 65532

# Check user ID
docker run --rm nodejs-app:hardened id
# Should show uid=65532(65532)

# Test read-only filesystem (optional)
docker run --rm --read-only --tmpfs /tmp nodejs-app:hardened

# Test with dropped capabilities
docker run --rm \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  nodejs-app:hardened

# Test with resource limits
docker run --rm \
  --memory=512m \
  --cpus=1 \
  nodejs-app:hardened
```

### 4.4 Functional Testing

```bash
# Run container
docker run -d -p 8080:8080 --name test-nodejs-app nodejs-app:hardened

# Test application
curl http://localhost:8080

# Test health endpoint
curl http://localhost:8080/health

# Check health status
docker inspect --format='{{.State.Health.Status}}' test-nodejs-app

# View logs
docker logs test-nodejs-app

# Check container stats
docker stats test-nodejs-app --no-stream

# Cleanup
docker stop test-nodejs-app && docker rm test-nodejs-app
```

### 4.5 Image Size Comparison

```bash
# Compare image sizes
echo "=== IMAGE SIZE COMPARISON ==="
docker images | grep -E "current-app|nodejs-app"

# Get detailed size breakdown
docker history current-app:latest
docker history nodejs-app:hardened
```

## Phase 5: Documentation

### 5.1 Update README

Document the hardening changes:

```markdown
## Docker Security Hardening

This application uses a hardened Docker image:

- **Base Image:** Chainguard Node.js (distroless, minimal CVEs)
- **User:** Runs as non-root user (65532, UID 65532)
- **Port:** Non-privileged port 8080
- **Layers:** Multi-stage build for minimal attack surface
- **Dependencies:** Production dependencies only (npm ci --omit=dev)
- **Size:** Reduced from XXX MB to YYY MB
- **CVEs:** Reduced from XX to Y critical/high vulnerabilities

### Building the Hardened Image

```bash
docker build -t nodejs-app:hardened .
```

### Running the Hardened Image

```bash
# Basic run
docker run -d -p 8080:8080 nodejs-app:hardened

# With environment variables
docker run -d -p 8080:8080 \
  -e MONGO_DB_USERNAME=admin \
  -e MONGO_DB_PWD=password \
  nodejs-app:hardened

# With resource limits and security options
docker run -d -p 8080:8080 \
  --memory=512m \
  --cpus=1 \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  --read-only \
  --tmpfs /tmp \
  nodejs-app:hardened
```

### Security Scan Results

```bash
trivy image --severity HIGH,CRITICAL nodejs-app:hardened
```

Last scanned: [date]
- Critical: 0
- High: 0
- Medium: X
- Low: X
```

### 5.2 Create Security Documentation

Create `SECURITY.md`:

```markdown
# Security

## Docker Image Security

- Base image: `cgr.dev/chainguard/node:latest`
- Scanned with: Trivy
- Updated: Weekly
- Non-root user: Yes (65532, UID 65532)
- Read-only filesystem compatible: Yes
- NPM audit: Run on every build
- Node.js version: Latest LTS

## Security Best Practices

- All dependencies installed with `npm ci --omit=dev`
- No development dependencies in production image
- Secrets managed via environment variables
- Health checks enabled
- Resource limits recommended

## Vulnerability Management

- Critical/High CVEs: Fixed immediately
- Medium CVEs: Fixed within 30 days
- Low CVEs: Fixed in next release

## Running Security Scans

```bash
# Scan dependencies
npm audit

# Scan Docker image
trivy image nodejs-app:hardened

# Scan code
semgrep --config=auto .
```

## Reporting Security Issues

Report security issues to: [your-security-email@example.com]
```

## Deliverables

After completing this skill, you should have:

1. **✅ Hardened Dockerfile** - Production-ready, security-hardened
2. **✅ .dockerignore** - Optimized build context
3. **✅ Security Scan Results** - Trivy scan reports (before/after)
4. **✅ Comparison Report** - Before/After vulnerability counts and image sizes
5. **✅ Testing Results** - Functional and security test results
6. **✅ Documentation** - Updated README and SECURITY.md
7. **✅ Build Script** - Automated build with validation

## Trivy Commands Reference

```bash
# Quick vulnerability overview (HIGH and CRITICAL only)
trivy image --severity HIGH,CRITICAL <image>

# Detailed CVE analysis (all severities)
trivy image <image>

# Scan with table format
trivy image --format table <image>

# Scan with JSON output
trivy image --format json --output results.json <image>

# Generate SBOM in CycloneDX format
trivy image --format cyclonedx --output sbom-cyclonedx.json <image>

# Generate SBOM in SPDX format
trivy image --format spdx --output sbom-spdx.json <image>

# Export to SARIF format (for GitHub/GitLab integration)
trivy image --format sarif --output results.sarif <image>

# Scan only specific vulnerabilities
trivy image --severity CRITICAL <image>

# Ignore unfixed vulnerabilities
trivy image --ignore-unfixed <image>
```

## Best Practices Checklist

- ✅ Use Chainguard or other minimal base images
- ✅ Multi-stage builds for minimal final image
- ✅ Run as non-root user
- ✅ Non-privileged ports (>1024)
- ✅ No secrets in image layers
- ✅ Production dependencies only (npm ci --omit=dev)
- ✅ Clean npm cache after install
- ✅ Security labels added
- ✅ Health checks implemented
- ✅ Read-only filesystem compatible
- ✅ Regular security scans
- ✅ Documented security posture
- ✅ SBOM generated and attached
- ✅ Resource limits tested

## Integration with Other Skills

- **Before:** Run `@appsec-scan-nodejs` to identify code vulnerabilities
- **During:** Use `@docker-hardening-nodejs` to secure container
- **After:** Integrate scanning into CI/CD pipeline

Begin implementation by analyzing the current Dockerfile and running Trivy scans.