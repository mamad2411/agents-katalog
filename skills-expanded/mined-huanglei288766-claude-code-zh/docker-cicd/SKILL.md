---
name: docker-cicd
description: Docker 容器化与 CI/CD 流水线最佳实践，涵盖 Dockerfile 优化、docker-compose 编排、GitHub Actions 部署、镜像管理
version: "1.0"
---

# Docker + CI/CD 实践

## 概述

本 Skill 提供 Docker 容器化和 CI/CD 流水线的完整实践指南，包含 Dockerfile 最佳实践、开发环境编排、GitHub Actions 自动化部署等。

适用场景：
- 编写高效安全的 Dockerfile
- 搭建本地开发环境（MySQL + Redis + ES + 应用）
- 构建 GitHub Actions CI/CD 流水线
- 制定镜像版本管理策略

---

## Dockerfile 最佳实践

### 多阶段构建（Java Spring Boot）

```dockerfile
# ===== 第一阶段：构建 =====
FROM maven:3.9-eclipse-temurin-21-alpine AS builder

WORKDIR /build

# 先拷贝 pom.xml，利用 Docker 缓存层加速依赖下载
COPY pom.xml .
RUN mvn dependency:go-offline -B

# 拷贝源码并构建
COPY src ./src
RUN mvn package -DskipTests -B \
    && java -Djarmode=layertools -jar target/*.jar extract --destination extracted

# ===== 第二阶段：运行 =====
FROM eclipse-temurin:21-jre-alpine AS runtime

# 安全：创建非 root 用户
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# 按变化频率从低到高拷贝分层（充分利用缓存）
COPY --from=builder /build/extracted/dependencies/ ./
COPY --from=builder /build/extracted/spring-boot-loader/ ./
COPY --from=builder /build/extracted/snapshot-dependencies/ ./
COPY --from=builder /build/extracted/application/ ./

# 使用非 root 用户运行
USER appuser

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD wget -qO- http://localhost:8080/actuator/health || exit 1

# JVM 参数优化：容器感知内存限制
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:InitialRAMPercentage=50.0"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS org.springframework.boot.loader.launch.JarLauncher"]
```

### 多阶段构建（Node.js）

```dockerfile
# ===== 第一阶段：安装依赖 =====
FROM node:20-alpine AS deps

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

# ===== 第二阶段：构建 =====
FROM node:20-alpine AS builder

WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN corepack enable && pnpm build

# ===== 第三阶段：运行 =====
FROM node:20-alpine AS runtime

# 安全：非 root 用户
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# 只拷贝生产依赖和构建产物
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package.json ./

USER appuser
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```

### 镜像瘦身原则

```dockerfile
# 1. 使用 alpine 基础镜像（体积最小）
FROM eclipse-temurin:21-jre-alpine    # 约 100MB vs 标准版 300MB+

# 2. 合并 RUN 指令，减少层数
RUN apk add --no-cache curl tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata

# 3. 使用 .dockerignore 排除无关文件
# .dockerignore 内容：
# .git
# .idea
# target/
# node_modules/
# *.md
# docker-compose*.yml
# .env*

# 4. 清理构建缓存
RUN mvn package -DskipTests \
    && rm -rf ~/.m2/repository    # 多阶段构建时非最终阶段可清理

# 5. 不安装不必要的包
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps
```

### 安全扫描

```bash
# 使用 Trivy 扫描镜像漏洞
trivy image --severity HIGH,CRITICAL myapp:latest

# 使用 Hadolint 检查 Dockerfile 规范
hadolint Dockerfile

# 使用 Dockle 检查容器最佳实践
dockle myapp:latest

# 在 CI 中集成扫描（见 GitHub Actions 章节）
```

---

## docker-compose 开发环境编排

### 完整开发环境

