---
name: sdk-tx-analyse
description: 为 AX615/爱芯 SDK 的 AX_TX（外部模拟同轴发送芯片）提供两类能力——问题分析/客户答疑，以及示例代码生成/修改。覆盖 TX_VI（BT 接收）、TX_VO（CVI/AHD/TVI/CVBS 同轴发送）、TX_CLK（BtClk/PLL/MCLK）、RS485、正反向音频，以及 VO BT656/BT1120 输出与 TX 芯片对接的完整通路。当用户问 TX 同轴为什么无输出/花屏/抖动、DVR 锁不上、制式或分辨率不匹配、BtClk/BtWorkMode/SDR/DDR 该怎么选、某个 AX_TX API 或枚举含义、返回错误码代表什么、VO timing 与 TX 参数是否匹配、需要给客户解释 TX 行为与排查步骤时，进入分析答疑模式；当用户要求编写 vin_ivps_vo_tx 类示例、配置 TX 芯片输出制式、把 VO 的 BT 输出接到 TX、调整 VO timing 与 TX BtWorkMode/BtClk 映射、增删 TX_VIDEO_PROTOCAL/VO_INTF_FMT 组合时，进入代码生成模式。知识库是当前 header/external 头文件（ax_tx_api.h、ax_tx_common.h、ax_vo_api.h）、仓库 sample（msp/sample/vin_ivps_vo_tx）与本 skill 的 knowledge-base/《AX615 VO时序配置.md》，结论与代码必须引用真实 API/枚举/sample 行为与时序表，不凭记忆捏造 SDK API、枚举值或板级参数。
---

# AX615 TX 分析与代码生成

针对 AX_TX 外部模拟同轴发送芯片，本 skill 提供两种模式，按用户意图选择：

- **§A 分析答疑模式（只读）**：定位问题、根因分析、客户答疑。读头文件与 sample、还原通路、给排查步骤和依据，**不生成或修改代码**。
- **§B 代码生成模式**：生成或修改 `vin_ivps_vo_tx` 类 TX 示例代码，把同轴输出规格映射到 VO BT 输出 timing、TX_CLK、TX_VI、TX_VO 的完整生命周期与 VO×TX 映射表。

两种模式共享 **§0 通路心智模型** 与 **§1 知识库**，并都受 **§2 通用准确性约束** 约束。用户问“为什么/是什么/怎么排查”走 §A；要求“写/改/新增/生成”走 §B；若分析后确需改代码，可从 §A 平滑转入 §B。

## 0. TX 通路心智模型（两模式共享）

TX 是 SoC 外部的模拟同轴发送芯片，数据单向流动：

```text
(VIN -> IVPS -> VO)  VO 通过 BT656/BT1120 并口输出 YUV422
        |  并口 (BT clk + data pin)
        v
   TX_VI (芯片内 BT 接收)  ->  TX_VO (调制成 CVI/AHD/TVI/CVBS)  -> 同轴线 -> DVR/后端
```

关键理解与分层：

- **VO 侧**决定 BT 接口格式、timing、SDR/DDR（单沿/双沿）、data pin map，是 TX 的上游喂数；`/proc/ax_proc/vo/display_status` 无帧率＝VO 没送数。
- **TX_VI**（`AX_TX_VI_*`）：芯片内 BT 接收，配 `VI_BT_WORK_MODE_E`/采样沿/YUV 序/data line/BtClk；`AX_TX_VI_GetBtStatus` 的 `bEnable`/`u32Fps`/`u32ErrStatus` 反映收数情况。
- **TX_VO**（`AX_TX_VO_*`）：输入制式 `VIDEO_FMT_E` 调制成输出制式 `VIDEO_OUT_FMT_E`（CVI/AHD/TVI/CVBS）送同轴。
- **VO×TX 必须成套匹配**（最高频根因）：VO 的 SDR/DDR 与 TX 的 `VI_MODE_BT656_HD1`（单沿）/`VI_MODE_BT656_DUL_HD1`（双沿）一致；VO 的分辨率/帧率/pixel clock 与 TX 的 InFmt/OutFmt/BtClk 一致。sample 用一张 `VIDEO_PARAM_MAP_S` 表把这些绑成一行。

分析问题或生成代码前，先把关注点落到：VO 侧没送数 / TX_VI 没收到 / TX_VO 没发出 / VO×TX 不匹配。

## 1. 知识库：必须引用的真实资料（两模式共享）

结论与代码必须落到仓库内文件，禁止凭记忆断言：

