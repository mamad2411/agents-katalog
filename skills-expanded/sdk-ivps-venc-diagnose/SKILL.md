---
name: sdk-ivps-venc-diagnose
description: 诊断 AX615 IVPS(VPP/VGP) 到编码器之间的链路卡死。用户提供 `/proc/ax_proc/link_table`、`link_table_kernel`、`syncagent`、`venc`、`jenc`、`ivps` 的 proc 输出，或描述 IVPS 出图正常但编码无输出、帧率掉零、某个编码通道停住时使用；`SW_Low_Mem`/`SW_Low_Latency` 的 HSK 绑定按握手形态、握手高度和 16 位模进度判定，`SW_Offline` 等非 HSK 绑定按 IVPS 输出与编码器接收/送编码/取流的业务计数差值定位卡死段。解析单次采样即可给出静态判断，两次采样用于确认推进计数是否持续不变。用户要求跑 IVD Golden Case、回归自检或评估分析准确性时，按「回归自检」执行 evals/ 下的盲测。
---

# IVPS→VENC 诊断

根据 proc 信息判断 HSK 形态或 offline 链路的数据流状态、卡死模块和初步原因。结论必须区分证据确认和待验证推断，不能只凭一次 `cat` 或单个静态字段下结论。

本 skill 覆盖两类链路，判定方法不同，不要混用：

- **HSK 链路**：`SW_Low_Mem`/`SW_Low_Latency` 绑定，有握手寄存器，按第 2 节识别形态、按第 3.1 节判握手进度。
- **非 HSK 链路**：`SW_Offline`、`HW_Online`、`Mode_Unset` 绑定，没有握手寄存器，按第 3.2 节的业务计数差值定位卡死段；`HW_Online`/`Mode_Unset` 只标注模式，不下卡死结论。

本文的“HSK 链路”指 IVPS 侧（VPP/VGP）与下游编码器之间的握手；第 2 节的一对二/二对一形态里第二个消费者可能是 JENC，但分析对象始终是 IVPS 输出的这条握手链路，不是编码器内部。

## 分析顺序

先判编码器有没有正常收到帧，再决定往哪个方向看，不要一上来就逐通道罗列计数：

1. **编码器有没有正常收到帧**：看目的编码通道的 `FrmRecv`（JENC 另看 `SubmitCnt`）。在涨就说明 IVPS 出图、link 派发、编码器收帧这三段都通，问题在编码器内部；两轮都不涨才怀疑上游。
2. **收到了，就顺着编码器的处理链往下看**，停在第一段不推进的地方：收帧 → 送编码（`Send2EncCnt`/`SubMitCnt`）→ 编码完成（`EncSucCnt`/`SucCnt`）→ 码流写出与取走（`WriteCycle`/`ReadCycle`、`AvalRSize`）。前三段里任何一段的不推进都判编码器（H26x 或 JENC）为最可能的问题模块；只有码流写出在涨、取走不动时才判用户态取流。
3. **没收到，才回头看 IVPS**：先看该链路 IVPS 末尾 filter 的 `OutCnt`（第 3.2 节步 1）。输出在涨而编码器不收，判卡在 link 派发；连输出也没有，再往上游看 IVPS 输入和 VIN。

最可能的问题模块取「自己不再推进」的最靠下游那一级：上游计数冻结不等于上游停摆 —— 计数冻结的那一级，只要它的目的编码器 `FrmRecv`/`SubMitCnt` 还在涨，帧就已经流过去了（低内存握手下 IVPS 滤器计数不逐帧更新），要继续往它的下游找。

## 脚本执行约定

`scripts/` 与本 SKILL.md 在同一目录内，脚本不依赖当前工作目录。执行前先把本 SKILL.md 所在目录的绝对路径导出为 `SKILL_DIR`，后续命令一律用 `"$SKILL_DIR/scripts/<脚本名>"` 调用：

```bash
export SKILL_DIR="<本 SKILL.md 所在目录的绝对路径>"
```

不要写死路径，也不要先 `cd` 到 skill 目录再用相对路径执行；用户数据文件（proc 文本、寄存器输出）仍按用户给出的路径解析，与 `SKILL_DIR` 无关。

## 报告输出目录

HTML 报告默认写入本 skill 的 `reports/` 目录（`$SKILL_DIR/reports/`），与执行时所在的工作目录无关；该目录已随 skill 建好，脚本会自动创建。用户指定目录时用用户的目录，不要写死其他路径。脚本执行后会打印 `HTML_REPORT` 和 `HTML_REPORT_DIR`，回复中原样给出这两个绝对路径。

## 1. 采样与证据分级

先在设备上打开同步信息，再连续采样两轮，建议间隔 3--10 秒；卡死时间较长时可采样第三轮确认：

```sh
echo 'priv on' > /proc/ax_proc/syncagent
for n in 1 2; do
    echo "===== SAMPLE $n $(date) ====="
    cat /proc/ax_proc/link_table
    cat /proc/ax_proc/link_table_kernel
    cat /proc/ax_proc/syncagent
    cat /proc/ax_proc/venc
    cat /proc/ax_proc/jenc
    cat /proc/ax_proc/ivps
    [ "$n" = 1 ] && sleep 5
done > /tmp/hsk_proc.txt
```

`link_table` 只有 Src/Dst/Mode/Line，**没有 Engine 列**；`link_table_kernel` 才带 `Engine(srcId:SrcEngine --> dstId:DstEngine)`（见 `ax_sys_link_proc_show.c`）。第 2 节判断 VENC/JENC 分支依赖 Engine，所以两个节点都要采；只采到 `link_table` 时脚本会给出提示，JPEG HSK 分支只能标注待确认。

`link_table` 是拓扑快照；`syncagent`、`venc`、`jenc`、`ivps` 是动态状态。收到部分 proc 或单次 `cat` 时，先分析当前现场，不要因为信息不完整而停止判断：

