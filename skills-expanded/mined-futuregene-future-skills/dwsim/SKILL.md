---
name: dwsim
description: "DWSIM 化工流程模拟：用 Python 调用 DWSIM .NET 自动化接口搭 flowsheet、跑 PT/PH 闪蒸与单元操作、查组分库与推荐物性方法；无需 DWSIM 时可单独用 22 种物性方法目录与 21 个常见组分数据"
---

> **移植说明（2026-11-02，本仓库添加）**：本技能自 fdias78git/dwsim-claude-integration 固定 commit `91e1f7a` 导入。上游 SKILL.md 没有 YAML frontmatter，本仓库补了 `name`/`description` 两行；正文只改了一处链接（见下），其余未动。
> 
> **物性方法选择表的去处**：上游正文 Step 2 说「Apply the selection table from the `dwsim-expert` agent」，那张表在上游 `.claude/agents/dwsim-expert.md` 里，本技能已把它作为 `references/dwsim-expert-agent.md` 一并导入（含选择表、自动推荐判定树、收敛故障排查表、单元操作检查清单）。
> 
> **运行前提（本机实测）**：`src/` 是真实 Python 库（23 个 .py，`py_compile` 全通过，16 个模块可直接 `import`），但它只是 DWSIM .NET 自动化接口的薄封装——`src/core/automation.py` 在 `initialize()` 里 `import clr` 并 `AddReference` 六个 DWSIM DLL，所以闪蒸、flowsheet、单元操作、报告生成都必须先装 DWSIM 桌面端（上游按 Windows `C:\Program Files\DWSIM` 叙述，Linux 需 Mono，macOS 未验证）再 `pip install pythonnet`。本机 pythonnet 与 DWSIM 均不存在：`DWSIMAutomation()` 构造即抛 `ValueError`（`config.example.json` 的 `install_path` 为空），填好路径后也会卡在 `initialize()` 的 `import clr`。**因此本技能在本环境只提供方法与代码骨架，不能真正跑出流程模拟结果。**
> 
> **无需 DWSIM 就能用的子集（实测）**：`src/thermo/property_packages.py` 的 22 种物性方法目录与 `recommend_for_system()`（水+乙醇→`nrtl`/`uniquac`/`unifac`；烃类→`peng-robinson`/`srk`/`lee-kesler-plocker`；含电解质→`extended-nrtl`/`sour-water`）；`src/thermo/compound_properties.py` 的 `CompoundDatabase()` 退化到内置 21 个组分（Water…Acetic acid）。注意正文示例 `db.search("propyl")` 在无 DWSIM 时返回 `[]`（内置表里没有 propyl 前缀名），`property_packages.py` 注释自称 "31+ property packages" 而实际字典只有 22 条。
> 
> **未导入的部分**：上游 `.claude/commands/*.md`（`/dwsim`、`/dwsim-flash`、`/dwsim-props` 斜杠命令）、`.claude/skills/dwsim/` 之外的 agent 安装说明 `SETUP_PROMPT.md`、`CHANGELOG.md`。因此随附的 `SETUP.md` 中「安装到 Claude Code」的段落不适用，Python 库与环境变量部分适用。
> 
> **许可**：本仓库代码 MIT（Copyright (c) 2026 Felipe Dias）。DWSIM 本体是 GPLv3，未随本技能分发，需用户自行从 dwsim.org 安装。

# DWSIM Automation Skill

## What This Skill Does

Enables Claude Code to operate DWSIM process simulations programmatically via
the Python automation library in `src/`. Use this skill when you need to:

- Run thermodynamic flash calculations
- Build and solve chemical process flowsheets
- Analyze compound properties from the DWSIM database
- Debug convergence issues in existing simulations
- Generate phase diagrams and simulation reports
- Select the correct property package for a given system

## When to Activate

TRIGGER this skill automatically when the user mentions:

- "flash calculation", "PT flash", "PH flash", "bubble point", "dew point"
- "property package", "Peng-Robinson", "NRTL", "steam tables"
- "flowsheet", "unit operation", "distillation", "reactor"
- "DWSIM", "process simulation", "thermodynamic calculation"
- "vapor fraction", "phase equilibrium", "VLE", "LLE"

## Skill Execution Steps

### Step 1 — Understand the System

Ask or infer:
- What chemical species are present?
- What temperature and pressure ranges?
- Are there polar compounds, water, electrolytes, or polymers?
- Is this a new simulation or debugging an existing one?

### Step 2 — Select Property Package

