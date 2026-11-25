---
name: docker-production-deployment
description: Production Docker deployment patterns — decoupling service startup, container health vs process health, restart policies, startup wrapper scripts, cross-arch image builds.
tags: [docker, deployment, production, colima, qemu, architecture]
---

## Process-Level Resilience: Crash-Loop Wrapper Pattern

*Background: Boss requirement — "ensure Docker starts properly even if the code inside breaks."*

**Problem:** Spring Boot apps exit with non-zero when DB is unreachable, config is wrong, or code throws at startup. Container exits → Docker marks it dead → if restart policy isn't `always`, it stays dead.

**Solution:** Wrap `ENTRYPOINT` in a shell script that never exits:

```dockerfile
# Dockerfile
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]
```

```bash
#!/bin/bash
# docker-entrypoint.sh — keeps PID 1 alive
while true; do
  java -Xms256m -Xmx512m -jar /app/app.jar
  echo "JVM exited with code $?, restarting in 3s..."
  sleep 3
done
```

**Why this works:** Docker tracks PID 1. The shell script loops indefinitely — even if the JVM exits, the script stays alive. Docker sees the container as `Up`. `restart: unless-stopped` handles VM-level restarts; the loop handles app-level crashes.

**Caveats:**
- Logging goes to stdout (Docker-friendly)
- Healthcheck still reports `unhealthy` when the app is down — that's correct, it's a monitoring signal, not a kill signal
- Combine with `HEALTHCHECK --start-period=60s` so initial DB connection retries don't trigger restart loops

**Decouple services** — remove `depends_on` from compose. Each service gets its own `restart: unless-stopped`. If the DB is down, the app loops until it comes back, and Docker never sees it as dead.

## Pre-Compiled JAR Pattern (Skip Maven in Docker Build)

当构建环境内存不足（如 Kylin VM 仅 2.9GB），Maven 编译容器极易被 OOM kill。改用预编译 JAR 模式：

```dockerfile
# ❌ 多阶段构建 — Maven 需要大量内存
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline -B -q  # ← 可能 OOM
COPY src/ ./src/
RUN mvn clean package -DskipTests -B -q
FROM eclipse-temurin:17-jre
COPY --from=build /build/target/*.jar ./app.jar

# ✅ 预编译 JAR — 跳过 Maven
FROM eclipse-temurin:17-jre
COPY app.jar ./app.jar            # app.jar 在本地 mvn package 预编译好
```

**适用场景：**
- VM 内存 ≤ 4GB
- 无法使用 CI/CD 预编译
- 需要快速迭代 Docker 镜像（10 秒 vs 5 分钟）

**工作流：**
```bash
# 在构建机上预编译
cd backend && mvn clean package -DskipTests

# 复制 JAR 到 Docker 构建上下文
cp backend/target/*.jar app.jar

# 构建镜像（秒级）
docker build -t myapp:latest -f Dockerfile.jaronly .
```

## ⚠️ JDK 版本兼容性检查（必做）

Spring Boot Fat JAR 的 MANIFEST.MF 包含 `Build-Jdk-Spec` 字段。**必须检查该值后选择正确的 JRE 基础镜像**，否则 `java -jar` 报 `Invalid or corrupt jarfile`。

```bash
# 检查编译 JDK 版本
unzip -p app.jar META-INF/MANIFEST.MF | grep Build-Jdk-Spec
# → Build-Jdk-Spec: 25    ← 需要用 Java 25 JRE
# → Build-Jdk-Spec: 17    ← 需要用 Java 17 JRE
```

**错误示范（踩坑实例）：** 用 Mac 的 `mvn package` 编译（JDK 25），docker-compose.yml 中用了 `eclipse-temurin:17-jre`。结果容器启动时报 `Error: Invalid or corrupt jarfile app.jar`。排查耗时 20 分钟才发现是 JDK 版本不匹配。

**修复方案：**
1. 拉对应版本的 JRE 镜像：`eclipse-temurin:25-jre` 或 `eclipse-temurin:17-jre`
2. 或使用 Docker Maven 容器编译：`docker run --rm -v $(pwd)/backend:/build maven:3.9-eclipse-temurin-17 sh -c "cd /build && mvn clean package -DskipTests -B -q"`
3. 编译后再次检查 `Build-Jdk-Spec` 确认

```bash
# 用 Docker Maven 编译（确保 JDK 版本正确）
docker run --rm -v "$(pwd)/backend:/build" \
  maven:3.9-eclipse-temurin-17 \
  sh -c "cd /build && mvn clean package -DskipTests -B -q"

# 验证
unzip -p backend/target/*.jar META-INF/MANIFEST.MF | grep Build-Jdk-Spec
# → Build-Jdk-Spec: 17  ✅
```

## Docker Hub China Mirror Configuration

中国大陆服务器直连 registry-1.docker.io 频繁超时。配置国内镜像源：

```bash
# daemon.json
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.m.daocloud.io",
    "https://docker.nju.edu.cn",
    "https://dockerproxy.com"
  ]
}
```

**注意：** Kylin V10 的 Docker 18.09 也能使用镜像源。配置后测试：`docker pull hello-world`。

## Production Deployment

## Service CLI Tool for Production Management

For Docker Compose deployments (especially offline/air-gapped), create a unified CLI that wraps `docker compose` and adds health checks. This replaces remembering multiple commands and `curl` test lines.

### Recommended commands

