---
name: cst-modeling-guide
description: CST Studio Suite 2025 天线仿真建模规范指南。使用本skill获取CST正确的建模流程、求解器选择、网格设置、边界条件、端口配置、场监视器设置和后处理规范。当用户提到CST建模、仿真设置、网格设置、求解器选择、边界条件、天线仿真、S参数、远场、或者需要检查CST模型是否正确时使用。
---

# CST 天线仿真正规建模指南

基于 CST 2025 官方 demo 宏、文档和行业最佳实践提炼的建模规范。覆盖天线仿真全流程。

## 环境

- **CST 2025**：`<CST安装目录>`
- **CST Python**：`<CST安装目录>\AMD64\python\Scripts\python.exe`
- **API 包**：`<CST安装目录>\AMD64\python_cst_libraries\cst\`
- **官方 Demo 宏**：`<CST安装目录>\Library\Macros\Construct\Demo Examples\`

## 求解器选择决策树

天线仿真第一步是选对求解器。选错求解器会导致结果不收敛或精度不足。

### T-Solver（时域求解器）— 宽带天线首选

**适用场景**：
- 宽带/超宽带天线（跨多个倍频程）
- 5G MIMO 天线（如 3-6 GHz）：一次运行获得全频段 S 参数
- 阵列天线需全频段 S 参数矩阵
- 信号完整性 / TDR 分析（需要瞬态响应）
- 电大尺寸结构的参数扫描阶段

**基本原理**：有限积分法（FIT）/ TLM，六面体网格，时域步进 + FFT，一次计算覆盖宽带。

**关键参数**：
```
SteadyStateLimit: 默认 -30 dB → 天线远场建议 -40 至 -50 dB
NumberOfPulseWidths: 默认 20 → 高 Q 结构酌情增加到 50-100
AdaptivePortMeshing: False（天线仿真通常关闭）
StimulationType: Gaussian
MeshType: Hexahedral (PBA)
```

**注意**：高 Q 值窄带天线（如介质谐振器天线）用 T-Solver 信号衰减极慢，改选 F-Solver。

### F-Solver（频域求解器）— 窄带/高精度首选

**适用场景**：
- 窄带谐振天线（微带贴片、PIFA 等）
- 高 Q 值结构（滤波器、谐振腔）
- 曲面共形天线（四面体网格拟合能力强）
- 需要精确近场分布（SAR 分析）
- 毫米波阵列（频段窄，FEM 精度优势显著）

**基本原理**：有限元法（FEM），四面体网格，逐频点独立求解。

**关键参数**：
```
Method: Tetrahedral, General purpose
Adaptive mesh refinement: 必须开启
  - MaxPasses: 10-15
  - ConvergenceDeltaS: 0.02（S 参数变化 <2% 时停止自适应）
  - SetAdaptionStrategy: ExpertSystem
  - SetLinearGrowthLimitation: 40（防止网格膨胀失控）
