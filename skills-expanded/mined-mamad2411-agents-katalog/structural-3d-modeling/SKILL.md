---
name: structural-3d-modeling
description: "三维构造建模 (Structural Geology & Petrology). 创建GemPy地质模型（GeoModel）对象，定义三维建模空间的地理范围（extent）和体素分辨率（resolution）。extent以[xmin, xm. Use when user asks about 构造地质学与岩石学 tasks such as: 用GemPy根据地质图和产状数据构建三维地质模型; 这个区域有复杂褶皱，帮我用LoopStructural建模; 在三维模型上切几条剖面，和地震剖面做对比. Core tools: geovista_bridge_from_netcdf, meshio_read_mesh."
---

# 三维构造建模

Category: **构造地质学与岩石学** / Structural Geology & Petrology | Match: **EXACT** | Skill ID: `05-08`

## When to Use

Use this skill when you need to:

- geological mapping / 地质填图
- structural analysis / 构造分析
- cross-section construction / 剖面制作
- stratigraphic interpretation / 地层解释

Do not use this skill for:
- General programming tasks unrelated to geological
- Setting up development environments or installing packages
- 与地质填图无关的一般编程任务
## Tool Invocation
All tools are invoked via the geo-runner HTTP API (`_invoke_tool_http`).
See `scripts/call_tool.py` for the reusable client wrapper.

### Primary: `geovista_bridge_from_netcdf`

创建GemPy地质模型（GeoModel）对象，定义三维建模空间的地理范围（extent）和体素分辨率（resolution）。GeoModel是GemPy所有建模操作的核心容器对象。

```python
function_name = "geovista_bridge_from_netcdf"
arguments = { "project_name": "default_project", "extent": 1.0, "resolution": 1, "importer_helper": "/shared/geo-runtime-work/tools_input_data/geovista_bridge_from_netcdf/importer_helper.csv" }
_invoke_tool_http(function_name, arguments)
```

### Helper: `meshio_read_mesh`

执行GemPy三维地质模型的核心计算，基于输入的控制点和产状数据，通过通用协克里金隐式插值方法，计算三维空间中每个体素的地质属性值和岩性编号。

```python
function_name = "meshio_read_mesh"
arguments = { "gempy_model": null, "engine_config": null, "compute_meshes": "true" }
_invoke_tool_http(function_name, arguments)
```

## Instructions

### Step 1: 创建模型空间

用GemPy创建模型对象，定义extent和resolution `[Tool-supported]`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_name` | str | No | 地质模型项目名称 |
| `importer_helper` | gempy.ImporterHelper | No | 数据导入辅助对象，指定控制点和产状数据CSV路径 |

### Step 2: 层序定义与数据导入

定义地层的叠加顺序（如：Q>C>P>C2>O>∈），导入控制点和产状数据 `[Code-required]` — 需整理地质界线和产状数据

### Step 3: 断层建模

定义断层面和位移量 `[Code-required]` — 需在GemPy中添加断层约束

### Step 4: 褶皱建模

用LoopStructural的褶皱框架方法建模褶皱轴面和翼间角 `[Code-required]` — 需配置褶皱参数

### Step 5: 插值计算

运行隐式建模引擎，生成三维地质体 `[Tool-supported]`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `gempy_model` | gempy.core.data.GeoModel | Yes | 已配置好的GemPy地质模型对象 |
| `engine_config` | GemPyEngineConfig | No | 计算引擎配置（Aesara/PyTorch，CPU/GPU） |
| `compute_meshes` | bool | No | 是否同时计算三角网格用于可视化 |

- 注意：若断层关系、层序或产状约束冲突较大，应保留多种候选模型并说明不确定性

### Step 6: 可视化与剖面

用PyVista交互展示三维模型，可切剖面 `[Code-required]` — 需用PyVista实现交互可视化

输出以下文件：
- `3d_geological_model.vtk`：三维地质模型文件
- `cross_sections.png`：典型剖面图
- 模型参数摘要

## Troubleshooting

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| GemPy创建模型时报extent错误 | extent参数格式不正确 | 确保extent为[xmin,xmax,ymin,ymax,zmin,zmax]六元组 |
| 插值计算不收敛 | 控制点和产状数据存在矛盾 | 检查产状一致性，减少冲突约束 |
| 褶皱建模结果不符合预期 | 褶皱参数（轴面/翼间角）设置不当 | 根据野外实测数据调整褶皱参数 |
| 断层面穿切地层异常 | 断层位移量设置不合理 | 检查断层offset参数，结合地震剖面约束 |
| PyVista渲染黑屏 | GPU驱动不兼容或模型数据为空 | 切换到CPU渲染，检查模型计算结果是否有效 |

## Example User Requests

- "用GemPy根据地质图和产状数据构建三维地质模型"
- "这个区域有复杂褶皱，帮我用LoopStructural建模"
- "在三维模型上切几条剖面，和地震剖面做对比"
