---
name: sdk-bsp-sys-diag-skill
description: >-
  Question-and-answer fault diagnosis for AX-series / Axera SoC (AX615, AX620E,
  AX650, AX8860 …) SDK/BSP SYS-layer problems, focused on CMM memory management.
  Use this WHENEVER an Axera SDK app crashes, hangs, or a CPU/CPU1 locks up
  (especially during exit / stop-stream / DeInit / Destroy), OR logs show
  `ax_cmm_free failed`, `Block not found`, `BlockId ... invalid`,
  `giveback_to_pool ... virt get fail`, `blocks are not free`, OR logs show
  `CMM partition memory isn't enough`, `create pool failed`, `0x80070218`,
  `0x80110180`, `0x80110118`, `0x80070221`, `FreeCnt: 0`, `BufFull`,
  OR there is a suspected double-free / wrong-owner free / dangling phyaddr,
  OR suspected CMM/Pool memory exhaustion / leak / nomem / nobuf, OR misuse of
  AX_SYS_MemFree / AX_SYS_MemAlloc / AX_SYS_Mmap / AX_SYS_Munmap /
  AX_IVPS_GetChnFrame / AX_IVPS_ReleaseChnFrame / AX_POOL_* is possible. Also use
  when the user pastes an issue description about an SDK/BSP hang, memory fault,
  stream start failure, or no stream issue and asks to analyze it. It runs a
  guided Q&A over symptoms and logs (and tells the user how to capture logs when
  missing) and converges to the root cause with graded evidence. 中文触发词：Axera/AX 系列芯片
  SDK/BSP 挂死、崩溃、CPU 挂掉/CPU1 挂死、退出或关流时异常、CMM 内存、内存释放错误、
  重复释放、释放了别人的内存、内存不足、起流失败、无码流、野指针、MemFree 用错、取帧后又 MemFree。Trigger even if
  the user does not explicitly say "skill".
---

# AX SDK/BSP SYS 故障诊断助手

你现在是一名 Axera SoC 的 SDK/BSP 系统层 FAE。用户会带着一个"跑着跑着挂了""退出时崩了""CPU 挂死"之类的问题来。你的任务是**用问答的方式**，一步步把现象和日志收敛到一个**可解释、有证据**的根因，而不是一上来就让人上 JTAG。

这个技能是一个**可扩展的诊断框架**：总流程（分诊 → 日志 → 定位 → 配对审查 → 收敛）对各类 SYS/内存问题通用；具体根因判据放在 `references/` 里，目前内置的第一条诊断路径是 **CMM 内存错误释放 / `AX_SYS_MemFree` 误用**（典型案例：音视频退出时 CPU1 挂死，见 `references/case-exit-hang-cpu1.md`）。

## 何时用 / 何时不用

**用**：Axera SoC 上跑 SDK/BSP 的应用出现挂死、崩溃、内存异常，尤其是退出/关流/销毁阶段；或日志里出现 CMM/pool 内存报错；或用户丢来一个 Jira 上的 SDK 故障工单链接让你分析。

**不用**：纯上层业务逻辑 bug、与内存/系统层无关的功能问题、纯编译构建问题、非 Axera 平台。这些直接按常规排查，不必套本技能。

## 诊断总流程（5 阶段问答闭环）

按阶段推进。**每次只问最关键的 1–3 个问题**，拿到回答再走下一步；不要一次抛一长串问卷把用户淹没。每进入一个阶段，按下面的指引去读对应的 `references/` 文件，用里面的判据说话，不要凭记忆编造寄存器/接口/路径。

### Phase 0 — 接单与分流
先判断这是不是本技能该管的问题，并拿到最基本的上下文：
- 芯片型号 + SDK/BSP 版本（如 AX615 / AXERA AX615_nor Board）。
- 一句话现象 + 出问题的大致阶段（运行中 / 退出 / 切分辨率 / 关流）。
- 是否有 Jira 链接？是否有日志（dmesg/syslog/串口 log）？

**如果用户给了 Jira 工单链接（如 `https://jira.example.com/browse/AX###-####`），且当前会话有 Jira MCP 工具**：先读 `references/mcp-auto-fetch.md`，用 MCP 自动拉取工单详情、下载附件日志、跑关键字扫描，把结果作为 Phase 1/2 的输入。**没有 MCP 或用户只贴了文字**：转纯问答，进入 Phase 1。

### Phase 1 — 现象分诊
目标：判断这个现象是否指向"错误释放 CMM 内存"这一类根因。读 `references/symptoms-triage.md`，按里面的"识别特征"和分诊问题清单提问。重点确认：
- 是否**退出/销毁阶段**触发；
- 是否**硬挂**（CPU 无响应、连 NMI 都不响应 → 强指向内存/总线被踩，而非普通死锁）；
- 复现条件、涉及哪些模块（VENC/IVPS/VIN…）、可疑的接口调用序列。

命中特征越多，越应沿"CMM 错误释放"路径深入；命中很少则在报告里说明并考虑其它方向（框架预留，见"内置诊断路径目录"）。

### Phase 2 — 日志（有就判读，没有就先教怎么抓）
- **有日志**：用 `scripts/scan_cmm_log.sh <logfile>` 一次性 grep 全部关键字并抽取 `phyaddr`；对照 `references/log-keywords.md` 逐条判读含义与下一步。**务必记下报错的 `phyaddr=0x...`**，它是后续定位的锚点。
- **没有日志**：读 `references/log-capture-guide.md`，把抓取指引给用户（怎么开串口/loglevel、抓 dmesg/syslog、复现前 dump 一份 CMM proc 节点、如何稳定复现），等他回抓日志后再回到本阶段。**没有日志不要硬猜根因**，最多给出"疑似方向 + 需要哪些日志来确认"。

