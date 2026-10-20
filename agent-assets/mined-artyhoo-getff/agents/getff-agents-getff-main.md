# AGENTS.md — framework contributor context (off-CC harnesses)

> **Authoritative for:** off-CC session context for contributors to this framework; portable rule index (§Rules).
> **NOT authoritative for:** project goal — see [README.md#why-this-exists](README.md#why-this-exists). CC-specific session boot — see [CLAUDE.md](CLAUDE.md) (auto-loaded by Claude Code at session start).

Universal format read by Cursor, Codex CLI, Aider, Windsurf, and other non-CC harnesses.
**Claude Code users:** `CLAUDE.md` is your authoritative entry doc — CC auto-loads it AND `.claude/rules/*.md`. Read this file only if working across harnesses or onboarding off-CC.

## What this project is

**Goal:** AI agents can't silently bypass undocumented conventions. Every codified rule is an executable artifact (ESLint rule, pre-push check, principle test, mutation gate, drift probe) that fails at the earliest reachable channel — edit-time → pre-commit → pre-push → CI → production audit. CI is the last resort, not the primary gate. Full statement: [README.md#why-this-exists](README.md#why-this-exists).

**Methodology:** recursive self-application — the framework validates itself with its own logic.

## Session start (Step 0)

1. Read [README.md#why-this-exists](README.md#why-this-exists) — the project goal.
2. Read [.claude/session-bootstrap.md](.claude/session-bootstrap.md) — goal restatement + invariants (compaction-resilient).
3. Read the rules below that apply to your task.

## Rules

**On Claude Code:** `.claude/rules/*.md` auto-load at session start — no manual action needed.
**On other harnesses (Cursor, Codex, Aider, Windsurf):** these rules do NOT auto-load. Read the ones relevant to your task from the list below before starting.

<!-- getff:begin section=rule-index plan=scripts/render-rule-index.mjs -->
One line per rule — full text: read `.claude/rules/<name>.md` (index: `.claude/rules/00-rule-index.md`).

| Rule | Class | Fires | Channel(s) |
|---|---|---|---|
| `ai-laziness-digest.md` | A | any R-phase, audit, sample-based investigation, or open-ended AI task. | always-on core |
| `ai-laziness-traps.md` | A | any R-phase, audit, sample-based investigation, or open-ended AI task. | paths:(5), edit-time inject |
| `attention-is-not-a-mechanism.md` | C | designing any load-bearing check (gate vs. bare human/AI attention). | always-on core |
| `autonomous-loop-continuity.md` | B | unattended turn ending with work in flight. | hook, digest |
| `build-first-reuse-default.md` | A | any capability commit / new-capability proposal. | paths:(7), edit-time inject |
| `ci-tool-pinning.md` | A | editing `.github/workflows/**` or any repo shell script. | paths:(6), edit-time inject |
| `cold-seat-economy.md` | C | re-running a cold seat on already-judged work; resume-vs-fresh choice. | skill-embed(2) |
| `companion-install-principle.md` | B | editing `setup.d/**` (companion install manifest/engine). | paths:(1), edit-time inject |
| `destination-environment-verification.md` | B | kickoff authoring; accepting container work; a cannot-reach claim. | paths:(1), edit-time inject |
| `doc-authority-hierarchy.md` | A | creating/editing any canonical or shipped consumer-facing doc. | paths:(4), edit-time inject |
| `dual-implementation-discipline.md` | A | shipping a new CC-native hook + choosing its delivery channel(s). | paths:(3), edit-time inject |
| `effort-worthiness.md` | C | any effort/rigor fork: probe demand, extra round, budget breach. | skill-embed(4) |
| `egress-no-api-bypass.md` | B | harvesting/egressing a finished aif-agent branch to a PR. | skill-embed |
| `evidence-regeneration.md` | B | a freshness gate RED, or a first live-fired matrix cell. | paths:(1), edit-time inject |
| `git-conflict-merge-forward.md` | B | a CONFLICTING PR, or any rebase/force-push urge. | claude-md |
| `kickoff-staging-placement.md` | A | editing/creating any file under `.claude/orchestrator-prompts/<umbrella>/`. | paths:(1), edit-time inject |
| `language-discipline.md` | A | writing any internal machinery or human-facing output. | paths:(3), edit-time inject |
| `memory-codification.md` | B | writing a durable behavioural convention to agent memory. | hook |
| `no-paid-llm-in-ci.md` | A | editing `.github/workflows/**` or `.github/actions/**`. | paths:(2), edit-time inject |
| `parallel-subwave-isolation.md` | C | dispatching parallel sub-wave / batch AI sessions. | paths:(1), edit-time inject |
| `phase-research-coverage.md` | A | phase research, prior-art lookups, negative-existence claims. | paths:(4) |
| `recommendation-laziness-discipline.md` | C | before an inline verdict/recommendation or an ambiguous fork. | digest |
| `research-source-trust.md` | A | authoring a rule-research provenance entry / resolving allowed sources. | paths:(2), edit-time inject, skill-embed |
| `reviewer-discipline.md` | C | review sessions (`/review`, `/ultrareview`, or a prose "проверь"/verdict ask). | agent |
| `rule-enforcement-channel-selection.md` | A | codifying any new rule / choosing its enforcement channel. | paths:(2), edit-time inject |
| `seat-lifecycle.md` | B | seat birth, self-cleaning handoff, or retirement in a seat session. | paths:(4) |
| `skill-description-quality.md` | C | authoring/updating any SKILL.md `description` field. | paths:(1), edit-time inject |
| `source-before-shape.md` | B | creating a new SKILL.md/agent/module, or authoring a dispatch/kickoff. | paths:(3), edit-time inject |
| `zcode-parity-doctrine.md` | A | editing hook twins, the harness-config renderer, or zcode-parity decision docs. | paths:(10), edit-time inject |
<!-- getff:end section=rule-index -->

## Key files for contributors

| What | Where |
|---|---|
| Project goal (authoritative) | [README.md#why-this-exists](README.md#why-this-exists) |
| AI-tooling conventions, capability-commit gates | [CLAUDE.md](CLAUDE.md) |
| Session bootstrap + invariants | [.claude/session-bootstrap.md](.claude/session-bootstrap.md) |
| Build-vs-reuse SSOT | [docs/meta-factory/prior-art-evaluations.md](docs/meta-factory/prior-art-evaluations.md) |
| Execution plan | [docs/meta-factory/EXECUTION-PLAN.md](docs/meta-factory/EXECUTION-PLAN.md) |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for full contributor details (hook setup, bypass policy, PR strategy).

## Configuration access

<!-- getff:begin section=configuration-access plan=packages/core/composition/fixtures/root-agents-demo.docplan.json -->
_Generated demo region (MT stage 4): fixture conventions rendered from Convention IR; enforcement lines are derived from live RenderOutcomes — see spec §5.1._

### Configuration access

Read configuration through the injected config accessor, never std::env::var directly
<!-- @nodes: no-direct-env-var -->
> Enforced: astgrep-python-yaml — FF7001 (type-aware bans need a type checker; route to the mypy backend (deferred, post-v0)) · cargo-clippy-toml ✅ · npm-eslint-declarative — FF7001 (typed rules are not expressible in the no-restricted-syntax declarative class; route to a type-aware backend (post-v0)) · ruff-tidy-imports-toml — FF7001 (type-aware bans need a type checker; route to the mypy backend (deferred, post-v0))
> Never (fires): fn main() { let _ = std::env::var("HOME"); }
> Always (clean): fn main() { let _ = app_config::env_var("HOME"); }

Read configuration through the injected config accessor, never process.env directly
<!-- @nodes: no-direct-process-env -->
> Enforced: astgrep-python-yaml — FF7002 (params contract violation: missing/invalid kind) · cargo-clippy-toml — FF7001 (not expressible in clippy.toml; route to the ast-grep escape-hatch backend (post-v0)) · npm-eslint-declarative ✅ · ruff-tidy-imports-toml — FF7002 (params contract violation: missing/invalid kind)
> Never (fires): const url = process.env.DATABASE_URL;
> Always (clean): const url = config.get('databaseUrl');
<!-- getff:end section=configuration-access -->

## Time handling

<!-- getff:begin section=time-handling plan=packages/core/composition/fixtures/root-agents-demo.docplan.json -->
_Generated demo region (MT stage 4): fixture conventions rendered from Convention IR; enforcement lines are derived from live RenderOutcomes — see spec §5.1._

### Time handling

Use an injected clock, not datetime.datetime.now() directly
<!-- @nodes: no-datetime-now -->
> Enforced: astgrep-python-yaml ✅ · cargo-clippy-toml — FF7001 (not expressible in clippy.toml; route to the ast-grep escape-hatch backend (post-v0)) · npm-eslint-declarative — FF7002 (params contract violation: missing/invalid selector) · ruff-tidy-imports-toml — FF7001 (call-with-args ban not expressible in ruff (bans a qualified name, not a call site); route to the ast-grep backend (#212))
> Never (fires): import datetime
x = datetime.datetime.now()
> Always (clean): x = clock.now()
<!-- getff:end section=time-handling -->
