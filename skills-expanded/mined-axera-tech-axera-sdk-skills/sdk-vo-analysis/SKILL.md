---
name: sdk-vo-analysis
description: AX615 芯片（含项目代号 MC20L）VO（视频输出）模块问题诊断与配置生成（仅适用于 AX615 芯片，AX615D/AX615Q）。两类任务入口：(1) 诊断——客户报告 ax615/AX615 VO 相关问题（黑屏、无输出、花屏、闪烁、撕裂、颜色异常、帧率不对、VO 初始化/使能失败、SendFrame2Disp 超时等），或提供图像现象、proc 信息、调用 SDK 接口的代码、日志要求排查 VO 问题时，按「诊断流程」输出有证据支撑的排查结论（四种终态：原因与修复建议 / 信息不足继续追问 / 原因未知 / 场景无法实现）；(2) 配置生成——客户在已知应用场景（芯片型号、输出接口、分辨率/帧率、屏规格、源色域）下需要生成 VO 初始化流程配置（Init→SetPubAttr→SetDataPinMap→SetCSC→Enable→SendFrame2Disp 的参数取值、C/Python 代码骨架、送帧建议）时，按「生成流程」输出标注证据等级的配置（已验证表条目 ＞ SDK 预设模式（预设名由公开头文件确认，能力/PCLK 仍须按当前 SDK 核验） ＞ 推导值）。内化 AX615 VO 公开头文件、54 组已验证时序表、官方 sample 19 组时序、PCLK 离散档位表、版本化行为摘要与 V3 全系版本历史（不依赖外部本地源码目录）。问题明显非 ax615 芯片、或芯片型号模糊不清时，回答中必须显式声明本 skill 的适用范围。
---

# AX615 VO 模块问题诊断与配置生成

目标：一个 skill 覆盖 AX615 VO 的两类任务——**诊断**（为什么会坏）与**配置生成**（怎么配才对）。进入时先判断任务类型：客户报告问题/要求排查 → 诊断流程；客户要生成配置/参数 → 生成流程。

## 适用范围（AX615 限定）

本 skill **仅用于 AX615 芯片（AX615D/AX615Q）的 VO 模块分析**。**MC20L 是 AX615 的项目/市场代号（MC20L = AX615），客户提及 MC20L 时按 AX615（D/Q）正常处理，不视为其他芯片**。回答前先核对芯片型号，命中以下情形时必须在回答中**显式声明适用范围**：

- **明显非 ax615 芯片**（如 AX620/AX630/AX650 等其他 SoC 型号）：回答开头显式声明"本 skill 仅适用于 AX615 芯片（AX615D/AX615Q），当前问题涉及的 <芯片型号> 超出适用范围"。不得把本 skill 的约束、时序表、错误码直接套用到该芯片；如需给出同类排查思路，必须注明未经本 skill 证据验证。
- **芯片型号模糊不清**（客户未说明、且日志/proc 无法确认型号）：回答开头显式声明"本 skill 仅适用于 AX615 芯片；当前芯片型号未知，以下分析仅在确认芯片为 AX615（D/Q）时适用"，并请客户先确认芯片型号。
- **已确认是 AX615（D/Q）**：正常按对应流程分析，结论中注明芯片型号。

核心资源（本工作区）：
- **知识目录按项目区分**：`references/ax615/` 存放 AX615 项目的内化知识；后续支持其他项目时在 references/ 下增加平级目录（如 `references/<project>/`），引用与检索按项目目录选择，不得跨项目混用
- MCP 知识库（可选）：由运行环境配置的 AX615 知识库，检索脚本 [scripts/kb_query.py](scripts/kb_query.py)
- **已内化的知识（skill 自包含，优先用内化副本）**：
  - [references/ax615/vo-timing-table.json](references/ax615/vo-timing-table.json) — 54 组已验证时序表（条目名保留原 key；**SDK V3.14.0 实现行为，需按版本核验**）
  - [references/ax615/sample-vo-timings.json](references/ax615/sample-vo-timings.json) — 官方 sample 内置 19 组时序 + 与 54 组表的差异说明（**不静默合并**）
  - [references/ax615/vo-pclk-table.json](references/ax615/vo-pclk-table.json) — PCLK 5×16 完整离散档位表（80 槽位/62 可达值，来源标注固定为 **SDK V3.14.0 实现行为，需按版本核验**）
  - [references/ax615/vo-sdk-behavior-notes.md](references/ax615/vo-sdk-behavior-notes.md) — 版本化行为摘要（**已授权源码核验的 SDK 行为约束**，每条均带固定版本标注；不含实现路径/文件/符号/行号）
  - [references/ax615/vo-api-inline.md](references/ax615/vo-api-inline.md) — ax_vo_api.h/ax_global_type.h 关键定义逐字副本（结构体、错误码、CSC 矩阵、色域枚举）
  - [references/ax615/vo-constraints.md](references/ax615/vo-constraints.md) — 诊断约束速查（调用顺序、接口限制、时序/时钟规则、CSC、SendFrame2Disp、proc 判据）
  - [references/ax615/vo-config-reference.md](references/ax615/vo-config-reference.md) — 配置生成速查（结构体/枚举/能力矩阵/生成自检/错误码速查）
  - [references/ax615/sdk-inline/ax_vo_api.h](references/ax615/sdk-inline/ax_vo_api.h) / [ax_global_type.h](references/ax615/sdk-inline/ax_global_type.h) — 公开 SDK 头文件**完整逐字内化副本**（已脱敏版权头，行号与原文对齐）——字段/枚举/错误码/预设名核对的权威来源
  - [references/ax615/vo-python-binding.md](references/ax615/vo-python-binding.md) — 客户可见 Python 运行时模块/API 包装调用约定摘要（mdk_vo/uax_vo_api/ax_vo_api、Call_AX_VO_* 形状；不含逐字产物代码）
  - [references/ax615/version-manifest.json](references/ax615/version-manifest.json) / [references/ax615/version-routing.md](references/ax615/version-routing.md) — 内化版本、V3 全系版本历史、版本来源优先级、匹配结果和证据降级规则
