---
name: gene-drug-automd
description: Plan and run gene/protein/PDB/mmCIF/AlphaFold 3 or nucleic-acid target workflows with small molecules using AutoDock Vina and GROMACS, including protocol recommendation, runtime estimates, system building, MD analysis, reports, and standalone Python reproduction scripts for EM/NVT/NPT/production/resume/analysis. Keep each study in a portable projects/project-name directory, parallel to the Skill by default or under a user-selected root, with absolute input/config/output paths and the required doctor, plan, run sequence. Classify missing or risky inputs as BLOCKER, CONFIRM or WARNING with corrective guidance. Use also for NVIDIA/AMD/Intel/Apple GPU, CUDA, WSL, GROMACS backend, multi-GPU, installation and repair tasks. Diagnose before changes; for installation, show the isolated directory, hardware-specific dry run and effects, obtain explicit approval, then validate the backend and real mdrun GPU evidence.
---

# GeneDrug-AutoMD Skill

## 适用场景

当用户希望提供“基因、蛋白质、PDB 或核酸三维结构 + 小分子药物名称”，自动完成结构解析、分子对接、GROMACS 分子动力学、轨迹分析和结果报告时使用。

示例：

> 靶点 EGFR，药物 Erlotinib，人，100 ns。自动下载结构、对接、模拟、分析并生成报告。

## 项目目录与三步调用

任何新任务都先完整读取 [references/project-layout.md](references/project-layout.md)，然后使用
`automd init-project` 创建项目。默认与 Skill 平行；也可让接收者选择绝对
`--projects-root`。项目不能创建在 Skill 内部：

```text
WORKSPACE/
├── GeneDrug-AutoMD-Skill/
└── projects/
    └── EGFR_erlotinib/
        ├── input/
        ├── config/
        │   └── project.yaml
        └── output/
```

执行：

```bash
python automd.py init-project EGFR_erlotinib \
  --target EGFR \
  --target-type protein \
  --ligand erlotinib \
  --projects-root "/absolute/path/chosen/by/user/projects"
```

本地 PDB/mmCIF、置信度和配体文件只放到该项目的 `input/`；项目 YAML 只放到
`config/`；所有运行结果只写入 `output/`。YAML 内这些路径必须是绝对路径。
不得把用户输入、配置、日志、轨迹或报告放进 Skill 源代码目录。

每次正式任务严格分三步，不能把 `plan` 省略：

1. `automd doctor --strict`：只检查环境。
2. `automd plan --config /绝对路径/config/project.yaml`：只检查项目布局、输入、方案和门禁。
3. `automd run --config /绝对路径/config/project.yaml`：仅在 doctor 通过、所有 `BLOCKER` 修正且所需确认完成后运行。

`plan` 和 `run` 必须使用项目 `config/` 下的配置文件。不得仅用零散命令行参数启动正式计算。
项目布局问题属于 `BLOCKER`，结构确认参数不能绕过。正式运行将项目审查写入
`output/00_input/project_review.json`。

## 执行前方案推荐与确认

当用户没有明确研究目的、PDB/链、突变、pH、口袋、重复数、MD 时长、硬件、截止时间或对照组时，不得直接把代码默认值当作用户的科学选择。先完整读取 [references/protocol-planning.md](references/protocol-planning.md)，然后：

