---
name: sdk-venc-rc-config-audit
description: 审查 AX615/AX VENC 码控配置和可选码流结构。用户提供 `/proc/ax_proc/venc`、VENC RC 参数、码流文件，或描述呼吸效应、码率偏高/超出、竞品对比、GOP/IP 比例、帧率异常等问题时使用；解析单次 proc，不要求两次采样，并在有码流时调用 ffprobe 分析实际 GOP、I/P/B 帧、帧大小、码率和时间戳，再结合编码模式给出证据、风险和修改建议。用户要求跑 RC Golden Case、回归自检或评估审查准确性时，按「回归自检」执行 evals/ 下的盲测。
---

# AX615 RC Config Audit

## 目标

把一次配置审查拆成两种证据：

1. 单次 proc：判断字段是否合法、字段之间是否矛盾、当前模式下哪些参数生效。
2. 可选码流：用 `scripts/analyze_bitstream.py` 统计实际结构和码率，验证问题描述。

当用户只提供 proc 而未描述现象时，完成配置审查后询问具体遇到的问题，再决定是否需要码流分析。

## 脚本执行约定

`scripts/` 与本 SKILL.md 在同一目录内，脚本不依赖当前工作目录。执行前先把本 SKILL.md 所在目录的绝对路径导出为 `SKILL_DIR`，后续命令一律用 `"$SKILL_DIR/scripts/<脚本名>"` 调用：

```bash
export SKILL_DIR="<本 SKILL.md 所在目录的绝对路径>"
```

不要写死路径，也不要先 `cd` 到 skill 目录再用相对路径执行；用户数据文件（proc 文本、码流、报告输出目录）仍按用户给出的路径解析，与 `SKILL_DIR` 无关。

## 报告输出目录

报告默认写入本 skill 的 `reports/` 目录（`$SKILL_DIR/reports/`），与执行时所在的工作目录无关；该目录已随 skill 建好，脚本会自动创建。用户指定目录时用用户的目录，不要写死其他路径。脚本执行后会打印 `HTML_REPORT` 和 `HTML_REPORT_DIR`，回复中原样给出这两个绝对路径。

## 工作流

### 1. 收集输入

- 接受用户粘贴的一次 `/proc/ax_proc/venc` 输出；一次 `cat` 足够。
- 若有码流，记录文件路径、封装格式、编码格式和采样时长。裸 H.264/H.265 必要时给 ffprobe 增加 `-f h264` 或 `-f hevc`。
- 记录用户明确提出的现象；没有现象时只做配置审查，不虚构问题。

### 2. 解析 proc

运行：

```bash
python3 "$SKILL_DIR/scripts/parse_venc_proc.py" --input proc.txt --pretty
```

也可以通过 stdin 输入。脚本输出规范化 JSON，保留原始未知字段，便于兼容不同 SDK 版本。重点读取：通道属性、RC ATTR 1/2/3、GOP ATTR、RJ&SupFrm、ROI、USER QPMAP1/2/LocalMap、SVC PARAM/REGION（智能编码）、JENC RC ATTR、`STATUS 2` 的 `RecvFps/OutFps/BitRate(kbps)`；也识别另一实现的 `H26X RC CTRL0/1/2`。

`SVC PARAM INFO` 和 `SVC REGION INFO` 是多行记录：每多一个 `TypeId`／`RectIdx` 就多一行，且该行前面的列全部留空。脚本按列宽把续行并回上一条记录，输出为 `svc_param.types[]` 和 `svc_region[].rects[]`；续行无法对齐表头时会给出「错误」级问题，不静默丢弃。

### 2.1 确认 SDK 版本

`environment.sdk_version` 来自 proc 头部的 `[SDK version]` 行，`environment.sdk_version_source` 记录取值来源。识别到版本时，在结论中原样引用该字符串，并据此判断字段差异是版本行为还是配置问题。

proc 未输出版本行时脚本输出 `unknown` 并追加一条「提示」级问题。此时按以下顺序补齐，取到即停：

1. 让用户执行 `cat /proc/ax_proc/version`（或该 SDK 对应的版本节点）并粘贴结果；
2. 在提示词注入或用户指定的 SDK 包内检索版本文件名（如 `version.mk`、`ax_version.h`）取版本号；
3. 仍无法确认时，把版本记为「未知」，并在结论中标注「版本相关差异未经确认」，不按某个具体版本的行为下判断。

### 3. 按模式审查

先根据编码格式和 `RcMode` 选择 [references/rc-mode-matrix.md](references/rc-mode-matrix.md)，再应用公共规则：

- `MinQp <= MaxQp`，`MinIQp <= MaxIQp`，且值在 0..51；
- `SrcFr/DstFr` 必须为正；用 `RecvFps` 对比 `SrcFr`，用 `OutFps` 对比 `DstFr`，偏差超过 10% 报告提示；
- CBR/AVBR 用 `TargetBitRate`，VBR/CVBR 用 `MaxBitRate` 与实际 `BitRate(kbps)` 对比；超过上限 10% 才报告高风险，避免把单点瞬时值当长期超码率；
- 帧率、分辨率、GOP 和目标/最大码率必须为正且相互可解释；
- 只评价当前模式会读取的字段，其他模式字段标记为“不适用”；
- `-`、空值或 proc 未输出字段标记为“未知”，不能当作 0；
- API 声明但当前 proc 未暴露的模式，标记“支持状态需版本确认”，不套用其他模式规则。

