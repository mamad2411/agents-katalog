---
name: playwright-ui-nl2spec-zh
description: 子 Skill：执行 specs/web JSON（run_case）。编排用 playwright-ui-orchestrator-zh。触发词：run_case、执行 spec、### Error。登录 login-zh；自愈 heal-zh。
disable-model-invocation: true
---

# Web 业务用例执行（子 Skill）

> 自然语言端到端 → **playwright-ui-orchestrator-zh**（先 spec-gen 再本 Skill）。  
> 本 Skill 只**执行** JSON（`specs/web/draft/` 与终版），不生成草案。

## 唯一推荐入口

```bash
python scripts/run_case.py specs/web/<用例>.json
```

内部：检查/自动登录 → `run_ui_spec` 执行业务 → **默认**生成 `report.html` 并复制到 `reports/web/`。

## 登录（自动，勿让用户记 --login）

| 情况 | 行为 |
|------|------|
| 无 state 或 state 无效 | 自动 `run_login`，再跑业务 |
| **终稿** + 有 state | 步骤 1 始终「打开」首页并加载 state；**不 skip-open** |
| **草案** + 有 state | 首页会话可 skip-open；在业务页会先回首页/state 恢复，**避免误判重登** |
| 业务失败像登录超时 | 终稿步骤 1 类失败可能自动重登；步骤 2+ 保持当前页（草案可续跑） |
| `--login` | **仅**用户或编排要求强制重登时 |

## 草案 vs 终稿（`run_case` 行为）

| 路径 | 无参数再跑 | 失败后 |
|------|------------|--------|
| `specs/web/draft/*.json` | 自动从 `failure.json` **续跑**（保持浏览器、不重新登录） | 修脚本后同命令再跑 |
| `specs/web/*.json`（非 draft） | **全量从步骤 1** | 修脚本后同命令 **全量**，不续跑 |

登录配置：`config/web/logins/`（业务 spec 的 `登录配置` 字段）。
单独刷新 state：`python scripts/tools/run_login.py`（见 **playwright-ui-login-zh**）。

## 假成功（必读）

1. `run_code` JS：`async (page) => { ... }`，**禁止**文件末尾 `};`
2. 成功看 `cli_success()`：输出无 `### Error`；不信单独退出码或 run-log 假成功
3. Windows 复杂逻辑用 `@scripts/run_code/*.js`，勿超长内联

## 其它命令（调试 / 草案续跑）

| 场景 | 命令 |
|------|------|
| 草案失败后续跑 | 直接再跑 `run_case specs/web/draft/...`（自动 `--from-step`） |
| 手动从第 N 步（草案 heal） | `run_case specs/web/draft/... --from-step N --keep-browser` |
| 已在同一会话（底层） | `run_ui_spec.py ... --skip-open --keep-browser` |
| 终稿全量回归 | `run_case specs/web/<终版>.json`（无额外参数） |
| 强制重登 | `--login` |
| 关浏览器 | `--close` |
| 不要报告 | `--no-report` |

**禁止**日常拆成：`run_login` 关窗后再另开终端 `run_ui_spec`。

## JSON 规范

[reference/case-spec-schema.md](reference/case-spec-schema.md)

示例：`examples/web/specs/demo-saucedemo-login.json`

## 常见 Web 要点

| 现象 | 处理 |
|------|------|
| 登录态失效 / 步骤 2 超时 | `run_case <spec> --login` 或删 `state/*.json` |
| SauceDemo 仍见登录页 | URL 含 `inventory` 但 DOM 有 `#user-name` → 会话过期，重登 |
| 复杂表单（el-select / cascader） | 见 [form-controls-zh](../playwright-ui-form-fill-zh/reference/form-controls-zh.md)；用 `执行代码` + `*_form.js` |
| 验证码登录 Demo | 先起 `examples/web/demo-site`，登录 spec 见 `examples/web/logins/demo-captcha-user.example.json` |
| JS 语法错误 | `async (page) => { ... }`，**禁止**末尾 `};` |

## 产物

| 路径 | 说明 |
|------|------|
| `runs/web/<runId>/run-log.md` | 步骤日志 |
| `runs/web/<runId>/failure.json` | 失败与 `resumeHint` |
| `runs/web/<runId>/steps/*.png` | 每步截图 |
| `reports/web/<runId>/report.html` | **默认**可读报告 |
| `reports/index.html` | 历次总览 |

补报告：`python scripts/tools/generate_run_report.py --platform web --latest`

## 禁止

- `run/*.bat`、Selenium
- 业务 spec 写密码
- `run_code` 以 `};` 结尾

## 失败

→ **playwright-ui-heal-zh**