- 有 `link_table`：先识别可见的 HSK 形态和连接关系；缺少它时，根据 `syncagent` 的 `SessId/Cons/wait` 给出拓扑候选，并标注形态待确认。
- 有任一模块 proc：提取该模块的状态、错误计数、输入输出计数和等待关系，给出当前最可能的问题模块及原因；没有对应 proc 的模块不作无证据的确定性结论。
- 只有一次 `cat`：可以判断静态状态、错误字段和当前计数关系，但不能把计数不变表述为“持续卡死”；应标注“疑似停滞，缺少第二次采样确认”。无论静态判读正常还是疑似停滞，结论都只能写“持续性待确认”，且「还需补充」必须给出补采指令（间隔 3~10 秒再采一轮，如 `for i in 1 2; do cat /proc/ax_proc/{link_table,link_table_kernel,syncagent,venc,jenc,ivps} >> hsk_proc.txt; sleep 5; done`），不能只写“待确认”而不说明如何确认。
- 只有部分模块：沿已知数据流分析，明确指出结论受哪个缺失模块限制；只提示补充该缺失模块或相关字段，不要求无关模块全部重新提供。
- 至少两次采样：对已有模块比较 `S1 -> S2`，确认计数是否持续不变；`venc`、`jenc`、`ivps`、`syncagent` 不要求必须同时齐全，缺哪一项就说明哪一项无法交叉验证。

`syncagent` 的 `SESSION State` 是 HSK 工作前置条件：只有 `State=2` 才表示该 session 处于正常工作状态。若目标 HSK session 的 `State` 不是 `2`，先报告同步 session 未正常工作，再分析连接值和业务计数；此时不能把 wait 未推进直接归因于 VPP、VENC 或 JENC。

### 1.1 解析 proc

拿到采样文件后，先跑解析脚本，把字段对齐、16 位模运算和 `S1 -> S2` 差值交给脚本处理，不要手算：

```bash
python3 "$SKILL_DIR/scripts/parse_hsk_proc.py" --input /tmp/hsk_proc.txt --pretty
```

也可以直接通过 stdin 传入粘贴的 proc 文本。脚本按 `===== SAMPLE n =====` 切分多轮采样；没有该标记时按单次采样处理，并置 `sample_marker_present=false`。输出包含 `environment`（`sdk_version`、`module_versions`、采样轮数）、`samples`、`deltas`、`issues` 和 `coverage`。

`issues` 是扁平列表，每项含 `level`（`错误`/`高风险`/`提示`）、`channel`、`field`、`message`。`错误` 表示 proc 行与表头列数不一致（列错位风险），`高风险` 表示违反第 3 节判定规则，`提示` 表示需要人工确认的疑点。脚本不静默丢弃任何无法对齐的行。

脚本只解析本 SKILL.md 用到的表与列：只有本 SKILL.md 按名引用、或脚本判定逻辑实际使用的字段才会进入 JSON。`GOP`、`RC ATTR 2/3`、`CHN ATTR 1` 的属性列、耗时/带宽统计、节点池，以及其他与 HSK 无关的 IVPS 表整表不参与诊断；同一张表内未被引用的列同样不输出。例外是码控表：`VENC CHN RC ATTR 1` 与 `JENC CHN RC ATTR` 的 `RcMode`/`SrcFr`/`DstFr`（VENC 另有 `TargetBitRate`）必须解析——第 3.2、5 节要靠它区分「配置的低帧率」和「真停滞」。完整清单以 `coverage.excluded` 为准，不要凭印象列举。

脚本已经确定性完成的计算：

- 模块切分（`link_table`/`link_table_kernel`/`syncagent`/`ivps`/`venc`/`jenc`）与链路拓扑：HSK 链路进 `topology.hsk_links`（排除 `SW_Offline`，见第 2 节），非 HSK 绑定进 `topology.non_hsk_links` 并在每个 sample 上生成 `offline_links`（见第 3.2 节）。
- 两张 link_table 按 `(Src, Dst)` 合并成同一条链路，并由 `Engine.dst` 决定消费端模块（`consumer`），优先于 `ModId`。`link_table` 对用户侧把 H.26x 与 JENC 统一打印成 `VENC`，这不是异常；没有 kernel 表时，按目的通道实际落在 venc 还是 jenc proc 里归一消费端。只有在两侧编码 proc 里都没有该通道时才判为无法确认：该链路只列进 `topology.hsk_links` 并给出一条「提示」，不计入 HSK 形态。目的端是编码侧 `srcNum=2` 的通道时，它由二对一形态解释，link_table 只作为该形态的来源绑定，不另算一对一。
- 表头 `[...]` 列名分组、`RegVal0/1/2` 这类同前缀编号列、`0.0 :  0.0` 与 `1 :24064` 这类被空格拆开的字段对齐。
- `venc/jenc HSK STATUS` 两段表的合并：第一段给 `initVal/syncVal/waitId/upId`，第二段给 `waWaPhy0/waUpPhy0/waReInfo*`。
- 第 3.1 节的 `握手高度/当前进度`（16 位模 65536）和四种判定。
- `waitId/upId` 与 `syncagent` 的 `ConId/ChnId` 映射，以及 `waWaPhy0/waUpPhy0` 与 `SyncAddr` 的地址交叉核对。
- 握手高度与 `ceil(EncH/64)*64`、`sliceNum*minhskLin` 的一致性核对；不一致时按第 3.1 节报告「HSK 参数或版本配置不一致」。
- 两次采样的 `S1 -> S2` 差值、单调计数停滞判定，以及 `HoldCnt/ReleaseCnt` 差值扩大判定。
- 第 3.2 节的 offline 链路判定：把每条 `offline_links[]` 的 IVPS 输出、编码器接收/送编码/取流计数挂到 `S1 -> S2` 差值上，给出 `verdict` 与 `evidence`，并附上两端的配置帧率（`rate_hint`）。

几个键位提示：`link_table.links[]` 每条含 `src/dst/mode/line`，采到 kernel 表时多一个 `engine`（`src_id/src/dst_id/dst`），`topology.hsk_links[].consumer` 就是按 `Engine.dst` 归一后的消费端模块；编码通道的 `frame` 来自 `CHN ATTR 2`，只有 `EncW/EncH/SeqNum/PTS`，`rc` 来自 VENC `CHN RC ATTR 1` / JENC `CHN RC ATTR`，只有 `RcMode/SrcFr/DstFr`（VENC 多 `TargetBitRate`），`hsk_channels[].rc` 就是它，供第 3.1 节/第 3.2 节对照配置帧率；HSK STATUS 拆成 `hsk`（握手寄存器与 `conId/waitId/upId`）和 `hsk_wait`（`cntWa/douWa/opWaChn*/opUpChn*` 等待分支关系），`hsk_info` 给 `waWaPhy0/waUpPhy0` 物理地址和 `waReInfo*/upReInfo` 的 `索引:值`（编码侧 wait/update 寄存器当前值，用于第 3.1 节的两侧进度比对）；JENC 的 `HwState`/`busyCnt` 在 `jenc.frame_list`（模块级单行表，不要当成 `jenc chn0`）；IVPS 输出积压 `OutSts`/`OutDepth` 与抽帧配置 `FrcMode`/`Frc(src:dst)` 都在 `ivps.chn_info`。`offline_links[]` 每条含 `src/dst/mode/verdict/evidence`，`upstream` 是 IVPS 末尾 filter 的 `InCnt/OutCnt/Fail1/Fail2` 加 `chn_info` 的 `OutSts/OutDepth/OutFps/FrcMode/Frc(src:dst)`，`downstream` 是编码器通道的 `FrmRecv/SubMitCnt/ReadCycle/AvalRSize/HwUsed` 加 `RcMode/SrcFr/DstFr/OutFps`，超出 `SW_Offline` 之外的模式 `verdict` 为 `null`，只用 `evidence` 说明模式。

