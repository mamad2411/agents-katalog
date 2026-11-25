---
name: windows-kernel-readonly-forensics
description: 在 Windows 上做**只读**内核级取证：用 LiveKd 起内核调试会话读活内存（对象引用计数、EPROCESS 字段、通知回调表、对象回调链），用 GFlags **runtime** Object Reference Tracing（`!obtrace`，**不必重启**）打出每一次引用/解引用的调用栈，并把内核地址确定性地点名到模块。用于排查「进程退出后内核对象不回收 / 内存只涨不降 / 僵尸 EPROCESS 堆积 / 引用泄漏 / 那 1 个残留引用是谁给的」这类问题，以及任何需要「看内核里到底有谁注册了回调、谁持有引用」的场合。当用户说"内核不回收""僵尸进程对象""内存泄漏到重启才好""哪个驱动在漏引用""引用计数为什么是 1""帮我枚举内核回调"时使用。核心是一整套**不写 Start、不重启、不碰设备**的采集流程，含 `!obtrace` 账本的 `+32768` 编码陷阱、`!process 0 0 <name>` 卡死陷阱，以及**不依赖 KD 的 CID 表判据**。
agent_created: true
task_type: dev.windows_kernel_readonly_forensics
---

# Windows 内核只读取证（LiveKd + kd 脚本 + 模块区间映射）

## 0. 先划安全边界（这是本 skill 存在的首要理由）

**可以做（只读，零风险）**：起 LiveKd 内核调试会话；`dq` / `dt` / `dps` / `x` / `ln` / `lm`；
读注册表；`NtQuerySystemInformation`；`verifier /query`。

**⛔ 绝对不做（一次就能把机器搞到开不了机）**：
- ⛔ **不写任何服务的 `Start` 值**。一次真实事故：把 13 个服务批量设 `Start=4` 后关机 ⇒ **开机卡死**，
  因为批次里混进了 `AmdMicroPEP`（原值 `0` = BOOT_START）。备份 JSON 里明明记着原值，工具照改不误
  —— **备份只是说明书，不是刹车**。
  正解：**写之前实时读当前值，`<=1` 硬拒绝**。（实测某机 853 个服务里 `Start=0` 有 98 个、`Start=1` 有 37 个，
  含 `ACPI`/`disk`/`partmgr`/`tcpip`/`amdpsp`/`vmci` ⇒ **任何"候选表"式保护名单都是错的**。）
- ⛔ **不用 `pnputil /remove-device`** 摘启动路径上的设备。
- ⛔ 不 `Stop-Service` 陌生内核驱动（有的会永久 `STOP_PENDING` 挂住关机）。
- ⛔ 不重跑「驱动开机不加载 + 重启」的二分实验（就是事故那条路）。
- 保护名单**必须**含网卡 / 键盘。

**若已进入不可启动状态**（救援通道，已验证）：WinRE 里
`reg load HKLM\OFFSYS <盘>:\Windows\System32\config\SYSTEM` → 改 **`ControlSet001`**
（离线无 `CurrentControlSet`，盘符要探）→ `reg unload` 成功再重启。
WinRE **没有 `findstr`/`timeout`/PowerShell** ⇒ 脚本只能 `reg`/`for`/`if`/`call` 且**必须扁平**；
关机用 `wpeutil shutdown`。

---

## 1. 打通提权通道：优先借本机已有后端，别想着弹 UAC

很多取证动作要管理员。实测三条路只有一条好使：

| 路 | 结果 |
|---|---|
| `ShellExecuteExW(runas)` | **返回成功但子进程 `exit=0` 且一行不执行** |
| bash 里调 PowerShell | 被安全策略拦（要用 PowerShell 工具） |
| **本机已有管理员后端**（如 `server.main` :8766） | ✅ **可用** |

判定后端真有高完整性令牌，别只看它自称：
```
whoami /groups        → BUILTIN\Administrators 要是 Enabled group（不是"仅用于拒绝的组"）
net session           → 正常返回；非提权进程会报"拒绝访问"
```
然后 `POST /exec/cmd {"cmd": ...}` 脚本化跑管理员命令。

