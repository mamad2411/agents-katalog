---
name: nodapt
description: 当用户请求执行 Node.js / npm 命令时使用该技能，并允许指定 Node.js 版本。
---

# Nodapt

nodapt 是一个虚拟 Node.js 运行环境，旨在为 Node.js 项目提供简单可靠的版本管理工具。它可以根据 `package.json` 中的版本约束自动选择并安装合适的 Node.js 版本，并执行相关命令。

如果 `package.json` 中包含 Node.js 版本约束，或者用户明确要求使用特定 Node.js 版本或管理已安装版本，则应使用此技能执行命令。

如果用户要求使用或删除某个 Node.js 版本，但未提供有效版本格式，应在执行前请求用户明确具体版本。

如果用户未安装 nodapt，可以建议其按照下方“安装”部分进行安装。

---

## 使用场景

在以下情况下使用该技能：

1. 执行任何 Node.js 或 npm 命令
2. 项目 `package.json` 中包含 `engines.node` 版本约束
3. 用户明确指定 Node.js 版本
4. 管理 Node.js 版本（安装 / 删除 / 列出）
5. 用户提到 “nodapt” 或 Node.js 版本管理

---

## 基本用法

### 1. 自动版本选择

根据 `package.json` 自动选择 Node.js 版本执行命令：

```bash
nodapt node -v
nodapt npm install
nodapt npx create-react-app my-app
```

---

### 2. 指定 Node.js 版本

使用指定版本运行命令：

```bash
nodapt use v14.17.0 node app.js
nodapt use 22 node script.js
nodapt use ^16.14.0 npm test
```

---

### 3. 版本管理

列出已安装版本：

```bash
nodapt ls
```

列出可用远程版本：

```bash
nodapt ls-remote
```

删除指定版本：

```bash
nodapt rm v14.17.0
```

清理所有已安装版本：

```bash
nodapt clean
```

---

## 常见场景

### 场景 1：基于版本约束运行项目

若 `package.json` 包含 `engines.node`：

```json
{
  "engines": {
    "node": ">=16.0.0 <19.0.0"
  }
}
```

执行：

```bash
nodapt npm start
```

---

### 场景 2：多版本测试

```bash
nodapt use 14 npm test
nodapt use 16 npm test
nodapt use 18 npm test
```

---

### 场景 3：全局工具安装

```bash
nodapt npm install -g yarn
nodapt yarn build
```

---

## 错误处理

### 版本不存在

```bash
Error: Version v14.17.0 not found
```

应提示用户查看可用版本：

```bash
nodapt ls-remote
```

---

### 版本格式无效

当用户输入不规范版本时，应要求澄清，例如：

- “你希望使用 14.x 最新版本，还是精确 v14.0.0？”

---

### 无兼容版本

当自动匹配失败：

```bash
Error: No compatible Node.js version found
```

应提示用户手动指定版本或修改 `package.json`。

---

## 安装方式

### 方式 1：Cask（推荐）

```bash
cask install github.com/axetroy/nodapt
```

### 方式 2：npm

```bash
npm install -g nodapt
```

### 方式 3：手动安装

参考源码仓库获取二进制版本。

验证安装：

```bash
nodapt --version
```

---

## 配置

### 环境变量

```bash
NODE_MIRROR=https://registry.npmmirror.com/-/binary/node/
NODE_ENV_DIR=/custom/path/.nodapt
DEBUG=1
```

---

## 使用原则

1. 优先检查 `package.json` 是否存在版本约束
2. 优先使用自动版本选择
3. CI 环境中必须使用明确版本
4. 定期清理无用版本
5. 使用语义化版本范围优先

---

## 故障排查

### 命令未找到

确认 nodapt 是否安装：

```bash
which nodapt
```

---

### 权限问题

检查安装权限或调整 npm prefix：

```bash
npm config set prefix ~/.npm-global
```

---

### 下载慢

建议使用镜像：

```bash
export NODE_MIRROR=https://registry.npmmirror.com/-/binary/node/
```

---

## 帮助命令

```bash
nodapt --help
```

---

## 仓库地址

[https://github.com/axetroy/nodapt](https://github.com/axetroy/nodapt)