1. 先区分技术试跑、初步筛查、投稿基线和机制研究；根据用户措辞推荐一个层级，并同时说明较低和较高层级的取舍。
2. 完全没有目的信息时，默认推荐“先做 3×10 ns 初筛、审查结果后再决定是否重建为 3×100 ns”，不得把 10 ns 描述为发表级或已收敛。
3. 用户出现“论文、发文、投稿、机制、收敛”等意图时，默认推荐至少 3 个独立 100 ns 重复，并根据假设提出 apo、突变体、已知抑制剂或阴性对照；不得承诺一定发表。
4. 先给出结构选择及理由、配体状态、对接验证、力场、水模型、EM/NVT/NPT 门禁、重复数、每条时长、分析项目和局限性。
5. 优先从同一硬件和相近体系的已完成 `mdrun` 日志提取 `ns/day`。按 `总生产期小时 = 体系数 × 重复数 × 每条 ns ÷ ns/day × 24` 计算，并单列准备、对接、建系、平衡、分析及 20%–50% 风险余量。没有基准时只给低置信区间，不得编造精确完成时间。
6. 明确列出所有假设、预计磁盘/计算量（可获得时）、可能触发的自动延长和停止条件。
7. 输出“推荐方案、备选方案、预计时间、推荐理由、尚需确认”五部分。用户没有明确要求立即运行时，在得到方案确认前不得启动 Vina、建系、平衡或 production MD。
8. 环境诊断是只读步骤；安装、升级、创建环境或改变驱动仍必须遵守后续安装授权规则。

## 安装授权与安全策略

这是必须遵守的最高优先级流程：

1. 第一次运行以及用户更换机器、环境或路径后，先执行：

```bash
automd doctor
```

2. 环境缺失时，先停止对接和 MD，并：
   - 列出缺失软件和用途；
   - 推荐安装根目录 `~/opt/gene-drug-automd` 和环境目录 `~/opt/gene-drug-automd/env`；
   - 允许用户选择其他可写目录，例如 `/data/<user>/gene-drug-automd`，但不得默认选择系统或管理员目录；
   - 检查候选目录是否存在、是否可写、是否已有环境，避免覆盖已有内容；
   - 展示将执行的包管理器、目标目录、完整命令和主要影响；
   - 询问用户选择哪个目录，以及是否授权助手执行这些命令。
3. 用户明确批准前，不得执行 `conda`、`mamba`、`micromamba`、`pip`、安装脚本或创建安装目录。
4. 用户明确批准目录和命令范围后，助手可以：
   - 创建已批准的用户级安装目录；
   - 使用现有的 Conda/Mamba/Micromamba 创建隔离环境；
   - 使用该隔离环境中的 Python 执行 `pip install -e .`；
   - 监控安装、处理非破坏性错误并报告进度；
   - 运行 `automd init-paths` 登记绝对路径；
   - 重新运行 `automd doctor --strict` 验证环境。
5. 未经单独、明确授权，不得使用 `sudo`、`apt`、`yum`、`dnf`、`brew`、系统 Python、`cmake --install`，不得修改 `~/.bashrc`、`~/.zshrc`、系统 PATH、登录脚本、module 配置或管理员目录。
6. 如果实际命令、包管理器、目标目录或权限范围与用户批准内容不同，必须暂停并重新询问。
7. 如果目标目录已存在且需要删除、覆盖或重建，必须先说明现状并取得单独确认；优先复用或创建新目录。
8. 只有 doctor 显示所有必需项通过后，才能执行 `automd run`。
9. 如果用户选择自定义目录，使用 `paths.json` 记录绝对路径；不得假设软件一定在 PATH。

## 环境检查入口

```bash
automd doctor
```

严格模式：

```bash
automd doctor --strict
```

使用用户路径配置：

```bash
automd doctor \
  --paths "$HOME/.config/gene-drug-automd/paths.json"
```

用户已经手动创建环境后，只登记路径：

```bash
automd init-paths \
  --prefix "$HOME/opt/gene-drug-automd/env" \
  --output "$HOME/.config/gene-drug-automd/paths.json"
```

`init-paths` 只扫描并写入路径配置，不安装软件。

## 安装协作流程

环境缺失时，按以下顺序与用户协作：

1. 展示 `doctor` 的缺失项。
2. 提供推荐目录和用户可选的自定义目录。
3. 检测操作系统、WSL、GPU 型号和现有 GROMACS 后端，询问用户选择 CPU 或 GPU 安装方案。
4. 根据服务器磁盘、写权限和已有环境帮助用户选择目录。
5. 展示将执行的完整命令和包管理器 dry-run 结果，不执行。
6. 获得用户对目录、硬件方案和命令的明确批准。
7. 在批准范围内安装并持续报告进度。
8. 登记路径并重新运行严格诊断。

