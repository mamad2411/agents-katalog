---
name: coding-principles
description: Mandatory activation — 3 Pre-Gates + 6 Principles + 3 Traps layered discipline system. V2.9 adds breadcrumb exemption from 300-line count + self-check rule 29 file-size auto-check. Regardless of task type, self-check all before outputting any code.
tags: [ai-coding, programming-principles, code-quality, mandatory, breadcrumb, pre-gate, discipline, file-size-check]
version: 2.9.0

---

# Mandatory: AI Coding Discipline / AI编程纪律（每次对话强制激活）

> **Mandatory rule. Every coding session executes three-layer discipline: Pre-Gates → 6 Principles → 3 Traps. V2.7 adds Multi-Stack Detection + Progressive L1/L2/L3 Activation.**
> **强制纪律。每次编码会话必须执行三层体系：前置门 → 六大原则 → 三大陷阱。V2.7 新增多技术栈陷阱检测 + 按改动大小分层激活。**

## Usage Rules / 使用规则

**Must execute when any of the following is true / 以下任一条件满足时必须执行：**

- User asks to modify code / 用户要求修改代码
- User reports a bug / 用户报告 Bug
- User requests a new feature / 用户要求新功能
- Code review / refactoring / 代码审查或重构

---

## Layer 1: Pre-Gates / 第一层：前置门（Pre-Code — Must Pass Before Writing Any Code / 动手前必须通过，不通不许写代码）

### Gate 1: Three Questions / 门1：三问三答（Patch Self-Check / 补丁自检）

**Before proposing any change, answer these three questions (all three required): / 提出修改方案前必须回答三个问题（缺一不可）：**

```
Q1: Have I traced the full call chain? / 我追踪了完整调用链吗？
  → List every node: user entry → API endpoint → data layer → rendering
  → 列出每个节点：用户入口 → 服务端端点 → AI调用 → 前端渲染
  → Write down actual file+function names for each node, don't just say "I checked"
  → 写清文件+函数名，不只是口头说"我看过了"

Q2: Have I confirmed all branch paths? / 我确认了所有分支路径吗？
  → List all paths: different views / environments / user types / platforms
  → 列出所有路径
  → Mark each: "✅ confirmed unaffected" or "🔧 needs sync change"
  → 每一行标注"✅确认不受影响"或"🔧需要同步修改"

Q3: Is my fix an architecture-level unified fix, or a single-path patch? / 修复是架构层面统一修复还是单路径补丁？
  → If only one path was changed → first answer "why can't we unify" before proceeding
  → 如果只改了一个路径 → 先回答"为什么不能统一修复"再动手
  → If the answer is weak → stop and rethink, don't continue
  → 如果答案牵强 → 停下来重新思考，不要继续
```

**Violate any question → the change is invalid, must roll back and restart. / 违反任一条 → 修改视为无效，必须回退重来。**

**Self-check pass indicator**: explicitly output the three answers (short is fine, but must be verifiable). / **自查通过标志**：在回复中显式输出三问三答（不用太长，但必须可验证）。

### Gate 2: Repeat Bug Cap / 门2：重复Bug上限

```
Rule: If the same bug has been fixed 2 times and still broken,
      the 3rd action MUST be web search, NOT a 3rd code fix.
规则：同一个Bug改了2次还修不好时，第3次行动必须是上网搜索，不是改第3版代码。

Search strategy / 搜索策略:
1. "[Framework] + [symptom keywords]" (e.g. "React useEffect infinite loop")
2. GitHub Issues (framework official repo)
3. StackOverflow / community forums
4. Try 3 different keyword combinations / 关键词试3组不同组合

Consequences of ignoring / 违反后果:
- 3 fixes = wasted time / 浪费时间
- 4 fixes = introduces new bugs / 引入新Bug
- 5 fixes = project quality collapses / 项目质量崩塌
```

### Gate 3: File Size Decision / 门3：空间决策（300-line Redline + New Feature = New File / 300行红线 + 新功能开新文件）

