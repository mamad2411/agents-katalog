---
name: sdk-dataflow-analysis
description: 分析 AX615/MC20L 模块间数据流转日志，定位 AX_SYS_Link_V2、HSK、LowMem/LowLatency/Offline link 参数或硬件拓扑约束导致的启动失败、断流或卡死，并对 HSK 建链后断流/不出流做机制分流。用户提供 FRTDemo、SYS、VIN、IVPS、VENC 日志并询问数据流、Link、HSK 或模块绑定问题时使用；先检查输入完整性，缺失时提示并在板端补采；当前知识覆盖 AX_SYS_Link_V2 参数检查、IVPS→VENC/JENC HSK 资源冲突、HSK 参数切换时序，以及 HSK 断流现象到机制候选的分流。用户要求跑 AXDF Golden Case、回归自检或评估分析准确性时，按「回归自检」执行 evals/ 下的盲测。
---

# AX 数据流日志分析

从日志证据定位模块间数据流转问题。当前覆盖 `AX_SYS_Link_V2` 参数错误、IVPS→VENC/JENC HSK 硬件拓扑约束、HSK 模式下的参数切换时序，以及 HSK 建链后断流/不出流的机制分流；没有足够证据时输出缺失项，不把相邻报错当作根因。

## 输入完整性门禁

分析前必须先运行：

```sh
python3 <skill-dir>/scripts/check_input.py <input-dir>
```

其中 `<skill-dir>` 是当前 `SKILL.md` 所在目录。

完整输入必须同时包含且通过内容检查：

- `serial.log`：应用从启动到异常发生后的连续串口信息；
- `syslog.log`：覆盖同一复现窗口的板端 syslog；
- `logctl.proc`：VIN、IVPS、VENC 的 userlog 均为 info，即当前固件的 `level(U)=6`；
- `vin.proc`：VIN attr、statistics、mode、ife_itp_hsk；
- `ivps.proc`：IVPS 和 ivps_sched；
- `venc.proc`：VENC；
- `link.proc`：link_table、link_table_kernel、vin_ivps_mode、syncagent。

检查返回 `PASS` 后才能进入问题分析。返回 `INCOMPLETE` 时：

1. 原样输出检查脚本给出的缺失项和补采指令，不对残缺输入推断根因。
2. 已有目标板会话和复现命令时，按 [references/input-completeness.md](references/input-completeness.md) 在板端补采，并写入上述固定文件名；补采前必须设置并验证 VIN、IVPS、VENC userlog 为 info。
3. 如果应用现场仍在，允许只补抓缺失的 proc；如果现场已结束，或缺失 `serial.log`、`syslog.log`，重新复现并采集完整一组，避免混用不同轮次证据。
4. 没有目标板连接信息或复现命令时，给出补采指令，并只询问这一项必要信息；不得创建空文件代替证据。
5. 补采完成后再次运行检查脚本。仍未通过时继续补采，不进入后续分析。

## 分析流程

1. 将串口、syslog 和 proc 按采集时间关联，保留日志原始时间顺序，识别首个失败点。优先找 `AX_SYS_Link_V2`、`Linkage setup`、`Linkage failed`，再看上层 `PPL build failed` 等传播结果。
2. 从日志提取 source/destination module tuple、flow mode、`nRingLineCnt`、source/destination engine、编码类型和返回码。对 IVPS 分流按 group 汇总同时工作的各 channel，检查它们最终占用的 VENC/JENC engine。日志未打印某字段时标记“未知”，不要从场景名或 token 猜值。
3. 出现 HSK、断流、不出流、无码流或 VPP timeout 等现象时，先读 [references/hsk-stream-failure-patterns.md](references/hsk-stream-failure-patterns.md) 选机制类。若该类涉及 Link 参数、engine 绑定或切换时序，再读 [references/ax-sys-link-v2.md](references/ax-sys-link-v2.md) 核对细则；若有 venc HSK STATUS / STREAM BUF，再读 [references/venc-hsk-proc.md](references/venc-hsk-proc.md)。同一失败点只许一个主根因。
4. 区分直接证据与推断：底层参数校验日志是直接原因；已建链场景中的 engine 拓扑、两路编码类型和首个 HSK/VPP timeout 可共同证明硬件资源冲突。FRTDemo 构建失败、继续启动、进程退出、pool 耗尽或无流通常是传播结果。应用继续运行不等于数据流正常。
5. 只在日志能唯一支持时给出确定结论。多个原因仍可能成立时列出候选，并给出最小补充日志命令。
6. 输入含 proc 时交叉验证：VIN/IVPS/VENC 的帧计数和接收状态，以及失败 Link 是否缺失于 `link_table`。`venc.proc` 的 H26X HSK STATUS 按 [references/venc-hsk-proc.md](references/venc-hsk-proc.md) 判读握手是否推进、配对是否错位，表头以代码为准而非文档截图。proc 是采集时刻的状态证据；不能用晚于首错的 proc 覆盖更早的日志因果顺序。

