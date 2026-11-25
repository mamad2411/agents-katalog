---
name: req-suite-orchestrator-zh
description: PRD（md/docx）→ 需求套件：Excel 测试用例 + 执行文件 → 人工审 Excel → 自动跑。触发词：上传 PRD、需求转用例、PRD 生成 Excel、需求套件、req_suite_init、从需求到自动跑。
---

# 需求套件主编排（PRD → Excel → 自动跑）

用户上传 **PRD（.md / .docx）** 并指定目标目录时走本 Skill。人工**只审 Excel**；执行文件在跑前**自动同步**，无需单独 sync / dry-run。

## 子 Skill / 工具

| 阶段 | 工具 / Skill |
|------|----------------|
| 平台 | **ui-automation-router-zh**（Web / App） |
| 一键初始化 | `scripts/tools/req_suite_init.py` |
| PRD 入库 | `scripts/tools/req_ingest.py` |
| PRD→Excel | `scripts/tools/req2excel.py`、**req2excel-zh** |
| 批量执行 | `scripts/tools/run_feature_suite.py`（**内含 Excel→执行文件同步**） |
| Web 跑挂 | **playwright-ui-heal-zh**（默认 ≤20 轮，`HEAL_MAX_ROUNDS` 可调） |
| App 跑挂 | **app-ui-heal-zh**（同上） |

列定义：[reference/excel-columns.md](reference/excel-columns.md)  
PRD 模板：[reference/prd-template.md](reference/prd-template.md)  
目录布局：[reference/output-layout.md](reference/output-layout.md)

## Agent 工作流（按序）

```
1. 确认：PRD 路径、目标目录 requirements/<featureId>/、平台、登录（Web）
2. 依赖：pip install openpyxl；docx 时需 pip install python-docx
3. 一键初始化：
     python scripts/tools/req_suite_init.py <prd.md|docx> --out requirements/<featureId>/ \
       --platform web --login @examples/web/logins/saucedemo-user.example.json
4. 复用检测：Web 搜 `specs/web/`、`examples/web/specs/`；App 查 [reuse-matrix](../app-ui-orchestrator-zh/reference/reuse-matrix.md)；必要时编辑 Excel「复用终版」列
5. （可选）Agent 精修 Excel 行 → req2excel --rows-json rows.json
6. 汇报用户审查：
     - requirements/<featureId>/测试用例.xlsx
     - execution/README.md
   ★ 禁止擅自将「评审状态」改为「已通过」
7. 用户确认通过后：
     - 用户把 Excel 评审状态改为「已通过」并保存关闭
     - python scripts/tools/run_feature_suite.py requirements/<featureId>/
       （自动 sync + 执行，改几次 Excel 都行，每次跑前都会重读）
8. 失败 → 对应 heal Skill（环境变量 **HEAL_MAX_ROUNDS**，默认 20）；Excel 稳定后再 promote 终版
```

## 用户话术示例

> 上传 `@需求.docx`，生成到 `requirements/my-feature/`，Web 登录用 `@examples/web/logins/saucedemo-user.example.json`。

审查 Excel 通过后：

> 跑 `requirements/my-feature/` 套件。

## 命令速查

```bash
# 一条命令（推荐）
python scripts/tools/req_suite_init.py path/to/prd.docx --out requirements/我的需求/

# 审查 Excel 通过后（唯一需要跑的）
python scripts/tools/run_feature_suite.py requirements/我的需求/
```

## Agent 精修 Excel（可选）

当 PRD 复杂、规则解析不够时，Agent 生成 `rows.json`：

```json
{
  "rows": [
    ["TC-001", "用例名称", "web", "P0", "是", "草稿", "前置", "http://...", "@config/web/logins/....json", "1. 步骤\n2. ...", "1. 预期\n2. ...", "specs/web/....json", "", "备注"]
  ]
}
```

```bash
python scripts/tools/req2excel.py requirements/我的需求/ --rows-json rows.json
```

列顺序见 [excel-columns.md](reference/excel-columns.md)。

## DoD

- 目标目录含：`prd.md`、`meta.json`、`测试用例.xlsx`、`execution/README.md`
- Excel 至少 1 行 P0，步骤/预期非空
- 用户改「已通过」后 `run_feature_suite` 退出码 0

## 禁止

- 未经用户确认把评审状态改为「已通过」
- 把 draft JSON 当交付物给用户维护
- 不转 docx 直接读二进制
- 跳过 Excel 审查直接全量 run（除非用户明确说已审）
- 要求用户手动 sync 或 dry-run（已内置到 run_feature_suite）

## 完成汇报模板

```
需求套件：requirements/<featureId>/
请审查：测试用例.xlsx（改「评审状态」为「已通过」）
说明：execution/README.md
通过后一条命令：
  python scripts/tools/run_feature_suite.py requirements/<featureId>/
```
