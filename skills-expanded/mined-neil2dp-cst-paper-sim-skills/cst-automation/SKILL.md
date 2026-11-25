---
name: cst-automation
description: CST仿真工作流的总入口和路由器。接到CST相关请求后判断意图，分发给正确的子skill执行——建模执行委托cst-em-sim，设置规范委托cst-modeling-guide，视觉自查自己保留。本skill不再包含执行代码，只做编排。触发词：CST仿真、CST建模、帮我建模仿真、跑CST、参数化建模、扫参、帮我写CST脚本、视觉自查、模型截图对比。
---

# CST 仿真工作流 · 路由器

## 你是什么

你是 CST 仿真工作流的**总入口和路由器**。用户说"帮我做个 CST 仿真"时，你第一个被触发，负责：

1. **判断用户意图**（是要建模执行？还是问设置规范？还是视觉验证？）
2. **分发给正确的子 skill**（见下方路由表）
3. **自己保留三项独有能力**：model_spec.yaml 输入格式、vision.js 视觉自查、项目脚手架模板

> ⚠️ **本 skill 不再包含 CST 执行代码**。真正调 API 建模/求解/导出的代码在 `cst-em-sim`（`scripts/cst_runner.py`），规范决策在 `cst-modeling-guide`。这里只做编排和路由。

---

## 路由决策表

| 用户意图 | 委托给 | 关键词信号 |
|---------|--------|-----------|
| **真正建几何、设端口、跑求解器、导结果** | `cst-em-sim` | "建模""执行""跑仿真""导出S参数""建brick""跑求解器""导入STEP""求解器报错""CSTRunner" |
| **问求解器选型、网格怎么设、边界怎么设、端口选哪种** | `cst-modeling-guide` | "求解器选型""时域还是频域""网格设多少""边界条件""端口类型""检查模型""远场图为空""S11全0dB" |
| **建模后截图对比论文图、视觉自查** | **自己做**（见下方"视觉自查"） | "视觉自查""模型截图""对比论文图""看看模型对不对" |
| **扫参/批量仿真** | `cst-em-sim`（执行）+ 自己（场景识别+夜间提醒） | "扫参""扫频""批量""参数扫描" |
| **论文复现（全流程 Phase1-6）** | `em-simulation-pipeline`（总编排） | "复现论文""照着论文建模""验证论文结果" |
| **仿真结果整理汇总/作图/图文汇报** | `cst-result-report` | "整理结果""汇总""出报告""结果作图""图文并茂""验收汇报""复现对照""和论文对照""结果可以看了吗" |

### 典型调用链示例

用户："帮我复现这篇 ME dipole 天线论文并扫参"

```
cst-automation（路由器）
  ├→ em-simulation-pipeline（全流程总编排 Phase1-6）
  │    ├→ paper-parser（Phase1 提取参数 → model_spec.yaml）
  │    ├→ paper-formula-falsify（Phase1.5 公式预扫雷）
  │    ├→ cst-modeling-guide（Phase3 求解器选型 + 网格建议 + 检查清单）
  │    ├→ cst-em-sim（Phase3 调 cst_runner.py 建模、求解、导出）
  │    └→ cst-automation（Phase3 视觉自查 vision.js 截图对比）
  └→ cst-em-sim（Phase6 扫参执行 + 夜间运行）
```

---

## ★ CST 开工纪律 · 独占使用防冲突（硬约定）

**本机 CST 同一时刻只允许一条自动化链。开工前必查冲突，收尾必清场——两者配对，缺一不可。**

