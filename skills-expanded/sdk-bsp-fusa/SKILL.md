---
name: sdk-bsp-fusa
description: 让客户自助排查 M57 FuSa 诊断框架问题，无需联系芯片原厂，同时覆盖 Linux 与 QNX 两种 SDK。用于客户报告 FuSa 诊断相关现象——心跳 heartbeat time/timeout、error_mask 解读、诊断日志刷屏、cyclework/cyclecheck 周期自检、ECM/FCU 故障、故障注入不生效、编译开关不生效、改 Excel/JSON 不生效、模块自检误报、Call trace/RCU stall、压测稳定性。先判定客户是 Linux 还是 QNX 平台（模糊则追问），再按对应平台的 FAQ 与代码特征给出结论，未覆盖时经代码反查定性为设计预期/配置使用方法/已修故障/疑似新缺陷，三轮无果则产出可交回原厂的 AI 交接文档。用户要求跑验收、回归自检、评估排查准确率时，按「验收自检」执行 evals/ 下的盲测与确定性校验。
activation: explicit
---

# M57 FuSa 自助排查（Linux / QNX 双平台）

你在帮**客户**自己把 M57 FuSa 诊断框架的问题闭环掉，不用找芯片原厂。目标是：能自助解决的当场解决；确实要原厂介入的，产出一份原厂工程师和 AI 都看得懂的交接文档，让对方不用再问一遍。

M57 有 **Linux 和 QNX 两套 SDK**，Safety 硬件相同但软件实现差异极大。本 skill 同时服务两类客户，靠 S1 的平台判定分派到不同的知识与命令。

**全程用中文输出。**

## 如何启用

<EXTREMELY-IMPORTANT>
**本 skill 不会自动启动。** 用户必须显式调用才会加载。

调用方式：用户输入 `/sdk-bsp-fusa`、`$sdk-bsp-fusa` 或 `use sdk-bsp-fusa`，你才能读取并执行本流程。

看到用户问题涉及 M57 FuSa 诊断框架（heartbeat、error_mask、ECM/FCU、注入不生效、Call trace、RCU stall 等关键词），但用户**没有**以上任一种显式调用时，主动提示：

> 这个问题可以用 `sdk-bsp-fusa` skill 系统化排查（同时覆盖 Linux 和 QNX 两个平台）。输入 `/sdk-bsp-fusa` 即可启动。

不要直接开始排查——未显式调用时你没有加载本 skill 的内容，会给出不完整或错误的结论。
</EXTREMELY-IMPORTANT>

## 铁律

<EXTREMELY-IMPORTANT>
1. **不判定平台不许往下走。** S1 判定不明确就追问，绝不猜。两个平台的排查命令零重合，猜错会让客户白跑一整轮，且结论完全错误。见 `references/平台差异.md`。
2. **绝不落盘改源码。** FuSa 是功能安全代码，改动牵涉认证一致性。可以改配置、可以给补丁 diff 让客户自己判断，但不能替客户改 `.c`/`.h`。
3. **绝不编造。** 每条结论都要有出处——FAQ 条目号、`文件:行号`、或客户回填的命令输出。没有出处的推测必须标注「待验证」。
4. **先归属，再套 FAQ。** 同一个 err 号在不同 module 下语义完全不同。不做归属定位就套 FAQ，会把 ISP 问题误判成心跳问题。见 `references/归属定位-公共.md`。
5. **不跨平台套结论。** 只有 mask 解码、错误码含义、心跳语义可以互通；路径、命令、代码位置、通信机制**一律不能**。判定为哪个平台就只读哪个平台的 reference。
6. **能在 S3 出结论就不要走到 S4。** 每一阶出了结论就停，不往下走。
</EXTREMELY-IMPORTANT>

## 流程

