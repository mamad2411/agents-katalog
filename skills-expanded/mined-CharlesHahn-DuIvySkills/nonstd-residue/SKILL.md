---
name: nonstd-residue
description: "非标残基力场构建的完整流程指南。当 Agent 需要为共价修饰的非标准残基（如 BBO-10203 共价结合 CYS 形成的 CYB）构建 GROMACS 力场定义时必须调用此技能。覆盖场景：从 Sobtop 输出的 itp 文件（RESP2 电荷 + GAFF 拓扑已就绪）开始，生成 rtp/hdb 残基定义、注册 GAFF 参数到本地力场副本、组装 PDB、运行 pdb2gmx 验证。适用于任何通过共价键连接到蛋白残基的小分子配体（如分子胶水、共价抑制剂）。即使用户只是提到'非标残基'、'共价修饰'、'构建力场'、'rtp/hdb'而没有详细说明，也应触发此技能。本技能包含五阶段端到端流程、六步检查点确认和十四项验证清单，确保构建的力场可直接用于 MD 模拟。"
---

# 非标残基力场构建

本技能封装了从 Sobtop 输出的 itp 文件到 GROMACS 可用非标残基力场的完整构建流程。适用于任何通过共价键连接到蛋白残基的小分子配体。

## 前提条件

### 1. 理解问题本质

非标残基力场构建的本质是**四层变换**：

```
输入                          →   处理              →   输出
sobtop itp (GAFF拓扑+RESP2)       拓扑抽象化          非标残基定义 (rtp+hdb)
复合物晶体 PDB                   几何重组            组装后 PDB + 力场副本 + 验证报告
连接声明 (CYS-SG-thioether)      力场参数聚合
```

四层不变量：
1. **拓扑层**：itp `[atoms]/[bonds]/[dihedrals]` → rtp `[atoms]/[bonds]/[impropers]` + hdb
2. **参数层**：GAFF atomtypes/bondtypes/angletypes/dihedraltypes → amber14sb 副本（去重、幂等）
3. **电荷层**：骨架 Amber 标准值 + 侧链/配体 RESP2 + 均摊调整
4. **几何层**：晶体 PDB 中"连接残基重原子 + 配体 HETATM"重组为连续残基

### 2. 输入文件要求

#### Sobtop 输出的 itp 文件

**什么是 Sobtop？**
Sobtop 是一个分子力场参数化工具，用于计算小分子的 RESP2 电荷和 GAFF 拓扑参数。它基于量子力学计算（如 Gaussian/ORCA）的输出，生成 GROMACS 可用的 .itp 文件。

**itp 文件必须满足的条件：**
- 已完成 RESP2 电荷计算（`[ atoms ]` 段第 8 列为电荷值）
- 已完成 GAFF 拓扑参数化（`[ bonds ]/[ angles ]/[ dihedrals ]` 段完整）
- 通常使用**加帽三肽**构型（ACE-连接残基-NME），但也可使用其他构型

**为什么通常使用加帽三肽？**
- 孤立配体的 RESP2 电荷不包含骨架电荷信息
- 加帽三肽（ACE-CYS-NME）提供了完整的骨架原子（N/CA/C/O/HA/H）
- 这些骨架原子的电荷需要与 Amber ff14SB 标准值一致
- 如果使用其他构型，需要手动提供骨架电荷信息

**如何验证 itp 文件？**
```bash
# 检查是否有 [ atomtypes ] 段（GAFF 参数）
grep -A 10 "\[ atomtypes \]" <input>.itp

# 检查是否有 [ atoms ] 段（RESP2 电荷）
grep -A 10 "\[ atoms \]" <input>.itp

# 检查原子数（加帽三肽通常 80-120 个原子）
grep -c "^\s*[0-9]" <input>.itp
```

#### 复合物晶体 PDB 文件

**PDB 文件必须满足的条件：**
- 包含连接残基（如 CYS242）的 ATOM 记录
- 包含配体（如 BBO-10203）的 HETATM 记录
- 配体残基编号紧跟连接残基之后（通常为连接残基编号 + 1）
- 只保留主构象（altloc = '' 或 'A'）

**如何验证 PDB 文件？**
```bash
# 检查连接残基是否存在
grep "ATOM.*CYS.*242" <complex>.pdb

# 检查配体是否存在
grep "HETATM.*1000\|HETATM.*BBO" <complex>.pdb

# 检查残基编号连续性
grep -E "^(ATOM|HETATM)" <complex>.pdb | awk '{print $5}' | sort -n | uniq
```

