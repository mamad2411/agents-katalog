---
name: obsidian-doc-router
description: >
  MANDATORY pre-flight gate & architecture pattern router for ANY engineering, ops,
  coding, deploy, onboarding, or configuration task.
  EVERY task MUST first consult the Obsidian vault to discover existing mature execution
  chains (成熟链路), established design patterns (设计模式), and canonical SOPs before
  writing code, creating scripts, or executing actions.
  DO NOT reinvent the wheel. DO NOT perform redundant live testing or exploratory hacking.
  BEFORE answering ops questions or grepping blindly, you MUST consult 00.MOC/AI-DOC-ROUTER.md.
  WHENEVER writing/creating/modifying docs, strictly follow the Anti-Orphan Recording SOP.
  Triggers when: ANY task involving coding, architecture, ops, automation, script writing,
  adding sites/channels, deployment, upgrade, configuration, or whenever user mentions 最佳实践,
  SOP, 接入, 设计模式, 架构, 签到, ainovel, CPA, tebi, pxed, Bohrium, Obsidian, 查文档.
---

# Obsidian 权威路由与成熟链路/设计模式复用规范（强制）

> **核心使命**：本 Skill 是 Agent 每次工程行动的 **最高前置门控（Pre-flight Gate）**。
> 用户的大量工程、运维、自动化与架构体系均已在知识库中完成沉淀与生产验证。
> **在敲下任何一行代码、新建任何一个脚本、调用任何一次浏览器或执行任何生产命令之前，必须首先进入知识库查验：是否存在已验证成熟的链路？是否存在现成可套用的设计模式？**
> **严禁忽视既有资产而凭直觉现场重造轮子或进行盲目的试错性 Live Testing！**

---

## Iron Law（三大核心铁律）

```
1. 事前（成熟链路与模式复用铁律）：NO ACTION BEFORE PATTERN & SOP LOOKUP
   执行任何任务（接入、开发、改构、部署、运维、治理）前，必须先在知识库中查验既有成熟链路与设计模式。
   凡有现成模式（如标准声明式接入、影子实例法升级、CDP 9222 挂载契约等），必须严格对齐复用，严禁现场臆造新变体！

2. 读时（权威路由铁律）：NO OPS/FACT FROM MEMORY OR BLIND SEARCH UNTIL ROUTER IS READ
   严禁凭模型记忆答复生产现状，严禁在全库盲目 grep 历史排查碎片；必须查阅 00.MOC/AI-DOC-ROUTER.md 并以下钻的 canonical 权威入口为准。

3. 写后（防孤岛闭环铁律）：NO ORPHAN DOC — 产出与新模式必须双向挂载
   新建或升级架构规范、最佳实践、部署手册时，必须闭环双向挂载回 AI-DOC-ROUTER 与 MOC 索引，严禁留孤儿笔记。
```

- **违反事前铁律** = 盲目重写已有成熟逻辑、在已知坑点上反复撞墙、浪费 API 额度与时间做无效现场试错（如多余的浏览器自动化测试），破坏生产一致性。
- **违反读时铁律** = 误把过时路径、旧域名或历史废弃变体当成现状的高概率事故。
- **违反写后铁律** = 辛辛苦苦提炼的新设计模式沦为孤岛，后续会话无法复用。

---

## Vault 基础环境

```bash
# 多机同步路径（带空格必须加双引号）
# macOS:
"$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/obsidian-note"
# Windows:
"E:/profile/note/note"
```

权威入口索引（相对 vault 根）：
- **全库总路由**：`00.MOC/AI-DOC-ROUTER.md`
- **技术与架构索引**：`00.MOC/技术笔记索引.md`
- **项目与业务索引**：`00.MOC/项目索引.md`
- **成熟经验与设计模式专区**：`Note/AI/经验/`
- **基础设施与运维手册专区**：`Note/Infra/`

---

## 一、 事前三级透视检索协议（Pre-flight Three-Tier Protocol）

当收到用户的任务需求后，**第一步绝对不是打开代码文件或启动终端跑测试**，而是执行以下标准检索链：

```
用户请求 → 提炼 [业务动作] + [核心组件/领域] 
         ↓
第 1 级：查路由表 (doc-lookup / AI-DOC-ROUTER.md) —— 定位权威入口与生产真相速读
         ↓
第 2 级：查成熟链路与设计模式 (Note/AI/经验/ & Note/Infra/) —— 继承成熟 SOP 与架构范式
         ↓
第 3 级：模式对齐确认（显式输出采纳的成熟模式） → 方可开始最小化、精准化执行
```