```yaml
# docker-compose.yml — 本地开发环境
version: "3.8"

services:
  # ===== 应用服务 =====
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder    # 开发时使用构建阶段，方便调试
    ports:
      - "8080:8080"
      - "5005:5005"      # 远程调试端口
    environment:
      - SPRING_PROFILES_ACTIVE=dev
      - SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/mydb?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Shanghai
      - SPRING_DATASOURCE_USERNAME=root
      - SPRING_DATASOURCE_PASSWORD=dev123456
      - SPRING_DATA_REDIS_HOST=redis
      - SPRING_DATA_REDIS_PORT=6379
      - SPRING_ELASTICSEARCH_URIS=http://elasticsearch:9200
      - JAVA_OPTS=-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005
    volumes:
      - ./src:/build/src       # 挂载源码，支持热重载
      - maven-cache:/root/.m2  # 缓存 Maven 依赖
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
      elasticsearch:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped

  # ===== MySQL =====
  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: dev123456
      MYSQL_DATABASE: mydb
      MYSQL_CHARSET: utf8mb4
      MYSQL_COLLATION: utf8mb4_unicode_ci
      TZ: Asia/Shanghai
    volumes:
      - mysql-data:/var/lib/mysql
      - ./docker/mysql/init:/docker-entrypoint-initdb.d  # 初始化 SQL
      - ./docker/mysql/conf:/etc/mysql/conf.d             # 自定义配置
    command: >
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --max-connections=200
      --innodb-buffer-pool-size=256M
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-pdev123456"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - app-network
    restart: unless-stopped

  # ===== Redis =====
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: >
      redis-server
      --requirepass dev123456
      --maxmemory 256mb
      --maxmemory-policy allkeys-lru
      --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "dev123456", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - app-network
    restart: unless-stopped

  # ===== Elasticsearch =====
  elasticsearch:
    image: elasticsearch:8.12.0
    ports:
      - "9200:9200"
      - "9300:9300"
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
      - TZ=Asia/Shanghai
    volumes:
      - es-data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - app-network
    restart: unless-stopped

  # ===== Kibana（可选，ES 可视化） =====
  kibana:
    image: kibana:8.12.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - app-network
    profiles:
      - debug    # 仅在 docker compose --profile debug up 时启动

volumes:
  mysql-data:
  redis-data:
  es-data:
  maven-cache:

networks:
  app-network:
    driver: bridge
```

### 常用命令

```bash
# 启动所有服务
docker compose up -d

# 启动含可选服务（如 Kibana）
docker compose --profile debug up -d

# 查看日志
docker compose logs -f app

# 仅重建应用服务
docker compose up -d --build app

# 清理所有数据卷（慎用）
docker compose down -v

# 进入容器调试
docker compose exec mysql mysql -u root -pdev123456 mydb
docker compose exec redis redis-cli -a dev123456
```

---

## GitHub Actions CI/CD 流水线

### 完整流水线配置

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  # 支持手动触发
  workflow_dispatch:

# 同一分支只保留最新的一次运行
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  JAVA_VERSION: "21"

jobs:
  # ===== 阶段一：代码检查 =====
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 设置 Java 环境
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: ${{ env.JAVA_VERSION }}
          cache: maven

      - name: 代码风格检查
        run: mvn checkstyle:check -B

      - name: Dockerfile 规范检查
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile

  # ===== 阶段二：测试 =====
  test:
    runs-on: ubuntu-latest
    needs: lint
    services:
      # 集成测试依赖的服务
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: test123456
          MYSQL_DATABASE: testdb
        ports:
          - 3306:3306
        options: >-
          --health-cmd="mysqladmin ping -h localhost"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd="redis-cli ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5
    steps:
      - uses: actions/checkout@v4

      - name: 设置 Java 环境
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: ${{ env.JAVA_VERSION }}
          cache: maven

      - name: 运行单元测试和集成测试
        run: mvn verify -B -Dspring.profiles.active=test
        env:
          SPRING_DATASOURCE_URL: jdbc:mysql://localhost:3306/testdb
          SPRING_DATASOURCE_USERNAME: root
          SPRING_DATASOURCE_PASSWORD: test123456
          SPRING_DATA_REDIS_HOST: localhost

      - name: 上传测试报告
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-reports
          path: target/surefire-reports/

      - name: 上传覆盖率报告
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: target/site/jacoco/

  # ===== 阶段三：构建并推送镜像 =====
  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'    # 仅 push 时构建镜像
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.version }}
    steps:
      - uses: actions/checkout@v4

      - name: 登录容器仓库
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: 生成镜像标签
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            # 分支名 + 短 SHA
            type=sha,prefix={{branch}}-
            # 语义化版本（基于 git tag）
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            # latest 标签仅在 main 分支
            type=raw,value=latest,enable={{is_default_branch}}

      - name: 构建并推送镜像
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: 安全扫描镜像
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.meta.outputs.version }}
          format: table
          severity: HIGH,CRITICAL
          exit-code: 1    # 发现高危漏洞则失败

  # ===== 阶段四：部署到测试环境 =====
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment: staging
    steps:
      - name: 部署到测试环境
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          script: |
            cd /opt/app
            export IMAGE_TAG=${{ needs.build.outputs.image-tag }}
            docker compose pull app
            docker compose up -d app
            # 等待健康检查通过
            timeout 60 bash -c 'until curl -f http://localhost:8080/actuator/health; do sleep 2; done'

  # ===== 阶段五：部署到生产环境 =====
  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production    # 需要手动审批
    steps:
      - name: 部署到生产环境
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/app
            export IMAGE_TAG=${{ needs.build.outputs.image-tag }}
            # 滚动更新
            docker compose pull app
            docker compose up -d --no-deps app
            timeout 120 bash -c 'until curl -f http://localhost:8080/actuator/health; do sleep 3; done'
