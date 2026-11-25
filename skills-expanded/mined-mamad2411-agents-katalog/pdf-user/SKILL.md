---
name: pdf-user
version: 1.0.0
description: "pdf-cli 用户模块：个人信息管理、文件列表、操作记录、API Key 管理、意见反馈。当用户需要查看/修改个人信息、管理文件和操作记录、创建/删除 API Key、提交反馈时使用。"
metadata:
  requires:
    bins: ["pdf-cli"]
  cliHelp: "pdf-cli user --help"
---

# user

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../pdf-shared/SKILL.md`](../pdf-shared/SKILL.md)，其中包含认证、配置、错误处理**

## 命令概览

| 命令 | 说明 | 需要登录 |
|------|------|----------|
| [`profile`](references/pdf-user-profile.md) | 查看个人信息 | 是 |
| [`update`](references/pdf-user-update.md) | 修改个人信息 | 是 |
| [`files list`](references/pdf-user-files.md) | 查看文件列表 | 是 |
| [`records list`](references/pdf-user-records.md) | 查看操作记录列表 | 是 |
| [`records get`](references/pdf-user-records.md) | 查看操作记录详情 | 是 |
| [`api-key list`](references/pdf-user-apikey.md) | 查看 API Key 列表 | 是 |
| [`api-key create`](references/pdf-user-apikey.md) | 创建 API Key | 是 |
| [`api-key delete`](references/pdf-user-apikey.md) | 删除 API Key | 是 |
| [`feedback submit`](references/pdf-user-feedback.md) | 提交意见反馈 | 是 |

## 快速开始

```bash
# 查看个人信息
pdf-cli user profile

# 查看文件列表
pdf-cli user files list

# 查看操作记录
pdf-cli user records list --page-size 10

# 管理 API Key
pdf-cli user api-key list
pdf-cli user api-key create --name "my-key"
pdf-cli user api-key delete --id <key-id>
```