1. `header/external/ax_tx_api.h`：TX 函数声明，三组——TX 生命周期（`AX_TX_Init/Deinit/Reset`）、TX_CLK（`AX_TX_CLK_SetClkEn/GetClkEn`、`SetBtClk/GetBtClk`、`SetClkSel`、`SetAudMclk`、`GetClkStatus`）、TX_VI（`AX_TX_VI_SwitchWorkMode/SetDevAttr/GetDevAttr/SetDataLine/EnableDev/DisableDev/GetBtStatus`）、TX_VO（`AX_TX_VO_SetVideoParam/GetVideoParam/SetVideoExtParam/GetVideoExtParam/SetVideoEn/SetAudioParam/SetAudioPubAttr/SetAudioExtParam/GetAudioExtParam/SetRs485Param/SendRs485Data/RecvRs485Data/SwitchRs485Position/SetSignalParam/SetBufferConfigParam/SetDigitalCoaxialPnSeq`）。
2. `header/external/ax_tx_common.h`：所有 TX 结构体、枚举、错误码的唯一来源——
   - 制式：`VIDEO_FMT_E`（`TX_VIDEO_FORMAT_*` 输入）、`VIDEO_OUT_FMT_E`（`HDCVI_*`/`A_*`/`T_*`/`H960_*` 输出，前缀区分协议）。枚举末尾 BTOUT 段的 `BT_*` 制式芯片实际不支持，不作为可用输出。
   - TX_VI：`VI_BT_WORK_MODE_E`、`VI_BT_SAMP_MODE_E`、`YUV_SEQ_E`、`VI_DEV_ATTR_S`、`VI_WORK_PARAM_S`、`VI_BT_STATUS_S`。
   - TX_CLK：`BT_IN_CLK_FREQ_E`（`CLK_BT_IN_36M`/`74P25M`/`148P5M`）、`BT_IN_CLK_PHASE_E`、`BT_IN_CLK_S`、`CLK_SRC_EN_S`、`CLK_SRC_SEL_S`、`AUD_MCLK_FREQ_E`。
   - TX_VO：`VO_VIDEO_PARAM_S`、`VO_VIDEO_EXT_PARAM_S`、`VO_COLORBAR_MODE_E`、`VO_RS485_PARAM_S`、`VO_AUDIO_PARAM_S`、`VO_AUDIO_PUB_ATTR_S`、`VO_AUDIO_EXT_PARAM_S`、`VO_SIGNAL_PARAM_S`、`VO_BUFFER_CONFIG_PARAM_S`。
   - 错误码：`AX_ERR_TX_VI_*`、`AX_ERR_TX_VO_*`、`AX_ERR_TX_CLK_*`（用 `AX_DEF_ERR(AX_ID_TX, 子模块, 错误类型)` 组合）。分析返回码时按这套解出子模块与错误类型。
3. `header/external/ax_vo_api.h`：VO 侧 `AX_VO_PUB_ATTR_T`、`AX_VO_SYNC_INFO_T`、`AX_VO_INTF_BT656/BT1120`、`AX_VO_OUT_FMT_YUV422`、`AX_VO_CLK_SDR_EDGE_*`、`AX_VO_OUTPUT_*`/`AX_VO_OUTPUT_USER`、`AX_VO_SetDataPinMap`、`AX_VO_SetClipParam`、`AX_VO_Init/SetPubAttr/Enable/Disable/Deinit`，用于核对/生成 VO 喂给 TX 的 BT 输出。
4. `msp/sample/vin_ivps_vo_tx/`：`sample_tx.c/h`、`sample_vo.c/h`、`sample_main.c/h`（音频再看 `sample_audio.c/h`、`wave_parser.c/h`）。sample 是“正确配置长什么样”的参照系，也是代码生成的基线：
   - `sample_tx.c` 的 `gastVideoParamMap[]`（`VIDEO_PARAM_MAP_S`）：`{VO_INTF, TX_PROTO} -> {BtClkFreq, BtWorkMode, InFmt, OutFmt}` 的权威对应表。
   - `sample_vo.c` 的 `gastPubAttr[]`：各 `VO_INTF_FMT_TYPE_E` 对应的 VO timing（SDR 标准 timing / DDR USER timing）。
   - `vo_audio_cfg[]`：各输出制式的反向音频 `u8TransMode`/`u8DataWidth`。
   - `sample_tx.h` 的 `TX_VIDEO_PROTOCAL_E` 是 sample 自定义类型，不在 external 头文件里。
5. **本 skill 的 `knowledge-base/AX615 VO时序配置.md`**：VO 对接 TX 的 BT656 USER timing 权威查表。按 SDR（单沿，默认 `bDlbClk=0`、`u8DelaySel=0`）/DDR（双沿，默认 `bDlbClk=1`、`u8DelaySel=3`）逐分辨率制式列出完整 `bIop/u16Vact/Vbb/Vfb/Hact/Hbb/Hfb/Hpw/Vpw/u32Pclk/bIdv/bIhs/bIvs/bDlbClk/u8DelaySel` 字段与 delay 区间，并给出计算规则 `Vact+Vbb+Vfb+Vpw=vts`、`Hact+Hbb+Hfb+Hpw=u32Pclk/fps/vts`。核对客户 timing 或填 `gastPubAttr[]` 的 USER timing 时以该表为准，再与映射表的 `enBtClkFreq`/`enBtWorkMode` 相互印证（SDR↔单沿、DDR↔双沿）；表中没有的制式按规则推导并在输出中标注。

无 `.codegraph` 索引时用 `rg`、`find`、定向读取；不要引用其它平台的同名头文件。

---

# §A 分析答疑模式（只读）

只做只读分析：读头文件与 sample、还原通路、定位问题、给排查步骤和依据。不生成、不修改代码；用户需要写或改代码时转入 §B。

## A.1 先收集问题上下文

