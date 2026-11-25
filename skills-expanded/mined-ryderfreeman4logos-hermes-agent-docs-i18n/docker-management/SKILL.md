---
name: docker-management
description: Manage Docker containers, images, volumes, and Compose.
version: 1.0.0
author: sprmn24
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [docker, containers, devops, infrastructure, compose, images, volumes, networks, debugging]
    category: devops
    requires_toolsets: [terminal]
---

# Docker 管理

通过标准的 Docker CLI 命令来管理 Docker 容器、镜像、卷、网络以及 Compose 集群。除 Docker 本身外无需其他依赖。

## 适用场景

- 运行、停止、重启、删除或检查容器
- 构建、拉取、推送、标记 Docker 镜像或清理旧镜像
- 使用 Docker Compose 管理多服务集群
- 管理卷或网络配置
- 调试崩溃的容器或分析日志
- 查看 Docker 磁盘使用情况并释放空间
- 审查或优化 Dockerfile

## 先决条件

- 已安装并运行 Docker 引擎
- 用户已添加到 `docker` 组（或使用 `sudo` 权限）
- 安装了 Docker Compose v2（现代 Docker 安装版本均包含）

快速检查：

```bash
docker --version && docker compose version
```

## 快速参考

| 操作 | 命令 |
|------|---------|
| 运行容器（后台） | `docker run -d --name NAME IMAGE` |
| 停止并删除 | `docker stop NAME && docker rm NAME` |
| 查看日志（实时跟踪） | `docker logs --tail 50 -f NAME` |
| 进入容器终端 | `docker exec -it NAME /bin/sh` |
| 列出所有容器 | `docker ps -a` |
| 构建镜像 | `docker build -t TAG .` |
| 启动 Docker Compose 服务 | `docker compose up -d` |
| 停止 Docker Compose 服务 | `docker compose down` |
| 查看磁盘使用情况 | `docker system df` |
| 清理无用资源 | `docker image prune && docker container prune` |

## 操作步骤

### 1. 确定所属领域

首先判断请求属于以下哪个范畴：

- **容器生命周期管理** → 运行、停止、启动、重启、删除、暂停/取消暂停
- **容器交互操作** → 进入容器终端、复制文件、查看日志、检查状态、获取统计信息
- **镜像管理** → 构建镜像、拉取镜像、推送镜像、标记标签、删除镜像、保存/加载镜像
- **Docker Compose 管理** → 启动服务、停止服务、列出服务、查看日志、进入容器终端、构建镜像、配置文件管理
- **卷与网络管理** → 创建卷/网络、检查状态、删除卷/网络、清理无用资源、连接卷/网络
- **故障排查** → 日志分析、退出码检查、资源问题处理

### 2. 容器操作

**运行新容器：**

```bash
# Detached service with port mapping
docker run -d --name web -p 8080:80 nginx

# With environment variables
docker run -d -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=mydb --name db postgres:16

# With persistent data (named volume)
docker run -d -v pgdata:/var/lib/postgresql/data --name db postgres:16

# For development (bind mount source code)
docker run -d -v $(pwd)/src:/app/src -p 3000:3000 --name dev my-app

# Interactive debugging (auto-remove on exit)
docker run -it --rm ubuntu:22.04 /bin/bash

# With resource limits and restart policy
docker run -d --memory=512m --cpus=1.5 --restart=unless-stopped --name app my-app
```

常用标志：`-d` 表示分离模式，`-it` 表示交互式终端模式，`--rm` 表示自动删除容器，`-p` 用于指定端口（主机:容器），`-e` 用于设置环境变量，`-v` 用于挂载卷，`--name` 用于指定容器名称，`--restart` 用于设置重启策略。

**管理正在运行的容器：**

```bash
docker ps                        # running containers
docker ps -a                     # all (including stopped)
docker stop NAME                 # graceful stop
docker start NAME                # start stopped container
docker restart NAME              # stop + start
docker rm NAME                   # remove stopped container
docker rm -f NAME                # force remove running container
docker container prune           # remove ALL stopped containers
```

**与容器交互：**

```bash
docker exec -it NAME /bin/sh          # shell access (use /bin/bash if available)
docker exec NAME env                   # view environment variables
docker exec -u root NAME apt update    # run as specific user
docker logs --tail 100 -f NAME         # follow last 100 lines
docker logs --since 2h NAME            # logs from last 2 hours
docker cp NAME:/path/file ./local      # copy file from container
docker cp ./file NAME:/path/           # copy file to container
docker inspect NAME                    # full container details (JSON)
docker stats --no-stream               # resource usage snapshot
docker top NAME                        # running processes
```

### 3. 图像管理

```bash
# Build
docker build -t my-app:latest .
docker build -t my-app:prod -f Dockerfile.prod .
docker build --no-cache -t my-app .              # clean rebuild
DOCKER_BUILDKIT=1 docker build -t my-app .       # faster with BuildKit

# Pull and push
docker pull node:20-alpine
docker login ghcr.io
docker tag my-app:latest registry/my-app:v1.0
docker push registry/my-app:v1.0

# Inspect
docker images                          # list local images
docker history IMAGE                   # see layers
docker inspect IMAGE                   # full details

# Cleanup
docker image prune                     # remove dangling (untagged) images
docker image prune -a                  # remove ALL unused images (careful!)
docker image prune -a --filter "until=168h"   # unused images older than 7 days
```

