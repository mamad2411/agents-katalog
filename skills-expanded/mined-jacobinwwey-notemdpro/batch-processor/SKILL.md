---
name: batch-processor
description: Execute bounded Markdown batches with complete task logs and explicit partial failures.
---

# Batch processor

## English

Use [workflow-runner](../workflow-runner/SKILL.md) for the common task record. Resolve the authorized folder and output policy once. Enumerate eligible files deterministically, exclude symlinks outside the selected tree, and process each file through read -> transform -> validate -> write. Recheck the source before writing; preserve unrelated notes and source artifacts.

Bound concurrency according to the host/provider. Retry only transient transport failures and HTTP 408/425/429/500/502/503/504 within a finite attempt/time budget; honor Retry-After when available. Authentication, invalid configuration, parser errors and cancellation do not retry. Stop scheduling new work when cancelled, retain completed outcomes, and report pending/cancelled files separately.

Keep a single task transcript across stages and files. Log stage, path, attempt, severity and actionable error summaries; never log credentials, authorization headers or raw provider payloads. Record partial failures honestly. File helper progress is separate from transcript retention. No `app.vault` API or local provider implementation exists here.

## 中文

共享任务记录遵循 [workflow-runner](../workflow-runner/SKILL.md)。一次性确认授权目录及输出策略，确定性枚举可处理文件，排除指向选定目录外的符号链接，逐文件执行读取 -> 转换 -> 验证 -> 写入。写入前重新检查源文件，保留无关笔记与源产物。

按宿主/provider 能力限制并发。仅对暂态传输失败和 HTTP 408/425/429/500/502/503/504 在有限次数及时间内重试；可用时遵循 Retry-After。认证、配置、解析错误及取消不得重试。取消后停止调度，保留已完成结果，分别报告待处理及已取消文件。

跨阶段、跨文件保留一份完整任务日志。记录阶段、路径、重试次数、严重级别及可操作的错误摘要，不记录凭据、认证头或原始 provider 载荷。如实报告部分失败。进度与日志保留独立；此处不存在 `app.vault` API 或本地 provider 实现。