回答前先确认或从上下文推断（缺失且影响结论时只问一个简短问题）：

- 现象：无输出 / 花屏错位 / 画面抖动闪烁 / DVR 锁不上 / 颜色异常 / 音频或 RS485 异常；一直不行还是偶发。
- 配置：目标制式（CVI/AHD/TVI/CVBS）、分辨率帧率、VO 接口（BT656/BT1120、SDR/DDR）、用的哪个 `VO_INTF_FMT_TYPE_E` 与 `TX_VIDEO_PROTOCAL_E` 组合。
- 证据：`/proc/ax_proc/vo/display_status`、`AX_TX_VI_GetBtStatus` 输出、相关 API 返回码、串口日志、板级类型（FPGA 还是量产板）。
- 数据源：实时 VIN、灌图还是 colorbar 测试图。

对答疑类问题（“某 API 是什么意思”“该怎么选参数”），直接查头文件/sample/时序表给依据即可，不必强行索要现场信息。

## A.2 VO×TX 匹配核对（最高频根因）

用 `gastVideoParamMap[]` 作基准，逐项核对客户配置：

- **SDR/DDR ↔ BtWorkMode**：VO SDR（`AX_VO_CLK_SDR_EDGE_DOWN` + 标准 `AX_VO_OUTPUT_*`）配 TX 单沿 `VI_MODE_BT656_HD1`；VO DDR（USER timing、`bDlbClk=1`）配 TX 双沿 `VI_MODE_BT656_DUL_HD1`；960H/CVBS 配 `VI_MODE_BT656_SD`。错配会导致 TX_VI 收数错位/花屏。
- **BtClk 频率**：1080P SDR 常 148P5M、DDR 常 74P25M；4M/更高常 148P5M；960H/CVBS 用 36M。BtClk 与 timing 的 pixel clock 不匹配会抖动或锁不上。
- **输出制式前缀 ↔ 协议**：`HDCVI_*`→CVI、`A_*`→AHD、`T_*`→TVI、`H960_*`/`H940_*`→CVBS。前缀与 `TX_VIDEO_PROTOCAL_E` 不一致，后端 DVR 按错协议解自然锁不上。（`BT_*` 段芯片不支持，客户误用应指出改回 CVI/AHD/TVI/CVBS。）
- **InFmt/OutFmt 分辨率帧率**：必须同分辨率同帧率对齐。
- **2880x1620 V20 版本**：TX 输出 `HDCVI_2880x1620_*_V20` 时，VO 侧必须用带 `_vts1728` 的 timing（vtotal=1728，`gastPubAttr[]` 注释 `(4297*1728)`）；误用普通 vts1650 timing（`(4500*1650)`）会不匹配。另外 2880x1620 非 V20 制式不支持反向音频，V20 制式才支持。
- **VO/TX 用同一 eVoIntf**：sample 中 `SAMPLE_VoInit` 与 `SAMPLE_TXInit` 传同一个 `eVoIntf`，各填各的必然不匹配。
- **VO 侧 BT656 timing 核对**：优先对照 `knowledge-base/AX615 VO时序配置.md`。客户 VO timing 与表中同制式行不符（尤其 `u32Pclk`、`bDlbClk`、`u8DelaySel`、blanking），常是 TX_VI 收数错位/抖动/DVR 锁不上的根因。

## A.3 常见问题→根因对照

- **完全无输出**：查 VO 是否使能出帧（`display_status`）、TX 时钟使能（`CLK_SRC_EN_S` 各位）、`AX_TX_VO_SetVideoEn(AX_TRUE)` 是否调用、pin mux/data line 是否配。
- **DVR 锁不上/断流后不恢复**：确认有没有按 sample 做 `SetVideoEn(FALSE)` → `sleep(1)` → 重配 → `SetVideoEn(TRUE)` 的断流重锁；输出制式与 DVR 期望是否一致。
- **数字音频制式画面异常/无数字音频**：CVI 段（sample 中 `enOutFmt < A_1280x720_25FPS`）需要 `VO_VIDEO_EXT_PARAM_S.u8PnSeqEn=1`，漏开会异常。
- **花屏/错位/颜色错**：`YUV_SEQ_E`（sample 用 `YUV_SEQ_VYUY`）与 VO YUV422 序不符；data line / `AX_VO_SetDataPinMap` 线序错（FPGA 与量产板不同，跨板复制会错）；采样沿（DUL 用 `VI_BT_SAMP_AUTO`，单沿用 `VI_BT_SAMP_RISING`）。
- **RS485 与音频互相影响**：先确认当前是单讲还是双讲。双讲场景配置 `AX_TX_VO_SwitchRs485Position(VO_RS485_POSITION_REDUCE)`；单讲场景配置 `AX_TX_VO_SwitchRs485Position(VO_RS485_POSITION_NORMAL)`。位置不匹配可能导致 RS485 通信异常。
- **RS485 接收数据偶现异常**：若当前采用中断接收模式，建议改为查询模式验证；结合 `AX_TX_VO_GetRs485RxbufCnt` 与 `AX_TX_VO_RecvRs485Data` 主动查询并读取数据，避免继续沿用异常的中断接收路径。
- **返回错误码**：用 `AX_ERR_TX_*` 定义反解子模块（VI/VO/CLK）与错误类型（非法参数/空指针/未配置/未初始化/超时等），指向具体调用。