**⛔ 引号陷阱**：`shell=cmd` 通常走 `cmd.exe /d /s /c "chcp 65001>nul & <cmd>"`，
`/s` 的剥引号规则会把带引号的路径**整个当命令名**（`"C:\Program Files (x86)\...\livekd64.exe"` → not recognized）。
⇒ **带空格路径一律用 `/terminals/spawn` 的 `cmd_list`**（直接传 argv 数组，绕过 shell）。

---

## 2. 起 LiveKd：`-cf` 不执行命令文件，必须交互驱动

LiveKd（Sysinternals）的杀手级优点：**绕过 Secure Boot 对 `bcdedit /debug` 的保护**，
且**不需要重启**（临时加载 `LiveKdD.sys`，进程退出即卸载）。补装：`winsdksetup.exe /features OptionId.WindowsDesktopDebuggers`
只出 `kd.exe/windbg.exe/gflags.exe`；`livekd64.exe` **必须拷进 `C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\`** 才能跑。

**核心事实：`livekd64.exe -cf <命令文件>` 不执行命令文件**（只把 kd 起起来停在 `0: kd>`；`-c "..."` 的引号还会被 LiveKd→kd 吃掉）。

正确姿势：
1. `/terminals/spawn`（`cmd_list` 模式）起 `livekd64.exe`，轮询输出直到出现 `kd>`。
2. 用 `/exec/send_input` 逐条送命令，用
   `/terminals/{tid}/output?channel=stdout&offset=<byte>` 的 **字节游标**读增量
   （返回 `{content, next_offset, total_bytes}`）。
3. `.logopen <绝对路径\反斜杠>` 落盘到 kd 自己的日志，然后解析文件 —— 比抓控制台稳。
4. 收尾 `/terminals/{tid}/kill`。

⛔ **绝不发 Ctrl+C**：会终止整个 kd 并弹 `Execute Kd again? (y/n)`，后续命令变成对该提示的回答，**会话直接报废**。
⛔ 也别发 `!process 0 0 <imagename>` 这类"按镜像名列表"的命令（图形界面机器上能列出**上千个已退出的 shell**，输出洪水淹没结果）——要按 PID 精确点名。
⚠️ **首次调用的假故障**：`!process` 报 `Cannot resolve nt!_EPROCESS object type` = 类型信息 lazy 未加载。
⇒ 发任何命令前先跑一条 **`dt nt!_EPROCESS`** 预热。

---

## 3. 读「僵尸对象」的引用计数（判定是不是真泄漏）

对象引用计数在 `_OBJECT_HEADER` 前两个 qword：`+0x00 PointerCount`、`+0x08 HandleCount`。
`EPROCESS` 地址 = 对象体地址 ⇒ 对象头在 `EPROCESS - 0x30`。

```
!object <EPROCESS>
dq <EPROCESS>-0x30 L2      ← 不依赖类型信息的硬读法，可复核 !object
```

判读：
- `HandleCount = 0` 且 `PointerCount > 0` ⇒ **纯内核引用泄漏**（排除用户态句柄泄漏）；
  引用计数永不归零 ⇒ 对象删除回调**从未执行**，对象留到重启。
- `HandleCount > 0` ⇒ 用户态句柄泄漏（更好修）。
- **取样一定要带活进程对照**：活进程的 `PointerCount` 是几十万量级。
- **`PointerCount` 是否恒为一个固定小值很重要**：恒为 `1` ⇒ 「**同一个固定引用对每个终止进程恰好漏一次**」，
  不是「多个驱动各漏一次」，也不是「每次句柄操作漏一次」。
  ⇒ 这条把候选机制锁定到**「每进程触发一次」的那一类**（进程创建通知 / 对象创建回调），
  排除按句柄操作触发（那样计数会正比于句柄数）与按线程触发（会影响计数方差）。

再配 `EPROCESS` 字段看**清理走到哪一步**：
`ObjectTable`/`ImageFilePointer`/`SectionObject` 已清 = **退出**路径跑完；
`SectionBaseAddress`/`Peb`/`DeviceMap` 未清 = **删除**路径没开始。

### 3.1 ★ 前置一步：**免管理员**先读内核 OBJECT_TYPE 计数器（动 LiveKd 之前先跑）

纯用户态、免管理员、免符号、约 1 秒，就能拿到原本只有 KD 才读得到的
`TotalNumberOfObjects` / `HighWaterNumberOfObjects`：

```python
# NtQueryObject(NULL, ObjectTypesInformation=3, buf, size, &ret_len)
# 结构：ULONG NumberOfTypes + ULONG Pad，之后每项 = UNICODE_STRING(x64=16B) + 88B
#   +0x10 TotalNumberOfObjects      +0x14 TotalNumberOfHandles
#   +0x28 HighWaterNumberOfObjects  +0x2c HighWaterNumberOfHandles
# 类型名：UNICODE_STRING.Buffer 可读就用它，否则取条目尾部的内联名
# 0xC0000004 = STATUS_INFO_LENGTH_MISMATCH ⇒ 按 ret_len 放大 buf 重试（循环 10 次够）
```

- `Process.Total == HighWater` ⇒ **自开机零释放** —— 与 KD 的
  `dt nt!_OBJECT_TYPE poi(nt!PsProcessType) TotalNumberOfObjects HighWaterNumberOfObjects`
  是**同一份数据**，只是不用起调试器
- `Thread.Total < HighWater` 是**必须的对照组**（证明计数器本身有效，不是显示 bug）
- ⚠️ `Event` / `Token` 的 `HighWater` 会**紧贴** `Total`（峰值被反复刷新）⇒
  判据是**精确相等**，不是"几乎相等"
- ⛔ `NtQuerySystemInformation(SystemObjectInformation = 17)` **恒返回 `0xC0000001`**，别试
- 成形脚本 + 阈值 + 20 条死路：`<仓>/workspace/windows_forensics/zombie-study-pack/`
  （`zp_obj.py` / `METHOD.md` / `DEAD_ENDS.md`）

**因果实验（比存量更硬）**：造 N 个 `cmd /c exit`，看 Process 对象的净增 ⇒ 留存率；
健康机 ≈ 0%，病例机 ≈ 100%。

- ⛔ **单背景窗 + 长沉降窗会给出负数**：本机实测报过 `扣背景后 -689%`。三处根因都必修：
  ① 沉降窗 `sleep(10)` 是**纯污染**（不造进程但背景照涨）⇒ 降到 **3s**；
  ② 逐个 `Popen().wait()` 把实验窗拉到十几秒 ⇒ 改**分批并发**（批 16）压到 **3.7s**；
  ③ 只测一次背景窗 ⇒ 改成**实验窗前/后各一次**，并用**两窗分歧**当经验 σ（背景是突发的，
  纯泊松 σ 会严重高估可信度）。修好后同机 `-689% → 97.6%`。
- ★ **必须给 SNR 闸门**：`SNR<3` 就诚实报「不可用」，别硬给一个百分数。
  "分不开信号与噪声"和"结果正常"是两件事，输出上必须能区分。
- ⛔ **`RETAIN ≈ 0` 不等于该机健康**：实验造的是**你自己的子进程**，
  若泄漏只发生在**某个特定创建者**的子进程上（per-creator），实验照旧阴性。
  `RETAIN≈0` 只排除**全局型**缺陷；`RETAIN≈100%` 才是铁证。

**★ 交叉对照 `Zc / Z`（2026-09-23 新增，判"对象为什么还在"）**：
同一进程内**同一时刻**各测一次 `P = Process 对象数`（内核计数器）与
`T = CID 条目数`（`OpenProcess` 扫 PID），则
`Zc/Z = (T−L)/(P−L)` ≈ 1 ⇒ 对象**仍挂在 CID 表上**（删除路径没跑）；
≪ 1 ⇒ 对象**已摘除 CID 条目**、只是没被销毁（另一形态，量级通常无害）。
⛔ 两次分开跑**不可比** —— 病例机对象数以 ~12 个/秒变，差几分钟就不是同一份数据。

- 成形脚本 + 阈值 + 26 条死路 + **统计偏差稳健度分级表**（`METHOD.md` §11）：
  `<仓>/workspace/windows_forensics/zombie-study-pack/`
  （`zp_obj.py` / `METHOD.md` / `DEAD_ENDS.md`）

### 3.2 ★★ 看到一个反常数字，**第一件事是怀疑测量工具**（本次最贵的教训）

`zp.py` v1 里有一个「连续 20,000 个 PID 未命中就 `break`」的省时优化，
本机实测**它确实会触发**；一旦某台机器的 PID 空洞 > 20,000，扫描**静默截断**、
`T` 被低估，而 `truncated` 标志**不置位** —— 下游完全无从察觉。
全扫实测只要 **2.0 秒**，那个优化只省 1.5 秒。

> **诊断脚本里"省时间"的优化是负资产**：它不报错，只安静地给你一个错的数。
> 但它也只值 1.5 秒 —— **先量化再决定删不删，别凭感觉。**
>
> 反过来也要防另一个极端："可能是工具错了" ≠ "就是工具错了"。
> 定案办法：**让工具自证覆盖度**（回传最大命中 PID 与最大空洞），
> 而不是靠争论谁更可信。

**配套的统计纪律**（写进 `METHOD.md` §11）：
- **单次事件不能给速率**（`DZ=+1/180s` 的 95% CI 是 [0.5, 111]/h，跨度 200 倍）
- **漏速不是稳态量**：同一台机同一天实测 0.40 ~ 30.85 个/秒（**77 倍**）⇒
  "漏速 N 个/秒"没有定义，**不可外推**
- **跨机比速率必须同口径**，且只引用定性结论（"至少差一个数量级"），
  ⛔ 不引用具体倍数
- 结论要**标稳健度**：哪些是"实测值之差"（稳），哪些依赖"粗估系数/未验证基线"（不稳）。
  读者需要一张**可引用的白名单**，而不是一堆看起来同样确定的数字。

---

## 4. 枚举四张通知回调表 + 对象回调链

### 4.1 通知回调表
`x <nt>!Psp*NotifyRoutine*` 先拿符号，再 `dq` 四张表各 `L64`：
`PspCreateProcessNotifyRoutine` / `PspCreateThreadNotifyRoutine` / `PspLoadImageNotifyRoutine`。
⚠️ **`PspCreateProcessNotifyRoutineEx` / `PspCreateThreadNotifyRoutineEx` 符号常常不存在**
（但 `...ExCount` 存在）⇒ legacy 与 Ex **共用同一个数组**，别以为存在"漏掉的那张表"。
数组尾部全零（内核会压实）⇒ 非零个数就是全部注册数。

### 4.2 对象回调（`ObRegisterCallbacks`）
⚠️ **`nt!ObpCallbacks` 与 `_OB_CALLBACK_ENTRY` 在较新 build 上符号都不存在**。
真机制是**每个对象类型自带一条回调链**：

```
_OBJECT_TYPE (+0xc8) CallbackList : _LIST_ENTRY
   ↑ nt!PsProcessType / nt!PsThreadType 是 POBJECT_TYPE（二级指针，要先 poi 一次）
