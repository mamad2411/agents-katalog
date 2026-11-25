---
name: playwright-ui-heal-zh
description: 子 Skill：Web 失败后自愈，改 draft/run_code 重跑。默认最多 20 轮（HEAL_MAX_ROUNDS 可调）。触发词：failure.json、自愈、### Error、登录态失效、TimeoutError。
disable-model-invocation: true
---

# Web 用例失败自愈

由 **playwright-ui-orchestrator-zh** / CLI heal prompt 注入；Cursor 中勿依赖自动触发（`disable-model-invocation`）。

## 轮次上限

- 默认 **20 轮**（环境变量 `HEAL_MAX_ROUNDS`；代码常量 `MAX_HEAL_ROUNDS` 见 `scripts/framework/pipeline.py`）
- 用户要求更多时：执行前设 `HEAL_MAX_ROUNDS=50` 或 `100`（Windows: `$env:HEAL_MAX_ROUNDS=50`）
- 每轮：读 failure → 改 draft/脚本 → 重跑；**跑通即停**，不必跑满上限

## 何时用

- `run_case` 失败或「日志成功但页面没动」
- 编排迭代：**只改 draft**，不改终版直至 promote

## 输入（按序）

1. **`runs/web/<runId>/heal-context.json`**（推荐，含 failure + 参考脚本片段）
2. `runs/web/<runId>/failure.json`（含 category、failedScript、suggestedActions、resumeFromStep）
3. `failure.json` 内 `snapshotPath`（失败 DOM 快照，若有）
4. `runs/web/<runId>/run-log.md` 与 `steps/*.png`（screenshots.failedStep / previousStep）
5. `guardian` 字段（若 Guardian 已介入仍失败 → 改 run_code 永久修复）

**优先按 failure.category / suggestedActions 分诊**，再查下方分诊树与 form-fill-zh。

## 假成功

| 信号 | 处理 |
|------|------|
| `Unexpected token ';'` | JS 末尾去掉 `};` |
| 退出码 0 但有 `### Error` | 未成功 |
| run-log「执行成功」但 UI 未变 | 查 Error / 多 session |

## 分诊树

1. **登录页 / 首页元素 Timeout** → 登录态失效：`run_case <spec> --login` 或依赖 run_case **自动重登**
2. **SyntaxError** → 修 JS 格式（`async (page) => { ... }`，无末尾 `};`）
3. **SauceDemo inventory 断言失败** → 先确认 URL 与 DOM 是否仍在登录页；见 `examples/web/run_code/saucedemo_inventory_assert.js`
4. **弹窗遮挡** → 关 cookie / overlay，限定 dialog scope
5. **iframe** → 在正确 frame 内操作，勿在全页找控件
6. **断言** → `_assert.js`、测试数据 `window.__lastXxx`
7. **el-cascader / el-select** → 勿 `page.selectOption`；见 [form-controls-zh](../playwright-ui-form-fill-zh/reference/form-controls-zh.md)
8. **验证码 Demo 连不上** → 确认 `examples/web/demo-site` 已在 8765 端口
9. **表单未提交 / 字段未填 / 选错控件** → [form-controls-zh](../playwright-ui-form-fill-zh/reference/form-controls-zh.md)、[script-index](../playwright-ui-form-fill-zh/reference/script-index.md)、[form-fill-checklist](../playwright-ui-form-fill-zh/reference/form-fill-checklist.md)

## 修改范围

| 可改 | 勿改 |
|------|------|
| `specs/web/draft/`、draft run_code | 密码进 spec |
| 终版（用户明确要求时） | Selenium、`.bat` |

## 重跑命令

```bash
# 草案：修完脚本后直接再跑（自动续跑，勿加 --login）
python scripts/run_case.py specs/web/draft/<file>.json

# 分段验证
python scripts/tools/run_web_step_code.py specs/web/draft/<file>.json --step N --keep-browser --skip-login-check

# 草案：手动从第 N 步
python scripts/run_case.py specs/web/draft/<file>.json --from-step N --keep-browser --skip-login-check

# 终稿：heal 改终版后始终全量
python scripts/run_case.py specs/web/<终版>.json

# 强制重登
python scripts/run_case.py specs/web/<用例>.json --login
```

**草案**迭代用 `specs/web/draft/...`，**勿**默认写 `--login`。

## 产物与报告

- 每步截图：`runs/web/.../steps/`
- 失败 enrich：`failure.json` + `heal-context.json` + 可选 `failure-snapshot.md`
- 分类规则：`scripts/framework/heal_playbook.json`
- 失败后可用 `generate_run_report.py` 补报告

## 完成定义

- 退出码 0，无 `### Error`
- `reports/.../report.html` 步骤与截图符合目标