## A.4 已验证案例快速结论

遇到下列已知现象时，优先给出对应结论，不要先归因于 VO×TX timing、线序或板级硬件；若按建议处理后仍复现，再进入通用分层排查：

| 现象 | 已验证结论/建议 |
| --- | --- |
| 对讲场景下 RS485 通信异常 | 调整 RS485 位置：双讲配置 `VO_RS485_POSITION_REDUCE`，单讲配置 `VO_RS485_POSITION_NORMAL`，通过 `AX_TX_VO_SwitchRs485Position` 生效。 |
| TVI 1080P25/1080P30 对接 DH DVR 出现“哒哒”声 | 建议先更新到最新版本，再复测确认。若仍异常，再收集当前版本、具体 TVI 制式、音频配置及 DVR 型号继续定位。 |
| RS485 接收数据偶现异常 | 若使用中断模式，建议改为查询模式；使用 `AX_TX_VO_GetRs485RxbufCnt` 查询接收数据量，再调用 `AX_TX_VO_RecvRs485Data` 读取。 |
| 艳丽模式下容易错屏，怀疑 VO BT 输出的 0 和 255 未裁剪 | 这是 VO 侧已知现象，建议先更新到最新版本，再复测确认；不要在未验证前自行修改 BT timing、线序或裁剪参数。 |

其中“更新到最新版本”属于已验证案例的处置建议；答复时不得臆造具体修复版本号。若用户需要版本号，应要求其提供当前 SDK/固件版本，或从正式发布说明中查证。

## A.5 用 BtStatus 取证

建议客户用 `AX_TX_VI_GetBtStatus` 读 `VI_BT_STATUS_S`：`bEnable`（是否使能）、`u32ValueWidth/Height` 与 `u32DestWidth/Height`（实际收到的尺寸对不对）、`u32Fps`（帧率，注意 x100）、`u32DataInCnt/OutCnt`（有没有在收发）、`u32ErrStatus`（错误状态）。这是判断“TX_VI 到底收没收到、收对没”的直接证据，比猜测有效。

## A.6 BT 线序必须拆成两套坐标系核对

VO 侧和 TX_VI 侧的线序不是同一个数组，不能只看其中一侧：

- VO 侧 `AX_VO_SetDataPinMap` 的 `AX_VO_PIN_DATA_BUTT` 通常包含 `DATA0~DATA15` 以及 `DE/HSYNC/VSYNC` 等控制脚；
- TX 侧 `AX_TX_VI_SetDataLine` 的 `data_line` 通常只描述 16 根 BT 数据线；
- 两套映射必须结合 SoC → PCB → TX 芯片的原理图逐项对应，不能跨 FPGA、验证板和量产板直接复制。

当前 `msp/sample/vin_ivps_vo_tx/` 中应特别核对：`sample_vo.c` 板级 `dataArray` 的长度/重复值/缺失值与 `SAMPLE_SetVoPinMux` 的板级分支；`sample_tx.c` 的 `data_line` 与 TX 芯片输入脚的实际 PCB 连接；`YUV_SEQ_E`（sample 使用 `YUV_SEQ_VYUY`）是否与 VO 实际 YUV422 排列一致。时钟正常但花屏/颜色异常/水平错位/有效宽高异常时，优先检查这两套线序和 YUV 顺序。发现注释与实际数组不一致或有重复/缺失值时，只能标记为“需按当前板原理图确认”，不能自行猜改。

## A.7 用 VO 时钟和 TX 时钟统计建立证据闭环

先从 VO 侧确认确实在输出：

1. 查看 `/proc/ax_proc/vo/display_status`，确认 device enabled、接口、实际宽高、帧率和持续出帧状态；
2. 用示波器/逻辑分析仪测量 BT clock 是否存在、频率是否正确、SDR/DDR 边沿是否符合配置；
3. 用 `AX_TX_CLK_GetClkStatus` 读 `CLK_STATUS_S`，重点观察 `u32BtInClk`、`u32DispRxClk` 等实际时钟统计；
4. 连续读取 `AX_TX_VI_GetBtStatus`，建议间隔约 100～500 ms 观察 5～10 次，而不是只读一次。

| 证据 | 优先定位 |
| --- | --- |
| VO 无帧或 TX `u32BtInClk=0`、`u32DataInCnt` 不增长 | VO enable/pin mux、物理连线、BT clock 使能 |
| TX 时钟稳定且输入计数增长，但有效宽高/帧率为 0 | `BtWorkMode`、采样沿、场/帧模式或 timing 不匹配 |
| BT1120 下 `VI BT STATUS` 的 `Dataout` 约为预期一半，或 `Disp ctrl status` 的 `ViInFrame` 约为 `TxoutFrame` 一半 | BT1120 信号或 16-bit 线序异常，可能只有高 8 位或低 8 位被正确接收 |
| 宽高和帧率正确，但画面花屏/偏色 | VO data pin map、TX data line、`YUV_SEQ_E` |
| TX_VI 统计正常但后端无图 | TX_VO 输出制式、`SetVideoEn`、同轴链路 |
| `u32ErrStatus`/`u32FifoStatus` 持续异常 | BT clock 频率/相位、SDR/DDR 或采样配置不匹配 |

