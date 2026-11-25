---
name: playwright-ui-guardian-zh
description: Web 运行时 Guardian：L0 规则 + LLM 分诊关 layui 弹层/重试。默认开启。触发词：guardian、弹窗救场、--no-guardian。
disable-model-invocation: true
---

# Web Guardian（运行时 LLM 分诊）

**默认开启**；**不改终稿 spec**；永久修复仍走 **playwright-ui-heal-zh**。Guardian 是运行时救场，**不能**代替草案续跑或终稿全量回归。

环境变量：见项目根 `README.md` §Guardian、`specs/web/guardian/`（LLM 与 App 共用 `GUARDIAN_LLM_*`）。

## 默认行为

```powershell
python scripts/run_case.py specs/web/<用例>.json
```

| 关闭 / 降级 | 命令 |
|-------------|------|
| 完全关闭 | `--no-guardian` 或 `WEB_GUARDIAN=0` |
| 仅 L0 规则 | `--no-guardian-ai` |

| 环境变量 | 说明 |
|----------|------|
| `WEB_GUARDIAN` | 默认 `1` |
| `WEB_GUARDIAN_AI` | 默认 `1` |
| `GUARDIAN_LLM_API_KEY` | 无密钥时 L0 仍生效 |

## 插桩

`run_ui_spec.py` 每步：`before` → 点击/填写/执行代码 → 失败 `after_fail` 救场+重试 → `after`

## 决策流

```
L0 specs/web/guardian/*.rules.json（layui 遮罩、确认弹窗等）
→ L1 异常检测
→ L2 LLM（截图+页面摘要）
→ press_escape / click_outside / click_text / dismiss_layui / dismiss_overlays
```

## 产物

- `runs/web/<runId>/interventions.jsonl`
- `runs/web/<runId>/guardian-summary.json`
- 报告 HTML「Guardian 介入」

## 参考

- `scripts/web/guardian/`
- **app-ui-guardian-zh**（App 对称实现）