AutomaticReSweep: True（自适应后自动重扫）
```

**⚠️ 关键警告**：F-Solver 默认不计算远场！必须在 Solver → Advanced Settings 中显式勾选 "Calculate Farfields"，否则跑完后远场图为空。

**⚠️ 宽带插值陷阱**（2026-08-16 借鉴外部 cst-simulation skill）：F-Solver 宽带扫描默认用有理函数拟合整条 S 参数曲线，**尖锐窄凹陷可能是拟合伪影而非真实谐振**。疑似窄谐振/深凹陷处必须强制直接采样频点（`.AddSampleInterval`）复核；最终权威曲线要区分"插值曲线"与"直接求解点"并记录实际采样间距。另：**不要为得到好看的曲线去缩窄求解频段**——求解频段必须覆盖评估频段并留余量，汇报时分开记录 `solver_band` 与 `evaluation_band`。

### 双求解器交叉验证 — 论文级验证铁律

对重要结果（如发表论文数据），同一模型分别用 T-Solver 和 F-Solver 计算，S11 和增益一致才确认可信。不一致 → 加密网格至两者吻合。

**交叉验证细则**（2026-08-16 借鉴外部 cst-simulation skill）：
- **先校准后信任**：TD/FD 先在简单校准结构（均匀波导、馈电过渡段）上对齐，再信复杂装配体的结果。
- **TD 门槛**：求解 success + 稳态收敛判据满足 + 模态/总功率闭合可接受。**非收敛曲线只能用于诊断，不得参与变体排名。**
- **TD/FD 大分歧先查端口**：端口口径过窄（没盖住真实横截面）会人为制造 TD/FD 假分歧——先扩口径再怀疑物理。
- 关键结论遇严重警告/近截止行为/尖锐谐振时，做网格敏感性复查后再定稿。

### 选择口诀

> **宽带用时域，窄带用频域。交叉验证是铁律。**

---

## 标准建模流程（13 步）

基于 CST 官方 demo 宏提炼，每一步顺序有讲究：

| 步骤 | 操作 | VBA 对象 | 要点 |
|------|------|---------|------|
| 1 | 设置单位 | `Units` | Geometry=mm, Frequency=GHz, Time=ns |
| 2 | 定义材料 | `Material` | εr, μ, TanD, TanDFreq 必须齐全 |
| 3 | 创建 Component | `Component.New` | 组织几何、方便复制/旋转 |
| 4 | 构建几何体 | `Brick/Cylinder/Extrude/Curve` | 用变量名驱动的参数化尺寸 |
| 5 | 布尔运算 | `Solid.Add/Subtract/Insert` | 合体/减体/插体 |
| 6 | 设置端口 | `Port/DiscretePort/DiscreteFacePort` | 见端口选择指南 |
| 7 | 设置背景材料 | `Background` | 天线辐射 → Type=Normal（真空），**绝不 PEC** |
| 8 | 设置边界条件 | `Boundary` | 天线辐射 → 6 面全 `expanded open` |
| 9 | 设置频率范围 | `Solver.FrequencyRange` | 覆盖所需全频段 |
| 10 | 设置网格 | `Mesh/MeshSettings` | 见网格设置指南 |
| 11 | 设置场监视器 | `Monitor` | **★ 标准套件：远场+Efield+Hfield(含表面电流)@中心频点+带边**，必须在求解前定义（求解后不可补） |
| 12 | 设置求解器参数 | `Solver/FDSolver` | 收敛标准、自适应等 |
| 13 | 激活后处理 | `PostProcess1D/FarfieldPlot` | VSWR, YZ 矩阵, 远场切面 |

---

## 网格设置规范

### 六面体网格（T-Solver）

```
LinesPerWavelength (LPW):
  10   — 最低可接受值，快速初扫
  15-20 — 可靠工程精度
  25-35 — 论文发表级精度（微带贴片天线推荐 ≥25）

LowerMeshLimit (LML):
  10   — 默认值，电大尺寸合适
  20-50 — 电小天线需要精调

RatioLimit:
  10-20 — 控制最大/最小网格步长比，过大导致不稳定
```

**收敛性检验**：逐次提高 LPW（10→15→20→25），S11 最低点变化 <0.1 dB 即为收敛。

**网格量估算**：`网格数 ∝ (LPW)³`，LPW 从 10→20 格数增加约 8 倍，仿真时间也大幅增加。先粗后细。

### 四面体网格（F-Solver）

- 不直接设 LPW，依靠**自适应网格精炼**（Adaptive Mesh Refinement）
- 初始 `StepsPerWavelength ≥ 8`（当前项目用 4 太粗）
- 自适应设置：MaxPasses=15, DeltaS=0.02, ExpertSystem 策略

### 局部网格加密

天线辐射体周边画空气盒子设局部加密：
```vba
' 对特定 shape 设置自动网格参数
Solid.SetAutomeshParameters "component:solid", "1", "True"
Solid.SetAutomeshStepwidth "component:solid", "0.5", "0.5", "0.5"
```

---

## 端口选择指南

详细内容见 `references/port-guide.md`。核心决策：

| 场景 | 推荐端口 | 原因 |
|------|---------|------|
| 微带线/带状线边缘馈电 | **Waveguide Port** | 计算实际模式阻抗，S 参数最准 |
| 同轴探针馈电 | Discrete Port | 探针馈电结构 |
| 偶极子间隙馈电 | Discrete Port | 间隙源，传统做法 |
| 缝隙耦合馈电（如你的耦合贴片） | **Discrete Port** | 电流源模型更合适 |
| 任意角度馈电（非坐标轴对齐） | Discrete Port | Waveguide Port 必须轴对齐 |
| 精确 S11（发表对比用） | **Waveguide Port**（如可能） | S 参数精度最高 |

**阻抗**：默认 50 Ω。Discrete Port 可用户指定；Waveguide Port 自动计算模式阻抗。

**阻抗重归一化**：F-Solver 需要手动设置参考阻抗：
```vba
With FDSolver
    .Reset
    .SetMethod "Tetrahedral", "General purpose"
    ' ...自适应设置...