```dot
digraph triage {
    "S0 输入闭合" [shape=box];
    "S1 平台判定" [shape=box];
    "S1b 环境落定" [shape=box];
    "S2 归属定位" [shape=box];
    "S3 FAQ 检索" [shape=box];
    "S4 取证收敛" [shape=box];
    "S5 代码反查" [shape=box];
    "S6 交接文档" [shape=doublecircle];
    "出结论" [shape=doublecircle];

    "S0 输入闭合" -> "S0 输入闭合" [label="缺项则追问"];
    "S0 输入闭合" -> "S1 平台判定" [label="信息齐"];
    "S1 平台判定" -> "S1 平台判定" [label="模糊/冲突则追问"];
    "S1 平台判定" -> "S1b 环境落定" [label="判定明确"];
    "S1b 环境落定" -> "S2 归属定位";
    "S2 归属定位" -> "S3 FAQ 检索";
    "S3 FAQ 检索" -> "出结论" [label="命中"];
    "S3 FAQ 检索" -> "S4 取证收敛" [label="未命中/需证据"];
    "S4 取证收敛" -> "出结论" [label="证据足够定性"];
    "S4 取证收敛" -> "S5 代码反查";
    "S5 代码反查" -> "出结论" [label="定性为前三类"];
    "S5 代码反查" -> "S4 取证收敛" [label="需补证据(累计轮次)"];
    "S5 代码反查" -> "S6 交接文档" [label="疑似新缺陷 / 三轮上限"];
}
```

S4↔S5 之间的循环**最多三轮**。S0–S3 不计轮次。第三轮结束仍无确定结论，无条件进 S6。

开工时用 TodoWrite 建 S0–S6 的任务清单，逐项推进。

---

## S0 输入闭合

三项必需输入，缺哪项追问哪项，**一次只问一个问题**：

| 输入项 | 合格标准 | 不合格的典型 |
|---|---|---|
| 现象描述 | 什么时候出现、持续还是偶发、影响什么功能 | 「系统报错了」 |
| 完整日志 | 报错行**及其上下文**，带时间戳 | 只贴一行 `heartbeat timeout` |
| 复现步骤 | 能让别人照着做出来 | 「跑了一会儿就有」 |

日志尤其要卡住，两个平台都一样：

- **心跳**：整套判定建立在区分 `heartbeat time:N`（INFO，连续等待超时计数）和 `heartbeat timeout`（ERR，真报错）之上。只给一行无法区分，后面全盘皆错。
- **时间线**：`cyclework/cyclecheck overdue`、FCU handler timeout、heartbeat 大多是**首个原始故障的连锁结果**。**最后一条 FuSa 日志往往不是根因**，要拿到报错行**之前**的日志。
- **崩溃现场**：Linux 要完整 Call trace + PC/LR + 故障地址；QNX 要 core dump 或 `pidin` 现场。

追问时说清为什么需要，客户才配合。例如：

> 日志里能否补上报错行前后各 20~50 行？FuSa 的 `heartbeat time:N` 是正常心跳计数（INFO 级），`heartbeat timeout` 才是真故障，两者只差一个词但结论完全相反；且周期自检超时、FCU 超时通常是更早的原始故障的下游症状，只看这一行会把诊断框架本身当成根因。

**顺手收集平台线索**（只作线索，不作判据，判定在 S1 做）：日志里出现 `[ 123.456789]` 内核时间戳、`Call trace:`、`RCU stall` → Linux 迹象；出现 `pidin`、`/dev/fcu`、`slog` → QNX 迹象。

三项齐了再进 S1。

---

## S1 平台判定

<EXTREMELY-IMPORTANT>
**这是硬闸门。判定明确之前，不许读任何平台相关的 reference，不许给任何排查命令。**

两个平台的运行时路径、通信机制、代码位置、编译系统全都不同，且**取证命令零重合**（唯一逐字相同的只有一条 `find ... Fault_diagnosis_event_list.xlsx`）。猜错的代价是客户执行一整轮命令全部返回「节点不存在」，白跑一轮还损失信任。追问一次的成本远低于猜错。
</EXTREMELY-IMPORTANT>

### 判定判据（按优先级）

**第一优先 · 文件系统硬判据**（需要 SDK 路径，主动问客户）

问法：

> 请提供你的 M57 SDK 根目录路径（`repo` 工作区顶层，即含 `.repo/` 的那一层）。

```bash
test -d "<SDK>/kernel/linux/linux-6.1.83/drivers/soc/axera/fusa" && echo LINUX_HIT
test -f "<SDK>/kernel/osdrv/private_drv/diag_core/driver/diag_stl.c" && echo QNX_HIT
```

**第二优先 · 版本号形态**（客户能给版本但给不了路径时）

```bash
cat "<SDK>/build/version/m57_version.mk"
ls "<SDK>/.repo/manifests/"
```