- **知识来源分级（已去敏，仅记录语义出处；原路径不再保留、不再提及）**：内化知识的来源分为公开头文件、官方 sample、知识库文档、版本化行为摘要四级，详见 [references/ax615/vo-knowledge-provenance.md](references/ax615/vo-knowledge-provenance.md)。**全流程不依赖任何外部本地源码目录，一切结论证据取自内化副本与知识库**
- **知识库检索配置**：`scripts/kb_query.py` 不内置服务地址。运行前设置 `XIAOZHI_MCP_URL`（完整 HTTPS MCP endpoint，例如 `https://<mcp-host>/mcp/`）和 `XIAOZHI_MCP_AUTH_TOKEN`，并用 `--kb` 或 `XIAOZHI_KB_IDS` 指定知识库 ID，Token 不回显；脚本也兼容从 `~/.agents/xiaozhi.env` 读取 Token；缺少配置时脚本退出码为 2。
- **访问边界：不主动访问 skill 目录以外的路径，也不访问任何外部源码树**（历史依赖路径已按用户要求全部去除，不再保留、不再提及）；**用户显式提供的文件（客户日志、proc 采集、代码片段、屏规格书、版本文件等）允许读取**，作为客户环境证据；**不主动读取凭据/密钥文件**。本 skill 的一切资料与结论均不得依赖外部源码目录。**新增任何知识引用路径必须经用户显式要求**
- 诊断排查剧本：[references/ax615/troubleshooting-playbook.md](references/ax615/troubleshooting-playbook.md)
- 时序校验脚本：[scripts/check_vo_timing.py](scripts/check_vo_timing.py) —— 计算**配置公式刷新率**、按离散表校验 PCLK、与两张内化时序表比对（bDlbClk 参与比较；u8DelaySel 缺失或表未记录记 unknown；`--intf dpi` 必须显式 `--fmt`）
- 时序求解脚本：[scripts/gen_vo_timing.py](scripts/gen_vo_timing.py) —— 正向求解器（查表/推导/校验三模式，读 skill 内离散档位表；dpi/srgb 必须显式 `--fmt`；退出码 1 为搜索无解，**不构成能力证明**）
- SDK 版本探测脚本：[scripts/detect_sdk_version.py](scripts/detect_sdk_version.py) —— 解析客户提供的 `display_status`、系统版本、dmesg 和口述文本，输出匹配、V3 版本历史差异点与降级策略

## 任务分流

| 客户意图 | 进入流程 | 结论形态 |
|---|---|---|
| 报告问题/排查请求（黑屏、花屏、报错等） | 诊断流程（第 1~6 步） | 四种终态（见诊断流程） |
| 已知场景要配置（接口/分辨率/屏规格/源色域） | 生成流程（第 1~5 步） | 配置参数表 + 代码骨架 + 送帧建议 + 验证步骤 |

两条流程共享：SDK 版本路由（诊断第 2 步 = 生成第 2 步）、内化知识、时序脚本、可靠性红线。

---

## 诊断流程

### 第 1 步：整理已知信息，判断缺口

对照下表判断缺口。**缺关键信息时停下来向用户追问**（宁可多问一轮，不可凭猜测下结论）：

| 类别 | 关键信息 | 说明 |
|---|---|---|
| 现象 | 黑屏 / 无输出 / 花屏 / 撕裂 / 闪烁 / 颜色异常 / 帧率不对 / 偶发 | 现象决定排查方向 |
| 图像 | 现象照片/截图（显示器"无信号"字样、背光、OSD、颜色偏移方向、撕裂位置形态） | 用于现象定性；不是根因级证据 |
| 客户代码 | 调用 SDK 接口的代码片段（AX_VO_* 调用序列、参数字面值、返回值处理、buffer 管理） | 用法/配置错误的直接证据来源 |
| 输出接口 | BT656 / BT1120 / BT601 / LCD(DPI) / MIPI / CVBS / SRGB + 芯片型号（AX615D/Q） | 决定时序与 DataPinMap；AX615D 不支持 BT1120 与**并行** DPI（串行 sRGB 可用，上限 640x480@30） |
| 时序 | 分辨率、帧率、bIop、u32Pclk、bDlbClk、全部 porch/pw 参数 | 花屏/无输出的首要怀疑对象 |
| 日志 | AX_VO_* 各 API 返回值（hex）、驱动报错（dmesg） | 每个非 0 返回值都是线索 |
| proc | `/proc/ax_proc/vo/display_status` 输出 | 含 SDK 版本、显示状态权威信息 |
| 版本 | SDK 版本（见第 2 步版本路由） | 结论适用范围与已知问题匹配 |
| 复现 | 必现/偶发、概率、与分辨率/接口/温度相关性 | 偶发问题需重点收集 |

**必问清单**（客户未提供时逐项询问，可用一个消息一次问清）：
1. 输出接口类型、芯片型号（AX615D/Q）、分辨率/帧率（时序参数全部要）
2. 各 AX_VO_* 调用返回值、dmesg 报错
3. `/proc/ax_proc/vo/display_status` 的输出
4. SDK 版本（优先提供完整 display_status，由脚本扫描 `[SDK version]:` 行；该行不保证位于物理首行）
5. 复现概率与触发条件

### 第 2 步：SDK 版本探测与路由（与生成流程共享）

1. 优先从客户提供的 `/proc/ax_proc/vo/display_status` 探测运行中 VO 驱动版本。版本行不是固定物理首行，须扫描 `[SDK version]:`；可执行：
   `python3 <skill-dir>/scripts/detect_sdk_version.py --display-status <采集文件> --json`。