End With
' VBA 宏中可用：Solver → Reference Impedance Settings
```

### 端口纪律细则（2026-08-16 借鉴外部 cst-simulation skill）

- **从物理横截面定义端口**，不是从图面上看着差不多的一块面。波导端口盖住整个传播口径；微带波导端口必须包含**地 + 基板 + 带线 + 带线上方足够空气**，只有基材的口径无效。
- **不假设带线宽度就是 50 Ω**：读 CST 端口参考阻抗的实际计算值，而不是想当然。
- **过渡结构先独立校准**：微带-SIW、SIW-过模波导等过渡，先单独建模校准 S 参数，再接入整机。
- **多模端口验明模式身份**：TE/TM 标签必须三方核对（截止频率 + 端面场图 + CST mode order）才可标注；不确定时按 CST 端口/模式索引（如 S1,1 mode2）标注并声明映射 pending。
- **"additional propagating mode not considered" 警告 = 诊断旗标**：说明有未考虑的传播模式。先加诊断模式数或跑校准模型，再判断主 S 参数是否仍有效，不要直接忽略。
- **阵列快速评估不建馈网**（2026-08-15 实测）：全阵每个单元给独立端口 + 均匀幅相激励（如 8×8 开缝贴片阵用 64 个独立 SIW 端口），跳过馈电网络建模——适合扫结构参数看方向图/栅瓣/口径趋势（LPW 可先降到 10 提速）；要看匹配/馈网损耗需另建完整馈网模型。

---

## 边界条件设置

### 天线辐射问题标准设置

```
6 面全设为 "expanded open"（PML 吸收边界）
背景材料 Type = "Normal"（εr=1, μr=1）
```

**为什么**：
- `expanded open` 自动在模型外围扩展 λ/8 自由空间，PML 在此距离工作最佳
- 背景设为 PEC 会反射所有辐射波 → 远场完全错误
- 普通 `open`（不加 expanded）紧贴模型表面，需要手动在 Background 中设 Surrounding Space

### 特殊情况

| 场景 | 设置 |
|------|------|
| 对称天线（利用对称面） | 设 Magnetic/ Electric Symmetry Plane，计算量减半/四分之一 |
| 周期结构/阵列 | 用 Periodic 或 Unit Cell 边界 |
| 天线+金属反射板 | 辐射方向 `expanded open`，金属方向直接建模在计算域内 |

### 对称面判断

- **Electric (Et=0)**：电场垂直于对称面的结构 → 对应 XY/YZ/XZ 对称
- **Magnetic (Ht=0)**：磁场垂直于对称面的结构

```vba
' 偶极子天线示例：Y 向磁对称 + Z 向电对称
With Boundary
    .Xsymmetry "none"
    .Ysymmetry "magnetic"
    .Zsymmetry "electric"
