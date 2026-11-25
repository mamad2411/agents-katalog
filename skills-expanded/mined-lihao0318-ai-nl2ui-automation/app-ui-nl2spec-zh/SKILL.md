---
name: app-ui-nl2spec-zh
description: 子 Skill：预检后执行 specs/app JSON（run_app_case，adb/u2）。编排用 app-ui-orchestrator-zh。触发词：run_app_case、执行安卓 spec、真机跑用例。
disable-model-invocation: true
---

# App 用例执行（子 Skill）

> 自然语言端到端 → **app-ui-orchestrator-zh**。本 Skill 只**执行** JSON。

**跑前**：**app-ui-preflight-zh**（probe_u2 + probe_app_input）

**必读**：[app-pitfalls-zh.md](../app-ui-orchestrator-zh/reference/app-pitfalls-zh.md)

## 入口

```bash
python scripts/tools/probe_u2.py
python scripts/tools/probe_app_input.py
python scripts/run_app_case.py examples/app/specs/demo-open-settings-wifi.json
```

内部：`prepare_app_session` → `run_app_spec`（每 spec 步可插 Guardian）→ 默认 `reports/app/.../report.html`。

## 启动与登录

| 情况 | 行为 |
|------|------|
| App 不在前景 | 自动 `am start` |
| 已在前景 | 跳过冷启动 |
| `--launch` | **仅** force-stop 后冷启动 |
| 业务登录 | `run_code_app` 内按需（Demo 无需登录） |

## 参数

| 参数 | 含义 |
|------|------|
| `--fast` | 少等待、少关键页截图 |
| `--record` | adb 录屏 mp4 |
| `--no-page-screenshots` / `--no-show-click` / `--no-report` | 截图与报告控制 |
| **`--no-guardian`** | 关闭 Guardian（默认已开） |
| **`--no-guardian-ai`** | Guardian 仅 L0 规则 |

**无** `--from-step` / `--only-step`（Web 专用）。App 长流程分段：直接跑 `scripts/run_code_app/*.py` 或看 `step-results.json`。

## 定位与规范

- `text:`、`textContains:`、`resourceId:`
- 复杂流程：`执行代码` → `@scripts/run_code_app/...` 或 `@examples/app/run_code_app/...`
- [app-case-spec-schema.md](reference/app-case-spec-schema.md)

## 跑后验收

退出码 0 + `runs/app/<runId>/steps/flow-records.json` 与用户 NL 对应。

## 分段调试（heal 第 2 轮起优先）

```bash
python examples/app/run_code_app/demo_tap_wifi.py
```

复用查表：[reuse-matrix.md](../app-ui-orchestrator-zh/reference/reuse-matrix.md)

## 产物

| 路径 | 说明 |
|------|------|
| `runs/app/<runId>/run-log.md` | 步骤日志 |
| `runs/app/<runId>/steps/flow-records.json` | 业务记录 |
| `runs/app/<runId>/failure.json` | 失败与 resumeHint |
| `runs/app/<runId>/interventions.jsonl` | Guardian 介入（若启用） |
| `reports/app/<runId>/report.html` | 默认可读报告 |

补报告：`python scripts/tools/generate_run_report.py --platform app --latest`

## 禁止

Appium、编排默认 `--launch`、预检未过反复全量跑、默认剪贴板输入。

失败 → **app-ui-heal-zh**