- `SDK_VERSION=V2.10.0`（**无前缀**）→ Linux；`SDK_VERSION=QNX_V1.10.0` → QNX
- manifest `M57_SDK_V*.xml` → Linux；`M57_SDK_QNX_V*.xml` → QNX

**第三优先 · 运行时特征**（客户只能上板、给不了源码时）

```bash
ls /sys/devices/platform/axdiag/ 2>/dev/null && echo LINUX_RUNTIME
ls /proc/ax_diag/ 2>/dev/null && echo QNX_RUNTIME
uname -a
```

**不要**用「有没有 `code_review/`、`fcu_codereview/` 目录」当判据——那是个人 review 工作区产物，不在 manifest 里，随时可能出现或消失。

### 四种判定结果

| 情况 | 处理 |
|---|---|
| 单边命中 | 明确，**不要弹勾选**，复述判定结果后直接进 S1b |
| **两边都不命中** | 弹勾选。可能路径给错、给了子目录、或不是 M57 SDK |
| **两边都命中** | 弹勾选。异常情况：可能客户同时有两套 SDK、给了公共父目录、或工作区被污染 |
| 客户给不出任何判据 | 弹勾选 |

**能自动判定就不要打扰客户。** 只有上面后三种情况才走下面的勾选流程。

### 判不出时：用勾选让客户确认

<EXTREMELY-IMPORTANT>
**用 `AskUserQuestion` 工具弹选项，不要用纯文字提问。**

纯文字问「你是 Linux 还是 QNX」会得到含糊回答（「应该是 Linux 吧」「我们用的安卓那套」），而勾选强制客户在明确选项里做选择，且每个选项都附了自查特征，客户能对照着判断。
</EXTREMELY-IMPORTANT>

调用 `AskUserQuestion`，问题与选项如下：

**问题**：你的 M57 SDK 是哪个平台？（header 用「SDK 平台」）

| 选项 | description 要写的内容 |
|---|---|
| **Linux SDK** | 版本号形如 `V2.10.0`（无前缀）；板端节点在 `/sys/devices/platform/axdiag/`；诊断框架是内核模块 |
| **QNX SDK** | 版本号形如 `QNX_V1.10.0`；板端节点在 `/proc/ax_diag/`；诊断框架是用户态进程 |
| **不确定，需要帮我判断** | 我会给你一条命令，贴回输出即可判定 |
| **两套都在用** | 需要确认本次问题出在哪一套上 |

选项里带自查特征很重要——客户看到「版本号形如 `V2.10.0`」往往当场就能对上，比让他回忆「我们是什么平台」可靠得多。

### 各选项的后续动作

**选 Linux 或 QNX** → 记下客户自报结果，进 S1b。但**必须在 S4 第一轮取证时验证**（见下方「证据兜底」）。

**选「不确定」** → 给一条自带判据的命令，让客户贴回输出：

```bash
# 板端跑（二选一有输出即可判定）
ls -d /sys/devices/platform/axdiag /proc/ax_diag 2>&1
# 或 SDK 侧跑
cat <SDK>/build/version/m57_version.mk 2>&1
```

**选「两套都在用」** → 追问本次问题出在哪一套，并要求给出**那一套**的 SDK 路径或板端输出。不要假设两套现象相同——同一个符号名在两个平台的排查路径完全不同。

### 证据兜底（自报后必须验证）

<EXTREMELY-IMPORTANT>
**客户自报的平台不能当作已确认。** 应用工程师可能不清楚底层，项目里有两套时也容易记混。

所以 S4 第一轮取证命令**必须内置平台判据**——把「列节点结构」那条（本来就是第一条必给的命令）当成平台校验：

- 客户自报 Linux，但 `ls /sys/devices/platform/axdiag/` 返回「不存在」而 `/proc/ax_diag/` 有内容 → **自报错了**，立即改判并告知客户
- 反之亦然

发现自报与实际不符时，**停下来纠正，不要继续用错误平台的命令**。已经给出的结论要重新走一遍。
</EXTREMELY-IMPORTANT>

这样设计的好处是：客户自报正确时（多数情况）零额外往返；自报错误时在第一轮回填就被抓出来，代价只有一轮。

### 冲突处理

客户口头说的平台与硬判据**冲突时，以硬判据为准**，但必须点明冲突并请客户确认：

> 你提到是 QNX 环境，但 `<SDK>/kernel/linux/.../fusa/` 目录存在、且未找到 QNX 的 `diag_stl.c`，判据指向 Linux。请确认这个路径是不是你实际出问题的那套 SDK？

