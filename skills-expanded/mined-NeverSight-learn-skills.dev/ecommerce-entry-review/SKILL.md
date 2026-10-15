---
name: ecommerce-entry-review
description: Use this skill whenever the user needs to review a new hire's entry task project — especially a Java plus Spring Boot e-commerce system (monolith or microservices) — and prepare for a 1-1 discussion. Trigger on phrases like "review 新人的入职项目", "帮我看新同学的 entry task", "准备和新人 1-1", "review new hire code", "onboarding task review", "新人入职任务 review", or when the user uploads a Java/Spring e-commerce codebase in the context of onboarding or mentoring. Apply this even if the user just says "帮我 review 一下这个项目" when the prior context is about onboarding a new engineer. The skill produces two deliverables — a prioritized growth-oriented review report, and a Socratic 1-1 discussion guide with open-ended questions rather than direct answers — with focus on order state machines, concurrent inventory deduction, payment callback idempotency, DDD and bounded contexts, microservice boundaries, distributed transactions, caching, async, and observability.
---

# New Hire E-commerce Entry Task Review

Help a mentor run a thorough, growth-oriented review of a new hire's entry task (Java 25 + Spring Boot 3.5 e-commerce system, monolith or microservices) and produce a 1-1 discussion guide that teaches through questions rather than lectures.

## Core philosophy

The goal is **not** to produce an exhaustive list of flaws. A new hire who receives 80 bullet points will feel attacked, not coached. Instead:

- **Prioritize ruthlessly** — a new hire can absorb maybe 3–5 key points in a 1-1.
- **Balance** — a good review names what works alongside what doesn't.
- **Socratic over didactic** — prefer "你当时是怎么权衡的？" over "你应该这样做". The new hire should leave the 1-1 with new *ways of thinking*, not just a fixed to-do list.
- **Trade-offs, not verdicts** — most real engineering choices have trade-offs. Frame discussion around trade-off exploration, not right/wrong.
- **Specific over generic** — "OrderServiceImpl.java:45–80 混合了库存扣减和订单持久化" beats "代码分层不清晰".

## Process

Follow these steps in order. Don't skip ahead.

### Step 0: Check for a previous review

Before doing anything else, look for previous review files in the directory where you're working:

```
ls reviews/review-*.md 2>/dev/null | sort | tail -1
```

If a previous review file exists:
- Extract its `**Reviewed commit:**` line to get the prior commit hash.
- Run `git log <prior_commit>..HEAD --oneline` to see what changed since then.
- Note which top issues from the prior review are still open vs. likely addressed.
- You will use this to produce a **Delta section** in Deliverable 1 (see Step 4).

If no previous review exists, skip the delta section — this is the baseline review.

### Step 1: Get the bird's-eye view first

Before opening individual files, answer these:

- **What did they build?** Scope — products, cart, orders, payment, inventory, user, promotion?
- **Monolith or microservices?** What was their rationale? If microservices: how many services, what are the boundaries?
- **Rough size** — LOC, number of modules/services, dependency count.
- **Stated goals vs. actual** — if there's a README or design doc, compare claims with reality.

Look at, in order: `README.md`, architecture diagrams, root `pom.xml` / `build.gradle`, module/package layout, `docker-compose.yml`, main `@SpringBootApplication` classes.

Only after this, dive into specific files. The bird's-eye view shapes everything that follows.

### Step 2: Review systematically across dimensions

Read `references/review-checklist.md` for the full dimension list — generic Java/Spring concerns: architecture, modern Java 25 & Spring Boot 3.5 usage, API design, persistence, testing, security, observability, build/ops, code quality.

Then read `references/ecommerce-hotspots.md` for e-commerce-specific hot zones:
- 订单状态机 (order state machine)
- 并发扣减库存 (inventory concurrency)
- 支付回调幂等 (payment callback idempotency)
- 领域建模 / DDD / 限界上下文
- 微服务边界 / 分布式事务 / Saga
- 性能 / 缓存 / 异步 / 可观测性

For each dimension, capture:
- **✅ Strength** — done well, with specific file/line citation.
- **⚠️ Issue** — labeled **Blocker / Major / Minor / Nitpick**.
- **💡 Growth opportunity** — not wrong, but a learning stretch (e.g., "能跑，但虚拟线程没用上 —— 可借此理解 JDK 21+ 结构化并发").

### Step 3: Prioritize — do not overwhelm

Distill down to:
- **Top 3–5 strengths** (specific, not patronizing)
- **Top 3–5 issues for 1-1** (conceptual/design > typos)
- **Top 2–3 growth areas** for the next 1–3 months

Everything else — minor style issues, naming nitpicks, small refactors — goes into a written appendix. The mentor may share it in writing but shouldn't spend 1-1 time on it.

### Step 4: Produce the two deliverables

Output **two clearly separated sections** in Chinese (since the mentor and new hire are Chinese).

#### Deliverable 1: Review Report

Use this exact structure:

```
# [项目名] 入职任务 Review Report

## 总体评价
[2–3 句话：完成度、技术深度、整体水平。要有判断力，不要"总体不错"这种空话。]

## 亮点 (top 3–5)
- **[亮点标题]**: [具体做得好的地方，引用文件/类/行号]

## 需要 1-1 讨论的关键问题 (top 3–5)
### [问题标题] — [Blocker | Major | Minor]
- **现象**: [在哪、是什么]
- **为什么重要**: [实际影响 —— 不是"规范要求"，而是"在生产环境会导致什么"]
- **讨论方向**: [1-2 个探索方向，提示思路而非直给答案]

## 成长机会 (top 2–3)
- **[方向]**: [为什么这是下一步的好目标]

## 详细反馈附录
按文件/模块组织所有 minor / nitpick。可直接作为书面反馈发给新人。

## 与上次 Review 的对比 (仅当存在上次 review 文件时)
**上次 review commit**: `<prior_commit_hash>`
**本次 review commit**: `<current_commit_hash>`
**新增提交**: `git log <prior>..HEAD --oneline` 的结果摘要

### 已改善
- [上次的 issue 标题] — 具体哪里改了，改得怎么样

### 仍然存在
- [上次的 issue 标题] — 是否有进展？原因分析。

### 新发现的问题
- [新 issue] — 是否与新增代码相关，还是之前遗漏了
```

#### Deliverable 2: 1-1 讨论指南

Use this exact structure:

```
# 1-1 讨论指南 — [项目名]

## 准备
开会前 5 分钟看一眼，对齐今天的目标。核心原则：**少讲、多问**。

## 开场 (≈5 分钟)
让他先自我讲述：
- "讲一下你做的项目吧 —— 重点想解决什么问题、你最满意的部分、最卡壳的地方？"

观察：
- 他主动提的和你发现的重合/不重合在哪里？
- 他对自己设计的判断力如何？

## 技术决策深挖 (≈15–20 分钟)
对每个 Top 问题准备一组开放式问题。先问开放的，如果答得浅再追问。

### 问题 1: [标题]
- **起手式**: [开放式问题，引导描述思考]
- **如果答得浅 / 没意识到问题**: [更具体的追问，但仍不直给答案]
- **如果答得好**: [推进一步，扩展到更大场景或更复杂 case]

[对每个 top 问题重复]

## 正反馈 (≈5 分钟)
具体、明确 call out 他的亮点 —— 不是泛泛表扬，而是"你在 X 处做了 Y，说明你已经有 Z 的思维"。

## 成长方向对齐 (≈10 分钟)
- 问他："如果再做一次，你会在哪些地方不一样？"
- 对齐接下来 1–3 个月的 2–3 个重点成长方向。
- 让他自己 commit 到下一步的行动。

## 行动项
- [ ] [具体 follow-up — 谁做、做什么、什么时候]
```

See `references/discussion-guide.md` for question templates (by review dimension) and facilitation tips — how to probe deeper, how to handle defensive or over-agreeable responses.

### Step 5: Save the review to a dated file

After producing both deliverables, write the review to a persistent file so future reviews can diff against it.

1. Get the current HEAD commit: `git log -1 --format="%H %s"`
2. Determine the save path: `reviews/review-YYYY-MM-DD.md` relative to the working directory. Create the `reviews/` directory if it doesn't exist.
3. Write the file with this header followed by both deliverables:

```
---
reviewed_commit: <full commit hash>
reviewed_at: YYYY-MM-DD
project: <project name>
---

**Reviewed commit:** `<full commit hash>` — <commit subject>

[Deliverable 1 content here]

---

[Deliverable 2 content here]
```

4. Tell the user: `已保存 Review 至 reviews/review-YYYY-MM-DD.md（commit: <short hash>）。下次 review 时会自动与本次结果对比。`

If the `reviews/` directory is inside the reviewed project's git repo, remind the user to add it to `.gitignore` if they don't want to commit mentor notes there, or commit it intentionally as a coaching artifact.

## Tone guidelines

- **Curious, not judgmental** — "这里我想听听你的思路" > "你这里错了".
- **Kind but honest** — don't sugarcoat real issues; new hires respect honest feedback more than empty reassurance. But frame every critique as a learning opportunity.
- **Actionable** — every issue should imply a direction. If you can't articulate what "better" looks like, the issue isn't ready to discuss.
- **Trade-off aware** — if you propose an alternative, name its cost. "Redis 分布式锁比 DB 乐观锁更高性能 —— 但带来 Redis 运维负担和锁续期逻辑" is good feedback. "应该用 Redis 分布式锁" is not.

## Edge cases

- **No code provided** — briefly ask what form the project is in (repo link / zip / pasted snippets). One or two questions, not a barrage. If code truly can't be provided, produce a *review preparation checklist* the mentor can work through manually.
- **Microservices with many services** — don't deep-review every service. Pick 2–3 representative ones (different concerns: write-heavy, read-heavy, integration-heavy) for depth; survey the rest.
- **Very small or very large project** — scale accordingly. A 500-line project doesn't need 5 deep-dive questions. A 20k-line project needs you to pick the most instructive slices.
- **Clearly rushed / incomplete project** — don't hide it, but focus the 1-1 on understanding *why* and on what *is* complete. Incomplete work still reveals a lot about thinking.
