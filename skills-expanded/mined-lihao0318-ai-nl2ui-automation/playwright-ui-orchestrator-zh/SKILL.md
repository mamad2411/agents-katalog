---
name: playwright-ui-orchestrator-zh
description: Web NL orchestration: spec-gen → draft → run → heal → promote. For browser / Playwright cases.
---

# Web 编排

用户描述 **网页 / Web / Playwright** 回归用例时走本 Skill。

- **探索性测试 + 报告** → **playwright-ui-explore-zh**（不 promote）
- **安卓 App** → **app-ui-orchestrator-zh**
- **PRD 批量** → **req-suite-orchestrator-zh**
- **终版导出 Excel** → **playwright-ui-spec-export-excel-zh**

## 子 Skill

| 阶段 | Skill |
|------|-------|
| 生成草案 | **playwright-ui-spec-gen-zh** |
| 执行 | **playwright-ui-nl2spec-zh**（`run_case`） |
| 登录 / state | **playwright-ui-login-zh**（run_case 自动调用） |
| 自愈 | **playwright-ui-heal-zh**（环境变量 `HEAL_MAX_ROUNDS`，默认 20） |
| 表单 / 弹窗 | **playwright-ui-form-fill-zh**（spec-gen / heal 引用） |
| 运行时救场 | **playwright-ui-guardian-zh**（默认开启，`--no-guardian` 关闭） |

复用：生成前搜 `specs/web/`、`examples/web/specs/` 与 `scripts/run_code/` 已有终版/脚本，重叠 ≥80% 则扩展而非新建。

## 流水线

```
1. 【spec-gen】NL → specs/web/draft/<runId>-<slug>.json + scripts/run_code/draft/
2. 【nl2spec】python scripts/run_case.py specs/web/draft/...
3. 失败 → 【heal】改 draft/脚本；轮次上限 HEAL_MAX_ROUNDS（代码常量 MAX_HEAL_ROUNDS）
4. 连续通过 → Promote → specs/web/ + scripts/run_code/
5. （可选）【export-excel】终版 JSON → exports/*.xlsx
```

## Demo 参考

- `examples/web/specs/demo-saucedemo-login.json`
- `examples/web/specs/demo-captcha-dashboard.json`

## 命令

```bash
python scripts/orchestrator/run_web.py "demo saucedemo add to cart"
python scripts/orchestrator/run_web.py --spec specs/web/draft/xxx.json
python scripts/orchestrator/chat.py --platform web
python scripts/run_case.py examples/web/specs/demo-saucedemo-login.json
```

登录：**playwright-ui-login-zh**（`simple` / `captcha`）