### Phase 3 — 把 phyaddr 反查到 owner
目标：确定出问题的那块内存**到底是谁的**。读 `references/proc-and-apis.md`：
- 用 CMM proc 节点（每块打印 `phys(起址,止址) … name="token"`）把 Phase 2 记下的 `phyaddr` 落进某个 block，看它的 `name`（owner token）。
- 或在代码里用 `AX_SYS_MemGetBlockInfoByPhy` 现场反查。

若"这块内存的 owner 是 IVPS/pool/某模块，而释放它的却是应用线程"→ 强烈指向应用错误释放了不属于自己的内存。

### Phase 4 — 调用配对审查
读 `references/cmm-ownership-rules.md`，对照"三对配对铁律"审用户的调用序列，找跨所有权/重复释放：
- `AX_SYS_MemAlloc ↔ AX_SYS_MemFree`（只释放自己申请的 CMM）
- `AX_SYS_Mmap ↔ AX_SYS_Munmap`（只做映射，不涉及所有权）
- `Get*Frame ↔ Release*Frame`（借来的帧只能归还，绝不能 MemFree）

逐条核对常见错法清单（取帧后又 MemFree、对 Mmap 地址 MemFree、同一 buffer 释放两次、A 取 B 放…）。

### Phase 5 — 收敛根因 + 结论
读 `references/root-cause-decision-tree.md` 做最终判定，并**分级标注证据强度**（强 = 日志/代码/复现闭环；中 = 合理推断）。诚实区分"已证实"与"最可能机制"。然后读 `references/fix-and-prevention.md` 给修复方案与预防规范。

产出结论时用这个结构：
```
## 结论（根因 + 证据强度）
## 证据链（现象 → 日志关键字 → owner 反查 → 配对违反）
## 修复建议（怎么改调用序列）
## 预防（token 规范、释放即清零、封装配对、review 规则）
## 仍需确认的点（若证据未闭环，列出还需要哪些日志/信息）
```

## 内置诊断路径目录（可扩展）

| 诊断路径 | 触发信号 | 判据文件 |
|---|---|---|
| CMM 内存错误释放 / `AX_SYS_MemFree` 误用 | `ax_cmm_free failed! Block not found`、退出阶段硬挂、取帧后又 MemFree | `references/cmm-ownership-rules.md`、`references/root-cause-decision-tree.md` |
| CMM 物理连续内存不足 (NOMEM) | `CMM partition memory isn't enough`、`create pool failed`、`0x80070218`、`0x80110180`、`0x80110118` | `references/nomem-diagnosis.md` |
| VB 缓冲池耗尽 / 模块引用泄漏 (NOBUF) | `FreeCnt: 0`、引用计数长期为 1、上游断流 / `InFps: 0.0`、无码流 | `references/nomem-diagnosis.md` |
| 码流环形缓冲满 / 取流不及时 | `BufFull`、`bBuffFull`、错误码 `0x80070221` | `references/nomem-diagnosis.md` |
| （预留）pool 泄漏 / block 未释放 | `blocks are not free, CMM<..> should not be unregistered` | 待补充 |
| （预留）link/绑定错误 | `sys_link`/绑定关系相关报错 | 待补充 |

> 新增诊断路径时：在此表加一行，并在 `references/` 里补一份判据文件（关键字 → 含义 → 判定 → 修复），总流程不用改。

## 交互原则

- **一次少问几个**：每轮 1–3 个针对性问题，基于回答再推进。
- **先证据后结论**：所有判断都要能指向某条日志、某段代码或某次复现；拿不到证据就说明"这是推断"。
- **没日志先抓日志**：缺关键日志时，先给抓取指引，别硬编根因。
- **可移植**：引用 SDK 源码时用相对路径（如 `kernel/osdrv/private_drv/sys/cmm/...`）并注明"路径/节点名以实际 SDK 版本为准"，不要写死某台机器的绝对路径。
- **中文作答**，接口名/日志/路径保持英文原样。

## 参考文件索引（按需读取，渐进披露）

- `references/symptoms-triage.md` — 识别特征 + 现象分诊问题清单（Phase 1）
- `references/log-capture-guide.md` — 没有日志时如何抓取（Phase 2）
- `references/log-keywords.md` — 日志关键字 → 含义 → 下一步（Phase 2）
- `references/proc-and-apis.md` — CMM proc 节点 + 用户态查询 API + token 反查 owner（Phase 3）
- `references/cmm-ownership-rules.md` — 三对配对铁律 + 体系判别 + 常见错法（Phase 4）
- `references/root-cause-decision-tree.md` — 收敛决策树 + 证据强度分级（Phase 5）
- `references/fix-and-prevention.md` — 修复建议 + 预防规范（Phase 5）
- `references/mcp-auto-fetch.md` — 有 Jira 链接且 MCP 可用时如何自动拉取工单与日志（Phase 0）
- `references/case-exit-hang-cpu1.md` — 标杆案例：音视频退出 CPU1 挂死的完整推理过程
- `scripts/scan_cmm_log.sh` — 扫描日志：grep 全部关键字 + 抽取 phyaddr + 给初判
