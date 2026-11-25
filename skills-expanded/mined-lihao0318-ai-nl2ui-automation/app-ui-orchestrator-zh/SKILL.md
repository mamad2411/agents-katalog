---
name: app-ui-orchestrator-zh
description: App NL orchestration: spec-gen → draft → run → heal → promote. Android + uiautomator2.
---

# App 编排

用户用 **自然语言** 描述安卓 / App / 真机回归用例时走本 Skill。

- **真机录制 → 用例** → **app-ui-record-orchestrator-zh**（非本 Skill）
- **Web** → **playwright-ui-orchestrator-zh**
- **PRD 批量** → **req-suite-orchestrator-zh**

## 子 Skill

| 阶段 | Skill |
|------|-------|
| 生成草案 | **app-ui-spec-gen-zh**（先查 [reuse-matrix.md](reference/reuse-matrix.md)） |
| 预检 | **app-ui-preflight-zh**（u2、IME、前台） |
| 执行 | **app-ui-nl2spec-zh**（`run_app_case`） |
| 自愈 | **app-ui-heal-zh**（环境变量 `HEAL_MAX_ROUNDS`，默认 20） |
| 运行时救场 | **app-ui-guardian-zh**（默认开启） |
| 启动配置 | **app-ui-launch-zh**（`examples/app/launches/` 或 `specs/app/launches/`） |

Pitfalls：[app-pitfalls-zh.md](reference/app-pitfalls-zh.md)

## 流水线

```
1. 【spec-gen】NL → specs/app/draft/<runId>-<slug>.json（复用 reuse-matrix）
2. validate_app_spec.py
3. 【preflight】→ 【nl2spec】run_app_case（默认勿 --launch）
4. 失败 → 【heal】改 draft / run_code_app；轮次上限 HEAL_MAX_ROUNDS
5. 连续 2 次通过 → Promote → specs/app/
```

## Demo

`examples/app/specs/demo-open-settings-wifi.json` — 系统 Settings，无需 APK。

## 命令

```bash
python scripts/orchestrator/run_app.py "open android settings wifi"
python scripts/orchestrator/chat.py --platform app
python scripts/run_app_case.py examples/app/specs/demo-open-settings-wifi.json
```

前置：`adb devices`、`python -m uiautomator2 init`

Launch：`examples/app/launches/android-settings.json`
