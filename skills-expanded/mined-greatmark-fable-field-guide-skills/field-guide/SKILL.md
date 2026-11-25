---
name: field-guide
description: >-
  Master index for the fable field-guide family (8 finding-unknowns skills):
  routes to the right skill and defines the artifact contract they share.
  Use when the user says "field guide", "which of these skills",
  "该用哪个 skill", "这套流程怎么用", "finding unknowns 工具怎么选", asks
  which of these skills applies or how the family fits together, or is stuck
  and can't say what they need — "不知道从哪下手", "where do I even start",
  "你都会什么", "装了哪些技能"; also read when unsure which finding-unknowns
  skill fits the current situation.
---

# Field Guide

Route by the unknown blocking the user right now, then read and follow that
skill. Unsure which: three quick questions — unfamiliar ground? decisions only
the user can make? needs to see something? Enter at the current stage (an
outside plan or spec counts as approved); don't re-run earlier stages. When
several rows apply, drop rows their "Not for" clauses reject; take the earliest
stage neither done nor explicitly skipped by the user (done: approval words,
an artifact, or time phrasing — never route backwards past completed work).
design-directions vs reference-hunt: a fork, not a sequence. Chained requests
run each stage in order — never silently drop later parts. Mis-routed? Switch
— "Not for" clauses decide; keep anything produced.

## Routing table

| Stuck on | Skill |
| --- | --- |
| Nothing — no unknown blocks it; small task, clear path (没有未知数阻塞的小事) | none — just do the work |
| Unfamiliar area before starting; hidden pitfalls (unknown unknowns; 开工前不熟悉、怕有暗坑) | blindspot-pass |
| Known ambiguities the user must decide (known unknowns; 已知模糊点要用户拍板；"有不确定可以问我"不算) | interview-me |
| Can't say what they want but would recognize it; no concrete reference (说不出想要什么、看到能认出、无参照物) | design-directions |
| Has a concrete reference: "make it like that" (有具体参照物、要像它那样) | reference-hunt |
| Discussion converged, ready to build; reviewable plan first (讨论收敛要动手、先出可评审方案) | implementation-plan |
| Implementing an approved plan (按批准的方案实现中) | implementation-notes |
| Verify your own understanding of this change set before merging (合并前验证自己真懂、怕有没看出来的坑) | change-quiz |
| Quiz failed on a real defect (quiz 暴露实现有误) | fix + log in implementation-notes, re-quiz; plan wrong → implementation-plan |
| Persuade or explain to others after the work (说服不在环内的评审者、跟团队讲清楚这次改动；纯科普不算) | pitch-explainer |

## Artifact contract (every skill in this family follows it)

- `interview-decisions.md`, `porting-checklist.md`, `implementation-plan.md`,
  `implementation-notes.md`, `change-report.html`, `pitch-<topic>.html` live
  in the project root (in a monorepo: the affected package's root);
  prototypes live in `./design-directions/`. Parallel tasks: append a titled
  section (notes) or suffix the filename with a task slug.
- Never commit artifacts unless the user explicitly asks (change-report.html:
  never); exclude them via each member skill's worktree-safe command; if that
  write fails, fall back to leaving them untracked and tell the user.
- Artifacts are caches: if one is lost, rebuild it from the session history
  or rerun its skill — never block on a missing artifact.
- Artifacts are written in the language of the conversation (pitch may
  follow the reviewer's language).