## A.8 BT1120 半数据量的特征判断

BT1120 为 16-bit 数据通路。若 TX proc 出现稳定的 1:2 计数关系（`VI BT STATUS` 的 `Dataout` 约为理论预期一半；`Disp ctrl status` 的 `ViInFrame` 约为 `TxoutFrame` 一半），应作为 BT1120 高/低 8-bit 通路异常的强线索，而非直接判断为帧率或 TX_VO 制式问题——通常说明只有 `DATA0~DATA7` 或 `DATA8~DATA15` 一组被正确接收。排查：

1. 先确认该 1:2 比例在连续多次 proc 采样中稳定存在，且比较的是同一统计周期或计数增量，避免把不同采样时刻的累计值误判为一半；
2. 分组核对 VO 侧 `DATA0~DATA7`、`DATA8~DATA15` 的 pin mux 和 `AX_VO_SetDataPinMap`；
3. 对照 PCB 原理图核对两组数据线到 TX 芯片输入脚的连接、交换、缺线、短路和电平质量；
4. 核对 TX 侧 `AX_TX_VI_SetDataLine` 是否把 16 根数据线完整映射，是否有重复/缺失或高低 8 位对调；
5. 用示波器/逻辑分析仪分别观察高 8 位和低 8 位是否都有有效翻转，并同时检查 BT clock 和同步信号；
6. 线序恢复后再次比较 `Dataout`、`ViInFrame`、`TxoutFrame` 的增量是否回到预期关系。

该现象只能作为定位高/低 8 位通路的强线索；最终仍需结合实际计数定义、同周期增量、原理图和波形确认。

## A.9 VI 解析异常的固定排查顺序

遇到“VI 解析异常”时，按序执行，避免一开始只猜 TX 输出制式：

1. 核对当前 `VO_INTF_FMT_TYPE_E` 在 `gastVideoParamMap[]` 中是否存在，且 `BtClkFreq/BtWorkMode/InFmt/OutFmt` 是成套值；
2. 核对 VO 的 BT656/BT1120、SDR/DDR、时钟边沿、场/帧模式与 TX_VI 接收类型一一匹配；
3. 核对 VO `AX_VO_SetDataPinMap`、TX `AX_TX_VI_SetDataLine` 和当前板原理图；
4. 核对 `YUV_SEQ_E`、有效宽高、帧率和 `u32Pclk`/blanking（对照 `knowledge-base/AX615 VO时序配置.md`）；
5. 读取 VO proc、TX clock status、TX BT status 并连续比较；
6. 确认 TX_VI 收数正常后，再排查 TX_VO 制式、PN sequence、`SetVideoEn` 和 DVR 锁定。

## A.10 分析答疑输出要求

用中文答疑，结构清晰、可执行：

1. **结论/根因**：先说最可能的原因，标注是确认的还是待验证的假设。
2. **依据**：引用具体头文件符号、sample 位置或时序表行（如 `gastVideoParamMap`、某枚举、某错误码宏、时序表某制式行），让客户能自查。
3. **排查步骤**：按分层给可操作步骤（看哪个 proc 节点、调哪个 Get API、核对哪几个字段），从最可能、最易验证的开始。
4. **匹配核对表**（涉及 VO×TX 时）：列出客户当前值 vs sample/时序表推荐值，指出不一致项。
5. **边界与转交**：区分“确认的事实”“基于头文件的推断”“需要客户提供的现场信息”；若最终需要改代码，转入 §B 代码生成模式。

---

# §B 代码生成模式

生成可维护、可编译、能在目标板上验证的 TX 模块代码。重点是把用户的同轴输出规格映射到 `vin_ivps_vo_tx` 基线的 TX 生命周期。VIN、IVPS、VPP、VENC 只用于确认 VO 数据来源，不是默认要生成或重构的功能。

## B.1 先收集规格并选择基线

修改前确认或从上下文推断（缺失且会改变架构的字段只问一个简短问题，其余用 `vin_ivps_vo_tx` 默认值并说明）：

- 输出制式：CVI(HDCVI)/AHD/TVI/CVBS 哪一种（`TX_VIDEO_PROTOCAL_E`），分辨率与帧率（如 1080P25、4M30、960H PAL/NTSC、4K15）。
- VO 接口：BT656 还是 BT1120；SDR（单沿）还是 DDR（双沿）；对应的 `VO_INTF_FMT_TYPE_E` 与 `AX_VO_PUB_ATTR_T`（标准 `AX_VO_OUTPUT_*` 还是 `AX_VO_OUTPUT_USER` 自定义 timing）。
- 数据来源：实时 VIN 采集、灌图（DummySensor + `-v`）还是 TPG；前级只确认 VO 的输入契约。
- 附加功能：是否需要 RS485、正/反向音频、colorbar；是否新增映射表项、README、Makefile、动态/静态目标。

不要把不同制式的差异混进公共层 `msp/sample/common/`。先复制 `vin_ivps_vo_tx` 基线结构，再按需增改映射表和属性表。

