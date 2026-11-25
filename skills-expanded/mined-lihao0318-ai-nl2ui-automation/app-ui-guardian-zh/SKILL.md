---
name: app-ui-guardian-zh
description: App 运行时 Guardian：L0 规则 + LLM 分诊关弹窗/重试。默认开启。触发词：guardian、弹窗救场、LLM 分诊、--no-guardian。
disable-model-invocation: true
---

# App Guardian（运行时 LLM 分诊）

**默认开启**；**不改终稿 spec**；永久修复仍走 **app-ui-heal-zh**。

安装与环境变量：见项目根 `README.md` §Guardian、`specs/app/guardian/env.example`。

## 默认行为

```powershell
python scripts/run_app_case.py specs/app/<用例>.json
# 已含 Guardian（L0 + LLM，有密钥时）
```

| 关闭 / 降级 | 命令 |
|-------------|------|
| 完全关闭 | `--no-guardian` 或 `APP_GUARDIAN=0` |
| 仅 L0 规则 | `--no-guardian-ai` |

| 环境变量 | 说明 |
|----------|------|
| `APP_GUARDIAN` | 默认 `1` |
| `GUARDIAN_LLM_API_KEY` | MiniMax 等（Anthropic 兼容）；无密钥时 L0 仍生效 |
| `GUARDIAN_LLM_BASE_URL` | 默认 `https://api.minimaxi.com/anthropic` |
| `GUARDIAN_LLM_MODEL` | 默认 `MiniMax-M2.7` |
| `APP_GUARDIAN_AI_MAX` | 每 run LLM 次数上限（默认 5） |

## 插桩范围

| 层级 | 位置 |
|------|------|
| **Spec 步** | `run_app_spec.py` 每步 before / 失败救场 |
| **业务子步** | `run_guarded_step()`（18 步全流程等） |

## 决策流

```
L0 规则（specs/app/guardian/*.rules.json）→ 不调 LLM
L1 异常 → L2 LLM（截图+UI 摘要）→ 白名单 action → 可选 retry
```

白名单 action：`keyevent_back`、`tap_outside`、`tap_text`、`dismiss_overlays`、`none`

## 产物

- `runs/app/<runId>/interventions.jsonl`
- `runs/app/<runId>/guardian-summary.json`
- 报告 HTML「Guardian 介入」一节

## 禁止

- LLM 自动改 `run_code_app` / 终版 spec
- 密钥写入仓库
- 设置面板用 `tap_text 取消`（会撤销开关）

## 参考

- `scripts/app/guardian/`
- **app-ui-heal-zh**（跑挂后改 draft）