如果用户希望自行安装，只提供命令并等待其完成；如果用户授权助手安装，则助手可按本节和安全策略参与执行。

详细安装说明见：

```text
environment/INSTALL_ENVIRONMENT.md
```

## GPU 安装与四层预检

配置、安装或修复 GPU 环境时，必须先完整读取 [references/gpu-environment.md](references/gpu-environment.md)。不得把“`nvidia-smi` 能看到显卡”直接解释为 GROMACS 可以使用 GPU。依次验证：

1. **硬件/驱动层**：识别每张 GPU 的厂商、运行时编号、型号、驱动版本和 compute capability，并记录 WSL 与 `CUDA_VISIBLE_DEVICES`。
2. **构建后端层**：解析 `gmx --version` 的 `GPU support`，记录 `CUDA`、`OpenCL`、`SYCL`、`HIP` 或禁用。
3. **运行时绑定层**：生成第一份真实 TPR 后运行零步探测；日志必须证明选中 GPU 并把短程非键计算映射到 GPU。
4. **实际任务层**：保存真实 `mdrun` 的设备/任务映射证据，最终报告以实际运行日志为准。

安装前必须让用户选择：

- **CPU/便携方案**：允许普通 GROMACS 构建，明确说明不会承诺 GPU 加速。
- **NVIDIA GPU 方案**：必须选择 CUDA 构建。不得只写无构建约束的 `gromacs>=2024`，因为求解器可能选择 OpenCL 变体。
- **AMD GPU 方案**：优先选择 AdaptiveCpp/ROCm SYCL；按 GROMACS 版本评估 HIP。不得安装 CUDA。
- **Intel GPU 方案**：选择 oneAPI SYCL。不得安装 CUDA。
- **Apple M 系列方案**：选择 OpenCL。不得安装 CUDA。
- **混合厂商/未识别方案**：先让用户明确选择目标设备或停止；不得猜测。

`environment.yml` 故意不安装 GROMACS。先建立基础环境，再按识别出的硬件选择精确 GROMACS 后端。当前环境被运行中任务占用时，不得原地更换包；先保留 checkpoint，并让用户批准停止/恢复或创建新环境。

NVIDIA Conda/Mamba 安装方案应先展示 dry-run，再请求批准。构建约束使用：

```bash
micromamba install -p "$ENV_PREFIX" -c conda-forge \
  "gromacs[version='>=2024',build='nompi_cuda*']" \
  --dry-run
```

用户批准 dry-run 显示的变更后，才移除 `--dry-run` 执行。安装后必须确认：

```bash
gmx --version
automd doctor --require-gpu --strict
```

对于 NVIDIA GPU，`gmx --version` 必须显示 `GPU support: CUDA`。OpenCL 构建不得用于 Volta 或更新的 NVIDIA GPU；在 WSL 中同样优先 CUDA。

WSL2 只使用 Windows 宿主 NVIDIA 驱动；不得在 WSL 内安装 Linux 显示驱动或 `cuda-drivers` 类元包。`--gpu auto` 的零步探测失败时，在正式 MD 前记录原因并切换 CPU；`--gpu on` 探测失败时立即停止。多卡服务器使用 `--gpu-id <运行时编号>` 明确选卡；存在 `CUDA_VISIBLE_DEVICES` 时按进程可见编号解释。不得把构建支持或零步探测成功单独写成“已使用 GPU”。

## 环境通过后的执行入口

```bash
automd plan \
  --config "$PROJECTS_ROOT/EGFR_erlotinib/config/project.yaml"
```

```bash
automd run \
  --config "$PROJECTS_ROOT/EGFR_erlotinib/config/project.yaml"
```

不得省略 `plan`，也不得使用相对配置或输出路径。