```
Before touching any file, check / 动手前判断:
1. Target file current line count > 300? / 目标文件当前超过300行？
   → YES: split first, then modify (never append to large files)
   → 是：先拆分再修改，不往大文件追加
   → Note / 注：🍞 breadcrumb headers (~15-20 lines) do NOT count toward 300 / 🍞 面包屑头部不计入300行上限
2. Is this a new feature or modifying existing? / 这是新增功能还是修改现有？
   → New feature: MUST create new file/module / 新增功能：必须新建文件/模块
   → Modify existing: consider splitting first if file is large / 修改现有：优先考虑先拆分再修改

Exemptions / 豁免:
  - Pure config/declaration/boilerplate: relax to 500 lines / 纯配置/声明/框架代码：可放宽至500行
  - Highly cohesive algorithms (state machines, compiler cores): relax to 400 lines / 高度内聚算法：可至400行
  - Auto-generated code: don't count / 框架自动生成代码：不计入
  - 🍞 Breadcrumb headers (metadata): don't count / 🍞 面包屑头部（元数据）：不计入

Post-change auto-check (self-check rule 29): after modifying a file, if functional code still > 300 lines → ⚠️ warn suggest split
改后自检强制检查（规则 29）：改后自检时，若改动后功能代码仍超 300 行 → ⚠️ 警告建议拆分
```

---

## Layer 2: Six Principles / 第二层：六大原则（While Coding — Follow Each One / 写码时逐条遵守）

### Principle 0: Breadcrumb Pre-Scan 🍞 / 原则0：面包屑预扫描

> Breadcrumbs are the AI's project map. Before modifying any file, scan its 🍞 header to understand what else depends on it.
> 面包屑是AI的"项目地图"。改文件前先扫描🍞头部，了解改了这里会影响谁。

**When opening any file for modification / 打开文件准备修改时:**

1. **Scan for 🍞 breadcrumb block**: search for `🍞 AI Breadcrumb` in file header / 搜索文件头部🍞导航块
2. **If found** → parse the breadcrumbs / 解析面包屑:
   - `@COUPLED` entries → these files must be checked/updated together / 联动文件，必须同步检查
   - `📖` entries → these docs contain related design details → read them / 关联设计文档，需要读
   - `@GOTCHA` entries → known traps in this code → avoid them / 已知陷阱，避开
   - `@BUGFIX` entries → historical bugs fixed here → don't regress / 历史修复记录，别回退
3. **If NOT found** → 🚨 **DO NOT modify code yet! Seed breadcrumbs first (30 seconds max):** / **禁止直接改代码！先播种面包屑：**
   a. **Search linked files / 搜联动文件**: `search_content` for `import`/`require` of this file in the project → write `@COUPLED`
   b. **Search design docs / 搜设计文档**: `search_content` in dev docs for this file name or module name → write `📖`, read key decision docs if found
   c. **Check git history / 查历史Bug**: `git log --oneline -10 <this file>` → recent bug fixes → write `@BUGFIX`
   d. After completing a-c, insert the 🍞 header block (format below), then proceed with the code change / 完成以上三步后插入🍞头部，再改代码
4. **Use parsed breadcrumbs to expand change scope**: add @COUPLED files to your "must check" list before making changes / 把联动文件加入检查清单

**Breadcrumb standard format / 🍞 面包屑标准格式** (design principle: AI understands at a glance, no external docs needed / AI一眼就能理解，不需要读任何外部文档):

```
/*
 * ─── 🍞 AI Breadcrumb Navigation ──────────────────
 * Tag meanings: @COUPLED=linked files @GOTCHA=gotcha @BUGFIX=bug fix @MAGIC=magic number
 *              @DEPENDS=external dependency @ASSUME=assumption @TODO=todo @WHY=design rationale
 *              @PERF=performance @CONTRACT=interface contract 📖=dev doc reference
 * 
 * Breadcrumbs (changing this affects):
 *   @COUPLED sync needed: fileA.js#L200, fileB.html
 *   📖 see: docs/architecture/tool-registration.md
 *   @BUGFIX 2026-07-06: reason, fix: solution
 * ──────────────────────────────────────────────────
 */
```

**Why this format AI-readable without external docs / 为什么这个格式 AI 能理解（无需外部文档）**:
- `🍞` emoji = visual anchor, AI can grep `/🍞/` to locate instantly / 视觉锚点，一秒定位
- Tag meanings line = **inline cheat sheet**, no need to read ANCHOR_SPEC.md / 内嵌速查手册
- `@COUPLED sync needed: file1, file2` = tells AI exactly what to change together / 直接告诉 AI 改哪里
- `📖 see: doc path` = entry point to detailed design docs / 设计文档入口
- `@BUGFIX date:reason, fix:solution` = don't regress / 别回退

**Key principles / 关键原则**:
- Breadcrumbs are **alive** — update with every change, not write-once-forever / 面包屑是活的，每次改动都要更新
- Breadcrumbs are **specific** — `@COUPLED` must specify file paths, not vague "all frontend files" / 必须写具体路径
- Breadcrumbs are **self-documenting** — the tag glossary ensures even AI without this Skill loaded can understand / 自解释的
- Don't aim for massive one-time annotation — **seed as you go** / 改代码即播种

