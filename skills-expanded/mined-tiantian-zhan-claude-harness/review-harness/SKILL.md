---
name: review-harness
description: Audit a project's harness (CLAUDE.md + supporting docs) against current code and git activity, and catch lifecycle/hygiene drift (completed work stuck in active/, stale or silently-parked plans, executed-runbook/dead-spec sections needing a tombstone, date-patch stacking, index↔directory drift, broken links or clickable links into a gitignored archive, status metadata contradicting the body, phantom-audience docs, double graveyards). Produces a markdown report only — never edits files. Use after a milestone, after a major line closeout, on a monthly cadence, or when the user runs /review-harness. Works in any repo with harness-shaped docs.
allowed-tools: Read, Grep, Glob, Bash(git log:*), Bash(git diff:*), Bash(git status:*), Bash(find:*), Bash(wc:*), Bash(ls:*), Bash(grep:*)
---

# review-harness

Audit whether the harness still matches reality, and whether it's drifting structurally. **Never edit during review** — produce a report; the user approves changes in a follow-up.

This skill is the harness's **slow lane** — it catches what a machine gate can't: stale prose, structural drift, second-source rot. Mechanically checkable invariants (counts, lifecycle moves, link validity) belong in a **deterministic CI / pre-commit gate**, not a periodic human review — so part of this review's job is to spot invariants caught *only* here and **recommend gating them** (derive-from-code + `git diff --exit-code`) so they stop recurring. Run on a cadence (`/schedule`) or after each milestone — output should be issue/PR-ready. *(A project with no gate yet: this review is the primary catch until one exists.)*

## When to invoke