Apply the selection table in `references/dwsim-expert-agent.md` (imported from the
upstream `dwsim-expert` agent). When uncertain, default to Peng-Robinson and note that
it may need adjustment.

### Step 3 — Write Python Code

Use the library from `src/`:

```python
from src.core.automation import DWSIMAutomation
from src.core.flowsheet import FlowsheetManager
from src.thermo.flash_calculations import FlashCalculator
from src.thermo.property_packages import PropertyPackageManager
from src.thermo.compound_properties import CompoundDatabase
```

### Step 4 — Validate Results

Before presenting results, verify:
- [ ] Mass balance closes (sum of outlet flows = inlet flows)
- [ ] Mole fractions sum to 1.0 per phase
- [ ] Temperature and pressure are physically reasonable
- [ ] Phase behavior is consistent with expected VLE

### Step 5 — Present Results

Format outputs with:
- Values with units explicitly stated (K, bar, mol/s, kJ/kg)
- Phase split clearly labeled (vapor / liquid / solid)
- Key derived quantities (bubble point, dew point, enthalpy)
- Suggestion for next steps

---

## Quick Reference Templates

### Minimal Flash Script

```python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.automation import DWSIMAutomation
from src.core.flowsheet import FlowsheetManager
from src.thermo.property_packages import PropertyPackageManager
from src.thermo.flash_calculations import FlashCalculator

compounds = ["Methane", "Ethane", "Propane"]
composition = {"Methane": 0.85, "Ethane": 0.10, "Propane": 0.05}
T_K = 250.0     # -23.15 C
P_Pa = 5e6      # 50 bar

dwsim = DWSIMAutomation()
dwsim.initialize()
fs = dwsim.create_flowsheet()
manager = FlowsheetManager(fs, dwsim)
manager.add_compounds(compounds)
manager.set_property_package("Peng-Robinson")

stream = manager.add_object("material_stream", "Feed", 100, 100)
stream.set_conditions(
    temperature_K=T_K,
    pressure_Pa=P_Pa,
    molar_flow_mol_s=1.0,
    composition=composition
)
dwsim.calculate(fs)

calc = FlashCalculator(fs)
result = calc.pt_flash(stream.dwsim_object, T_K, P_Pa)
print(f"Vapor fraction:    {result.vapor_fraction:.4f}")
print(f"Liquid phase:      {result.liquid_composition}")
print(f"Vapor phase:       {result.vapor_composition}")
```

### Find Compounds by Name

```python
from src.core.automation import DWSIMAutomation
from src.thermo.compound_properties import CompoundDatabase

dwsim = DWSIMAutomation()
dwsim.initialize()
db = CompoundDatabase()

matches = db.search("propyl")
for name in matches[:10]:
    print(name)
```

### Recommend Property Package

```python
from src.thermo.property_packages import PropertyPackageManager

manager = PropertyPackageManager()
recommended = manager.recommend_for_system(
    compounds=["Water", "Ethanol"],
    has_polar=True,
    has_water=True
)
print(f"Recommended: {recommended[0]}")
print(f"Alternatives: {recommended[1:]}")
```

---

## Error Handling Patterns

```python
import logging
logger = logging.getLogger(__name__)

try:
    result = dwsim.calculate(fs)
    if not result["success"]:
        logger.warning("Simulation did not converge: %s", result["errors"])
        # Suggest adjustments
except Exception as exc:
    logger.error("Calculation failed: %s", exc)
    raise RuntimeError(f"DWSIM calculation error: {exc}") from exc
```

---

## Environment Setup Check

Before running any simulation, verify:

```python
import os

import json

dwsim_path = os.environ.get("DWSIM_PATH")
if not dwsim_path:
    # Fall back to config.json
    try:
        with open("config.json") as f:
            dwsim_path = json.load(f).get("dwsim", {}).get("install_path", "")
    except FileNotFoundError:
        dwsim_path = ""

if not dwsim_path:
    raise EnvironmentError(
        "DWSIM_PATH not set. "
        "Set the DWSIM_PATH environment variable or update config.json "
        "with the path to your DWSIM installation."
    )
```

## Notes for Claude Code

- The `dwsim-expert` agent handles the *thinking* part (analysis, selection, strategy)
- This skill handles the *doing* part (code templates, validation steps, error patterns)
- Always import from `src/` using relative paths
- Never hardcode compound compositions from real projects as examples
- Use descriptive variable names matching chemical engineering conventions
  (T_K, P_Pa, x_mol_frac, V_m3, H_kJ_kg)
