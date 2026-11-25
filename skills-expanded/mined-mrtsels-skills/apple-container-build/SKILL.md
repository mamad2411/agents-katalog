---
name: apple-container-build
description: Build Docker/OCI images on macOS ARM without Docker Desktop, using apple/container. Pre-compiled JAR pattern for Java projects.
tags: [docker, container, macos, arm, java, build]
---

## macOS ARM → Linux x86_64 Docker Build

Build Docker images on macOS ARM for deployment on Linux x86_64 servers. Two approaches:

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| **apple/container** (推荐) | 零依赖，macOS 内置 | `container save/export` 插件常缺失 | macOS 27+，不需要 docker compose |
| **Colima + QEMU** | 完整 Docker 体验（compose/build/inspect） | 需要 QEMU 模拟器，启动慢，需单独安装 | 需要 `docker-compose.yml` 构建多服务 |

### Colima x86_64 Setup

```bash
# 1. Install dependencies
brew install colima qemu docker docker-compose docker-buildx lima-additional-guestagents

# 2. Configure docker CLI
mkdir -p ~/.docker/cli-plugins
ln -sf /opt/homebrew/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx

# 3. Disable docker-credential-desktop credentials
echo '{"credsStore":""}' > ~/.docker/config.json

# 4. Start colima with x86_64 architecture
colima start --arch x86_64 --cpu 4 --memory 8

# 5. Switch docker context to colima
docker context use colima

# 6. Verify
docker info --format '{{.OSType}}/{{.Architecture}}'
# Expected: linux/x86_64
```

> ⚠️ First start downloads a ~2GB VM image + disk. Expect 5-10 minutes.

### Build with docker-compose (via Colima)

```bash
cd ~/project
docker-compose build backend
```

If `docker compose` (with space) not found, use `docker-compose` (hyphen) — install via `brew install docker-compose`.

### Transfer via SMB

```bash
# 1. Save image
docker save <image>:<tag> -o /tmp/<image>.tar

# 2. Mount SMB share
mount_smbfs //user:password@host/share /path/to/mount

# 3. Copy to VM
cp /tmp/<image>.tar /path/to/mount/Desktop/

# 4. On VM
docker load -i ~/Desktop/<image>.tar
```

### Note on `docker compose` vs `docker-compose`

Colima's docker context provides `docker` CLI but the `compose` plugin (docker compose with space) may not be installed. Install separately:

```bash
brew install docker-compose   # provides `docker-compose` (hyphen)
# or
brew install docker-buildx && \
  mkdir -p ~/.docker/cli-plugins && \
  ln -sf /opt/homebrew/Cellar/docker-compose/*/bin/docker-compose ~/.docker/cli-plugins/docker-compose
  # provides `docker compose` (space)
```

> Colima 详细步骤见 `devops/docker-production-deployment` skill 的「Cross-arch Docker Build」节。

## When to use

- You need Docker images but the Mac has no Docker Desktop
- Apple's `container` CLI is available (macOS 27+)
- Target deployment is Linux x86_64 (e.g. Kylin, Ubuntu, CentOS on x86_64 VMs)
- You want to build on Mac and ship the tar.gz to a remote VM

## Setup check

```bash
container --version            # Check apple/container availability
container build --help | grep output  # Check -o/--output options
```

## Java projects: pre-compiled JAR pattern (recommended)

For Java/Spring Boot projects, use **single-stage** Dockerfiles that COPY a locally compiled JAR. **Avoid multi-stage Maven builds** — Maven downloading all deps inside apple/container is extremely slow (20+ minutes) and prone to network/proxy issues.

### 1. Find JDK

```bash
# JDK 17 (from Homebrew)
export JAVA_HOME=/opt/homebrew/opt/openjdk@17
$JAVA_HOME/bin/java -version

# Other JDK versions
/usr/libexec/java_home -v 21    # Check for JDK 21
ls /opt/homebrew/opt/openjdk*   # List installed JDKs
```

### 2. Compile JAR locally

```bash
cd project/backend
export JAVA_HOME=/opt/homebrew/opt/openjdk@17
mvn clean package -DskipTests -q
ls -lh target/*.jar
```

Verify the JAR is a proper fat JAR (Spring Boot: 50-70MB is typical, not a few KB stub).

### 3. Single-stage Dockerfile

```dockerfile
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY target/enterprise-mvp-0.1.0-SNAPSHOT.jar app.jar
RUN mkdir -p /app/uploads
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
ENTRYPOINT ["java", "-Xms256m", "-Xmx512m", "-jar", "/app/app.jar"]
```

Build is instant (~1-2s) because only a JRE base image + local file copy needed.

#### Production hardening: crash-resilient entrypoint

For production deployments where the container must stay "up" even if the JVM crashes, use the `templates/docker-entrypoint.sh` wrapper:

```dockerfile
# Replace the ENTRYPOINT line with:
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]
```

The script loops: JVM exit → sleep 3s → restart. Docker's PID 1 stays alive, so `docker ps` shows the container as running even after code crashes. Pair with `restart: unless-stopped` in docker-compose.

### 4. Build and export

```bash
cd project/backend

# Build and export to tar directly
container build --platform linux/amd64 \
  -t my-app:latest \
  -f Dockerfile \
  -o type=tar,dest=/tmp/my-app.tar .

# Alternative: build to OCI layout, then save separately
container build --platform linux/amd64 -t my-app:latest -f Dockerfile .
container export my-app:latest -o /tmp/my-app.tar
```

> **Note:** `-o type=tar,dest=<path>` is the most straightforward — single command, single output.
> `container export` may not be available (plugin not installed).

### 5. Compress for transport

```bash
gzip -f /tmp/my-app.tar
ls -lh /tmp/my-app.tar.gz   # Should show e.g. 150MB for a Spring Boot app
```

### 6. Verify image architecture

```bash
tar tzf /tmp/my-app.tar.gz | head -5
# Should show: linux_amd64/
```

## Deployment

On the target Linux VM:

```bash
gunzip my-app.tar.gz
docker load -i my-app.tar
docker compose up -d
```

## Pitfalls

### Multi-stage Maven builds are extremely slow inside apple/container

### docker-credential-desktop not found

```
error listing credentials - err: exec: "docker-credential-desktop": executable file not found in $PATH
```

**Fix:** `echo '{"credsStore":""}' > ~/.docker/config.json` — disable the credential helper and fall back to plain auth.

A `FROM maven:3.9-eclipse-temurin-17 AS builder` stage that does `RUN mvn package` inside the container can take **20+ minutes** on first run (Maven downloads all dependencies). The network goes through apple/container's NAT stack which can be slow or flaky.

**Fix:** Always pre-compile the JAR locally and use the single-stage pattern above.

### container save/export plugins may be missing

`container save`, `container export`, `container pull` are not always installed. The reliable way is `-o type=tar,dest=<path>` during build.

### Architecture mismatch

Always specify `--platform linux/amd64` when targeting x86_64 VMs (Kylin, Ubuntu, CentOS). Without it, apple/container builds for the host architecture (ARM64), which won't run on x86_64 Docker.

### JAR not found during build

Make sure the Dockerfile's COPY path is relative to the build context. The context is the directory you pass as `.` at the end of the `container build` command.