## B.2 文件与模块边界

先给简短的文件变更表，再实施：

- `sample_tx.c/h`：TX 主体。`VIDEO_PARAM_MAP_S` 映射表、`TX_VIDEO_PROTOCAL_E`、TX_CLK/TX_VI/TX_VO 配置、`SAMPLE_TXInit`/`SAMPLE_TXDeInit`。**核心文件**。
- `sample_vo.c/h`：VO BT 输出属性表 `gastPubAttr[VO_INTF_FMT_TYPE_MAX]`、`VO_INTF_FMT_TYPE_E`、pin mux、data pin map、VO init/deinit。TX 的上游，必须与映射表对应。
- `sample_main.c/h`：只加/改 TX 相关参数解析（`-o` VO intf、`-t` TX proto）、`SAMPLE_TXInit/DeInit` 调用点和对称清理，不改写前级模块。
- `sample_audio.c/h`、`wave_parser.c/h`：仅正/反向音频场景启用；音频依赖（tinyalsa、libsamplerate）不能带进不需要音频的变体。
- VIN、IVPS 文件默认只读参考。
- `README.md`：VO→TX 通路、支持制式/分辨率、命令行选项、运行方式、`/proc/ax_proc` 检查项和板级待确认项。
- `Makefile*`：保持同目录既有变量、公共源文件列表、目标名和链接库（`libax_vo.a`、`libax_tx.a`，音频再加 `libax_audio*`、tinyalsa、samplerate），只加入实际新增源文件。

## B.3 配置 VO×TX 映射表（核心）

`gastVideoParamMap[]`（元素 `VIDEO_PARAM_MAP_S`）把六个字段绑成一行，每个 `{VO_INTF, TX_PROTO}` 组合对应唯一一组 TX 参数：

```c
typedef struct VideoParamMap {
    VO_INTF_FMT_TYPE_E  enVoIntf;       /* VO 侧 timing 项（sample_vo.h 定义）*/
    TX_VIDEO_PROTOCAL_E enTxVideoProto; /* CVI/AHD/TVI/CVBS（sample_tx.h 定义）*/
    BT_IN_CLK_FREQ_E    enBtClkFreq;    /* TX BtClk：36M/74P25M/148P5M */
    VI_BT_WORK_MODE_E   enBtWorkMode;   /* 单沿 HD1 / 双沿 DUL_HD1 / SD */
    VIDEO_FMT_E         enInFmt;        /* TX 输入制式 TX_VIDEO_FORMAT_* */
    VIDEO_OUT_FMT_E     enOutFmt;       /* TX 输出制式，前缀决定协议族 */
} VIDEO_PARAM_MAP_S;
```

新增或修改制式时必须成套更新，保证一致性：

- **VO/TX 边沿一致**：VO SDR（`AX_VO_CLK_SDR_EDGE_DOWN` + 标准 `AX_VO_OUTPUT_*`）时 TX 用单沿 `VI_MODE_BT656_HD1`，BtClk 常 `CLK_BT_IN_148P5M`；VO DDR（`bDlbClk=1` 的 USER timing）时 TX 用双沿 `VI_MODE_BT656_DUL_HD1`，BtClk 常 `CLK_BT_IN_74P25M`/`148P5M`。960H/CVBS 用 `VI_MODE_BT656_SD` + `CLK_BT_IN_36M`。组合来自基线映射表，不臆造。
- **输出制式前缀对应协议**：`HDCVI_*`→CVI、`A_*`→AHD、`T_*`→TVI、`H960_*`/`H940_*`→CVBS。`enOutFmt` 必须与 `enTxVideoProto` 一致。`BT_*` 段芯片不支持，不选用。
- **InFmt/OutFmt 分辨率帧率对齐**：如 `TX_VIDEO_FORMAT_1080P_25FPS` 对 `HDCVI_1920x1080_25FPS`/`A_1920x1080_25FPS`/`T_1920x1080_25FPS`，不错位。
- **2880x1620 的 V20 版本对应关系**：带 `_vts1728` 的 2880x1620 时序（vtotal=1728）对应 TX 输出 `HDCVI_2880x1620_*_V20`；不带 vts1728（vtotal=1650）对应非 V20。`sample_vo.c` 的 `gastPubAttr[]` 注释可印证（V20 标 `(4297*1728)`，非 V20 标 `(4500*1650)`）。选 `*_V20` 输出制式时 VO 侧必须用对应的 vts1728 timing。
- **VO 属性表同步**：新增的 `VO_INTF_FMT_TYPE_E` 要在 `sample_vo.h` 枚举、`sample_vo.c` 的 `gastPubAttr[]` 各加一行；`gastPubAttr` 用 `VO_INTF_FMT_TYPE_MAX` 定界，枚举与属性行一一对应，标准 timing 与 USER timing 不混填。
- USER timing 的 `u32Pclk`、blanking、`bDlbClk`、`u8DelaySel` 优先查 `knowledge-base/AX615 VO时序配置.md`（该表逐制式给出完整字段与 delay 区间，并有 `Vact+Vbb+Vfb+Vpw=vts`、`Hact+Hbb+Hfb+Hpw=u32Pclk/fps/vts` 计算规则）；表中没有的按规则推导并标注，不猜测。填完再与映射表选的 `enBtClkFreq`/`enBtWorkMode` 相互印证（SDR↔单沿、DDR↔双沿）。