脚本有意不输出的结论直接看 `coverage.limits`，需要帧阶段信息或第二次采样的判定都在其中；这些结论按第 3.1、3.2、4 节人工判断后写入报告。

### 1.2 确认 SDK 版本

`environment.sdk_version` 来自 proc 头部的 `[SDK version]` 行，`environment.sdk_version_source` 记录取值来源，`module_versions` 按模块给出各自的版本横幅。HSK 的握手节奏、`minhskLin` 取值和 `link_table` 是否带 `Engine` 都会随版本变化，所以识别到版本时要在结论中原样引用该字符串，再判断字段差异是版本行为还是配置问题。

proc 未输出版本行时脚本输出 `unknown` 并追加一条「提示」级问题。此时按以下顺序补齐，取到即停：

1. 让用户执行 `cat /proc/ax_proc/version`（或该 SDK 对应的版本节点）并粘贴结果；
2. 在提示词注入或用户指定的 SDK 包内检索版本文件名（如 `version.mk`、`ax_version.h`）取版本号；
3. 仍无法确认时，把版本记为「未知」，并在结论中标注「版本相关差异未经确认」，不按某个具体版本的握手节奏下判断。

## 2. 先识别形态

以 `link_table` 的实际连接为准，`syncagent` 用于验证 HSK 等待关系；不要用通道编号或分辨率猜形态。

| 形态 | 拓扑判定 | syncagent 常见证据 |
|---|---|---|
| 一对一 | 同一个 IVPS/VPP 输出只有一个 VENC/JENC 消费者 | 一个 HSK 会话对应一个上游和一个下游；通常 `srcNum=1`、`cntWa=0`、`douWa=0` |
| 一对二 | 同一个 IVPS/VPP 输出同时 link 到两个编码消费者，通常 VENC+JENC | `link_table` 中同一源有两个有效 HSK 编码目的端；编码器侧通常 `srcNum=1`，`dst_num=2` 或 `ConWait=1` 是辅助证据 |
| 二对一 | 一个编码消费者需要两个上游生产阶段/输入事件，通常 VPP+VGP 汇入 JENC | 编码器侧 `srcNum=2`，两个来源为 VPP/VGP，且通常 `DoubleWait=1`；不能只凭 `DoubleWait` 判定。`srcNum` 只说来源个数，报告里的依据必须引用 `link_table` 的绑定关系（目的模块打印为 `VENC` 时按编码通道归一后照原样引用），确实没有对应链路时才标注绑定待确认 |

识别步骤：

1. 以 `link_table` 的 `Src/Dst`、`Mode`、`Line` 为准，编码分支用 `link_table_kernel` 的 `Engine(src->dst)` 确认。`link_table` 对用户侧把 H.26x 和 JENC 两条分支统一打印成 `VENC`，所以目的模块写着 `VENC` 不代表它一定是 H.26x：没有 kernel 表时，看目的通道实际落在 venc 还是 jenc proc 的 `CHN ATTR`/`HSK STATUS` 里，落在 jenc 侧就是 JPEG 分支，按该侧通道号继续判形态。只有两侧都没有该通道时才判消费端无法确认，该链路不计入形态并补采 `link_table_kernel`；同一个目的端已经在编码侧体现为 `srcNum=2` 时，它属于二对一，不能既算一对一又算二对一。
2. 按 `(源模块, grp, chn)` 分组统计有效 HSK 编码目的端。一个源对应两个目的端，判为一对二——同一个 IVPS/VPP 输出同时连两个编码消费者时，即使 `syncagent` 或某个消费者 proc 缺失也要按一对二识别，不能退回一对一。只有 `SW_Low_Mem`/`SW_Low_Latency` 的链路计入，其余模式不计入 HSK 形态。
3. 对每个编码目的端检查 `srcNum` 和 `syncagent` 的 `Cons/wait` 关系。一个目的端 `srcNum=2` 且来源为 VPP+VGP，判为二对一；不能要求两个分支必须属于同一个 `SessId` 才成立。
4. 若同时存在多个会话，分别识别后报告组合形态，例如“一对一 + 二对一”，不要强行归为单一形态。
5. `link_table` 与 `syncagent` 矛盾时，报告“拓扑/同步配置不一致”，优先排查 link 建立、解除顺序和通道映射。**典型触发**：编码器 `HSK STATUS` 里某通道 `bHsk=Y` 且有 `conId/waitId/upId`，但这些 id 在 `syncagent` 里找不到任何连接（两侧无法交叉映射）——这不是“无法核对、暂不视为异常”，而是明确的矛盾信号；即使该通道业务计数还在推进，也必须把「拓扑/同步配置不一致」作为结论输出（业务推进只作旁证），排查方向给 link 建立/解除顺序、采集完整性（`priv on` 后重采 syncagent）与版本匹配，矛盾解决前不下任何模块的卡死结论。

### 非 HSK 绑定的链路

HSK 只在 `SW_Low_Mem` 和 `SW_Low_Latency` 下启用（`venc.c` 的 `VENC_CHECK_HSK_MODE`）。所以 `SW_Offline`（以及 `HW_Online`、`Mode_Unset`）绑定的链路**没有握手寄存器可判**：VENC 侧不置 `bHsk=Y`、HSK STATUS 段不打印、`syncagent` 没有对应会话，这些都是正常现象，不是数据缺失。这类链路不进 HSK 形态统计，改走第 3.2 节的数据流判定；脚本会用一条「提示」列出具体链路和 Mode，再按两次采样的业务计数差值给出 `offline_links[].verdict`。另外 `WaitEncFail` 在 offline 路径不会增长，一旦出现就是异常升级信号。

