---
name: yashandb-docker
name_for_command: yashandb-docker
description: |
  自动部署 YashanDB Docker 镜像。从 Docker Hub 拉取镜像，创建数据目录，
  并启动容器。

  适用场景：在 Linux 或 Windows 上快速部署 YashanDB。

variables:
  image: docker.1ms.run/yasdb/yashandb:23.4.7.100
  docker_hub_image: yasdb/yashandb:latest
  password: Cod-2022
---

# YashanDB Docker 部署

自动化完成 YashanDB Docker 部署。

## 前置条件

- **操作系统**：Linux（x86_64 或 aarch64）/ Windows 10/11（x86_64）
- **Docker** 已安装并运行（Windows 需要 WSL2）
- **网络连接** 用于拉取 Docker Hub 镜像
- **至少 5GB** 可用磁盘空间

## 快速开始

### 拉取镜像

#### 方式一：从毫秒镜像拉取（推荐，国内加速）

```bash
docker pull {{image}}
```

> **提示**：毫秒镜像是国内加速镜像，访问速度更快。如果该镜像不可用，可尝试其他标签或使用方式二。

#### 方式二：从 Docker Hub 拉取

```bash
docker pull {{docker_hub_image}}
```

如果 Docker Hub 访问失败，请使用**方式三**从崖山官网下载。

#### 方式三：从崖山官网下载（Docker Hub 访问失败时使用）

访问 [https://download.yashandb.com/download](https://download.yashandb.com/download) 下载 Docker 镜像包。

**Linux/macOS:**

```bash
# 下载镜像（根据系统选择 x86_64 或 aarch64）
curl -fL -o yashandb-image.tar.gz "https://download.yashandb.com/download/xxx"

# 导入镜像
docker load -i yashandb-image.tar.gz
```

**Windows (PowerShell):**

```powershell
# 下载镜像
Invoke-WebRequest -Uri "https://download.yashandb.com/download/xxx" -OutFile yashandb-image.tar.gz

# 导入镜像
docker load -i yashandb-image.tar.gz
```

> **提示**：如果官网下载速度慢，可尝试使用内网下载链接：<https://linked.yashandb.com/upload1010/>

### 创建数据目录

```bash
mkdir -p ~/yashan/data ~/yashan/yasboot
```

### 启动容器

```bash
docker run -d \
  -p 1688:1688 \
  -v ~/yashan/data:/data/yashan \
  -v ~/yashan/yasboot:/home/yashan/.yasboot \
  -e SYS_PASSWD={{password }} \
  --name yashandb \
  {{image}}
```

### 验证部署

```bash
# 等待约 30 秒让数据库完全启动
docker exec -it yashandb yasql sys/{{password}}
```

## 清理环境

```bash
docker stop yashandb
docker rm yashandb
docker rmi {{image}}
rm -rf ~/yashan
```

## 参考文档

- [离线导入](references/offline-import.md) - 无法访问 Docker Hub 时的备选方案
- [安装指南](references/installation.md)
- [配置说明](references/configuration.md)
- [故障排查](references/troubleshooting.md)
