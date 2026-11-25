---
name: agentic-doctor
description: Standalone verifier for an agentic-os install — checks the file manifest against the install journal, py-compiles AND imports every hook it owns (a badly-rendered scalar compiles but raises on load), dry-runs the enforcement hooks with canned events (block hooks must exit 2 on a synthetic violation, 0 on clean), runs the HITL smoke test on the output-contract gate, verifies settings registration, git hook installation, dependency plugins, scorecard thresholds, and agent-registry table integrity. Writes .agentic/agentic-os/doctor.json. Use when the user says "/agentic-doctor", "verify the agentic-os install", "check the agent setup", "run doctor", or after /agentic-init and /agentic-upgrade. Not for: performing the install (agentic-init), upgrading (agentic-upgrade), or fixing the issues it reports.
version: 0.1.0
license: Apache-2.0
---

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"agentic-doctor"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.



# agentic-doctor — install verifier

Read-only except for two things: `.agentic/agentic-os/doctor.json` (the
verdict) and the temporary probe contract Check 3 creates and deletes. You
never fix anything — you diagnose, report, and write the verdict. `TARGET` =
the current repo root (`git rev-parse --show-toplevel`).

Resolve the canonical agent, skill and state directories from
`journal.adoption` rather than assuming `.agentic/` — an adopted fleet keeps its
own layout. Files recorded as `origin: "adopted-existing"` belong to the user:
a missing one is a warning, and hash drift is information, not a fault. Finding
contracts in **both** `.agents/agents/` and `.agentic/agents/` is a failure —
that is the competing-fleet state the installer refuses to create, so seeing it
here means something else made it.

On Codex, additionally verify that `agentic-os`, `agentic-sdlc` and the required
`superpowers` version are enabled; that plugin hooks are enabled; that journaled
Codex TOML agents parse and point at canonical contracts; that journaled rules
exist; and that hook commands resolve from `git rev-parse --show-toplevel`.
Never read authentication values — their presence is checkable without their
contents.

Precondition: `TARGET/.agentic/agentic-os/install.json` exists (the install
journal written by `/agentic-init`). Missing ⇒ report "not installed — run
/agentic-init" and write a failed `doctor.json` with only that finding.

Collect results into `checks` (each check: `passed` bool + `detail`), plus
`failures` (flat list of failed-check messages) and `pending_restart` (plugin
names). Run every check even after failures — the report must be complete.

## Check 1 — File manifest vs journal

For every entry in `journal.files`:
- File missing ⇒ **fail** (`manifest`), unless `owner: "user"` with a skip
  origin (a skipped collision journals the pre-existing file — its absence is
  still worth a warning, not a failure).
- Current sha256 (`shasum -a 256`) differs from journaled ⇒ not a failure:
  report as `modified` (expected for `owner: "user"`; for `owner: "managed"`
  it means local edits an upgrade will prompt about; for `owner: "generated"`
  it means the contract drifted from its audited state — cross-check Check 7).

## Check 2 — Hook compilation and load

For each `.claude/hooks/*.py` the journal records with **`owner: "managed"`**, all
three must hold (key: `py_compile`). A mature repo's `.claude/hooks/` also holds the
team's own hooks; Claude Code runs those as `python3 hook.py`, so they need no
`__main__` guard and are none of the doctor's business. Skip them, and say how many
you skipped in the check's `detail`.

Filter on `owner`, not on the path. A team hook that *collides* with one of ours is
journalled at our path with `owner: "user"` — the installer skips rather than
overwrite it (Check 1 expects those entries to differ from their template). Keying on
the `.claude/hooks/` prefix alone would import someone else's file and fail the
install over something we never wrote.

2a. `python3 -m py_compile .claude/hooks/<name>.py` — any non-zero exit ⇒ fail.