### Principle 1: Think First / 原则1：先思考

```
Don't code from memory. Read files to confirm current state before acting.
Understand WHY the code looks like this before deciding HOW to change it.
Define change scope beforehand — don't expand while coding.

改代码前必须读文件确认现状，不准凭记忆盲改。
先理解为什么代码长这样，再决定怎么改。
修改范围必须事前想清楚，不准边改边扩大范围。
```

**Intent Anchor Pre-Judgment / 意图锚点预判（before writing code, plan what breadcrumb tags you'll need / 写码前预判需要什么标签）:**

When reading the target file, scan existing anchors and pre-plan new ones / 读文件时扫锚点并预判:

```
□ Multiple design choices? → Prepare @WHY chose-A-not-B: reason / 方案有多个选择？→ @WHY
□ Hardcoded business numbers/constants? → Prepare @MAGIC value=meaning, sync with [file] / 硬编码了业务数字？→ @MAGIC
□ Change affects other files? → Prepare @COUPLED sync needed: [file list] / 改动影响其他文件？→ @COUPLED
□ Depends on external system quirks? → Prepare @DEPENDS [system]'s [behavior], must [action] / 依赖外部系统怪异行为？→ @DEPENDS
□ Depends on data format assumptions? → Prepare @ASSUME [assumption], if [condition changes] adjust [logic] / 依赖数据格式假设？→ @ASSUME
□ Temporary workaround? → Prepare @TODO [date] [planned solution] / 临时方案？→ @TODO
□ Fixing a bug? → Prepare @BUGFIX [date]:[cause], fix:[solution], test:[entry] / 修Bug？→ @BUGFIX
□ Performance-sensitive but intentionally not optimized? → Prepare @PERF [why not optimize] / 性能敏感但故意不优化？→ @PERF
□ Design intent too complex for inline comment? → Prepare 📖 [doc path] / 代码写不下设计意图？→ 📖

Don't wait until self-check to add these — by then you've already forgotten the design rationale.
不要等到自检时才补——那时已经忘了设计理由。
```

### Principle 2: Subtraction First / 原则2：做减法优先

```
When fixing bugs, always ask first: can this be solved by DELETING code?
A bug fixable by removing 3 lines should NEVER add even 1 line of patch.
Fight the LLM's natural instinct to "add code" — code growth is entropy,
good fixes should be entropy reduction.

修Bug时优先问：能不能通过删除代码来解决？
能删3行解决的Bug，绝对不加1行补丁。
对抗LLM天然的"堆代码"本能——代码量增长是熵增，好的修复应该是熵减。

Anti-pattern / 反例:
- ❌ Add an if-branch for a special case (piling code) / 加if分支处理特殊情况
- ✅ Remove the redundant logic that created the special case (subtraction) / 删掉导致特殊情况的冗余逻辑

Self-check: Is the net line count (added - deleted) positive or negative?
If positive, ask: are these added lines truly impossible to delete?
自检：本次改动的净行数是正还是负？如果为正，这些新增代码真的不可删除吗？
```

### Principle 3: Keep It Simple / 原则3：保持简单

```
Minimize change scope. Never touch unrelated code.
Don't introduce unnecessary abstraction layers.
Keep code readable, maintainable, rollbackable.

最小化改动范围，无关代码一律不动。
不引入不必要的抽象层。
保持代码可读、可维护、可回滚。
```

### Principle 4: Precise Modification / 原则4：精准修改

```
Only change target code. Don't "optimize" unrelated modules on the side.
Confirm impact scope before modifying, confirm only target files changed after.
Must go through Pre-Gate 1 (Three Questions) to confirm all branch paths.

只改目标代码，不顺手"优化"无关模块。
修改前确认影响范围，改后确认只动了目标文件。
必须走前置门1（三问三答）确认所有分支路径。
```

### Principle 5: Goal-Driven / 原则5：目标驱动

```
Code must run after changes. Feature must be a closed loop.
Leave no half-finished work, no "I'll fix it later" traps.
Modification complete → verify immediately → confirm closure.

改完代码必须能跑，功能闭环。
不遗留半成品、不留下"回头再弄"的坑。
修改完成 → 立即验证 → 确认闭环。
```

---

## Layer 3: Three Traps / 第三层：三大陷阱（Must Avoid While Coding / 写码时强制避开）

### Trap A: Numeric Values Cannot Use `||` for Null Check / 陷阱A：数值不可用 `||` 判空

```javascript
// ❌ Wrong / 错误: 0 is treated as falsy / 0被当作falsy
const count = userInput || defaultValue;

// ✅ Correct / 正确: only check null/undefined / 只判null/undefined
const count = userInput ?? defaultValue;
// Or for wider compatibility / 或兼容旧版:
const count = userInput != null ? userInput : defaultValue;
```