### 1. 检索执行动作
- **脚本检索（首选）**：
  在 vault 根执行 `python3 .local/bin/doc-lookup "<业务词> <动词>"`（例如 `doc-lookup "公益站 签到"`、`doc-lookup "CPA 升级"`、`doc-lookup "反代 最佳实践"`）。
  *注：`doc-lookup` 会按词全命中匹配领域、触发词、权威入口及速查列，命中即停。*
- **路由直读**：若脚本受限，直接 **Read** `00.MOC/AI-DOC-ROUTER.md`。
- **模式下钻**：若涉及架构选型或复杂流程，进一步 Read 入口链接的主手册（`Note/Infra/*.md`）或经验库（`Note/AI/经验/*.md`）。

### 2. 知识库典型成熟设计模式矩阵（直接对齐，严禁重造）

| 业务场景 | 库内成熟设计模式 / Canonical 链路 | 典型权威入口 | 严禁犯的低级错误（反模式） |
|---|---|---|---|
| **接入新签到站 / 服务** | **声明式配置模式**：优先只在 `sites.yaml` + DB + 任务投影登记；已有现成标准 New API / SSO 解析流 | `[[公益站签到运维手册]]` | ❌ 重新手写爬虫脚本<br>❌ 唤起 CDP 做无用 live 登录测试撞验证码 |
| **浏览器自动化 / 爬虫** | **CDP 9222 Attach-Only 模式**：只读挂载用户常驻 Chrome，严禁 kill、严禁 restart，严禁无差别清 Cookie | `[[公益站签到运维手册]]`<br>`[[Playwright MCP共享浏览器架构与避坑]]` | ❌ 杀掉浏览器进程<br>❌ 清空所有域名 Cookie<br>❌ 多开实例撞 SingletonLock |
| **服务 / 反代版本升级** | **影子实例法（Shadow Instance SOP）**：分配临时独立端口拉起验证，健康检查全绿后原子割接并清理 | `[[tebi CPA 栈部署与运维]]`<br>`[[CPA 升级最佳实践（影子实例法 SOP）]]` | ❌ 直改生产配置盲目重启<br>❌ 未做热备直接就地覆盖升级 |
| **数据库或重要配置变更** | **原子快照与回滚脚本先行模式**：变更前必须 SQLite `VACUUM INTO` 或文件 copy 快照，并备好 rollback.sql | `[[MangoApi 部署与运维]]` | ❌ 在生产数据库执行裸 update/delete<br>❌ 出现故障无法一键回滚 |
| **内网穿透 / 机器互联** | **EasyTier Mesh + STCP 双栈中继模式**：通过网格内网虚拟 IP 直连，无公网入站机器走 FRP STCP | `[[windows-hosts]]`<br>`[[Cue 沙盒接入最佳实践]]` | ❌ 暴露不安全的公网高位端口<br>❌ 新建重复的 FRP 服务端 |
| **跨会话防丢与知识沉淀** | **双向挂载防孤岛模式**：标准 Frontmatter + 权威入口速读 + MOC 双链 + 路由表登记 | `[[AI-DOC-ROUTER]]`<br>`[[AI 文档路由治理经验]]` | ❌ 新写散落的文件后关会话<br>❌ 建带时间戳的临时垃圾笔记 |

### 3. 行动前对齐契约（Pre-action Alignment）
在完成知识库查验后、开始动工前，应当在规划中或对用户有一句话明确确认：
> *「已核对知识库，本项目存在成熟链路 `[[xxxx]]`。本次操作将直接复用 `[声明式配置 / 影子实例法 / CDP 只读接入 / ...]` 模式执行，不进行冗余的现场试错与重复开发。」*

---

## 二、 读与查询流程（答复与事实下钻）

1. **查路由**：`python3 .local/bin/doc-lookup "<query>"` 或 Read `00.MOC/AI-DOC-ROUTER.md`。
2. **读入口**：匹配表中「权威入口」→ **Read 入口整篇**。
3. **查细节**：需要深入再读入口链接的主手册；**禁止**用全库 `rg` 的任意碎片命中覆盖入口。
4. **冲突仲裁**：若入口与其它笔记冲突：**以入口 + 其指向的主手册为准**，并点名冲突文件。
5. **归因输出**：回答生产事实时写明依据笔记名（如「据 [[公益站签到运维手册]]」）。