## 输入支持

### 蛋白质

支持：

- 基因符号；
- UniProt accession；
- PDB ID；
- 本地 PDB/ENT/CIF/mmCIF 文件；
- AlphaFold 2/3 本地输出。

基因符号先解析为 UniProt，再检索实验 PDB；无合适实验结构时才使用 AlphaFold DB。

### 本地结构输入审查与用户提醒

用户提供本地结构时，必须先完整读取
[references/structure-input-review.md](references/structure-input-review.md)，执行 `automd plan`，
并把所有问题连同处理建议展示给用户。不得先启动 Vina、体系构建或 MD。

问题分为：

- `BLOCKER`：文件缺失或为空、格式/解析失败、未识别到聚合物、结构来源未声明、模型编号越界、指定链不存在、mmCIF 链 ID 无法无损写入 PDB、预测结构仍启用共晶重对接、未处理的敏感金属。必须修正，`--acknowledge-structure-warnings` 不能绕过。
- `CONFIRM`：多模型选择、多链未选择、结构来源未声明、预测模型缺少置信度文件、预测模型没有明确口袋、预测结构含非聚合物坐标。必须逐项告诉用户影响和建议，用户人工复核后才可显式确认。
- `WARNING`：已自动找到置信度文件、实验结构配置了预测置信度文件等不会立即破坏运行但必须保留到报告的事项。

本地结构必须声明 `target.structure_source`：
`experimental`、`alphafold2`、`alphafold3`、`predicted` 或 `local_model`。
`auto` 只用于计划阶段发现问题；正式运行前必须改成明确来源，不能用确认参数代替。

预测结构中的配体、离子或其他 `HETATM` 坐标不是实验共晶证据。它们默认从受体中移除，
不得用于共晶配体重对接或宣称重对接验证成功。预测结构必须使用
`docking.redock_reference: false`；如需共晶重对接，另行提供实验结构。

AlphaFold 结构应提供 `target.confidence_file`，或把标准
`summary_confidences`/`confidences` JSON 放在结构同目录。缺少置信度文件时要求用户确认，
但即使文件存在，也必须人工检查结合口袋/界面附近的局部置信度、PAE 和 ipTM；不得仅凭全局分数认定结构适合对接。

所有正式运行都要把审查结果写入 `00_input/structure_review.json` 和 `manifest.json`。
用户确认 `CONFIRM` 项后，可设置：

```yaml
runtime:
  acknowledge_structure_warnings: true
```

或使用 `--acknowledge-structure-warnings`。确认只表示用户已复核风险，不表示模型正确或结果可发表。

### RNA/DNA

优先支持：

- 核酸 PDB ID；
- 用户提供的本地 RNA/DNA PDB/ENT/CIF/mmCIF 文件。

不得把任意基因名称臆造为可靠的核酸三维结构。找不到可信实验结构时停止并说明。

### 小分子

支持：

- PubChem 可识别名称；
- 本地 SDF、MOL2、MOL 或 SMILES 文件。

必须记录结构来源、PubChem CID、标准化 SMILES、净电荷及用户覆盖项。

## 自动流程

```text
环境检查 + GPU 硬件/构建后端检查
→ 缺失则显示安装目录与命令并询问用户
→ 用户选择 CPU/GPU 方案和目录并明确批准后，可由助手参与安装
→ 登记绝对路径并重新严格检查
→ 环境通过
→ 在动态默认或用户选择的 projects 根目录创建 <项目名>/input/config/output
→ 项目绝对路径和目录边界检查
→ 本地结构 BLOCKER/CONFIRM/WARNING 审查与用户提醒
→ UniProt/RCSB/AlphaFold/PubChem 解析
→ PDBFixer 受体处理
→ 用户口袋坐标 / 共晶配体 / fpocket
→ Meeko + AutoDock Vina 对接
→ antechamber + parmchk2 生成 GAFF2 参数
→ tleap 构建 AMBER 体系
→ ParmEd 转换为 GROMACS 拓扑
→ 第一份 TPR → 零步 GPU 运行时探测 → EM → NVT → NPT → production MD
→ PBC 修正
→ RMSD/RMSF/Rg/SASA/氢键/温度/压力/密度
→ PNG 图 + JSON 统计 + HTML/Markdown 报告
```