再检查叠加在 `RcMode` 之上的 QP 干预（两者可同时存在，判定阈值见 rc-mode-matrix.md）：

- 出现 `USER QPMAP1/2/LocalMap` 表即说明外部 QP map 已挂上；核对 `MbWidth/MapSize` 为正、`QpMapPhyAddr` 非 0；`UseMbuf=N` 时 `BlkId=-1` 是正常值。map 的 block unit、QP 类型和 QPMAP mode 不在 proc 输出中，需要时向用户索取 API 侧配置，不要凭 proc 推断；
- 出现 `SVC PARAM/REGION INFO` 表即说明智能编码已使能。这里的 SVC 指**智能编码**（背景与区域 QP 分配），不是手册第 10 章的 SVC-T 时域分层编码，不要套用 SVC-T 规则；
- 判断智能编码 QP 前必须先读 `AbsQp`：`Y` 为绝对 QP `[0,51]`，`N` 为相对 deltaQp `[-51,51]`；把负 delta 当越界是典型误判；
- 核对 `TypeNum` 在 `[1,5]`、`RectNum` 不超过 32，且续行数与之一致；`RIdx/WIdx/IsFull/ResIdx` 是区域信息的缓存指针和槽位，不是通道号或帧号；
- `RC ATTR 1` 的 `SvcEn` 应与是否输出 SVC 表一致，不一致时报告并要求确认使能状态。

### 4. 有码流时分析

运行：

```bash
python3 "$SKILL_DIR/scripts/analyze_bitstream.py" stream.mp4 --pretty
```

脚本调用 `ffprobe`，统计实际关键帧间隔、GOP 长度、I/P/B 帧数量和大小、I/P 码量比例、平均码率、帧率和时间戳连续性。把结果与 proc 的 `Gop/GopMode`、`SrcFr/DstFr`、`RecvFps/OutFps`、`TargetBitRate/MaxBitRate/BitRate(kbps)` 逐项对照；详细指标和限制见 [references/bitstream-analysis.md](references/bitstream-analysis.md)。

### 5. 根据现象触发规则

按 [references/symptom-rules.md](references/symptom-rules.md) 输出：

1. 现象和证据；
2. 明确异常字段或“不足以确认”的原因；
3. 可能根因，按置信度排序；
4. 修改建议，包括参数方向、建议范围和副作用；
5. 下一步需要的输入（码流、画面、QP 日志或场景信息）。

建议等级：`错误`（越界/明显矛盾）、`高风险`（很可能造成所述问题）、`提示`（可优化）、`信息`（正常或不适用）。

### 6. 生成 HTML 报告

每次完成分析后都生成一个自包含 HTML 文件。将终端结论整理为 JSON，至少包含 `title`、`conclusion`、`summary`、`channels`、`issues`、`suggestions`、`next_step`；把解析脚本输出的 `environment` 原样带上（或用顶层 `sdk_version` 覆盖），报告头部会展示 SDK 版本。可用 `source` 标记输入来源、用通道的 `assessment` 标记判断。`summary` 优先使用 `[{"label": "通道 0", "text": "配置说明"}]`；使用字符串时，每行只写一个通道或一个主题，并采用 `标签：内容` 格式。完成标准是 HTML 中每个摘要主题独立成行，禁止把多个通道拼成一个长段落。然后运行：

```bash
printf '%s' '<analysis-json>' | python3 "$SKILL_DIR/scripts/render_audit_html.py"
```

不传 `--output-dir` 时写入 `$SKILL_DIR/reports/`；用户指定目录时再加 `--output-dir <用户目录>`。必须把脚本输出的 `HTML_REPORT` 和 `HTML_REPORT_DIR` 原样转换为最终回复中的路径提示，例如：`HTML 报告已生成：/abs/path/reports/ax615-rc-audit-....html`、`生成目录：/abs/path/reports/`。

## 输出格式

```text
结论：<正常 / 存在异常 / 需要结合问题继续分析>

SDK 版本：<proc 或用户提供的版本字符串 / 未知（版本相关差异未经确认）>

配置摘要：每个通道独立一项，分别列出 codec、分辨率、fps、RcMode、GOP、码率和 QP 范围；跨通道运行状态另列一项

问题清单：
- [等级] 通道/字段：观测值；规则或码流证据；影响

修改建议：
- 参数：从什么方向调整；适用条件；副作用

后续：用户未描述现象时，询问具体问题；用户描述码率/GOP/IP 比等码流问题时，再调用 ffprobe 分析

HTML 报告：`HTML_REPORT` 输出的文件路径和 `HTML_REPORT_DIR` 输出的目录路径
```

