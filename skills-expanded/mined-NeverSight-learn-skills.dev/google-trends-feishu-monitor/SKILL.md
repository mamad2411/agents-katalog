---
name: google-trends-feishu-monitor
description: 执行固定飞书工作簿上的 Google Trends 关键词监控流程。用于执行、续跑、稳定化 Google Trends 到飞书“每日找词”的周期性监控任务。该技能只负责监控流程本身，包括 Trends 采集、暴涨词筛选、与 `GPTs` 的对比判定、写回飞书，以及运行记录/检查点编排；不负责浏览器环境安装、代理安装切换或 Feishu 工具初始化。
---

# Google Trends Feishu Monitor

## 概述

这个技能用于执行固定工作簿上的 Google Trends 监控流程：

- 从飞书读取词根行和 `trends url`
- 采集 `Related queries > Rising`
- 将暴涨词与 `GPTs` 做 7 天对比
- 按规则筛选候选词
- 写回飞书 `每日找词`
- 维护每次执行的 run markdown 和 checkpoint 文件

这个技能刻意保持窄职责。它不负责安装浏览器工具、不负责配置 MCP、不负责切换代理节点，也不负责初始化飞书凭据。

## 技能内置资源定位规则

先按下面规则理解本技能里的路径，再开始执行：

- 本文中出现的 `scripts/...`、`references/...` 路径，全部都是相对于当前技能目录的内置资源路径，不是相对于当前工作区。
- 触发该技能后，应直接从技能目录读取和调用这些内置资源，不要先去当前仓库或工作区里搜索同名脚本。
- 如果工作区里不存在这些 wrapper 脚本，这是正常情况，不构成阻塞。
- 只有当技能目录里确实缺少对应文件时，才算技能资源不完整。

换句话说，这里的：

- `scripts/run_trends_collect.ps1`
- `scripts/run_feishu_bootstrap.ps1`
- `scripts/new_monitor_run.py`
- `references/*.md`

都默认指向技能目录内的打包资源，而不是用户当前仓库。

## 依赖边界

先读取这些文件：

- `references/dependency-boundaries.md`
- `references/runtime-prereqs.md`
- `references/default-workbook.md`
- `references/execution-rules.md`
- `references/operational-improvements-2026-04-20.md`

如果缺少依赖，要停止并明确说明缺什么依赖、应该先配置什么。

例子：

- 如果缺少飞书访问能力：
  明确说明必须先安装并配置 `$feishu-sheets-toolkit`。
- 如果浏览器/CDP 不可用或健康检查失败：
  明确说明必须先修复浏览器自动化环境。
  不要把那部分安装流程混进这个技能里。

## 本技能负责的内容

- 本地 `127.0.0.1:9225` CDP 会话检查与按需补起
- Trends 请求与页面结果解析
- 暴涨相关词筛选
- 候选词与 `GPTs` 的 compare 页面判定
- 本工作流内的重试、延后和跳过规则
- 通过 wrapper 编排 Feishu 读写
- run 文档和 checkpoint 的创建与更新

## 本技能不负责的内容

- Playwright MCP 安装
- 其他浏览器 MCP 安装
- 浏览器安装或系统级配置
- 代理工具安装或节点切换
- 飞书凭据创建
- Feishu 工具本身的实现

## 核心流程

### 1. 验证前置条件

先确认环境满足 `references/runtime-prereqs.md`。

然后对一个真实 Trends URL 做健康检查：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_trends_collect.ps1 health "https://trends.google.com/trends/explore?date=now%207-d&q=seedance,wan,qwen,veo,sora"
```

默认 wrapper 会先检查本地 `127.0.0.1:9225`；如果未监听，会尝试自动补起本地 Edge/Chromium CDP 会话，再进入 `health`。

只有在下面条件都满足时才继续：

- Google 首页可达
- Trends explore 页面能打开
- `relatedStatuses` 为 `200`

如果健康检查失败，停止批量执行，并提示用户先修复浏览器或代理环境。

如果自动补起后仍报 `connect ECONNREFUSED 127.0.0.1:9225`，优先按“本地 CDP 会话补起失败”处理；先修复浏览器环境，再重试 `health`。

### 2. 创建本次执行文件

不要把运行中的状态写进稳定的任务说明文档。每次执行都创建新的 run 文件和 checkpoint：

```powershell
python scripts/new_monitor_run.py --workspace . --date 2026-04-19 --run-id 1 --start-sheet oUaATj --start-row 2
```

这会创建：

- `docs/google-trends-monitoring/runs/<date>-run-<id>.md`
- `docs/google-trends-monitoring/checkpoints/<date>-run-<id>.json`

### 3. 读取飞书输入

本技能假定 `$feishu-sheets-toolkit` 已经安装并可用。这里使用内置 wrapper，不要硬编码机器相关路径：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_feishu_bootstrap.ps1 sheets --url "<workbook-url>"
powershell -ExecutionPolicy Bypass -File scripts/run_feishu_bootstrap.ps1 read --url "<workbook-url>" --range "oUaATj!A1:B20"
```