2b. The hook **imports cleanly**. Two rules, in this order:

  - **Guard first.** If the file has no `if __name__ == '__main__':` line (accept
    either quote style), **do not import it** — record that as the failure.
    Importing is only safe because every managed hook guards its entry point; an
    unguarded one runs `main()` the moment anything loads it, and `main()` may
    `git fetch`/merge (`session_start_bootstrap`), run `ENV_CHECK_COMMANDS` through
    a shell, or block a tool call. **Import, never execute.**
  - Then load it as a module (not as `__main__`), so its top-level statements run
    and `main()` does not. Any traceback ⇒ fail — including `SystemExit`, which is
    not an `Exception` subclass, so a bare `except Exception` would let a hook that
    calls `sys.exit()` at import silently pass.

```
python3 -c "
import importlib.util as u, sys
spec = u.spec_from_file_location('h', sys.argv[1])
try:
    spec.loader.exec_module(u.module_from_spec(spec))
except BaseException as e:
    sys.exit('hook raised on import: %r' % (e,))
" .claude/hooks/<name>.py
```

`except BaseException`, not `except Exception` — and never a bare
`exec_module(...)` with no handler. A hook that calls `sys.exit()` at module level
raises `SystemExit`, which is not an `Exception` subclass: an unhandled one makes
this very process exit **0**, and the check records a pass over a hook that quits
before it ever reads an event.

**`py_compile` alone is not sufficient and never was.** A badly-rendered scalar
(see `VARIABLES.md § Rendering convention`) produces `X = "alembic … -m "<msg>""`,
which Python parses as the chained comparison `"…" < msg > ""` — it *compiles* and
exits 0. Every in-literal placeholder in the template set sits in a module-level
statement (an assignment, or the module docstring), so the `NameError` fires on
import, before any event is read. Without
2b, Checks 1–8 all pass over a `PostToolUse` hook that tracebacks on **every**
`Write` or `Edit` tool call (`settings-fragment.json.tmpl` wires
`migration_notice.py` to both matchers with no path filter, and the import fails
before `MIGRATIONS_DIR in file_path` is ever evaluated).

2c. Grep each hook for a leftover literal `{{` — an unrendered placeholder is a
    scaffold bug ⇒ fail.

## Check 3 — Canned-event dry-runs (exit-2 on violation, 0 on clean)

Same technique as the product's own `tests/t0/` cases (do **not** modify those
files; they live in the plugin repo, not the target). Skip any hook that is
not installed. All events are piped as single-line JSON on stdin.

To read a rendered list out of a hook, **import the module and read the attribute**
— never scrape the file's text. Per `VARIABLES.md § Rendering convention` the
newlines inside those strings are `\n` escapes, not literal line breaks, so the
source reads `X = """a\nb"""` on one line. Import it the same way Check 2b does
(that check discards its module, so load it again) and take the first line the
hook itself would honour — `next(s for l in m.HUMAN_GATED_COMMANDS.splitlines()
if (s := l.strip()) and not s.startswith("#"))`. Blanks and `#` comments are
skipped by the hook's own loop; feeding it one as `<GATED>` yields exit 0 and a
false failure.

1. **`human_gated_commands.py`** (only if its rendered list is non-empty; take
   the first listed command `<GATED>`):
   - `{"tool_name":"Bash","tool_input":{"command":"<GATED>"}}` → must exit 2.
   - `{"tool_name":"Bash","tool_input":{"command":"echo ok"}}` → must exit 0.
2. **`guarded_write_paths.py`** (only if its rendered list is non-empty; take
   the first guarded path `<GUARDED>` the same way):
   - `{"tool_name":"Write","tool_input":{"file_path":"<GUARDED>"}}` → exit 2.
   - `{"tool_name":"Write","tool_input":{"file_path":"README.md"}}` → exit 0
     (unless README.md itself is guarded — pick any unguarded path).
3. **`precommit_review_gate.py`**: `python3 .claude/hooks/precommit_review_gate.py status`
   → must exit without a Python traceback (exit code reflects approval state,
   both 0 and non-zero are healthy; a traceback fails the check).