### 判定后的动作

1. **向客户复述判定结果和依据**，给客户纠正的机会：

   > 判定为 **Linux 平台**（依据：`drivers/soc/axera/fusa/` 存在，`SDK_VERSION=V2.10.0` 无 QNX 前缀）。后续排查按 Linux 路线走。

2. **只加载对应平台的 reference**。不要把两个平台的路径和命令同时读进上下文——会互相污染，给出混杂的错误命令。

| 判定 | S2 读 | S3 读 | S4 读 | S5 读 |
|---|---|---|---|---|
| Linux | `归属定位-公共.md` + `归属定位-linux.md` | `FAQ-linux.md` | `取证框架.md` + `取证命令-linux.md` + `运行时接口-linux.md` | `代码地图-linux.md` + `已知可疑点-linux.md` |
| QNX | `归属定位-公共.md` + `归属定位-qnx.md` | `FAQ-qnx.md` | `取证框架.md` + `取证命令-qnx.md` + `运行时接口-qnx.md` | `代码地图-qnx.md` |

客户明确说「我两个平台都在用」或需要跨平台迁移结论时，读 `references/平台差异.md`。

---

## S1b 环境落定

平台已定，收集版本与分支信息。

```bash
cat "<SDK>/build/version/m57_version.mk"
```

| | Linux | QNX |
|---|---|---|
| 版本形态 | `V2.10.0`（无前缀） | `QNX_V1.10.0` |
| manifest | `M57_SDK_V*.xml` | `M57_SDK_QNX_V*.xml` |
| 分支 | `m57h_trunk` 主干；`m57_phase1_mp_v1.1.0`、`m57_phase2_mp_v2.0.1` 量产分支 | 按 manifest 版本号 |
| **版本号的用途** | 只用于交接文档记录**不**作修复判据 | **是 S3「已修故障」判定的主判据** |

最后一行是**双轨分派的第一个分叉点**，原因见 S3。

Linux 侧分支名要记下来：FAQ 里提到的修复在不同分支上进度不同，客户在哪条分支决定了能不能直接升级。

---

## S2 归属定位

**这一步不能跳过。** 先读 `references/归属定位-公共.md`（三步定位法、domain 枚举、module 全表、双层检查），再读平台补充文件。

公共的三步：

1. 合成 mask：`mask = (domain << 27) | ((module & 0x7FF) << 16) | event`
2. 在错误码表里查这个 mask，得到**确切符号名**（表 739 行、620 条目，**两平台逐字节相同**）
3. 按符号名判定归属，选择排查路线

为什么必须查表——同一个 `err 17`，`module 0` 是心跳超时，`module 45` 是 ISP 帧 ID 校验，毫无关系。

归属确定后按类型分流：

- **DFC（domain 0 / module 0）** → 诊断框架自身，走对应平台 FAQ 的心跳/框架类条目
- **ECM_\*** → 就地检测层，读 `<SDK>/docs/internal/domain/bsp/ecm.md` + 平台 ECM 排查清单
- **FCU_SAFETY** → 跨域汇聚层，读 `<SDK>/docs/internal/domain/bsp/fcu.md` + 平台 FCU 排查清单
- **具体子系统**（NPU、DDR、EMMC、ISP_PIPE、IVE 等）→ 查该模块自检实现，**并同时检查它是否经 ECM/FCU 通路上报**

<EXTREMELY-IMPORTANT>
**归属到具体子系统时，输出里必须显式写出这一句结论**：

> 该故障是否经 ECM/FCU 通路上报？（是 / 否 / 无法排除 ＋ 依据）

写"是"或"无法排除"时，下一步先查两层——ECM 侧看检测是否误判、FCU 侧看上报链路是否正常，**排除这两层之后**才能把结论落在子系统自身。

**只把 `ecm|fcu` 写进检索命令或 grep 里不算完成这一步**——必须用一句自然语言给出判断。这是 S2 的硬性输出项，漏了就等于 S2 没做完。
</EXTREMELY-IMPORTANT>

最后一条要特别注意：**ECM 是 FCU 的上游**，ECM 检测到的错误是经 FCU 上报的。所以一个子系统的故障码往往要 ECM 侧（检测是否误判）和 FCU 侧（上报链路是否正常）两层都看。