2. `display_status` 不可得时，再使用 `/proc/ax_proc/version`、`AX_SYS_GetSdkVersion()` 结果、VO 用户态库日志、dmesg 旁证或客户告知。来源优先级、可用性和冲突处理严格按 [references/ax615/version-routing.md](references/ax615/version-routing.md)。
3. 按脚本的 `match` 路由（`match` 只有 `same`/`different`/`unknown` 三种取值；`conflict` 是**独立的布尔标记**，表示多来源版本不一致，不属于 `match`，两者可同时出现，如 `same` + `conflict=true`）：
   - `same`：可使用内化 D/E 级资料，但仍保留固定版本标注；
   - `different`：先查 [references/ax615/version-manifest.json](references/ax615/version-manifest.json) 的 version_history——探测版本在 V3 历史中时**可分析**：D/E 级行为判据按该版本差异点引用（三个实质差异点：V3.1.0 Clip 仅 BT 生效、V3.5.0 VSYNC 事件线程重构、V3.11.0 数字 Coax 修复；脚本输出 `history_vo_changes` / `history_version` 字段），无差异区间注明"已收录记录未发现相关差异，目标环境仍需核验"（**无提交/无差异记录不等于行为保证**）；**版本不在历史中时一律降级**——V2.x 及更早，以及未收录的 V3.y.z（脚本给 `history_unverified=true`，即未核实的 V3 区间同样不给"无差异"背书），D/E 级资料全部降为待验证假设，不得据此下“已确认”结论，用客户版本头文件、知识库、Gerrit 或实机复核；
   - `unknown`：明确写出“SDK 版本未知，当前内化资料基于 V3.14.0”，然后**先询问用户是否同意按 V3.14.0 作为临时基线继续分析**。未得到明确同意前停止版本相关诊断/配置，不引用 D/E 级资料形成结论；用户同意后才继续，并将所有 D/E 级结论标为“基于 V3.14.0 的推测，须按客户实际版本核验”。同时继续请求完整 `display_status` 等版本证据；
   - `conflict=true`：以 `display_status` 的 VO 驱动版本路由，同时列出冲突来源，提示可能存在系统/驱动/用户态库混装。
4. **构建变体**（`V3.10.0_2771`、`V3.14.0_20260915123456` 等）：后缀保留在 `raw_version`/`build_variant`，主版本归一化为 `Vx.y.z` 参与路由与历史匹配；结论中把 `raw_version` 原样写回客户，避免对号入座出错。多段点分数字（IP、`3.14.0.1`）不会被误识别为版本。
5. 知识库 query 和 Gerrit 检索词必须带探测版本（如 `"VO SendFrame2Disp 超时 SDK 3.12.0"`），确认结论适用于该版本。
6. **新增知识授权闸门**：如果匹配目标版本需要查询并内化当前 skill 未包含的新版本行为、时序、错误码或修复知识，先向用户说明拟查询来源、拟内化内容和安全边界，并询问是否执行；只有得到明确允许后才能检索和写入 references。未授权时继续按现有资料降级分析，不得自动引入。
7. **Gerrit 工具不可用或权限不足时的降级规则**：如果工具未注册、调用被拒绝、认证失败、网络不可达、目标项目/分支不可见，或无法确认返回结果是否完整，必须先向用户提示："当前无法完成 Gerrit 查询，原因是<工具不可用/认证失败/权限不足/网络不可达/结果不可确认>；以下分析不包含 Gerrit 已知问题与修复版本核验"。随后继续使用本 skill 的内化资料、知识库、客户提供的代码、日志、proc 和时序脚本完成当前分析；不得因 Gerrit 不可用而中止，也不得把"未执行查询"表述为"未发现已知问题"。

### 第 3 步：查内联约束 → 检索知识库

1. 先查 [references/ax615/vo-constraints.md](references/ax615/vo-constraints.md)：现象对应的约束条目直接给出现成判据（如"BT656 SDR 下 u32Pclk 须为像素时钟×2"），多数配置错误在这一步就能定性
2. 需要更完整语义（结构体字段、注意事项原文）时再检索知识库：

```bash
python3 <skill-dir>/scripts/kb_query.py \
  --query "VO 黑屏 无输出 Enable 返回错误" --top-k 8
```

query 要具体（现象 + 模块 + 疑似 API/版本）。检索范围为 `--kb` 或 `XIAOZHI_KB_IDS` 指定的知识库。检索不到时换措辞重试 1-2 次；仍无结果明示"知识库未命中"，不得编造文档内容。

**检索失败降级（按脚本退出码区分"未命中"与"未执行"）**：`kb_query.py` 退出码 `0` 命中、`1` 检索已执行但无结果（未命中）、`2` 参数或 Token 等本地错误、`3` 网络/协议层失败（未执行成功）；token 缺失、超时、连接失败、跨源重定向被拒都归入未执行。据此：

- **未命中**（退出码 1）：换措辞重试，累计不超过 4 次；仍无结果按终态 2/3 处理，并在结论中写"知识库未命中"。
- **未执行**（退出码 2/3）：先向用户提示"当前无法完成知识库检索，原因是<无 Token/超时/网络不可达/服务错误>"，**不得表述为"知识库中不存在该问题"**；随后用内化副本继续分析，并在结论中注明"本次结论未包含知识库检索证据"。服务端对空结果与失败可能都返回 HTTP 200，务必以退出码和 `--json` 的 `hits` 字段判断，不要只看 HTTP 状态。

**检索预算（防止无限换词重试）**：每个问题的 `kb_query.py` 检索累计不超过 **4 次**、gerrit 检索不超过 **2 次**。预算用尽仍未获有效证据时，按「结论终态」转终态 2（信息不足）/ 终态 3（原因未知），并在结论中列出全部已用检索词与命中情况。内化副本（vo-constraints / vo-api-inline / vo-timing-table / vo-sdk-behavior-notes）已能回答的问题不得再检索知识库。