4. **`instruction_gate.py`** — both probes use the deliberately-unregistered
   dummy name `__agentic_doctor_probe__` (never a real agent; on a healthy
   install every real contract IS scorecarded — see Check 7b):
   - No contract: echo `{"subagent_type":"__agentic_doctor_probe__"}` into it
     → must exit 0 (no canonical contract ⇒ not a governed agent).
   - Ungraded contract: create a temporary dummy contract at
     `.agentic/agents/__agentic_doctor_probe__.md` (one line of text is
     enough; it is intentionally absent from the scorecard), repeat the same
     event → must exit 2 ("never graded" — the gate enforcing). Delete the
     dummy file immediately after, even on failure.

## Check 4 — HITL smoke (the output-contract gate)

Targets the installed `.claude/hooks/subagent_gate.py` (rendered at install
with the default section list `Summary,Why,Blocking,Non-blocking,Escalate to
human`). Reuses the synthetic-transcript technique from
`tests/t0/run-output-contract.sh`: write a one-line JSONL transcript whose
assistant message carries the synthetic final text, then pipe a `SubagentStop`
event pointing at it.

```bash
HOOK="$(git rev-parse --show-toplevel)/.claude/hooks/subagent_gate.py"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

mktranscript() {  # $1 = transcript path, $2 = agent final text
  python3 - "$1" "$2" <<'EOF'
import json, sys
open(sys.argv[1], "w").write(json.dumps(
    {"message": {"role": "assistant", "content": [{"type": "text", "text": sys.argv[2]}]}}) + "\n")
EOF
}
runsmoke() {  # $1 = transcript path; prints nothing, exit code is the verdict
  python3 -c 'import json,sys; print(json.dumps({"hook_event_name":"SubagentStop","stop_hook_active":False,"transcript_path":sys.argv[1]}))' "$1" \
    | python3 "$HOOK" 2>"$WORK/stderr.txt"
}
```

The section lines in the transcript text must start at column 0 (`## …`) —
the gate matches sections at line start, so keep these blocks flush-left
exactly as written (same as `tests/t0/run-output-contract.sh` does).

**Smoke A — non-empty `## Blocking` must block (exit 2):**

```bash
mktranscript "$WORK/block.jsonl" '## Summary
PASS with caveats.
## Why
- smoke
## Blocking
- synthetic blocking finding (doctor smoke)
## Non-blocking
None
## Escalate to human
None'
runsmoke "$WORK/block.jsonl"   # expect exit 2
```

**Smoke B — clean PASS must pass (exit 0):**

```bash
mktranscript "$WORK/pass.jsonl" '## Summary
PASS — all checks green.
## Why
- smoke
## Blocking
None
## Non-blocking
None
## Escalate to human
None'
runsmoke "$WORK/pass.jsonl"    # expect exit 0
```

**Smoke C — escalation must demand AskUserQuestion (exit 2):**

```bash
mktranscript "$WORK/esc.jsonl" '## Summary
PASS.
## Why
- smoke
## Blocking
None
## Non-blocking
None
## Escalate to human
- synthetic escalation flag (doctor smoke)'
runsmoke "$WORK/esc.jsonl"     # expect exit 2
grep -q AskUserQuestion "$WORK/stderr.txt"   # must succeed
```

The AskUserQuestion instruction on stderr is how a raised `escalate_on` flag
reaches the human — the parent must surface the listed options before
proceeding.

Any deviation ⇒ fail (`hitl_smoke`) — a broken output-contract gate silently
disables the whole HITL pillar.

## Check 5 — Settings registration

