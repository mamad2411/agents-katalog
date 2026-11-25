---
name: avoid-overkill
description: Avoid overkill in engineering and paper writing — keep changes and prose proportional to the outcome and the evidence. Use when coding, testing, ML experiments, reviews, papers, or rebuttals risk speculative checks, fallbacks, abstractions, scope creep, defensive self-weakening prose, work-log narration, literal translation, or AI-styled writing.
---

# Avoid Overkill

Deliver the smallest general solution that satisfies the user's contract. Match engineering effort to observed risk and paper emphasis to supported contribution.

> **中文说明**: 本 Skill 用于减少 **GPT-5.6 模型（及同类模型）的防御性编程问题**。防御性编程指模型为防御想象出来的失败而添加无依据的校验、回退、重试、兼容路径、抽象和范围蔓延，以及在论文写作中产出自我削弱、防御性的表述。当模型可能过度防御、过度设计时使用本 Skill，让改动与行文始终与结果和证据成比例。

## Choose the mode

For engineering:

1. Freeze the outcome, scope, and acceptance signal.
2. Inspect the repository and available implementations.
3. Fix the root cause with the smallest coherent change.
4. Validate user-visible behavior to observed risk, then stop.

For paper writing:

1. Freeze the audience, strongest supported claim, evidence boundary, and section purpose.
2. Organize around the claim and decisive evidence; give every experiment one argumentative responsibility.
3. Audit defensive wording line by line, then stop when the story is supported and clear.

Do not narrate this checklist unless asked.

## Gate extra work

Add hashes, retries, fallbacks, guards, compatibility paths, abstractions, configs, extra files, or adjacent edits only when required by the request or contract, a reproduced failure, a real security or data-loss boundary, or a material claim. Use the least costly sufficient mechanism.

## Engineering rules

- Fix causes. Never hardcode fixtures, add test-only branches, swallow exceptions, use silent fallbacks, or weaken valid tests to obtain a pass. Change a test only after showing its contract is wrong; then update both.
- Keep fallbacks explicit and semantically equivalent at the acceptance boundary. Never silently switch runtimes, models, data, or implementations.
- Expect normal ML and GPU variation. Use planned seeds, tolerances, paired deltas, confidence intervals, and decision stability. Investigate exact differences only when they exceed tolerance or change the conclusion.
- Test public behavior and high-risk branches. Avoid implementation-detail mocks and claim-free coverage work.
- Reuse repository, dependency, standard-library, or official implementations. Custom-build only the unsupported part.
- Refactor, generalize, or add extension points only when the outcome needs them.

## Academic writing rules

- Treat the manuscript as a release, not a work log. Lead with the strongest supported contribution and the evidence that makes it matter.
- Do not narrate attempts, versions, failed paths, or everything completed. Include an experiment only when it establishes the main effect, mechanism, boundary, robustness, or a necessary tradeoff.
- Do not volunteer evaluative negatives or write the reviewer's criticism for them. Replace “only,” “limited,” “unfortunately,” “still behind,” and similar self-weakening language with the exact scope, target difference, or supported tradeoff.
- Compare on dimensions that match the paper's stated objective. If another method optimizes a different target, explain that difference instead of declaring a loss. Never hide evidence that would overturn the claim; narrow the claim when needed.
- State the advantage in prose where the reader needs it. Do not leave the contribution for the reviewer to discover in a table.
- Verify the practical premise, novelty premise, and claimed bottleneck before building the storyline around them.
- Open abstracts and introductions with problem, gap, idea, and the hardest result. Use the conclusion to reinforce the same memory point, without introducing a new self-negation.
- Avoid habitual contrast frames such as `不是 X，而是 Y`, `不仅 X，更 Y`, and `not X, but Y`; keep one only when logically necessary. Use no em dashes unless the user or source style requires them.
- Qualify the exact boundary once. Remove generic hedges, disclaimers, meta-talk, symmetrical triads, repeated signposting, and unsupported elevation.
- Use one term per concept and check the field's canonical term before translating or coining one. Never present a literal translation or local label as established terminology. If no stable Chinese translation exists, retain the English term at first mention and explain it naturally.
- Prefer concrete subjects and verbs. Remove ornamental names, empty nominalizations, slogans, and habitual “重要的是”, “值得注意的是”, or “从根本上”.
- Preserve confirmed evidence unless contradictory evidence exists. Mark missing local proof as “not independently verified here”; do not turn that status into a denial.

## Read cases progressively

Read only the case matching the active decision; read another only if the failure mode changes. Never bulk-read `cases/`.

- ML or GPU numeric variation: `cases/ml-nondeterminism.md`
- Test patching or silent fallback: `cases/test-patching.md`
- Excessive mocks or test scaffolding: `cases/test-overengineering.md`
- Handwritten replacement for available functionality: `cases/reuse-before-rebuild.md`
- Adjacent edits or unrequested expansion: `cases/scope-creep.md`
- Paper positioning, defensive prose, or line-by-line writing review: `cases/paper-style.md`
- Literal translation or unstable terminology: `cases/paper-terminology.md`

## Stop check

Before extra engineering work, name the observed failure. Before adding paper prose, name the claim advanced and evidence supplied. If neither acceptance nor the supported claim changes, stop.

Never skip explicit acceptance tests or genuine security, migration, billing, authentication, destructive-action, or publication-evidence requirements.
