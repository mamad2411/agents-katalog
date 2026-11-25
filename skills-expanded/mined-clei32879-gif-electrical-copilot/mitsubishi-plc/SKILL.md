---
name: mitsubishi-plc-skill
description: 三菱 PLC 编程快速参考技能（FX 系列为主，兼 Q/L/iQ-F），覆盖 GX Works2/3、软元件（X/Y/M/S/D/T/C/特殊）、基本指令与常用应用指令（MOV/CMP/ADD、定时计数、高速、脉冲定位、通信 MC 协议/CC-Link/Modbus）、与威纶通 HMI、伺服（MR-JE 等）联动。用于编写、审查、调试三菱 PLC 程序。深层厂商细则路由到 plc-skill 的三菱模块。
metadata:
  {
    "version": "1.0.0",
    "author": "Local Industrial Setup",
    "tags": ["mitsubishi", "plc", "fx", "gxworks", "melsec", "servo", "modbus"]
  }
---

# 三菱 PLC 编程 Skill（快速参考）

与 `plc-skill` 的三菱 vendor 模块配合：本技能给高频操作速查，复杂/边界情况以官方手册为准。

## 一、软件与工程

- **GX Works2**（FX/Q/L）、**GX Works3**（iQ-F FX5U/iQ-R，结构化工程）。
- 梯形图/指令表/ST/FBD 混合；FX5U 支持结构化文本与功能块。
- 工程：新建 → 选机型（FX3U-32MT/ES 等）→ 全局标签/软元件注释 → 写程序 → 编译 → 写入 PLC → 在线监控（软元件/时序图/强制）。
- 仿真：GX Works2/3 内置仿真器可离线调试逻辑。

## 二、软元件速记（FX3U 为例）

| 类别 | 范围 | 说明 |
|---|---|---|
| 输入 X | X0~X7（8 进制） | 外部输入 |
| 输出 Y | Y0~Y7（8 进制） | 外部输出 |
| 中间 M | M0~M7679 | 内部继电器 |
| 状态 S | S0~S4095 | 步进/状态（SFC） |
| 定时 T | T0~T255 | 100ms/10ms/1ms 段 |
| 计数 C | C0~C255 | 16/32 位，C235+ 高速 |
| 数据 D | D0~D7999 | 数据寄存器 |
| 特殊 M/D | M8000+ / D8000+ | 系统状态（M8000 常ON、M8002 首次扫描） |

## 三、基本与常用指令

- 基本：LD/LDI/AND/ANI/OR/ORI、ANB/ORB、SET/RST、PLS/PLF、MPS/MRD/MPP、OUT(定时/计数)。
- 应用（FNC 号）：MOV(FNC12)、CMP(FNC10)、ZCP(FNC11)、ADD/SUB/MUL/DIV、INC/DEC、BMOV、FMOV、BCD/BIN、ENCO/DECO、比较类、数据检索。
- 定时/计数：`OUT T0 K50`（50×100ms=5s）；`OUT C0 K100`，用 `RST C0` 复位。
- 高速计数：C235+（单相）配合 DHSCS/DHSCR/DHSCZ 中断比较。
- 脉冲/定位：PLSY、PLSR、定位 DRVI/DRVA（FX3U 配 1PG/高速输出）；FX5U 用定位指令更丰富。
- PID：PID 指令（FX3U 支持，参数放 D 区）。

## 四、通信

- **编程口协议**：FX 串口/以太网（MC 协议 4E 帧）——威纶通 HMI 选「Mitsubishi FX」或「FX3U-ENET」。
- **CC-Link**：远程 I/O 站；**CC-Link IE** 总线（FX5U/Q）。
- **Modbus**：FX3U-485ADP 等做 Modbus RTU 从/主站；FX5U 以太网做 Modbus TCP。
- **与威纶通**：EBPro 设备选三菱 FX（串口）或 MC 协议（以太网），地址用 `M100`、`D0`、`X/Y`。

## 五、调试排障

- PLC 不运行：RUN 开关/远程 RUN、程序保护、电池低（ERR 闪）。
- 输出无：强制状态、Y 双线圈（同一线圈多次 OUT 常见问题）、输出回路电源/COM。
- 通信：协议、站号、波特率、线序、是否被占用（编程口同时连 HMI 与编程线时冲突）。
- 用 GX Works 在线监控逐点跟踪，时序图查抖动脉冲。

## 安全边界

- 改定位/伺服/高速参数先备份；急停/安全回路必须硬接线独立于 PLC 程序。
- 与 plc-skill 的西门子/罗克韦尔等术语不混用（三菱用 X/Y/M/D 体系）。

## 参考

- `references/fx-quickref.md` — FX 指令与软元件更全速查
- `references/gxworks-notes.md` — GX Works2/3 操作与下载调试要点
- 深层路由：`plc-skill` → `references/vendors/mitsubishi/`
- 配合：`hmi-skill`（威纶通连三菱）、`computer-use-skill`（操控 GX Works）
