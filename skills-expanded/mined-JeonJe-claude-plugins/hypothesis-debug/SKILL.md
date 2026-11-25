---
name: hypothesis-debug
description: 장애·버그를 경쟁 가설(≥2)과 반증 시도로 좁혀가는 체계적 트러블슈팅. 코드로직/환경데이터/측정오류 3레인 가설 생성, 판별 프로브, 5-why 세로 하강, 회귀 방지 1:1 매핑 포함. 장애 분석, 원인 조사, 트러블슈팅, "왜 안 되지" 디버깅 시 사용.
---

# Hypothesis-driven debugging

Force a systematic path from symptom to root cause: facts-only intake → parallel evidence collection → competing hypotheses (≥2) with mandatory falsification → discriminating probe → report with regression prevention. Never "just try a fix" on a guess.

## References index

| File | When to read |
|---|---|
| [references/hypothesis-lanes.md](references/hypothesis-lanes.md) | Phase 3 — building the competing-hypothesis set; Phase 4+ — 5-why vertical descent |
| [references/troubleshoot-report-template.md](references/troubleshoot-report-template.md) | Phase 5 — report skeleton |

## Phases

### 1. Intake — facts only

Record: symptom in one line; when it started; affected scope (users/requests/time window); what changed recently (deploys, config, data); **and explicitly, what is NOT yet known**. No hypotheses at this phase — an early guess anchors the whole investigation.

### 2. Parallel evidence collection

Collect from every available source in parallel, read-only: application/error logs, DB state (read-only queries), metrics/APM, reproduction attempt in a safe environment. Label each finding with its source and timestamp. Time-zone discipline: convert all timestamps to one zone before correlating — mixed-zone timelines fabricate causality.

### 3. Localize + hypothesize (competing, ≥2)

Read [hypothesis-lanes.md](references/hypothesis-lanes.md). Draw at least one hypothesis from each of the three lanes — code logic / environment & data / measurement error — so a single fixation cannot capture the investigation. For each hypothesis maintain:

| Hypothesis | Evidence for | Evidence against | Discriminating probe | Status |
|---|---|---|---|---|

**Mandatory falsification**: for the leading hypothesis, actively look for evidence that would disprove it before promoting it. A hypothesis you never tried to kill is not confirmed.

### 4. Probe loop

Design the cheapest probe that discriminates between the top hypotheses (a log line, a targeted query, a minimal reproduction). Run it, then promote or falsify. Repeat until one hypothesis survives with direct evidence. If the same probe fails twice, stop gathering more of the same logs — restate hypothesis/observation/next-probe in three lines and pick a different check.

When the proximate cause is confirmed but "why did that state occur" is still open, descend vertically with 5-why (see hypothesis-lanes.md §5-why): each "why" step closes on evidence, not conjecture, and stops at the last controllable leaf.

### 5. Report

Use [troubleshoot-report-template.md](references/troubleshoot-report-template.md): timeline, root cause with evidence, impact analysis, and recommended actions in three tiers — immediate mitigation / root fix / **regression prevention mapped 1:1 to each root-cause leaf** (a prevention attached to a symptom only papers over it).

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Fix on the first plausible guess | Competing hypotheses + discriminating probe |
| All hypotheses from one lane | Force one per lane (§3) |
| Correlating mixed-timezone logs | Normalize to one zone first |
| "It stopped reproducing" → close | Explain why it stopped, or track as unresolved flake |
| Writing to prod state during investigation | Read-only evidence collection; mitigation is a separate, approved step |
| Same failing probe repeated | 3-line restate + a different verifiable check |
