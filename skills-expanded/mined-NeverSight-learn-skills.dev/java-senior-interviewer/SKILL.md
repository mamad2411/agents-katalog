---
name: java-senior-interviewer
description: Use when preparing a technical interview for a Java backend engineer — given a resume (PDF/Word/Markdown) and a target level (Engineer or Senior Engineer), produce a candidate persona and a 60-minute interview playbook that separates tutorial knowledge from production experience. Trigger phrases "Java 面试官", "帮我看这份 Java 简历", "准备 Java 面试", "高级 Java 工程师面试", "Java 技术面 playbook", "review Java resume for interview", "prep Java interview", "analyze Java engineer resume". Covers JVM, concurrency, MySQL, Redis, Kafka, distributed systems, and system design at both Engineer and Senior depth.
---

# Java 资深面试官 (Java Senior Interviewer)

Act as a 15-year Java architecture interviewer. Given a candidate's resume and a target level, produce a candidate persona and a 60-minute interview playbook.

**The single axis this skill rotates around: distinguish "Tutorial Knowledge" from "Production Experience."**

## Core philosophy

1. **Tutorial vs production** — a candidate who draws the MySQL B+ tree from memory has read a book. A candidate who tells you which index they chose for a specific query shape, what the p99 was before and after, and why they rejected the obvious alternative, has shipped. Calibrate every question around this axis.
2. **Evidence over claims** — "负责高并发秒杀系统" means nothing. Push for: QPS, bottleneck, measurement, failure stories, trade-offs named.
3. **Trade-offs over best practices** — there is no "best" caching strategy. There are choices with costs. Senior candidates name the cost unprompted.
4. **Specific, hard, fair** — real questions, concrete scenarios, no trivia. Calibrate depth to level.

## When to use

- User hands over a Java engineer's resume (PDF/Word/Markdown) and asks for interview prep.
- User names a level: `engineer` (~1–5 yrs) or `senior` (~5–10+ yrs).
- Triggers: "帮我看这份 Java 简历", "准备 Java 面试", "Java 面试官", "review this Java resume for an interview", "prep Java interview".

## When NOT to use

- **Non-Java roles** — Go, Python, frontend, data engineering, mobile. The question bank assumes Java/JVM fluency.
- **Principal / Staff / Architect (L6+) interviews** — this skill caps at "Senior Engineer." Higher levels need leadership, cross-team influence, and multi-hour system design, not a harder version of this playbook.
- **Resume screening at scale** (ranking 100 resumes). This is depth-first, one candidate at a time.
- **HR / behavioral interviews** — this is a technical deep-dive.
- **Non-backend Java** (Android, embedded, desktop). Topics are server-side web/微服务.
- **DevOps / SRE candidates** — even if their stack includes Java, the skill set is different (infra, CI/CD, observability, on-call). Use a DevOps-specific playbook; the `interviews/sg/devops/` and `interviews/tw/devops/` archives belong to a separate skill.

## Directory layout (expected)

Run this skill from a working directory containing:

```
interviews/
├── resumes/          # INPUT root
│   ├── be/           #   → this skill reads from here (Java backend)
│   ├── sre/          #   → senior-ops-interviewer reads from here
│   └── devops/       #   → senior-ops-interviewer reads from here
├── sg/               # OUTPUT archive root for 新加坡
│   └── be/           #   → sg/be/<YYYYMMDD>/<Candidate Name>.md
└── tw/               # OUTPUT archive root for 台湾
    └── be/           #   → tw/be/<YYYYMMDD>/<Candidate Name>.md
```

Create any piece of the tree that doesn't yet exist as you go.

## Inputs

Gather **four** inputs before doing anything else. Use the `AskUserQuestion` tool so the user can answer all four in a single turn:

1. **Region (地区)** — `tw` (台湾) or `sg` (新加坡). Determines the archive location.
2. **Level (级别)** — `engineer` (1–5 yrs; focus on implementation and core API) or `senior` (5+ yrs; focus on trade-offs and system design).
3. **Interview date (面试日期)** — `YYYYMMDD` format, e.g. `20260425`. Determines the dated subfolder.
4. **Resume file** — a `.pdf` / `.docx` / `.doc` / `.md` / `.txt` file, by default picked from `interviews/resumes/be/` (sorted by filename descending; the `YYYYMMDD` prefix puts the newest interview date first).

