---
name: memory-hygiene-two-layer
description: 压缩被注入的长期记忆并维持「全局只放跨项目、项目只放铁律+指针、长细节下沉 TOPIC」的两层结构。当用户说「把记忆压缩一下」「记忆太长了 / 被截断了」「这条不该在全局记忆里」「整理记忆」，或发现注入的记忆结尾被硬截断（出现 "… (memory truncated)"）时使用。含**注入上限实际按字符数计**（全局 4000 / 项目 8000）的实测判据与完整动作顺序。
agent_created: true
task_type: daily.memory_hygiene_two_layer
---

# 记忆两层压缩（全局 / 项目）

## 0. 先量，别猜：注入上限按**字符**计

- 全局**注入层**：上限 **≈4000 字符**。WorkBuddy 实测注入的那份是
  `~/.workbuddy/user-<account-id>-personal/MEMORY.md`（2026-10-14 实测 2368 字符）。
  ⚠ **家目录下另有一份 `~/.workbuddy/MEMORY.md`（实测 4443 字符、内容含旧路径）——它不是本会话被注入的那一份**
  ⇒ 判据只有一条：**把注入到上下文的正文与磁盘文件逐字比对**，别按路径假设。按错文件"压缩"= 白干，且真源一字未动。
- 项目**注入层** `<repo>/.workbuddy/memory/MEMORY.md`：上限 **≈8000 字符**
- （这两个数是 harness 注入通道的上限；它们是**投影**，真源位置见 §1）
- ⛔ 用字节当判据必误判：中文 **3 字节/字**，所以「8000 字符」约等于十几 KB 的文件；旧文档里写「上限 10 KB / 13 KB」就是这么错的。
- **实测真实上限的办法**：把注入到上下文的那段内容（"... (memory truncated)" 之前）**最后一句**当锚点，在原文件里定位，得到的字符偏移就是上限：

```python
t = open(p, 'rb').read().decode('utf-8')
print(len(t), 'chars /', len(t.encode()), 'bytes')   # 当前体积
print(t.find('注入内容末尾的那句'), '<- 约等于上限')
```

## 1. 三层结构（动手前先给每条信息定位置）

⛔ **2026-10-14 起「真源出 harness 私有目录」**：`~/.workbuddy/MEMORY.md` 与 `<repo>/.workbuddy/memory/MEMORY.md`
只是 **harness 注入进来的投影**；真源（日志 / 专题 / 台账）统一放**跨 harness 共享空间** `.agents/memory/`。
换 harness 就没人读 `.workbuddy/` ⇒ 真源写那里 = 失忆 + 换机丢失。

| 层 | 位置 | 只放 |
|---|---|---|
| **L2 常驻**（注入投影，最贵） | 全局 `~/.workbuddy/MEMORY.md`（≈4000 字符）／项目 `<repo>/.workbuddy/memory/MEMORY.md`（≈8000 字符） | 带代价的红线 / 不可推导的环境事实 / 高频经验 / **指向 L1 的指针**（不复制正文） |
| **L1 检索**（真源，入库） | 全局 `~/.agents/memory/`（`README.md` / `TOPIC_*.md`）；项目 `<repo>/.agents/memory/`（`README.md` / `TOPIC_*.md` / `machine/`） | 领域细节、本机台账、结论档案——**按需 Read**，不进注入、不受字符上限约束 |
| **L0 事件流** | 项目 `<repo>/.agents/memory/YYYY-MM-DD.md` | 流水账，append-only，不入注入也不入库 |

归属判据：**换个项目还用得上吗？** 用得上 → 全局；只对这个仓库成立 → 项目。只解释一次性的来龙去脉 → L0 / TOPIC。

⛔ **冲突优先级**：注入的 `MEMORY.md` 与目标项目 `AGENTS.md` / `docs/` 冲突时，**一律以项目规定为准**
（注入无法阻止、只是投影、可能滞后）。典型冲突：注入的 reminder 仍写「日志落 `.workbuddy/memory/`」——那是**旧路径**。

**升 L2 准入四问**（任一答否不许升）：① 不可推导？② 会重复发生？③ 零上下文会踩？④ 有消费场景？
**置换纪律**：两份注入文件都卡在硬上限 ⇒ 新条目进 L2 必须报**挤掉了谁**，被挤的**降级回 L1 不删除**。

## 2. 动作顺序（每次照做）