### 第 4 步：时序校验（脚本优先）与代码对照

- 客户时序参数 → 跑 [scripts/check_vo_timing.py](scripts/check_vo_timing.py)：自动算出**配置公式刷新率**、PCLK 是否**精确命中**离散档位表、与 54 组表及官方 sample 19 组表的字段差异（bDlbClk 参与比较；u8DelaySel 缺失或表未记录记 unknown，不得默认等价）。**确定性计算交给脚本，不心算**
- API 语义：以 [references/ax615/vo-api-inline.md](references/ax615/vo-api-inline.md) 与 [references/ax615/sdk-inline/ax_vo_api.h](references/ax615/sdk-inline/ax_vo_api.h)（完整头文件内化副本）和知识库文档为准；实现级行为以 [references/ax615/vo-sdk-behavior-notes.md](references/ax615/vo-sdk-behavior-notes.md)（版本化行为摘要）为准，不得访问工作区外源码目录
- 客户 Python/RPC 调用问题：以 [references/ax615/vo-python-binding.md](references/ax615/vo-python-binding.md) 内化调用约定核对
- 标准调用序列：见约束表第 1 节（源自官方 sample）；退出顺序 `UnReg → Disable → Deinit`
- 刷新率为**配置公式值**；存在版本实现差异时按 vo-sdk-behavior-notes.md 的核验提示处理，以 proc `Refresh`/`OutFps` 与 VSYNC 实测为准

### 第 5 步：形成假设并分级验证

对每个候选根因标注证据等级，禁止凭记忆下结论。证据链分三段，不得混为一谈：

1. **事实确认**：知识库文档原文、公开头文件定义、proc 输出、日志或已内化的版本化证据直接佐证某个**行为事实**（默认值、错误码含义、某组合不支持等）。
2. **根因确认**：把已确认的事实与本次现场证据（客户代码、返回值、proc/dmesg、复现规律）连成完整因果链，才能判**已确认（根因）**；缺现场证据时只能判**推测**。**文档/知识库/内化副本只能支持事实确认与假设，不能单独证明本次问题的因果。**
3. **修复验证**：修复/规避建议须经客户按验证步骤实机复现（改前改后对比）后，才可称"已验证"。

每条结论注明来源（文档名 / 文件路径:行号 / 客户日志原文 / 脚本输出）。

### 第 6 步：输出解决方案

按「结论终态」选择输出模板，**禁止输出第五种形态**：

```
## 现象摘要
（一句话 + 客户提供的关键信息，含 SDK 版本/未知）

## 排查结论
1. 【已确认（根因）/ 事实确认 / 推测】结论 — 证据：<来源>
   - 验证步骤（推测时必须给）：<客户可执行的具体操作>

## 建议处理方案
（修复/规避/配置建议，逐条对应上述结论；涉及 API 参数给出具体取值和依据）

## 待补充信息
（如需客户进一步提供，逐条列出）
```

**结论终态（只允许四种，禁止第五种"似是而非的猜测结论"）**：

1. **给出原因与修复建议**：结论按第 5 步分级（已确认（根因）/事实确认/推测；文档与内化副本只能支持事实确认，不能单独证明本次因果），每条注明证据来源；推测必须附客户可执行的验证步骤；修复建议须经客户实机复现验证后才可表述为"已验证"
2. **信息不足 → 继续提问**：按第 1 步缺口表与必问清单，**一次消息把缺失项问清**，不得带着缺口下结论
3. **原因未知**：走完排查路径仍无法定性时，直接明确告知"原因未知"。必须同时给出：已排除的假设及排除依据、已查证的证据位置（文档/代码/proc）、还缺哪类证据才能继续
4. **应用场景无法实现**：若排查指向芯片/接口能力边界（如 AX615D 不支持 BT1120 与并行 DPI（串行 sRGB 上限 640x480@30）、Layer 级 CSC 不支持、PCLK 档位不可达），**直接下结论"该场景在 AX615 上无法实现"**，引用 vo-constraints.md 对应约束条目作为原因证据，并尽量给出可行的替代方案（换接口/换芯片型号/换实现方式）。**能力结论只引用能力矩阵/约束条目，脚本求解无解不是能力证明**

- **输出紧凑性**：结论与证据为先，证据引用压缩到可核验的最小形式（来源文件:行号 + 关键原文一句）；同类检索证据合并引用，不得大段粘贴检索原文；总长度与问题复杂度相称。
- **终态 3（原因未知）**输出模板：现象摘要 → 「## 排查结论：原因未知」→ 已排除假设及依据 → 已查证范围（文档/代码/proc/知识库检索词）→ 还需要哪类证据（逐条列出，请客户补充）
- **终态 4（场景无法实现）**输出模板：现象摘要 → 「## 结论：该场景在 AX615 上无法实现」→ 原因与证据（引用 vo-constraints.md 约束条目原文来源）→ 可行的替代方案（如有）→ 待补充信息

---

## 生成流程

### 第 1 步：场景解析

从用户描述提取生成所需的全部要素，缺项一次性问清：

| 要素 | 说明 |
|---|---|
| 芯片型号 | AX615D / AX615Q（决定能力边界；未给出时按第 2 步追问） |
| 输出接口 | BT656 / BT601 / BT1120 / DPI（含串行 sRGB） / CVBS（无通路，见能力矩阵） / Coax（专项，须产品线确认） |
| 分辨率/帧率 | 目标 WxH@fps；竖屏场景注明（如 720x1280） |
| 屏规格书 | porch/pw/pclk 参数（有则走校验模式，无则走查表/推导） |
| 源视频 | 色域（BT601/BT709/RGB）、格式（YUV/RGB）→ 决定 CSC 矩阵 |
| 送帧方式 | 帧源（VI/IVPS/解码器）、帧率、是否 VSYNC 节拍 |