## 3. 两次采样的比较方法

对每个有效通道记录 `S1 -> S2` 的变化。递增计数包括 `SeqNum`、`hskCnt`、`FrmRecv`、`SubmitCnt`、`SucCnt/EncSucCnt`、`TotalCnt`、`InCnt`、`OutCnt`、`ReadCycle`、`WriteCycle`、`HoldCnt`、`ReleaseCnt`。FPS、地址、PTS 可辅助判断，但不能替代计数差值。计数差值本身只能说明“是否还在动”，判断阻塞位置时按以下口径读：

- 计数有增长：该环节在运行；只能称为“未发现此环节完全停住”。
- 关键输入计数增长、输出计数不增长：该模块或其下游正形成阻塞。
- `hskCnt`、`FrmRecv`、`SubmitCnt` 等连续两轮不变：该通道没有新的 HSK/编码工作，结合上下游定位等待点。
- `HoldCnt` 增长而 `ReleaseCnt` 不增长，或两者差值持续扩大：存在未释放的同步 hold，优先看对应 `wait` 端和下游消费者。
- 地址或 `RegVal` 变化但业务计数不变：只说明同步寄存器活动，不能证明帧已完成。

两类链路的比较口径不同：HSK 链路在计数差值之外还要按第 3.1 节的 16 位模握手判进度；非 HSK 绑定没有寄存器，只按第 3.2 节的业务计数差值判卡在哪一段。

### 3.1 HSK 链路：16 位模握手与推进节奏

#### 握手基准与 16 位溢出计算

`venc/jenc` 的 HSK proc 会记录 `initVal` 和 `syncVal`。同一条 HSK 链路中，VPP 和编码器两侧的有效 `wait/update` 同步寄存器都以 `initVal` 作为本轮起点；一帧正常完成后，应按各自的握手节奏推进到对应目标区间，不能要求多分支寄存器始终相等。这三个值都是 16 位无符号数，最大 `65535`，必须按模 `65536` 计算，例如 `65536 -> 0`、`65537 -> 1`，不能直接用十进制大小判断前后关系：

```text
init = initVal & 0xFFFF     # 握手起点
sync = syncVal & 0xFFFF     # 正常完成位置
reg  = RegVal  & 0xFFFF     # 待判定的同步寄存器

握手高度 = (sync - init) & 0xFFFF
当前进度 = (reg  - init) & 0xFFFF
```

例如 `initVal=8704`、`syncVal=10880` 时握手高度为 `2176`。该差值是本轮 HSK 的预期推进范围，通常是编码高度按 HSK 对齐规则后的行数，不能把它当作普通帧计数。编码侧 `syncVal` 一般对应 `ceil(EncH/64)*64` 的推进量；应以现场 `syncVal-initVal` 和 `minhskLin/sliceNum` 交叉核对，不要用未对齐的 `EncH` 替代。

判断规则：

- `当前进度 = 0`：寄存器位于 `initVal`，本轮尚未推进。
- `0 < 当前进度 < 握手高度`：寄存器处于本轮握手区间。
- `当前进度 = 握手高度`：寄存器到达 `syncVal`，本轮该侧握手完成。
- `当前进度 > 握手高度`：寄存器不在本轮 `initVal -> syncVal` 的有效区间，属于越界、旧值或同步状态异常，不能解释为正常帧内推进。

当 `sync < init` 时，本轮区间发生 16 位溢出。例如 `initVal=65000`、`syncVal=1000`，握手高度为 `(1000-65000)&0xFFFF=1536`；此时 `RegVal=200` 的当前进度为 `736`，仍位于合法握手区间。反之，若 `sync >= init`，本轮不跨界，正常寄存器值应处于 `[initVal, syncVal]`；小于 `initVal` 的值不能按正常溢出解释。

比较 `syncagent` 时，必须同时记录每个连接的 `Type=update/wait`、`ConId`、当前 `RegVal` 以及对应编码器 HSK 的 `initVal/syncVal`，并按上述 16 位模距离计算进度，不能只比较两个 `RegVal` 是否相等或直接比较数值大小：

- 对应生产侧/消费侧的有效 `update` 和 `wait` 按本轮节奏推进到目标区间：本帧握手完成；不能要求所有连接的寄存器在帧内任意时刻相等。
- 两侧都停在 `initVal`：本帧尚未开始，或上游没有产生新的同步事件；需结合业务计数判断。
- 生产侧 `update` 已到 `syncVal`，消费侧 `update/wait` 仍为 `initVal` 或更早位置：消费侧没有完成本轮握手，属于编码器输入/HSK wait 异常候选。
- 两侧当前进度都小于握手高度：只能说明当前可能处于帧内握手过程；连续两次不变才可判定推进停滞。
- 任一侧当前进度大于握手高度：该寄存器不在本轮有效区间，直接标记同步状态异常；再结合另一侧进度和业务计数定位责任模块。
- 生产侧和消费侧值不一致但都在推进：先按握手阶段分析；只有滞后持续存在，或生产侧已完成而消费侧未完成，才升级为异常。

`initVal`、`syncVal` 可能分别出现在 `syncagent` 会话/连接字段和 `venc/jenc` HSK STATUS 中；字段来源不同但应按同一条 `ConId/waitId/upId` 关系映射后再比较。若数值不在同一量纲或无法映射，报告“同步字段无法交叉映射”，不要强行比较。

#### 映射 syncagent 到编码通道

同步值是否正常不能只看是否到达 `syncVal`，还要按链路的生产和消费节奏判断当前帧是否应当等待。比较前必须用 `ConId`、`waitId/upId`、物理寄存器地址和 `initVal` 把 `syncagent` 行映射到具体编码通道，不能把不同 session 或不同分支的数值直接相减：

- `Line` 的初始窗口、VPP 的输出行步长、`ahead=(vpp_update-vpp_wait)&0xFFFF` 的下限、帧尾窗口例外，以及编码侧按 `minhskLin` 递增的节奏，都只在确认当前采样落在哪个帧阶段后才成立；这些帧阶段相关规则见 [references/hsk-design.md](references/hsk-design.md)，SKILL.md 不重复。
- `Line`、`minhskLin`、编码高度和 `syncVal-initVal` 不一致时，先报告 HSK 参数或版本配置不一致，不要直接判 VPP/VENC/JENC 硬件异常。

