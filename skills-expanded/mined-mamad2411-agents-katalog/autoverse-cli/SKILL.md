---
name: autoverse-cli
description: 仅在用户要安装、配置、调用或排障 Autoverse CLI 本身时使用，处理登录、凭证 profile、账户与点数、命令语法、JSON/退出码和原子命令合同。不要因普通“找论文、做开题、沿种子扩展”请求单独触发。
metadata:
  version: 0.1.0
---

# Autoverse CLI

Autoverse 的系统层 Skill。只负责让 Agent 正确安装、登录、发现和调用 CLI。

产品链路：

```text
scholar-relay API → autoverse CLI
```

CLI 是唯一稳定执行面。没有 MCP 产品路径。

## 何时使用

使用本 Skill：

- 用户要安装、升级或验证 `autoverse`；
- 要登录、退出、切换 profile 或检查身份；
- 要查看点数、价目或补点入口；
- 要了解命令、旗标、JSON、退出码或错误 code；
- CLI 调用失败，需要按结构化错误恢复；
- 开发/CI 需要平台 Key，而不是浏览器会话。

不要因普通“找论文、做开题、沿种子扩展”请求单独触发；本 Skill 不定义科研作业流程或产物。

## 安装与版本

```text
pipx install autoverse
autoverse --version
autoverse --help
```

要求 Python 3.12+。包名和命令都是 `autoverse`。

如果用户明确要升级：

```text
pipx upgrade autoverse
```

不要安装或配置 MCP；0.2.0 起 CLI 只有 `autoverse` 入口。

## 登录与凭证

默认登录：

```text
autoverse login
autoverse whoami
```

- 浏览器由人完成邮箱或 GitHub 确认。
- 凭证进入 OS 钥匙串；不要写入论文项目、Skill 或对话。
- 不索要或打印 API Key。
- CI / 脚本明确需要平台 Key 时，才使用 `AUTOVERSE_API_KEY` 或 `login --token`。
- `--profile <name>` 是全局旗标，放在动词前；不同 profile 使用独立凭证。

## Agent 标准调用

Agent 和自动化调用固定为：

```text
autoverse --json --quiet <动词> ...
```

- stdout 成功时只有一行 `{request_id,data}`；
- stderr 成功时为空；
- 失败时 stdout 为空，stderr 只有一行 `{error:{code,message,request_id,retryable}}`；
- 只根据 code、retryable 和退出码分支，不解析自然语言日志；
- 用法/输入错误退出 2，运行时/鉴权/点数/上游错误退出 1；
- 不添加 `--raw`、`--fields`、`--jq`、TSV 或 YAML；完整公开 API 的高级调试走 `api` 逃生舱。

用户问具体命令、字段或错误时，读取 [references/commands.md](references/commands.md)。

## 最小直接配方

题名识别：

```text
autoverse --json --quiet search "<title fragment>" --limit 5
```

单篇解析：

```text
autoverse --json --quiet resolve doi:10.x/y
```

一袋 ID：

```text
autoverse --json --quiet batch -f ids.txt
```

- `ids.txt` 必须 UTF-8、一行一个稳定 ID、1–50 条；
- 不把 Markdown 笔记直接交给 batch；
- batch 部分失败仍 exit 0，逐条读取 `items[].error`。

## 错误恢复

- `INVALID_SESSION` / 401：请求人重新 `autoverse login`。
- `INSUFFICIENT_CREDITS` / 402：执行 `usage`，再给出 `topup`；停止付费调用。
- `REQUEST_OUTCOME_UNKNOWN`：先查 usage，不重复发送。
- `retryable=true`：同一逻辑调用最多再尝试一次。
- `retryable=false`：停止，不猜路径、不换来源。
- `CURSOR_OPTION_CONFLICT`：cursor 页只带 cursor 和可选 limit。
- `INPUT_FILE_*`：修正文件后再调用 batch。
- `RELATED_ID_*`：不要把 DOI、裸数字或含斜杠 ID 塞入 related 路径。
- 503：按当前命令合同停口，不用 search 假装替代 related。

## 账户与点数

```text
autoverse --json --quiet whoami
autoverse --json --quiet usage
autoverse topup
```

`topup` 只显示账户邮箱和购买入口，不在 CLI 内收款。Agent 不代用户付款。

## 能力边界

- 精选动词输出稳定最小 DTO，不透出完整 OpenAPI 对象。
- `api` 只用于用户明确要求的高级原始 API 调试；普通调用优先精选动词。
- CLI 不创建或管理 run、keep、工作区、`notes/` 或 `kept.md`。
- CLI 不写综述正文、不声称全文、不提供期刊分区。
- 用户文件由人或调用方管理。

## 完成标准

一次系统层任务完成时：

- CLI 已安装且版本可确认；
- 登录/凭证路径明确，没有泄露 Key；
- 使用了正确的全局旗标位置；
- Agent 调用采用 `--json --quiet`；
- 错误按 code 和 retryable 处理；
- 没有调用或重新引入 MCP。