平台特有部分（错误码表路径、符号名前缀、日志形态、ECM/FCU 清单条目）见 `归属定位-<平台>.md`。

---

## S3 FAQ 检索

读对应平台的 FAQ（`references/FAQ-linux.md` 或 `references/FAQ-qnx.md`），用 S2 得到的符号名和现象去匹配，别只用客户的原话匹配。

FAQ 每条都有「其他问法」字段，客户的措辞往往能直接命中那里。开头的速查表是最快入口。

<EXTREMELY-IMPORTANT>
**两份 FAQ 的编号格式不同**（一份两位补零、一份不补零），且 FAQ 会持续新增条目。

所以：**引用时一律照抄该 FAQ 文件里的原始编号，不要自己换算、补零或跨平台映射编号。** 本 skill 的其它文件也不硬编码 FAQ 条目号。看到「FAQ-07」和「FAQ-7」不要以为是同一条——它们属于不同平台的不同文件。
</EXTREMELY-IMPORTANT>

三类性质各有各的出结论方式：

### 命中「设计预期」

把机制解释清楚，**必须带代码依据**，不能只说「这是设计」。

例：客户问 `heartbeat time:N` 刷屏。结论是每轮等待 `SERVER_HEARTBEAT_TIMEOUT` = 5ms，超时才 `heartbeat_time++` 并打一行 INFO；**只有累计超过 5 轮**才真正报 `heartbeat timeout` 并上报故障。所以刷 `heartbeat time:N` 是去抖过程的正常痕迹，不是「已收到 N 次心跳」。（这条机制**两平台一致**，但代码文件位置不同，引用行号时用对应平台的。）

告诉客户怎么自己确认（关键词区分、计数是否连续增长），以及为什么不用担心。

### 命中「配置·使用·方法」

指出**哪里没配好、怎么配、怎么验证配对了**。三件都要给。

这类可以指导客户改配置文件、重跑 `make PLAT=<平台> fusa_config`、写运行时节点。改配置是允许的，改源码不允许。

**两平台共有的一个模式**：配置有多个层次，改了上游不等于下游生效。

```
源 Excel → 生成 JSON/头文件 → rootfs 里的实际 JSON → 板端节点实际值
```

**结论一律落在「回读板端节点实际值」**，不要只看 JSON 或服务返回成功。

### 命中「已修故障」——双轨分派

<EXTREMELY-IMPORTANT>
两个平台的判据不同，**这是知识来源差异，不是设计不一致**：QNX 的 FAQ 带版本速查附录（记录了每条修复对应的 SDK 版本），Linux 的 FAQ 不提供 Fix Version、只给代码特征。所以两边只能用各自可得的判据，矩阵行数也不同。

**不要把一边的判据套到另一边**，尤其不要在 Linux 侧编造修复版本号。
</EXTREMELY-IMPORTANT>

#### QNX 轨：版本号比对 + 代码特征（双判据，4 行矩阵）

代码特征检测**只作旁证**，版本号比对才是主判据。

| 版本号比对 | 代码特征检测 | 结论 | 对客户怎么说 |
|---|---|---|---|
| 版本 < 修复版本 | 搜不到特征 | 确认未含修复 | 升级到 `Vx.y.z` 即解决 |
| 版本 ≥ 修复版本 | 搜到特征 | 确认已含修复 | 已含此修复，需另找原因 → 进 S4 |
| 版本 ≥ 修复版本 | **搜不到特征** | **检测不确定** | 版本上应已含修复。特征未检出可能因重构或原语差异，**不据此判定未修复** → 进 S4 |
| 版本 < 修复版本 | 搜到特征 | 已打零散补丁 | 已单独打过补丁，需确认补丁完整性 |

第 3 行**禁止**输出「未含修复」的结论。已实测两例假阴性（均在 `QNX_V1.10.0`，按版本号应含全部修复），详见 `references/代码地图-qnx.md`。

#### Linux 轨：仅代码特征（单判据，3 行矩阵）

Linux 侧**不查 Jira、不查 Gerrit**，判据只有：FAQ 条目 + 客户 SDK 里的代码特征。

**搜不到特征时的默认结论是「不确定」，不是「未修复」。**