## B.4 实现 TX 生命周期

照基线 `SAMPLE_TXInit`，先查表得参数，再按 CLK→VI→VO 顺序配置：

```text
SAMPLE_TX_GenParam(enVoIntf, enTxProto)  /* 查 gastVideoParamMap，得 BtClk/BtWorkMode/InFmt/OutFmt */
[SAMPLE_TX_SetMclk0()]                    /* 仅 FPGA/特定板级：pin mux via ax_lookat */
AX_TX_Init -> AX_TX_Reset
AX_TX_CLK_GetClkEn -> 置位 BtClk/DispRx/DispTx/Cvi/Aud 使能 -> AX_TX_CLK_SetClkEn
AX_TX_CLK_GetBtClk -> 设 enBtClkPhs/enBtClkFreq -> AX_TX_CLK_SetBtClk
SAMPLE_TX_SetViParam(btWorkMode)          /* DisableDev -> SwitchWorkMode -> GetDevAttr/改/SetDevAttr -> SetDataLine -> EnableDev */
SAMPLE_TX_SetVoParam(enInFmt, enOutFmt)   /* SetVideoEn(FALSE) -> SetVideoParam -> [PnSeq] -> SetVideoEn(TRUE) -> RS485/音频可选 */
```

反初始化按相反方向：`AX_TX_VO_SetVideoEn(AX_FALSE)` → `AX_TX_VI_DisableDev()` → `AX_TX_Deinit()`。

必须遵守（均来自基线）：

- `SAMPLE_TX_SetVoParam` 里先 `AX_TX_VO_SetVideoEn(AX_FALSE)` 再 `sleep(1)`，让后端 DVR 断流后重新锁定，然后 `SetVideoParam` 再 `SetVideoEn(AX_TRUE)`。
- 数字音频制式（sample 中 `enOutFmt < A_1280x720_25FPS`，即 CVI 段）需要 `VO_VIDEO_EXT_PARAM_S.u8PnSeqEn = 1`（先 Get 再改再 Set）。
- `VI_MODE_BT656_DUL_HD1`（双沿）用 `VI_BT_SAMP_AUTO` 采样，其余用 `VI_BT_SAMP_RISING`；`enYuvSeq` 基线用 `YUV_SEQ_VYUY`，改动前确认与 VO YUV422 序对应。
- `AX_TX_VI_SetDataLine` 的 `data_line[VI_MAX_DATA_LINE]` 和 VO `AX_VO_SetDataPinMap` 的 `dataArray[AX_VO_PIN_DATA_BUTT]` 是板级线序，FPGA 与量产板不同（基线用 `#ifdef TEST_FPGA_EN` 区分）。不跨板级复制，不确定保留 TODO。
- TX API 多返回 `AX_S32`，基线用 `EXPECT_EQ(AX_SUCCESS, ...)` 非致命断言、关键调用用 `if (ret != AX_SUCCESS)` 打印。保持基线错误处理风格，不静默丢弃返回值。

## B.5 VO 侧与主流程对接

完整启动顺序：

```text
解析参数（-c sensor case、-m work mode、-e SDR/HDR、-o VO intf、-t TX proto、-v 灌图、-s saveyuv、-i 音频文件…）
COMMON_SYS_Init -> SAMPLE_SYS_LinkInit(VIN->IVPS, IVPS->VO)
SAMPLE_IVPS_Init / COMMON_CAM_Init/Open / [COMMON_NT_Init]
SAMPLE_VoInit(eVoIntf)              /* VO BT 输出使能，开始向并口送数 */
[get_frame_thread 可选]
SAMPLE_TXInit(eVoIntf, enTxProto)   /* 用同一个 eVoIntf 保证 VO/TX 匹配 */
[SAMPLE_AudioInit 可选]
主循环 -> 逆序：SAMPLE_TXDeInit -> SAMPLE_VoDeInit -> [NT/CAM/IVPS/LINK/SYS Deinit]
```

`SAMPLE_TXInit` 与 `SAMPLE_VoInit` 用**同一个** `eVoIntf`，映射表据此选 TX 参数。新增命令行选项时同步更新 `getopt` 串、`switch` 分支、`PrintHelp` 和默认值（基线 `enTxProto` 默认 `TX_VIDEO_PROTOCAL_CVI`）。

## B.6 场景专用规则