### 3.2 Offline 链路：业务计数与反压判定

`SW_Offline` 绑定的 IVPS→编码器链路没有握手寄存器，帧靠**同步回调携带共享内存块**派发：IVPS 侧 `ivps_link_dispatch` 在 `ax_ivps_sched_fifo_mgr.c` 触发，经 `ax_ivps_syslink.c` 的 `ax_link_dispatch` 同步调用 `ax_sys_link.c` 的目的端回调，VENC 侧落到 `VencCalLinkNotify`（`venc.c`），再走 `VENC_CAL_SendLinkFrame` → `pfnSubMitFrame` 送入编码。这条路径没有 ring/queue，所以判卡死只能顺着它看每一段计数是否推进：

1. IVPS 末尾 filter 是否在出图。对应 `(grp, chn)` 里 `FltId` 最大的一级才是进 link 的那一级，看它的 `InCnt/OutCnt`：`OutCnt` 不涨且 `InCnt` 也不涨 → `no_input`（该通道没有新输出，先看 VIN 与上游 filter）；`InCnt` 涨而 `OutCnt` 不涨 → `upstream_stall`（卡在 IVPS 这一级，看 `Fail1/Fail2`）。
2. IVPS `OutCnt` 在涨、目的编码通道 `FrmRecv` 不涨 → `link_dispatch_drop`。派发是同步回调，丢帧只在 syslog 里留 `Chn %d busy!` / `Chn %d full!`（`venc.c` 的 `VencCalLinkNotify_SendLinkFrameWithHandling`），IVPS 侧没有反压计数（`ivps_link_infifo_probe_callback` 恒返回 `FIFO_STATUS_NOT_FULL`），只能辅以 `ivps.chn_info` 的 `OutSts`/`OutDepth` 判断输出积压。
3. `FrmRecv` 在涨、`SubMitCnt` 不涨 → `downstream_stall`。看 VENC 的 `Send2EncFail/BufFullCnt/TimeOutCnt`；JENC 看 `BusyCnt` 与 `jenc.frame_list` 的 `busyCnt/freeCnt/HwState`，以及 `EncFail/TimeOutCnt/AbortCnt/BufOver`。
4. `SubMitCnt` 在涨、`stream_buf.ReadCycle` 不涨、`AvalRSize` 还在增加（或 `HwUsed=Y`）→ `stream_buf_backpressure`，优先判用户态取流/释放码流不及时，不要判编码硬件卡死。
5. 全链路都在涨 → `progressing`，只报「未发现停滞」，不要升级成卡死。
6. 缺少该链路 IVPS 或编码器对应通道的 proc、或两次采样对不齐 → `insufficient_evidence`，说明受限在哪，不要硬判。

判定的边界：

- **定位顺序按「分析顺序」执行**：先看编码器有没有收到帧，再判是哪一级停摆。上游某一级的计数冻结不等于这一级停摆，别把「计数不动」直接当结论。
- 只有 `SW_Offline` 走这条路径；`HW_Online`/`Mode_Unset` 只标注模式，不下数据流结论。脚本中 `offline_links[].verdict` 取 `no_input`/`upstream_stall`/`link_dispatch_drop`/`downstream_stall`/`stream_buf_backpressure`/`progressing`/`insufficient_evidence` 之一，非 `SW_Offline` 为 `null`。
- `no_input` 与 `insufficient_evidence` 只作信息呈现，不写成现场问题；只有另外四种卡死段构成要报的问题。
- 单次采样只能给出上下游计数的当前关系，`verdict` 要等第二次采样确认后才能写进结论。
- **判停滞前先对配置帧率**：慢不等于卡。IVPS 的 `FrcMode`/`Frc(src:dst)`（抽帧）与编码器的 `RcMode`/`SrcFr`/`DstFr` 是两处独立配置，`Frc` 抽到 1fps 时 JENC 的 `SrcFr/DstFr` 就是 `1/1`，两个 `OutFps` 都低仍属正常。只有当计数在两次采样间完全不动、且配置的目的帧率在采样间隔内本该出帧（目的帧率 × 间隔 ≥ 1 帧）时才判停滞；配置帧率本身很低时延长采样间隔再判，不要在低帧率链路上直接报 `upstream_stall`/`downstream_stall`。`evidence` 里的 `rate_hint` 已经带上这两处配置。

## 4. 卡死定位决策树

先按「分析顺序」判编码器有没有收到帧，再取对应步骤：收到了看编码器内部（步骤 5、7、8）与码流取出（步骤 6），没收到才往上游看（步骤 1--4）。先按链路模式分派，两类链路的规则不要混用：

- `SW_Low_Mem`/`SW_Low_Latency`（HSK）走下面全部步骤；其中步骤 2 的 `syncagent` 前置条件只对 HSK 链路成立。
- `SW_Offline` 走第 3.2 节的六步业务计数判定：步骤 1、4--8 与它同源（对应第 3.2 节的步 1--4），步骤 3 的握手节奏规则对它不适用。
- `HW_Online`/`Mode_Unset` 只标注模式，不下硬件卡死结论。

两类链路共存时分别输出两组结论，不要用一条链路的停滞去解释另一条。按数据流从上游到下游看，不要只看 VENC 的 `HwUsed`：

