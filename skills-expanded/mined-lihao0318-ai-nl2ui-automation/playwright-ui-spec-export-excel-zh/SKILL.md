---
name: playwright-ui-spec-export-excel-zh
description: 终版 specs/web 或 specs/app JSON → 评审 Excel（步骤/预期合并编号换行）。触发词：导出 Excel、终版 json、用例文档、评审、xlsx。
---

# UI 用例导出 Excel（终版 JSON → 评审表）

用户提供 **promote 后** 终版 JSON 时，生成**一行一用例**扁平表；**不执行浏览器/真机**。

## 输入与输出

| 输入 | 路径 |
|------|------|
| Web 终版 | `specs/web/<用例名称>.json` |
| App 终版 | `specs/app/<用例名称>.json`（含 `平台: android`） |
| 草案 | **勿**导出，先 promote |

| 输出 | 路径 |
|------|------|
| 单用例 | `exports/<用例名称>.xlsx` |
| 合并 | `exports/测试用例汇总.xlsx`（`-o` 指定） |

## 执行命令

```bash
pip install openpyxl
python scripts/tools/export_spec_to_excel.py examples/web/specs/demo-saucedemo-login.json
python scripts/tools/export_spec_to_excel.py examples/app/specs/demo-open-settings-wifi.json
```

多个用例：

```bash
python scripts/tools/export_spec_to_excel.py specs/web/A.json specs/app/B.json -o exports/双端汇总.xlsx
```

## 表头结构

| 列 | 说明 |
|----|------|
| 用例名称 | JSON `用例名称` |
| 用例说明 | JSON `用例说明` |
| 前置条件 | 登录态 / 启动配置 / 有头模式 |
| 基础地址 | Web `基础地址`；App 可为包名或 `—` |
| 关联脚本 | `run_code/` 或 `run_code_app/` 文件名 |
| **步骤描述** | 全部步骤合并，`1.` `2.` 换行 |
| **预期结果** | 全部预期合并，同样编号 |
| 备注 | JSON 路径、推荐 `run_case` / `run_app_case` 命令 |

Web 登录类 JSON（`examples/web/logins/`、`config/web/logins/`）合成 4 条步骤；密码脱敏。

## Agent 工作流

1. 确认终版 `specs/web/` 或 `specs/app/`（非 `draft/`）。
2. 检查 `@scripts/run_code/...` 或 `@scripts/run_code_app/...` 存在。
3. `python scripts/tools/export_spec_to_excel.py <json> [...]`
4. 告知 `exports/*.xlsx`；Web 复跑 `run_case`，App 复跑 `run_app_case`（**无** `--login` / `--launch`）。

## 禁止

- Excel 不能作为执行输入
- 不得写入真实密码
- 不得用 draft 当评审终稿

## 完成定义

- 退出码 0，xlsx 可打开
- 「步骤描述」条数 = JSON `步骤` 条数（登录类为 4）
- 单元格内编号列表可换行显示