End With
```

---

## 远场/场监视器设置

### ★ 场监视器是硬约定（仿真必须保留 2D/3D 场分析图）

> **目的**：可视化呈现整个电磁波工作状态（场分布/表面电流/功率流向），不只交 S 参数曲线。
> 执行层实现见 cst-em-sim「★ 场监视器与 2D/3D 场图硬约定」（`add_standard_monitors` 一键套件 +
> `export_field_ascii` 点云导出）；本节管"设什么、设几个频点"。

### 必须跑前定义

场监视器必须在求解前定义，跑完后不可追加——**忘加 = 该批无场图，只能重跑**，所以套件必须进建模脚本而不是事后补。

### 标准监视器套件（缺省配置，天线/微波器件通用）

| 监视器 | FieldType | 出什么图 | 备注 |
|--------|-----------|---------|------|
| 远场 | `Farfield` | 3D 方向图 + E/H 面切面 | 原有要求：中心频率 + 带边 |
| E 场（Volume） | `Efield` | 2D 主平面切面 \|E\| 图、3D 分布/热点图、场强直方图 | 击穿风险/热点分析原料 |
| H 场（Volume） | `Hfield` | 2D 切面 \|H\| 图 + **金属表面电流分布** | ⚠️ CST 的 Hfield 结果**同时含磁场与表面电流**（切向 H 导出），没有单独的 SurfaceCurrent 类型 |
| 坡印廷（可选） | `Powerflow` | 功率流向/能量流动 | HPM 馈电链路、功分/合成结构推荐加 |

### 频点选择策略（每频点每类型存一整份场数据，≤3 个为宜）

- **中心/工作频点**（必选）——工作状态主图
- **带边或谐振点**（选 1-2 个）——S11 最深点、频带边沿的场分布对比
- 扫参批次：监视器频点全批一致（对比才有意义），只对**最佳变体**补额外频点

### 监视器 VBA 模板

```vba
' 1. 远场监视器 — 至少覆盖中心频率 + 带边
With Monitor
    .Reset
    .Name "farfield (f=4.15)"
    .FieldType "Farfield"
    .Frequency "4.15"
    .Create
End With

' 2. E-field 体监视器（中心频率）——2D 切面/3D 分布图原料
With Monitor
    .Reset
    .Name "e-field (f=4.15)"
    .Dimension "Volume"
    .Domain "Frequency"
    .FieldType "Efield"
    .Frequency "4.15"
    .Create
End With

' 3. H-field 体监视器（中心频率）——磁场 + 表面电流
With Monitor
    .Reset
    .Name "h-field (f=4.15)"
    .Dimension "Volume"
    .Domain "Frequency"
    .FieldType "Hfield"
    .Frequency "4.15"
    .Create
End With

' 4. 功率流监视器（可选，HPM/馈电链路推荐）
With Monitor
    .Reset
    .Name "powerflow (f=4.15)"
    .Dimension "Volume"
    .Domain "Frequency"
    .FieldType "Powerflow"
    .Frequency "4.15"
    .Create
End With
```

> FieldType 合法枚举（官方文档 `VBA_3D/special_vbamonitors_monitor_object.htm`）：
> `Efield / Hfield（含表面电流）/ Powerflow / Current / Powerloss / Eenergy / Farfield`。

### ★ 场图交付清单（每批仿真验收时在场）

| # | 交付物 | 内容 | 落盘位置 |
|---|--------|------|---------|
| 1 | 2D 主平面切面场图 | 工作频点 \|E\|（和/或 \|H\|）沿传播轴/口径面的切面分布 + 沿传播方向 max\|E\| 剖面 | `04_figs/` |
| 2 | 3D/热点层分布图 | 全域 max\|E\| 所在层的俯视热图（标出峰值位置），或 3D 体渲染 | `04_figs/` |
| 3 | 表面电流图 | 金属表面电流分布（源自 Hfield 监视器） | `04_figs/` |
| 4 | 场点云数据 | ASCII 点云 txt（9 列 x y z 复数分量）留档，图可重生成 | `03_data/` |
| 5 | （HPM 类）功率流图 | 坡印廷矢量分布/热点 | `04_figs/` |

- 出图：pandas 读点云 → matplotlib 切片剖面/热点热图/直方图三件套
- 场图英文标签（matplotlib 无中文字体坑同 cst-result-report），中文解释写汇报 md
- 图最终进 cst-result-report 图文汇报的「场分布」章（内嵌，不裸给路径）

### F-Solver 特别注意

F-Solver 默认不计算远场！必须额外设置：
1. Solver → Advanced Settings → 勾选 "Calculate Farfields"
2. 或在 VBA 中：`FDSolver.CalculateFarfields "True"`

---

## 后处理规范

仿真完成后自动激活以下后处理：

```vba
' VSWR — 检验阻抗匹配
With PostProcess1D
    .ActivateOperation "vswr", "True"
End With

' YZ 矩阵 — 导出等效电路参数
With PostProcess1D
    .ActivateOperation "yz-matrices", "True"