### 第 2 步：SDK 版本探测与能力校验

版本探测与路由同「诊断流程第 2 步」。`different` 时：探测版本在 V3 历史中 → **可生成候选配置**——按该版本差异点标注（脚本输出 `history_vo_changes`），无差异区间注明"已收录记录未发现相关差异，目标环境仍需核验"（**无提交/无差异记录不等于行为保证**），生成物仍须在目标 SDK 实机核验；**版本不在历史中（V2.x 及更早，或未收录的 V3.y.z，`history_unverified=true`）→ 一律降级**：D/E 级时序、PCLK 和实现行为只能生成候选，必须标记"基于 V3.14.0 内化资料，须在目标 SDK 重新核验"，不得声称是目标版本的已验证配置；`unknown` 时先询问用户是否同意按 V3.14.0 作为临时基线继续，未获同意前停止生成版本相关配置。

能力闸门：对照 [vo-config-reference.md](references/ax615/vo-config-reference.md) 第 4 节能力矩阵逐项核对，**任何一项不满足即不生成无效配置**，直接输出：

- **场景无法实现**（如 AX615D + BT1120/并行 DPI、AX615D 串行 sRGB 超 640x480@30、DSI/LVDS 输出、BT656 配 RGB 格式）→ 说明原因 + 证据 + 替代方案（换芯片型号/换接口/桥接方案）；能力判定只引用能力矩阵/约束条目，**脚本求解无解不构成能力证明**
- **无通路场景**（CVBS/模拟输出、DSI/LVDS/CSI）→ 明示"该场景在 AX615 上无法实现"并给替代方案；
  **Coax（HDCVI 风格）通路已实现但属专项方案**，默认不生成，客户确有需求时先与产品线确认板级支持（保守结论，见 vo-config-reference.md 第 4 节）

### 第 3 步：时序求解（脚本优先，三级策略）

按优先级依次尝试，输出中必须标注来源等级：

1. **SDK 预设模式**（标准分辨率）：`enIntfSync = AX_VO_OUTPUT_*` 预设值。**预设名与 API 语义由公开头文件确认，但不代表"天然可用"或"由 SDK 保证"**——最终时钟仍须经过当前 SDK 的离散 PCLK 档位表与接口/芯片能力校验（第 2 步能力闸门对预设同样适用，如 AX615D 串行 sRGB 的 640x480@30 上限），故预设同样需要实机核验；该可用性判定属「**已授权源码核验的 SDK 行为约束**」（**当前内化版本行为，需按版本核验**）。预设名**以 [references/ax615/sdk-inline/ax_vo_api.h](references/ax615/sdk-inline/ax_vo_api.h) 第 98-145 行逐字为准**（完整 39 个成员已内化）；头文件未列的预设名不得写入代码
2. **查表命中**：`python3 <skill-dir>/scripts/gen_vo_timing.py --intf <接口> --res <WxH> --fps <f> [--fmt <格式>]` → mode=table（已验证时序表条目，最高可信；可交叉核对官方 sample 19 组表）。**接口为 dpi/srgb 时必须显式 `--fmt`**（并行 `rgb565`；串行 `srgb565`/`srgb666`/`srgb565s`/`srgb888`/`srgb888a`/`srgb888b`），缺格式脚本按缺失拒绝；查询无解（退出码 1）只说明当前搜索空间内无解，**不构成能力证明**
3. **近邻推导**（表外自定义分辨率）：同脚本 mode=derived → 候选组合（近邻模板 porch 缩放 + PCLK 离散表枚举），**标注"推导值，须实机验证"**，porch 须按客户屏规格书核对
4. **屏规格书校验**（客户给了完整 porch）：`gen_vo_timing.py --verify --intf <接口> [--fmt <格式>] --json '<完整时序>'`（**dpi/srgb 必须显式 `--fmt`**，如 `--fmt srgb565`）→ 配置公式刷新率/离散表命中/格式与尺寸约束提示（输出带版本标注）

### 第 4 步：生成配置

输出四部分（模板见下），参数逐字段标注来源等级：

1. **配置参数表**：AX_VO_PUB_ATTR_T / AX_VO_CSC_T / DataPinMap 各字段取值 + 来源（表条目/预设/推导/屏规格书）
2. **C 代码骨架**：标准序列 Init→SetPubAttr→SetDataPinMap→SetCSC→Enable→SendFrame2Disp，每步返回值检查（对照错误码表）；含 buffer 获取（AX_POOL_GetBlock + 物理地址）与 VSYNC 节拍送帧
3. **Python（MicroPython RPC）等价写法**：按 [references/ax615/vo-python-binding.md](references/ax615/vo-python-binding.md) 调用约定摘要生成（`from uax_vo_api import ...` / `from ax_vo_api import ...`，`Call_AX_VO_*` 包装，模块名 mdk_vo；Getter 返回元组）；客户 SDK 版本与内化版本不同时标注"以客户实际封装为准"
4. **验证步骤**：`cat /proc/ax_proc/vo/display_status` 预期值（Refresh/ScanType/Pclk/InFifoSize/DiscFrames）、VSYNC 计数实测帧率、按「sample 回归流程」更换表中已知时序做回归（见 vo-config-reference.md 第 9 节）

### 第 5 步：生成自检（输出前逐项核对）

