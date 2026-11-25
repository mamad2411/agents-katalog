---
name: okr-run-web
description: Launch a local bilingual Web console for DoWithOKR, accepting raw requirements or user-authored GM OKR, visualizing .okr/ state, and refreshing after each skill step.
---

# OKR Run Web

## 核心定位

`okr-run-web` 是 `okr-run` 的可视化入口，不替代命令行流程。用户在浏览器中输入需求或 GM OKR，查看角色树、层级 OKR、KR 关联、状态看板、执行日志、证据和评分。

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| --project | string | 否 | 项目根目录，默认当前工作目录 |
| --no-runner | flag | 否 | 禁用自动 Runner，仅展示状态 |
| --no-browser | flag | 否 | 不自动打开浏览器 |

## 前置条件

- Node.js 运行时可用（v18+）。
- 运行时脚本存在于以下位置之一：
  1. `.claude/dowithokr/scripts/okr-run-web.mjs`（Claude Code 安装）
  2. `.agents/plugins/plugins/dowithokr/scripts/okr-run-web.mjs`（Codex 安装）
  3. `.codex-plugin/scripts/okr-run-web.mjs`（旧版 Codex 安装）
  4. 插件源目录 `scripts/okr-run-web.mjs`（开发模式）
- 缺失处理：提示用户运行 `install.sh` 安装运行时资源。

## 前置读取

- 检查 `.okr/` 目录是否存在。
  - 存在 → 读取 `.okr/active.md`、`.okr/status.md`、`.okr/evidence/`、`.okr/reviews/`，在页面展示断点续跑选项。
  - 不存在 → 页面展示启动表单，等待用户输入。
- 读取 `.okr/web/events.jsonl`（如存在），展示历史执行日志。

## 执行规则

- 本技能启动本地 Web 服务，不直接修改 `.okr/` 状态文件（状态修改由 `okr-run` 及其子技能完成）。
- Web 服务只监听 `127.0.0.1`，不暴露局域网地址。
- 启动时生成随机 session token，所有 API 请求必须携带 token。
- 不向外部网络发送需求、OKR、代码路径或证据内容。
- 页面支持中文 / English 切换，语言偏好保存在浏览器 localStorage。
- 子技能完成后通过 SSE 事件流和文件监听双机制刷新页面。

## 执行步骤

1. 定位运行时脚本：按优先级检查 `.claude/dowithokr/scripts/okr-run-web.mjs`、`.agents/plugins/plugins/dowithokr/scripts/okr-run-web.mjs`、`.codex-plugin/scripts/okr-run-web.mjs`、插件源 `scripts/okr-run-web.mjs`。
2. 启动本地服务：`node <script> --project <cwd>`。
3. 服务自动探测可用端口（从 3767 开始），生成 token，打开浏览器。
4. 终端输出访问 URL：`http://127.0.0.1:<port>/?token=<token>`。
5. 用户在页面选择输入模式：
   - **原始需求模式**：输入自然语言需求，点击"开始运行"触发 `okr-run` 从 M0 开始。
   - **GM OKR 模式**：输入 Objective、KR、边界，点击"开始运行"写入 `.okr/active.md` 并从 M1 继续。
6. Runner Adapter 检测可用执行器（Codex > Claude > 手动降级），触发 `okr-run`。
7. 页面通过 SSE `/events` 和文件监听持续刷新 OKR 状态。
8. 用户可在页面查看角色树、层级 OKR、KR 关联、状态看板、执行日志、证据和评分。
9. 服务退出时保留 `.okr/` 正常状态，不删除用户数据。

## 输出格式

本技能的输出是浏览器页面，不产生终端文本输出。终端仅显示：

```
DoWithOKR Web: http://127.0.0.1:<port>/?token=<token>
```

页面展示内容包括：

- 当前交付幕
- GM OKR（含边界和确认状态）
- 角色树（树形结构）
- 层级 OKR（按角色分组）
- KR 状态看板（表格，支持点击查看关联链路）
- 执行日志（时间倒序）
- 证据文件列表
- 评分复盘记录
- 最终 R

## 异常处理

- Node.js 不可用：提示用户安装 Node.js v18+。
- 运行时脚本不存在：提示用户运行 `install.sh` 安装。
- 端口被占用：自动尝试下一个端口。
- Runner 不可用（无 Codex 或 Claude CLI）：页面展示降级提示，生成可复制的 `okr-run` 指令。
- `.okr/` 文件解析失败：页面展示原始内容并标注"结构化解析失败"。
- SSE 连接断开：页面显示连接状态，自动重连。

## 产出写入

- 本技能通过 Runner Adapter 间接触发 `okr-run`，由子技能写入 `.okr/` 文件。
- GM OKR 模式下，直接写入 `.okr/active.md`（标记 `source: user_gm_input`）。
- 执行事件追加到 `.okr/web/events.jsonl`。
