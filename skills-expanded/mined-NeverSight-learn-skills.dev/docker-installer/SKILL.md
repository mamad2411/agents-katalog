---
name: docker-installer
name_for_command: docker-installer
description: 帮助用户在 Windows、Linux（Ubuntu/Debian/CentOS/Fedora）或 macOS 环境下安装和配置 Docker。当用户需要使用 Docker 但检测到未安装时，自动触发此 skill。根据用户操作系统自动选择合适的安装方式。
---

# Docker Installer Skill

## 概述

此 skill 用于帮助用户在不同操作系统环境下安装和配置 Docker Desktop 或 Docker Engine。当检测到用户未安装 Docker 但需要使用 Docker 时（如运行 /yashandb-docker），自动引导用户完成 Docker 安装。

**支持的操作系统：**
- Windows 10/11
- Linux：Ubuntu、Debian、CentOS、Fedora、Rocky Linux、AlmaLinux
- macOS

## 工作流程

### 步骤 1：检测 Docker 是否已安装

运行以下命令检测 Docker 是否已安装：

**Windows (PowerShell/CMD)：**
```powershell
docker --version
docker-compose --version
```

**Linux/macOS (Bash)：**
```bash
docker --version
docker-compose --version
```

- 如果命令成功执行并返回版本号，说明 Docker 已安装，验证 Docker 服务是否正在运行
- 如果命令未找到或报错，继续下一步安装

### 步骤 2：检测操作系统类型

根据当前环境自动检测操作系统：

**Windows：**
```powershell
$os = (Get-CimInstance Win32_OperatingSystem).Caption
Write-Host $os
```

**Linux：**
```bash
cat /etc/os-release
# 或
uname -a
```

### 步骤 3：根据系统安装 Docker

#### 3.1 Windows 安装

**系统要求：**
- Windows 10/11 专业版/企业版（64位）
- 4GB+ RAM
- 虚拟化功能已启用（BIOS 中）
- 至少 20GB 可用空间

**安装步骤：**

1. 下载 Docker Desktop：https://www.docker.com/products/docker-desktop
2. 运行 `Docker Desktop Installer.exe`
3. 勾选 "Use WSL 2 instead of Hyper-V"（推荐）
4. 等待安装完成
5. 点击 "Close and restart"

**验证安装：**
```powershell
docker --version
docker run hello-world
```

#### 3.2 Ubuntu/Debian 安装

**安装步骤：**

```bash
# 1. 更新软件源
sudo apt update

# 2. 安装依赖包
sudo apt install -y ca-certificates curl gnupg lsb-release

# 3. 添加 Docker GPG 密钥
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. 添加 Docker 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. 安装 Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 7. 验证安装
sudo docker run hello-world
```

**国内镜像（可选）：**
如果访问国外资源较慢，可以使用国内镜像：

```bash
# 使用阿里云镜像
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### 3.3 CentOS/RHEL 安装

**安装步骤：**

```bash
# 1. 卸载旧版本（如有）
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# 2. 安装依赖包
sudo yum install -y yum-utils

# 3. 添加 Docker 仓库
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 4. 安装 Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 5. 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 6. 验证安装
sudo docker run hello-world
```

**国内镜像（可选）：**
```bash
# 使用阿里云镜像
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

#### 3.4 Fedora 安装

**安装步骤：**

```bash
# 1. 安装依赖包
sudo dnf -y install dnf-plugins-core

# 2. 添加 Docker 仓库
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# 3. 安装 Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 4. 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 5. 验证安装
sudo docker run hello-world
```

#### 3.5 Rocky Linux / AlmaLinux 安装

**安装步骤：**

```bash
# 1. 安装依赖包
sudo dnf install -y dnf-plugins-core

# 2. 添加 Docker 仓库（使用 CentOS 仓库）
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 3. 安装 Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 4. 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 5. 验证安装
sudo docker run hello-world
```

#### 3.6 macOS 安装

**方式一：使用 Homebrew（推荐）**

```bash
# 安装 Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Docker
brew install --cask docker

# 启动 Docker 应用（在 Applications 中点击 Docker 图标）
```

**方式二：手动安装**

1. 下载 Docker Desktop：https://www.docker.com/products/docker-desktop
2. 运行 `Docker.dmg`
3. 将 Docker 拖入 Applications 文件夹
4. 启动 Docker 应用

**验证安装：**
```bash
docker --version
docker run hello-world
```

### 步骤 4：验证 Docker 安装

所有系统安装完成后，运行以下命令验证：

```bash
docker --version
docker-compose --version
docker run hello-world
```

如果所有命令成功执行，说明 Docker 已正确安装。

### 步骤 5：处理常见问题

#### Linux 常见问题

1. **权限问题**：将当前用户加入 docker 组
   ```bash
   sudo usermod -aG docker $USER
   # 重新登录后生效
   ```

2. **Docker 服务未启动**：
   ```bash
   sudo systemctl start docker
   sudo systemctl status docker
   ```

3. **防火墙问题**：检查端口是否被阻止

#### Windows 常见问题

1. **"Docker is not running"**：启动 Docker Desktop 应用
2. **WSL 2 相关错误**：安装 WSL 2 更新包
3. **虚拟化未启用**：在 BIOS 中启用虚拟化
4. **端口冲突**：检查并关闭占用 2375/2376 端口的程序

## 注意事项

- Linux 安装需要 sudo 权限或 root 权限
- 安装完成后建议将用户加入 docker 组，避免每次使用 sudo
- Windows 和 macOS 需要保持 Docker 应用处于运行状态
- 如果使用家庭版 Windows，可能需要启用 Hyper-V 或使用 WSL 2

## 输出格式

完成安装后，向用户确认：
- Docker 版本信息
- Docker Compose 版本信息
- 确认可以正常运行容器
- 提醒 Linux 用户如需免 sudo 使用 Docker，执行 `sudo usermod -aG docker $USER`