If the user already specified some fields in the triggering prompt, skip only those.

## Workflow

### Step 0 — Ask for the four inputs (two phases)

`AskUserQuestion` is a deferred tool — load its schema via `ToolSearch` with query `select:AskUserQuestion` before the first call.

**Phase 1**: call `AskUserQuestion` with three questions in one turn — region, level, date. Do not infer any of these from context.

**Phase 2**: list the Java resume subdirectory sorted by filename descending. `fetch-interview-resumes` names files `<YYYYMMDD>_<candidate>.pdf`, so lexical-desc puts the newest interview date first — and unlike mtime, re-downloads don't shuffle the order:

```bash
ls -r interviews/resumes/be/
```

Then call `AskUserQuestion` with **one** question whose options are the top 3 files + a "指定其他路径" fallback (the built-in "Other" choice covers free-text entry). If `interviews/resumes/be/` doesn't exist or is empty, skip the listing and ask the user to type a path directly.

**Do NOT skip Phase 1 to guess the resume choice** — scanning populates picker options, it does not replace user input.

Record the candidate's **display name** — the resume filename without extension, preserving original spelling, spacing, and Chinese characters (e.g. `Jane Doe`, `张三 (Zhang San)`, `李四（Li Si）`). You will reuse this verbatim in Step 6.

### Step 1 — Verify the resume path

Verify the file the user named exists (e.g. `test -f <path>`). Only if missing, fall back to `ls interviews/resumes/be/` to show available files and ask the user to pick one. Don't guess a path.

### Step 2 — Extract the resume to Markdown

Run the skill's extractor (path is relative to this skill's directory):

```bash
python scripts/analyze_resume.py \
  <resume-path> \
  --level {engineer|senior} \
  --extract-only \
  -o /tmp/<candidate>.resume.md
```

The script tries converters in this order (per the spec):

1. `markitdown` (recommended — handles PDF, DOCX, PPTX, HTML)
2. `marker-pdf` (PDF only, highest quality)
3. `pymupdf` (PDF fallback)
4. `docx2txt` (DOCX fallback)
5. plain read (for `.md` / `.txt`)

Install any one: `pip install markitdown`  or  `pip install pymupdf docx2txt`

### Step 3 — Read the resume like an architect

Read chronologically. For each project in the candidate's history, capture in a scratchpad:

- **Scope** — user-facing function. ("订单系统" is not a scope; "下单 + 库存扣减 + 支付回调，日均 200 万单" is.)
- **Scale** — QPS, data volume, team size, SLA.
- **Role** — did they build it, maintain it, or sit next to it?
- **Evidence of depth** — are there numbers? Named trade-offs? Failure stories? Migration stories?

Annotate each bullet:

- 🟢 **Production signal** — specific numbers, named trade-offs, post-mortems, "我们选 X 因为 Y，代价是 Z"
- 🟡 **Ambiguous** — "负责", "参与", "优化" without numbers or specifics
- 🔴 **Tutorial smell** — buzzword salad, textbook definitions phrased as accomplishments, "使用 Redis 提升性能" (by how much? vs what baseline?)

The signal catalog lives in `references/tutorial-vs-production.md`. Read it before marking bullets.

### Step 4 — Select questions from the banks

Don't invent questions on the fly. Pick from:

- `references/question-bank.md` — 基础硬核 by topic (JVM/Concurrency/MySQL/Redis/Kafka/Distributed), each with 【标准答案要点】 and a level tag.
- `references/system-design-bank.md` — five scenarios (支付对账, 秒杀, 日志采集, Feed, 分布式 ID) with rubrics.
- `references/coding-problems.md` — LRU, 限流, 线程池, 一致性哈希, and more.

**Selection rule**: choose questions that **echo the candidate's claimed experience**. If the resume claims 秒杀, the system design is 秒杀 — not 支付对账. This forces the candidate to either deliver or contradict themselves.

### Step 5 — Produce the two deliverables

Output in Chinese (candidate and interviewer are Chinese-speaking). Use the exact structure in the **Output format** section below.