1. **开工前必查占用**（任何 CST 任务的第一步）：
   ```powershell
   Get-Process | Where-Object { $_.Name -like 'CST*' } | Select-Object Id, Name, StartTime, CPU
   ```
   发现 `CST DESIGN ENVIRONMENT` 或求解器进程且**不是本会话启动的**，先分清是谁的再动手：
   - **另一条 agent 会话/后台任务在跑 CST**（多项目并行时常见）→ **排队等它收尾**，绝不并行启动第二条 DE 链——多实例会导致 COM 路由混乱、内存互踩（cst-em-sim 坑 4、坑 12）；
   - **用户手动开着的 CST GUI** → **停手问用户**，绝不接管连接，收尾时也绝不能 `cleanup_cst()` 误杀用户窗口；
   - 常驻后台服务（`cstd` / `CSTDCMainController` / `CSTDCSolverServer`，无活动 CPU）不算占用，无需处理。
   - ⚠️ **判归属看证据，不靠猜**（2026-08-28 远场导出实测事故）：只看进程名就断定"是我的残留僵尸"会误杀并行会话的 DE。判据：① 进程 `StartTime` 是否落在**自己会话的活动时间窗**内；② 是否存在工作锁文件（锁被谁持有）；③ 两者都对不上 → 当成别人的，排队或问用户。**不确定 = 不杀**。
2. **写工作锁**：确认无冲突后在 CST 项目根写 `.cst_autolock.json`（字段：`pid`、`project`、`task`、`started_at`），收尾 `cleanup_cst()` 时删除。后到会话见锁：锁内 **PID 有效且活着 → 排队等待**；PID 已死或字段无效 → 需**同时核对锁的写入时间**（<30 分钟且 pid 缺失/无效 = 写锁方可能还在跑，只是锁写得有 bug——**按活锁对待去问，不要直接清**；>30 分钟才算陈旧锁可清理）。2026-08-28 实测：并行会话写过 `pid: None` 的锁，被误清后引发双会话 DE 争用。
3. **一个 `.cst` 工程同时只能被一个会话打开**：工程目录被锁（`Model.lok` 残留 / open 失败）→ 复制 `.cst` 到隔离目录操作，不硬写、不双开。
4. **跨机委托同理**：委托远程节点跑 CST 时，本地先清场、工程文件传完再让对方开工；同一工程本地与远程绝不同时打开。

---

## ★ CST 收尾纪律（硬约定，2026-08-12 制定；2026-08-15 增补第 3 条）

**每个 CST 仿真任务完毕后必须做三件事，不可遗漏：**

1. **关闭 CST 窗口** — 求解 + 导出 + SaveAs 全部完成后、脚本退出前，调用 `cleanup_cst()`（项目 `cst_config.py`）关闭所有 CST* 进程。
   - 原因：`de.close()` 只断 COM 连接，**不关 CST 界面**；多次求解会积累多个 CST DESIGN ENVIRONMENT 进程（COM 路由混乱、占资源、界面残留——本机实测 4 次求解后残留 5 个 DE 进程）。
   - 实现：PowerShell `Get-Process | Where-Object { $_.Name -like 'CST*' } | Stop-Process -Force`。
   - ⚠️ 会一并关闭用户手动开的 CST 窗口——自动化跑 CST 时不应同时手动操作 CST。

2. **简洁汇报** — 任务汇报只给**产出文件路径和文件名**（如 `results/farfield.csv`、`results/synthesis_result.json`），不要长篇叙述 CST 建模/求解过程。汇报末尾附一个**结果状态标签**（见下节）。

3. **图文汇报文件**（2026-08-15 增补）— 一批仿真（多变体/扫参/归属实验）跑完后，委托 `cst-result-report`
   产出图文并茂的验收汇报：指标表 + 分组对比图 + 论文对照拼接图 + `仿真结果汇总_<任务>_YYYYMMDD.md`。
   - 标准产物结构和工作流见 `~/.zcode/skills/cst-result-report/SKILL.md`（含三个实测可跑的模板脚本）。
   - 单次小求解（单个工程、无对比需求）可降级为：一张对比图 + 指标表，但**不许只交 txt**。

**执行脚本末尾标准收尾**（所有 CST 脚本必须遵守）：
```python
from cst_config import cleanup_cst
# ... 求解、导出、SaveAs 完成后 ...
cleanup_cst()                       # 关闭 CST 窗口
print(">>> 产出：results/xxx.csv")  # 简洁汇报路径
# 委托 cst-result-report 生成图文汇报（多变体/扫参批次必做）
```