### 3. 软件依赖

| 软件 | 版本 | 用途 | 安装方式 |
|------|------|------|----------|
| GROMACS | 2024+ | pdb2gmx 验证 | 系统包管理器或源码编译 |
| Python | 3.6+ | 脚本运行 | 系统自带 |
| PDBFixer | — | 修复晶体 PDB 缺失原子 | `conda install -c conda-forge pdbfixer` |
| OpenBabel | — | 分子格式转换 | `conda install -c conda-forge openbabel` |

**GROMACS 路径配置：**
```bash
# 查找 gmx 可执行文件
which gmx

# 如果 gmx 不在 PATH 中，需要设置 GMXLIB 和 PATH
# 例如：export GMXLIB=/path/to/gromacs/share/gromacs/top
# 例如：export PATH=/path/to/gromacs/bin:$PATH

# 验证 GROMACS 版本
gmx --version
```

**conda 环境激活：**
```bash
# 激活环境（包含 PDBFixer、OpenBabel）
conda activate <env_name>

# 或使用 micromamba
micromamba activate <env_name>
```

### 4. 工作目录准备

```bash
# 创建工作目录
mkdir -p /tmp/nonstd_residue_build
cd /tmp/nonstd_residue_build

# 复制输入文件（根据实际路径调整）
cp <path_to_itp>/input.itp .
cp <path_to_pdb>/complex.pdb .

# 复制力场目录（从项目或下载）
cp -r <path_to_ff>/amber14sb.ff .
```

## 输入契约

| 输入 | 必需 | 说明 |
|------|:----:|------|
| `*.itp` | ✓ | Sobtop 输出的拓扑文件（RESP2 电荷 + GAFF 参数已就绪） |
| `complex.pdb` | ✓ | 复合物晶体 PDB（含连接残基和配体坐标） |
| `linkage` | ✓ | 连接类型（cys_thioether / ser_ester / lys_amide / tyr_ether） |
| `resname` | ✓ | 新残基名（≤3 字符，如 CYB） |
| `residue_num` | ✓ | 连接残基在 PDB 中的残基编号 |
| `formula` | | 分子式（如 C34H32，用于 H 数验证） |

详细参数说明见 [input-contract.md](references/input-contract.md)。

## 端到端流程（五阶段 A–E）

### 阶段 A：结构层 — 基础准备

1. **准备力场副本**：下载或复制 Amber ff14SB 力场到工作目录
2. **PDBFixer 补全**：修复晶体 PDB 中缺失的重原子

**为什么需要 PDBFixer？**
- 晶体 PDB 可能缺失部分原子（如侧链、氢原子）
- PDBFixer 补全缺失的重原子（非氢原子）
- 氢原子由 pdb2gmx 按 hdb 规则生成

### 阶段 B：拓扑抽象化 — itp → 残基定义

1. **解析 itp**：读取 `[atoms]/[bonds]/[dihedrals]` 段
2. **识别残基区间**：自动推断 ACE/连接残基/NME/配体分段 → **【检查点①】用户确认**
3. **电荷层处理**：骨架 Amber 标准值 + 侧链 RESP2 + 均摊调整
4. **生成 rtp**：含 `-C N` 肽键 + improper 项
5. **生成 hdb**：按方法码映射表自动判定 → **【检查点②】用户确认原子数/电荷/method 分布**

**为什么 rtp 首键必须是 `-C N`？**
- `-C N` 表示前一个残基的 C 原子与当前残基的 N 原子之间的肽键
- 这是 pdb2gmx 识别残基连接的关键
- 缺少这个键会导致残基与 N 端跑散

### 阶段 C：参数聚合 — GAFF → 力场副本

1. **安装 rtp/hdb**：追加到本地力场副本（先 .bak 备份）
2. **注册 GAFF 参数**：atomtypes/bondtypes/angletypes/dihedraltypes（幂等、去重）→ **【检查点③】用户确认文件清单**

**为什么需要注册 GAFF 参数？**
- GAFF 原子类型（如 ca、c3、ha）不在标准 Amber ff14SB 中
- 必须注册到 `ffnonbonded.itp` 的 `[ atomtypes ]` 段
- 否则 grompp 会报 `Unknown atomtype`