End With

' 远场切面 — 用于方向图分析
With FarfieldPlot
    .ClearCuts
    .AddCut "lateral", "0", "1"    ' phi=0° (E-plane)
    .AddCut "lateral", "45", "1"   ' phi=45°
    .AddCut "lateral", "90", "1"   ' phi=90° (H-plane)
    .AddCut "polar", "45", "1"     ' theta=45°
    .AddCut "polar", "90", "1"     ' theta=90°
End With
```

获取增益/方向图/效率：用 **Template Based Postprocessing**（Results → Template Based Postprocessing → Farfield and Antenna Properties）。

---

## 运行前验证检查清单

在点 "Start Simulation" 之前，逐项确认：

- [ ] 单位：Geometry=mm, Frequency=GHz, Time=ns
- [ ] 背景材料：Type=Normal（真空），**不是 PEC**
- [ ] 6 面边界：全部 `expanded open`（天线辐射问题）
- [ ] 材料参数：εr, μr, TanD, TanDFreq 均已正确设置
- [ ] 端口阻抗：已确认（默认 50 Ω 或手动设置）
- [ ] 频率范围：覆盖所需分析的全频段
- [ ] 网格：LPW ≥ 10（Hex），或自适应已开启（Tet）
- [ ] 远场监视器：至少在中心频率设有 Farfield Monitor
- [ ] **★ 场监视器套件：Efield + Hfield 体监视器已加（出 2D/3D 场分析图用；求解后不可补）**
- [ ] **★ 场图导出已排进收尾流程：list_3d_results 枚举真名 → ASCIIExport 带 .Step 出点云 → 重绘图**
- [ ] F-Solver：已勾选 "Calculate Farfields"（如果使用频域）
- [ ] VSWR/YZ 后处理：已激活
- [ ] PEC 不接触 open 边界：金属结构应被空气包围

---

## 常见错误及修复

| 错误现象 | 原因 | 修复 |
|---------|------|------|
| 远场图为空 | F-Solver 未开 "Calculate Farfields" | 开启后重跑 |
| 远场图为空 | 跑前没设 Farfield Monitor | 设置后重跑 |
| S11 全为 0 dB | 背景材料设为 PEC | 改为 Normal |
| 谐振频率偏移 >5% | 网格太粗（LPW<10） | 加密至 LPW≥15 |
| "Farfield is inaccurate" 警告 | 边界离辐射体太近 | 用 `expanded open` 替代 `open` |
| 仿真超长时间不收敛 | 高 Q 结构用错求解器 | 换 F-Solver |
| 时域求解器 unstable abort | 网格线比（RatioLimit）太大 | 降至 10-15 |
| S11 与测量差异大 | 端口类型不对 | 微带馈电换 Waveguide Port |
| TD 与 FD 结果分歧大 | 端口口径过窄，未盖住真实横截面 | 扩大端口至完整物理截面 |
| 窄深凹陷疑似假谐振 | F-Solver 宽带插值伪影 | 凹陷附近 `.AddSampleInterval` 强制直接采样 |
| TE/TM 模式标签对不上 | mode identity 未验证 | 用截止频率 + 场图 + mode order 三方核对 |
| 场点云导出只有表头 2 行 | ASCIIExport 缺 `.Step`（采样步宽） | 补 `.Step ("1.0")`（mm）重导（cst-em-sim 坑 17） |
| 3D 场结果树路径 Select 失败 | 叶子名带 `[N]` 运行号后缀被硬拼 | 先 ResultTree 遍历枚举真名再导出 |
| 想看表面电流但没有该监视器类型 | Hfield 结果已含表面电流 | 加 Hfield 监视器即可，无单独 SurfaceCurrent 类型 |

---

## 参考资源

- `references/mesh-guide.md` — 详细的网格收敛性研究方法和经验数据
- `references/port-guide.md` — 端口选择决策树和详细配置
- `references/boundary-guide.md` — 边界条件选择矩阵
- `references/solver-params.md` — 求解器全部参数速查表
- 官方 Demo 宏：`<CST安装目录>\Library\Macros\`
- PDF 手册：`<CST安装目录>\Documentation\`
- 视频教程：`<CST安装目录>\Videos\`