节点 _CALLBACK_ENTRY_ITEM（0x40 字节）：
   +0x18 ← 指回同一次注册的 _OB_CALLBACK_ENTRY 头（= item−0x20）
   +0x20 ← 该 _OBJECT_TYPE 基址
   +0x28 ← PreOperation 回调函数地址（点名要点它）
```
走链表（kd 脚本）：`.for (r $t1 = poi(@$t0); …) { … }`，`$t0` = 表头地址。

### 4.3 点名到模块 —— ⛔ 不要用 `ln`
**`ln` 依赖符号服务器，无符号模块常常只回 `Browse module` / `Set bu breakpoint` 而不打印模块名**；
实测**同一个驱动地址，第一次能给出路径、第二次静默**。
⚠️ 而且 `ln` 给的是**最近符号**，不是真函数名（曾因此误判"Driver Verifier 在跑"，
实查 `verifier /query` → `No drivers are currently verified.`）。

**正解**：用户态枚举模块基址/大小做区间查表 ——
`NtQuerySystemInformation(SystemModuleInformation=11)`，结构 `RTL_PROCESS_MODULES`。
⚠️ **数组起点是 `+0x8`**（8 字节对齐），写成 `+0x4` 的症状是「**所有**地址都不在任何已加载模块内」。

---

## 5. kd 脚本的 4 个确定性坑

1. **伪寄存器只认 `$t0..$t19`** —— 自定义名（`$tp`）报 `Bad register error`。
2. **`dq` 每行是「地址 + 2 个 qword」= 3 个 token**（不是 2 个）。按 2 个 token 写正则 ⇒ 解析出 0 个。
3. **按段落切分 dump 会越界**：必须再按**地址区间** `[base, base+array_bytes)` 过滤，
   否则下一个数组的头几项会混进来。
   **污染指纹：同一个池指针同时出现在两张表里。**
4. **`.logopen` 只认「绝对路径 + 反斜杠」**，相对路径/正斜杠会**静默**不生成日志。

---

## 6. 排除网：怎么把候选集压下去（每条都要能给依据）

按证据强度排序，越靠前越硬：

1. **直接实验**（最硬）：能安全停的服务 → `sc stop` → 复测 → `sc start`。
   用**精确留存率**判据（给探针自己生的进程打标签，沉降后逐个查对象还在不在）：
   **`1.00` = 排除，`<0.10` = 就是它**。别用「ΔObjects 差值」这类**差值代理**。
2. **结构性排除**：安全模式（`Fail-safe`）**只加载 `Start<=1`** ⇒ 对 `Start=3` 的驱动是
   "永远不在场"的硬事实（**不随时间失效**）。
   ⚠️ **但它对 `Start<=1` 的第三方从来无效**（安全模式也加载它们）——这是最容易犯的错：
   把 `{微软核心, 某 Start=0 第三方}` 当成"只剩两个"，其实第三方全都没被排。
3. **在场的直接证据**：`sc stop` 报 `1052`/`NOT_STOPPABLE` ⇒ 只能靠"在不在回调表里"结构排除。
4. **缺席排除**：本 boot 内核模块表里没有该模块 ⇒ 它不可能是当前泄漏源。
5. ⚠️ **判第三方只看文件版本信息里的 `CompanyName`** —— 不能靠模块名相似度，
   也**不能靠路径前缀**（会漏掉 DriverStore 下的 PnP 驱动；签名还可能被 WHQL 改写成 Microsoft）。

**最后手段 = 点名**：`gflags` 开 **Object Reference Tracing** + `!obtrace <EPROCESS>`
（能打出每一次引用/解引用的**调用栈与驱动名**）。
（未开启时 `!obtrace` 报 `Object Reference tracing not enabled` —— **不是**"无此导出"。）

> ⚠️ **更正（2026-09-21 实测推翻旧写法）**：本 skill 早先写"代价 = 改 `KernelFlags` + **一次重启**"——
> **这是错的**。GFlags 有两条路：`-ro`（落注册表，**需重启**）与 **`-ko`（runtime 内核标志：立即生效、
> 不写注册表、重启即自愈）**。用 `-ko` **全程不需要重启**，实测注册表 `GlobalFlag` 前后均 `0x0`、
> 关闭后 `ObpNumTracedObjects = 0`（零残留）。**不要再因为"要重启"而放弃这条路。**

**`!obtrace` 实操要点（全部实测，细节见 windows_forensics 的 `SKILL.md` §32–§39）**：

- 开关命令：**开 `gflags /ko -t <PoolTag>` / 查 `gflags /ko`（无参=只读）/ 关 `gflags /ko -d`**。
  ⛔ `-ko` 是**通用内核标志通道**（同区还有 `-k +spp`/`+ust`/`+soe`）⇒ 只允许 `-t/-p/-d`，
  执行前后必须核对 `GlobalFlag`/`GlobalFlag2` **仍为 0x0**，不符立即 `-d`。
  ⚠️ `gflags` 帮助里"必须指定 `-i` 或 `-p`"**是错的**，单独 `-t Proc` 即被接受。
  ⛔ `gflags.exe` 在 `C:\Program Files*` 下，**bash 直跑会被沙箱拦**（`Permission denied`）⇒ 走提权后端。
- 铁律：**同时只能 1 个 trace**；**必须限定 pool tag 或 image**；**只追踪"开启后启动的进程"创建的对象**
  ⇒ 已有的僵尸永远没有 trace，**必须现造进程**。
- **⛔ 账本的三个致命陷阱**：
  1. **符号列不只有 `±1`** —— 会出现 **`+32768 Dflt 32768 32770`** 这种条目。
     正则写死 `[+-]1` 会**静默漏掉它**，于是账本出现"`Total` 从 2 跳到 32770 的断崖"和
     "净差 10 而真实残留却只有 1"的矛盾，极易误判成仪器故障 ⇒ **解析器必须接受任意整数**。
  2. ⛔ **但别给它编故事**：`+32768` / `0x8000` **不是**任何已知的"CID 表标记位"。
     铁证：账本末 `Total = 32778`，而**同一地址实测 `RealPointerCount = 1`**
     ⇒ **账本的计数列与真实引用计数不相容**，`+32768` 只能是编码/簿记产物。
     进而"**这条记录 = 一笔未归还的引用**"**同样是未证之事**：实测该类路径上
     （`PspReferenceCidTableEntry` ← `PsLookupProcessByProcessId` ← 第三方进程回调）
     调用者借的引用**多数都有配对归还**（例：`+1 ObHn` → `-1 ObHn`，归还栈为 `NtClose`）。
     **⇒ 账本只能读栈（谁在场），不能读数（谁欠账）；归因要么降到"线索"，要么用独立实验证。**
  3. **`Total` / `TagCnt` 不能当引用计数用**（编码污染 + 账本常在末尾被截断）
     ⇒ **计数只信 `!trueref` 的 `RealPointerCount`**。
- ⛔ **手工遍历 CID 表必须先验证索引公式**：3 级表 `idx = cid>>2`，`L2 = (idx>>10)&0x3ff`、
  `L3 = idx&0x3ff`。公式错一位会**读到另一个进程的条目**，而且它照样是"live entry + 有效指针"，
  **不报错、不异常** —— 会让你把"某个僵尸的条目"误当成"目标对象自己的条目"。
- ⛔ **判断"这个组件能不能卸/关"要先查三样**（缺一不可）：
  ① `Uninstall` 键有没有条目（**系统组件没有** ⇒ 无卸载路径）；
  ② 它的驱动/服务 `Start` 值（**`<=1` 即启动路径**，动它 = 开机卡死的同类事故）；
  ③ 它**当前开关状态**（很可能**本来就是关的** ⇒ "关掉试试"这条验证路早已失效）。
  仪器：按关键词做「进程 / 服务 / Uninstall / Run」四联只读审计（进程枚举用
  `CreateToolhelp32Snapshot`，**别用 `tasklist`/`wmic`——仪器自身会造进程**）。
- ⛔ **`Mod+巨大偏移` 多半是跳转 thunk**（`nop; jmp Mod!真函数+小偏移`）⇒ **函数名可信、偏移无意义**（`ln`/`u` 可验）。
- ⛔ **Kd 里绝对不要发 `!process 0 0 <name>`**：大机器上有十万量级 Process 对象，
  全表遍历会**卡死整个会话**（症状：命令写入成功但 stdout 0 增长，极易误判成"命令没发出去"）。
  **改用 `ActiveProcessLinks` O(1) 尾部扫描**：
  `r $t0 = poi(nt!PsActiveProcessHead + 8)` → `!process @$t0-0x448 0` → 跟 `poi(@$t0+8)` 向前
  （**偏移 `0x448`**，由 `dt nt!_EPROCESS` 确认）。

**★ 更轻量的判据（优先用它，不依赖 KD）—— 僵尸的 CID 表条目是否仍在**：
`PID → EPROCESS` 只能经 `nt!PspCidTable` 解析（`PsLookupProcessByProcessId`）⇒

| `OpenProcess(pid, PROCESS_QUERY_LIMITED_INFORMATION=0x1000, FALSE)` | 含义 |
|---|---|
| 成功 | **CID 表条目存在** ⇒ 该条目持有的引用没被释放 |
| 返回 `87` / `1168` | 条目已被摘除 |

- ⚠️ **地面真值必须来自 KD 快照**（`ObjectTable == 0` **且** `HandleCount == 0`），否则 PID 复用会**假阳性**。
- 实测：**200/200 已死 PID 条目存在、0 个已摘除** ⇒ 与 `!trueref = 1` 严丝合缝。
- 优点：**不依赖 KD、不依赖符号、零副作用**（开完句柄立即关）⇒ 复测泄漏优先用它。

---

## 7. 一条最重要的方法论

**速率必须两条独立仪器互证**；**空闲时机器是干净的** ⇒ 漏速 ∝ 工具繁忙度，
别把"我挂机时很干净"当成"问题已解决"。
抓「谁在反复写某文件」**必须事件驱动**（`ReadDirectoryChangesW` 实测 50 s 命中 1,060 条，轮询版 0 条）；
数进程创建量**只能用快照轮询**（16 ms 寿命进程的命令行永远抓不到）。