- [ ] 调用顺序符合标准序列（含退出顺序 UnReg → Disable → Deinit）；SetCSC 在 SetPubAttr 成功之后（Enable 前后均可）
- [ ] u32Pclk 精确命中 [vo-pclk-table.json](references/ax615/vo-pclk-table.json)（无容差）；BT656/601 SDR 已 ×2；**u8DelaySel 按所选表条目取值（不得简化为 DDR=3/非 DDR=0）；表条目未记录或客户未提供时记 unknown，不得默认取值**
- [ ] 接口×格式合法（BT 系 YUV422；**DPI 为并行 RGB565 或串行 SRGB 系列，串行注意时钟倍率**）；AX615D 能力未越界（BT1120 与并行 DPI 不支持；串行 sRGB ≤640x480@30）
- [ ] bIop 与屏扫描方式一致（逐行屏 bIop=1）
- [ ] enIntfSync 预设名逐字核对过（**预设不豁免能力/PCLK 校验**，可用性须按当前 SDK 核验）；USER 模式已跑脚本校验
- [ ] 源色域→CSC 矩阵选择有依据（RGB 源 + YUV422 输出不能配 IDENTITY）
- [ ] 帧约束自检：宽高范围/对齐、stride 16 或 128 对齐、crop/LBA 等式、隔行不用压缩帧
- [ ] 送帧节拍建议（VSYNC 回调/阻塞 s32MS=-1），InFifoDepth ∈ [1,8]，Pool buffer 获取/释放成对
- [ ] 已运行版本探测；记录 `same/different/unknown` 和冲突来源；`different/unknown` 时 D/E 级配置已降为候选并要求目标 SDK 复核
- [ ] 每条参数标注来源等级；推导值已标注"须实机验证"；引用表数据时带固定版本标注

**生成终态与证据链确认标准（只允许两种终态，禁止"未标注就直接给配置"的中间态）**：

1. **不可生成**：能力闸门或版本授权闸门未通过 → 输出"该场景在 AX615 上无法实现"或"未获授权/版本未知，暂停生成"，附原因、证据与替代方案，不输出配置代码。
2. **生成**：输出配置 + 逐字段来源；每条结论/参数都要能回答"证据是什么"，来源只能是：客户可见输入、本 skill 内化副本（含固定版本标注）、知识库/公开头文件检索原文；`evidence_signatures` 式的笼统引用不算证据。版本链确认：`same` 或 `different`+`history_version` 命中 → 可直接引用并带版本差异说明；`different`+`history_unverified`/`unknown`/检索未执行 → 结论一律标"候选/待验证"，不得表述为"已验证"。

## 输出模板

```
## 场景摘要
（芯片型号/接口/分辨率帧率/源色域/屏规格一句话）

## 能力校验
（通过 / 无法实现+证据+替代方案 / 知识缺口声明）

## 时序参数（来源：<表条目名 | 预设模式名 | 推导值 | 屏规格书>）
（bIop/u16Vact/.../u32Pclk/bDlbClk/u8DelaySel 全字段取值（u8DelaySel 为 unknown 时明确写 unknown）+ 配置公式刷新率 + 离散表命中 + 版本标注）

## 配置代码（C）
（标准序列代码骨架，返回值检查，关键参数注释标注来源）

## Python 等价写法
（标注：签名以客户 SDK 实际封装为准）

## 送帧与 buffer 建议
（buffer 来源/物理地址/VSYNC 节拍/s32MS 取值/InFifoDepth）

## 验证步骤
（proc 预期值 + 实测帧率 + 回归手段）
```

---

## 可靠性红线（诊断与生成共用）

1. **API 参数语义、结构体字段、错误码含义**：只引用 vo-constraints.md / vo-config-reference.md / 知识库文档原文 / `ax_vo_api.h` 定义，找不到就说不确定并检索/询问，不得凭训练记忆编造
2. **时序参数**：以 `check_vo_timing.py` / `gen_vo_timing.py` 的比对结果与 skill 内化时序表为准；客户参数与表中不符时指出差异而非直接断言错误；**bDlbClk 必须参与比较，u8DelaySel 缺失或表条目未记录记 unknown，不得默认**；两表冲突时不静默合并
3. **证据冲突**（文档与实现不一致、proc 与预期不符）时如实呈现冲突，说明哪边更可信及理由；**公开 API 返回码只按公开头文件/错误码文档解释；实现行为差异引用 vo-sdk-behavior-notes.md 并带其固定版本标注「SDK V3.14.0 实现行为，需按版本核验」**
4. **证据等级必标**：诊断结论分级（已确认（根因）/事实确认/推测，推测必附验证步骤；**文档/内化副本只能支持事实确认，不能单独证明本次因果**）；生成参数标注来源（已验证表条目名 / sample 表条目 / 预设模式名 / 推导值 / 屏规格书），推导值必须附"须实机验证"；引用 D/E 级来源时**必须同时引用固定版本标注**
5. **区分"芯片限制"与"用法错误"**：先对照官方 sample、约束表和 API 文档排除用法错误，再下芯片限制结论
6. **图像、客户代码与文档都不单独充当本次根因证据**：图像只用于现象定性，客户代码可证明用法错误，文档/内化副本可确认行为事实；"根因成立/修复可行/场景可实现"的最终结论必须形成完整因果链并回到 proc/日志/文档/已内化证据/时序表，修复建议须实机复现验证后才可表述为"已验证"
7. **不得硬凑结论**：走完排查路径仍无法定性时明确回答"原因未知"并说明已排除项与证据缺口，禁止输出似是而非的猜测结论
8. **"场景无法实现"结论必须有芯片能力证据**：引用约束/能力矩阵条目及其来源；若只差芯片型号确认，说明确认后可给出最终定论
9. **能力边界不妥协（生成）**：AX615D+BT1120/并行 DPI、AX615D 串行 sRGB 超 640x480@30、DSI/LVDS/CSI 输出、格式×接口不匹配、PCLK 不在离散表等场景**不生成配置**，直接给替代方案；预设名不虚构，核对不到降级为 USER+表条目或 USER+推导；**预设模式不豁免能力闸门**（公开头文件只确认预设名/API 语义，最终时钟仍须经过当前 SDK 的离散 PCLK 与接口/芯片能力校验，可用性须实机核验）；**脚本搜索无解不作为能力不支持的证据**
10. **Python 调用约定不编造**：按 vo-python-binding.md 摘要生成；摘要未涵盖的 API（EnumMode/Layer/Chn/WBC/Batch/CscMatrix 未导出）不得编造，客户 SDK 版本不同时标注核对要求
11. **结构体字段按内化原文**：字段名/枚举值以 vo-api-inline.md / vo-config-reference.md 检索原文为准（如 u32Satuature 拼写、enClkEdge 字段），不得按训练记忆编造
12. **缺要素不硬生成**：芯片型号（影响能力边界）、接口、分辨率/帧率缺一时先追问，不生成
13. **版本路由与新增知识授权**：先按 version-routing.md 判定版本；目标版本不同或未知时不得把 V3.14.0 的 D/E 级资料冒充目标版本已验证结论；结论注明 SDK 版本适用范围，版本未知时声明局限。需要引入当前 skill 未包含的新版本知识时，必须先征得用户明确许可，未获许可不得检索或内化
14. **访问边界**：不主动访问 skill 目录以外的路径，也不访问任何外部源码树；**用户显式提供的文件（客户日志/proc 采集/代码片段/规格书等）允许读取并作为客户环境证据，但不主动读取凭据/密钥文件**；**诊断/生成不依赖任何外部源码目录**（知识已内化，历史路径已去敏），引用证据来自知识库、gerrit、客户输入与本 skill 的 references（内化副本）。**新增任何知识引用路径必须经用户显式要求**。Gerrit 是可选外部依赖，不可用或权限不足时按第 2 步的降级规则提示用户并继续分析，不得声称已完成 Gerrit 查询或已排除已知问题
15. **来源隔离红线**：本 skill 内不得出现实现侧源码路径/文件名/内部符号名/源码行号，也不得据此展开推理；实现行为一律以 vo-sdk-behavior-notes.md 的行为约束形式引用并带固定版本标注。**该约束对 skill 自身文档同样适用**——新增内化内容时先自查，发现残留改为行为约束表述
16. **适用范围声明**：本 skill 仅适用于 AX615 芯片（AX615D/AX615Q）。问题明显非 ax615 芯片、或芯片型号模糊不清时，回答中必须**显式声明适用范围**（见「适用范围」节），不得默认按 AX615 分析、不得将本 skill 的约束/时序表/错误码套用到其他芯片