## 参数与执行规则

1. 用户提供的 PDB 优先于自动检索结构。
2. 蛋白靶点优先选择带共晶小分子且分辨率较好的实验 PDB；无合适实验结构时再使用 AlphaFold DB。
3. 结合口袋优先级：用户坐标 > 共晶配体 > fpocket > 全受体边界框兜底。
4. 默认力场路线：蛋白 ff14SB、DNA bsc1、RNA OL3、配体 GAFF2/AM1-BCC、水 TIP3P。
5. 不得使用 `gmx grompp -maxwarn` 掩盖拓扑或参数错误。
6. 不得依赖 GROMACS 默认交互组号；应使用工作流生成的命名索引组。
7. `runtime.gpu=auto` 时，只有硬件可见、GROMACS 后端兼容且零步运行时探测有设备与任务映射证据后才启用 GPU；否则在正式 MD 前记录原因并使用 CPU。
8. 用户明确设置 `--gpu on` 时，硬件、构建后端、零步绑定或实际 `mdrun` 证据任一不满足都必须停止，不得静默改用 CPU；多卡时保存 `runtime.gpu_id`。
9. 只有外部命令返回成功、日志满足完成条件且输出文件有效时，才能说该阶段完成。
10. Vina 分数只用于姿势排序，不得解释为实验亲和力或严格结合自由能。
11. 单条稳定轨迹不能证明生物学有效性、选择性或完全收敛；报告必须保留局限性。

## 自动停止条件

- 环境 doctor 未通过；
- 项目不在当前机器配置的 projects 根目录；
- 输入、配置或输出不是绝对路径，或位于对应项目子目录之外；
- 本地结构审查存在任一 `BLOCKER`；
- 本地结构存在 `CONFIRM` 项但用户尚未明确确认；
- 核酸名称找不到可信实验三维结构；
- 配体净电荷或质子化状态无法可靠确定；
- 关键金属中心没有专门参数方案；
- 检测到共价抑制剂或共价连接；
- 膜蛋白、复杂糖基化或非标准残基缺少专门流程；
- `tleap check`、`gmx grompp` 或能量最小化失败；
- 出现 LINCS warning；
- 生产期轨迹不存在或模拟没有正常结束。

## 结果目录

```text
00_input/
  project_review.json
01_target/
02_ligand/
03_receptor/
04_docking/
05_system/
06_md/
  reproduce/
    run_em.py
    run_nvt.py
    run_npt.py
    run_production_md.py
    resume_md.py
    run_analysis.py
    run_all.py
    common.py
    bundle_manifest.json
    commands.jsonl
    environment.json
    README.md
07_analysis/
08_report/
logs/
state.json
manifest.json
preflight.json
```

最终报告至少包含：

- 实际使用的软件路径和版本；
- 所选结构、链和结构来源；
- PubChem CID、配体净电荷；
- 口袋来源和对接盒坐标；
- Vina 最佳姿势排序分数；
- 力场和水模型；
- 请求与实际完成的 MD 时长；
- GPU/CPU 使用情况；
- 警告与科学局限；
- `report.html` 和 `REPORT.md` 路径。

### 独立 Python 复现脚本

正式 MD 开始前必须在 `06_md/reproduce/` 生成独立脚本和完整的相对路径输入。
生成失败时停止，不得只完成轨迹而缺失复现包。

1. `run_em.py`、`run_nvt.py`、`run_npt.py` 和 `run_production_md.py` 分阶段运行；
   `run_all.py` 按 EM → NVT → NPT → production 顺序运行。
