---
name: win-console-inject-probe
description: Windows 终端 TUI 工具注入与屏读探测工作流——为新 CLI 工具（终端里跑的 coding agent TUI）定 Windows 注入规格（事件形态/分块/回车/方向键/写入确认）与屏读形态矩阵（整屏 dump/锚判据/解析期望），或诊断注入故障与屏读解析失配。Use whenever 用户要探测某工具能否注入 Windows 终端、接入新 CLI 前的规格探测、注入异常诊断（写不进/被吞/打完字不提交/停摆）、屏读解析与实机不符的诊断（读得到屏但解析不出/误报形态/卡片与终端脱钩）、或版本升级后复验规格。不适用 GUI/APP 类工具（见「边界与转介」）。
---

# Windows 终端注入探测（win-console-inject-probe）

为新终端 TUI 工具定注入规格，或诊断注入故障。方法论经 M6R 全量实证 + 独立评审闭环（2026-09-18，兔维斯 项目）。

## 核心认知（三句话，先内化）

1. **「消费墙」不存在**：Windows 控制台输入缓冲无界动态增长，WriteConsoleInput 无「缓冲满」失败模式（官方文档+两代 conhost 源码+ReactOS 三重实证）。看到「写不进」先怀疑自己的探测方法（错误码采集/部分写处理/形态错误），再怀疑目标。
2. **真正的约束在 TUI 事件形态层**：每家 TUI 框架对输入事件的取舍不同（纯字符形态的控制键可能被丢、裸 ESC 可能被当按键吃）。**能不能注入是通用的，怎么注入才被正确理解要逐家定规格**。
3. **按族入座**：绝大多数工具落入两个已知族之一（见下）；新族才需要全量方法论。

## 快路径（新工具确认性探测，30–60 分钟）

### P0 · 环境与会话（5 分钟）

- 记录：OS build、PowerShell 版本、Windows Terminal 版本、目标 CLI `--version`、宿主类型。
- 临时项目目录（如 `$env:TEMP\probe-<tool>`）；用 `scripts/launch-session.ps1` 起 **conhost + WT 各一个**会话，记 PID 树。
- 首启信任/确认对话框：用注入通道自身处理（VK 形态回车或数字键）——成功关闭本身即送达证据。

### P1 · 模式采样定族（5 分钟，判别力最强）

用 `scripts/probe-mode.ps1` 对目标 CONIN$ 句柄采 idle/busy 两态各 2 次：

| GetConsoleMode | 族 | 已知成员 |
|---|---|---|
| `0x0208`（WINDOW_INPUT\|VT_INPUT，RAW_VT） | **A 族（Node/libuv·ink 系）** | claude 2.1.251、kimi 2.0.0、opencode 1.18.31 |
| `0x01F0`（MOUSE\|INSERT\|QUICK_EDIT…，无 VT_INPUT） | **B 族（Rust crossterm 系）** | codex 0.154.0 |
| 其他 | **新族** → 读 `references/methodology.md` 走全量流程 |

定族后读 `references/known-families.md` 拿该族预填规格——后续步骤变为「验证预填 + 找例外」。

### P2 · 短消息地面真值（5 分钟）

注入 39 字符短消息 + VK 回车 → 确认**会话文件命中**（会话文件位置每家不同，P2 顺带定位并记入规格表——这是写入确认机制的根基）。截图辅助。**存储形态注意**：JSONL 类用 `scripts/verify-stamp.ps1` grep 对账；**SQLite 类（如 opencode，WAL 库）grep 不可用**——拷贝 db+wal+shm 副本后查询（参考实现 `scripts/verify-oc.py`），勿查活库。

### P3 · 长度阶梯（15 分钟，规格确认核心）

`scripts/probe-e5.ps1`（基线参数：**80 字符/块、块间 50ms、正文后 150ms 发 VK 回车、成对按下/抬起事件**）：200 / 2000 / 10000（或项目上限）三档 × 双宿主 × ≥3 取样。判据：全量精确到达（会话文件长度对账，注意尾空格类 TUI 修剪按语义归一）。