### 阶段 D：几何重组 — 晶体 PDB → 连续残基

1. **提取重原子**：连接残基重原子 + 配体 HETATM，按 rtp 顺序合并
2. **组装 PDB**：原子序严格对齐 rtp → **【检查点④】用户确认重原子数/来源**

**为什么只保留重原子？**
- 氢原子由 pdb2gmx 按 hdb 规则生成
- 晶体 PDB 中的氢原子坐标不精确
- hdb 规则确保氢原子的初始几何符合力场要求

### 阶段 E：验证与交付

1. **pdb2gmx 验证**：用本地力场副本运行 pdb2gmx
2. **全量验证**：十四项清单 → **【检查点⑤】用户确认验证报告**
3. **人工复核**：分子式/H 数/立体化学/手性中心 → **【检查点⑥】用户签字**

## 执行检查点（六步确认流程）

```
① 残基区间划分：展示 itp 解析结果 → 用户确认 ACE/连接残基/NME/配体分段
② rtp/hdb 生成：展示原子数/总电荷/method 码分布表 → 用户确认
③ 力场注册：展示将修改的文件清单（先 .bak 备份）→ 用户确认
④ PDB 组装：展示重原子数与来源 → 用户确认
⑤ pdb2gmx 验证：展示拓扑 + 十四项验证报告 → 用户确认
⑥ 人工复核：分子式/H 数/立体化学/手性中心 → 用户签字
```

## 已知易错点

| # | 故障 | 根因 | 检测 |
|---|------|------|------|
| 1 | pdb2gmx 通过但残基与 N 端跑散 | rtp `[ bonds ]` 缺 `-C N` 肽键 | 检查 rtp 首键含 `-C N` |
| 2 | H 初始几何偏差 | hdb 方法码与母原子杂化不一致 | method↔杂化一致性校验 |
| 3 | mdrun 含非标残基崩溃 | GAFF improper 在 GPU bonded kernel 越界 | 强制 `-bonded cpu -update cpu` |
| 4 | 残基总电荷不为零 | 均摊调整计算错误 | 验证电荷总和 |
| 5 | GAFF 类型未注册 | 遗漏 atomtypes 注册 | 检查 itp 中每个 GAFF 类型都在 atomtypes.atp 中 |

详细故障排查见 [troubleshooting.md](references/troubleshooting.md)。

## 拒绝策略

| 情况 | 行为 |
|------|------|
| `linkage` 不在模板库 | 停止，提示未覆盖的连接类型 |
| 配体含未覆盖的 H 环境 | 停止，报"需人工处理" |
| 区间推断有歧义 | 停止，请求用户指定 |
| method 码校验失败 | 停止，提示修正生成器 |
| 分子式 H 数 ≠ rtp H 数 | 警告 + 要求确认 |

## 参考文档

- [输入契约](references/input-contract.md) — 输入参数全解
- [hdb 方法码规范](references/hdb-method-codes.md) — 方法码权威定义与 GAFF 映射
- [连接模板](references/linkage-templates.md) — CYS/SER/LYS/TYR 连接化学
- [电荷策略](references/charge-strategy.md) — 骨架电荷与均摊调整
- [故障排查](references/troubleshooting.md) — 已知故障与修复方案
- [验证清单](references/verification.md) — 十四项可执行验证

## 脚本说明

本技能包含七个 Python 脚本，按顺序执行。

### 脚本与原始脚本的关系

| 位置 | 脚本 | 说明 |
|------|------|------|
| `examples/cyb/scripts/` | 10 步构建脚本 | **原始实战版**，经过 CYB 构建验证，包含硬编码参数 |
| `nonstd-residue/scripts/` | 7 个 Python 脚本 | **技能通用版**，从头写的简化版，参数化设计 |

**建议**：验证技能脚本时，以 `examples/cyb/scripts/` 的输出为基准（golden files）。

### 如何修改脚本用于其他非标准残基

1. **CYS 硫醚连接**（当前支持）：直接使用
2. **SER 酯连接**：修改 `build_rtp.py` 中的骨架电荷来源为 SER
3. **LYS 酰胺连接**：修改 `build_rtp.py` 中的骨架电荷来源为 LYS
4. **TYR 醚连接**：修改 `build_rtp.py` 中的骨架电荷来源为 TYR

