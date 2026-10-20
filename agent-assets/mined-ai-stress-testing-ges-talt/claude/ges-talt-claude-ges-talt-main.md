# Ges-Talt — session operating manual

Agent org + docs conventions for this repo (and any repo adopting it).
Read `README.md` for philosophy; this file is what you *do*.

## On session start

1. Ensure the docs scaffold exists: `python3 scripts/init_docs.py .`
   (idempotent; safe to run every session). In a different target repo:
   `python3 scripts/init_docs.py /path/to/repo`.
2. Identify the current sprint folder: `docs/sprint-<m>-<y>-<dd>-<dd>/`
   (month, 2-digit year, start day, end day — e.g. `sprint-7-26-12-19`
   = 2026-07-12 → 07-19). If today falls outside every sprint window,
   scaffold the next one before starting work.
3. Run the gate — one command: `python3 scripts/gate.py` (regenerates INDEX,
   personas, and repo-map, then runs every lint + the hard-verifier registry,
   failures-first; `--check` verifies without regenerating). A red verifier is
   a to-do, not noise. `docs/repo-map.md` is the token-cheap
   where-is-everything index — read it before grepping the tree.
4. `gate.py` already regenerates the personas at `.claude/agents/` (via
   `build_personas.py`) so every role is a callable `subagent_type`. Run it
   after any roster change.
5. Tooling provisioning: `scripts/setup-tools.sh` installs the PDF-extraction
   toolchain (`poppler-utils`/`pdfminer.six`) so `scripts/extract_text.py`
   never dead-ends; the environment setup step should run it. Read a PDF/binary
   with `python3 scripts/extract_text.py <path>` instead of failing on it.
   Other one-command helpers: `scripts/new_sprint_log.py <slug>` (stamp the
   sprint-log entry), `scripts/backlog.py add|done` (backlog rows),
   `scripts/ship.py [--main]` (push dev + fast-forward main, guarded).

## Routing — use the roster, don't bypass it