2. `resume_md.py` 只在 `.tpr` 与 `.cpt` 同时存在时使用 `-cpi ... -append` 恢复，
   已完成轨迹默认跳过。
3. `run_analysis.py` 重新生成 PBC 修正轨迹和核心 XVG 指标；分析失败项必须记录，
   不得生成虚假占位结果。
4. 脚本必须从自身位置解析 `06_md` 和 `07_analysis`，不得嵌入发布者或原机器的
   用户名、IP、盘符和项目绝对路径。
5. `--gpu on` 延续正式流程的 GPU 强制门禁；`--gpu auto` 只允许在生产期开始前
   选择 CPU；`--gpu-id` 选择单卡。
6. 默认不得覆盖现有输出；`--force` 必须先移动到 `reproduce_archive/`。
7. 每条独立脚本执行的命令、工作目录、时间和返回码写入 `commands.jsonl`；
   `environment.json` 只记录原始环境证据，不作为新机器的硬编码配置。
8. 修改 MD 参数后必须重新运行正式 `automd run` 生成匹配的 MDP、清单和脚本，
   不得只手工编辑脚本造成配置与报告不一致。

已有完整 `06_md` 输入但缺少复现包时，使用以下命令补生成；该命令不运行
GROMACS，也不重新计算轨迹：

```bash
automd export-reproduction --config /当前机器/项目/config/project.yaml
```

## 科学验证与自动门禁

本流程必须执行以下检查，不能只生成文件后默认成功：

1. 配体在 `pH ± ph_tolerance` 内用 Dimorphite-DL 枚举质子化状态，并用 RDKit 枚举互变异构体。状态总数受配置上限约束；用户指定净电荷时，只保留匹配状态。不同状态间的 Vina 分数比较只是启发式排序，不代表状态布居或自由能。
2. 每个配体状态默认执行 3 次不同随机种子的 Vina 对接，保存全部运行、分数范围和最终所选状态。
3. 实验结构存在合适共晶配体时，必须在相同受体、口袋和协议下进行重对接。默认要求全局最高排名姿势的受体坐标系重原子 RMSD 不超过 2.0 Å；不得先单独拟合配体再计算 RMSD。没有共晶配体时明确记录“不可验证”，不得写成验证通过。
4. ParmEd 生成 GROMACS 拓扑后，为每个受体分子类型及 `LIG` 的重原子写入条件式位置限制。NVT/NPT 的 MDP 必须同时定义受体和配体限制宏，`grompp` 必须传入 `-r`；NPT 使用 `refcoord-scaling = all`。
5. 能量最小化日志必须解析实际 `Maximum force`。数值高于 `em_max_force_kj_mol_nm`、日志明确未收敛或无法解析时立即停止。
6. NVT 检查最终窗口温度均值及漂移；NPT 检查温度、压力和密度漂移。未通过时按配置限次延长相应平衡段；达到上限仍未通过则不启动生产期。
7. 默认执行 3 个独立速度种子的 MD 重复，每个重复独立完成 NVT、NPT 和生产期。输出按 `06_md/replicate_XX` 和 `07_analysis/replicate_XX` 分开保存。
8. 默认 10 ns 只代表每个重复的最低采样长度，不自动证明收敛。只有重复数、每条时长、末半程 RMSD 斜率及重复间 RMSD 离散度全部满足预先配置的阈值时，报告才可写 `configured_criteria_met`；措辞必须是“满足配置的诊断标准”，不得写成“已证明绝对收敛”。
9. 受体缺失残基只允许自动补建有两端结构约束、且长度不超过 `target.max_modeled_gap_residues` 的内部缺口。末端缺失或超过上限的内部缺口不得静默补建，必须保留为未解析并写入报告；所有补建环区都必须标记为需要结构审查。

如需降低计算量，必须让用户明确修改 `docking.repeats`、`simulation.replicates` 或枚举上限，并在报告中保留由此产生的验证局限。不得为了完成任务而静默跳过门禁。
