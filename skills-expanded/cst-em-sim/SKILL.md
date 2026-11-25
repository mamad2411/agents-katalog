---
name: cst-em-sim
description: CST Studio Suite 电磁仿真自动化 skill。用 CST 自带 Python (cst.interface) 通过 COM 驱动 CST 建模、设端口/边界/监视器、跑时域求解器、导出 S 参数、远场方向图与 2D/3D 场分析数据。触发词：CST 仿真、电磁仿真、微波天线仿真、相控阵 phased array、S 参数、远场方向图 farfield、场监视器、场分布、E 场 H 场、表面电流、波导端口、时域求解器、复现天线论文、.cst 工程、建 brick、磁电偶极子 ME dipole。当用户要做天线/微波器件的全波仿真、批量扫角/扫频、参数化建模、或复现 IEEE 天线论文时使用。
---

# CST EM Simulation Skill

## Scope

本 skill 用于在 **CST Studio Suite 2025**（本机装在 `<CST安装目录>\`）上做电磁全波仿真自动化，覆盖：

- 参数化几何建模（brick / cylinder / 拉伸 / 布尔运算）
- 材料、边界、背景、频率范围设置
- 波导端口 / 离散端口激励
- **场监视器套件（★ 硬约定，见下）**：远场 + E 场 + H 场（含表面电流）+ 坡印廷
- 时域 / 频域求解器调度
- 结果导出：S 参数 (Touchstone / ASCII)、远场方向图 (CSV / 1D / .ffd)、**2D/3D 场分布 ASCII 点云**（→ matplotlib 重绘 2D 切面 / 3D 分布 / 表面电流图）
- 批量参数扫描、扫角（相控阵 beam scanning）

适用于：天线单元与阵列、滤波器、耦合器、波导器件、超表面等微波/毫米波结构。

## ★ 场监视器与 2D/3D 场图硬约定（硬约定）

**所有电磁仿真求解前必须定义标准场监视器套件，求解后导出场点云并重绘 2D/3D 场分析图**——目的是可视化呈现整个电磁波工作状态（场分布 / 表面电流 / 功率流向），不只交 S 参数曲线。

1. **求解前**：`r.add_standard_monitors([中心频点, 带边/谐振点])`（缺省 farfield+efield+hfield；HPM/馈电链路类加 `"powerflow"` 看功率流向）。监视器**求解后不可追加**——忘加 = 该批无场图只能重跑，所以套件必须在跑前进脚本。
2. **求解后**：`r.list_3d_results()` 拿 3D 结果树真名（叶子带 `[N]` 运行号后缀）→ `r.export_field_ascii(tree, out, step_mm)` 导点云。⚠️ `step_mm` 必填，缺失 = 零数据（坑 17）。
3. **重绘图**：点云 → matplotlib 出图（切片 max|E| 沿传播轴剖面 / 热点层俯视热图 / 场强直方图，matplotlib 三件套：切片 max|E| 剖面 / 热点层俯视热图 / 场强直方图，写法可参考 cst-result-report 作图模板），PNG 落项目 figs/、点云 txt 落 data/，最终进 cst-result-report 图文汇报（场图内嵌章）。
4. 监视器频点 ≤3 个为宜（每频点每 kind 存一整份场数据，多了工程膨胀）；大模型点云步宽先用 1.0mm 档，热点区再单独细扫 0.25mm。

## 关键技术决策（本机实测，勿改）

这些结论是在本机实测得出的，违反会直接报错：

| 项 | 值 | 说明 |
|---|---|---|
| **Python 解释器** | `<CST安装目录>\AMD64\python\Scripts\python.exe`（3.9.15）| **必须用 CST 自带 Python**。系统 Python 3.13+ 不被 `cst.interface` 支持（仅 3.8–3.12）。从 Git Bash 调用：`"$CST_PY" script.py` |
| **接口库** | `cst.interface`（DesignEnvironment / Project / model3d 对象模型）| 不要用纯 win32com 后绑定——CST 没有公开类型库(.tlb)，方法名全靠猜 |
| **建几何入口** | `m.add_to_history(header, vba_code)` 然后 `m.full_history_rebuild()` | model3d 的 Solid/Port/Boundary 对象**只有 Get 查询方法，没有 Create**。创建一律走 history VBA 命令字符串 |
| **几何名前缀** | `component1:name` | `Solid.DoesExist('name')` 返回 False，要 `DoesExist('component1:name')`。`GetNameOfShapeFromIndex(i)` 返回带前缀的全名 |
| **默认单位** | Length=mm, Frequency=GHz | 新建 MWS 工程默认就是 mm/GHz，建模坐标直接用毫米，不用换算 |

## 工作流

0. **开工查占用**：确认当前没有别的 CST/DE 进程在求解（`Get-Process | Where-Object { $_.Name -like 'CST*' }`）——单实例独占是铁律，多 DE 并存是坑 6 与坑 12 的根源（判归属/排队/问用户的完整判据见 cst-automation「★ CST 开工纪律」）。
1. **连接 / 新建工程**：`DesignEnvironment.new()` → `de.new_mws()` 拿到空 HF 工程；或 `connect_to_any_or_new()` 复用已运行实例。
2. **参数化**：用 `m.StoreParameter('name', '5.0')` 把关键尺寸设成参数，便于扫角/扫频/优化。
3. **建模**：每个几何体写一段 `With Brick ... End With` 的 VBA 字符串，调 `add_to_history` 追加，最后 `full_history_rebuild()` 一次性重建。布尔运算（加/减/交）同样用 history 命令（`Solid.Add` / `Solid.Subtract`）。
4. **物理设置**：背景材料、边界（`Boundary` VBA）、频率范围（`Solver.Frequency` VBA）、**场监视器套件（★ 硬约定：`add_standard_monitors`，必须在求解前——见上方专节）**。
5. **端口**：波导端口用 `With Port ... End With` 选面 + 设模式数。
6. **求解**：`Solver` VBA 启动时域求解器；`start_solver()` / `run_solver()` 等待完成。
7. **取结果**：⚠️ `proj.result1d` 属性实测**不存在**、`cst.results.ProjectFile` 只能读 3D 结果无 1D（2026-08-15 实测）——1D 数据可靠取法只有 ASCIIExport 导出后读文件，导出坑见下方坑 9。远场用 `FarfieldPlot` 或导出 1D 方向图。
8. **导出**：`StoreCurvesInASCIIFile` 导出 S 参数/方向图为 CSV；`TOUCHSTONE` 导出 .sNp；**场点云**（★ 硬约定）`list_3d_results()` 拿真名 → `export_field_ascii(tree, out, step_mm)`（坑 17），重绘 2D/3D 场图（见上方场图专节）。
9. **存盘**：`m.SaveAs(path)` 存成 `.cst` 工程。
10. **★ 关闭 CST 窗口（硬约定，2026-08-12）**：任务完毕必须关闭 CST 界面。`de.close()` 只断 COM 不关进程，必须用 PowerShell 杀 CST*：
    ```python
    import subprocess
    subprocess.run(["powershell", "-Command",
        "Get-Process | Where-Object { $_.Name -like 'CST*' } | Stop-Process -Force"],
        capture_output=True, timeout=20)
    ```
    或调用项目 `cst_config.cleanup_cst()`（标准收尾函数）。**杀进程前先确认当前无用户手动 GUI 会话**（判据见 cst-automation「★ CST 开工纪律」）。
    **汇报只给产出文件路径，不叙述 CST 过程**（详见 cst-automation「★ CST 收尾纪律」）。

## 何时加载哪个参考

- 不确定 VBA 命令语法（建 brick / 波导口 / 远场监视器 / 求解器）→ 读 `references/cst-interface-guide.md`（含经实测验证的命令模板）。
- **导入外部 CAD（STEP/IGES/SAT/STL/CATIA/SolidWorks 等 .stp/.step/.igs/.sat/.stl）** → 读 `references/step-import-guide.md`。**关键: 导入必须用 `add_to_history`，绝不能用 `_execute_vba_code`**（`With STEP` 是 CST 私有简写，标准 VBA 解析器认不出）。
- 想了解 `.cst` 工程内部目录结构、哪些是源哪些是产物 → 读 `references/cst-project-layout.md`。
- 复现包内自带的天线论文案例（ME dipole AWPL 2024）→ 读 `references/paper-ant3-spec.md` + 项目目录 `D:\CST_Projects\ME_dipole_AWPL2024\`。

## 通用执行器

`scripts/cst_runner.py` 封装了上述经实测验证的模式（CSTRunner 类），提供：
- `new_project(path)` / `connect_existing()`
- `add_brick(name, p_min, p_max, material='PEC')` — 轴对齐长方体
- `add_cylinder(name, center, radius, height, axis='z')`
- `add_polygon_extrude(name, points, thickness, material)` — **任意多边形拉伸体**（Polygon3D+ExtrudeCurve；2026-08-17 经真机实测 VBA 实现并真机验证建形成功，⚠️ 曲线+拉伸必须批量追加最后一次性 rebuild，中途 rebuild 会因曲线被二次消费导致 DE 崩溃）
- `subtract(tool, target)` / `add_shapes(a, b)` — 布尔运算
- `set_background_vacuum(**sides)` / `set_boundary(...)`
- `set_frequency_range(fmin, fmax)` (内含 Method="Hexahedral")
- `add_waveguide_port(...)` / `add_farfield_monitor(name, freq)`
- `add_field_monitor(name, freq, field_type, dimension)` — E/H/Powerflow/Current/Powerloss 体场监视器（求解前必加，求解后不可补）
- `add_standard_monitors(freqs, kinds)` — ★ 一键标准监视器套件（远场+E场+H场含表面电流，可选 powerflow；场可视化硬约定的缺省实现）
- `list_3d_results()` — 枚举 2D/3D 结果树真名（叶子带 [N] 运行号后缀，导出前必查）
- `export_field_ascii(tree_item, out_file, step_mm)` — 3D 场结果→ASCII 点云（坑 17 路线；step_mm 必填否则零数据）
- `update_mesh()` / `run_time_domain_solver(accuracy_db, timeout)` (含 Unknown error 兜底)
- `export_result(tree_item, out_file)` / `get_result_1d(tree_item)`
- `save(filename, must_succeed=False)` — must_succeed=False 时存盘失败仅警告不阻塞

复现新天线时优先基于它扩展，不要从零重写连接逻辑。

## 边界与已知差异提醒

- 单天线自由空间仿真 vs 论文周期边界阵列单元：**波束宽度不等价**。论文 Fig.7/9 的方向图是阵列单元（周期边界）环境，单天线自由空间通常更宽。要严格对齐需加 unit cell / 周期边界。
- `.cst` 是私有 `DE` 容器（非 zip），不能 unzip 解包；只能由 CST 创建/打开。
- CST 2025 已废弃 `.his/.mcs/.mcr`，建模历史在 `Model/3D/ModelHistory.json`。

## CST 2025 关键坑（实测，违反会卡住）

### 1. Solver.Method 的有效值是 "Hexahedral" 不是 "Time Domain"
`With Solver` 块里 `.Method("Time Domain")` 报错。CST 2025 把求解器类型从方法名改成网格类型:
```vba
With Solver
 .Reset
 .Method ("Hexahedral")         ' ✅ 高频时域求解器
 .FrequencyRange (23.5, 26.5)
