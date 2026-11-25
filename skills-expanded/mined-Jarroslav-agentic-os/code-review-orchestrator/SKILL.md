---
name: code-review-orchestrator
description: >-
  Resolves the SDLC code-review gate with a multi-lens review fan-out and
  persists one canonical verdict JSON as the hand-off back to gate-arbiter.
  Invoked inline (Skill tool) by gate-arbiter at gate ids `code-review.final`
  (full multi-lens pass after implementation evidence) and `code-review.check`
  (narrow re-check of prior blocking findings against a fix-up diff). Trigger
  when the router reaches "code review", "resolve the review gate", "run code
  review", "re-check the prior findings", or "verify the fix-up diff". Not for: direct user
  invocation (the router owns it) or ad-hoc reviews outside a managed pipeline
  (use code-review).
discoverable: false
license: Apache-2.0
version: 0.1.0
---

# code-review-orchestrator

Replace a single-pass review with a multi-lens orchestration. Materialize the
diff, gather project context, fan out three independent review lenses as
subagents, adjudicate standards and security against project guides, triage the
merged findings, and write exactly one verdict JSON. That file is the whole
hand-off: `gate-arbiter` reads it back and records the outcome.

> Blast radius: **R1**. The only file this skill writes is the verdict report.
> No source files. No broad test suites. No end-of-turn — control returns inline
> to `gate-arbiter`.

## Contract

| Field | Value |
| --- | --- |
| Gate ids | `code-review.final`, `code-review.check` |
| Output (`final`) | `<run_dir>/code-review-final.json` |
| Output (`check`) | `<run_dir>/code-review-check.json` |
| Diff reconstruction | `git diff <diff_base> -- . ':(exclude)package-lock.json'` |
| Finding IDs | `CR-001`, `CR-002`, … ; check-round new id = `max(existing CR number) + 1` |
| Verdict fields | `decision` (`approve`\|`request-changes`), `confidence` (`low`\|`medium`\|`high`), `risk_flags`, `business_review[]`, `standards_review[]`, `findings[]`, `rationale`, `finding_status` (check round only) |
| `finding_status` values | `resolved`, `unresolved`, `superseded` |
| triage buckets | `decision_needed`, `patch`, `defer`, `dismiss` |
| severity enum | `critical` \| `major` (no `minor`) |
| risk_flags examples | `security`, `breaking-change`, `public-api` |

Each `findings[]` entry carries a stable ID + a `triage` bucket + a `severity`.
`decisions.jsonl` is written by `gate-arbiter`, never by this skill.

## Inputs

`gate_id`, `original_task`, `artifacts` (ArtifactRefs), `prior_verdict`
(required on `code-review.check` — full verdict object OR readable ArtifactRef),
`memory_brief`, `run_dir` (effectively required; safe-fail if absent or
unwritable). Story path pattern: `docs/stories/<story>.md`.

ArtifactRef shape: `{"path": ..., "summary": ..., "signature": ...}`. Keys:
`story`, `spec` (`<run_dir>/design.md`), `git_workflow`, `code_quality`,
`security`, `prior_verdict` (`<run_dir>/code-review-final.json`). Acceptance
artifacts resolvable under `run_dir`: `design.md`, `requirements.md`, the story
file.

The review bundle (`review-bundle.json`) carries only metadata — `diff_base`,
`changed_files`, `diffstat`, `evidence_summaries`, `risk_flags`,
`artifact_refs`. It never carries the diff body. **You** materialize the diff.

## code-review.final — operating steps

1. **Materialize the diff.** Run
   `git diff <diff_base> -- . ':(exclude)package-lock.json'`. No `diff_base` /
   no diff / unwritable `run_dir` → safe-fail (below). If the diff is too large
   to review fully, degrade — do not pass: record the truncated coverage in
   `rationale` and force `confidence: "low"`.
