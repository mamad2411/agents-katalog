---
name: gmx-mmpbsa
description: "gmx_MMPBSA 结合自由能计算的完整方法论指南。当 Agent 需要使用 gmx_MMPBSA 计算蛋白-蛋白或蛋白-配体结合自由能（ΔG_bind）时必须调用此技能。覆盖场景：MM/PBSA、MM/GBSA 计算、结合能分析、gmx_MMPBSA 参数配置、力场搭配、采样策略选择、受体/配体定义、PBC 轨迹预处理、结果验证。即使用户只是提到'算结合能'、'MMPBSA'、'binding energy'、'gmx_MMPBSA'而没有详细说明，也应触发此技能。本技能包含五步决策流程、八项已知易错点、六步检查点确认和七项验证清单，确保计算结果可靠。"
---

# gmx_MMPBSA 结合自由能计算

本技能封装了基于 GROMACS MD 轨迹，用 gmx_MMPBSA 计算两分子间（蛋白-蛋白/蛋白-配体）结合自由能的完整方法论。方法论与具体项目解耦，可复用于任何 GROMACS 体系。

## 前提条件

- GROMACS 模拟已完成，有 .tpr、.xtc（或 .trr）、.ndx、topol.top
- gmx_MMPBSA 已安装（conda 环境，v1.6.x，基于 AmberTools 20+）
- 轨迹已做 PBC 校正 + fit（若未做，需先执行 PBC 修正）

**版本兼容性**：本技能基于 gmx_MMPBSA v1.6.x 编写。v1.5.x 及更早版本的部分参数可能不同（如 `strip_mask` 语法、`&pb` 段参数名）。运行前建议 `gmx_MMPBSA --version` 确认版本。

## 核心概念

gmx_MMPBSA 计算结合自由能的公式：

```
ΔG_bind = G_complex - G_receptor - G_ligand
G = E_MM + G_solv - TΔS
E_MM = E_bond + E_angle + E_dihedral + E_vdw + E_elec
G_solv = G_polar(GB/PB) + G_nonpolar
```

**关键认知**：MM/PBSA 的绝对量级不可靠（系统性偏高），但**同参数多体系的相对趋势**是可靠的。验证以相对趋势为核心，不依赖绝对值。

## 输入契约

运行前确认以下文件齐全：

| 输入 | 必需 | 说明 |
|------|:----:|------|
| `*.tpr` | ✓ | 复合物结构（GROMACS 运行输入文件） |
| `*.xtc` | ✓ | PBC 校正 + fit 后轨迹（**不能用原始 xtc**） |
| `index.ndx` | ✓ | 含受体/配体独立索引组 |
| `topol.top` | ✓ | 拓扑文件（非标残基/小分子必须） |
| `ref.pdb` | | 参考结构（无氢、正确链 ID） |

详细参数说明见 [input-contract.md](references/input-contract.md)。

## 五步决策流程

运行 gmx_MMPBSA 前，必须完成以下五项决策。每项决策都有明确的确定方法，不是拍脑袋。

### 决策 1：力场搭配（forcefields）

从 topol.top 的 `#include` 和 `[ molecules ]` 识别体系构成：

| 体系构成 | forcefields 写法 |
|----------|------------------|
| 纯蛋白 | `"leaprc.protein.ff14SB"` |
| 蛋白 + 小分子（GAFF/GAFF2） | `"leaprc.protein.ff14SB,leaprc.gaff2"` |
| 蛋白含非标残基（共价修饰） | `"leaprc.protein.ff14SB,leaprc.gaff2"` |

**确定方法**：
1. 查 topol.top 的 `#include` 和 `[ molecules ]`
2. 识别标准蛋白（ff14SB）、独立小分子（GAFF）、自定义残基（揉进蛋白链）
3. 独立小分子 → 查 itp 力场 → 对应 leaprc
4. 自定义残基 → 默认追加 gaff2（稳妥）

详细决策表见 [forcefield-mapping.md](references/forcefield-mapping.md)。

### 决策 2：受体/配体定义（-cg）