详细说明见 [linkage-templates.md](references/linkage-templates.md)。

### 脚本执行流程

```bash
# 1. 解析 itp + 识别残基区间
python3 scripts/detect_linkage.py --itp <input.itp> --pdb <complex.pdb>

# 2. 生成 rtp
python3 scripts/build_rtp.py --itp <input.itp> --linkage <type> --resname <name>

# 3. 生成 hdb
python3 scripts/build_hdb.py --itp <input.itp> --linkage <type>

# 4. 安装力场
python3 scripts/install_ff.py --rtp <name.rtp> --hdb <name.hdb> --ff-dir <amber14sb.ff>

# 5. 组装 PDB
python3 scripts/merge_pdb.py --pdb <complex.pdb> --residue-num <num> --resname <name>

# 6. 验证
python3 scripts/verify.py --ff-dir <amber14sb.ff> --resname <name>
```

每个脚本的详细用法见脚本内的 `--help` 说明。

## 完整示例（CYB 构建）

`examples/cyb/` 包含 CYB（BBO-10203 共价结合 CYS242）的**完整可运行示例**。

### 示例背景

- **体系**：KRAS-PI3Kα 信号通路
- **配体**：BBO-10203（共价抑制剂）
- **连接**：丙烯酰胺弹头与 CYS242 的 SG 发生迈克尔加成
- **残基名**：CYB
- **结果**：CYB 已成功用于 1 μs MD 模拟，体系稳定

### 快速运行

```bash
cd examples/cyb/
./run_all.sh --skip-download
```

### 分步运行

```bash
cd examples/cyb/

# 1. 下载力场（如已下载，跳过）
bash scripts/01_download_ff.sh

# 2. 复制输入文件
bash scripts/02_copy_inputs.sh

# 3. PDBFixer 补全缺失原子
bash scripts/03_fix_pdb.sh

# 4. 电荷计算（RESP2 + Amber 标准骨架 + 均摊调整）
python3 scripts/04_calc_charges.py

# 5. 生成 CYB.rtp 和 CYB.hdb
python3 scripts/05_generate_ff_files.py

# 6. 安装力场修改（rtp/hdb/residuetypes）
bash scripts/06_install_ff.sh

# 7. 添加 GAFF 参数到力场（atomtypes/LJ/键/角/二面体）
python3 scripts/07_add_gaff_params.py

# 8. 构建 RBD_CYB.pdb
python3 scripts/08_build_pdb.py

# 9. pdb2gmx 验证
bash scripts/09_run_pdb2gmx.sh

# 10. 全量验证
bash scripts/10_verify.sh
```

### 预期产物

| 文件 | 说明 | 预期内容 |
|------|------|----------|
| `CYB.rtp` | 残基定义 | 87 原子（52 重 + 35 H），总电荷 ≈ 0 |
| `CYB.hdb` | H 生成规则 | 22 条规则，方法码 1/3/4/6 分布 |
| `RBD_CYB.pdb` | 组装后 PDB | 1203 原子（CYB: 52 重原子） |
| `test.gro` | pdb2gmx 输出 | 坐标文件 |
| `test.top` | pdb2gmx 输出 | 拓扑文件 |

### 验证结果

运行 `scripts/10_verify.sh` 应该：
- ✓ CYB.rtp 首键含 `-C N`
- ✓ CYB 总电荷 ≈ 0（-0.000015）
- ✓ CYB.hdb 22 条规则
- ✓ pdb2gmx 成功
- ✓ 无 NaN 坐标

### 已知问题

1. **hdb 方法码瑕疵**：C24 的 sp³ CH 用了 method 3 而非标准 method 5，但对 MD 结果零影响
2. **脚本不完全幂等**：`07_add_gaff_params.py` 可能重复添加 dihedraltypes
3. **硬编码路径**：脚本中有部分硬编码路径，需要根据实际环境修改

### 与技能脚本的关系

| 位置 | 脚本 | 说明 |
|------|------|------|
| `examples/cyb/scripts/` | 10 步构建脚本 | **原始实战版**，经过 CYB 构建验证 |
| `nonstd-residue/scripts/` | 7 个 Python 脚本 | **技能通用版**，从头写的简化版 |

**建议**：验证技能脚本时，以 `examples/cyb/scripts/` 的输出为基准（golden files）。

详细说明见 [examples/cyb/README.md](examples/cyb/README.md)。