### Trap B: `<select>` Must Have Placeholder `<option>` / 陷阱B：`<select>` 必须加占位 `<option>`

```html
<!-- ✅ Correct: default non-submittable placeholder / 有默认不可提交的占位项 -->
<select>
  <option value="" disabled selected>Please select... / 请选择...</option>
  <option value="a">Option A</option>
</select>
```

### Trap C: POST upsert UPDATE Branch Must Not Hardcode Fields / 陷阱C：POST upsert 更新分支不可硬编码字段

```
POST upsert interface's update logic MUST dynamically read field names,
never hardcode specific fields.
Schema changes over time — hardcoded fields cause new fields to be lost.

POST upsert 接口的更新逻辑必须动态获取字段名，不可硬编码具体字段。
因为schema会变，硬编码字段会导致新字段丢失。
```

---

## Layer 4: Multi-Stack Trap Detection / 第四层：多技术栈陷阱检测 (V2.7 NEW)

> Not all projects are JavaScript. Different languages have their own "foot-guns" — patterns that look correct but silently cause bugs.
> 不是所有项目都用 JavaScript。不同语言有各自的"暗坑"——看起来正确但悄悄出错的模式。

### Python Traps / Python 陷阱

```python
# ❌ Trap P1: Mutable default arguments / 可变默认参数
def add_item(item, items=[]):  # BUG: items shared across all calls!
    items.append(item)
    return items

# ✅ Correct / 正确:
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# ❌ Trap P2: Late Binding Closures / 延迟绑定闭包
funcs = [lambda x=i: x for i in range(3)]  # BUG: all return 2!
# ✅ Correct / 正确:
funcs = [lambda x=i: x for i in range(3)]  # actually still wrong...
# Really correct:
funcs = [(lambda v: lambda: v)(i) for i in range(3)]

# ❌ Trap P3: `is` vs `==` for value comparison / is用于值比较
if x is 1000:  # BUG: small ints cached but 1000 might not be
# ✅ Correct / 正确:
if x == 1000:
```

### Rust Traps / Rust 陷阱

```rust
// ❌ Trap R1: Unbounded collect() on huge iterators / 无界collect()
let all: Vec<_> = huge_file.lines().collect();  // OOM risk!
// ✅ Correct: use iterators lazily / 惰性迭代
for line in huge_file.lines() { /* process one */ }

// ❌ Trap R2: Clone in hot loop instead of borrow / 热循环中clone而非借用
for item in items.clone() {  // unnecessary clone
// ✅ Correct:
for item in &items {  // borrow instead
```

### Go Traps / Go 陷阱

```go
// ❌ Trap G1: Loop variable capture in goroutines / goroutine闭包捕获循环变量
for _, item := range items {
    go func() {
        process(item)  // BUG: all use last item!
    }()
}
// ✅ Correct / 正确:
for _, item := range items {
    item := item  // capture per iteration
    go func() {
        process(item)
    }()
}

// ❌ Trap G2: Nil interface != nil concrete type / nil接口 ≠ nil具体类型
var p *MyStruct = nil
var i MyInterface = p
if i != nil {  // BUG: true! Interface is non-nil with nil concrete
```

### Detection Rule / 检测规则

When opening a project file for modification:
1. Detect file extension → activate corresponding language trap checklist
2. `.py` → check P1/P2/P3 | `.rs` → check R1/R2 | `.go` → check G1/G2
3. `.js`/`.ts` → standard Traps A/B/C (Layer 3) still apply
4. Unknown language → skip multi-stack check, but still apply universal Principles

---

## Progressive Activation by Change Size / 按改动大小分层激活 (V2.7 NEW)

> Not every change needs the full three-layer discipline. Match depth to change impact.
> 不是每次改动都需要三层全开。按改动影响面匹配合适的深度。

```
Change size assessment / 改动规模评估:
  ├── ≤ 3 files + ≤ 30 net lines → L1 Lightweight / 轻量
  │   Execute: Pre-Gate 1 (Three Questions) + Principles 1-5 (skip full Gate 2/3)
  │   执行：前置门1（三问三答）+ 原则1-5（跳过高开销的门2/3）
  │
  ├── 3-10 files OR involves routes/data-flow → L2 Standard / 标准
  │   Execute: All 3 Pre-Gates + All 6 Principles + All 3 Traps
  │   执行：全部前置门 + 全部六大原则 + 全部三大陷阱
  │
  └── > 10 files OR new feature/refactor → L3 Full / 完整
      Execute: Full L2 + Intent Anchor Pre-Judgment explicit output required
      执行：完整L2 + 意图锚点预判必须显式输出
```