Parse `.claude/settings.json`:
- Every installed **managed** gate hook is wired under `hooks` at its event.
  The authoritative set is the fragment
  `plugins/agentic-os/templates/hooks/settings-fragment.json.tmpl` — check
  **every** hook it wires, not the subset shown in any older summary, and in
  particular do not skip `prompt_scan_guard.py` (the prompt-injection scanner).
  The full wiring is:
  UserPromptSubmit → `prompt_scan_guard.py`;
  PreToolUse Bash → `human_gated_commands.py` + `precommit_review_gate.py`;
  PreToolUse Write/Edit → `guarded_write_paths.py` + `write_scope_guard.py block`;
  PostToolUse Write/Edit → `migration_notice.py` + `instruction_stale_notice.py`
  + `lint_on_save.py`;
  PostToolUse (all tools) → `context_monitor.py`;
  SubagentStart → `instruction_gate.py`;
  Stop → `subagent_gate.py` + `session_learnings_notice.py`;
  SubagentStop → `subagent_gate.py`;
  SessionStart → `session_start_bootstrap.py`;
  PreCompact → `precompact_checkpoint.py`.
  A hook the fragment wires that is **installed but not registered** at its
  event is a **failure**. A hook that is not installed (some are skipped by the
  installer when their capability does not apply) is not — the check is over
  the managed hooks actually present, matching Check 2's owner filter. Team-
  owned hooks in `.claude/hooks/` are outside the fragment and are not this
  check's business.
- The inverse is a **failure**: a wired hook command whose script file does
  not exist (it would exit 2 on every event and block all tool use).
- `permissions.deny` contains at least `Read(.env*)`, `Read(.auth/**)`,
  `Read(*token*.env)`.

## Check 6 — Git hook + dependencies

- **Git hook**: **applies only when the git layer is installed** — i.e. when
  `.githooks/pre-commit` is present in `journal.files`. Six of the ten presets
  (`ba-po`, `data`, `design`, `pm-delivery`, `portfolio`, `security`) carry no
  `githooks/pre-commit`, so a repo installed with only those must not be failed
  for a hook it was never meant to have. Not journaled ⇒ skip this clause and
  report `git_hook` as `passed: true` with the reason in its `detail`
  ("git layer not installed for this preset set").

  When it **is** journaled: `HOOKS_DIR="$(git rev-parse --git-path hooks)"`;
  `$HOOKS_DIR/pre-commit` exists, is executable, and contains the
  `agentic-os:` marker ⇒ installed. Tracked twin `.githooks/pre-commit`
  exists. Missing installed hook ⇒ fail with the remedy
  `bash scripts/install-git-hooks.sh`. If `pre-commit.local` exists, report it
  as the chained foreign hook (informational).
- **Git hook — gate-script presence (commit-blocking hazard).** Checked
  whenever `$HOOKS_DIR/pre-commit` carries the `agentic-os:` marker,
  *independent of the journal* — the installed hook lives outside the working
  tree and can outlive the layer that placed it. Then
  `.claude/hooks/precommit_review_gate.py` **must exist** ⇒ else **fail**. The
  hook runs `python3 "$ROOT/.claude/hooks/precommit_review_gate.py" precommit
  || exit $?` as its first action, so a missing gate script makes `python3`
  exit non-zero and **blocks every `git commit` in the repo**, including
  commits made outside any agent harness. The chained `pre-commit.local` runs
  *after* that line, so a team's own pre-existing hook stops firing too.
  Remedy: re-run `/agentic-init` to restore the script, or delete
  `$HOOKS_DIR/pre-commit` (and restore `pre-commit.local` if present) when the
  git layer is no longer wanted.
- **Dependencies**: for each non-optional plugin in the plugin's
  `manifest/dependencies.json` — present in
  `~/.claude/plugins/installed_plugins.json` at ≥ `min` ⇒ ok; registered in
  the target's `.claude/settings.json` (`extraKnownMarketplaces` +
  `enabledPlugins`) but not installed ⇒ add to `pending_restart` (not a
  failure — activation needs a session restart); neither ⇒ fail
  (`dependencies`) with the remedy "re-run /agentic-init Phase 3".

## Check 7 — Scorecard coverage and thresholds