- 受体/配体必须是索引文件中的**两个独立组**
- **0-based 编号**（从 0 开始数，不是 1）
- **通用原则**：受体/配体定义由科学问题决定
  - 比较"蛋白 A 与蛋白 B 的相互作用" → A、B 各自独立分组
  - 比较"药物如何改变 A-B 结合" → 药物算进 A 侧（保持化学完整性）
  - 例：分子胶水 → 算进受体侧；共价修饰 → 算进受体链

### 决策 3：轨迹与 PBC（-ct）

轨迹必须是 **PBC 校正后 + fit** 的（无跨盒跳跃、无旋转平移漂移）。**不能用原始 xtc 直接喂给 gmx_MMPBSA**。

若轨迹未做 PBC 校正，调用 `gromacs-protein-analysis` 技能完成 PBC 修正后再继续。

### 决策 4：采样策略（startframe/endframe/interval）

| 溶剂模型 | 每帧成本 | 目标帧数 |
|----------|:--------:|:--------:|
| GB | 低 | 数千帧 |
| PB | 高（比 GB 贵数倍） | 数百帧（100-500） |

**确定方法**：
1. `gmx check -f <traj>` 得轨迹总帧数 N
2. `interval = N / 目标帧数`
   - 例：N=100000（1 μs @ 10 ps/帧），PB 目标 100 帧 → interval=1000
   - 例：N=100000，GB 目标 2000 帧 → interval=50

**必须先跑小规模测试（10-100 帧）验证配置无误，再放全量。**

### 决策 5：溶剂模型选择（&gb / &pb）

| 模型 | 适用 | 关键参数 |
|------|------|----------|
| GB (igb=5) | **推荐默认**。快速筛选、大体系 | saltcon=0.150 |
| GB (igb=2) | 旧版模型，适合小蛋白 | saltcon=0.150 |
| GB (igb=8) | 更精确的 GB 模型（GBneck2），适合蛋白-蛋白 | saltcon=0.150 |
| PB (ipb=2) | 更严格的静电处理 | indi=1.0, exdi=80.0, istrng=0.15 |

saltcon/istrng 应与模拟时的盐浓度匹配（如 0.15 M NaCl → 0.150）。

详细参数与模型选择指南见 [sampling-strategy.md](references/sampling-strategy.md)。

### 生成 mmpbsa.in

使用 gmx_MMPBSA 自带命令生成初始模板，然后按需编辑修改：

```bash
# 生成 GB 模板
gmx_MMPBSA --create-input gb

# 生成 PB 模板
gmx_MMPBSA --create-input pb
```

生成的 `mmpbsa.in` 包含所有参数的默认值和说明注释，只需修改 `startframe`/`endframe`/`interval`/`forcefields`/`saltcon`/`istrng` 等关键参数，其余保持默认。

## 执行检查点（六步确认流程）

这是 agent 交互式 skill 的核心——每步都需要用户确认后再继续。

```
① 输入检查：tpr/xtc/ndx/top 齐全 + PBC 已校正 + 三原子数一致
   → 展示索引组列表 → 用户确认受体/配体组名和编号

② 力场推断：从拓扑识别蛋白/小分子/自定义残基
   → 展示 forcefields 写法 → 用户确认

③ 采样确认：展示轨迹帧数 + 建议 interval
   → 用户确认（或覆盖）

④ 试跑验证：小规模（10-100 帧）跑通
   → 展示中间产物 + 无报错 → 用户确认放全量

⑤ 全量执行：mpirun 并行
   → 结果摘要（ΔG_bind 均值/标准差）

⑥ 验证报告：文件齐全 + 相对趋势合理 + 无 NaN
   → 用户签字
```

## 已知易错点（故障排查）

以下 8 个易错点来自实战踩坑，必须在执行前检查：

| # | 故障 | 根因 | 修复 |
|---|------|------|------|
| 1 | `Could not find necessary program [ GROMACS ]` | gmx_path 填了文件路径而非目录 | 填绝对目录路径 `.../bin` |
| 2 | -cg 组错（受体配体搞反/编号错） | 0-based 编号误解 | 跑前确认索引组，make_ndx 编号直接用于 -cg |
| 3 | 轨迹有 PBC 跳跃 | 未做 PBC 校正 | 调用 `gromacs-protein-analysis` 技能完成 PBC 修正 |
| 4 | 非标残基报错无法识别 | 没提供拓扑 | 加 `-cp topol.top` + forcefields 追加 gaff2 |
| 5 | parmed `Overriding DihedralType` 警告 | 自定义参数与蛋白力场重叠 | 正常警告，可忽略 |
| 6 | PB 太慢/内存爆 | 帧数太多 | interval 放大 |
| 7 | tpr 与 top 不同源（原子数不符） | 用了不同 pdb2gmx/grompp 产物 | 核对 tpr/top/ndx 原子数一致 |
| 8 | 轨迹未 fit（整体旋转漂移） | 只 center 没 fit | 调用 `gromacs-protein-analysis` 技能完成 fit |

