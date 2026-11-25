---
name: gauntlet-loop
description: >-
  Domain-agnostic method for producing top-tier work with the Gauntlet Loop —
  split → build → blind-critic → repeat — against a hard "bar" the agent cannot
  argue its way around. A lead splits a goal into independently gradeable parts;
  each part gets a specialist builder plus a ruthless blind critic (clean
  context) who inspects the REAL artifact and only passes it when it beats the
  bar. Use for ANY kind of work: coding, writing, design, data analysis,
  research, prompt/agent evaluation, blue-team detection engineering. On
  invocation, identify the work type and read the matching file in
  references/domains/ for how to pick the bar plus a checklist and worked
  example. Trigger keywords: "gauntlet loop", "iterate to a high bar",
  "build-critic loop", "builder critic", "make this world-class", "beat a
  reference", "test-as-bar", "eval-as-bar", "blind A/B", "write a detection
  rule", "keep looping until it's great". For security
  vulnerability hunting use the separate security-vuln-gauntlet skill.
---

# Gauntlet Loop — core skill (domain-agnostic)

A disciplined loop for producing high-quality work in **any** domain: **build → blind critique → revise → repeat**, against a bar the agent cannot talk its way past. Coding, writing, design, data, research, prompt engineering and detection all use the *same* loop — they differ only in **how you pick the bar**, **what the critic inspects**, and **the checklist**. Those live in `references/domains/`.

> **Origin:** the Gauntlet Loop method is **Matt Shumer's**, from *"How to Run a Gauntlet Loop"* (https://somethingbig.ai/gauntlet-loop), with the companion repo `mshumer/Claude-of-Duty`. This skill is an independent, attributed adaptation — see `../../CREDITS.md`.

## Prerequisite: a real agent harness

This loop **requires an agentic harness** that can open files, run code, render output, take screenshots, call tools, and **spawn sub-agents with their own clean context** (Claude Code, Cowork, Codex, or equivalent). A single-turn chat cannot produce an independent blind critic — if you can only reply in one context, say so and fall back to a single self-review pass instead of pretending the loop ran.

For large multi-agent runs, use the harness's parallel-agent facilities (in Claude Code: sub-agents, or `/ultracode` when available).

## The four pillars

1. **A bar the agent cannot argue around.** The strongest form: the artifact must **match or beat something real** — a reference implementation, a test suite, a top product's screenshot, a model essay, an eval set, an ATT&CK technique, a working PoC. The bar may be *aspirational*: it does not have to be realistically reachable. An unreachable bar keeps the loop pulling upward instead of stopping at "good enough".
2. **Give the goal, not the implementation.** State what the finished thing must achieve; let the agent choose the route. Prescribing architecture replaces the model's judgment with yours and caps the result at your imagination.
3. **Let the agent split the work.** The lead breaks the goal into the smallest pieces that can be **improved and graded independently**. Independent pieces can run as parallel loops.
4. **The builder never grades itself.** The builder and the judge are different agents with **separate context**. The critic is blind to the builder's reasoning and inspects the **real artifact** — running code, rendered pixels, actual test output — never the builder's summary.

## First step when this skill loads

1. **Identify the work type.**
2. **Read the matching domain file** for how to choose the bar, what the critic must inspect, and a worked example:
   - Code / refactor / library / feature → `references/domains/coding.md`
   - Essays, docs, messaging, marketing copy → `references/domains/writing.md`
   - UI / visual / landing pages → `references/domains/design.md`
   - Analytics, metrics, modeling → `references/domains/data-analysis.md`
   - Literature / market / competitive research → `references/domains/research.md`
   - Prompts, agents, skills, LLM features → `references/domains/prompt-eval.md`
   - SIEM/EDR detection rules (blue team) → `references/domains/detection.md`
   - Anything else → the generic frame below plus `references/choosing-the-bar.md`
3. **Read `references/running-the-loop.md`** for orchestration mechanics: budget, parallelism, the progress workbench, and the final smoothing pass.
4. Run LEAD → BUILDER → CRITIC as described.

> Hunting **security vulnerabilities** is a special case with different triggers and mandatory safety rules → use the separate `security-vuln-gauntlet` skill.

