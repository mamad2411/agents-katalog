---
name: github-recruiter
description: Use when 用户想从 GitHub 上发现并联系活跃开发者（招聘、找贡献者、技术建联）。输入关键词，搜索仓库、提取贡献者/PR 作者、采集公开邮箱、按模板批量发邮件。命令行工具。
---

# GitHub Recruiter

从 GitHub 仓库发现活跃开发者，采集公开联系方式并按模板发招聘邮件的 CLI 工具。

## 何时用

用户要按技术关键词找开发者、采集贡献者邮箱、批量发招聘或建联邮件。

## 安装与配置

```bash
pip install -e .            # 在本 skill 目录内
cp config.example.yaml config.yaml
```

编辑 `config.yaml`：GitHub Personal Access Token（需 `public_repo` scope）、SMTP 邮箱（Gmail 用应用专用密码）。

## 常用命令

- 搜索并采集：`github-recruiter search "agent" --language python --min-stars 500`
- 查看候选人：`github-recruiter list [--status pending|sent]`
- 发邮件：`github-recruiter send --dry-run --limit 5`（预览）/ `--limit 10`（实发）
- 一键执行：`github-recruiter run "agent" --language python --dry-run`
- 统计：`github-recruiter stats`

邮箱采集优先级：公开 email 字段 → commit author email → bio/blog 正则匹配；自动跳过 `noreply@github.com`。

## 注意

未认证 GitHub API 限速 60 次/小时，认证后 5000 次/小时；内置退避重试 + 发信频率控制。只使用公开信息。邮件模板在 `templates/default.txt`，首行须为 `Subject: 标题`。