| Command | What it does |
|---------|-------------|
| `appname start` | `docker compose up -d` + container checks + health check |
| `appname stop` | `docker compose down` |
| `appname status` | Show Docker containers + systemd + HTTP health in one view |
| `appname logs [-f]` | Tail application log (auto-detect file or journalctl) |
| `appname check-ai` | Progressive diagnostics for external API (DNS → hosts → per-IP → API) |

### Progressive diagnostics pattern

When the deployed app depends on an external API, create a `check-ai` command that tests connectivity depth-first:

1. **Locate API key** — search `docker/.env` → systemd service file → container `ai-config.json` (inside Docker volume, read via `docker exec`)
2. **Check hosts** — verify `/etc/hosts` or Docker container `/etc/hosts` has the required mapping
3. **Probe each IP** — use `curl --resolve` to directly connect to each known backend IP (bypasses DNS)
4. **Send test request** — a minimal API call and report the result
5. **On failure** — suggest next steps (DNS config, firewall rules, key validity)

This avoids the user having to remember curl flags and search for where the API key is stored.

### Dynamic project root

The CLI should auto-detect the project install path instead of hardcoding it:

```bash
find_project_root() {
  for dir in "${APP_HOME:-}" /opt/app /srv/app /app ~/app; do
    [ -f "$dir/docker/docker-compose.yml" ] && { echo "$dir"; return 0; }
  done
  echo "/opt/app"
}
```

**Pitfall — `set -u` kills the loop.** If the script has `set -euo pipefail` (which includes `-u` for unbound variables), referencing `$APP_HOME` without a default value causes an immediate fatal error:

```bash
# BROKEN: set -u makes this crash when APP_HOME is unset
for dir in "$APP_HOME" /opt/app; do ... done
# → script exits with "unbound variable" error

# FIXED: use ${VAR:-} default syntax
for dir in "${APP_HOME:-}" /opt/app; do ... done
```

Always use `${VAR:-}` in loops under `set -u`, even if the var is meant to be optional.

### Install via setup script

Copy the CLI to `/usr/local/bin/` during installation so it's available from any directory:

```bash
cp enterprise /usr/local/bin/enterprise
chmod +x /usr/local/bin/enterprise
```

### Why a dedicated CLI?

- `check-ai` does progressive diagnostics no single curl command covers
- `status` shows both Docker and systemd state in one view
- `logs` auto-detects the log source
- New team members learn one tool instead of 5+ docker/curl commands

### Prompt-before-search pattern

When an `update` command handles multiple components (backend JAR, frontend HTML, CLI script), ask the user which components to update **before** scanning for files — not after:

```bash
# RIGHT: ask first, then search only what's needed
if [ -t 0 ]; then echo -n "  Update backend? [Y/n] "; read -r ans
  [ "$ans" != "n" ] && [ "$ans" != "N" ] && update_backend=true
else update_backend=true; fi

if [ "$update_backend" = true ]; then
  # search for JAR, present options
  JAR_OPTS=(); JAR_LABELS=()
  # ... find files ...
  case ${#JAR_OPTS[@]} in ...
  esac
fi
```

Non-TTY (cron/CI) defaults both to true, same as `--all`.

### CLI flags to skip interactive prompts

Provide `-b|-f|-c|--all` flags so the update can run non-interactively. Parse them before calling the update function:

```bash
# In the main case statement:
case "${1:-}" in
  update)
    shift
    UPDATE_BACKEND=false; UPDATE_FRONTEND=false; UPDATE_CLI=false; UPDATE_ALL=false
    while [ $# -gt 0 ]; do
      case "$1" in
        -b|--backend)  UPDATE_BACKEND=true  ;;
        -f|--frontend) UPDATE_FRONTEND=true ;;
        -c|--cli)      UPDATE_CLI=true      ;;
        --all)         UPDATE_ALL=true      ;;
        *) usage ;;
      esac; shift
    done
    cmd_update
    ;;
esac
```

In the update function, check flags before prompting:

```bash
HAS_FLAGS=false
[ "$UPDATE_ALL" = true ] || [ "$UPDATE_BACKEND" = true ] && HAS_FLAGS=true
[ "$UPDATE_FRONTEND" = true ] && HAS_FLAGS=true; [ "$UPDATE_CLI" = true ] && HAS_FLAGS=true

do_backend=false
if [ "$UPDATE_ALL" = true ] || [ "$UPDATE_BACKEND" = true ]; then do_backend=true
elif [ "$HAS_FLAGS" = false ]; then
  # interactive prompt
  if [ -t 0 ]; then echo -n "  Update backend? [Y/n] "; read -r ans
    [ "$ans" != "n" ] && do_backend=true
  else do_backend=true; fi
fi
```

### `add_jar()` dedup with `set -u` empty array pitfall

When building a list of JAR sources from multiple paths, a dedup function prevents duplicate entries. Under `set -euo pipefail`, iterating an **empty** array inside a function body triggers "unbound variable":

```bash
# BROKEN: empty array + set -u + function = crash
JAR_OPTS=()
add_jar() { local p="$1"; for existing in "${JAR_OPTS[@]}"; do [ "$existing" = "$p" ] && return; done; JAR_OPTS+=("$p"); }
# → line 670: JAR_OPTS[@]: unbound variable

# FIXED: check length first (length expansion works fine), only loop if > 0
JAR_OPTS=()
add_jar() { local p="$1"; if [ ${#JAR_OPTS[@]} -gt 0 ]; then for existing in "${JAR_OPTS[@]}"; do [ "$existing" = "$p" ] && return; done; fi; JAR_OPTS+=("$p"); }
```