Skip only when `.claude/hooks/instruction_gate.py` is not installed.
`docs/audits/instruction-scorecard.json` **missing while the gate is
installed ⇒ fail** — every governed spawn would hard-block as "never graded".
Otherwise read it (`files` map; entries carry `content_sha256`,
`composite_score`, optional `gate_threshold`; seeded entries also carry
`source: "template-inherited"` at score 100 — valid, not a finding).

**7a — generated-agent thresholds.** For every `owner: "generated"` canonical
contract in the journal:
- No scorecard entry ⇒ fail (spawns will hard-block as "never graded").
- `content_sha256` ≠ current file hash ⇒ fail as stale (spawn-blocked until
  re-graded — remedy: re-run the audit loop or the instruction-auditor).
- `composite_score <` its effective threshold (its `gate_threshold` when
  present, else 95) ⇒ fail.
- `gate_threshold` present (< 95) ⇒ **warning**, not failure: a PLAN decision-6
  relaxed install; echo the matching `journal.follow_ups` entry.

**7b — full-fleet coverage (certification hole closed here).** For **every**
`.md` file in the canonical agents dir (`.agentic/agents/*.md`) and its
`.claude/agents/<name>.md` pointer, plus `CLAUDE.md`, `AGENTS.md`,
`PATTERNS.md` when present:
- No scorecard entry ⇒ **fail** — `instruction_gate.py` checks exactly these
  paths per spawn and blocks on a missing entry, so an uncovered contract
  means that agent (templated or generated) cannot spawn. Remedy: re-run
  `/agentic-init` (its Phase 4 scorecard seeding) or grade the file via the
  instruction-auditor.
- Entry present but `content_sha256` ≠ current hash ⇒ warning (stale — the
  gate will block that agent's spawn until re-graded; escalate to fail if the
  file is `owner: "generated"`, which 7a already does).

## Check 8 — Agent-registry integrity

Skip only when `.agentic/guides/agent-registry.md` is absent from
`journal.files` (the `governance/agent-registry` template wasn't in the preset
union). When it is journaled but missing from disk, that is **Check 1's**
failure, not this one — report `registry` as N/A and move on. Otherwise this
check always runs, even with zero generated agents.

That file is THE routing matrix: `.claude/commands/pipeline-orchestrator.md`
reads it at runtime to discover which agent owns which intent. It is a
**hybrid of three parts** — template output above the marker row (the curated
rows), rows appended by Phase 5 step 6 immediately below it, and template output
again below those (the closing paragraph and `## Orchestration rules`). Nothing
else verifies the hybrid survived. A
broken table here is invisible: every other check passes, the file exists, its
hash matches, its text contains the rows — and the orchestrator still cannot
see a single generated agent.

Define a **valid table block**: a header row, followed *immediately* by a
delimiter row (each cell matching `:?-+:?`) whose **cell count equals the
header's**, followed by the run of consecutive lines that each begin with `|`.
GFM recognises a table only in that exact shape. Two consequences, both verified
against GitHub's renderer:

- Drop or mangle the delimiter row and the **entire** table becomes paragraph
  text (`<table>` count: 0) — not just the appended rows. No agent is routable.
- A blank line, a prose paragraph, or a bare `<!-- comment -->` line **ends** the
  block; any pipe-delimited line after it comes back as `<p>| … |</p>`.

The **routing table** is the valid block whose header row's first cell is
`Trigger / intent`.

- **8a — the routing table is a valid GFM table.** A header row with that first
  cell exists, and it is immediately followed by a matching delimiter row. A
  header present but not followed by a valid delimiter ⇒ **fail** (the whole
  matrix renders as prose). No such header at all ⇒ **fail**.
- **8b — marker row present, as a row.** Exactly one line has
  `<!-- generated-agent-rows -->` as its **first cell** and begins with `|`.
  Zero ⇒ **fail**. A `<!-- generated-agent-rows -->` appearing as a bare comment
  line instead of a table row ⇒ **fail**: it ends the block, so Phase 5's
  appended rows land outside it. More than one ⇒ **fail**.