## 参考资料

- 码控手册（审查 CBR/VBR/AVBR/CVBR、QPMAP、智能编码、GOP、I/P 比、呼吸效应或码率策略时加载）：[AX 码率控制模式与参数使用指南](references/ax-rate-control-manual.md)。公共参数只在第 3 章统一说明；QPMAP 在第 8 章、智能编码（SVC）在第 9 章、GOP 在第 10 章，专项问题和参考配置在后续章节补充。
- 详细规则：[references/rc-mode-matrix.md](references/rc-mode-matrix.md)、[references/symptom-rules.md](references/symptom-rules.md)。

需要核对 SDK 实现时，在用户指定或提示词注入的 SDK 包内按文件名检索，不假设固定目录结构：`ax_venc_rc.h`（API 模式和字段、QPMAP 枚举）、`ax_venc_comm.h`（智能编码 `AX_VENC_SVC_*` 结构和取值域）。proc 的输出分支、字段宽度和参数校验行为不在对外头文件中，只能从实际 proc 输出和 API 返回值反推，不要凭空断言。未提供 SDK 包时，只依据 proc 输出和上述参考资料给出结论，并标注结论未经源码核对。

## 测试

`tests/` 是开发期回归测试：保存脱敏 proc/ffprobe 记录和预期 JSON，验证版本差异、占位符和各码控模式不会导致解析回归。它不是用户输入目录，也不是运行时必需依赖。运行：

```bash
python3 -m unittest discover -s "$SKILL_DIR/tests" -v
```

## 回归自检

`evals/` 存放 Golden Case，用于在修改审查规则、references 知识或解析脚本后确认没有退化。每个 Case 目录分两个区：

- `input/`：现场 proc 快照（`venc_proc.txt`），分析阶段唯一可读的内容；现场现象（用户反馈）由任务提示词提供，不在 proc 内。
- `answer/`：`manifest.yaml`（含 `title`/`category`）、`oracle.yaml`，即答案与元数据，只在评分阶段读取。

当前 Case：`rc-001`～`rc-006`，配比与填充状态见 [evals/README.md](evals/README.md)。每个 Case 具体考什么写在它自己的 `answer/manifest.yaml` 里，本文件不复述，以免自检前泄露答案。

### 盲测纪律

答案与输入同在本 Skill 目录内，隔离靠执行顺序保证，不靠目录边界。因此：

**进入评分阶段之前，不得以任何方式读取该 Case `answer/` 目录下的任何文件（`manifest.yaml`、`oracle.yaml`），也不得通过检索猜测答案。** 一旦提前读取，这次自检结论作废，必须换一个未读过答案的 Case 重跑。

### 执行

1. 预检 Case，参数是 Case ID 或目录：

   ```sh
   python3 "$SKILL_DIR/scripts/validate_case.py" rc-001
   ```

   失败时输出 `ERROR` 和缺陷，不进入分析。预检只打印 `input/` 文件清单，不打印 `answer/` 下任何路径。

2. 运行输入完整性检查：

   ```sh
   python3 "$SKILL_DIR/scripts/check_input.py" <case-dir>/input
   ```

   返回 `PASS`（可附带 `NOTE`，如缺版本行）后按本文档工作流正常审查；返回 `INCOMPLETE` 时按补采指令处理，不凭残缺输入断言。

3. 只读取预检给出的 `analyzer_visible` 文件，结合任务提示词中的现场现象完成审查，把自己当作没有答案的分析者，不打开 `answer/` 目录；将审查输出**冻结**为 `analyzer_result`。冻结后不得依据答案补写、删改或重跑。

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

`Analyzer result` 必须原样保留。批量跑多个 Case 时逐 Case 输出，再汇总 `total/pass/fail/error`；一个 Case 的 oracle 不得用于评判另一个 Case。`FAIL` 表示审查结果不符合 oracle，`ERROR` 表示 Case、输入或流程无法完成，两者不可互换。关键故障用例（如 rc-001）一票否决：出现一次 FAIL 即判定未达标，不得通过多次运行取多数掩盖。

### 维护

新增 Case 按 SKILL.md 第 1 节采集（或按 tests/ 的构造方式派生并在 `answer/manifest.yaml` 标注来源类型 captured / derived / synthetic）。每个 Case 目录固定两个区：`input/` 放 `venc_proc.txt`，`answer/` 放 `manifest.yaml`、`oracle.yaml`（元数据不叫 `case.yaml`——该名字保留给 Case 根目录的 axap-eval 外壳，`answer/` 内出现 `case.yaml` 可能让评测工具的用例发现失败）。`manifest.yaml` 的 `separation.analyzer_visible` 只能列 `input/` 下的文件，`separation.evaluator_only` 只能列 `answer/` 下的文件且必须包含 `answer/manifest.yaml`，`oracle` 指向 `answer/oracle.yaml`；预检脚本会强制这些约束。除用户明确要求，自检过程不修改 `input/`、`answer/` 或本 Skill 知识。