1. `ivps` 的组 `InCnt` 两轮增长但某个 filter/chn 的 `OutCnt` 不增长：问题模块优先判 IVPS（对应 `FltId/ChnId`）；初步原因是 VPP/VGP 处理、输出 FIFO 或下游反压。
2. 目标 HSK session 的 `State != 2`：问题模块优先 `syncagent` session/启动状态；先报告 session 未进入正常工作态，不按寄存器滞后直接归因于 VPP/VENC/JENC。
3. VPP/VENC 两侧 `wait/update` 的 16 位模进度异常（`ahead` 低于 `Line` 允许的窗口下限、编码侧没有按 `minhskLin` 步长推进、两侧进度差持续不收敛）：先区分 VPP 生产侧与 VENC 消费侧，不要越过它直接归因于编码硬件；这些规则依赖当前帧阶段，窗口与步进口径见 [references/hsk-design.md](references/hsk-design.md)。
4. IVPS 对应输出增长，而 VENC 的 `Send2EncCnt`/`FrmRecv` 不增长：问题在 link、VENC 输入接收或 HSK wait；核对 `link_table`、`syncagent` 的 `waitId/upId`。
5. VENC `Send2EncCnt` 增长但 `EncSucCnt` 不增长：问题模块优先 VENC 编码硬件/固件或 VENC HSK；若 `TimeOutCnt`、`ErrorCnt`、`Send2EncFail` 增长，直接报告对应错误方向。**注意「差一帧在途」形态**：`Send2EncCnt` 领先 `EncSucCnt` 恰好一帧且两轮不变、`HwUsed=Y`（硬件占着码流缓冲未归还）、编码侧 `update` 停在 `initVal` 而 VPP 侧 `update` 已推进——这一组证据合起来就是编码消费侧停滞的完整签名，直接判 VENC；此时 IVPS filter、其他通道计数跟着冻结属于下游停滞的反压传播，不是上游未供帧（判上游的前提是编码器 `FrmRecv` 本来就没涨，见「分析顺序」第 1 步），不要把整链冻结当成 VIN/ISP 输入问题。
6. VENC `EncSucCnt` 增长但 `ReadCycle` 不增长、`AvalRSize` 持续增加：编码已完成，优先判用户态取流/释放码流不及时，可能导致后续 stream buffer 满；不要判编码硬件卡死。
7. JENC `SubmitCnt`/`FrmRecv` 增长但 `SucCnt`、`RecvBsCnt` 不增长：问题模块优先 JENC；检查 `HwState`、`busyCnt`、`TimeOutCnt`、`EncFail`、`AbortCnt`、`BufOver` 和 JENC HSK `waitId/upId`。若 `bHsk=N` 或 `HwState=IDLE` 且输入本来未送入，不要判 JENC 硬件卡死。
8. JENC `FrmRecv` 增长而 `DiscardedNum`、`RatDrpCnt` 增长，`SucCnt` 也增长但明显低于输入：优先判帧率控制/丢帧策略，不直接判卡死；只有连续两轮所有有效输出都不增长才判停滞。
9. IVPS、VENC、JENC 业务计数在同一时间点全部停止，且 `syncagent` 的 `HoldCnt/ReleaseCnt` 也停止：优先判上游输入、全局同步代理或公共内存/调度问题；不能仅归因于编码器。
10. 只有一个分支停止，其他同一会话分支仍增长：优先判停止分支的消费者或该分支的 wait/链路。对一对二形态尤其检查 VENC/JENC 是否一支正常、一支停住。

## 5. 字段速查

- `link_table`: 真实模块连接和数据流模式；`SW_Low_Mem` 的 `Line` 是环形行数配置，不是帧计数。目的模块按用户侧命名把 JENC 和 H.26x 统一打印成 `VENC`，判编码分支看目的通道实际落在哪一侧编码 proc 里（采到 kernel 表时以 `Engine` 为准）。
- `link_table_kernel`: 比 `link_table` 多 `Engine(src->dst)`，用来在两侧编码 proc 都缺该通道时确认编码分支；`Engine` 优先级高于 `ModId`。
- `syncagent`: `SessId` 是同步会话；`update` 是当前侧更新事件，`wait` 是等待对端事件；`Cons`、`OppUpChn`、`OppWaitChn` 用来映射模块；`DoubleWait/ConWait` 是多等待关系的重要线索。
- VENC/JENC `HSK STATUS`: `bHsk` 表示通道是否启用 HSK；`srcNum` 表示参与同步的源数量；`hskCnt` 是 HSK 工作进度；`bFrmDrop/errDropCnt` 是丢帧线索；`conId/waitId/upId` 用来回查 syncagent。
- VENC `STATUS 0/2`: `Send2EncCnt`、`EncSucCnt`、`FrmRecv`、`RecvBsCnt`、`BsFrmCnt`、`OutFps` 分别反映送编码、编码完成、接收和码流完成；`SubMitCnt`/`SubMitFail`/`WaitEncFail`/`SeqDiscont` 是第 3.2 节 offline 判定的关键，其中 `WaitEncFail` 在 offline 路径正常恒为 0，增长即按异常升级。
- 编码 `RC ATTR`: VENC `CHN RC ATTR 1` 的 `RcMode`/`SrcFr`/`DstFr`/`TargetBitRate` 与 JENC `CHN RC ATTR` 的 `RcMode`/`SrcFr`/`DstFr` 是这一路编码的源/目的帧率配置，用于区分「配置的低帧率」与「真停滞」（第 3.2 节）。
- JENC `STATUS 1/2`: `SubmitCnt`、`SucCnt`、`EncFail`、`TimeOutCnt`、`BusyCnt`、`FrmRecv`、`DiscardedNum`、`RecvBsCnt` 是 JPEG 路径的核心进度字段；`jenc.frame_list` 的 `busyCnt`/`freeCnt`/`HwState` 是模块级编码状态。
- 编码 `stream_buf`: `ReadCycle`/`WriteCycle` 反映码流写入与取出是否推进，`AvalRSize` 是未取走的码流字节数，`HwUsed` 表示编码硬件正在占用码流缓冲（即编码正在硬件上跑）。
- IVPS `FILTER STATE`: `TotalCnt/InCnt/OutCnt` 判断处理是否前进；`Fail1/Fail2` 判断处理失败。
- IVPS `CHN INFO`: `OutSts` 和 `OutDepth` 判断输出积压；`FrcMode`/`Frc(src:dst)` 是该通道的抽帧配置（如 `RATIO 30.0:1.0` 表示每 30 帧取 1 帧），用来解释低 `OutFps`。

字段的精确枚举值以当前 SDK 版本 proc 输出为准；不要把 `State=2`、`RegVal`、物理地址或单次 `HwUsed=Y` 单独解释为卡死。

## 6. 输出格式

有两种输出模式，默认**简洁**。只有用户明确要求「详细输出」「完整报告」「展开讲」时才用详细模式；详细模式同样要精简，只写关键数字和结论，不复述 proc 原文，不把同一个事实说两遍。

两种模式都**禁止在输出里引用代码**：不写源码文件名、函数名、行号、宏名，也不用代码视角解释机制；证据只用 proc 的字段名和数字（如 `Send2EncCnt`、`OutCnt`、`hskCnt`）。

### 7.1 简洁模式（默认）