- **8c — marker row inside the routing block.** Otherwise ⇒ **fail**.
- **8d — no orphaned rows.** Every pipe-delimited line in the file belongs to
  *some* valid table block. A pipe line in no block is an orphaned row: it looks
  like a row in the source and renders as a paragraph ⇒ **fail**, quoting it.
  (A second, unrelated table elsewhere in the file forms its own valid block and
  is fine.) This is exactly what a paraphrased — rather than verbatim-rendered —
  Phase 4 template produces, and it is silent everywhere else.
- **8e — every generated contract has a row.** For each `owner: "generated"`
  canonical contract in `journal.files` under `.agentic/agents/` (a generated
  *guide* under `.agentic/guides/` is not dispatchable and gets no row): exactly
  one row **inside the routing block, below the marker row**, whose Owning-asset
  cell cites that contract's path. Zero ⇒ **fail** (the agent exists but is
  undiscoverable). Two or more ⇒ **fail** (breaks one-owner-per-intent, which
  Phase 5 step 6's replace-by-path rule exists to preserve).
- **8f — no stale rows.** Every row below the marker cites a path that exists on
  disk. A row pointing at a removed slot ⇒ **fail** (the orchestrator would
  dispatch to a missing contract).
- **8g — the tail survived.** Below the marker row and its run of generated
  rows, the file must still carry a non-empty tail containing the
  `## Orchestration rules` section. The template renders it unconditionally, so
  an empty tail or a missing rules section is never a legitimate state ⇒
  **fail**. This catches a registry truncated at the marker row by an
  `/agentic-upgrade` run under the old two-way split reconciliation — damage
  that 8a–8f cannot see, because the marker row, the table block, and every
  generated row all survive the truncation intact, and GitHub still renders a
  perfectly valid table. Remedy: re-run `/agentic-upgrade` and accept the tail
  diff ("take theirs").

Failures here are `registry`. Remedy for 8a/8b/8c/8d: the template portion
drifted from `templates/governance/agent-registry.md.tmpl` — re-render it
verbatim, then re-append the generated rows below the marker row. Note
`/agentic-upgrade`'s Agent-registry split-reconcile **cannot** do this unattended
when the marker is missing entirely: it is specified to stop and ask rather than
guess where the split belongs. Remedy for 8e: re-run Phase 5 step 6.

**Do not infer this check from the file's text alone.** Grepping for a
contract's path finds the row whether or not it sits inside the table — that is
precisely how a generated contract can audit at 100/100 on an
"automatic delegation" claim while being unroutable. Parse the block structure;
never substring-match. The deterministic subset — 8a–8d plus 8g — is implemented
in `tests/lib/check-registry.py`, which runs against the Phase-4 scaffold in the
acceptance matrix; 8e/8f have no generated agents to check there and are yours
alone.

## Write the verdict

Write `.agentic/agentic-os/doctor.json`:

```json
{
  "schema": 1,
  "checked_at": "<ISO-8601 now>",
  "agentic_os_version": "<from the install journal>",
  "passed": <true iff failures is empty>,
  "checks": {
    "manifest": {"passed": true, "detail": "..."},
    "py_compile": {"passed": true, "detail": "..."},
    "dry_runs": {"passed": true, "detail": "..."},
    "hitl_smoke": {"passed": true, "detail": "A:2 B:0 C:2+AskUserQuestion"},
    "settings": {"passed": true, "detail": "..."},
    "git_hook": {"passed": true, "detail": "..."},
    "dependencies": {"passed": true, "detail": "..."},
    "scorecard": {"passed": true, "detail": "..."},
    "registry": {"passed": true, "detail": "..."}
  },
  "pending_restart": ["<plugin names>"],
  "failures": ["<one message per failed check item>"]
}
```

Then report to the user: PASS/FAIL headline, each failed check with its
one-line remedy, pending-restart plugins, and relaxed-threshold warnings.
