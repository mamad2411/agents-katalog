---
name: playwright-ui-spec-gen-zh
description: 自然语言 → specs/web/draft + run_code/draft。不执行浏览器。由 orchestrator 调用。
disable-model-invocation: true
---

# Web 用例生成（NL → draft）

**只生成文件**。执行由 orchestrator → **playwright-ui-nl2spec-zh** / `run_case`。

## 输出

| 产物 | 路径 |
|------|------|
| 草案 spec | `specs/web/draft/<runId>-<slug>.json` |
| 草案 JS | `scripts/run_code/draft/<slug>_*.js` |

## 生成规则

1. [reference/draft-template.md](reference/draft-template.md)、[case-spec-schema](../playwright-ui-nl2spec-zh/reference/case-spec-schema.md)
2. 必备：`用例名称`、`用例说明`、`基础地址`、`有头模式`、`登录配置` 或 `状态文件`、`依赖登录态`、`步骤`
3. 推荐：`登录配置": "@examples/web/logins/saucedemo-user.example.json"`，`状态文件": "state/saucedemo-user-auth.json"`
4. **不写**账号密码
5. 操作：`打开` | `点击` | `填写` | `等待` | `执行代码`
6. JS：`async (page) => { ... }`，禁止末尾 `};`
7. 复杂步骤用 `@scripts/run_code/draft/...`

## 表单步骤（新增 / 编辑）

含下拉、上传、必填、cascader、弹窗填表时，生成「执行代码」前阅读：

- [form-controls-zh](../playwright-ui-form-fill-zh/reference/form-controls-zh.md)
- [form-fill-checklist](../playwright-ui-form-fill-zh/reference/form-fill-checklist.md)
- 范例索引：[script-index](../playwright-ui-form-fill-zh/reference/script-index.md)

铁律：

1. 弹窗表单在 `.el-dialog` / layer 内按 **label** 定位，禁止全页 placeholder（易误填列表筛选）。
2. `.el-select` / layui 下拉 / `.el-cascader` **禁止** `page.selectOption`。
3. 提交前在表单容器内审计必填（`*` / `lay-verify` / 「请选择」占位）。
4. 复杂表单统一用 `执行代码` + `*_form.js`；测试数据写 `window.__lastXxx`，assert 步骤配对。

## 默认步骤骨架

1. `打开` 首页（执行时可能因已有会话跳过）
2. `执行代码` 关弹窗 + 进菜单
3. `执行代码` iframe 操作
4. `等待`
5. `执行代码` 断言

## 交给编排执行

```bash
python scripts/run_case.py specs/web/draft/<runId>-<slug>.json
```

- 失败后在 **draft** 内迭代：修脚本 → 同命令再跑（自动续跑，不重新登录）
- **勿**在生成步骤写 `--login`（run_case 自动处理登录）
- promote 后终版命令：`python scripts/run_case.py specs/web/<用例名称>.json`（**全量**，无参数）

## 禁止

- 不执行浏览器（除非用户只要生成）
- 不写终版 `specs/web/`（promote 时再做）
- Selenium、`.bat`