The `${#array[@]}` length expansion works correctly under `set -u` because it doesn't iterate — it just reads the count. The `${array[@]}` expansion fails because bash's `set -u` treats an empty array expansion inside a `for` loop as referencing an unbound variable.

### Port variable pattern (BP/FP from .env)

Don't hardcode ports. Define them early in the update function and source from `.env`:

```bash
# Define at the top of cmd_update, before any docker operations
BP=8082; FP=8088  # project-specific defaults
if [ -f "$PROJECT_ROOT/docker/.env" ]; then
  source "$PROJECT_ROOT/docker/.env" 2>/dev/null
  BP="${BACKEND_PORT:-$BP}"
  FP="${FRONTEND_PORT:-$FP}"
fi
```

Reference `$BP` and `$FP` throughout: health checks, wait loops, verify sections. Don't re-define them mid-function.

Pitfall: `BACKEND_PORT=` and `FRONTEND_PORT=` may be swapped — always check `.env.example` for the actual mapping. In this project `BACKEND_PORT=8082, FRONTEND_PORT=8088`.

### `update` subcommand: Container hot-reload pattern

For Docker Compose deployments, create an `update` command that copies files directly into running containers instead of rebuilding images. This eliminates `docker compose build` + `docker save` + `docker load` for every code change.

**Support multiple components:**
- **Backend JAR**: Detect from multiple paths (`/opt/project/backend/target/`, `$PROJECT_ROOT/backend/target/`, root-level `app.jar` or `enterprise-*.jar`). Handle the `/opt` → `/opt/projectname/backend/target/` path adjustment.
- **Frontend HTML**: Detect from similar paths (`/opt/projectname/index.html`, `$PROJECT_ROOT/index.html`, `/usr/share/nginx/html/index.html`).
- **CLI script**: Self-update via `docker cp` or direct `cp` to `/usr/local/bin/`.

**Mechanism:**

```bash
cmd_update() {
  # 1. Detect JAR + HTML files across multiple paths
  JAR_OPTS=()
  for dir in "/opt/app" "$PROJECT_ROOT"; do
    jar=$(ls "$dir/backend/target/app-*.jar" 2>/dev/null | head -1) || true
    [ -n "$jar" ] && JAR_OPTS+=("$jar")
  done
  # single → auto-select; multiple → prompt user; none → warn

  # 2. Copy new JAR into running container & restart
  docker stop app-container
  docker cp "$JAR_SOURCE" app-container:/app/app.jar
  docker start app-container

  # 3. Brief wait, then verify health once (NOT a polling loop)
  sleep 10

  # 4. Copy static files without restarting
  docker cp index.html app-frontend:/usr/share/nginx/html/index.html
  docker exec app-frontend nginx -s reload

  # 5. Always verify both services at the end (never skip)
  if curl -sf http://localhost:8080/api/health > /dev/null; then
    ok "backend healthy"
  else
    fail "backend unhealthy"
  fi
  if curl -sf http://localhost/ > /dev/null; then
    ok "frontend healthy"
  fi
}
```

**Key advantages over image-based updates:**
- No Docker image build required (especially slow on ARM→x86 emulation)
- No image export/import cycle for air-gapped servers
- Frontend static files update instantly without container restart

**Why NOT a polling health check loop:** A `for i in $(seq 1 30); do curl ...; sleep 3; done` loop looks smart but has two problems:
1. The `fail` inside the loop is a `warn()` equivalent — it prints a message but does NOT `return` or `exit`, so the script continues as if nothing happened
2. The verify step after the loop typically skips backend checks when JAR was updated (assuming the loop already validated it), creating a blind spot — if the loop times out, nobody checks

The simpler pattern (`sleep 10` + verify once) is more robust: the sleep gives Spring Boot time to initialize, and the verify step ALWAYS runs, catching failures reliably.

### Multi-path file detection with user selection

When an `update` command needs to find files across environments (production server `/opt/`, dev workspace), discover all sources and let the user pick:

```bash
opts=(); labels=()
for dir in "/opt" "$PROJECT_ROOT"; do
  sub="$dir/backend/target"
  [ "$dir" = "/opt" ] && sub="$dir/enterprise/backend/target"  # /opt/projectname/path
  f=$(ls "$sub/app-*.jar" 2>/dev/null | head -1) || true
  [ -n "$f" ] && opts+=("$f") && labels+=("$sub")
done

case ${#opts[@]} in
  0) warn "not found" ;;
  1) src="${opts[0]}" ;;  # auto-select
  *)
    echo "  choose source:"
    for i in "${!opts[@]}"; do echo "    [$((i+1))] ${labels[$i]}"; done
    if [ -t 0 ]; then
      echo -n "  input [1-${#opts[@]}] (default 1): "; read -r sel
      sel=${sel:-1}
    else sel=1; fi  # non-TTY: auto-pick first
    src="${opts[$((sel-1))]}"
    ;;
esac
```

The `[ "$dir" = "/opt" ]` adjustment is needed because on the production server, the project lives at `/opt/enterprise/backend/target/`, not `/opt/backend/target/`.

Do NOT include `.` in the search — it duplicates `$PROJECT_ROOT` when run from the project root.

**Pitfall:** `read` in non-TTY → guard with `[ -t 0 ]`.
**Pitfall:** `ls` + unmatched glob under `set -e` → always add `|| true`.
**Pitfall:** `git add -A` commits JARs → add `*.jar` to `.gitignore`.