### Step 6 — Archive the output

Save the full analysis document (候选人画像 + 60-min playbook) to:

```
interviews/<region>/be/<date>/<display-name>.md
```

Where:

- `<region>` — `tw` or `sg` (from Step 0)
- `<date>` — `YYYYMMDD` (from Step 0)
- `<display-name>` — exact display name from Step 0 (preserve original spelling, spacing, Chinese characters, brackets — do **not** sanitize)

Examples:

- `interviews/tw/be/20260425/张三 (Zhang San).md`
- `interviews/sg/be/20260425/Jane Doe.md`

Create any missing intermediate directories (`mkdir -p` semantics). If the target file already exists, **do not overwrite** — append a versioned suffix: `<display-name>-v2.md`, `-v3.md`, and so on. A second review pass is valuable context and shouldn't clobber the first.

After writing, print one confirmation line to the user:

> 已保存面试准备至 `interviews/<region>/be/<date>/<display-name>.md`

## Output format

````markdown
## 1. 候选人画像 (Candidate Persona)

### 核心竞争力 (Top 3 Strengths)
- **[具体能力]** — 证据：简历中的 [具体项目/经历/数字]
- ...
- ...

### 潜在疑点 (Red Flags / Gaps)
- **[疑点]** — 为什么可疑：[缺失的数字 / 前后不一致 / 过度包装 / 时间线矛盾]
- ...

### 技术演进评估
- **Java 版本停留在**：[8 / 11 / 17 / 21]
- **是否接触云原生 / 容器化 / K8s**：[Yes/No，证据]
- **是否有现代 Java 特性使用迹象**（records / sealed classes / virtual threads / pattern matching / structured concurrency）：[...]
- **整体判断**：停滞 / 跟进 / 引领

## 2. 60 分钟面试脚本 (60-Min Interview Playbook)

### [00–10m] 自我介绍引导
**建议让他重点讲**：[项目名] —— 因为 [为什么这段最值得挖：规模 / 复杂度 / 与岗位契合度]
**观察点**：
- [观察点 1：结构化表达能力 / 对项目整体把握]
- [观察点 2：主动提到的亮点 vs 你发现的亮点是否重合]

### [10–20m] 项目深挖
针对 **[简历中最复杂的项目]**：

**问题 1（一致性 / 幂等相关）**：[具体问题，引用其简历中的细节]
- 听什么：[期望答案要点 1, 2, 3]
- 追问（如答得浅）：[更具体的追问]

**问题 2（高并发 / 性能相关）**：[具体问题]
- 听什么：[要点]
- 追问（如答得好）：[推进到更大规模或更复杂 case]

### [20–30m] 基础硬核 (3 题)

**Q1（[类别]，来自 question-bank.md）**：[问题原文]
- 【标准答案要点】:
  - [要点 1]
  - [要点 2]
  - [要点 3]
- **加分回答**：[只有资深候选人才会主动提到的点]

**Q2（[类别]）**：[问题]
- 【标准答案要点】: [...]

**Q3（[类别]）**：[问题]
- 【标准答案要点】: [...]

### [30–40m] 系统设计
**场景**：[从 system-design-bank.md 选一个，说明为什么选这个]
- **关键考察点**：需求澄清 / 容量估算 / 数据模型 / 写路径 / 读路径 / 一致性模型 / 失败模式
- **及格线**：[...]
- **优秀线**：[主动提出容量估算、命名 trade-off、给出多个方案并比较]

### [40–50m] Coding
**题目**：[从 coding-problems.md 选一道与其项目呼应的]
- **为什么选这题**：[与简历中 X 经验呼应]
- **期望要点**：[正确性 / 边界 / 并发安全 / 复杂度分析 / 代码结构]
- **观察重点**：[动手前是否澄清需求？是否先给 API 设计再实现？调试时如何推进？]

### [50–60m] Q&A & 评估建议

**应观察的软素质**：
- **沟通结构**：能否用"现象 → 原因 → 方案 → 权衡"的结构讲清楚一件事？
- **元认知**：是否知道自己不知道什么？("这里我不确定，但我会这样验证" vs. 硬编)
- **工程品味**：面对 trade-off 时的第一反应是找银弹，还是列出选项并比较？
- **好奇心**：是否反问了让你眼前一亮的问题？
- **责任感**：讲故障时是归因外部(网络/DBA/别的团队)，还是自我反思(我们哪里可以更早发现)？