End With
```

### 2. 网格密度控制：VBA 密度命令全部静默失效，唯一旋钮是 Fmax（2026-08-28 十三轮探针实锤）
**`With Mesh` 块经 `add_to_history` 全部无效**（不报错、进历史、`Mesh.Update` 后 `GetNumberOfMeshCells` 纹丝不动）：
`.LinesPerWavelength`（With 块/裸语句/带引号/带括号全形态）、`.MinimumStepNumber`、`.MinimumLineNumber`、
`Mesh.AddAutomeshFixpoint`——逐一验证。`.MeshType "Hexahedral"` 报 10091（枚举值不存在，六面体叫 `"PBA"`）。
`get_active_solver_name()` 确认默认求解器就是 'HF Time Domain'（非求解器类型问题）。
旧结论"值必须用字符串"（源自官方宏 Combline^+MWS.mcs）**已推翻**——GUI 宏上下文能用，COM 自动化历史通道用不了。

**唯一可控密度通道 = 求解频率范围 Fmax**（λ@Fmax 驱动自动网格，`set_frequency_range` 是活的）：
```
300mm WR62 波导实测: Fmax 13.6→67,410 | 15.6→106,272 | 17.6→136,344 单元
R22 弯头实测:       Fmax 11.6→911,988 | 13.6→1,386,798 单元
```
- **加密网格** = 抬高 Fmax（如 15.6），S 参数照常取关心子段（TD 是脉冲响应 FFT，带外求解不影响带内有效性）。
- **缩规模防内存崩** = 压低 Fmax（如 10.6，单元数 ~(10.6/13.6)³≈0.47×）。
- 网格档位标签一律以**实测单元数**为准（meta 记 `n_cells`），不以设置命令自报。
- 同批对比实验必须同 Fmax（默认网格 = Fmax 档，不同 Fmax 的结果不构成同网格家族）。

### 3. 倾斜面/楔形建模: Polygon3D + ExtrudeCurve
Brick 只能轴对齐。倾斜面 (ME dipole 楔形偶极子、Vivaldi 渐变线) 必须用:
```python
r.add_polygon_extrude(name, points=[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)], thickness=2.0)
# VBA:
#   Curve.NewCurve "<name>_curve"
#   With Polygon3D ... .Point(x,y,z) ...  # 闭合三角形, 首点重复为末点
#   With ExtrudeCurve .Thickness(2.0)      # 沿法向拉伸
```
⚠️ **镜像坑**: X 镜像的两个多边形 (如左右偶极子臂), 同点序下法向相反,
   `thickness` 符号要翻转才能对称拉伸。
**圆弧边逼近**（2026-08-15 实测）: 圆边(领结形圆弧、圆角等)用 ~13 段折线
   Polygon3D 逼近即可, 视觉与电气精度均够用, 不必追求更多分段。

### 4. 多 DE 实例导致 COM 路由混乱 (SaveAs 失败)
多次 `DesignEnvironment.new()` 创建多个 DE 进程, COM 调用会被路由到错误实例,
`SaveAs` 报 "Saving of xxx.cst failed"。
**解决**: 每次新工程前 PowerShell 强杀所有 CST DE 进程:
```powershell
Get-Process | Where-Object { $_.Name -like 'CST DESIGN*' } | Stop-Process -Force
```
**防患于未然 (2026-08-28 增)**: 工作流第 0 步「开工查占用」要求单实例独占,
从源头避免多 DE 并存——排队的会话等先到者收尾, 不要靠事后杀进程兜底。

### 5. start_solver 抛 "Unknown error" 时, 改用 run_solver 看真实错误
**重要纠正 (2026-07-25 实测):** `start_solver()` (异步) 在求解器 pre-dispatch 失败时会
**吞掉真实错误**, 只对外抛 "Simulation could not be started. Unknown error"。
之前文档把它当成 "COM 时序问题, 求解器实际已启动" —— **这是错误的**, 会误导排查。

**正确做法:** 改用 `run_solver()` (同步), 它会阻塞到完成并抛出求解器的真实错误信息。
本机最常见的真实根因是 `ERROR: No valid excitation sources defined` (模型缺少端口/
平面波激励)。完整诊断流程见 `references/solver-startup-troubleshooting.md`。

```python
# 推荐: 同步, 抛真实错误
try:
    m.run_solver()    # 阻塞到完成