详细故障排查见 [troubleshooting.md](references/troubleshooting.md)。

## 验证清单

计算完成后，必须通过以下 7 项验证：

| # | 检查项 | 断言 |
|---|--------|------|
| 1 | FINAL_RESULTS_MMPBSA.dat 存在且含 ΔG_bind | 文件存在 + 有数值 |
| 2 | 相对趋势合理 | 同参数多体系对比趋势合理（不依赖绝对量级） |
| 3 | CSV 逐帧能量无 NaN/Inf | grep 检查 |
| 4 | 受体/配体 prmtop 生成成功 | REC.prmtop / LIG.prmtop 存在 |
| 5 | 采样帧数符合预期 | CSV 行数 == interval 采样的帧数 |
| 6 | 能量项完整 | PB: VDWAALS/EEL/EPB/ENPOLAR；GB: VDWAALS/EEL/EGB/ESURF |
| 7 | 力场/拓扑一致 | 无 forcefield 错误日志 |

详细验证脚本与判定标准见 [verification.md](references/verification.md)。

## 熵校正（可选）

gmx_MMPBSA 默认不计算熵贡献（-TΔS）。如果需要熵校正，有三种方法：

| 方法 | 命令参数 | 说明 |
|------|----------|------|
| Normal Mode Analysis | `&nmode` 段 | 最精确，但计算量极大（需收敛构象） |
| Interaction Entropy | `&general` 段 `interaction_entropy=1` | 较快，推荐用于大体系 |
| C2 Entropy | `&general` 段 `c2_entropy=1` | 最快，基于能量方差估算 |

**注意**：熵校正对绝对 ΔG_bind 影响大，但对相对趋势影响小。如果只比较相对趋势，可不加熵校正。

## 输出文件说明

gmx_MMPBSA 运行后会在当前目录生成以下文件：

| 文件/目录 | 说明 |
|-----------|------|
| `FINAL_RESULTS_MMPBSA.dat` | 最终结果（文本格式，含 ΔG_bind 及各能量分项） |
| `FINAL_RESULTS_MMPBSA.csv` | 逐帧能量（CSV 格式，可用于绘图和统计） |
| `COMPLEX.prmtop` | 复合物 Amber 拓扑 |
| `REC.prmtop` | 受体 Amber 拓扑 |
| `LIG.prmtop` | 配体 Amber 拓扑 |
| `_MMPBSA_*` | 临时文件（正常运行后可删除） |
| `mmpbsa.log` | 运行日志（排查错误用） |

临时文件 `_MMPBSA_*` 可通过 `gmx_MMPBSA --cleanup` 清理。

## 拒绝策略

以下情况必须停止并提示用户，不硬做：

| 情况 | 行为 |
|------|------|
| 轨迹未做 PBC 校正 | 停止，先跑 PBC 修正 |
| 索引缺受体/配体组 | 停止，指导 make_ndx 建组 |
| 非标残基且无 `-cp` 拓扑 | 停止，要求提供拓扑 |
| 小分子配体未知力场 | 停止，查 itp 确定 GAFF/GAFF2 |
| PB 采样帧数 > 500 | 警告，建议放大 interval |
| tpr/top/ndx 原子数不一致 | 停止，核对同源性 |

## 参考文档

深入阅读以下参考文档：

- [力场搭配决策表](references/forcefield-mapping.md) — 完整的力场选择方法与判断规则
- [输入契约与命令行](references/input-contract.md) — 输入文件清单、参数全解、索引组准备
- [采样策略](references/sampling-strategy.md) — 采样量计算与溶剂模型选择
- [故障排查](references/troubleshooting.md) — 8 个已知易错点的详细修复方案
- [验证清单](references/verification.md) — 7 项验证的可执行命令与判定标准
