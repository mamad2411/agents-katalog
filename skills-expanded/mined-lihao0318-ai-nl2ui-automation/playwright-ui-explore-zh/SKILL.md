---
name: playwright-ui-explore-zh
description: Web 模块探索性测试：登录 → 进入模块 → Agent 交互探索 → 记录发现 → 生成 HTML 报告。触发词：探索测试、探索性测试、帮我探索、模块探索、explore module、生成探索报告。
---

# Web 模块探索性测试

用户指定 **Web 模块名**并要求 **探索性测试 + 报告** 时走本 Skill。

与 **playwright-ui-orchestrator-zh**（脚本化回归）的区别：本 Skill **不生成终版 spec**，而是产出 **探索报告**（问题发现、区域覆盖、截图）。

## 前置

- 环境：`playwright-cli`、Python
- 模块清单：`specs/web/modules/registry.json`（Demo 已含 `inventory`；新模块在此注册）
- 探索 API：`scripts/web/explore_module.py`（`init_explore` / `add_journal_entry` / `finalize_explore`）

## 流水线（按序）

```
1. init — 登录 + 进入模块 + 创建 run 目录
2. explore — Agent 用 playwright-cli 交互探索
3. journal — 每条观察写入 explore-journal.jsonl
4. finalize — 生成 report.html 并发布到 reports/web/
5. 向用户汇报：模块、发现数、报告路径、主要问题摘要
```

## 1. 初始化

在项目根目录通过 Python API 调用：

```bash
python -c "import sys; sys.path.insert(0,'scripts'); from bootstrap import setup_paths; setup_paths(); from explore_module import init_explore; print(init_explore('inventory', login='@examples/web/logins/saucedemo-user.example.json'))"
```

可选登录：`login=` 传 `@config/web/logins/<your-login>.json` 或 `@examples/web/logins/saucedemo-user.example.json`

记下输出的 **runId** 与 **run_dir**（如 `runs/web/explore-20260608-120000-inventory`）。

解析模块清单：

```bash
python -c "import sys; sys.path.insert(0,'scripts'); from bootstrap import setup_paths; setup_paths(); from explore_module import resolve_module, load_registry; print(resolve_module('inventory', load_registry()))"
```

## 2. 探索策略（Agent 执行）

浏览器在 init 后**保持打开**。按 registry 中 **checklist** 逐区域探索：

| 区域类型 | 建议操作 |
|----------|----------|
| 导航入口 | 重复进/出、关弹窗 |
| 搜索/筛选 | 空值、非法格式、边界长度 |
| 表单 | 必填、控件类型；见 [form-controls-zh](../playwright-ui-form-fill-zh/reference/form-controls-zh.md) |
| 列表/结果 | 空结果、有数据、排序 |
| 按钮/操作 | 可见性、二次确认、取消路径 |

**交互方式**（任选，保持同一会话）：

- `playwright-cli run-code "async page => { ... }"`
- `playwright-cli click/fill/snapshot` 等

**每完成一项有意义观察**，记 journal（Python API）：

```bash
python -c "
import sys
sys.path.insert(0,'scripts')
from bootstrap import setup_paths
setup_paths()
from pathlib import Path
from explore_module import add_journal_entry
add_journal_entry(
    Path('runs/web/explore-<runId>'),
    area='商品列表',
    action='点击 Add to cart',
    observation='购物车角标 +1',
    severity='info',
    recommendation='',
    screenshot=True,
)
"
```

| severity | 含义 |
|----------|------|
| `info` | 正常行为记录 |
| `minor` | 体验/文案/小问题 |
| `major` | 功能缺陷 |
| `blocker` | 无法继续探索 |

## 3. 生成报告

```bash
python -c "import sys; sys.path.insert(0,'scripts'); from bootstrap import setup_paths; setup_paths(); from pathlib import Path; from explore_module import finalize_explore; finalize_explore(Path('runs/web/explore-<runId>'))"
```

产物：

| 路径 | 说明 |
|------|------|
| `runs/web/explore-*/report.html` | 探索报告 |
| `reports/web/explore-*/report.html` | 发布副本 |
| `reports/index.html` | 总览 |

## 4. 向用户汇报

1. 模块名、角色、耗时
2. 探索记录数、问题数（按 severity）
3. checklist 覆盖情况
4. **报告链接**
5. Top 3 发现（major/blocker 优先）

## 新模块注册

编辑 `specs/web/modules/registry.json`：

```json
{
  "baseUrl": "https://www.saucedemo.com",
  "modules": {
    "inventory": {
      "aliases": ["商品列表", "SauceDemo inventory"],
      "menuPath": [],
      "entrySelector": ".inventory_list",
      "checklist": [
        {"area": "商品列表", "hints": "加购、排序、详情链接"}
      ]
    }
  }
}
```

有现成 nav 脚本则填 `navScript`：`@scripts/run_code/xxx.js`

## 禁止

- 不要把探索过程 promote 成终版 spec（除非用户另要求）
- 不要 init 后关闭浏览器再另开终端
- 不要无 journal 直接 finalize

## 与编排 Skill 关系

| 用户意图 | Skill |
|----------|-------|
| 探索模块、找问题、出探索报告 | **本 Skill** |
| 写回归用例、跑通、promote | **playwright-ui-orchestrator-zh** |
| PRD → Excel 批量跑 | **req-suite-orchestrator-zh** |
