---
name: yashandb-c
name_for_command: yashandb-c
description: 安装和配置 YashanDB C 驱动（libyascli）。Go 和 Python 驱动依赖此驱动。当用户需要安装 C 驱动或遇到 "libyascli.so not found" 错误时使用此技能。
---

# YashanDB C 驱动安装

本技能指导用户完成 YashanDB C 驱动的安装和配置。

> **重要**：YashanDB 的 Go 驱动和 Python 驱动都依赖 C 驱动（libyascli.so / yascli.dll）。请先完成 C 驱动安装。

## 依赖关系

```
┌─────────────┐
│   Go 驱动    │
└──────┬──────┘
       │ 依赖
       ▼
┌─────────────┐     ┌───────────────┐
│  C 驱动     │◄────│  Python 驱动   │
└─────────────┘     └───────────────┘
```

## 安装路径

默认安装目录：`~/.yashandb/client`（`{USER}/.yashandb/client`）

## 步骤概览

1. 检查 C 驱动是否已安装
2. 下载 C 驱动（GitHub 优先，官网备用）
3. 安装 C 驱动
4. 验证安装

## 第一步：检查 C 驱动

### 检查方法

```bash
ls ~/.yashandb/client/lib/libyascli.so 2>/dev/null && echo "已安装"
```

### Windows (PowerShell)

```powershell
Test-Path "$env:USERPROFILE\.yashandb\client\lib\yascli.dll"
```

### 判断结果

| 检查结果 | 操作 |
|----------|------|
| 找到 libyascli / yascli.dll | C 驱动已安装，跳到验证步骤 |
| 未找到 | 继续安装 C 驱动 |

## 第二步：下载 C 驱动

### 下载来源

| 优先级 | 来源 | 地址 |
|--------|------|------|
| 第一（推荐） | GitHub Releases | https://github.com/yashan-technologies/yashandb-client/releases |
| 第二（备用） | 官网下载中心 | https://linked.yashandb.com |

### 下载方式（按优先级自动选择）

首先检测系统中有哪些下载工具，然后按以下顺序选择：

```
gh → wget → 官网直接下载
```

#### 方式一：使用 `gh` 命令（推荐）

如果 `gh` 命令可用，使用它获取下载链接：

```bash
# Linux x86_64
gh release view latest -R yashan-technologies/yashandb-client --json assets --jq '.assets[] | select(.name | contains("linux") and contains("x86_64")) | .browser_download_url'

# Linux ARM64
gh release view latest -R yashan-technologies/yashandb-client --json assets --jq '.assets[] | select(.name | contains("linux") and contains("aarch64")) | .browser_download_url'

# Windows x64
gh release view latest -R yashan-technologies/yashandb-client --json assets --jq '.assets[] | select(.name | contains("win64") and contains("amd64")) | .browser_download_url'
```

获取链接后用 `curl` 或 `wget` 下载对应压缩包。

> **提示**：实际文件名以 GitHub Releases 页面上发布的为准，`wget` 下载失败时请在浏览器打开 https://github.com/yashan-technologies/yashandb-client/releases 确认文件名。

#### 方式二：使用 `wget` 命令

如果 `gh` 不可用但 `wget` 可用，LATEST_TAG默认的版本号为`23.4.7.100`，先获取最新版本号再下载：

```bash
# 获取最新版本号
LATEST_TAG=$(wget -qO- https://github.com/yashan-technologies/yashandb-client/tags | grep -oP 'releases/tag/\K[^"]+' | head -1)
echo "最新版本: $LATEST_TAG"

# Linux x86_64
wget -O /tmp/yashandb-client.tar.gz "https://github.com/yashan-technologies/yashandb-client/releases/download/${LATEST_TAG}/yashandb-client-${LATEST_TAG}-linux-x86_64.tar.gz"

# Linux ARM64
wget -O /tmp/yashandb-client.tar.gz "https://github.com/yashan-technologies/yashandb-client/releases/download/${LATEST_TAG}/yashandb-client-${LATEST_TAG}-linux-aarch64.tar.gz"

# Windows x64
wget -O /tmp/yashandb-client.zip "https://github.com/yashan-technologies/yashandb-client/releases/download/${LATEST_TAG}/yashandb-client-${LATEST_TAG}-windows-amd64.zip"
```


#### 方式三：官网备用下载

如果所有下载方式均失败（包括 gh/wget/curl 均不可用或网络不通），请手动从官网下载：

| 操作系统 | 架构 | 下载链接 |
|----------|------|----------|
| Linux | x86_64 | https://linked.yashandb.com/upload1010/yashandb-client-23.4.1.102-linux-x86_64.tar.gz |
| Linux | ARM64 | https://linked.yashandb.com/upload1010/yashandb-client-23.4.1.102-linux-aarch64.tar.gz |
| Windows | x64 | https://linked.yashandb.com/upload1010/yashandb-client-23.4.1.102-windows-amd64.zip |
| macOS | - | 暂不支持 |

下载后手动解压到 `~/.yashandb/client` 目录。

## 第三步：安装 C 驱动

将C驱动解压到 `~/.yashandb/client`

### 安装步骤

::: tabs
== Linux

```bash
# 创建目录
mkdir -p ~/.yashandb/client

# 解压（保留顶层目录结构）
tar -xzf /tmp/yashandb-client.tar.gz -C ~/.yashandb/client

```

== Windows (PowerShell)

```powershell
# 创建目录
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.yashandb\client"

# 解压
Expand-Archive -Path "$env:TEMP\yashandb-client.zip" -DestinationPath "$env:USERPROFILE\.yashandb\client" -Force
```
:::

## 第四步：验证安装

```bash
# Linux
ls ~/.yashandb/client/lib/libyascli.so 2>/dev/null && echo "已安装"

# Windows
Test-Path "$env:USERPROFILE\.yashandb\client\lib\yascli.dll"
```

## 参考文档

- [installation](skills/yashandb-c/references/installation.md)
- [configuration](skills/yashandb-c/references/configuration.md)
- [troubleshooting](skills/yashandb-c/references/troubleshooting.md)

## 相关技能

- `/yashandb-go` - Go 驱动安装（依赖本技能）
- `/yashandb-python` - Python 驱动安装（依赖本技能）

## 相关资源

- GitHub 仓库：https://github.com/yashan-technologies/yashandb-client
- YashanDB 下载中心：https://download.yashandb.com
- YashanDB 官方文档：https://doc.yashandb.com
