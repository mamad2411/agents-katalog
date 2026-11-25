---
name: harden-codebase
description: "Implements the accepted hardening fixes, each backed by a test."
---

# Harden — Implement Accepted Hardening Deltas

When invoked, walk the queue of accepted Hardening Deltas and implement
each one. Each delta becomes a focused commit (or PR) following the
Red-Green-Blue cycle.

If arguments are provided, treat them as either:
- A specific delta ID (`/sulis:harden-codebase HD-003`) — implement only that delta.
- A project name — implement all accepted deltas in dependency order.

If no arguments and one project exists under `.architecture/`, use it.
Otherwise list available projects and ask.

---

## What You Read

| Source | Why |
|---|---|
| `.architecture/{project}/**/HD-*.md` (recursive) | The deltas themselves — ADDED/MODIFIED/REMOVED instructions. Discovered with `find .architecture/{project}/ -name 'HD-*.md' -type f`. Deltas may live in the canonical flat `hardening-deltas/` (audit/security/MUC/NFR sources) OR in per-review bundles under `code-reviews/PR-NN-{timestamp}/hardening-deltas/` (code-review-sourced drafts). |
| `.architecture/{project}/**/hardening-deltas/INDEX.md` (recursive) | The acceptance order and dependency graph. The top-level `hardening-deltas/INDEX.md` tracks deltas from non-review sources; per-review bundles carry their own INDEX.md tracking only the drafts produced by that review. |
| `.specifications/{project}/MISUSE_CASES.md` (if present) | When a delta's `source` field references `srd:misuse-case-MUC-NN`, you read the originating misuse case for full context — the abuse pattern, the System Response (REQUIRED), and the related NFRs. The MUC is the load-bearing requirement; the delta is its implementation. |
| `.specifications/{project}/NFR.md` (if present) | NFRs derived from the adversarial sweep (rate limits, retention periods, integrity thresholds) often parameterise hardening implementations — e.g., MUC-02's rate-limit response references NFR-12's specific limit. |
| The codebase | The current state of the files the delta touches |

You only implement deltas with `status: accepted`. Deltas at `proposed`,
`rejected`, or `implemented` are skipped. Code-review drafts ship at
`status: proposed` inside their review bundle; the user (or a follow-on
agent) promotes them to `accepted` in the delta's frontmatter to queue
them for this skill.

**Misuse-case-sourced deltas are first-class.** When a delta's frontmatter has
`source: srd:misuse-case-MUC-NN`, treat it as a contract bound to the MUC's
System Response — the test you write in Red must prove that the system either
refused/detected/logged/rate-limited the misuse pattern (as the MUC requires)
or did not before this delta. If you cannot construct that test, the delta is
not implementable yet — escalate to the user rather than relaxing the contract.

---

## Workflow Per Delta

For each accepted delta, follow the **Red-Green-Blue** cycle from
`references/red-green-blue.md`:

### 1. Red — Write the failing characterisation test

- Locate the test file named in the delta's `Verification` section.
- Write the failing test.
- Run the test suite — confirm the new test fails for the reason the delta describes.
- Commit: `test({HD-NNN}): characterise {gap} — RED`.

### 2. Green — Apply ADDED/MODIFIED/REMOVED

- Apply the file changes the delta specifies.
- Make the failing test pass.
- Run the broader test suite — confirm nothing else broke (this matters
  especially for MODIFIED changes; if it does break, that is a gap in the
  pre-existing test coverage — flag it and add the missing test before
  proceeding).
- Confirm code is "boring" per `references/boring-code.md`. No singletons,
  no hidden state, no metaprogramming, no `any` casts.
- Commit: `feat({HD-NNN}): {title} — GREEN`.

### 3. Blue — Refactor within scope

- Look for duplication introduced or revealed by the change (EP-03).
- Extract shared resilience primitives if 2+ instances now exist (e.g. two
  external calls now both use a timeout — extract a shared policy).
- Refactor stays in the file scope of the delta. Cross-file refactors that
  emerge become **new deltas** (file a follow-up delta, do not pursue
  mid-stream).
- Run the test suite — confirm Blue introduces no behaviour changes.
- Commit: `refactor({HD-NNN}): {what} — BLUE`.

### 4. Update the delta

- Update the delta's frontmatter `status: implemented`.
- Add an `implemented` block at the bottom recording the commit SHAs and date.

---

## What You Always Inject (Concrete Patterns)

For specific gap types, you use established libraries and patterns. Default
choices below — override based on the project's existing stack.