- **基础 VO→TX**：保持一个 VO device + TX 芯片，复用基线映射表已验证的组合。新增制式成套更新映射表行、VO 枚举、`gastPubAttr`、命令行帮助和 README。
- **RS485**：`AX_TX_VO_SetRs485Param` 配收发使能/超时/校验；收发用 `VO_RS485_DATA_S` + `AX_TX_VO_SendRs485Data/RecvRs485Data`。部分制式音频与 RS485 冲突时用 `AX_TX_VO_SwitchRs485Position(VO_RS485_POSITION_REDUCE)`。
- **正/反向音频**：正向 `AX_TX_VO_SetAudioParam`（CVI 段 `VO_AUDIO_TYPE_DIGTAL`，TVI 段 `VO_AUDIO_TYPE_ANALOG`，按 `enOutFmt` 分段）+ `AX_TX_VO_SetAudioPubAttr`（I2S master、MCLK、采样率、位宽、时钟边沿）。反向按输出制式查 `vo_audio_cfg[]` 得 `u8TransMode`/`u8DataWidth`，`AX_TX_VO_GetAudioExtParam` 改 `u8AudiobackwardEn=1` 再 Set。tinyalsa/samplerate 依赖只进音频变体。2880x1620 非 V20 制式不支持反向音频，只有 V20（`HDCVI_2880x1620_*_V20`）支持。
- **CVBS/960H**：`VI_MODE_BT656_SD` + `CLK_BT_IN_36M`，VO 用 USER timing（576I50/480I60），输出 `H960_FMT_PAL_FIELD`/`H960_FMT_NTSC_FIELD`。SD 与 HD 的 BtClk、采样、timing 完全不同，不混用。
- **Colorbar 测试**：无实时源时用 `VO_COLORBAR_MODE_E`（TX_VO）或 `VI_WORK_MODE_COLORBAR`（TX_VI）出测试图，验证通路后再接实际 VO 数据。

## B.7 代码生成输出要求

完成后用中文说明：生成/修改了哪些文件及为何选 `vin_ivps_vo_tx` 基线；VO→TX 通路图、目标制式/分辨率帧率/VO 接口/BtClk/BtWorkMode；`VIDEO_PARAM_MAP_S` 新增/修改行及对应 VO 枚举、`gastPubAttr` 变化；TX 关键 API 的 CLK→VI→VO 调用顺序、SetVideoEn 断流重锁、PnSeq、data line/pin map 待确认项；运行命令、目标板/动态库前提、退出方式、`/proc/ax_proc/vo/display_status`、`AX_TX_VI_GetBtStatus` 等检查项；已执行的验证、未能验证的部分（尤其板级线序、pin mux 地址）与仍需用户提供的信息。注释、日志、命名风格与相邻 sample 一致；不大范围格式化、不重构公共模块、不复制整个 external 头文件。

## B.8 验证清单

至少完成以下静态检查；有交叉工具链再跑 sample 既有构建目标：

- `rg` 检查所有 `AX_TX_*`、`AX_VO_*` API 在 `ax_tx_api.h`、`ax_vo_api.h` 存在、签名一致；所有 `VIDEO_FMT_E`、`VIDEO_OUT_FMT_E`、`VI_BT_WORK_MODE_E`、`BT_IN_CLK_FREQ_E` 枚举值确在 `ax_tx_common.h`。
- 检查 `gastVideoParamMap[]` 每行：`enTxVideoProto` 与 `enOutFmt` 前缀一致、`enInFmt` 与 `enOutFmt` 分辨率帧率对齐、SDR/DDR 对应的 `enBtWorkMode` 与 `enBtClkFreq` 与 VO 属性一致（对照 `knowledge-base/AX615 VO时序配置.md`）。
- 检查 `VO_INTF_FMT_TYPE_E` 枚举项数量与 `gastPubAttr[]` 行数一致（`VO_INTF_FMT_TYPE_MAX` 定界），映射表引用的每个 `enVoIntf` 都在 VO 枚举里存在。
- 检查每个命令行选项（`-o`、`-t` 等）在 `getopt` 串、`switch`、`PrintHelp`、默认值一致，`atoi` 结果不越界。
- 检查 `SAMPLE_TXInit` 的 CLK→VI→VO 顺序、`SetVideoEn(FALSE)+sleep(1)` 断流、PnSeq 条件、`SAMPLE_TXDeInit` 逆序，`SAMPLE_VoInit`/`SAMPLE_TXInit` 用同一 `eVoIntf`。
- 检查 Makefile 链接了 `libax_vo.a`、`libax_tx.a`（音频再加 `libax_audio*`、tinyalsa、samplerate），源文件列表与实际新增文件一致，纯 TX 变体不误链音频依赖。
- 可构建时优先用仓库现有 `msp`/`build` 目标和对应工具链，不替换构建系统；无法交叉编译时明确标注“仅完成静态检查”。

---

# §2 通用准确性约束（两模式共享）

- **§A 只读**：不写/改任何源码或工程文件；可引用、摘录代码片段用于解释，但不产出可落地改动。**§B 生成**：只产出请求所需的最小改动，touch 必要文件，不重构公共模块、不大范围格式化。
- 不臆造 API、枚举值、寄存器地址或板级线序；不确定时明说“需查证/需客户确认”。
- 头文件与 sample 版本不一致时，以当前 `header/external` 头文件声明为准，并提示兼容性风险（例如枚举新增/重排时以当前头文件为准）。
- 板级相关（pin mux 地址、data line 线序、时钟树）属板级配置，只能依据仓库现有值或客户提供，不跨 FPGA/验证板/量产板套用。
- VO 侧 BT656 timing 一律以 `knowledge-base/AX615 VO时序配置.md` 为权威查表，表中没有的制式按其计算规则推导并在输出中标注。