### Self-update for the CLI itself

The CLI script should be able to update itself:

```bash
cmd_update() {
  CLI_SOURCE="$PROJECT_ROOT/cli-script"
  CLI_TARGET="/usr/local/bin/cli-script"

  if [ -f "$CLI_SOURCE" ]; then
    if [ -w "$(dirname "$CLI_TARGET")" ]; then
      cp "$CLI_SOURCE" "$CLI_TARGET"
      chmod +x "$CLI_TARGET"
    else
      warn "needs sudo: sudo cp cli-script /usr/local/bin/"
    fi
  fi
}
```

**Do NOT delete the source.** Never `rm -f "$JAR_SOURCE"` at the end of an update — the source JAR is the Maven build artifact; deleting it forces a full rebuild for the next update. The only thing worth cleaning is a temporary copy, never the project source.

### `set -euo pipefail` plus `ls` glob safety

When `ls` with a glob finds no matches, it exits with code 2. Under `set -e`, this kills the script even when wrapped inside `$(...)`:

```bash
# Unsafe: ls fails when glob matches nothing
jar=$(ls /path/*.jar 2>/dev/null | head -1)

# Safe: redirect stderr, ls inside $() captures exit but set -e
# doesn't propagate through pipe to head
jar=$(ls /path/app-*.jar 2>/dev/null | head -1)
# → jar="" if no match, jar="path/to/jar" if found
```

The `2>/dev/null` is critical — without it, `ls` prints "No such file or directory" to stderr, which pollutes the output regardless of exit code.

## When to use

- 领导/客户要求「小容器不和基础设施绑在一起自启动」
- 需要确保 Docker 容器在代码崩溃时也能保持 `docker ps` 为 Up 状态
- macOS ARM → Linux x86_64 交叉构建 Docker 镜像
- 审查现有 docker-compose.yml 的生产就绪度

## 核心原则（来自甲方反馈）

领导说过的一针见血的大白话，直接对应技术实现：

> 「不要把小容器的自启动和大容器绑起来」

⇒ 去掉 `depends_on`，各自独立 restart policy。MySQL 挂了后端也要能启动（哪怕连不上 DB 就重试）。

> 「确保docker正常启动，哪怕里面的代码坏了」

⇒ 容器进程（JVM/entrypoint）本身不因业务层异常而退出。用启动包装脚本 + `restart: always` 让 Docker 层独立于业务健康。

### `-f` flag path resolution pitfall

When using `-f docker/docker-compose.yml`, Docker Compose resolves `./` relative paths in volumes/contexts **relative to the compose file's directory** (`docker/`), NOT the current working directory:

```yaml
# In docker/docker-compose.yml:
volumes:
  - ./init.sql:/docker-entrypoint-initdb.d/01-init.sql:ro   # resolves to docker/init.sql
  - ${LOG_DIR:-./logs}/backend:/app/logs                     # resolves to docker/logs/backend
```

This can silently create wrong directories (e.g. `docker/logs/backend/` instead of `logs/backend/`). Fixes:

1. **Use absolute paths with LOG_DIR:** `LOG_DIR="$(pwd)/logs" docker compose -f docker/docker-compose.yml up -d`
2. **Or reference parent paths:** `../init.sql` for files at the project root
3. **Or run `docker compose up -d` from the project root without `-f`** (but only works if the compose file is at the root)

**Rule of thumb:** If the compose file is in a subdirectory, all relative paths must account for the offset. Best practice — keep the compose file at the project root, or use a wrapper script that sets LOG_DIR to an absolute path.

### `\` line continuation inside `"..."` strings (bash pitfall)

When writing curl commands in bash scripts with `\` line continuations, closing `"` before the `\` is critical:

```bash
# BROKEN: the backslash continues the COMMAND LINE, not the string.
# The " on the next line closes the string opened on this line.
# Everything before the next " becomes mixed quoted/unquoted.
curl -H "Authorization: Bearer *** \   # ← " NEVER CLOSED
  -H "Content-Type: application/json" \   # ← the " HERE closes line 1's string
  -d '{"key":"value"}' \                  # ← now this runs outside any string
  https://api.example.com/endpoint

# FIXED: close the string before the backslash
curl -H "Authorization: Bearer ***" \  # ← " properly closed
  -H "Content-Type: application/json" \
  -d '{"key":"value"}' \
  https://api.example.com/endpoint
```

**Detection:** If `bash -n script.sh` reports "syntax error near unexpected token" at the `case` statement or end of file, look for unclosed `"` inside `$(...)` with `\` continuations. The error is often reported far from the actual culprit.

### Nginx Alpine healthcheck: use `curl`, not `wget`

In `nginx:alpine` images, the `wget` command (from BusyBox) can fail to connect to `http://localhost/` even though nginx is running. `curl` works reliably:

```dockerfile
# BROKEN: wget returns "Connection refused" from inside nginx:alpine
HEALTHCHECK CMD wget -qO- http://localhost/ || exit 1

# FIXED: use curl instead
HEALTHCHECK CMD curl -sf http://localhost/ || exit 1
```

The root cause appears to be BusyBox wget's IPv6 resolution or socket handling with nginx's multi-worker architecture. Curl handles this correctly.

### ❌ `depends_on` 耦合（最常见的问题）

