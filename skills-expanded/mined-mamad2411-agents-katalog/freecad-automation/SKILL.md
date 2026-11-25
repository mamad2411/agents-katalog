---
name: freecad-automation
description: |
  FreeCAD CAD 自动化技能，通过 Python 脚本直接驱动 FreeCAD 进行参数化建模。
  覆盖完整工程工作流：零件建模（Part Design + Sketcher）、装配体、工程图（TechDraw）、文件导出。
  跨平台（Windows / macOS / Linux），无需 GUI 亦可脚本批量运行。
  兼容 FreeCAD 0.21 及 1.0+。
  触发场景：用户提到 FreeCAD、开源 CAD、参数化建模、零件设计、草图、3D 建模脚本、
  STEP/STL/IGES 导出、FreeCAD 宏、FEM 仿真、钣金、工程图等相关需求时使用。
  触发关键词：FreeCAD、开源CAD、Part Design、Sketcher、TechDraw、FCStd、FreeCAD宏、
  FreeCAD Python、FreeCAD脚本、导出STEP、导出STL、免费CAD。
---

# FreeCAD 自动化技能

## 快速开始

### 环境要求

- FreeCAD 0.21+ 已安装（[freecad.org](https://www.freecad.org/downloads.php)）
- 运行方式三选一：
  - **GUI 宏**：FreeCAD → 工具 → 宏 → 创建/编辑
  - **无头脚本**：`freecadcmd myscript.py`（macOS/Linux）或 `FreeCADCmd.exe myscript.py`（Windows）
  - **嵌入 Python**：将 FreeCAD lib 路径加入 `sys.path` 后 `import FreeCAD`

### 连接 / 初始化

```python
import sys; sys.path.insert(0, r"SKILL_DIR/scripts")
from fc_connect import new_document, open_document, save_document, mm, deg

doc = new_document("MyPart")  # 创建新文档
# 或
doc = open_document("/path/to/file.FCStd")
```

> 将 `SKILL_DIR` 替换为本技能的实际安装路径。

## 核心工作流

根据用户需求选择对应模块：

| 需求 | 脚本 | 参考文档 |
|---|---|---|
| 文档管理 | `scripts/fc_connect.py` | — |
| 草图 + 特征建模（Part Design）| `scripts/fc_part.py` | `references/part-modeling.md` |
| 轻量几何操作（Part 工作台）| `scripts/fc_part.py` → `part_*` 系列函数 | `references/part-modeling.md` |
| 装配体 | `scripts/fc_assembly.py` | `references/assembly.md` |
| 工程图（TechDraw）| `scripts/fc_drawing.py` | `references/drawing.md` |
| 文件导出 | `scripts/fc_export.py` | `references/export.md` |
| 钣金 / FEM / 曲面 | — | `references/advanced.md` |
| 常见错误排查 | — | `references/troubleshooting.md` |

## 使用流程

1. 创建或打开文档（`fc_connect.py`）
2. 建模：Part Design 路线（Body → Sketch → Pad/Pocket/…）或 Part 路线（几何体 + 布尔运算）
3. 导出文件（`fc_export.py`）
4. 保存 `.FCStd`（`save_document(doc, path)`）

## 关键注意事项

- **单位**：FreeCAD API 内部使用**毫米（mm）**。`mm(5)` 仅为可读性封装，直接填数字即可
- **recompute**：每次修改属性后需调用 `doc.recompute()` 才会更新模型
- **Part Design vs Part**：复杂参数化零件用 Part Design（Body+Feature 树）；简单几何体或布尔运算用 Part 工作台直接操作 Shape
- **无头模式**：GUI 不可用时，所有 `FreeCADGui` 调用需跳过；导出仍可正常工作
- **基准面名称**：`XY_Plane`（= Top/XY）、`XZ_Plane`（= Front/XZ）、`YZ_Plane`（= Right/YZ）