目标是：**有问题就给出最可能的问题模块、问题和怀疑点，没问题就一句话结论**。内容要一眼能读：一段只讲一件事，段与段之间留一个空行，不要把多个计数、多句判断挤成一行。不加标题、不用表格、不写「已确认事实/置信度」这类只有详细模式才有的段落。

```text
结论：最可能的问题模块是 <IVPS / H26x / JENC / syncagent / link 派发 / 上游输入 / 用户态取流>，卡在 <环节>。<一句话说清现象>

[形态：<仅在形态没闭合或与配置不一致时给出，说明缺什么依据>]

问题：<问题模块>：<一句话现象，带 1-2 个关键计数>

怀疑点：<最可能的阻塞位置，一句话依据>

[未决：<当前无法解释的矛盾，一句话>]

[还需补充：<只列会改变判断的具体项>]

HTML 报告：<HTML_REPORT 的绝对路径>
生成目录：<HTML_REPORT_DIR 的绝对路径>
```

- `结论` 必须点名**最可能的问题模块**，写清卡在哪个环节；多个模块同时可疑时按嫌疑从大到小写，先写第一个。不要只写「两个环节」「多处异常」这类没有模块名的结论。
- 只写结论、形态、问题、怀疑点、未决、还需补充、报告路径这几段，**每段一行到两行**，总长度控制在 10 行以内。不复述 proc 原文，不逐个通道罗列计数。
- 「问题」「怀疑点」「还需补充」三段**只在有问题时出现**：`issues` 里有「错误」或「高风险」级记录、`deltas.stalled_groups` 非空、offline `verdict` 落在四种卡死段之一、或有 `State != 2` 的 HSK session 时才写。同一个模块的多条同类问题合并成一段，不要逐条罗列。没有任何问题时不写这几段，也不需要解释为什么没问题。
- 「未决」只在存在无法自洽的矛盾（例如两侧计数互相冲突）时出现，一句话说清矛盾是什么、需要什么才能定性。
- 「形态」一行只在拓扑还有未闭合项时出现：`link_table_kernel` 未采集且目的端仍显示 `VENC`、`link_table 目的通道` 提示未解释、或 `link_table` 与 `syncagent` 矛盾。形态完全闭合时不写。
- 「还需补充」只列能改变本节结论的具体项（缺失模块、第二次采样），没有就不写。不要为了完整性列出「建议定期采样」这类不改变判断的内容。
- 不输出寄存器采集命令（`ax_lookat` 等），也不要求用户拿寄存器/硬件现场来定位。
- 不把「查 syslog」当成常规补充项：只有判到 `link_dispatch_drop` 这类除 syslog 外没有其他证据来源的结论时才提，且只说清在该场景下 syslog 里能看到什么现象，不要索要错误码、返回码或任务异常 status 值这类用户没提过的东西。
- 报告路径两行固定输出，原样给出脚本打印的绝对路径。

### 7.2 详细模式（用户要求时）

按以下字段逐行输出，每行一句话，只写关键数字：

```text
HSK形态：一对一 / 一对二 / 二对一 / 组合 / 当前信息不足（说明缺失依据）；没有 HSK 链路时填「无」。二对一的依据必须引用 link_table 的绑定关系，不能只写 srcNum=2
Offline链路：每条一行「<源> -> <目的>（<Mode>）：<verdict>，<一句话证据>」；没有非 HSK 绑定时填「无」，`HW_Online`/`Mode_Unset` 只标注模式、不下结论
配置帧率：IVPS 抽帧 `FrcMode`/`Frc(src:dst)` 与编码 `RcMode`/`SrcFr`/`DstFr`；链路帧率偏低时说明它是不是配置如此（只在这一项会改变判断时才写）
SDK 版本：<proc 或用户提供的版本字符串 / 未知（版本相关差异未经确认）>
已确认事实：已提供的拓扑、状态、错误字段和计数关系，只写支撑结论的那几条
当前推断：最可能的问题模块及阻塞位置；单次采样时明确标注“持续性待确认”
Session状态：目标 `SessId` 的 `State`；非 `2` 时说明同步 session 未正常工作；只有 HSK 链路有这一行，offline 链路填「不适用（无 HSK 会话）」
问题模块：IVPS / H26x / JENC / syncagent / link 派发 / 上游输入 / 用户态取流 / 无法确认
初步原因：一句话描述阻塞位置和最可能原因
置信度：高 / 中 / 低
还需补充：仅列出会改变或提高当前判断置信度的具体模块、字段、第二次采样或握手节奏；没有必要时填写“无”
HTML 报告：`HTML_REPORT` 输出的文件路径和 `HTML_REPORT_DIR` 输出的目录路径
```

置信度规则：高表示拓扑和关键动态计数均有交叉证据；中表示模块链路或错误字段明确，但缺少一个关键动态证据；低表示只有一次采样、信息不完整或多个模块同时停滞。低置信度也必须给出当前最可能模块和原因，不得只输出“无法分析”。

详细模式的 `问题模块` 一行必须先把最可能的模块写在最前面，`初步原因` 一句话说清卡在哪个环节。

## 7. 生成 HTML 报告

每次完成分析后都生成一个自包含 HTML 文件。章节顺序固定为**问题优先**：结论摘要 → 问题与依据 → 下一步 → 支撑快照。支撑快照（HSK 形态 / 握手基准 / syncagent 会话 / 跨采样差值 / Offline 链路）是同一批静态事实，与采样轮次无关：连续两次 `cat` 只为「跨采样差值」服务，不构成两套形态，不要按轮次重复贴同一张表。默认简洁模式把这批快照整体折叠，详细模式（`--detail`）展开并额外渲染逐条计数器差值与「解析范围」，末尾只附分析 JSON（不内联整份解析结果，那是上百 KB 的重复内容）；两种模式都只写关键数字，不把 proc 原文搬进报告。帧率配置（IVPS 抽帧、编码 `SrcFr/DstFr`）直接渲染在握手表与 offline 上下游单元格里，判读低 `OutFps` 时先看它。

报告正文由 `--analysis` 传入的 JSON 提供，其余部分脚本自己生成：`title`（省略时用默认标题）、`conclusion`、`summary`、`next_step`。`conclusion` 一句话且必须点名最可能的问题模块和卡住的环节；`summary` 每个主题独立成项，禁止把多个结论拼成一个长段落，每项不超过两句话，也不要在其中引用源码文件名、函数名或行号。简洁模式下 `summary` 只保留会改变判断的项（结论、形态、问题与怀疑点），把「已确认事实」这类支撑材料留给详细模式。

