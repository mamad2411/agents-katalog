---
name: audit
description: Blueprint audit — run the consistency-check roster over an imported blueprint (gaps, jargon, channel conflicts, KPI drift, ownership, value dead-ends, hidden fees), recording findings ranked by impact and effort; re-run the checks, or dismiss or resolve a finding. Building → ub:map; hypothetical changes → ub:whatif.
---

# Blueprint Audit

A blueprint that is merely *valid* can still be *wrong*: a lane nobody
staffs, a step customers experience but no cell records, a fee the journey
never shows. The audit runs a fixed roster of **checks** — each a written
interrogation, each executed by a fresh-context auditor — and lands the
results as `audit_findings` rows a human can triage. The audit never fixes
anything: it points at cells by key, and rates each finding three ways —
severity (how wrong it is), impact (how much fixing it matters to the
service) and effort (how much work the fix takes) — so the report can say
what to fix first.

Paths resolve against the plugin root (`${CLAUDE_PLUGIN_ROOT}` in Claude Code) or the workspace root, per `AGENTS.md`.

## Entry-state detection (do this first)

| Entry state | Route |
| --- | --- |
| No workspace / no IR | Stop. Nothing to audit — that is the `ub:map` skill's job |
| IR exists, no DB reachable | Audit the IR files directly; `audit/findings-report.json` is the ledger (playbook §1 route substrate) |
| Imported blueprint, DB reachable | Full run: roster → auditors → dedupe → findings rows |
| "Audit just scenario X" | Same pipeline, cell universe scoped to that scenario's keys |
| "Dismiss / resolve finding X" | **Triage route** — status change only, playbook §4. Never re-run checks to honor a triage ask |
| Re-run after edits | Full run; supersede semantics below make it safe |
| "Add a new check" | Author a `skills/audit/references/check-*.md` from the template in playbook §5, then run it alone once before adding it to the roster |

Row precedence when the first three could overlap: DB reachability decides
(credentials present AND the target answers) — per-scenario draft status
never changes the route, only lands as a staleness note in the report.

**Playbook gating**: read `references/audit-playbook.md` before executing
any route. It carries the run semantics, the fingerprint algorithm, the
triage rules, and the check-authoring template.

## Hard rules

- ⚠ **REQUIRED — the audit's only writes are `audit_findings` rows**
  (insert, update, its own check's supersede); humans change `status`.
  Fixing what it finds is a separate, confirmed `ub:map` pass.
- ⚠ **REQUIRED — one fresh-context auditor per check, blind.** Each
  `agents/auditor.md` dispatch gets ONE check doc and the blueprint export,
  and never sees other checks' output. Cross-check synthesis happens in the
  main context after all auditors return.
- ⚠ **REQUIRED — dedupe by fingerprint through `audit_tools.py dedupe`**
  (playbook §2–§3); dismissed stays dismissed.
- ⚠ **REQUIRED — per-check atomic supersede.** A check that completes
  replaces its own previous open findings in one transaction; a check that
  fails leaves its previous findings untouched. Never wipe the whole run's
  findings up front.
- ⚠ **REQUIRED — no verbatim excerpts in a summary.** Findings are
  read by every signed-in account and travel into shared docs. Cite cell
  keys and titles; never paste evidence text, proposition figures, or
  interviewee words.
- ⚠ **REQUIRED — confirm the import target** before any DB write;
  `references/adapter-contract.md` applies unchanged — wrong-project
  protection. (Vacuous on the no-DB route — no DB write ever happens
  there, so there is no target to hunt for.)

## The pipeline

```
imported blueprint (or IR files)
  → roster    (enumerate skills/audit/references/check-*.md; skips decided HERE and
               only here — rules in playbook §1.5, every skip reported)
  → export    (one read-only blueprint export the auditors share —
               skills/audit/scripts/audit_tools.py export)
  → dispatch  (one auditor per check, parallel, blind)
  → collect   (findings JSON per check; validate each auditor's output
               against the findings-row shape pinned in agents/auditor.md
               BEFORE any dedupe or `report --apply` — `audit_tools.py
               validate`; a finding missing its severity, impact or effort
               is malformed output = check failed, re-dispatch once, then
               report the check as failed)
  → dedupe    (audit_tools.py dedupe, playbook §3)
  → write     (one run_id for the run; per-check atomic supersede)
  → report    (open findings in priority order — Do first, Plan, Quick
               wins, Later, playbook §3.5 — then per-check counts +
               skipped checks + failed checks; nothing silent)
```

## The check roster

One file per check, `skills/audit/references/check-<name>.md`. Wave 1 needs only core
blueprint data; wave 2 reads the spec columns and **skips gracefully** —
reported, never silent — when they are absent or empty.

The table below is **illustrative — the roster is the directory listing**
(`skills/audit/references/check-*.md`, enumerated at roster time). A check
file that exists runs (or is reported skipped) whether or not a row here
mentions it.

| Wave | Check | Asks |
| --- | --- | --- |
| 1 | `gap-sweep` | Which experienced moments have no cell — empty stretches, dangling dependencies, uncovered steps |
| 1 | `jargon-lint` | Which customer-facing cell texts use words the customer would never say |
| 1 | `channel-conflict` | Where do simultaneous cells compete for the same actor or channel |
| 1 | `obsolete-source` | Which cells model a surface or flow the mapped source no longer has (conditional on source access — playbook §1.5) |
| 2 | `kpi-alignment` | Do lane KPIs reward what the cells actually do (lane `kpis`/`tools`) |
| 2 | `perceived-owner` | Where the recorded owner and the perceived owner diverge (owner pair) |
| 2 | `value-ledger` | Which cells deliver value to nobody, and which audiences receive none (`value_props`) |
| 2 | `fee-visibility` | Where money changes hands invisibly to the customer journey |

## Deterministic exit conditions

| Phase | Exit condition |
| --- | --- |
| Roster | Every `check-*.md` either dispatched or reported skipped-with-reason |
| Collect | Every dispatched check returned valid findings JSON or is reported failed after one retry |
| Write | Rows for this `run_id` = deduped findings; open-fingerprint index reports zero conflicts; per-check supersede left no orphaned open findings from prior runs of completed checks |
| Idempotence | Running twice on an unchanged blueprint yields zero new rows the second time; a re-run whose only change is a rating updates the open finding instead of adding one |
| Triage | The named finding's `status` changed and nothing else did |
| Report | Printed checklist: the open findings grouped Do first / Plan / Quick wins / Later (`audit_tools.py rank` on the file ledger; `list_findings` already returns that order on the canvas), then per-check found/skipped/failed counts and the run_id — never silent |

## Agents

- `auditor` — one check doc + the blueprint export in; findings JSON out
  (check, severity `info|warn|critical`, impact and effort
  `low|medium|high`, cell keys, summary). Blind to other checks. Tools:
  Read, Glob, Grep, Bash.
- `impact-tracer` — its Method is the walk the `channel-conflict` auditor
  runs itself when a chain is unclear.

## References

| Read when | File |
| --- | --- |
| Doing anything in this skill | `references/audit-playbook.md` |
| Executing a specific check | `skills/audit/references/check-<name>.md` |
| Anything touching an import target | `references/adapter-contract.md` |
| Understanding the findings table | `references/data-model.md` |
| Naming lanes/actors while reading | `references/lane-vocabulary.md` |
| How the same audit behaves on the app canvas (dedupe spaces, canonical dedupe row) | `references/canvas-adapter.md` |