**慢消费者判定（上长度档前先做）**：首档 200 字符注入后，若 stamp 迟迟不入库或回车响应迟缓 → 先用 `scripts/observe-occ.ps1` 采占用率曲线。消费速率慢的工具（如 opencode ~70 事件/秒，非瞬时排空）**固定节流会堆深队列并可能丢提交回车**（消息边界破坏、两条并一条，文本最终全达会掩盖此问题——必须靠占用率采样发现）。此时改背压节流（`scripts/probe-oc-paced.ps1`：每块写入后轮询占用率回落到阈值再续），规格表记「消费速率 + 背压阈值 + 长文耗时」。

### P4 · 回车形态验证（5 分钟，B 族必测）

对照「VK 回车事件」vs「vk=0 纯字符 '\r'」各一次（`scripts/probe-key2.ps1`）。B 族预期：字符形态被丢（打完字不提交）；A 族预期：两形态皆可。**统一采用 VK 形态**（跨族安全）。

### P5 · 控制键与方向键（10 分钟）

- esc/tab（审批应答键位场景）：VK 形态验证生效。
- 方向键：A 族用 VT 序列（ESC[A 等）**整条单批原子写**；B 族用 VK 形态——各验证一次历史召回。
- 禁区验证（B 族）：确认裸 ESC 字符流被当按键吃（cancel 风险）→ 规格表记「禁 BP 序列、禁裸 ESC 字符流」。

### P6 · busy 行为（10 分钟，可选但推荐）

目标 turn 运行期间用 `scripts/probe-type.ps1` 每 2s 注 2 字符探针 + `scripts/observe-occ.ps1` 监控占用率：字符入草稿（原生排队）还是被丢弃。结论写进规格表「busy 插队语义」栏。

### P7 · 规格表 + 判定（5 分钟）

按 `references/report-template.md` 产出规格定案表 + 判定：**GO**（全规格通）/ **GO-with-branches**（带按家分支，常态）/ **PARTIAL**（部分长度/宿主受限，注明）/ **NO-GO**（不可注入，注明证据）。归档：兔维斯 项目内入 `docs/research/refs/phase2-消息注入/`，其他项目入用户指定目录。

## 探测纪律（八条铁律，违反则该实验作废重做）

1. 日志追加式带 run-id（`<脚本>-<yyyymmdd-HHmmss>.log`），**永不覆盖**。
2. 每次 WriteConsoleInput 必记 BOOL / 实写数 / 错误码；**仅 ok=false 时读错误码**（ok=true 时 GetLastError 是噪声，可能 87/203）。
3. ok=true 但实写<分片长 = 部分写，从偏移续写，不得直接前进。
4. 统计条件 ≥3 取样（争议裁定/破案场景 ≥5）；逐工具 × 宿主分表，**禁止合并陈述**。
5. 三重证据：日志 + 截图 + 会话文件命中。截图用 PrintWindow 按窗口抓图（`scripts/probe-shot-win.ps1`；锁屏可用）。**WT 标签页例外**：窗口归属 WindowsTerminal 进程，按 PID 抓不到目标标签 → 用 `scripts/probe-shot-wintitle.ps1` 按窗口标题抓取。
6. 一次性子进程执行（附加→写→FreeConsole 复位）；结束 taskkill 清场，不留孤儿进程。
7. 禁区：不碰用户自己的终端/会话；不对非本次探测创建的控制台调 FlushConsoleInputBuffer（会吃掉真实键盘输入）；不经命令行传 `\r` 等转义（bash/PS 均不解释，脚本内置开关）；PowerShell 5.1 构造 ESC 必须用 `[char]27`。
8. **结论不得超过证据**（M6R 评审抓到的典型：没测的格子写了「全部生效」）——每个规格值都要能指到一条日志/截图/会话文件。

## 异常处置

- **写入成功但 TUI 无反应 + 占用率单调累积**：宿主进入文本选择模式冻结（conhost 已实证）→ 向宿主窗口 `PostMessage(WM_KEYDOWN/WM_KEYUP, VK_ESCAPE)` 解冻（`scripts/probe-postmsg.ps1`；Win11 26200 上 conhost 窗口归属 cmd 进程的主窗口句柄，用 `scripts/enum-windows.ps1` 找）。解冻后排队回车可能丢失提交语义——补发一次 VK 回车。
- **占用率 >0 持续 >5s**：判定异常态候选，转恢复流程并记录。
- 其余异常 → `references/methodology.md` 的全量实验清单。

## 边界与转介

- **本技能只管控制台会话**（conhost/WT 宿主里的 TUI）。GUI/APP 类工具（WorkBuddy、zcode 桌面形态、codex APP 等）不走控制台输入缓冲——注入问题域变为 UI 自动化可达性（D7 应急级）或协议通道（app-server/ACP/ZCode Protocol）。那是**另一个工作流**，首例实证后再立技能，勿用本流程硬套。
- DefTerm handoff 宿主（应用直接成为 ConPTY 客户端）无控制台可附加，登记不可达。
- macOS 侧是流水线第二段：Windows 定族规格 → Mac 四点差异验证（回车行为/长消息/审批可达性/环境项），见 `references/mac-verification.md`；族档案的 macOS 投影见 `references/known-families.md` 平台差异节。

## 脚本套件（scripts/，M6R 验证版 + opencode 实测迭代）

来源：兔维斯 M6R 探测（2026-09-18，经独立评审逐行核验）+ opencode 实测（2026-09-19，SQLite 对账器/背压节流 runner/WT 标题截图/WT 定位修复）。用法与依赖见 `scripts/README.md`。核心：`ConIn.ps1`（FFI 基座：附加/CONIN$/写记录/模式/占用率/复位）+ 各实验 runner。缺脚本时按 README 里的接口重写，纪律不变。

## 屏读侧（screen-read）：形态矩阵与四闸门（2026-10-02 起）

注入的镜像问题域：注入回答「怎么打进去」，屏读回答「**读出来是什么、解析器认不认**」。触发场景：①新工具屏读判据定规格；②屏读故障诊断（读得到屏但解析不出 / 误报形态 / 卡片与终端脱钩）；③版本升级后屏读规格复验（与注入复验同批次做）。

确立事故（claude 2.1.278 多题流验收）：单选子题屏无独立 Next/Submit 行 → 解析器整屏 0 行 → 卡片与终端脱钩，且中止文案误报「读不到问答屏」。核心教训：**解析判据的盲区不靠穷举屏形发现，靠闭环捕获**。

**四闸门**（逐字适用于屏读，细节与探针模式见 `references/screen-read-matrix.md`）：

1. **样本门槛**：解析判据改动前必有活体 dump（只读探针，零注入）；禁止按档案手抄夹具。
2. **证据自带失败**：屏读中止区分「读不到屏」vs「屏在但形态不符」，后者回执附屏面摘要——未知形态第一次出现就自带证据。
3. **账本吸收文案漂移**：短锚进 `anchor_ledger`；结构判据留代码（账本 ≠ 整屏 dump ≠ 解析器）。
4. **屏读体检表**：验收前对活会话跑全解析器，输出认识/不认识清单——不允许带盲区上实机。

## 深入阅读（按需）

- `references/known-families.md` —— 两族完整规格、版本漂移教训、按家分支表、平台差异（macOS 投影）（P1 定族后**必读**）
- `references/methodology.md` —— 全量实验 E1–E13 与判据（新族/破案/复验争议时读）
- `references/report-template.md` —— 规格定案表与报告模板（P7 用）
- `references/mac-verification.md` —— macOS 四点差异验证清单与环境处置（流水线第二段）
- `references/screen-read-matrix.md` —— 屏读形态定案表模板、四闸门细则、只读探针模式、三层漂移机制（屏读侧**必读**）