```yaml
# ❌ 错误的做法
services:
  backend:
    depends_on: [mysql]   # MySQL 崩了 → backend 也不启动
    restart: unless-stopped

# ✅ 正确的做法
services:
  backend:
    restart: always        # 独立重启，无限重试
    # 没有 depends_on — 容器启动后自行等待/重试连 DB
```

**为什么去掉 `depends_on` 安全：** Spring Boot / 多数框架自带重试机制，启动后 JDBC 连接失败不会导致进程退出，而是反复重试。`depends_on` 只带来一个风险：基础设施挂了 = 应用容器也不启动。

### ❌ `|| exit 1` 在 HEALTHCHECK 中

```dockerfile
# ❌ 错误的做法
HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1
# ↑ exit 1 不会杀人容器，但 Docker 的 restart policy 在容器不退出时不管用
# 而且 healthcheck + unhealthy 状态会让 orchestration 平台停止路由

# ✅ 正确的做法
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8080/health
# ↑ 纯监控：健康检查失败只标记 unhealthy，不 exit
```

### ✅ 启动包装脚本

```dockerfile
# Dockerfile
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]
```

```bash
#!/bin/bash
# docker-entrypoint.sh — 确保容器不因代码异常退出
set -e

echo "[entrypoint] Starting application..."

# 无限重试循环：DB 连不上或代码抛异常 → 等一会儿再重启
while true; do
  java -Xms256m -Xmx512m -jar /app/app.jar
  EXIT_CODE=$?
  echo "[entrypoint] Application exited with code $EXIT_CODE, restarting in 5s..."
  sleep 5
done
```

### restart policy 选择

| Policy | 行为 | 适用场景 |
|--------|------|---------|
| `no` | 从不重启 | 一次性任务 |
| `always` | 任何 exit code 都重启（包括 exit 0） | **生产应用**（推荐） |
| `unless-stopped` | 非手动停止的都重启 | 开发环境 |
| `on-failure[:max-retries]` | 仅非零 exit code 重启 | 批处理任务 |

**生产推荐：** `restart: always` + 启动包装脚本。这样包装脚本的 `while true` 兜住业务异常，`always` 兜住 VM/内核级别异常。

### docker-compose.yml 生产模板

```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: enterprise-mysql
    restart: always            # 独立重启
    environment:
      MYSQL_DATABASE: ${DB_NAME:-enterprise}
      MYSQL_USER: ${DB_USER:-app}
      MYSQL_PASSWORD: ${DB_PASS:-app123}
      MYSQL_ROOT_PASSWORD: ${ROOT_PASS:-root123}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  backend:
    build:
      context: ./backend
    container_name: enterprise-backend
    restart: always            # 和 MySQL 无关的独立重启
    # 没有 depends_on — 各自独立，不耦合
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/enterprise?autoReconnect=true
      SPRING_DATASOURCE_USERNAME: ${DB_USER:-app}
      SPRING_DATASOURCE_PASSWORD: ${DB_PASS:-app123}
    ports:
      - "8080:8080"
    volumes:
      - uploads_data:/app/uploads

volumes:
  mysql_data:
  uploads_data:
```

## Check for Cached Downloads First

Before downloading anything, check `~/Downloads/` and nearby directories — user keeps installers locally:
```bash
ls ~/Downloads/*Docker* ~/Downloads/*docker* 2>/dev/null
find ~/Downloads -name "*Docker*" -o -name "*docker*" 2>/dev/null | head -5
```

This applies to: Docker Desktop installer, OpenSSH ZIP, ISO files, etc.

## Copy to Non-Default Windows Drive via Temporary SMB Share

When the target file is on a non-C drive (e.g. F:\), create a temp admin share, mount, copy, unmount:

```bash
# 1. Create temp share on Windows
ssh user@host "net share F$=F:\ /GRANT:everyone,FULL"

# 2. Mount on Mac
mkdir -p /tmp/mnt/f
mount_smbfs //user:password@host/F$ /tmp/mnt/f

# 3. Copy file
cp /path/to/file /tmp/mnt/f/destination/

# 4. Clean up
umount /tmp/mnt/f
ssh user@host "net share F$ /delete"
```

## DNS-less Environment: hardcode API endpoints in docker-compose