如果用户没有明确指定其他工作簿，默认使用 `references/default-workbook.md` 中定义的工作簿。

### 4. 采集暴涨相关词

对每个 Trends URL 执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_trends_collect.ps1 related "<trends-url>"
```

只保留下面两类结果：

- `qualifiesExploding = true`
- 或者本地化标签等价于 `Breakout` / `爆发` / `飙升`

当前“暴涨”口径已经更新为：

- 增长率严格大于 `3000%`
- 或显示为 `Breakout`

不要并行打开多个 Trends 页面。

### 5. 与 GPTs 做对比判定

对每个暴涨词执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_trends_collect.ps1 compare "<candidate>"
```

重点使用这些字段：

- `candidateIsNewInWindow`
- `candidateVsBenchmarkRatio`
- `candidateEndsNearZero`
- `qualifies`

默认把 `qualifies = true` 视为通过。

如果出现 `multiline_unavailable`，按 `references/execution-rules.md` 的规则重试。超过重试预算后，把它记为 deferred，而不是强行继续。

### 6. 调研意图并写回飞书

写入前先做这些事：

1. 按 `日期 + 暴涨词` 去重
2. `trends截图` 字段直接写 compare 分析链接
3. `关键词意图研究` 保持中文短摘要

写入前先读取：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_feishu_bootstrap.ps1 read --url "<workbook-url>" --range "rBLswo!A1:F30"
```

写入：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_feishu_bootstrap.ps1 write --url "<workbook-url>" --range "rBLswo!A5:F8" --values-file "<json-file>"
```

写完后等待几秒，再读回对应区域，确认 revision 确实变化。

注意：

- `--values-file` 必须是标准二维数组 JSON
- 不要用临时 PowerShell 管道去拼写回 JSON
- 写回 payload 应由 Python 或 Node 直接生成 UTF-8 文件
- compare 链接里如果候选词包含 `'`，写回前先编码为 `%27`
- readback 校验前，先把 Feishu 富文本单元格归一化为完整字符串
- 如果 write 命令没有显式报错，但 revision 不变或回读为空，优先排查 payload 形状和编码，而不是先怀疑飞书权限

### 7. 优先使用批处理编排脚本

对于完整批次执行，优先使用：

```powershell
python scripts/run_monitor_batch.py --workspace . --date 2026-04-20 --run-id 1
```

这个脚本会顺序完成：

- `health`
- 读取输入表
- 串行抓取 `related`
- 候选去重
- 串行执行 `compare`
- 生成 UTF-8 二维数组写回 payload
- 写回并 readback 校验
- 更新 run / checkpoint 文件

如果只是单步调试某个 URL 或某个 candidate，才分别调用基础脚本。

## 内置脚本

- `scripts/trends_cdp_collect.mjs`
  提供 `health`、`related`、`compare` 子命令。
- `scripts/run_trends_collect.ps1`
  首次使用时本地安装 `playwright-core`；执行前先检查并按需补起本地 `127.0.0.1:9225` CDP 会话，然后运行 `trends_cdp_collect.mjs`。
- `scripts/run_feishu_bootstrap.ps1`
  从标准 Codex skills 目录中定位并调用 `$feishu-sheets-toolkit`。
- `scripts/new_monitor_run.py`
  在当前工作区创建新的 run markdown 和 checkpoint JSON。
- `scripts/run_monitor_batch.py`
  执行完整批次监控，减少手工拼脚本造成的 JSON、编码和校验问题。
  当前脚本也处理带 `'` 的 compare URL 和 Feishu 富文本 readback 校验。

## 维护规则

不要把其他技能的安装逻辑混入这个技能。

如果未来需要补充下面这些能力：

- 浏览器环境安装
- MCP 安装
- 代理切换自动化
- Feishu 工具初始化

这些都应该放在独立技能或外部环境准备流程里，不属于这里。