| 代码特征检测 | 结论 | 对客户怎么说 |
|---|---|---|
| 搜到特征 | 确认已含修复 | 已含此修复，需另找原因 → 进 S4 |
| 搜不到特征，且能确认当前实现用的是**同一套原语** | 疑似未含修复 | 特征缺失且实现方式未变，倾向未含修复。建议升级到较新版本验证 → 可出结论 |
| 搜不到特征，但当前实现已重构/换原语 | **检测不确定** | 代码已演进，无法据特征判定 → 进 S4/S5 用运行时证据定性 |

第 2 行和第 3 行的区别是**你有没有真的读过当前实现**。没读就只能落在第 3 行。

#### 两轨共同的检测纪律

- **不要照抄 FAQ 里的关键词就 grep。** 先读 `docs/internal/domain/bsp/*.md` 和实际代码，确认当前实现用什么原语，再决定搜什么。
- 搜索用 `rg -c` 计数或 `rg -l` 列文件，比看匹配文本可靠。
- 搜不到时可能是：**重构搬家、原语不同、补丁在 review 未合入**。原语对照表见 `references/平台差异.md`。
- **QNX 侧**检索范围必须含 `fcu_codereview/`、`code_review/`、`doc_modify/`——补丁可能在 review 中而非主线。
- **Linux 侧**实测这些 review 目录**不存在**（也不在 manifest 里），不用搜。

FAQ 完全没覆盖，或命中后需要现场证据才能定性 → 进 S4。

---

## S4 取证收敛

生成命令清单让客户在板子上执行并回填。

先读 `references/取证框架.md`（使用原则、症状分支目录、回填后怎么用——**两平台通用**），再读 `references/取证命令-<平台>.md` 取实际命令，属性含义查 `references/运行时接口-<平台>.md`。

核心原则（两平台一致）：

- 一次给 6~8 条，不要更多。先给必做项，看回填结果再追加按需项。
- **每条都要说明看什么、什么值算正常。** 客户不知道 `cycle_enable` 该是 0 还是 1。
- 命令要能直接复制粘贴，别让客户自己拼路径。
- **第一条永远是路径确认**（先让客户 `ls`），不要凭 FAQ 示例路径硬猜。
- 客户回填后逐条比对预期，把「符合预期」的项排除掉，缩小范围。

平台特有的强制要求：

<EXTREMELY-IMPORTANT>
**Linux**：FCU 同步读取使用不可中断等待，`timeout` 不能保证解除 D 状态。已有读取卡住或 RPMsg 状态不明时，停止新增 FCU 同步读取，先取现有任务栈、RPMsg/握手日志和节点信息；无响应只能说明请求未完成，不能直接断定未建链。通信恢复确认后再串行读取。见 `取证命令-linux.md` 的 FCU 分支。

**QNX**：进程状态取证要看 `pidin` 的线程阻塞态（REPLY-blocked / RECEIVE-blocked / MUTEX）。QNX 的 `MsgSend` 是同步阻塞，对端不回包会反向拖死发送线程——这是 QNX 特有的死等风险。
</EXTREMELY-IMPORTANT>

拿到回填后：能定性就出结论（回到 S3 的三类输出方式）；仍不能定性则进 S5。

---

## S5 代码反查

在客户的 SDK 里查证，定性为四类之一。路径与关键判定点见 `references/代码地图-<平台>.md`。

| 性质 | 判据 | 输出 |
|---|---|---|
| **设计预期** | 代码里找到「有意为之」的证据：显式阈值定义、去抖计数、注释说明 | 解释机制 + `文件:行号` 依据 + 为什么不用担心 |
| **配置·使用·方法** | 找到某配置项的读取点和默认值，能解释现象 | 确切改法 + 验证方法 |
| **已修故障** | 命中 FAQ 已修条目 | 走 S3 对应平台的修复判定矩阵 |
| **疑似新缺陷** | 前三类都排除，且能给出「代码这样写 → 导致这个现象」的推理链 | 进 S6 |

定性为**配置·使用·方法**时可以指导客户改配置，改完给出验证方法。

定性为**疑似新缺陷**前，先比对已知清单：

- **Linux**：读 `references/已知可疑点-linux.md`——6 条在当前 SDK 上实证过、但 FAQ 和 SDK 文档都未记录的代码事实。客户现象很可能已经在列，其中两条在配置层面可以规避、能当场解决。
- **QNX**：比对 FAQ 的版本速查附录 + `fcu_codereview/` 等 review 目录（`代码地图-qnx.md` 有实测案例）。QNX 侧目前没有等价的已知可疑点清单。