1. **先备份** `cp` 到 `<memory>/_backup/<YYYYMMDD>-compress/`，再动原文。
2. **移**：全局里出现的项目专属路径 / 脚本 / 约定 → 改写成通用说法（「该项目 venv 的 python」这种），具体值下沉到该项目记忆或对应 skill。⛔ 直接删 = 丢信息，不算压缩。
3. **反向查重（项目 → 全局）**：项目 MEMORY.md 里凡是**跨项目内容**（git 自装、PowerShell/heredoc 怪癖、回收站红线、C 盘桌面路径…）都要删掉改指全局 —— 全局已有 = 纯重复，删它零信息损失，是提升压缩比最快的一刀。
4. **下沉**：项目注入层里已成段落的细节 → 剪进 `<repo>/.agents/memory/TOPIC_<主题>.md`（真源、入库）；注入层只留「一句话铁律 + 一行指针」。指针要写明 TOPIC 文件名与章节。**优先下沉**篇幅最大且最"只解释一次"的块（下游台账、性能实测、事故复盘）。⚠ 落点迁移期：旧 `TOPIC_*.md` 可能还在 `.workbuddy/memory/`，要顺手迁到 `.agents/memory/`。
5. **量化验收**：目标 全局 ≤3800 字符、项目 ≤5000 字符（留 35%+ 余量；至少不低于 15%）。用上面 python 片段核对，⛔ 别拿 `ls -l` 的字节数下结论。
6. **验不丢信息**：从原文抽 30 个左右"锚点"（wxid / commit 号 / 函数名 / 坑号 / 常量），在「MEMORY + 各 TOPIC」拼起来的全文里逐个 `in` 检查，输出缺失清单，**必须为空**才算完成。
7. **改文件头**：把上限写成**字符**表述，并把本次压到的体积记进去（下次才知道该压到多少）。
8. 在项目 `<repo>/.agents/memory/YYYY-MM-DD.md` 追加一条流水账（append-only；⛔ 不写 `.workbuddy/memory/`——那是旧路径）。

> ⛔ **不要动没读过的项目记忆就删东西**：别的项目没有当前会话的上下文，必须先完整 Read 该文件，
> 才能判断哪块是"项目专属细节"、哪块是"跨项目重复"。只按体积排名就动手 = 高风险。

## 3. 坑

- **`glob.glob('F:/a/*/b')` 在 Windows 上返回的路径可能带反斜杠** ⇒ 用 `p.split('/')[N]` 取项目名会 `IndexError`。
  一律用 `os.path.basename/os.path.dirname` 取分量。
- **bash heredoc 里写 Windows 反斜杠路径会被 JSON 层吃掉一层** ⇒ Python 报 `truncated \UXXXXXXXX escape`。正解：正文用 Write 工具落盘，再 `python` 读入该文件后 `open(log,'ab').write(...)` 追加，正文里干脆不出现反斜杠字符。
- 追加日志前探行尾：`eol = "\r\n" if raw[-400:].count(b"\r\n") else "\n"`（本项目多文件混排行尾）。
- **改写后核对行尾风格与原文一致**（用 `_backup` 里的 .bak 对比块：本项目正文是**纯 LF**，别被系统 `core.autocrlf=true` 带成 CRLF）。
- 同一文件多次 Edit **不能并行发**。
- 顺手体检所有项目：`ls -d /f/project_temp/*/.agents/memory /f/project_temp/*/.workbuddy/memory`，逐个量字符数，
  超 8000（项目）/ 4000（全局）的会静默截断。**迁移期两处并存**：`.agents/memory/` 是真源、`.workbuddy/memory/` 里
  历史日志作归档（未迁的 harness 仍可能往旧路径写）。
- 日流水账**不需要压缩**（不进注入），别去动；按维护规则只蒸馏 30 天前的旧日志。

## 4. 项目体检台账（2026-10-01 快照）

> ⚠ **本节是历史快照，落点仍按当时的 `.workbuddy/memory/` 记**。2026-10-14 共享空间落地后真源已迁 `.agents/memory/`
> （见 §1）；同日 `Parcae` 已按项目规矩重做一轮（7996 → 7815 → 6981 字符，分区配额 + 强制置换）。
> 另：本节提到的下沉目标 skill `web-query-debug-methods` **已不再作为用户级 skill**，内容并入项目
> `docs/environment-constraints.md`（「网络与环境查询技巧」章）。

| 项目 | 字符数 | 状态 |
|---|---|---|
| **全局 `~/.workbuddy/MEMORY.md`** | **3393**（原 4136，注入端已截断） | 四次压缩：「网络与查询技巧 / 通用方法论」下沉 skill `web-query-debug-methods`；收编项目跨项目怪癖（PS 四坑 / bash 反引号 / text=True）。余量 15.2% |
| `Parcae` | **5919**（原 7994，贴死上限） | 四次压缩，余量 26%；patchright 细节 → `TOPIC_backend.md` §十一、磁盘 I/O 审计 → `TOPIC_disk.md` 新章节 |
| `wechatDecode` | 4902 | 2026-09-23 已压缩 |
| `角色卡研究` | 565 | ok |

- 无 MEMORY.md（只有日志，无需处理）：`Future` / `WechatBot` / `WechatBot-private-bundle` / `x`。

- **2026-09-23 二次压缩**：全局 3731→3475、Parcae 6112→5813（均为**字符**）。起因是一轮误报：把**字节数**当成字符数读（Parcae 6112 字符 = 9328 字节 ≈ 9.1 KB），又误取了 `_backup` 里旧版快照的体积（12984 字节）当成当前值 ⇒ 得出「超限 12.98 KB、尾部被截断」的错误结论。**判据只用 `len(text)`（字符数），别看文件大小。**

- **2026-10-01 三/四次压缩**：全局 3478→4136（中途回升后又压）→3393；Parcae 5813→7994（回升贴死 8000）→5919。本轮新增经验：① **注入端截断是全局超限的直接证据**（尾部指针段只剩半句 ⇒ 定位丢失风险最高的段落）；② 锚点核验要**先对照备份确认锚点真实性**（本轮 `ConPTY` 是核验者自己加的假锚点，原文件本就没有）；③ 下沉目标 skill 可以自建方法论型 skill（如 `web-query-debug-methods`）承接「跨项目查询/调试技巧」这类无项目归属的内容。