2. **Load project context.** Read the guides that exist —
   `.agentic/guides/standards/git-workflow.md`,
   `.agentic/guides/standards/code-quality.md`,
   `.agentic/guides/development/security-patterns.md`, and any
   `.agentic/guides/**/*.md` — plus the project profile
   (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`). Absent guides invent no
   standards. A present-but-unreadable guide forces `confidence: "low"`.
3. **Fan out three lenses** (always as independent `general-purpose` subagents —
   never in orchestrator context; each dispatched at the **same model
   capability** as this session, no silent downshift). Inline the lens method
   from `references/review-lenses.md` and the return shape from
   `references/lens-output-formats.md` into each dispatch prompt; see
   `references/review-subagent-prompts.md` for the prompt scaffolds.
   - **Blind** — diff ONLY (no run context, no guides, no repo). Stays
     uninformed. Returns Markdown bullets.
   - **Edge-case** — diff + repo read access. Returns a JSON array.
   - **Acceptance** — diff + full inlined spec/story text. Dispatched whenever
     an acceptance artifact exists; if both `story` and `spec` exist, inline
     BOTH (concatenated, labeled). Returns a criterion-status list + findings.
4. **Triage** (per `references/triage-and-verdict.md`): normalize each raw
   finding (synthesize `problem` / `impact` / `recommendation`) → deduplicate
   across lenses (most specific wins, sources merged) → classify into exactly
   one bucket `decision_needed | patch | defer | dismiss` → drop `dismiss`
   (keep the count) → assign severity (`critical | major`) and derive
   `risk_flags`. Nominally-minor issues are dropped unless project rules make
   them blocking, in which case they become `major`.
5. **Adjudicate standards/security.** Each `standards_review` row is an audit
   record, not a decision. A `fail`/`partial` on a blocking standard MUST ALSO
   be raised as a finding (severity `major`; `critical` for security) to count
   toward the decision.
6. **Decide.** `decision = "request-changes"` if any of: a surviving `patch`
   finding is critical/major; any `decision_needed` finding exists; any
   required-AC `fail` OR `partial`; any concrete security issue; any blocking
   `standards_review` `fail` OR `partial`. Otherwise `approve`. `defer` and
   `dismiss` never block. `partial` blocks everywhere `fail` blocks.
7. **Persist** the verdict to `<run_dir>/code-review-final.json` per
   `references/verdict-schema.md`. Do not print it. Return inline to the router.

`findings[]` must NOT contain `defer` or `dismiss` findings — record their
counts in `rationale` only.

### final confidence

`low` when: no-spec round; any lens failed; acceptance failed despite spec
present; oversized/truncated diff; unreadable-but-present guide; persistence
failure; or any `decision_needed` finding remains. `medium` only when every
lens ran and exactly one returned thin-but-parseable output with no unresolved
ambiguity. Otherwise `high`.

**no-spec vs failed-acceptance** — both leave `business_review` empty, both set
`confidence: low`, but they are distinct: no-spec = no extractable criteria
(keep other findings); failed = a present-but-unreadable/unparseable spec
(record "acceptance failed" in `rationale`).

**Layer-failure** (some lenses failed): record the failed lens, keep the
surviving lenses' findings, force `confidence: "low"`.

## code-review.check — operating steps

Narrow blind + edge-case confirmation pass. Does NOT re-run the full fan-out —
no acceptance lens, no re-triage.

1. Obtain the fix-up diff via the same channel/order as final Step 1.
2. Re-check only the original **blocking** findings — bucket `patch` or
   `decision_needed`; a finding with NO `triage` annotation is treated as
   blocking. `defer` findings are never re-checked and never affect the
   decision. Per blocking finding ID set
   `finding_status ∈ resolved | unresolved | superseded`.
3. Scoped confirmation: you MAY dispatch blind + edge-case subagents on the
   fix-up diff ALONE to confirm a *suspected new* high-risk issue (security,
   public API, data loss, build/runtime break). A newly confirmed issue gets a
   fresh collision-safe id `CR-NNN = max(existing CR number) + 1` and
   `triage: "patch"`.
4. Carry `business_review` and `standards_review` forward from `prior_verdict`
   unchanged.
5. **Decide.** `request-changes` if: `prior_verdict` missing/unusable; any
   `finding_status` is `unresolved`; a new high-risk finding was added; or a
   suspected new high-risk issue could not be refuted. Otherwise `approve`.
   `superseded` does not block.
6. Persist to `<run_dir>/code-review-check.json` (include `finding_status`).
   Do not print. Return inline.

## Safe-fail (both rounds)

Return the canonical safe-fail verdict — `decision: "request-changes"`,
`confidence: "low"`, empty `risk_flags` / `business_review` / `standards_review`
/ `findings` (plus empty `finding_status` on check), `rationale` naming the
failure — when all lenses fail, dispatch is impossible, there is no diff, or
persistence fails. Never approve an unreviewed or unrecorded diff.

`code-review.check` additionally safe-fails when `prior_verdict` is absent OR
unusable (path-only unreadable ref, unparseable, or lacking a usable `findings`
array), OR no usable fix-up diff is obtainable. A prior verdict that reviewed
nothing (`request-changes` with no blocking findings) does NOT become a clean
check.

## Outputs

- Exactly one artifact: the verdict JSON at the round's path above.
- Optional single status line (never the verdict body), e.g.
  `Code review recorded → request-changes (CR-001); continuing the gate`.

## References

| Path | Use |
| --- | --- |
| `references/review-lenses.md` | Folded canonical lens methods (blind / edge-case / acceptance); inline into dispatch prompts. |
| `references/lens-output-formats.md` | Per-lens return shapes; inline alongside the method. |
| `references/review-subagent-prompts.md` | Dispatch prompt scaffolds for the three lens subagents. |
| `references/triage-and-verdict.md` | Step-4 triage flow and the decision rules. |
| `references/verdict-schema.md` | Field-level schema for the persisted verdict JSON. |

## Cross-refs

- `gate-arbiter` — caller; reads the verdict back, records to
  `decisions.jsonl` and `events.jsonl`, then runs the HITL `AskUserQuestion` or
  the autonomous decision + escalation rule.
- `sdlc-engine` (Phase 9 acts on approve/request-changes; commits the verdict
  alongside `spec.md`/`plan.md`) and `sdlc-brief` — commit the verdict file at
  handoff/artifact stages.
- `gate-runner` — owns test execution; this skill runs no broad suites, only cheap
  read-only Git commands.

## Non-goals

- Never print/echo the verdict JSON or file contents as a message.
- Never end the turn after writing — hand control back inline to
  `gate-arbiter`.
- Never run broad test suites (only cheap read-only Git commands).
- Never re-run the full fan-out on `code-review.check`.
- Never write source files (exactly one artifact: the verdict report).
- Never emit `defer`/`dismiss` findings in `findings[]` (counts go in
  `rationale`).
- Never invent standards when guides are absent.