## The three roles (never share context)

- **LEAD (orchestrator).** Sets the bar and the loop budget, splits the goal into gradeable units, routes FAILs back, merges results. Does **not** build — an agent that built something is a biased judge of it.
- **BUILDER (specialist, clean context).** Builds one part for real and produces an **artifact**. Allowed to be imperfect. Never declares PASS.
- **CRITIC (blind, separate clean context).** Never sees the builder's reasoning. Inspects the artifact against the bar, demands objective evidence, and passes only when the bar is met. See `references/critic-design.md`.

## The loop

1. **Set the bar and the budget.** Concrete, measurable, ideally *beat this specific real thing*. If no reference is obvious, the first job is: **"find a concrete comparison or measurement"** — do not start building against a vague target. See `references/choosing-the-bar.md`.
2. **Split (LEAD).** List the smallest units worth grading separately (by component, by flow, by quality dimension). Independent units → parallel loops.
3. **Build (BUILDER × N, parallel, clean contexts).** Each builder produces a real artifact.
4. **Critique (CRITIC, blind).** The critic inspects the real thing, grades each bar criterion with evidence, and returns PASS/FAIL plus specific fixes. Blind A/B against the reference whenever the domain allows.
5. **Fix and repeat.** Feed FAILs back with the critic's reasons. **Run longer than feels necessary** — most people stop several rounds too early. Split hard parts further; try variants.
6. **Smooth (optional but recommended).** One fresh agent inspects the whole assembled result and fixes inconsistencies between separately-improved pieces. It harmonizes; it does not redesign.
7. **Report.** Final artifact + the bar used + a round log + PASS evidence + anything still under the bar.

## Stopping

The bar may be unreachable by design, so "bar met" is not the only stop condition. Stop when **any** of these holds:

- every unit clears the bar; **or**
- two consecutive rounds produce no improvement against the bar; **or**
- the loop budget (rounds, time, tokens) is exhausted.

Always record what is still below the bar. If the work is still visibly improving and budget remains, keep going.

## Monitoring without interrupting

Long runs are worth watching, but stopping to ask for status costs a round. Have the loop maintain a **live progress workbench** — a `workbench.md` or a self-refreshing HTML page — updated after each round with: current round, per-unit PASS/FAIL, the critic's evidence, and links to the latest artifacts/screenshots. Read it asynchronously; intervene only when the loop is stuck on the wrong thing.

## Why this beats one-shot work

| One-shot | Gauntlet Loop |
|---|---|
| Builder decides it's "fine" | Blind critic inspects the real artifact and only passes against the bar |
| Vague standard | Concrete bar tied to a real reference |
| Stops at good enough | Keeps looping while it improves |
| Confirmation bias | Builder and critic kept in separate contexts |

## When NOT to use this

The loop costs many times the tokens and wall-clock of a single pass. Skip it for small, low-stakes, one-off work (quick answers, throwaway scripts, a one-line fix). Use it when quality genuinely matters and you can name something real to be measured against.

## Expected output

Final artifact that clears (or best-approaches) the bar, plus: the bar definition, a round log (what FAILed → what changed), objective PASS evidence (test results, blind A/B outcome, recomputation, screenshots, PoC), and remaining gaps.

## References
- `references/methodology.md` — the full method and its rationale.
- `references/running-the-loop.md` — orchestration: budget, parallelism, workbench, smoothing pass.
- `references/prompt-templates.md` — LEAD / BUILDER / CRITIC / SMOOTHER prompts + meta-prompt.
- `references/choosing-the-bar.md` — how to pick a bar per kind of work.
- `references/critic-design.md` — designing a blind critic that inspects reality.
- `references/domains/coding.md` — software (reference implementation / test-as-bar).
- `references/domains/writing.md` — writing (model text, blind A/B).
- `references/domains/design.md` — UI/visual (blind A/B against top products).
- `references/domains/data-analysis.md` — analysis (correct + robust + reproducible).
- `references/domains/research.md` — research (source-verified, no fabricated citations).
- `references/domains/prompt-eval.md` — prompts/agents/skills (eval-as-bar, head-to-head).
- `references/domains/detection.md` — detection engineering (ATT&CK + zero false positives).