When the target server has no DNS resolution (firewall blocks outbound DNS, or the VM's DNS is deliberately disabled), containers cannot resolve hostnames like `dashscope.aliyuncs.com`. Fix this with `extra_hosts` **in the docker-compose.yml itself** — not as a post-deploy manual step.

### Pattern: YAML anchor for shared extra_hosts

```yaml
# Define once
x-common-hosts: &common-hosts
  extra_hosts:
    - "api.example.com:203.0.113.10"
    - "api.example.com:203.0.113.11"

services:
  backend:
    <<: *common-hosts      # inject into each service that needs it
  worker:
    <<: *common-hosts
```

### DNS resolution for the compose file

Before writing `extra_hosts`, resolve the domain(s) from a machine that HAS DNS:

```bash
# Get all A records for the target domain
dig api.example.com A +short
# → 203.0.113.10
# → 203.0.113.11
```

Add ALL returned IPs — the hosting provider's GTM/CDN may use any of them.

### Compose `image:` + `build:` dual-declaration for offline deployment

当离线部署时（预编译 JAR + `docker load` 导入镜像），docker-compose.yml 须同时声明 `image:` 和 `build:`：

```yaml
services:
  backend:
    image: enterprise-backend:latest    # ← 告知 Compose 期望的镜像名
    build:                               # ← 保留构建信息（联网时可用）
      context: .
      dockerfile: docker/Dockerfile.backend
```

**为什么这样做：**

Docker Compose 的 `up` 行为是：
1. 先查本地是否已有 `image:` 标签的镜像
2. 有 → 直接启动，**跳过 build**
3. 无 → 执行 build → 构建新镜像 → 启动

离线部署时 `docker load` 导入了镜像，Compose 发现 tag 已存在，秒级启动。有网络环境（CI/CD）时 build 生效，自动重新构建。

**不要只写 `build:` 不写 `image:`** — Compose 会为没有 `image:` 的服务自动生成随机 tag，永远无法匹配 pre-loaded 镜像。

### Principle: pre-configure, don't document as manual steps

> User feedback: "你应该直接在docker-compose.yml里写好extra_hosts，只是提示一下同事。这些前期能做的事情就做好。"

If a configuration step is known and deterministic at authoring time, **put it in the code**. Don't write "before running, edit the compose file and add X" — that creates a manual step that will be forgotten, and the new person inheriting the project will encounter a broken setup and have to debug it. Instead:

- **Known IPs** → write them into `extra_hosts` directly
- **Known env vars** → set defaults in `environment:` with `${VAR:-default}` fallback
- **Known paths** → hardcode them, or use a single `.env` file
- **Build-time constants** → embed them in the Dockerfile

The only things that should remain as "manual steps" are truly environment-specific secrets: API keys, passwords, per-deployment URLs that change between staging and production.

### `extra_hosts` multiline failover behavior

When multiple `extra_hosts` entries target the **same hostname**, Docker appends each one as a separate line in the container's `/etc/hosts` — it does NOT overwrite:

```yaml
extra_hosts:
  - "api.example.com:203.0.113.10"
  - "api.example.com:203.0.113.11"
```

Results in:
```
203.0.113.10  api.example.com
203.0.113.11  api.example.com
```

**How failover works:**

| Tool | Behavior |
|------|----------|
| `getent hosts` / `ping` | Only the first IP is used |
| `curl` / wget | Happy eyeballs — tries first, falls back on connect failure |
| Java `InetAddress.getByName()` | Returns only the first |
| Java `InetAddress.getAllByName()` | Returns ALL IPs in order |
| Spring RestClient / `HttpURLConnection` | Tries each IP sequentially at the TCP level — connection timeout → next IP |

**Java's HTTP client failover is at the TCP connect layer, not the HTTP layer.** If the first IP's port is open but returns a wrong response (e.g. an unrelated server that happens to listen on 443), Java will not retry — it got a TCP connection, so it sends the HTTP request and receives the response. The 200/400/500 response is an application-level outcome, not a transport failure. Only TCP connection failures (connection refused, connection timeout) trigger failover to the next IP.

**Verification:**

```bash
# Check what's actually in /etc/hosts
docker run --rm --add-host api.example.com:1.2.3.4 --add-host api.example.com:5.6.7.8 alpine cat /etc/hosts | grep api.example

# Check which IP getaddrinfo returns first
docker run --rm --add-host api.example.com:1.2.3.4 --add-host api.example.com:5.6.7.8 alpine getent hosts api.example.com
# → 1.2.3.4  (only the first!)
```

### USB Drive Deployment Pattern

When the target server has **no network at all** (air-gapped, no SSH, no SMB, no physical network), transfer via USB:

```bash
# 1. On dev machine: copy project to USB
cp -r /path/to/project /Volumes/USB_DRIVE/

# 2. On target server console: copy from USB to install path
cp -r /media/USB_DRIVE/project /opt/project

# 3. Run install script
cd /opt/project && sudo bash install.sh
```

**Key differences from SMB/SSH deployment:**
- No `ssh`/`scp` commands — all work happens at the server's physical console
- The entire project directory (including `.env`, docker images, scripts) must be self-contained
- `install.sh` must create `.env` from `.env.example` if it doesn't exist (`.env` is gitignored)
- Offline image tarballs (`deployment/docker-images/*.tar`) must travel alongside the code
- `install.sh` must handle Docker engine installation from a local tarball (`docker-27.5.1.tgz`), not from the internet

**Documentation principle:** If the deployment workflow is USB-only, remove ALL ssh/scp commands from deployment docs. Don't leave stale "or you can SSH" alternatives — the first-time deployer will try them and waste time.

### Compose file audit: detect orphaned / conflicting configs

When a project accumulates multiple docker-compose files, containers with conflicting versions can start silently. The audit pattern:

1. **List all compose files** — `find . -name "docker-compose*.yml" -not -path './.git/*'`
2. **Identify the canonical one** — trace each startup script (install.sh, start.sh, CLI tool) to see which compose file each one uses
3. **Check for version conflicts** — compare `image:` tags across compose files (e.g. `mysql:8.0` vs `mysql:8.4`)
4. **Check for container name conflicts** — different compose files may define containers with different names (e.g. `enterprise-db` vs `enterprise-mvp-mysql`) both trying to bind port 3306
5. **Remove orphans** — delete compose files not referenced by any active script

```bash
# Audit script
echo "=== All compose files ==="
find . -name "docker-compose*.yml" | grep -v ".git/"

echo "=== Who references which ==="
grep -rn "docker-compose\.yml\|docker-compose\.prod" --include="*.sh" . | grep -v ".git/"

echo "=== MySQL image versions ==="
grep -rn "image: mysql:" --include="*.yml" . | grep -v ".git/"

echo "=== Container names ==="
grep -rn "container_name:" --include="*.yml" . | grep -v ".git/"
```

**Pitfall:** A compose file may be orphaned (unreferenced by any active script) but still be runnable directly by a user who types `docker compose up -d` from the root directory. Either delete orphans or add a `.gitignore` entry to prevent accidental use.

### Install script env var setup for offline deployment

When deploying offline (air-gapped VM), `.env` files don't travel with the git repo (they're gitignored because they contain secrets). The install script must handle this:

```bash
# In install.sh — before docker compose up

ENV_DIR="$PROJECT_ROOT/docker"
ENV_FILE="$ENV_DIR/.env"
ENV_EXAMPLE="$ENV_DIR/.env.example"

# Create .env if missing
if [ ! -f "$ENV_FILE" ]; then
  if [ -f "$ENV_EXAMPLE" ]; then
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    echo "Warnings: .env created from .env.example"
    echo "Please edit .env to set the API Key"
  fi
fi

# Check for placeholder values
if [ -f "$ENV_FILE" ]; then
  KEY=$(grep "^API_KEY=" "$ENV_FILE" | sed 's/^API_KEY=//')
  if [ -z "$KEY" ] || [ "$KEY" = "sk-you...here" ]; then
    echo "Warning: API_KEY not set or still placeholder"
  fi
fi
```

**Principle:** Never let `docker compose up` start with placeholder or empty environment values. Detect and warn before starting.

### Spring Boot env var chain: .env to compose to application.yml

For Spring Boot apps deployed via Docker Compose, the env var chain has several hops that must all align:

```
docker/.env (gitignored, real values)
    -> Docker Compose auto-loads .env from compose file directory
    -> container environment variables (docker-compose.yml environment: section)
    -> application.yml ${VAR_NAME:default} SPEL references
    -> @ConfigurationProperties(prefix="...") Java POJO
```

**Each hop must use the SAME variable name.** Common mismatch that breaks the chain:

```yaml
# docker-compose.yml — passes env var to container
services:
  backend:
    environment:
      AI_VISION_KEY: ${AI_VISION_KEY:-}   # <- this name
```

```yaml
# application.yml — reads env var via SPEL
ai:
  vision:
    api-key: ***            # <- must match docker-compose name
    base-url: ${AI_VISION_URL:}
    model: ${AI_VISION_MODEL:}
```

```java
// VisionProperties.java — Spring binds ai.vision.* via relaxed naming
@Component
@ConfigurationProperties(prefix = "ai.vision")
public class VisionProperties {
    private String apiKey;   // <- matches ai.vision.api-key in yaml
    private String baseUrl;  // <- matches ai.vision.base-url in yaml
}
```

**Common failure #1:** A developer puts `api-key: *** (literal placeholder) in application.yml thinking it will be overridden by env var. But if the env var name doesn't match what Spring expects (e.g. `AI_VISION_KEY` vs `AI_VISION_APIKEY`), the literal placeholder is used. **Always use `${VAR_NAME:}` SPEL syntax** in application.yml for env vars.

**Common failure #2 (check-ai CLI pattern):** A diagnostic CLI tries to read `AI_VISION_KEY` from `docker-compose.yml` with grep/sed. But `${AI_VISION_KEY:-}` is a variable *reference*, not a value — `grep` + `sed 's/.*${//;s/:-.*//'` yields the *variable name* `AI_VISION_KEY` as the extracted value. The actual value is in `docker/.env`. **Always read from `.env` for diagnostic scripts, not from compose files.**

**Verification:** After deployment, check the value is flowing:

```bash
# Inside container, check env vars are present
docker exec <container> sh -c "echo \$AI_VISION_KEY" | head -c10

# Check Spring Boot actuator (if enabled)
curl -s http://localhost:8080/actuator/env/ai.vision.api-key | python3 -m json.tool
```

### Reference file pattern for repeating IP sets

When the same set of IPs is needed across multiple compose files (dev compose, prod compose, deployment/docker/compose), create a small `references/` file documenting the resolved IPs so future readers know where they came from:

```bash
# Example: docs/references/dashscope-ip-mapping.md
# Resolved 2026-06-29 from 114.114.114.114
# dashscope.aliyuncs.com → gtm-cn-rt54j1mlg03.dashscope.aliyuncs.com
#   → 8.152.159.24
#   → 39.96.198.249
#   → 8.140.217.18
#   → 39.96.213.166
```

## Offline Deployment Package (Air-Gapped VM)

When the target VM has no DNS / no internet, create a self-contained offline tarball containing Docker engine + docker-compose + all images:

```bash
# 1. Build/collect all images on the build machine
docker save enterprise-backend:latest -o /tmp/offline/images/enterprise-backend.tar
docker save enterprise-frontend:latest -o /tmp/offline/images/enterprise-frontend.tar
docker save mysql:8.0 -o /tmp/offline/images/mysql-8.0.tar

# 2. Download Docker engine binary (for target arch)
curl -fsSL -o /tmp/offline/docker/docker.tgz \
  "https://download.docker.com/linux/static/stable/x86_64/docker-27.5.1.tgz"

# 3. Download docker-compose (for target arch)
curl -fsSL -o /tmp/offline/docker/docker-compose \
  "https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-linux-x86_64"
chmod +x /tmp/offline/docker/docker-compose

# 4. Package everything
cd /tmp && tar czf enterprise-offline.tar.gz offline/

# 5. Transfer via SMB
smbclient "//host/Users" -U "user%password" \
  -c 'cd user\\Desktop; put /tmp/enterprise-offline.tar.gz enterprise-offline.tar.gz'
```

