---
name: app-ui-preflight-zh
description: App 跑用例前预检：u2、静默 IME、前台、登录凭据。由 app-ui-orchestrator / app-ui-nl2spec 调用。触发词：预检、preflight、跑前检查。
disable-model-invocation: true
---

# App 跑前预检

**执行 `run_app_case` 前必做**（编排 Step 0.5）。阻塞项未解决则不跑全量。

## 命令

```bash
python scripts/tools/probe_u2.py
python scripts/tools/probe_app_input.py
python scripts/tools/validate_app_spec.py specs/app/draft/<file>.json   # 有 spec 时
```

## 检查清单

| # | 项 | 通过条件 | 失败处理 |
|---|-----|----------|----------|
| 1 | u2 连通 | `probe_u2.py` 退出码 0 | `pip install -r requirements.txt` + `python -m uiautomator2 init` |
| 2 | 静默 IME | `probe_app_input.py` 含 `silent_ime: OK` | `python -m uiautomator2 init` |
| 3 | adb 前景 | `probe_u2` 显示目标包或桌面 | 编排勿默认 `--launch`；不在前台会自动拉起 |
| 4 | spec 合法 | `validate_app_spec.py` OK | 修 draft JSON / `@scripts/run_code_app` 路径 |
| 5 | 业务登录凭据 | 用例含登录步骤 | 在 `用例说明` 或 `config/local.env` 中配置所需变量（勿写入 spec JSON） |
| 6 | 剪贴板策略 | 未设 `APP_USE_CLIPBOARD` | 默认禁止；见 [app-pitfalls-zh.md](../app-ui-orchestrator-zh/reference/app-pitfalls-zh.md) |

## Demo（Settings）无需登录

`examples/app/specs/demo-open-settings-wifi.json` 跳过第 5 项。

## 输出

- 全部通过 → 汇报「预检 OK」，进入 `run_app_case`
- 任一项失败 → 汇报阻塞项 + 修复命令，**不跑全量**（除非用户强制）

## 参考

- [app-pitfalls-zh.md](../app-ui-orchestrator-zh/reference/app-pitfalls-zh.md)