**L1 skip rules / L1 可跳过**: Gate 2 (Repeat Bug — not relevant for tiny fixes), Breadcrumb scan (small change rarely affects coupling)
**L2 minimum**: All gates + principles + traps must run. User can upgrade to L3 manually: "用完整L3"
**L3 required**: New feature dev, architecture refactor, cross-module changes

---

## Summary Checklist / 总结检查清单（Run Through Before Outputting Code / 输出代码前逐项检查）

```
□ Gate 1 — Three Questions / 三问三答: Full call chain? All branches? Unified fix or patch?
□ Gate 2 — Repeat Bug / 重复Bug: Fixed 2+ times already? → Search first, don't code
□ Gate 3 — File Size / 文件大小: Target file >300 lines? New feature needs new file?
□ Principle 0 — 🍞 Breadcrumb Pre-Scan / 面包屑预扫描: Open file → scan header → parse @COUPLED/📖
□ Principle 1 — Think First + Intent Anchor Pre-Judgment / 先思考+意图锚点预判: What tags will I need?
□ Principle 2 — Subtraction First / 做减法: Can I delete code instead of adding?
□ Principle 3 — Keep It Simple / 保持简单: Minimal changes, no over-engineering
□ Principle 4 — Precise Modification / 精准修改: Only target code, confirm all branch paths
□ Principle 5 — Goal-Driven / 目标驱动: Will it run? Verify immediately → close loop
□ Trap A — Falsy Coercion / 假值强制: Using `||` on numeric values?
□ Trap B — Select Fake-Selection / Select假选中: `<select>` has placeholder option?
□ Trap C — POST-as-UPSERT: UPDATE branch reads from `req.body`?
```

---

## Appendix: Classic Patch Anti-Patterns Quick Reference / 附录：经典补丁反模式速查

The following are typical patch anti-patterns extracted from real projects. Alert immediately when encountering similar patterns.
以下是从真实项目中提取的典型补丁反例，遇到类似模式立刻警觉。

| # | Pattern / 模式 | Lesson / 教训 |
|:--|:--|:--|
| 1 | Same bug fixed 3+ times, all failed / 同一个Bug改3次以上全失败 | Fix 2 times → search online (it's likely a known OS/framework-level issue) / 修2次不好就上网搜 |
| 2 | Fix crosses session boundaries, new session forgets context / 修复跨会话边界，新会话忘记上下文 | Trace the COMPLETE call chain, not just the current data stream / 追踪完整调用链 |
| 3 | Adding a "safety check" function at wrong call site → global breakage / 在错误位置加"安全检查"→全局崩溃 | Never call safety functions when the guarded object doesn't exist / 零对象时禁止调用防护函数 |
| 4 | Changed one entry point's HTML, forgot another / 改了入口A忘改入口B | Multi-entry projects: script/style tags must sync across all entry files / 多入口必须同步 |
| 5 | After splitting files, functions break because of missing bridge connections / 拆文件后函数崩溃 | After splitting, verify all cross-module bridges (imports, exports, call chains) / 拆分后验证跨模块桥接 |

---

## Related Skill Orchestration / 关联Skill编排

This Skill is the **first link** in the Vibe Coding Rules pipeline / 本Skill是流水线的**第一环节**:

```
coding-principles ← This Skill (pre-code mandatory) / 本Skill（改前强制）
    ├── Layer 1: Pre-Gates (Three Questions + Repeat Bug + File Size)
    ├── Layer 2: Six Principles (🍞 Pre-Scan → Think First → Subtraction → Simple → Precise → Goal-Driven)
    ├── Layer 3: Three Traps (|| falsy / select fake / POST hardcode)
    ↓
safe-terminal-executor (if API verification needed) / 如需API验证
    ↓
Write/Modify Code / 写/改代码
    ↓
self-check (28 rules + trust tiers + four-hop chain + 🛑 integrity gate V2.6 + 🍞 auto-seeding) / 自检
    ↓
web-testing (browser automation: DOM + screenshot + OCR, mandatory when gate passes) / 自动化测试
    ↓
changelog (change log + growth detection + anti-bloat) / 变更日志
    ↓
git commit / 自动存档
    ↓
✅ Delivery Closed Loop / 交付闭环
```

## Sources / 参考来源

Inspired by observations from the AI coding community on how AI-assisted programming changes development workflows.

- Community reference: https://x.com/karpathy/status/2015883857489522876
- Related project: https://github.com/forrestchang/andrej-karpathy-skills