> 本规则同步写入 `cst-em-sim` 工作流第 10 步；新建项目的 `cst_config.py` 必须含 `cleanup_cst()` 函数（见脚手架模板）。

---

## ★ 结果状态标签（2026-08-16 借鉴外部 cst-simulation skill）

**`.cst` 工程文件只是模型，不是证明。** 一个结果只有满足"目标几何已重建 + 端口/模式确认 + 求解器成功完成 + 真实导出数据/日志在手"才算验证。每次 CST 任务汇报**末尾必须附一个状态标签**，禁止把"建好了模型"说成"仿真完成了"：

| 标签 | 含义 |
|------|------|
| `template` | 可复用模板工程，无当前求解证据 |
| `model-built-not-solved` | 当前几何已建，求解器未完成 |
| `solver-failed` | 求解器运行了但失败 |
| `export-failed` | 求解完成但导出数据缺失/无效 |
| `CST-incomplete` | 建/解/导证据链不完整 |
| `CST-validated` | 几何 + 端口 + 求解 + 日志 + 导出全过验收检查 |
| `CST-regressed` | 本次完整求解比此前已完成的权威结果更差 |

使用规则：
- **扫参排名只认有真实导出的曲线**：非收敛/无导出的结果只能标记诊断用途，不得参与变体排名。
- **`CST-regressed` 专用于扫参/优化**：新算完的点若差于历史已完成最优点，如实标退步，不许只挑好看的汇报。
- **缺 CST 导出数据时如实说"对比 pending"**，绝不拿解析公式/电路级/插值曲线补位冒充 CST 结果。

---

## 你保留的三项独有能力

### 1. model_spec.yaml — CST 建模的标准输入格式

这是整个 CST 工作流的**标准入参契约**。paper-parser 产出它，cst-em-sim 消费它。

```yaml
# model_spec.yaml — 示例
project_name: ME_dipole_AWPL2024
source_paper:
  title: "..."
  doi: "..."
  authors: ["..."]

geometry:
  units: mm
  layers:
    - name: substrate
      material: RT5880
      thickness: 3.18
      # ...
  dimensions:
    patch_width: 14.0
    patch_length: 11.0
    # 变量名驱动，方便后续扫参

excitation:
  port_type: waveguide  # waveguide | discrete
  # ...

solver:
  type: time_domain     # time_domain | frequency_domain
  freq_range: [2, 8]    # GHz
  mesh_lines_per_wavelength: 15
  # ...

benchmarks:            # 论文声称的结果值（用于 em-verification 对比）
  resonant_freq_GHz: [3.5, 5.2]
  peak_gain_dBi: 5.3
  s11_min_dB: -35

vision_extractions:    # vision.js 从论文图提取的信息
  structure: "..."
  dimensions: "..."
```

> **必填字段**：几何参数（每层材料/尺寸/单位）、激励/边界条件、求解器设置、结果指标、隐式假设。

### 2. vision.js 视觉自查 — 建模后的视觉验证

建模完成后、求解之前，增加视觉验证环节。**这是本 skill 的招牌能力，其他 skill 没有。**

#### Step 1：CST 截图
在 CST GUI 中截取：
- **全貌图**：3D 视图，显示所有几何体
- **侧视图**：检查层叠是否正确
- **俯视图**：检查贴片/结构形状
- **端口特写**：确认端口位置和方向