```

---

## 镜像版本管理策略

### Tag 规范

```
# 格式：{仓库}/{项目}:{标签}
ghcr.io/myorg/myapp:latest            # 最新稳定版（仅 main 分支）
ghcr.io/myorg/myapp:1.2.3             # 语义化版本（推荐生产使用）
ghcr.io/myorg/myapp:1.2               # 主次版本（自动获取最新 patch）
ghcr.io/myorg/myapp:main-a1b2c3d      # 分支 + commit SHA
ghcr.io/myorg/myapp:develop-a1b2c3d   # 开发分支 + commit SHA
```

### 版本管理规则

```
规则                                  说明
─────────────────────────────────────────────────────────────
生产环境必须用具体版本号              禁止使用 latest
测试环境使用 branch-sha 格式          便于追溯
基础镜像锁定版本                      FROM node:20.11.1-alpine（非 latest）
定期更新基础镜像                      修复已知漏洞
镜像保留策略                          保留最近 30 个版本，定期清理旧镜像
```

### 自动化版本发布

```yaml
# .github/workflows/release.yml — 基于 tag 自动发布
name: Release

on:
  push:
    tags:
      - "v*.*.*"    # 匹配 v1.0.0 格式

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 提取版本号
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: 构建并推送正式版镜像
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ steps.version.outputs.VERSION }}
            ghcr.io/${{ github.repository }}:latest

      - name: 创建 GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
```

---

## 容器健康检查

### Spring Boot Actuator 健康检查

```java
// 自定义健康检查指标
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    private final DataSource dataSource;

    public DatabaseHealthIndicator(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Health health() {
        try (Connection conn = dataSource.getConnection()) {
            // 执行简单查询验证连接可用
            conn.createStatement().execute("SELECT 1");
            return Health.up()
                    .withDetail("database", "MySQL")
                    .withDetail("status", "连接正常")
                    .build();
        } catch (Exception e) {
            return Health.down()
                    .withDetail("database", "MySQL")
                    .withDetail("error", e.getMessage())
                    .build();
        }
    }
}
```

```yaml
# application.yml — 健康检查配置
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: when-authorized   # 仅授权用户可见详情
      probes:
        enabled: true                 # 启用 K8s 探针
  health:
    # 各组件健康检查开关
    db:
      enabled: true
    redis:
      enabled: true
    elasticsearch:
      enabled: true
    diskspace:
      enabled: true
      threshold: 100MB               # 磁盘空间阈值
```

### Docker Compose 健康检查模式

```yaml
# 健康检查最佳实践
services:
  app:
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8080/actuator/health/liveness || exit 1"]
      interval: 30s       # 检查间隔
      timeout: 3s         # 超时时间
      retries: 3          # 连续失败几次标记为不健康
      start_period: 60s   # 启动宽限期（JVM 启动较慢）

  # 依赖健康检查实现启动顺序控制
  worker:
    depends_on:
      app:
        condition: service_healthy
      mysql:
        condition: service_healthy
```

---

## .dockerignore 模板

```
# 版本控制
.git
.gitignore

# IDE
.idea
.vscode
*.iml

# 构建产物
target/
dist/
build/
node_modules/

# 文档
*.md
LICENSE
docs/

# Docker 自身配置
Dockerfile*
docker-compose*
.dockerignore

# 环境变量（敏感信息）
.env
.env.*

# 测试
test/
tests/
__tests__/
coverage/
.nyc_output/

# CI/CD
.github/
.gitlab-ci.yml
Jenkinsfile

# OS 文件
.DS_Store
Thumbs.db
```

---

## 常见问题速查

| 问题 | 解决方案 |
|------|---------|
| 镜像体积过大 | 使用多阶段构建 + alpine 基础镜像 |
| 构建缓慢 | 合理利用缓存层，先 COPY 依赖文件再 COPY 源码 |
| 容器时区不对 | 设置 `TZ=Asia/Shanghai` 环境变量 |
| 容器内无法连接宿主机服务 | 使用 `host.docker.internal`（macOS/Windows） |
| compose 服务启动顺序 | 使用 `depends_on` + `condition: service_healthy` |
| 生产环境用了 latest 标签 | 改为具体版本号，CI 中自动生成 tag |
| 镜像有安全漏洞 | 集成 Trivy 扫描，更新基础镜像 |
| 日志未持久化 | 使用日志驱动或挂载卷 |