命中已知清单时，可以直接给出代码事实和推理链，但**必须说清**「这是当前 SDK 的静态代码事实，缺陷性质需原厂确认」——不要自行断定是 bug，也不要让客户改代码。

定性为**疑似新缺陷**时：

- 可以给出建议补丁的 diff（只读展示，让客户自己判断是否采用）
- **不替客户落盘**，也不建议客户在未与原厂确认前用于量产
- 明确告知：改 FuSa 源码会影响功能安全认证一致性

每轮结束时向客户报告：当前结论、置信度、下一步能验证什么。三轮上限到了就进 S6。

---

## S6 交接文档

三轮无果，或定性为疑似新缺陷时产出。模板见 `references/交接文档模板.md`（公共骨架 + 平台补充段落）。

产出到**独立目录**，便于客户整个打包发回原厂：

```
fusa-handoff-<YYYYMMDD>-<关键词>/
├── README.md              主交接文档
└── attachments/
    ├── original-log.txt         客户原始日志（完整，不截断）
    ├── evidence-round1.txt      S4 各轮命令输出
    ├── evidence-round2.txt
    ├── config-snapshot/         相关配置文件快照
    └── suggested-patch.diff     若有建议补丁
```

<EXTREMELY-IMPORTANT>
**README 开头必须标注平台**（`> 平台：M57 **Linux**（非 QNX）` 或反之），并写明判定依据。否则原厂拿到文档还要再问一遍，或者按错误平台去查。
</EXTREMELY-IMPORTANT>

文档要同时服务两类读者——原厂工程师要能快速判断归属和优先级，AI 要能直接接手继续排查。所以必须包含：

- **平台判定结果与依据**
- 环境事实（SDK 路径、版本号、manifest 分支、板型/`PLAT`）
- 归属定位结果（mask、符号名、归属域）
- **已排除的可能性及排除依据**（这条最省原厂时间）
- 每轮做过的实验：做了什么、预期什么、实际什么、日志在哪个附件
- 当前最可能的根因假设及其代码推理链
- 还需要什么信息/权限才能继续

**Linux 侧额外必填时间线**：首个异常 → 后续 FuSa 事件的顺序。原厂看 Linux FuSa 问题的第一个动作就是找最早的原始故障，把时间线整理好能省掉一轮往返。

写完告诉客户：目录在哪、怎么打包、发给谁时附上什么话，以及提醒检查附件里是否有不宜外发的内容。

---

## 验收自检

`evals/` 是本 skill 的**验收用例集**，用来在改动 `SKILL.md`、`references/*.md` 之后确认判定能力没有退化——
重点盯三条硬闸门（S0 输入闭合、S1 平台判定、S2 归属定位）和两条铁律（不落盘改源码、不跨平台套结论）。

用户要求「跑验收 / 回归自检 / 评估排查准确率」时按本节执行。**本节不属于排查流程**：客户带着问题来时照旧走 S0–S6。

### 两条轨道

1. **确定性校验**（随时可跑，不含语义判定）：

   ```sh
   python3 <skill-dir>/evals/run_evals.py
   ```

   检查结构、隔离声明、跨平台串味、FAQ 编号纪律、参考文件完整性等可机械判定的事实，退出码 0 才是全绿。

2. **Golden Case 盲测**：`evals/FUSA-00x/`。每个 Case 分两个区——`input/` 是现场材料（分析阶段唯一可读），
   `answer/` 是 `case.yaml`（元数据与隔离声明）+ `oracle.yaml`（期望结论）。

### 盲测纪律

<EXTREMELY-IMPORTANT>
进入评分阶段之前，不得以任何方式读取该 Case `answer/` 下的任何文件，也不得通过全文检索猜测答案。
一旦提前读到，这次自检结论作废，必须换一个没读过答案的 Case 重跑。一次只跑一个 Case。
</EXTREMELY-IMPORTANT>

### 执行

1. 预检（只打印 `input/` 清单，不打印答案）：

   ```sh
   python3 <skill-dir>/evals/run_evals.py --list FUSA-001
   ```