## 输出

按以下字段回答，保持简短：

- `结论`：最可能的根因，指出错误字段、日志可见的实际值和约束；实际值未打印时明确写“未知”，证据不足时写 `INCONCLUSIVE`。
- `证据`：引用 2–4 条关键日志，按因果顺序排列。
- `分析`：说明底层错误如何传播成用户现象。
- `修正建议`：给出最小配置修正；不要修改现场或代码，除非用户另行要求。
- `置信度`：高/中/低。只有底层错误与文档约束互相印证时才可判高。
- `缺失信息`：仅在影响结论时列出需要补充的日志或 proc 信息。

相关 `ppl.json` 的 `src_mod`、`dst_mod`、`link_attr` 不属于七项硬门禁，但日志没有打印 Link 参数、影响唯一归因时仍需补充。

## 回归自检

`evals/` 存放 Golden Case，用于在修改分析流程或 `references/` 知识后确认没有退化。每个 Case 目录分两个区：

- `input/`：现场材料，分析阶段唯一可读的内容。
- `answer/`：`case.yaml`（含 `title`/`category`）、`oracle.yaml`、`reproducer.patch`，即答案与元数据，只在评分阶段读取。

当前有 9 个 Case：`AXDF-001`、`AXDF-002`、`AXDF-003`、`AXDF-004`、`AXDF-005`、`AXDF-006`、`AXDF-007`、`AXDF-008`、`AXDF-009`。每个 Case 具体考什么写在它自己的 `answer/case.yaml` 里，本文件不复述，以免自检前泄露答案。

### 盲测纪律

答案与输入同在本 Skill 目录内，隔离靠执行顺序保证，不靠目录边界。因此：

**进入评分阶段之前，不得以任何方式读取该 Case `answer/` 目录下的任何文件（`case.yaml`、`oracle.yaml`、`reproducer.patch`），也不得通过检索猜测答案。** 一旦提前读取，这次自检结论作废，必须换一个未读过答案的 Case 重跑。

### 执行

1. 预检 Case，参数是 Case ID 或目录：

   ```sh
   python3 <skill-dir>/scripts/validate_case.py AXDF-001
   ```

   失败时输出 `ERROR` 和缺陷，不进入分析。预检只打印 `input/` 文件清单，不打印 `answer/` 下任何路径。

2. 只读取预检给出的 `analyzer_visible` 文件，按本文档「输入完整性门禁」和「分析流程」正常分析。此阶段把自己当作没有答案的分析者，不打开 `answer/` 目录。

3. 将分析输出**冻结**为 `analyzer_result`。冻结后不得依据答案补写、删改或重跑。

4. 此时才读取该 Case 的 `answer/oracle.yaml`。先校验，再按 [references/grading.md](references/grading.md) 做语义对比：

   ```sh
   python3 <skill-dir>/scripts/validate_oracle.py <case-dir>/answer/oracle.yaml
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

`Analyzer result` 必须原样保留。批量跑多个 Case 时逐 Case 输出，再汇总 `total/pass/fail/error`；一个 Case 的 oracle 不得用于评判另一个 Case。`FAIL` 表示分析结果不符合 oracle，`ERROR` 表示 Case、输入或流程无法完成，两者不可互换。

### 维护

新增 Case 或补采现场材料按 [references/golden-capture.md](references/golden-capture.md) 收集串口、syslog、logctl 和数据流模块 proc，并在 `answer/case.yaml` 记录来源与缺失项。每个 Case 目录固定两个区：`input/` 放现场材料，`answer/` 放 `case.yaml`、`oracle.yaml`、`reproducer.patch`。`case.yaml` 的 `separation.analyzer_visible` 只能列 `input/` 下的文件，`separation.evaluator_only` 只能列 `answer/` 下的文件且必须包含 `answer/case.yaml`，`oracle` 指向 `answer/oracle.yaml`；预检脚本会强制这些约束。除用户明确要求，自检过程不修改 `input/`、`answer/` 或本 Skill 知识。