#### Step 2：vision.js 对比
> 路径坑（2026-08-15 实测）：vision.js（Node.js）不认 Git Bash 风格路径——`/c/Temp/x.png` 会被解析成 `C:\c\Temp\x.png`。传参一律用 `C:/Temp/x.png` 或 `C:\\Temp\\x.png` 风格。
```bash
# 对比 CST 模型全貌 vs 论文结构图
node ~/.zcode/skills/vision/vision.js "cst_model_3d.png" "对比CST模型和论文图1的天线结构：天线形状、馈线位置、基板比例是否一致"

# 对比端口位置
node ~/.zcode/skills/vision/vision.js "cst_port_detail.png" "检查端口位置：馈电点是否在天线边缘正确位置，与论文中的馈电示意图是否一致"

# 检查层叠
node ~/.zcode/skills/vision/vision.js "cst_side_view.png" "检查介质层叠：基板厚度、金属层厚度、地平面位置是否正确"
```

#### Step 3：结果判定
- ✅ **视觉一致** → 进入求解
- ⚠️ **有小差异** → 记录差异，人工判断是否可接受
- ❌ **明显不同** → 修改建模脚本，重建后重新截图验证

> 建模后一定要视觉自查：几何 Bug（Brick Z 范围重叠、端口放反了）肉眼看一眼就发现，比跑两小时仿真后才发现快得多。

### 3. 项目脚手架模板 — 新项目的推荐结构

```
project/
├── cst_config.py            # CST连接助手（委托 cst-em-sim 的连接逻辑）
├── model_spec.yaml          # 模型参数（本 skill 定义的格式）
├── screenshots/             # 视觉自查截图（本 skill 的 vision.js 流程产物）
│   ├── cst_3d_view.png
│   ├── cst_side_view.png
│   └── cst_top_view.png
├── cst/                     # 建模执行代码（委托 cst-em-sim 的 cst_runner.py 风格）
│   ├── cst_controller.py
│   ├── model_builder.py
│   ├── solver_setup.py
│   └── result_exporter.py
└── results/                 # 仿真输出
    ├── s_params.csv
    ├── farfield.csv
    └── cst_results.json
```

---

## 扫参场景识别

用户说"扫参"时，你负责**场景识别和提醒**，执行委托给 `cst-em-sim`：

- 识别扫参维度（扫贴片宽度？扫频率？扫间距？）
- 提醒"大批量扫参建议夜间跑"（遵守 AGENTS.md 作息规约）
- 委托 cst-em-sim 的 `CSTRunner` 执行参数化循环
- 结果交给 em-verification 做偏差分析

---

## 环境（参考，实际执行细节见 cst-em-sim）

- **CST 安装**：`<CST安装目录>`
- **CST Python**：`<CST安装目录>\AMD64\python\Scripts\python.exe`（3.9.15）
- **API 包**：`<CST安装目录>\AMD64\python_cst_libraries\cst\`
- **环境变量**：`CST_INSTALLPATH_2025`=`<CST安装目录>`
- **连接脚本**：各项目根目录 `cst_config.py`（连接逻辑详见 cst-em-sim）

---

## 与其他 skill 的关系（一张图）

```
                    ┌─────────────────────┐
                    │   cst-automation    │  ← 你在这里（路由器）
                    │   路由 + 视觉自查    │
                    │   + model_spec格式  │
                    └──┬──────┬───────┬───┘
                       │      │       │ 结果整理汇总/图文汇报
        建模执行/求解/导出│      │设置规范 │（收尾纪律第3条）
                       ▼      ▼       ▼
          ┌────────────────┐ ┌─────────────────────┐ ┌──────────────────┐
          │   cst-em-sim   │ │ cst-modeling-guide  │ │ cst-result-report│
          │ 执行引擎       │ │ 规范顾问            │ │ 验收汇报         │
          │ cst_runner.py  │ │ 决策树+检查清单     │ │ 指标表+对比图    │
          │ 7大实测坑      │ │ 错误修复表          │ │ 论文对照+md汇报  │
          └────────────────┘ └─────────────────────┘ └──────────────────┘