## 回归自检

`evals/` 存放 Golden Case，用于在修改分析/生成流程、`references/` 知识或脚本后确认没有退化。每个 Case 目录分两个区：

- `input/`：客户问题/场景材料（`scenario.md`），分析/生成阶段唯一可读的内容。
- `answer/`：`case.yaml`（含 `title`/`category`）、`oracle.yaml`，即答案与元数据，只在评分阶段读取。

当前有 11 个 Case：`AXVO-analysis-001` ～ `AXVO-analysis-007`（诊断类）与 `AXVO-setting-001` ～ `AXVO-setting-004`（配置生成类）。每个 Case 具体考什么写在它自己的 `answer/case.yaml` 里，本文件不复述，以免自检前泄露答案。

### 盲测纪律

答案与输入同在本 Skill 目录内，隔离靠执行顺序保证，不靠目录边界。因此：

**进入评分阶段之前，分析者不得直接以任何方式打开该 Case `answer/` 目录下的文件（`case.yaml`、`oracle.yaml`），也不得通过检索猜测答案。** 元数据可经预检脚本间接读取——`validate_case.py` 只核对 `title`/`category`/`separation` 等结构字段并在失败时报错，`validate_oracle.py` 只做结构校验，两者都不打印 `answer/` 内容。判断边界：**脚本可以因为结构错误而暴露"某个字段不合规"，但不能让答案内容进入分析上下文**；一旦答案内容（`root_cause`、`required_concepts`、`forbidden_conclusions`、`evidence_signatures` 的具体值等）出现在分析阶段，这次自检结论作废，必须换一个未读过答案的 Case 重跑。

### 执行

1. 预检 Case，参数是 Case ID 或目录：

   ```sh
   python3 <skill-dir>/scripts/validate_case.py AXVO-analysis-001
   ```

   失败时输出 `ERROR` 和缺陷，不进入分析。预检核对 `title`/`category`（含与 Case ID 流程的一致性）、`input/scenario.md` 真实存在且非空、`separation` 分区与 `analyzer_visible` 文件可用性；只打印 `input/` 文件清单，不打印 `answer/` 下任何路径。

2. 只读取预检给出的 `analyzer_visible` 文件（`scenario.md`），按 Case 类别进入对应流程：`AXVO-analysis-*` → 诊断流程，`AXVO-setting-*` → 生成流程。此阶段把自己当作没有答案的分析者，不打开 `answer/` 目录。

3. 将输出**冻结**为 `analyzer_result`。冻结后不得依据答案补写、删改或重跑。**批量跑多个 Case 时必须先完成全部 Case 的分析并逐个冻结（此阶段不得读取任何 `answer/` 内容），全部冻结完成后才进入第 4 步评分。**

4. 此时才读取该 Case 的 `answer/oracle.yaml`。先校验，再按 [references/grading.md](references/grading.md) 做语义对比：

   ```sh
   python3 <skill-dir>/scripts/validate_oracle.py <case-dir>/answer/oracle.yaml <case-dir>
   ```

   校验核对：`root_cause`/`required_concepts`/`forbidden_conclusions`/`evaluation_notes`/`expected_confidence` 的类型与取值，以及 `evidence_signatures` 的每个 key 都能在 Case 目录内找到对应的非空 `input/` 文件（不存在、为空、越出 Case 目录或绝对路径都报 `ERROR`；第二参数缺省时按 oracle 的上两级目录推断 Case 根目录）。重复 key 在解析阶段即被拒绝。