On the target VM:
```bash
cd /opt && tar xzf /path/to/enterprise-offline.tar.gz
# Load images
docker load -i images/enterprise-backend.tar
docker load -i images/enterprise-frontend.tar
docker load -i images/mysql-8.0.tar

# Install Docker engine (if not present)
tar xzf docker/docker.tgz -C /usr/local/bin/ --strip-components=1
cp docker/docker-compose /usr/local/bin/
```

**⚠️ GitHub downloads can time out** — use `--max-time 300` or python's `urllib.request.urlretrieve()` which handles large files better. Docker engine (~76MB) and docker-compose (~64MB) are large downloads that may fail on slow proxies — retry with `-C -` for resume.

## Transfer Docker Image via SMB + SSH

When building on macOS but deploying to a remote machine (Windows/ThinkPad), use SMB + SSH:

```bash
# 1. Build image (local, Mac)
docker save myimage:latest -o /tmp/myimage.tar

# 2. Mount SMB share to target
mount_smbfs //user:password@host/share /path/to/mountpoint

# 3. Copy image tar via SMB
cp /tmp/myimage.tar /path/to/mountpoint/Desktop/

# 4. Load via SSH on target
ssh user@host "docker load -i %USERPROFILE%\\Desktop\\myimage.tar"
```

**Avoid re-downloading:** Check local ~/Downloads/ for cached files before downloading. User keeps installers locally.

## Windows Docker Desktop Quirks

### Docker Engine Won't Start via SSH
Docker Desktop on Windows needs an interactive GUI session. SSH sessions run as SYSTEM. Patterns:

```bash
# Step 1: Start the service
ssh user@host "net start com.docker.service"

# Step 2: Start Docker Desktop (needs GUI login - tell user to open it)
# User: double-click Docker Desktop tray, wait for whale to stabilize

# Step 3: Load image after engine is up
ssh user@host "docker load -i \"C:\\Users\\user\\Desktop\\image.tar\""
```

### docker-users Group
If Docker Desktop says "user is not a member of the group":
```powershell
Add-LocalGroupMember -Group "docker-users" -Member "username"
# Then log OFF and back ON for change to take effect
```

### Hyper-V vs WSL2 Backend
- Check Hyper-V: `Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V`
- If Hyper-V enabled but `vmcompute` service missing (Windows Insider builds) → use WSL2 backend
- Docker Settings → General → "Use the WSL 2 based engine"
- WSL install: `wsl --install -d Ubuntu` (can be slow, 5-10 min)

## Cross-arch Docker Build (macOS ARM → x86_64)

在 ARM Mac 上构建 x86_64 Docker 镜像，用于部署到 x86_64 Linux 服务器。

### 方案：Colima + QEMU（经验证可靠）

```bash
# 1. 安装依赖
brew install colima qemu docker docker-compose docker-buildx
brew install lima-additional-guestagents  # 必须！否则 colima x86_64 报 guest agent 缺失
```

### 2. 启动 Colima x86_64 VM

```bash
colima start --arch x86_64 --cpu 4 --memory 8
# 首次启动耗时 ~5-10 分钟（下载 VM 镜像 + 拉 Docker 基础镜像）
# ⚠️ 如果报 "guest agent binary could not be found for Linux-x86_64"
# → 安装 lima-additional-guestagents 后再试
```

### 3. 切换 Docker context

```bash
docker context use colima
docker info --format '{{.OSType}}/{{.Architecture}}'
# → linux/x86_64  (确认是 x86 架构)
```

### 4. 构建镜像

```bash
# 先本地编译 JAR
export JAVA_HOME=/opt/homebrew/opt/openjdk
cd backend
mvn clean package -DskipTests

# 构建 Docker 镜像
cd ..
docker-compose build backend
```

### 5. 验证架构

```bash
docker inspect enterprise-backend:latest --format '{{.Os}}/{{.Architecture}}'
# → linux/amd64  (确认是 x86_64)
```

### Pitfalls

- **lima-additional-guestagents 缺失** — Colima 启动 x86_64 VM 时会报 `guest agent binary could not be found for Linux-x86_64`。安装 `brew install lima-additional-guestagents` 即可
- **`docker compose` vs `docker-compose`** — Colima 环境中的 Docker CLI 可能不包含 `docker compose` 插件。需要 `brew install docker-compose` 然后用 `docker-compose` 命令，或装 docker-buildx 插件
- **认证配置冲突** — Colima 启动后会创建 Docker context，而 macOS 上原有的 `~/.docker/config.json` 可能有 `credsStore: "desktop"`（指向 Docker Desktop，但 Docker Desktop 未安装）。修复：将 `credsStore` 设为空字符串 `""`，或删掉这行
- **代理转发** — Colima 会自动检测宿主机的 `http_proxy` 环境变量并转发到 VM 内（将 `127.0.0.1:1082` 重写为 `192.168.5.2:1082`）。如果不需要 VM 内用代理，启动前 `unset http_proxy https_proxy`
- **x86_64 emulation 性能** — 通过 QEMU 模拟运行的 x86_64 容器比原生 ARM 慢，Spring Boot 应用启动约慢 3-5 倍。常规开发仍用本地 JVM (ARM)，只打包时才走 Colima
- **用完关闭** — `colima stop` 停掉 VM 释放资源。`colima delete` 彻底删除（下次需要重新下载镜像）