except RuntimeError as e:
    print(f"真实错误: {e}")   # 这里能看到 "No valid excitation sources defined" 等
```

### 6. ZCode 后台任务 ~10 分钟会被杀, 长时求解必须 GUI 手动
时域求解 10 万网格需 10-20 分钟, ZCode 后台 bash 任务在 ~10 分钟会被环境杀,
Python COM 会话死时工程也被关。
**结论**: 复杂天线求解一律用 CST GUI 手动 Start, 脚本只负责建几何和读结果。

### 7. 导入 STEP/IGES/CAD 必须走 `add_to_history`, 不能走 `_execute_vba_code`
`With STEP ... .Read ... End With` 是 CST 私有简写（和 `With Brick` 同类）,
只能进 history list。`_execute_vba_code` 用标准 VBA 解析器, 遇到 `With STEP` 直接
报 `Expecting 'Declare | Delegate | ...'`。详见 `references/step-import-guide.md`。
最小可用: `m.add_to_history("Import STEP", 'With STEP\\n .Reset\\n .FileName ("x.stp")\\n .Id ("1")\\n .Version ("11.0")\\n .Read\\nEnd With')` → `m.full_history_rebuild()`。

### 8. 中文路径让 CST Python 加载失败（2026-08-15 实测）
脚本、`.cst` 工程目录必须**全 ASCII**（如 `C:\Temp\<项目>\`），放中文路径会 import/库加载报错。
输出文件（csv/png/md 汇报）可以写回中文项目目录——只有 CST 侧输入路径必须 ASCII。

### 9. S11/1D 结果导出的四个坑（2026-08-15 实测）
- `ResultTree.IsResult(...)` 报 bad lexical cast，不能用来判断结果是否存在
- `GetTreeResults(...)` 参数苛刻，1D 结果下返回 0 项（树索引未刷新）
- **批量 add_to_history 导出会全部导成同一个当前选中结果**：把多条 ASCIIExport 攒进 history 后
  一次 rebuild，所有导出跟随最后一次选中项。实测安全路线 = 逐条"SelectTreeItem → add → 立即
  rebuild"出文件（export_ff.py 多条循环真机验证可用；`cst_runner.export_result()` 已按此实现，
  并加了旧文件删除 + 产出文件存在性验证，不再只看选中是否成功）
- `p1.spi` 是 CST 内部二进制缓存，不是 Touchstone
**有效路线**：先 `rt.RefreshView()` / `UpdateTree()` 刷新结果树，用 `GetFirstChildName` /
`GetNextItemName` 遍历拿到结果树**真实名称**，再逐条 SelectTreeItem + ASCIIExport——每条
立即执行出文件，**不要攒进 history 批量重建**。

### 10. 材料定义 VBA 的正确写法（2026-08-15 实测）
```vba
With Material
 .Reset
 .Name "TLY-5"
 .FrqType "all"           ' ✅ 必须显式
 .Type "Normal"
 .Epsilon "2.2"
 .Mu "1"                  ' ✅ 是 .Mu 不是 .Mue；数值必须带引号（字符串）
 .Create                  ' ✅ 结尾 .Create 创建（不存在 .NewMaterial）