5. 输出结论（格式见 grading.md）：`Case`/`Verdict: PASS|FAIL|ERROR`、冻结的 `Analyzer result`、`Comparison` 五项（Root cause（生成类为 Expected config）、Required concepts、Forbidden conclusions、Evidence grounding、Confidence）、`Summary`。

`Analyzer result` 必须原样保留。批量跑多个 Case 时，**先冻结全部 Case 的 `analyzer_result` 再统一进入评分**，评分阶段逐 Case 输出并汇总 `total/pass/fail/error`；不得边分析边评分，也不得读取任一 Case 的 oracle 后回头修改其他 Case 的冻结结果。一个 Case 的 oracle 不得用于评判另一个 Case。`FAIL` 表示输出不符合 oracle，`ERROR` 表示 Case、输入或流程无法完成，两者不可互换。

### 维护

新增 Case 时把客户问题/场景全文写入 `input/scenario.md`（含芯片型号、接口、时序参数、返回码、proc、版本等全部已知信息），在 `answer/case.yaml` 记录 `title`/`category`（`title` 非空；`category` 一级域必须是 `diagnosis/` 或 `generation/`，与 Case ID 的 `analysis-`/`setting-` 流程对应）与平台信息，在 `answer/oracle.yaml` 记录期望结论、必备概念与禁止结论/配置。`case.yaml` 的 `separation.analyzer_visible` 只能列 `input/` 下的文件且必须包含 `input/scenario.md`，`separation.evaluator_only` 只能列 `answer/` 下的文件且必须包含 `answer/case.yaml`，`oracle` 指向 `answer/oracle.yaml`；预检脚本会强制这些约束，并拒绝重复 key、越出 Case 目录的路径。除用户明确要求，自检过程不修改 `input/`、`answer/` 或本 Skill 知识。

## 快速参考

以下 `<skill-dir>` 指本 skill 的安装目录（复制命令时替换为实际路径；脚本内部按自身位置定位 `references/`，可从任意工作目录执行）。

- 诊断约束速查：`cat <skill-dir>/references/ax615/vo-constraints.md`
- 配置生成速查：`cat <skill-dir>/references/ax615/vo-config-reference.md`
- API 定义内化副本：`cat <skill-dir>/references/ax615/vo-api-inline.md`
- 完整头文件内化副本：`<skill-dir>/references/ax615/sdk-inline/ax_vo_api.h`、`<skill-dir>/references/ax615/sdk-inline/ax_global_type.h`
- Python 调用约定摘要：`cat <skill-dir>/references/ax615/vo-python-binding.md`
- 时序表内化副本：`cat <skill-dir>/references/ax615/vo-timing-table.json`、`cat <skill-dir>/references/ax615/sample-vo-timings.json`
- PCLK 离散档位表：`cat <skill-dir>/references/ax615/vo-pclk-table.json`
- 版本清单与路由：`cat <skill-dir>/references/ax615/version-manifest.json`、`cat <skill-dir>/references/ax615/version-routing.md`
- SDK 版本探测：`python3 <skill-dir>/scripts/detect_sdk_version.py --display-status <采集文件> --json`（退出码 0 命中 / 1 读取错误 / 2 无版本痕迹 / 3 未解析出版本）
- 版本化行为摘要：`cat <skill-dir>/references/ax615/vo-sdk-behavior-notes.md`
- 知识来源分级与边界：`cat <skill-dir>/references/ax615/vo-knowledge-provenance.md`
- 排查剧本：`cat <skill-dir>/references/ax615/troubleshooting-playbook.md`
- 时序校验：`python3 <skill-dir>/scripts/check_vo_timing.py --json '<客户时序参数>' --intf bt656|bt1120|dpi [--fmt <格式>]`（**`--intf dpi` 时必须显式 `--fmt`**，如 `--fmt srgb565`；缺格式脚本按缺失拒绝，不假定并行倍率）
- 时序求解：`python3 <skill-dir>/scripts/gen_vo_timing.py --intf bt656 --res 1920x1080 --fps 30`；**dpi/srgb 必须显式 `--fmt`**；退出码 1 = 当前搜索空间无解（**不构成能力证明**）
- 参数校验：`python3 <skill-dir>/scripts/gen_vo_timing.py --verify --intf dpi --fmt srgb565 --json '<完整时序>'`（dpi 必带 `--fmt`）
- 知识库检索：`XIAOZHI_MCP_URL="https://<mcp-host>/mcp/" XIAOZHI_MCP_AUTH_TOKEN="<token>" XIAOZHI_KB_IDS="<kb-id,...>" python3 <skill-dir>/scripts/kb_query.py --query "<现象+模块+API>"`；列表：`... --list-kbs`；退出码 0 命中 / 1 未命中（检索已执行）/ 2 缺少 endpoint、Token 或其他本地配置错误 / 3 网络或协议失败（未执行）
- Golden Case 判定规则：`cat <skill-dir>/references/grading.md`
- Case 预检与 oracle 结构校验：`python3 <skill-dir>/scripts/validate_case.py <case-id>`、`python3 <skill-dir>/scripts/validate_oracle.py <case-dir>/answer/oracle.yaml <case-dir>`

**访问边界（脚本与检索同样适用）**：脚本只读取 skill 目录内的文件与用户显式传入的文件（`kb_query.py` 额外读取 `~/.agents/xiaozhi.env` 中的 Token——该凭据由脚本自行读取，分析者不主动打开凭据/密钥文件；endpoint 必须由运行环境通过 `XIAOZHI_MCP_URL` 提供，Token 不回显、不随跨源重定向转发，跨源跳转直接失败）。分析过程不主动访问 skill 目录以外的路径、不访问外部源码树；**用户显式提供的文件允许读取**，但分析者不得主动把客户材料的落盘位置选在 skill 目录之外。