### 4. Docker Compose

```bash
# Start/stop
docker compose up -d                   # start all services detached
docker compose up -d --build           # rebuild images before starting
docker compose down                    # stop and remove containers
docker compose down -v                 # also remove volumes (DESTROYS DATA)

# Monitoring
docker compose ps                      # list services
docker compose logs -f api             # follow logs for specific service
docker compose logs --tail 50          # last 50 lines all services

# Interaction
docker compose exec api /bin/sh        # shell into running service
docker compose run --rm api npm test   # one-off command (new container)
docker compose restart api             # restart specific service

# Validation
docker compose config                  # validate and view resolved config
```

**最简的 compose.yml 示例：**

```yaml
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      # Password comes from the POSTGRES_PASSWORD secret, not the URL
      - DATABASE_URL=postgres://mydb_user@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### 5. 卷与网络

```bash
# Volumes
docker volume ls                       # list volumes
docker volume create mydata            # create named volume
docker volume inspect mydata           # details (mount point, etc.)
docker volume rm mydata                # remove (fails if in use)
docker volume prune                    # remove unused volumes

# Networks
docker network ls                      # list networks
docker network create mynet            # create bridge network
docker network inspect mynet           # details (connected containers)
docker network connect mynet NAME      # attach container to network
docker network disconnect mynet NAME   # detach container
docker network rm mynet                # remove network
docker network prune                   # remove unused networks
```

### 6. 磁盘使用情况与清理

在开始清理之前，请务必先进行诊断：

```bash
# Check what's using space
docker system df                       # summary
docker system df -v                    # detailed breakdown

# Targeted cleanup (safe)
docker container prune                 # stopped containers
docker image prune                     # dangling images
docker volume prune                    # unused volumes
docker network prune                   # unused networks

# Aggressive cleanup (confirm with user first!)
docker system prune                    # containers + images + networks
docker system prune -a                 # also unused images
docker system prune -a --volumes       # EVERYTHING — named volumes too
```

**警告：** 未经用户确认，切勿运行 `docker system prune -a --volumes` 命令。该命令会删除可能包含重要数据的命名卷。

## 常见问题

| 问题 | 原因 | 解决方案 |
|---------|------|----------|
| 容器立即退出 | 主进程已结束或崩溃 | 查看 `docker logs NAME`，尝试使用 `docker run -it --entrypoint /bin/sh IMAGE` 启动容器 |
| “端口已被占用” | 有其他进程正在使用该端口 | 使用 `docker ps` 或 `lsof -i :PORT` 查找占用端口的进程 |
| “设备空间不足” | Docker 存储空间已满 | 先执行 `docker system df` 查看情况，再针对性地进行清理 |
| 无法连接到容器 | 应用程序在容器内绑定到 127.0.0.1 地址 | 应将绑定地址改为 `0.0.0.0`，并检查 `-p` 参数的映射设置 |
| 卷访问被拒绝 | 主机与容器的 UID/GID 不匹配 | 使用 `--user $(id -u):$(id -g)` 参数指定用户身份，或修正权限设置 |
| Compose 服务之间无法通信 | 网络配置或服务名称有误 | 服务会以服务名称作为主机名，需检查 `docker compose config` 的配置内容 |
| 构建缓存功能失效 | Dockerfile 中的层顺序错误 | 将更改频率较低的层放在前面（先将依赖项层放入，再放源代码层） |
| 镜像体积过大 | 未使用多阶段构建，也未添加 `.dockerignore` 文件 | 采用多阶段构建方式，并添加 `.dockerignore` 文件 |

## 结果验证

执行任何 Docker 操作后，都应验证操作结果是否正确：

- **容器已启动？** → 使用 `docker ps` 命令检查，状态应为“Up”  
- **日志是否正常？** → 运行 `docker logs --tail 20 NAME`，确保无错误信息  
- **端口可访问吗？** → 使用 `curl -s http://localhost:PORT` 或 `docker port NAME` 进行测试  
- **镜像已构建？** → 通过 `docker images | grep TAG` 查看对应标签的镜像是否存在  
- **Compose 集群运行正常？** → 执行 `docker compose ps`，所有服务状态应为“running”或“healthy”  
- **磁盘空间是否充足？** → 使用 `docker system df` 查看磁盘使用情况，并对比构建前后数据  

## Dockerfile 优化建议

在审查或编写 Dockerfile 时，可参考以下优化方法：

1. **多阶段构建** — 将构建环境与运行环境分离，从而减小最终镜像体积  
2. **层顺序调整** — 先放置依赖项，再放源代码，避免更改导致缓存层失效  
3. **合并 RUN 命令** — 减少镜像层数量，进而缩小镜像大小  
4. **使用 .dockerignore 文件** — 排除 `node_modules`、`.git`、`__pycache__` 等文件  
5. **锁定基础镜像版本** — 选择具体版本如 `node:20-alpine`，而非通用的 `node:latest`  
6. **以非根用户运行** — 添加 `USER` 指令以提高安全性  
7. **选用轻量级基础镜像** — 选择如 `python:3.12-slim` 而非完整版本的 `python:3.12`