End With
```
`TandMod` / `TandFit` 不存在，损耗只设 `.LossTangent`。

### 11. 几何查询 API 怪癖（2026-08-15 实测）
- `GetLooseBoundingBoxOfShape` 返回 **7 元组**（首元素是 bool，后 6 个才是 xmin..zmax）——按 3 元组解包会错
- cylinder 的 loose bbox 不准，做布尔/对位前先用多个视角核对或改用解析计算

### 12. 多段波导建模四坑（2026-08-26/27 折叠弯头项目实测）
- **面接触并集会静默丢件**：共面贴合的 solid 用 `Solid.Add` 逐个并入后体积缺失（40k mm³ 级），S21 全反射。
  可靠做法：**建一个包围盒 PEC，把每个内腔体逐一从壳上 Subtract**（不做并集），每步可用
  `Solid.GetVolume` 验证雕刻量是否等于该件体积。
- **Polygon3D 绕向由点序参数方向决定**：同一多边形函数按 z 升序参数化是 CCW、降序变 CW，
  ExtrudeCurve 拉伸会翻到法向反侧（bbox 偏移整整一个厚度）。多边形函数一律固定升序参数化；
  build 后必须做 **bbox + 体积双校验**（bbox 对体积错 = 拉伸方向问题；单看 bbox 抓不住）。
- **新建工程默认边界不是 electric**（纠正旧文档）：闭合波导器件必须显式六面 electric + 背景
  vacuum，否则 open 边界下端口错位泄漏（直波导 S21 仅 -17dB）。详见 interface-guide §6。
- **弯区外弧与壳壁相切=亚毫米PEC薄片**（2026-08-27）：蛇形板布局中 U 弯外弧顶到壳内壁仅 0.1mm 时，
  六面体网格产生薄片 PEC，结果违反无源性（S11>+0dB）。**弯头类结构四周呼吸间隙 ≥4mm** 是硬要求；
  修后 board2 仍存在 S11>0 异常（转 GUI 视觉自查+收敛性研究待办）。
- **Solid.Add 并集丢件的兄弟问题**：逐件 Subtract 方案下若两内腔体深重叠也会算错体积——verify() 的
  解析体积对照能兜住。

### 13. 远场方向图导出四坑（2026-08-28 远程委托实测，四轮定稿）
- **3D 远场结果不能直接 ASCIIExport**：选中 `Farfields\farfield (f=..)` 后导出报
  "No plot data available"（两次实测）——ASCIIExport 只认 1D 树项/活动 1D 绘图数据。
- **plot/export 类命令走 `add_to_history` 重放是空操作**：`With FarfieldPlot .Plot` /
  `.CopyFarfieldTo1DResults` / `.ASCIIExportAsSource` 塞进 history 后 rebuild 不报错但
  什么都没发生（copy 无子项、源文件不出现）。
- **`_execute_vba_code`（立即执行通道）要求顶层语句包 `Sub Main() ... End Sub`**：
  裸语句报 "Expecting 'Declare | Delegate | ...'"。包上后 plot 类命令真正生效。
- **切面导出唯一可靠路线 = 单个 Sub Main 内原子执行 plot+export**：
  ```python
  m._execute_vba_code(
    'Sub Main()\n'
    'SelectTreeItem "Farfields\\\\farfield (f=11.424) [1]"\n'
    'With FarfieldPlot\n .Reset\n .Plottype "cartesian"\n .Vary "angle1"\n'
    ' .Phi 90.0\n .Step 1.0\n .Plot\nEnd With\n'
    'With ASCIIExport\n .Reset\n .FileName ("D:/path/ff_cut.txt")\n'
    ' .Mode ("FixedNumber")\n .Execute\nEnd With\n'
    'End Sub')
  ```
  输出格式 `Theta[deg] Phi[deg] Abs(Dir.)[dBi] Abs/Phase(Theta) Abs/Phase(Phi) Ax.Ratio`
  ——**Abs(Dir.) 是方向性 dBi，固定取第 2 数据列**（表头 token 因 `[dBi ]` 定宽切分与数据列
  不对齐，不能按 token 序号取列；实测踩坑：误取 Phase 列得出 357"dBi" 荒谬值）。
- 分步 plot→copy 两次会抓到**同一默认切面**（copy 取工程存的绘图状态，新的 phi 设置不生效）；
  原子块内顺序执行才保证切面正确。流程要点：开工先查占用/写锁，收尾按 PID 精确回收（见 cst-automation 开工纪律）。

### 14. 远场无头导出五坑 + .ffd 全 3D 路线（2026-08-28 深夜远程委托 v1→v7 七轮实测）
- **quiet 模式（`DesignEnvironment.new()` 默认）绘图引擎不加载远场数据**：一切 plot 类命令
  （ASCIIExport/CopyFarfieldTo1DResults/CalculateList）报 "No plot data available" 或
  "Farfield could not be calculated"——**不是语法错，是数据没进绘图引擎**。1D 树数据
  ASCIIExport 不受影响（走结果树，不走绘图引擎）。
- **`with de.quiet_mode_disabled():` 开 GUI 跑远场 Plot 会死锁**：DE CPU 冻结、COM 调用
  永久阻塞（实测挂 35 分钟），疑似锁屏桌面 3D 渲染/模态框。**远场自动化禁用 GUI 模式**；
  判死法：远程 Get-Process 看 DE TotalProcessorTime 5s 零增量。
- **无头全 3D 远场唯一可行路线 = quiet 模式裸 `ASCIIExportAsSource`（不调 `.Plot`、不设
  Plottype）**：`SelectTreeItem FF` → `FarfieldPlot.Reset` → `ASCIIExportAsSource "path.ffd"`
  → 输出公开格式 Farfield Source v3.0（功率元数据 + 73φ×37θ@5° 复分量 Eth/Eph）。
  注意 `.Plot` 一旦调用反而不出文件（把绘图对象置空态）。离线积分 D=4π|E|²max/∮|E|²dΩ
  与 GUI 切线差 0.26dB（5° 网格正常量级）。离线重积分按 .ffd 公开格式解析即可。
- **`CopyFarfieldTo1DResults` 恰好 2 参数（VBA 逗号分隔）**：`.CopyFarfieldTo1DResults "a", "b"`
  （空格分隔报 "Unexpected text"，单参数报 "2 required, 1 provided"）。签名考古法：
  `tr -c '[:print:]' '\n' < modeler_AMD64.exe | sed -n 'N,Mp'` 看方法名邻域参数表。
- **`prj.close()`/`de.close()` 可段错误击杀整个 python（finally 不执行 → 锁+DE 双泄漏）**：
  收尾顺序必须是 落盘 manifest → 按本会话 PID 杀 DE → 删锁 → `os._exit(rc)` 硬退，
  绝不把锁释放托付给 finally。另：add_to_history 的 VBA 脚本里**所有变量必须显式 Dim**
  （含循环变量），Sub 包装不被 history 解析器接受（但被 `_execute_vba_code` 要求，见坑 13）。

### 15. TD 求解器"最大脉冲宽度数"截断长路径板级仿真（2026-09-01 长路径板级仿真实测）
**现象**：板级长路径（1.8–2.2 m 蛇形）TD 求解 ~14 min 即停，output.json 报
"Maximum number of pulse widths simulated, solver stopped. …steady state criterion could not be
satisfied"——S 参未收敛不可信（默认脉冲宽度上限远小于长结构 ring-down 需要的宽度数）。
**旋钮（2 m WR62 判决探针实证）**：`With Solver … .NumberOfPulseWidths ("300") … End With`——
对照实验：无上限自然收敛 112 s；配 "2" 61 s 截断（旋钮有效）；`Duration` 属性存在但配 "2"
117 s ≈ 自然收敛（无效）。注意：`.Accuracy` 在 2025.2 的 Solver 对象上**不存在**（版本敏感，
cst_runner 旧注释正确）；未知属性名 add_to_history 会报 10091（可做存在性快探，几秒一个）。
**判决法**：拿天然需要几十个脉冲宽度才衰减完的长直波导（2 m WR62, 9.6–12.6 GHz, ~38 万单元）
配极限值 "2"——秒级返回=旋钮有效，分钟级=无效。迷你短波导收敛太快，无法区分"旋钮生效"与"无效果"。
**配套纪律**：求解后必须读 `<proj>/<proj>/Result/output.json` 判 `steady_state`（truncated/ok），
截断数据禁入设计结论（meta.json 落 `steady_state` 字段，CSTRunner.solver_truncation_flag()）。

### 16. 跨机委托大模型求解：SSH 非交互会话挂起 → 计划任务注入交互会话（2026-09-01 实测）
SSH 直启 CST 跑大模型（百万单元级）会死在 TST "parallelization control"（小模型 24 s 正常解出，
非许可证/引擎/CPU/内存问题）；**同机交互桌面会话里同一模型可正常过该阶段**。
解锁路线：目标机有同用户交互登录会话时，用计划任务（`Register-ScheduledTask -Principal
(New-ScheduledTaskPrincipal -UserId <user> -LogonType Interactive)` + `Start-ScheduledTask`）
把跑批 cmd 注入其桌面会话（Win32_Process.SessionId 应等于 explorer.exe 的会话）。
**配套坑**：① `.cmd`/Python 补丁里 `C:\...\fold_board` 的 `\f` 会被转义层吃掉（写完必须
`Get-Content` 回读核对路径完整性）；② `subprocess` 派生任务脚本必须带 `python -u`，否则
任务脚本 stdout 块缓冲，远程 run_live.log 观测不到任何进度；③ 过夜跑前置检查：`powercfg
/change standby-timeout-ac 0` + `hibernate-timeout-ac 0` + 盖开合 `LIDACTION 0`（交流档）、
电池状态 BatteryStatus=2（在线）。④ 收尾 watchdog：run_batch 每任务独立 CST 进程 + 单任务
上限（5–6 h）+ 完成自动打包 results_bundle.zip，任何一任务挂死不拖垮整批。

### 17. 3D 场监视器结果导出三坑（2026-08-26 起 v1→v4 四轮排障实锤）
- **缺 `.Step(采样步宽)` = 导出零数据**：`ASCIIExport` 对 3D 场结果不报错，文件正常生成，
  但**只有表头 2 行**（x y z + Ex/Ey/Ez 复数分量的列头 + 分隔线）——v1→v3 全栽在这。
  **`.Step ("0.25")`（mm）必填**；全域扫描 1.0mm、热点区细扫 0.25mm 实测可用。
- **树路径叶子名带 `[N]` 运行号后缀，必须枚举拿真名**：如
  `2D/3D Results\E-Field\e-field (f=11.424) [1]`——后缀随求解次数递增，硬拼路径必错。
  枚举路线：`rt = m.ResultTree` → `RefreshView()` → `GetFirstChildName`/`GetNextItemName`
  遍历（`cst_runner.list_3d_results()` 已封装；⚠️ `cst.results.ProjectFile.get_tree_items`
  只支持 '0D/1D' 过滤器，2026-09-02 实测，列不了 3D）。
- **quiet 模式可导（与坑 14 远场 plot 类不同）**：3D 场数据走结果树不走绘图引擎，
  `ASCIIExport .Mode("FixedWidth") .Step .SetFileType("ascii") .ExportCoordinatesInMeter("False")`
  在 quiet 无头模式下正常出文件——别把坑 14 的"绘图引擎没数据"错推到场导出上不敢做。
  路线 = 坑 13 同款 `Sub Main()` 原子块 + `_execute_vba_code`（不走 history）。
- 输出格式：9 列定宽 `x y z ExRe ExIm EyRe EyIm EzRe EzIm`（mm/V/m；H 场为 Hx/Hy/Hz），
  规则网格点云（百万行级，写入需数十秒——轮询文件尺寸写稳再判成败，`cst_runner.export_field_ascii()`
  已内置）。Hfield 监视器结果同时含磁场与**表面电流**（官方文档：CST 由切向 H 导出）。
  参考实现：`scripts/remote/run_remote_cst.py` 的 field 导出路线。

## 补充纪律（2026-08-16 借鉴外部 cst-simulation skill）

1. **存参数 ≠ 改几何**：`StoreParameter` 后必须 `full_history_rebuild()` 并确认几何已更新——参数存储本身不会改变已建实体。
2. **解析曲线/曲面用端点安全公式**：避免非整数幂或端点奇异的表达式（边界处发散会导致 Rebuild 报 invalid analytical face）。短路面/非闭合曲线/布尔失败等警告一律视为几何审计失败，解释或修复后才继续。
3. **优化驱动的几何保持 CST 参数直接可调**：RL/优化器控制的轮廓用命名参数表达，不要冻结成静态采样折线（除非用户明确要冻结模型）——否则每轮优化都要重建工程。
4. **导出必须带元数据**：S 参数导出时同步把 port/mode 映射、求解器类型、solver band、日期、已知警告写进 `results/cst_results.json`。模式身份未验证时按 CST 端口/模式索引标注，不硬标 TE/TM。
5. **一次 run 可复现**：同一 run folder 内保留 source project、脚本、参数表、CST 版本、求解器、频段、状态标签（见 cst-automation「结果状态标签」），做到另一个 agent 照着能复现。
6. **工程被锁别硬写**（2026-08-15 实测）：`project.close()` 可能抛 TimeoutError，残留 DE 进程锁住 `.cst`——此时复制副本操作，不要对被锁文件强行 SaveAs；收尾用 taskkill / `cleanup_cst()` 清干净。

## 远程委托

本机资源紧张时，可把「打开工程→求解→导出」委托给局域网内另一台装了 CST 的 Windows 机器（OpenSSH + 同版本 CST）。通用载荷与流程见 `cst-automation` 的「远程委托参考」（`scripts/remote/run_remote_cst.py` + `spawn_detached.py`，坑 13/14/17 的导出路线已全部内置）。