2. 只读预检给出的文件，按 S0–S6 正常排查，把自己当作一个没有答案的排查者。
3. 把输出**冻结**为 `analyzer_result`。冻结之后不得依据答案补写、删改或重跑。
4. 此时才读 `answer/oracle.yaml`，按 `evals/README.md` 的判定规则做语义比对。
5. 按 `evals/README.md` 里的固定格式输出 `Verdict: PASS | FAIL | ERROR`。

批量跑多个 Case 时，逐 Case 冻结、逐 Case 评分；一个 Case 的 oracle 不得用于评判另一个 Case。
`FAIL` 表示结论不符合 oracle，`ERROR` 表示 Case 结构或流程无法完成，两者不可互换。

### 维护

新增 Case、改 oracle、补素材的规范见 `evals/README.md`（隔离声明、证据可溯源、素材脱敏三条硬约束）。
改完 `references/` 或 `SKILL.md` 后必须重跑一遍盲测，确认没有回归。

---

## 参考文件

### 公共（两平台都读）

| 文件 | 用途 | 什么时候读 |
|---|---|---|
| `references/平台差异.md` | 平台判定判据、两平台对照、原语换算、可互通与不可互通的边界 | S1；客户搞混平台；跨平台迁移结论 |
| `references/归属定位-公共.md` | 三步定位法、domain 枚举、module 全表、ECM/FCU 双层检查 | S2，必读 |
| `references/取证框架.md` | 取证使用原则、症状分支目录、回填后怎么用 | S4，必读 |
| `references/交接文档模板.md` | 交接文档结构（含平台补充段落） | S6 |

### Linux 分支

| 文件 | 用途 | 什么时候读 |
|---|---|---|
| `references/归属定位-linux.md` | Linux mask 写法、两种日志形态、三条动作链、ECM/FCU 清单 | S2 |
| `references/FAQ-linux.md` | Linux FAQ 知识库 | S3，必读 |
| `references/运行时接口-linux.md` | 三类 sysfs/debugfs 路径与全部属性名 | S4，必读 |
| `references/取证命令-linux.md` | Linux 取证命令 | S4 |
| `references/代码地图-linux.md` | 代码路径、Kconfig 开关、已知不一致 | S5 |
| `references/已知可疑点-linux.md` | 实证但文档未记录的代码事实 | S5，判疑似新缺陷前必读 |

### QNX 分支

| 文件 | 用途 | 什么时候读 |
|---|---|---|
| `references/归属定位-qnx.md` | QNX mask 写法、domain 1/16 表、ECM/FCU 机制与清单 | S2 |
| `references/FAQ-qnx.md` | QNX FAQ 知识库（含版本速查附录） | S3，必读 |
| `references/运行时接口-qnx.md` | `/proc/ax_diag` 属性、`diag_tools` 参数 | S4，必读 |
| `references/取证命令-qnx.md` | QNX 取证命令 | S4 |
| `references/代码地图-qnx.md` | 代码路径、review 补丁目录、假阴性实测案例 | S5 |

### SDK 内的权威文档

比 FAQ 更详细的机制说明，FAQ 未覆盖时优先读这些，**不要猜**：

| 文档 | Linux 文件名 | QNX 文件名 |
|---|---|---|
| diag 框架 | `docs/internal/domain/bsp/diagcore.md` | `docs/internal/domain/bsp/fusa_diagcore.md` |
| ECM | `docs/internal/domain/bsp/ecm.md` | 同左 |
| FCU | `docs/internal/domain/bsp/fcu.md` | 同左 |

每份文档的 `pitfalls` 段落是已知坑清单，往往直接命中客户的问题。

`docs/internal/domain/fusa/readme.md` 只有占位模板文本，没有实质内容，不用去读。

### 验收用例

| 文件 | 用途 | 什么时候读 |
|---|---|---|
| `evals/README.md` | 验收方式、盲测纪律、判定规则、执行话术、维护规范 | 跑验收 / 新增 Case |
| `evals/run_evals.py` | 确定性校验器（结构、隔离、跨平台串味、FAQ 编号纪律） | 每次改完 skill 先跑这个 |
| `evals/evals.json` | 标准 evals 条目（prompt / 期望输出 / 验收点） | 外部评测框架接入 |
| `evals/trigger-evals.json` | 触发与跨 skill 边界用例 | 核对激活行为（本 skill 是 explicit activation） |
| `evals/FUSA-00x/` | 盲测 Golden Case：`input/` 现场材料 + `answer/` 答案与元数据 | 语义回归自检，见「验收自检」 |
