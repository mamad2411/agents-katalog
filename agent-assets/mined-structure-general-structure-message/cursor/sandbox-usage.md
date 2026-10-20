---
description: |
triggers:
  - 沙箱
  - e2b
  - agentsphere
  - opensandbox
  - 代码执行环境
  - sandbox
  - 隔离执行
role: devops
priority: low
category: support
stack: _common
alwaysApply: false
---


# 沙箱使用

> 安全使用沙箱环境执行 AI 生成的代码。**不可信代码 MUST 在沙箱运行**。

## 沙箱选型对比

| 沙箱 | 适用 | 特点 |
|---|---|---|
| **e2b** | AI Agent 代码执行 | 完整 Linux 环境、长时间运行、持久化 |
| **agentsphere** | 企业级 AI 沙箱 | 审计、权限控制 |
| **opensandbox** | 轻量演示 | 快速启动、简单 |
| **Docker（本地）** | 本地隔离 | 无网络隔离 |
| **Kubernetes Job** | 生产级隔离 | 完整 K8s 生态 |

## e2b 使用

```bash
# 启动沙箱
e2b sandbox create --template base

# 执行代码
e2b sandbox exec <id> -- python script.py

# 上传 / 下载文件
e2b sandbox upload <id> ./local /remote/path
e2b sandbox download <id> /remote/path ./local

# 关闭沙箱
e2b sandbox kill <id>
```

## 关键约束

- ✅ **MUST** 不可信代码 MUST 在沙箱运行（不在生产 / 本地）
- ✅ **MUST** 沙箱 MUST 限制网络访问（除非必要）
- ✅ **MUST** 沙箱 MUST 限制资源（CPU / 内存 / 时长）
- ✅ **MUST** 沙箱 MUST 不挂载敏感目录（SSH key / 云凭据）
- ❌ **MUST NOT** 在沙箱中存放生产 Secrets

## 数据安全

- 沙箱内数据 MUST 视为"可能被泄露"
- 沙箱内 MUST NOT 传入生产数据
- 沙箱内 MUST NOT 传入用户 PII
- 沙箱结束后 MUST 清理

## 关联

- Wiki：`wiki/_common/security.md`
- 相关：`docker-cli` / `kubectl-ops`