### 路由未命中 Fallback 策略
若 `AI-DOC-ROUTER.md` 未命中：
1. 检查 `00.MOC/` 目录下相关索引（如 `技术笔记索引.md`、`项目索引.md`）。
2. 若仅在非 Canonical/历史排查笔记中搜到片段，**必须向用户声明**：「此信息仅在非权威历史笔记 [[xxx]] 中提及，生产可能已变更，建议核验」。
3. 协助用户将确认后的事实**就地登记**进 `AI-DOC-ROUTER.md`。

---

## 三、 Agent 记录文档防丢 SOP（写文档闭环）

为用户创建、重构或沉淀新设计模式/最佳实践时，**必须执行以下 5 步闭环**：

### 1. 规范落盘路径与命名
- 严禁随意堆在根目录。
- **经验 / 成熟 SOP / 架构模式**：`Note/AI/经验/<主题>最佳实践.md` 或 `<主题>设计模式.md`
- **运维 / 基础设施 / 部署手册**：`Note/Infra/<服务名或架构名>.md`
- **项目开发文档**：`Note/Project/<项目名>/<项目名> 开发文档.md`
- **账号 / 资产清单**：`Note/Accounts/`（私有敏感；Agent 只登记结构与路径，不回显敏感密钥）

### 2. 标准 Frontmatter 元数据
```yaml
---
title: <文档标题>
tags:
  - <主分类，如 Infra/Deploy/Ops/BestPractice>
  - <服务或领域名>
  - canonical  # 若为权威主手册/设计模式
status: canonical # 或 active / draft
updated: YYYY-MM-DD
aliases:
  - <别名1>
  - <缩写>
---
```

### 3. 文档主体标准骨架
```markdown
# <文档标题>

## 速读（当前有效 · 维护于 YYYY-MM-DD）

- 一行生产真相 / 核心结论：当前运行机器、端口、关键规范、标准化操作步骤。
- 注意：此标题写法是 doc-lookup 速读区与 scan-stale-docs --strict-tldr 的解析契约，勿改成别的格式。

## 核心设计模式与架构原则
- **模式定义**：...
- **标准化模式适用场景**：...

## 标准操作 / 接入 / 执行 SOP
1. 第一步：...
2. 第二步：...

## 变更与排障记录
- YYYY-MM-DD: ...
```

### 4. 双向挂载（核心防丢防孤岛步骤）
1. **登记路由**：在 `00.MOC/AI-DOC-ROUTER.md` 的表格中追加或更新对应的一行（触发词 ≤15 个，速查 ≤200 字）。
2. **挂入主题 MOC**：在 `00.MOC/` 下对应的 `项目索引.md` / `技术笔记索引.md` 挂入双链。
3. **原地更新原则**：已有对应 Canonical 文档时，严禁另起新孤儿文件，直接在原文档就地维护并更新 `updated` 日期。

### 5. 校验闭环
在 vault 根执行健康检查：
```bash
python3 .local/bin/scan-stale-docs
```
确保无断链、无语法解析错误。

---

## 四、 核心反模式（严厉禁止）

- 🔴 **「想当然」直接动手**：接单后立刻开始写脚本、调用工具打桩，把知识库已有的成熟模式弃置不顾。
- 🔴 **过度无用 live testing**：已有声明式配置规范时，偏要启动 live 真实运行（如多余的浏览器登录注册、撞验证码），浪费用户额度与时间。
- 🔴 **重新发明已被解决的轮子**：对已经存在稳定运行机制的业务（如 New API 渠道管理、签到适配器、反代网关），重新造一套孤立的新逻辑。
- 🔴 **破坏性调试**：在生产环境随意重启主服务、杀进程、清空 Cookie 或修改生产 DB 且不做备份。
- 🔴 **碎片化流水账**：随手新建带时间戳的文件（如 `xxx-20261104.md`），既不挂 MOC 也不登路由表，使知识库沦为垃圾场。

---

## 五、 跨 Skill 优先级与执行契约

- **前置优先级最高**：无论后续使用 coding、debugging、ops、deploy 还是 browser-use 类 skill，**本 skill 规定的事前最佳实践与设计模式查验具有绝对前置优先级**。
- **职责划分**：
  - 本 Skill 负责 **「行动前查什么模式/链路」**、**「读哪篇权威入口」** 与 **「产出如何防丢沉淀」**；
  - 专业执行 Skill（如 `systematic-debugging`, `evidence-driven-bugfix`, `browser-use` 等）负责在成熟模式指导下的具体落地实施。
