---
name: app-ui-record-orchestrator-zh
description: App 录制主编排：启停监控真机 → 生成 draft spec → run_app_case 复跑 → heal 多轮（默认≤20）→ promote 终版。触发词：监控手机、录制步骤、录完生成用例、录制复跑、录制终稿、record orchestrator。
---

# App 录制 → 用例 → 跑通 → 终版

与 **app-ui-orchestrator-zh**（自然语言）并列；Web 走 **playwright-ui-orchestrator-zh**。

## 子 Skill

| 阶段 | Skill |
|------|-------|
| 录制 | **app-ui-record-zh** |
| 生成草案 | **app-ui-spec-from-record-zh** |
| 预检 / 执行 / 自愈 | **app-ui-preflight-zh**、**app-ui-nl2spec-zh**、**app-ui-heal-zh** |
| 救场 | **app-ui-guardian-zh**（默认开启） |

命令速查：[reference.md](reference.md)。复用：[reuse-matrix.md](../app-ui-orchestrator-zh/reference/reuse-matrix.md)

## 流水线

```
1. 【app-ui-record-zh】启停录制 → runs/app/manual-<runId>/
2. 【app-ui-spec-from-record-zh】finalize → specs/app/draft/
3. validate_app_spec.py
4. 【app-ui-preflight-zh】→ 【app-ui-nl2spec-zh】run_app_case（默认勿 --launch）
5. 失败 → 【app-ui-heal-zh】最多 HEAL_MAX_ROUNDS 轮（默认 20）
6. 连续 2 次通过 → Promote → specs/app/
7. 汇报：复跑命令、report.html
```

## 执行

```bash
python scripts/run_app_case.py specs/app/draft/<runId>-<slug>.json
```

| 参数 | 何时用 |
|------|--------|
| `--launch` | 仅强制冷启动 |
| `--no-guardian` | 关闭默认 Guardian |
| `--fast` | 稳定后加速 |

## DoD / 禁止

- draft 校验通过 + 复跑退出码 0 + 报告与录制目标一致
- 不得 Appium、未跑通 promote、编排默认 `--launch`

## 参考

- [app-pitfalls-zh.md](../app-ui-orchestrator-zh/reference/app-pitfalls-zh.md)
- Demo：`examples/app/specs/demo-open-settings-wifi.json`