**This section overrides the default reluctance to spawn subagents.** The
roster is not documentation about how work *should* flow — it is the set of
workers work *does* flow through. The failure this repo exists to prevent is
the orchestrator authoring the roster and then doing all the work itself
(issue #59). Concretely:

- **Route implementation and review through the roster.** For anything beyond
  a single-file or tightly-coupled change, prefer delegating to the owning
  `subagent_type` (now installed at `.claude/agents/`, discoverable via
  `agents/INDEX.md` / `docs/repo-map.md`) over doing it inline.
- **A major output carries a recorded, risk-appropriate verdict.** Regardless
  of who implements, before it ships: security/legal at spec time
  (consultation-proximity, `ORCHESTRATION.md`), then a review pass whose depth
  scales with blast radius (issue #74) — the `logicians/falsifier` "presume
  this is wrong" pass for **critical systems** (auth, API, payments, crypto/
  secrets, irreversible/data-loss ops), and the linter/test-suite gate
  (`scripts/verify.py` + `testing/`, Playwright E2E where a UI/flow is
  involved) standing in for everything else. Record the outcome either way (a
  `COMMS.md` line + the run-manifest `verdicts:` field; `WORKFLOW.md §5`,
  verifier `verdict_recorded`). Don't spend the opus falsifier on a routine
  change a linter covers, and don't ship a major output with no verdict.
- **The caveat, so this stays followable:** delegation is not free — cold
  subagents re-derive context, cost tokens, and can collide on shared files.
  Inline implementation of a single tightly-coupled change is often the right
  call. This directive is **not** "fan out everything." It is: make the
  roster the default path for non-trivial work, and make the review/adversarial
  gate non-skippable. Skipping the gate is the violation; keeping a small
  change inline is not.

See `agents/ORCHESTRATION.md` (the orchestrator model) and `agents/WORKFLOW.md`
(the verdict loop + the gate). The SessionStart hook (`.claude/settings.json`)
reinjects this at the start of every session.

## Docs convention

- `docs/backlog.md` — one table row per issue; the spec-driven PM owns it.
- `docs/sprint-*/prd.md` — the sprint's requirements; issues cite `§n`.
- `docs/sprint-*/sprint-log/` — one dated entry per working session
  (template: `docs/templates/sprint-log-entry.md`). Write one before
  ending substantial work; decisions recorded there are not re-litigated.
- `docs/sprint-*/user-journeys/` — one file per journey
  (template: `docs/templates/user-journey.md`).

**Delivery conventions the agency hands to a target repo** (the SDLC
hand-off kit, #79–#92 — templates/conventions/verifiers, not filled-in
artifacts for this meta-repo):
- `docs/definition-of-done.md` — the one named DoD (cross-refs the gates,
  risk-tiered per #74); `docs/traceability.md` — the requirement→test chain
  (verifier `traceability`); `docs/doc-metadata.md` — the `owner`/
  `last_validated` marker (verifier `doc_freshness`).
- `docs/prioritization.md`, `docs/blueprinting.md`, `docs/testing-tiers.md`,
  `docs/risk-register.md`, `docs/accountability.md` — the PM/design/testing/
  risk/ownership conventions.
- `docs/templates/` — `adr.md` (+ `scripts/new_adr.py` → `docs/adr/`),
  `srs.md`, `design-spec.md`, `erd.md`, `release-decision.md`,
  `risk-assessment.md`, `vulnerability-assessment.md`, `customer-feedback.md`.
- `.claude/skills/release-readiness` — the go/no-go gate procedure.
- New to the repo? Read `docs/for-ai-agents.md` (architecture, setup,
  commands, troubleshooting).

## Workflow (spec-driven)

A user goal enters through `agents/pm/project-manager` (opus,
spec-driven): it reads/drafts the PRD, writes an issue spec per
`docs/templates/issue-spec.md`, and cuts issues + granular sub-issues —
every sub-issue has one assignee from `agents/INDEX.md`, checkable
acceptance criteria, and a negative prompt. Implementation flows to the
assigned agents; static review is `agents/logicians/`, empirical
verification `agents/testing/`, security `agents/security/`. Don't hand
work to an agent outside its charter — check the index first. See
`agents/ORCHESTRATION.md` for the orchestrator model (consultation
proximity, ephemeral agents, the user journey, "Finished view chat log"),
`agents/WORKFLOW.md` for the verdict loop (PASS/FAIL handback, retry cap,
escalation, issue-closing) and PM delegation rules, `agents/COMMS.md` for
the quoted-attribution reporting format (every relay/handoff closes with a
code-verified token cost via `scripts/verify_comms.py`), and
`docs/feedback-loop.md` for the closed-loop discipline (verdicts revise
the setpoint, not just gate).

## Roster rules

- Agents live in `agents/<team>/<role>/` as `agent.md` + `SPEC.md`
  (template: `agents/TEMPLATE/`).
- After adding/changing agents: `python3 scripts/build_index.py` must
  exit 0 (it regenerates `agents/INDEX.md` and lints the roster — opus
  never holds Edit/Bash; Write only via documented exception).
- Model policy: cheapest sufficient — a concrete model or a capability
  tier from `scripts/models.toml` (`docs/model-tiers.md`). Opus / `reason`
  tier = reasoning-bound roles only. `build_index.py` also flags tool-set
  widening vs `scripts/tools-baseline.json` (refresh intentionally).
- A role may carry an optional `DEPTH.md` loaded only on a depth trigger
  (`docs/depth-packs.md`) — depth without per-call token cost. Per-role
  selection scores from the ledger: `scripts/credit.py` → `docs/credit.md`.
- Skills are rare and only for repeatable procedures (`agents/skills-policy.md`):
  a role's `SKILL.md` must stay ≤500 LoC — `scripts/audit_skills.py` fails
  CI on a violation. Charter = who; `DEPTH.md` = how it reasons; `SKILL.md`
  = a procedure it runs. Most roles need no skill.
