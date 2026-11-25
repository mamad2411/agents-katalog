---
name: ui-automation-router-zh
description: Route user intent to Web or App orchestrator skills when platform is unclear.
---

# UI 自动化分流

| 用户描述 | 主编排 Skill |
|----------|--------------|
| 网页、Web、浏览器、Playwright、SauceDemo、写用例、跑通、promote | **playwright-ui-orchestrator-zh** |
| 安卓、Android、App、真机、Settings、自然语言 App 用例 | **app-ui-orchestrator-zh** |
| 监控手机、录制步骤、录完生成用例、真机录制 | **app-ui-record-orchestrator-zh** |
| 探索测试、探索性测试、模块探索、explore、探索报告 | **playwright-ui-explore-zh** |
| PRD、需求、Excel 套件、req_suite | **req-suite-orchestrator-zh** |
| 导出 Excel、终版 json 转 xlsx、用例文档 | **playwright-ui-spec-export-excel-zh** |
| 不确定 | 先问 Web 还是 App，或默认 Web demo |

## 勿混淆

| 意图 | 走 | 勿走 |
|------|-----|------|
| 探索找问题、HTML 探索报告 | explore-zh | orchestrator（回归 spec） |
| 真机点按录制 | record-orchestrator-zh | app-orchestrator（NL 生成） |
| promote 后导出评审表 | export-excel-zh | req-suite（PRD 批量） |

## Demo 入口

```bash
python scripts/run_case.py examples/web/specs/demo-saucedemo-login.json
python scripts/run_app_case.py examples/app/specs/demo-open-settings-wifi.json
```