### Resilience (timeouts, retries, circuit breakers)

| Stack | Default library |
|---|---|
| Node/TypeScript | `cockatiel` or `opossum` |
| .NET | `Polly` |
| Java/Kotlin | `resilience4j` |
| Python | `tenacity` (retry) + `pybreaker` (CB) |
| Go | `failsafe-go` or hand-rolled with `context.WithTimeout` |

If the project already uses a different library, prefer that — consistency
matters more than the SEA default.

### Secrets

| Stack | Default backend |
|---|---|
| Anywhere on AWS | AWS Secrets Manager via SDK |
| Anywhere on GCP | GCP Secret Manager via SDK |
| Anywhere on K8s | External Secrets Operator + cloud backend |
| Local dev | 1Password CLI or Doppler (NOT `.env`) |

### Observability

- **Traces:** OpenTelemetry SDK + OTLP exporter. Always.
- **Logs:** Structured JSON, `trace_id` correlated. Pino (Node), structlog (Python), Logback JSON (JVM).
- **Metrics:** OpenTelemetry metrics API, exported via OTLP.
- **Dashboards:** Grafana (or equivalent), pre-defined panels per service.

### Encryption / mTLS

- Service mesh if one exists (Istio, Linkerd, Consul Connect). Reuse it.
- If no service mesh: client cert + server cert per service, rotated via
  cert-manager.

---

## Workflow When Implementing Many Deltas

1. Read `INDEX.md` for the dependency order.
2. For each delta in order (skip if `dependsOn` not yet `implemented`):
   - Run the Red-Green-Blue cycle above.
   - Commit per stage (3 commits per delta).
   - Update the delta's status.
3. After all deltas in this run are implemented, update `INDEX.md` with the
   new statuses.
4. Report: deltas implemented, deltas skipped (and why), tests added,
   coverage delta if measurable.

---

## When You Must Stop

- The delta's failing test cannot be constructed deterministically (e.g. it
  requires a chaos primitive the codebase doesn't have yet). Resolution: file
  a precursor delta that adds the chaos primitive, then return to this delta.
- The delta's MODIFIED change breaks a pre-existing test that has no obvious
  fix without changing the delta's contract. Resolution: stop, surface to
  the user, do not paper over by deleting the broken test.
- The delta touches code outside the audited scope. Resolution: stop,
  surface to the user, propose a new delta or scope expansion.
- Boring-code violations cannot be avoided in Green (e.g. the framework
  requires a decorator). Resolution: document the framework boundary in the
  delta's Rationale and proceed.

---

## Adapting Depth

- **Quick** ("just close the criticals") — implement only `severity: critical` deltas, skip the rest. Useful before a deploy that needs to ship now.
- **Full** (default) — implement all accepted deltas in dependency order.
- **Dry-run** ("show me what would change") — produce the diff per delta as a markdown report; do not apply changes. Useful for review.

**Tier-aware batching.** Per `references/right-sizing.md`:

- Tier S/M (≤15 deltas in the queue): implement all in one run.
- Tier L (15-50 deltas): batch by `dependsOn` graph; review acceptance after each batch.
- Tier XL (50+ deltas): batch by bounded context; full review cadence between batches.

Read the tier from `.architecture/{project}/SIZING.md` if present, or from
`TDD.md`'s Sizing Report appendix as a fallback. If neither exists, infer
tier from current delta count (S=≤15, M=≤30, L=≤80, XL=80+) and note in the
final report that tier was inferred rather than read.

---

## Gotchas

- **Never skip Red.** A delta implemented without the failing test first cannot prove the gap existed. The test is the evidence.
- **Never skip Blue.** EP-02 in CLAUDE.md is a non-negotiable. The REFACTOR step is mandatory.
- **Don't expand scope mid-delta.** If you discover a related gap, that is a new delta. Pursuing it derails the dependency graph.
- **Don't suppress pre-existing test failures.** If your delta's MODIFIED change breaks an unrelated test, that is a signal — either your change is wrong or the codebase has hidden coupling. Investigate; do not delete.
- **Don't rotate secrets in this skill.** Rotating live production secrets is operational, not code-level. The delta replaces the hardcoded literal with a vault lookup; the rotation is a separate runbook.

---

## See Also

- `references/hardening-deltas.md` — the HD format (plugin root)
- `references/red-green-blue.md` — the cycle (plugin root)
- `references/boring-code.md` — the Green standard (plugin root)