解析结果不需要手工搬运：`--proc` 传原始采样文件，脚本自己调用 `parse_hsk_proc` 补齐形态、握手高度、session 进度、offline 链路判定和 `issues`。已经生成过解析 JSON 时，把它的内容放到分析 JSON 的 `parse` 键下即可，`parse` 优先于 `--proc`。

```bash
python3 "$SKILL_DIR/scripts/render_hsk_html.py" \
    --proc /tmp/hsk_proc.txt \
    --analysis /tmp/hsk_analysis.json
```

用户要求详细报告时追加 `--detail`。不传 `--output-dir` 时写入 `$SKILL_DIR/reports/`；用户指定目录时再加 `--output-dir <用户目录>`。必须把脚本输出的 `HTML_REPORT` 和 `HTML_REPORT_DIR` 原样转换为最终回复中的路径提示，例如：`HTML 报告已生成：/abs/path/reports/ax615-ivps-venc-diagnose-....html`、`生成目录：/abs/path/reports/`。

## 参考资料

详细故障矩阵见 [references/diagnosis-matrix.md](references/diagnosis-matrix.md)，工作模式和异常恢复规则见 [references/hsk-design.md](references/hsk-design.md)。

## 测试

`tests/` 是开发期回归测试：`tests/fixtures/hsk_proc_single_sample.txt` 保存一路真实采样，测试用它对齐字段宽度、列表列和握手高度计算，并用行级替换构造异常输入验证判定分支；`link_table_kernel` 的用例按 SDK 的打印格式构造，用于覆盖 Engine 合并与 `ModId`/`Engine` 冲突；offline 用例按第 3.2 节的每种 `verdict` 构造差值输入（fixture 里的 `IVPS 0/2 -> VENC 0/2` 就是 `SW_Offline`）；报告渲染的用例用同一份 fixture 校验 HTML 的形态表、握手表、offline 链路表和缺采样提示。它不是用户输入目录，也不是运行时必需依赖。运行：

```bash
python3 -m unittest discover -s "$SKILL_DIR/tests" -v
```

## 回归自检

`evals/` 存放 Golden Case，用于在修改判定规则、决策树或 `references/` 知识后确认没有退化。每个 Case 目录分两个区：

- `input/`：现场采样（`hsk_proc.txt`），分析阶段唯一可读的内容。
- `answer/`：`manifest.yaml`（含 `title`/`category`）、`oracle.yaml`，即答案与元数据，只在评分阶段读取。

当前 Case：`ivd-001`～`ivd-006`，配比与填充状态见 [evals/README.md](evals/README.md)。每个 Case 具体考什么写在它自己的 `answer/manifest.yaml` 里，本文件不复述，以免自检前泄露答案。

### 盲测纪律

答案与输入同在本 Skill 目录内，隔离靠执行顺序保证，不靠目录边界。因此：

**进入评分阶段之前，不得以任何方式读取该 Case `answer/` 目录下的任何文件（`case.yaml`、`oracle.yaml`），也不得通过检索猜测答案。** 一旦提前读取，这次自检结论作废，必须换一个未读过答案的 Case 重跑。

### 执行

1. 预检 Case，参数是 Case ID 或目录：

   ```sh
   python3 "$SKILL_DIR/scripts/validate_case.py" ivd-001
   ```

   失败时输出 `ERROR` 和缺陷，不进入分析。预检只打印 `input/` 文件清单，不打印 `answer/` 下任何路径。

2. 运行输入完整性检查：

   ```sh
   python3 "$SKILL_DIR/scripts/check_input.py" <case-dir>/input
   ```

   返回 `PASS`（可附带 `NOTE`，如单次采样限制）后按本文档「分析顺序」和「卡死定位决策树」正常分析；返回 `INCOMPLETE` 时按 NOTE/补采指令处理，不凭残缺输入断言卡死。

3. 只读取预检给出的 `analyzer_visible` 文件完成分析，把自己当作没有答案的分析者，不打开 `answer/` 目录；将分析输出**冻结**为 `analyzer_result`。冻结后不得依据答案补写、删改或重跑。

4. 此时才读取该 Case 的 `answer/oracle.yaml`。先校验，再按 [references/grading.md](references/grading.md) 做语义对比：

   ```sh
   python3 "$SKILL_DIR/scripts/validate_oracle.py" <case-dir>/answer/oracle.yaml
   ```

5. 输出结论：

   ```text
   Case: <id>
   Verdict: PASS | FAIL | ERROR

   Analyzer result:
   <第 3 步冻结的原始输出>

   Comparison:
   - Root cause: PASS | FAIL — <原因>
   - Required concepts: PASS | FAIL — matched [...]; missing [...]
   - Forbidden conclusions: PASS | FAIL — asserted [...]
   - Evidence grounding: PASS | FAIL — <原因>
   - Confidence: PASS | WARN — expected <...>; actual <...>

   Summary: <一两句话>
   ```

`Analyzer result` 必须原样保留。批量跑多个 Case 时逐 Case 输出，再汇总 `total/pass/fail/error`；一个 Case 的 oracle 不得用于评判另一个 Case。`FAIL` 表示分析结果不符合 oracle，`ERROR` 表示 Case、输入或流程无法完成，两者不可互换。关键故障用例（如 `ivd-001`）一票否决：出现一次 FAIL 即判定未达标，不得通过多次运行取多数掩盖。

### 维护

新增 Case 按第 1 节 SOP 采集（或按 tests/ 的差分拟合方式派生并在 `answer/manifest.yaml` 标注来源类型 captured / derived / synthetic）。每个 Case 目录固定两个区：`input/` 放 `hsk_proc.txt`，`answer/` 放 `manifest.yaml`、`oracle.yaml`（元数据不叫 `case.yaml`——该名字保留给 Case 根目录的 axap-eval 外壳，`answer/` 内出现 `case.yaml` 可能让评测工具的用例发现失败）。`manifest.yaml` 的 `separation.analyzer_visible` 只能列 `input/` 下的文件，`separation.evaluator_only` 只能列 `answer/` 下的文件且必须包含 `answer/manifest.yaml`，`oracle` 指向 `answer/oracle.yaml`；预检脚本会强制这些约束。除用户明确要求，自检过程不修改 `input/`、`answer/` 或本 Skill 知识。
