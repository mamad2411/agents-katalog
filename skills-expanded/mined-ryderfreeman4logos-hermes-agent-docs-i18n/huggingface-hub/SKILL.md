---
name: huggingface-hub
description: "HuggingFace hf CLI: search/download/upload models, datasets."
version: 1.0.0
author: Hugging Face
license: MIT
tags: [huggingface, hf, models, datasets, hub, mlops]
platforms: [linux, macos, windows]
---

# Hugging Face CLI (`hf`) 参考指南

`hf` 命令是用于与 Hugging Face Hub 进行交互的现代化命令行界面，它提供了管理代码库、模型、数据集以及 Spaces 的各类工具。

> **重要提示：** `hf` 命令已取代了现已过时的 `huggingface-cli` 命令。

## 快速入门
*   **安装：** `curl -LsSf https://hf.co/cli/install.sh | bash -s`
*   **帮助：** 使用 `hf --help` 查看所有可用功能及实际使用示例。
*   **身份认证：** 建议通过 `HF_TOKEN` 环境变量或 `--token` 参数来进行认证。

---

## 核心命令

### 基本操作
*   `hf download REPO_ID`：从 Hub 下载文件。
*   `hf upload REPO_ID`：上传文件/文件夹（推荐用于单次提交）。
*   `hf upload-large-folder REPO_ID LOCAL_PATH`：推荐用于大目录的分段上传。
*   `hf sync`：在本地目录与存储桶之间同步文件。
*   `hf env` / `hf version`：查看环境信息及版本详情。

### 身份认证 (`hf auth`)
*   `login` / `logout`：使用来自 [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) 的令牌来管理会话。
*   `list` / `switch`：管理和切换多个已存储的访问令牌。
*   `whoami`：查看当前登录的账户信息。

### 代码库管理 (`hf repos`)
*   `create` / `delete`：创建或永久删除代码库。
*   `duplicate`：将模型、数据集或 Space 克隆到新的 ID 下。
*   `move`：在不同的命名空间之间转移代码库。
*   `branch` / `tag`：管理类似 Git 的引用。
*   `delete-files`：使用模式删除特定文件。

---

## 针对 Hub 的特殊操作

### 数据集与模型
*   **数据集：** `hf datasets list`、`info` 以及 `parquet`（列出 Parquet 格式文件的 URL）。
*   **SQL 查询：** `hf datasets sql SQL` —— 通过 DuckDB 对数据集的 Parquet URL 执行原始 SQL 查询。
*   **模型：** `hf models list` 和 `info`。
*   **论文：** `hf papers list` —— 查看每日推荐论文。

### 讨论区与拉取请求 (`hf discussions`)
*   管理 Hub 贡献内容的生命周期：`list`、`create`、`info`、`comment`、`close`、`reopen` 以及 `rename`。
*   `diff`：查看拉取请求中的更改内容。
*   `merge`：完成拉取请求的合并。

### 基础设施与计算
*   **推理端点：** 部署并管理推理端点（`deploy`、`pause`、`resume`、`scale-to-zero`、`catalog`）。
*   **任务调度：** 在 Hugging Face 的基础设施上运行计算任务。包括用于运行带内联依赖项的 Python 脚本的 `hf jobs uv`，以及用于资源监控的 `stats`。
*   **Spaces：** 管理交互式应用。包括无需完全重启即可对 Python 文件进行开发的 `dev-mode` 和 `hot-reload` 功能。

### 存储与自动化
*   **存储桶：** 支持类似 S3 的完整存储桶管理功能（`create`、`cp`、`mv`、`rm`、`sync`）。
*   **缓存：** 使用 `list`、`prune`（移除已分离的版本）以及 `verify`（校验和检查）来管理本地存储。
*   **Webhook：** 通过管理 Hub 的 Webhook 来实现工作流的自动化（`create`、`watch`、`enable`/`disable`）。
*   **集合：** 将 Hub 中的物品组织到集合中（`add-item`、`update`、`list`）。

---

## 高级用法与技巧

### 全局参数
*   `--format json`：生成机器可读的输出，便于自动化处理。
*   `-q` / `--quiet`：仅输出 ID，减少输出信息量。

### 扩展功能与技能
*   **扩展插件：** 通过 GitHub 仓库使用 `hf extensions install REPO_ID` 来扩展 CLI 的功能。
*   **AI 技能：** 使用 `hf skills add` 来管理 AI 助手技能。
