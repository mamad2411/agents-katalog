---
name: inovance-plc-skill
description: 汇川（Inovance）PLC 与伺服技能，覆盖 H3U/H5U/AM 系列、AutoShop/InoProShop 编程环境、EtherCAT 运动控制（IS620N/IS650 伺服、总线定位）、H1U/H2U/H3U 小型机（类三菱 FX 风格）、Modbus 通信、伺服参数与调试。用于编写、审查、调试汇川 PLC/伺服程序。
metadata:
  {
    "version": "1.0.0",
    "author": "Local Industrial Setup",
    "tags": ["inovance", "hcf", "plc", "h3u", "h5u", "am", "servo", "ethercat", "autoshop", "inoproshop"]
  }
---

# 汇川（Inovance）PLC 与伺服 Skill

覆盖汇川常用机型与工具链。汇川产品线与三菱/欧系对应关系强，注意区分：

- **H1U/H2U**：小型机，指令类三菱 FX。
- **H3U**：主流小型机，类 FX3U 风格 + EtherCAT 从站/主站能力，AutoShop 编程。
- **H5U**：中型机，结构化工程，InoProShop（Codesys 内核），ST/FBD/梯形图，EtherCAT 运动控制。
- **AM 系列**：中型，Codesys 内核，InoProShop。
- **IS620N / IS650 / SV660N 等伺服**：总线（EtherCAT/Profinet）+ 脉冲，配汇川/禾川等电机。

## 一、编程环境

- **AutoShop**（H1U/H2U/H3U/IT 系列等）：工程树 → 程序（主/子/中断）→ 软元件表 → 编译下载 → 在线监控/时序图。类三菱 GX Works 操作。
- **InoProShop**（H5U/AM/AC800 等，Codesys 内核）：POU、任务配置、变量表、EtherCAT 主站配置、运动控制功能块（MC_MoveAbsolute 等）、在线下载（支持热下载）与 Trace。
- 两套工具**不要混用机型**：H3U 用 AutoShop，H5U/AM 用 InoProShop。

## 二、软元件/变量速记

- H3U（类 FX）：X/Y/M/S/T/C/D、特殊 M/D（M8000 常ON、M8002 首扫描）；地址与三菱 FX 体系类似，编程时以官方手册为准。
- H5U/AM（Codesys）：用**变量名**（全局变量、I/O 映射、总线从站变量），无传统地址概念；定位用 MC 功能块操作轴对象。

## 三、运动控制（重点，用户场景多）

### 脉冲方式（H3U + IS620N 脉冲型/步进）
- 高速输出端发脉冲（Y0/Y1 类），配方向信号；伺服设脉冲模式（位置模式、电子齿轮）。
- 定位指令：DRVI/DRVA（相对/绝对）或 PLSY/PLSR（定速/加减速）。

### EtherCAT 总线方式（H5U/AM + IS620N EtherCAT，或 H3U 扩展 EtherCAT）
- InoProShop：EtherCAT 主站 → 扫描/添加 IS620N 从站 → 映射 PDO（控制字/目标位置/速度/扭矩、状态字/实际位置/实际速度）。
- 运动指令：MC_Power、MC_Home、MC_MoveAbsolute、MC_MoveVelocity、MC_Stop、MC_Jog；轴状态机（Disabled→Standstill→Moving 等）。
- 伺服使能、回原点（Home）、限位、急停（EtherCAT 急停建议仍走硬线）。

### 伺服调试
- 汇川伺服调试软件（如 InoDriverShop/伺服调试助手）：参数读写、试运行（Jog/定位）、示波器看跟随误差、惯量辨识。
- 关键参数：脉冲模式（PP）/速度（S）/扭矩（T）、电子齿轮比（分子/分母）、方向、增益、惯量比、编码器分辨率。
- 报警：过流、过压、过载、编码器断线等，查官方报警码表。

## 四、通信

- Modbus RTU/TCP：H3U 485 做主/从站；H5U 以太网/串口；伺服可用 Modbus 读写参数。
- EtherCAT：主从站配置与 PDO 映射是核心。
- 与威纶通 HMI：H3U 可选「Inovance H3U」驱动或 Modbus；H5U 用 Modbus TCP / EtherNet/IP。
- 编程口/以太网连接 AutoShop/InoProShop 下载程序。

## 五、调试排障

- 程序不下载/连不上：通信设置、IP、型号选错、编程口被占用。
- 轴不动：使能未给（MC_Power=TRUE 且无急停）、模式/轴映射错、电子齿轮、硬限位/软限位触发、伺服报警。
- 伺服抖动：增益过高、惯量比不匹配、机械谐振（用滤波器/降低增益）。
- 通信断：站号/波特率/线序/终端电阻。

## 安全边界

- 运动控制改动（加减速、位置、方向）直接影响设备动作，先在安全距离/空载验证。
- 急停、门锁、光幕必须硬回路，不依赖总线或程序逻辑。
- 备份工程与伺服参数后再改。

## 参考

- `references/inoproshop-ethercat.md` — H5U/AM + InoProShop + EtherCAT 配置与 MC 指令
- `references/servo-tuning.md` — IS620N/SV660N 伺服参数与调试要点
- 配合：`hmi-skill`、`plc-skill`（通用控制模式）、`computer-use-skill`（操控 AutoShop/InoProShop）