```

| skill | 角色 | 核心资产 |
|-------|------|---------|
| **cst-automation**（本skill） | 路由器 + 视觉自查 | model_spec.yaml 格式、vision.js 流程、项目脚手架 |
| **cst-em-sim** | 执行引擎 | cst_runner.py（CSTRunner类）、场监视器套件、5个references、17大实测坑 |
| **cst-modeling-guide** | 规范顾问 | 求解器决策树、网格/端口/边界规范、检查清单、错误表 |
| **cst-result-report** | 验收汇报 | analyze_s11.py / plot_report.py / paper_compare.py 三模板、report_template.md |

---

## 远程委托参考（可选：把求解委托给另一台 Windows 机器）

本机资源紧张或需要并行时，可把「打开工程→求解→导出」整段委托给局域网内另一台装了 CST 的
Windows 机器（要求：OpenSSH 服务端 + 同版本 CST）。通用载荷在本 skill `scripts/remote/`：

- `run_remote_cst.py` — 委托载荷：quiet 模式打开工程 → `run_solver()` 同步求解 →
  按导出清单逐条导出（S 参数 ASCII / 远场 .ffd / 3D 场点云，cst-em-sim 坑 13/14/17 路线全内置）
  → 写 `_remote_done.flag` 完成标记（status/elapsed/exported JSON）。新机器首跑传
  `--cstroot "<CST安装目录>"` 免探测（也支持 `C:\ProgramData\cst_probe.json` 探测约定）。
- `spawn_detached.py` — 长任务点火器：Windows OpenSSH 会把会话内子进程放进 kill-on-close
  的 Job 对象（ssh 一断全连坐杀掉，Start-Process/DETACHED_PROCESS 都救不了），本脚本用
  `CREATE_BREAKAWAY_FROM_JOB` 生成真正脱离会话的工作进程，stdout/stderr 落
  `_remote_run.log/.err`。

标准流程：

```bash
# 1. 推工程 + 载荷（目标机工作目录用纯 ASCII 路径，如 C:/CST_Remote/<proj>/）
scp -r <工程目录> <host>:C:/CST_Remote/<proj>/
scp run_remote_cst.py <host>:C:/CST_Remote/<proj>/

# 2a. 短任务（<10min）：ssh 前台直接跑（<py> = 目标机 Python 3.8-3.12 或 CST 自带 Python）
ssh <host> "& '<py>' 'C:\CST_Remote\<proj>\run_remote_cst.py' --cst x.cst [--cstroot <CST安装目录>]"

# 2b. 长任务（>10min）：点火器脱离 SSH Job，防断线连坐杀
scp spawn_detached.py <host>:C:/CST_Remote/<proj>/
ssh <host> "& '<py>' 'C:\CST_Remote\<proj>\spawn_detached.py' --solve td"

# 3. 轮询（独立短命令，不挂长连接；判死法：远程 Get-Process 看 DE 的 TotalProcessorTime 5 秒零增量）
ssh <host> "type C:\CST_Remote\<proj>\_remote_done.flag & type C:\CST_Remote\<proj>\_remote_run.log"

# 4. 回流结果
scp -r <host>:C:/CST_Remote/<proj>/Export_remote ./<项目>/results_remote/
```

- **自定义导出清单**：`--exports exports.json`，格式
  `[{"tree":"1D Results\\S-Parameters\\S1,1","out":"s11.txt","mode":"ascii"},
  {"tree":"Farfields\\farfield (f=11.4) [1]","out":"ff.ffd","mode":"ffd"},
  {"walk":"2D/3D Results","step":1.0,"mode":"field"}]`
  ——`ascii`=1D 树数据；`ffd`=全 3D 远场（无头唯一可靠路线，绝不调 `.Plot`）；`field`=3D 场点云
  （`step` 采样步宽 mm **必填**，缺失=零数据；`walk` 哨兵自动枚举 E-Field/H-Field/Power Flow 叶子，
  叶子名带 `[N]` 运行号后缀必须枚举拿真名）。缺省 auto = S1,1 + 全部远场切面。
- **纪律不变**：远程机同样遵守「开工纪律」（同工程不双开、杀进程前判归属）；长任务跨时段时
  确保目标机电源计划不睡眠（`powercfg /change standby-timeout-ac 0`）。