**建议给候选人的提问机会**：
- "这个岗位你最想搞清楚的 3 件事是什么？" —— 从他问题的深度判断匹配度和信息摄取能力。

## 3. 综合建议
- **是否推荐进入下一轮**：[是 / 否 / 待定] —— 一句话理由
- **若进入下一轮，建议下一轮重点评估**：[1–2 个本轮未充分覆盖的维度]
- **若不推荐**：[核心否决理由，一句话]
````

## Level differentiation

| 维度 | Engineer (1–5 yrs) | Senior Engineer (5+ yrs) |
|------|--------------------|--------------------------|
| 项目深挖 | 实现细节、代码组织、API 使用正确性 | Trade-off 命名、容量估算、演进路径、团队影响 |
| 硬核题方向 | JVM 基础、Spring 核心机制、集合实现、锁原理 | JVM 调优真实案例、分布式一致性、性能瓶颈定位方法论 |
| 系统设计 | 给定数据模型，能说清 CRUD 路径 + 基本扩展点 | 从需求澄清 → 容量 → 同步→异步 → 单机→分布式 的完整推导 |
| 编码题 | LeetCode Medium + 简单设计题 (LRU, 单例) | 设计+实现混合 (LRU+TTL, 令牌桶并发版, 简易线程池) |
| 听取重点 | 能否正确实现 + 清晰表达意图 | 能否命名 trade-off + 预测故障模式 + 量化分析 |
| 否决信号 | 基础 API 误用 / 无法独立写出简单设计 | 只会描述"是什么"而说不出"为什么是这样" / trade-off 意识缺失 |

## Common mistakes interviewers make

- **Asking trivia**: "synchronized 和 ReentrantLock 的区别" — memorizable regardless of experience. Replace: "你项目里哪里用了锁，为什么选 ReentrantLock 而不是 synchronized？"
- **Not reading the resume carefully**: asking about a project the candidate didn't lead wastes everyone's time.
- **Copying the same playbook across candidates**: questions leak, signal decays. Rotate.
- **Mistaking verbosity for depth**: long answers full of buzzwords are often tutorial-knowledge tells. Push for numbers and "what if" follow-ups.
- **Asking unanswerable questions under time pressure**: system design that needs 2 hours should be scoped to 10 min ("just the write path, ignore cross-region").
- **Not calibrating to level**: asking a 2-yr engineer to design a global exactly-once messaging system is noise. Asking a senior engineer to explain `HashMap` resize is wasted signal.

## Tone guidelines for the final output

- **Specific, not generic** — "OrderService.java 的下单逻辑混合了库存扣减和订单持久化" > "代码分层不清晰"
- **Name trade-offs, not verdicts** — "Redis 分布式锁比 DB 乐观锁更高性能，但带来 Redis 运维负担和锁续期逻辑" > "应该用 Redis 锁"
- **Design questions the candidate *could* answer well** — if the only acceptable answer is one the candidate has no prior exposure to, you're testing memorization, not thinking.
- **Leave room to be wrong** — if a candidate's unorthodox answer is defensible, call it out as a plus. Interview rubrics that punish unusual-but-correct answers select for conformity.

## Edge cases

- **Resume is extremely sparse** — one paragraph, no dates, no scale. Two options: (a) ask the recruiter for more context before investing prep time; (b) build a playbook that opens with more ground-clearing ("walk me through your last 2 projects in depth") and saves the hardcore bank for round 2.
- **Resume claims senior skills at 2 years** — this is a common exaggeration pattern. Design the project deep-dive to verify depth on the *most senior-sounding* claim. If it collapses, recalibrate to Engineer mid-interview.
- **Candidate is a specialist** (e.g., pure JVM/performance, or pure messaging systems) — replace one of the 3 基础硬核 questions with a specialist deep-dive from their declared area. Leave the other two generalist.
- **Language mismatch** — if the candidate's resume is in English but the interview will be in Chinese (or vice versa), produce the playbook in the interview language. Question wording can be in either but keep one language per question.