- After a milestone / exec-plan / phase · after a major architectural change · on a periodic schedule · when the user types `/review-harness`.
- **Default cadence: monthly + after each major line closeout.** Weekly mechanical drift should be a CI cron (e.g. LinkPea's `weekly-harness-check.yml`), not this review — this is the slow lane for what machines can't judge. (2026-07-15 定,文档整治批次 D)

## When NOT to invoke

- Mid-task (context still changing) · right after `/bootstrap-harness` (nothing to audit) · a single one-off fix (just make it).

---

## Steps

### 0. Find the previous review report (追账前置)

Look for the most recent prior report (convention: `docs/archive/reviews/*harness-review*.md`, else ask git log / the user). If one exists, its **"Suggested next actions" become this report's opening accountability section** (see format). This is the loop-closing mechanism — 2026-07-05 的审计有 3 条药方悬空,10 天后长成全仓糜烂,就是因为没有这一步。

### 1. Discover harness files (don't hardcode)

```bash
ls CLAUDE.md AGENTS.md GLOSSARY.md README.md 2>/dev/null
find . -maxdepth 1 -name '*.md' -type f
find docs -type f -name '*.md' 2>/dev/null
ls docs/exec-plans/active/ docs/exec-plans/completed/ docs/exec-plans/archive/ 2>/dev/null
```

Read whatever exists — projects have different subsets (Seed / Standard / Full).

### 2. Scan current state

```bash
git log --oneline -20
git diff HEAD~5 --stat 2>/dev/null
git status --short
# code size — infer source dir from package.json / pom.xml / go.mod / pyproject.toml, then count *.ts/*.py/*.java/*.go
```

### 3. Compare harness claims vs reality — and run the hygiene checks

**Content drift (semantic — read and judge):**
- **Still accurate?** Does a listed command still work? Does a doc describe a module / count / phase that changed (e.g. "7 capabilities" when the code has 15)?
- **Missing?** A pattern in recent commits reflected nowhere.
- **Prose-as-second-truth (high priority).** Any prose doc duplicating something code / tests / ADRs already own (capability list, schema, phase status, counts)? If its copy now contradicts reality, that's the rot — flag it and name the contradiction. Fix is usually "delete the stale/duplicated part, link to the authoritative source," not "update both copies."
- **Retirement candidates(该退役的正文).** One-shot content whose job is done but still occupies the body: executed runbooks, superseded/dead specs, finished checklists, migration logs. Signal phrases: 「已执行」「留档」「勿重跑」「供考古」, "executed on", "kept for the record", "do not re-run". Fix = compress to a **tombstone line** (✅ + date + one-line pointer), delete the body, keep the heading so old references don't dangle — git history is the archive. Same family: **date-patch stacking** — ≥2 "⚠️ updated YYYY-MM-DD" blocks in one file instead of folding facts into the section.
- **Metadata vs body contradiction.** A status line / date that disagrees with the content: an ADR marked `Accepted` whose body says it was overturned (status should use a controlled vocab: Accepted/Superseded/Proposed/Deprecated/Amended); a top-of-file "draft <old date>" on a doc rewritten since; a plan status 🔄 with every box checked. Agents trust metadata first — a wrong status line poisons decisions downstream.
- **Phantom-audience docs.** Onboarding flows, role matrices, CODEOWNERS teams, collaboration process written for readers that don't exist (e.g. a solo+agents repo with a 5-person team workflow). Fix = delete, or compress to the real audience.

**Lifecycle & hygiene drift (mostly mechanical — grep / ls):**
- **Completed stuck in `active/`** — any `active/<plan>.md` marked `✅`/done/完成 but never moved to `completed/`. (The single most common rot: ✅ feels done, the move gets skipped.)
- **Stale / silently-parked active plans** — an `active/` plan with no commit in >21 days (adjust to project cadence) whose status line isn't explicitly 📌 (standing) or ⏸️ (parked); and any ⏸️ **without a `Revisit:<condition|date>`** — a park with no revisit is an unbounded sink. Three exits: push it, park it explicitly, or move it out.
- **Byproducts in `active/`** — rendered `.html`, reports, design variants sitting in `active/` instead of `archive/`.
- **Broken / dangling links** — tracked `.md` linking to a file that's missing.
- **Archive fake links** — tracked `.md` markdown-linking into a gitignored/local-only archive: clicks fine on this machine, 404s in every clone. Distinct fix from broken-link: **inline the 3-5 line conclusion, keep the path as backtick text + "local archive" note** — do NOT suggest committing the archive target.
- **Completed index drift** — `completed/<plan>.md` files missing from the index README, or index rows pointing at files that don't exist. Check BOTH directions (an unwatched completed index drifted twice in 10 days).
- **Double graveyard** — two or more archive areas (e.g. `docs/archive/` AND `docs/exec-plans/archive/`) → byproducts scatter, references split; merge to one.
- **Cross-doc duplication** — the same block (project-essence, pitfalls, phase table) maintained in 2+ docs with no link → one will rot.
- **Ungated invariant** — for EVERY mechanical finding above, the first question is **"can this become a gate?"** (a CI assert, a two-way index check, a link walker, a status-vocab regex). Ten days of natural experiment: every CI-gated invariant stayed correct, every ungated prose area rotted. Only what needs semantic judgment belongs in this slow lane — recommend gating the rest and mark each finding *gateable* / *slow-lane-only*.

**Graduate / dead:**
- **Graduate candidate** — a `docs/lessons.md` entry referenced in ≥2 places → propose promoting to a CLAUDE.md hard rule.
- **Dead** — a file nothing links to AND no recent edit → archive candidate.

### 4. Output this report format

```markdown
# Harness Review (<YYYY-MM-DD>)

## 🧾 上轮药方兑现状态(REQUIRED first section when a prior report exists)
> 上轮 = <path of previous report>(<date>)。逐条对账,没吃完的药就是下一轮的病。
- <上轮 action 1> → ✅ 已做(<PR/commit>) / ❌ 没做(→ 本轮重开或说明) / 🚫 不做了(<原因,一句话>)
- (首轮无上轮报告 → 写「首轮,无药方可对」)

## 📊 Stats
- CLAUDE.md (or AGENTS.md): N lines (**hard limit < 60**; if over, the ⚠️ section MUST give concrete slimming moves)
- Total harness files: N · Active exec-plans: N · Completed: N · Open tech debt: N
- Lessons total / since last review: N / M · Source files: N (<ext>)

## ✅ Still accurate (spot-check)
- `<file>`: <one-line confirm>

## 🧹 Lifecycle & hygiene  ← the mechanical drift this review exists to catch
- **✅-stuck-in-active**: `active/<plan>.md` marked done → should be in `completed/` (or "none")
- **stale-active / parked-no-revisit**: `active/<plan>.md` — N days no commit, status not 📌/⏸️ | ⏸️ missing `Revisit:` (or "none")
- **byproduct-in-active**: `active/<x>.html` → should be in `archive/` (or "none")
- **broken-link**: `<file>:<line>` → missing `<target>` (or "none")
- **archive-fake-link**: `<file>:<line>` → clickable link into gitignored `<archive path>` → inline conclusion + backtick path (or "none")
- **completed-index-drift**: `completed/<x>.md` not in index / index row without file (or "none")
- **double-graveyard**: `<dir A>` + `<dir B>` both archive areas → merge (or "none")

## 🪦 Retirement candidates(执行完该退役的正文)
- `<file>` §<section>: executed/dead content still in body (signal: <"已执行"/"do not re-run"/…>) → tombstone line (✅+date+pointer), delete body, keep heading
- date-patch stacking: `<file>` — N "⚠️ <date>" blocks → fold into sections, retire stale ones (or "none")

## ⚠️ Needs update
- `<file>:<line>`: <what's stale> → <precise old → new>
- metadata-contradiction: `<file>`: status/date says <X>, body says <Y> → fix the status line (controlled vocab), not just the prose

## 📝 Missing in harness
- <observed in code/git> → <which file/section should hold it>

## 🔁 Duplication / consolidation
- `<A>` and `<B>` both state Z (no link) → keep in <authoritative>, link from the other

## 🚦 Gate candidates (move from slow lane → CI)
> 每类机械发现先问「能不能变成一道门」;答不出「为什么不能」的,就该提门。
- `<invariant>` → **gateable**: `<assert sketch — e.g. two-way index check / link walker / status-vocab regex / assert len(REGISTRY)==N / git diff --exit-code on generated docs>`
- `<finding>` → **slow-lane-only**: needs semantic judgment because <reason>

## 🎯 Promote from lessons
- `docs/lessons.md: <entry>` (referenced N times) → `CLAUDE.md` §<section>

## 💀 Dead / archive candidates
- `<file>`: no inbound link + no edit in N days → archive/delete
- phantom-audience: `<file>` written for readers that don't exist (<evidence — e.g. team workflow in a solo repo>) → delete or compress to real audience

## Suggested next actions (by ROI)
1. <action — which file, which section> ...
```

### 5. Save the report, then stop

**Write the report to the project's reviews archive** (convention: `docs/archive/reviews/<YYYY-MM-DD>-harness-review.md`; local-only/gitignored is fine) — the next run's Step 0 depends on it existing. Then do NOT apply changes to harness files. Wait for the user to approve, then they ask you to implement specific items.

---

## Constraints

- **No file edits during review** — Read / Grep / Glob / Bash (read-only) only.
- **CLAUDE.md hard limit < 60 lines.** If over, the ⚠️ section MUST give *specific* slimming moves (which block → table, which → GLOSSARY / linked doc, which boundaries to merge) — not just "too long."
- **Don't promote a lesson unless referenced ≥2 times** — avoid over-fitting to a one-off.
- **Be honest about ✅** — don't pad. If clean, 1-2 spot-checks suffice; write "none" in empty hygiene categories.
- **Report < 500 lines** — bucket low-priority items into an appendix if long.
- **Tie findings to business impact** — "the agent will make mistake X," not "it's untidy."
- **No new quantitative metrics** — don't introduce SLO numbers / coverage % the project deliberately omits.
- **Delta, not rewrite** — propose targeted edits; never suggest rewriting a doc wholesale (ACE: full rewrites cause context collapse).

---

## Anti-patterns

- ❌ Editing files during review (the whole point is propose-then-approve).
- ❌ Promoting every lesson (lessons are sediment, not a promotion queue).
- ❌ Suggesting full-doc rewrites instead of delta edits.
- ❌ Adding new quantitative metrics the project chose to omit.
- ❌ Hardcoding a fixed file list — use Step 1 discovery so this runs in any repo.
- ❌ Reporting hygiene categories as prose paragraphs — keep them as the grep-backed bullet lists above so they're scannable and actionable.
- ❌ Fixing an archive fake link by "commit the archive target" — the archive is local by design; the fix is inline-the-conclusion + backtick path.
- ❌ Recommending "keep for archaeology" — git history IS the archive; executed/dead content gets a tombstone line, not a preservation layer.
