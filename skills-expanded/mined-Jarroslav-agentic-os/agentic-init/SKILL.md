---
name: agentic-init
description: Install the agentic-os process layer into the current repo — interview (role presets, HITL dial, autonomy matrix, stack confirm, adapters), dependency registration, template scaffold, stack-specific agent generation with instruction-quality audit, then doctor verification. Journaled and resumable. Use when the user says "/agentic-init", "install agentic-os", "scaffold the agent architecture", "set up the agentic process layer", or "add agentic-os to this repo". Not for: upgrading an existing install (agentic-upgrade), verifying one (agentic-doctor), or running SDLC work.
version: 0.1.0
license: Apache-2.0
---

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"agentic-init"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.



# agentic-init — the installer

You scaffold a governed multi-agent architecture into the **target repo** (the
current working directory's git root, `TARGET` below). Everything you copy,
render, or generate is journaled so an interrupted run resumes and a re-run is
idempotent.

## Conventions (read once, apply everywhere)

- **`PLUGIN`** = the agentic-os plugin root (`${CLAUDE_PLUGIN_ROOT}` when set;
  otherwise the directory two levels above this SKILL.md). It contains
  `templates/`, `generators/`, `presets/`, `manifest/`.
- **`AGENTIC_OS_VERSION`** = `"version"` from `PLUGIN/.claude-plugin/plugin.json`.
- **Journal** = `TARGET/.agentic/agentic-os/install.json`. Shape:

  ```json
  {
    "agentic_os_version": "<AGENTIC_OS_VERSION>",
    "stack_discovery": { "...": "the structured record from generators/stack-discovery.md — see templates/VARIABLES.md § The stack-fact record" },
    "answers": { "<interview key>": "<value>" },
    "phase": "preflight|interview|dependencies|scaffold|generate|verify|done",
    "files": {
      "<repo-relative path>": {
        "sha256": "<hex of the file as written>",
        "template": "<template ID, gen/* slot, or 'derived'>",
        "owner": "managed|user|generated",
        "origin": "plugin|adopted-existing|generated"
      }
    },
    "follow_ups": ["<human-readable follow-up items>"]
  }
  ```

  Update the journal **after every phase** (and after every file write in
  Phase 4/5). `sha256` of a file: `shasum -a 256 <file> | cut -d' ' -f1`.
- **How journal and file writes happen.** Never edit `install.json` by hand and
  never write scaffold files directly; send versioned requests to the plugin's
  `runtime/run.py` (same envelope as the preflight above, `target` = `TARGET`):
  - top-level journal fields (`answers`, `stack_discovery`, `adoption`,
    `follow_ups`, `sdlc_skills`, `qe_blueprints`, `phase`) →
    `install.record` with `fields`;
  - rendered or copied files → `install.apply` with
    `files: {path: {content, template, owner}}` and `agentic_os_version`. The
    installer journals `sha256`, owner and file identity, and preserves
    pre-existing or user-modified files on its own (the collision default).
    It only replaces an unedited `managed` file without a confirmation:
    rewriting a file the journal records `generated` (an upgrade
    regeneration, or a Phase 5 audit-loop retry) needs `expect_sha256` = its
    current sha256 plus `owner: "generated"` — a plain apply preserves it and
    records it user-owned, so later upgrades stop offering regeneration;
  - content merged into a file that may already exist (the `CLAUDE.md`
    block; `.claude/settings.json` after merging the fragment and pruning
    unscaffolded hooks) → compute the merged text, then `install.apply`:
    if the file is absent, or journaled `managed` with its recorded sha256
    still on disk, send `owner: "managed"` and no confirmation; otherwise
    (pre-existing, user-owned, or edited) send `expect_sha256` = its current
    sha256 and no owner — it lands user-owned. `install.merge-settings` is a
    shortcut only when the settings file is absent or an unedited `managed`
    file and no pruning is needed (it does not take a confirmation);
  - a collision answer: **rename** → `install.apply` of the `ao-<name>` path;
    **overwrite** → `install.apply` with `expect_sha256` of the bytes shown
    (the file stays user-owned: a confirmation never claims ownership).
  `install.plan` previews the same actions without writing. A refused request
  means the file changed since it was shown (stale confirmation) or the
  request was invalid (unknown field, or claiming `managed` under a
  confirmation for a file the journal does not record as managed): re-read,
  fix the request or ask again; never fall back to a direct write. Always read
  the result: `applied`, `preserved` and (for removal) `removed`,
  `preserved`, `missing` and `unapplied_confirmations` say what actually
  happened, and a preserved path was not written.
- **Owner semantics**: `managed` = agentic-os wrote it and may overwrite it on
  upgrade when unmodified; `user` = pre-existed or user-declined — never
  touched again; `generated` = produced by a generator subagent — upgrades
  offer regeneration, never overwrite.
- **Origin semantics**: `origin` records where a file came from, which `owner`
  alone cannot express. Assets adopted from a fleet the repo already had carry
  `owner: "user"` with `origin: "adopted-existing"` — they are inputs to
  verification and never destinations for scaffolding or upgrade.
- **Rendering** (registry: `PLUGIN/templates/VARIABLES.md`): substitution of
  `{{VAR}}` — no logic in templates; every conditional lives here. Files without
  `.tmpl` are copied verbatim. **How you substitute depends on the file type:**
  - **`.py.tmpl` and `.json.tmpl` — escape every scalar.** Substitute
    `json.dumps(value, ensure_ascii=False)[1:-1]`: the value with `"`, `\`, and
    control characters (newlines included) escaped, and **no** surrounding quotes.
    The template already supplies the quotes — do not strip them, and do not
    hand-escape. Mandatory in every position: whole literal, interpolated literal,
    triple-quoted block, comment. Templates quote with `"` only; `json.dumps`
    does not escape `'`.

    `ensure_ascii=False` matters: with the default, an astral character (emoji, an
    astral CJK ideograph) is emitted as a `\uXXXX` surrogate pair, which a Python
    string literal does **not** recombine — the constant silently becomes two lone
    surrogates. Templates are UTF-8; the character stays itself.

    Skipping this ships a broken hook past a green doctor. The answer
    `alembic revision --autogenerate -m "<msg>"` substituted plainly yields
    `X = "alembic … -m "<msg>""`, which **`py_compile` accepts** (Python reads the
    chained comparison `"…" < msg > ""`) and which raises `NameError` on import.
    `VARIABLES.md § Rendering convention` tables all three known instances.

    Escaping every scalar uniformly is safe: `{{SCORE_THRESHOLD}}` sits in a bare
    numeric position and `json.dumps("95")[1:-1] == "95"`. The one genuine
    exemption is **list-valued variables in `.json.tmpl`**, which render as quoted
    JSON array elements: `[{{ESCALATE_ON}}]` →
    `["security","breaking-change","migration","spend"]` (each item `json.dumps`'d
    in full, *with* its quotes). Applies to `{{ESCALATE_ON}}` in
    `templates/sdlc/config.json.tmpl`;
    `templates/hooks/settings-fragment.json.tmpl` intentionally has no placeholders.
  - **Newline-list variables** (`{{GATE_COMMANDS}}`, `{{HUMAN_GATED_COMMANDS}}`,
    `{{GUARDED_WRITE_PATHS}}`, `{{ENV_CHECK_COMMANDS}}`, `{{SECRET_DENY_PATTERNS}}`)
    are scalars whose value is the items joined by newlines. Inside a `.py.tmpl`
    they land in triple-quoted strings and take the escaping rule above — the
    newlines become `\n` escapes, which the hook's `.splitlines()` decodes back.
    Inside `.md.tmpl` fenced blocks, substitute the literal newline-joined text.
  - **`.md.tmpl` prose** and comma-list vars outside JSON (e.g. in
    `templates/commands/core/pipeline-orchestrator.md.tmpl` and
    `templates/policy/escalation-policy.md.tmpl`): substitute the plain
    comma-joined string, unescaped.
- **Never `git add` or `git commit` in the target repo.** Report what was
  written; committing is the human's call (and their own review gate applies).

## Phase 0 — Resume / idempotent re-run

1. If `TARGET/.agentic/agentic-os/install.json` exists, this is a re-run or a
   resume:
   - Pre-fill every interview answer from `journal.answers`.
   - If `journal.phase != "done"`, resume at the recorded phase.
   - On a completed re-run, for each journaled `owner: "managed"` file: if
     its current sha256 matches the journal, silently re-render/refresh it; if
     it differs (user-modified), **skip it and warn** — never overwrite.
     `owner: "user"` files are never refreshed this way (merge targets such as
     `CLAUDE.md` follow the merge rule); `generated` ones follow Phase 5; files not yet
     journaled are scaffolded normally. **One exception**:
     `.agentic/guides/agent-registry.md` (`template: "governance/agent-registry"`)
     is **never** blindly re-rendered here, matched sha256 or not — the
     template renders the portion above the `<!-- generated-agent-rows -->`
     marker row and the portion below the generated rows (the closing
     paragraph and `## Orchestration rules`), but by construction has no
     knowledge of the rows Phase 5 step 6 appended between them on the prior
     run, so a naive "refresh" would silently discard them on every
     `--reinstall` of an already-`done` install, with no diff, no warning,
     no adversarial action required. Since this file's sha already matches
     the journal (that's the precondition for reaching this branch at all),
     there is nothing to refresh — re-rendering the identical template with
     the identical journaled answers against the identical plugin version
     produces byte-identical template content to what's already on disk.
     **Skip it entirely; leave it untouched — no warning needed here even
     on a genuine sha mismatch** (a user-edited row, or an interrupted prior
     run): unlike every other file in this sweep, silence isn't a lost
     signal for this one — Phase 6's `agentic-doctor` run, later in this
     same pass, already reports any `owner: "managed"` sha drift as
     `modified` regardless of which file it is. (A plugin-version change is
     `/agentic-upgrade`'s job, not this phase's — its dedicated Agent
     registry split-reconcile section, `skills/agentic-upgrade/SKILL.md`,
     is where a real template-content change to this file gets handled.)
2. No journal ⇒ fresh install; continue to Phase 1.

## Phase 1 — Preflight

1. `git -C . rev-parse --show-toplevel` — not a git repo ⇒ AskUserQuestion:
   run `git init` here, or abort. `TARGET` = the toplevel.
2. `git status --porcelain` — dirty tree ⇒ warn (the scaffold adds many files;
   a clean tree makes the diff reviewable) but proceed on confirmation.
3. `python3 --version` — missing ⇒ abort with install instructions (every
   enforcement hook is Python).
4. **Adoption probe.** Run `python3 PLUGIN/scripts/detect-adoption.py TARGET`
   and journal its JSON as `journal.adoption`. Any conflict it reports is a hard
   stop, not a warning — two competing fleets in one repo is a state the
   installer must not create.

   In `adopt-existing` mode the probe's paths become canonical: inventory
   everything it returns as `owner: "user"`, `origin: "adopted-existing"`,
   `template: "adopted"`, and leave existing contracts, skills, adapters, hooks,
   rules, governance and scorecard entries exactly as they are. Governance that
   is genuinely missing may be added, but only as a reviewed managed block. Hook
   parity is reached by adapting the fleet's own implementation through a thin
   harness shim — never by writing a second copy alongside it.
5. **Stack discovery** (two tiers — full design and record schema in
   `PLUGIN/generators/stack-discovery.md`). **Re-run cost guard**: if
   `journal.stack_discovery` already exists (a prior run reached this step),
   skip both tiers and reuse the journaled record — same principle as Phase
   0's per-file sha256 skip and answer pre-fill. Tier 2 is a real subagent
   spawn, not a free heuristic; re-running it on every `--reinstall` would be
   wasted cost for a fact that hasn't changed. Re-discovery is out of scope
   here — it belongs to a future `/agentic-upgrade` flow, not a routine
   re-install.
   - **Tier 1 — marker prior** (you do this yourself, no subagent — it's a
     handful of cheap `Glob`/`Read` checks, and it must stay purely
     deterministic — no strength/confidence judgment here, that belongs to
     Tier 2): test each curated profile's "Detection markers" section in this
     explicit order (this list governs, not directory order), first match
     wins, exactly as before this change: `nextjs-supabase.md`, `django.md`,
     `spring.md`, `rails.md`, `go.md`, `playwright-taf.md`. This produces a
     prior — a matched profile ID, or `none` if no profile's markers matched.
   - **Tier 2 — spawn `stack-discovery.md`**: substitute its `{{VAR}}`s,
     append the input block it defines (mode + Tier-1 prior + the resolved
     role preset union's `generated` set from Phase 2 Screen 1 — but see the
     note below on sequencing), and spawn it.
     - Prior matched ⇒ **`confirm-only` mode**, passing the matched profile's
       full text. Must produce a record whose derived facts match today's
       profile-lookup behavior; this is the byte-unchanged regression
       guarantee for the six curated stacks. Tier 2's own confirm-only
       process re-checks the marker against the real repo and falls back to
       `full` mode itself if it turns out stale (a concrete fact check, not a
       Tier-1 judgment call) — Tier 1 never second-guesses its own match.
     - No prior ⇒ **`full` mode** — the subagent inspects the repo from
       scratch. This is what makes a non-curated stack (or no stack at all)
       produce real discovered capabilities instead of nothing.
   - **Sequencing note**: this step only ever runs on a genuinely fresh
     install — per Phase 0, any resume jumps straight to
     `journal.phase`'s recorded phase, which is already past "preflight" by
     the time `journal.answers` could contain a role-preset union. So there
     is never a role-preset union available here yet. Always pass
     `generated: null` (inspect all four capabilities unconditionally;
     slightly more thorough than scoping to a union, never wrong).
   - Journal the full record as `journal.stack_discovery`. `{{STACK_SUMMARY}}`
     = `stack_discovery.stack_summary`. Phase 2 Screen 6 reconciles it with
     the human (confirms high-confidence findings, resolves anything
     `unresolved`); Phase 5's applicability filter reads the reconciled
     `capabilities.*` fields directly — see Phase 5 step 1.
6. **Fresh vs mature**: mature if the adoption probe chose `adopt-existing`,
   or if any of `TARGET/CLAUDE.md`, `TARGET/.claude/`, `TARGET/.agentic/`
   already exists. Mode changes Phase 4
   behavior (managed blocks, collision prompts) and the Phase 2 git-sync
   default.
7. Detect `{{DEFAULT_BRANCH}}`: `git symbolic-ref refs/remotes/origin/HEAD`
   (fallback: `main` if it exists, else current branch).
8. Journal `phase: "preflight"` + detection results.

## Phase 2 — Interview (role and MCP choices followed by role-relevant screens)

Role selection is explicit: never silently select `developer`, `ba-po`, or any
other role. `--presets a,b` is an explicit non-interactive selection; without
it, Screen 1 must ask the user to choose one or more roles. Record the ordered
selection as `answers.presets` (the legacy singular `answers.preset` may be
read for compatibility, but new installs write only the list). The same
selected union is the only source of scaffolded assets.

The `--defaults` argument accepts detected stack and autonomy defaults only; it
does not invent a role selection. It is valid only when roles were supplied
explicitly with `--presets` or already exist in the install journal.

**Screen 1 — Role presets** (required multi-select): `developer`, `qa`, `ba-po`,
`architect`, `pm-delivery`, `devops`, `portfolio`, `security`, `data`, `design`
— one JSON
each
under `PLUGIN/presets/roles/`.
Display plain-language descriptions before the choices. For example, `ba-po`
means requirements, customer conversations, stories, and acceptance criteria;
it installs no code-writing agents. A `ba-po`-only install must not scaffold
developer instructions or agents. A later run may add roles; union the new
selection with the existing journal and preserve user-owned files.
Union rules (per `PLUGIN/presets/README.md`): `templates`, `generated`,
`sdlc_skills`, and `qe_blueprints` are set-unioned (shared IDs are identical
strings — presets never fork content); `default_hitl` resolves strictest-wins
(`strict > gated-autonomous > autonomous`); every orchestration style in the
union installs, the pre-filled default style comes from the first preset
listed, and `strict` HITL forces the `dispatcher` default.

**Screen 2 — MCP access**: choose exactly one: `connect now`, `configure later`,
or `continue without MCP`. MCP is optional; the latter path supports pasted
tables, CSV extracts, screenshots, and manually supplied Power BI findings.
When connecting now, explain the easiest available route: host directory/
"Add to Cursor", project-local config, or an organization-managed/global
server. Recommend read-only access, OAuth, and environment variables; never
write secrets to the repository. Record `answers.mcp_state` as
`configured`, `deferred`, or `without-mcp`. For configured servers, include
host-specific verification in the generated MCP onboarding guide:
`cursor-agent mcp list`, `cursor-agent mcp login <name>`,
`cursor-agent mcp list-tools <name>` for Cursor; `claude mcp list`,
`claude mcp get <name>`, and `/mcp` for Claude Code. An unavailable server is
not a blocker; record `unavailable` and continue without it.

**Screen 3 — HITL dial**: `strict` / `gated-autonomous` / `autonomous` →
`{{HITL_MODE}}`. Pre-fill from the preset union's strictest `default_hitl`.

**Screen 4 — Autonomy matrix**: may agents run tests? commit? push? create
tickets? (yes/recommend-only per capability). Each answer is compared to that
capability's cell in the active `{{HITL_MODE}}` column of the `ai-policy` matrix;
an answer **stricter** than the mode default (e.g. `recommend-only` where the mode
allows it) becomes a `{{AUTONOMY_OVERRIDES}}` bullet — overrides tighten, never
loosen. Accepting the default for every capability leaves `{{AUTONOMY_OVERRIDES}}`
as the "no overrides" note. Plus `{{MAX_LOC}}`/`{{MAX_FILES}}` (defaults 250/10)
and `{{ESCALATE_ON}}` (default `security,breaking-change,migration,spend`).

**Screen 5 — Gates to enable** (each independently toggleable; all default
on): precommit review gate, subagent output-contract gate, instruction-quality
spawn gate, write-scope guard, human-gated command block, guarded write paths,
migration notice (auto-off when `{{MIGRATIONS_DIR}}` is empty), session
bootstrap. **Session git-sync sub-question (explicit opt-in — hand-off c)**:
`auto-merge` (merge `origin/{{DEFAULT_BRANCH}}` at session start, clean tree
only) vs `warn-only` (fetch + report how far behind). Default: `auto-merge`
for fresh repos, **`warn-only` for mature repos**. Record as
`answers.git_sync_mode`. A disabled gate is neither scaffolded nor wired into
settings (see the Phase 4 settings-merge pruning rule).

**Screen 6 — Stack confirm/correct/fill** (reads `journal.stack_discovery`,
writes back the human-reconciled `capabilities.*` the rest of the install
relies on — this is where discovery becomes ground truth):

When the selected union has no generated slots (for example `ba-po` only),
show `Stack-specific coding agents: not selected for these roles` and do not
ask irrelevant framework, migration, or application-start questions. Continue
to the adapter and readiness summary.

1. **Show, don't re-ask, what's already confident.** One line per capability
   at `confidence ≥ 80` and not in `unresolved`: `<capability>: <applies —
   paradigm/style> (from <matched_profile> | discovered, confidence <n>)`.
   Like Screen 4's gates, these are pre-filled and displayed for the record,
   but — unlike Screen 4 — nothing here is an interactive toggle: there is no
   question to answer, just a summary the user reads before moving on. Also
   show the scalar defaults this seeded: `{{MIGRATIONS_DIR}}`,
   `{{GATE_COMMANDS}}`, `{{MIGRATION_DIFF_COMMAND}}`, `{{ENV_CHECK_COMMANDS}}`,
   `{{APP_START_COMMAND}}`, `{{BASE_URL}}`, `{{TEST_FRAMEWORK}}`.
2. **Ask only the gaps.** For each entry in `journal.stack_discovery.unresolved`
   (capability + ambiguity + candidate values, per `stack-discovery.md`'s
   schema), one `AskUserQuestion` with the named candidates as options plus
   an explicit "none of these — this capability doesn't apply" option. This
   is the **only** per-capability prompting Screen 6 does — a confident
   record (all six curated stacks in `confirm-only` mode, and many `full`-mode
   repos with unambiguous evidence) asks nothing here at all.
3. **Write back the answers.** For each resolved gap, update
   `journal.stack_discovery.capabilities.<cap>` (`applies`, `paradigm` or
   `api_style`/`catalog_format`, `write_scope` if the human's answer implies
   a different location than the guessed one — ask a one-line follow-up for
   the path only if the candidate values didn't already imply it) and remove
   it from `unresolved`. The record in the journal after this screen is the
   one Phase 5 reads — there is no separate "confirmed" copy.
4. **Human-gated commands / write paths / secrets / staging env** (unchanged
   from before Stage 2): ask for `{{HUMAN_GATED_COMMANDS}}` (always seeded
   with `git push origin {{DEFAULT_BRANCH}}`, **plus** any commands the
   matched profile's own "Variable defaults" table recommends adding — e.g.
   nextjs-supabase recommends `supabase db push --linked`; pre-fill the
   union, never just the generic default alone, so a generated agent's claim
   that a stack-specific operation is human-gated is actually true of the
   scaffolded `escalation-policy.md`), `{{GUARDED_WRITE_PATHS}}` (default
   empty; entries may carry a ` => <flow>` suffix naming the allowed flow),
   extra `{{SECRET_DENY_PATTERNS}}` beyond the baked-in `.env*` / `.auth/**` /
   `*token*.env`, and `{{STAGING_ENV_NAME}}`.

**Screen 7 — Adapters**: `{{TICKET_ADAPTER}}` (ADO / Linear MCP / Jira /
GitHub / GitLab / none), `{{TICKET_PREFIX}}`, `{{MR_ADAPTER}}` (`gh` / `glab`
/ MCP / none — pre-fill `gh` when `gh auth status` succeeds and the remote is
GitHub).
Derive `{{TICKET_ADAPTER_STATUS}}` as `configured` only when
`{{TICKET_ADAPTER}}` is not `none`; otherwise render `not configured` and make
the local-work-item fallback visible. Derive `{{MR_ADAPTER_STATUS}}` the same
way from `{{MR_ADAPTER}}`: a repo with no `gh`/`glab`/MCP review path must not
be handed a guide asserting one is configured.

Derive `{{TICKET_INTEGRATION_ENABLED}}` from that same condition, as the bare
JSON literal `true` or `false`. It lands unquoted in `sdlc/config.json`, and
the machine copy must agree with the guide it points at: `enabled: true` beside
an adapter of `none` asserts a ticket surface that does not exist, and a reader
hitting the two has no way to tell which one is lying.

Derived values (no screen): `{{PROJECT_NAME}}` = repo dir name (confirm on
screen 5), `{{STACK_SUMMARY}}` = `journal.stack_discovery.stack_summary`,
`{{ROLE_PRESETS_ACTIVE}}` = comma list from screen 1,
`{{AGENTS_CANONICAL_DIR}}` = the adoption probe's result (`.agentic/agents/`
when nothing was adopted), `{{SKILLS_CANONICAL_DIR}}` and
`{{ORCHESTRATION_STATE_DIR}}` = the probe's results, `{{SCORECARD_PATH}}` =
`docs/audits/instruction-scorecard.json`, `{{SCORE_THRESHOLD}}` = `95`,
`{{OUTPUT_CONTRACT_SECTIONS}}` =
`Summary,Why,Blocking,Non-blocking,Escalate to human`,
`{{AGENTIC_OS_VERSION}}` as defined above.

## Phase 3 — Dependencies

1. Read `PLUGIN/manifest/dependencies.json` (`plugins` array: `name`,
   `marketplace`, `source`, `min`, `optional`, `fallback_source`).
2. Check the active harness's own registry for each plugin at ≥ `min`:
   Claude reads `~/.claude/plugins/installed_plugins.json`, Codex reads
   `codex plugin list`.
3. For each missing/outdated **non-optional** plugin, register it in
   `TARGET/.claude/settings.json` (create the file if absent) via deep-merge:
   - `extraKnownMarketplaces.<marketplace>` ← its `source` object (use
     `fallback_source` only if the primary is known to be unavailable);
   - `enabledPlugins` ← append `"<name>@<marketplace>"` if absent.
   **Unpinned-source guard**: if a dependency's `source` (or the fallback you
   would use) contains the placeholder `OWNER/`, do **not** register it —
   record it in `journal.follow_ups` as
   `pending-source-pin: <name> (marketplace coordinate unpinned)` and warn the
   user that the marketplace coordinate is unpinned and will be fixed by the
   release process; never write a placeholder repo into their settings.
4. Optional plugins (e.g. `ponytail`): offer, don't force.
5. Announce: **newly registered plugins require a session restart**;
   `/agentic-doctor` reports them as `pending-restart` until they appear in
   `installed_plugins.json`.
6. Record the union's `sdlc_skills` and `qe_blueprints` in the journal
   (informational — both run from their own plugin; nothing is copied).
   `agentic-qe` is an optional dependency: if a preset in the union names
   blueprints and the plugin is absent, offer to register it and carry on
   either way — the blueprints are methodology references, so their absence
   degrades guidance rather than breaking the install.
7. Journal `phase: "dependencies"`.

## Phase 4 — Scaffold

Render/copy every template ID in the preset union. Destination map (IDs from
`PLUGIN/templates/VARIABLES.md` § Template IDs; sources under
`PLUGIN/templates/`):

| Template ID(s) | Source | Destination in TARGET |
|---|---|---|
| `hooks/precommit-review-gate` | `hooks/claude/precommit_review_gate.py` | `.claude/hooks/precommit_review_gate.py` (verbatim) |
| `hooks/subagent-gate` | `hooks/claude/subagent_gate.py.tmpl` | `.claude/hooks/subagent_gate.py` |
| `hooks/instruction-gate` | `hooks/claude/instruction_gate.py.tmpl` | `.claude/hooks/instruction_gate.py` |
| `hooks/instruction-stale-notice` | `hooks/claude/instruction_stale_notice.py` | `.claude/hooks/instruction_stale_notice.py` (verbatim) |
| `hooks/write-scope-guard` | `hooks/claude/write_scope_guard.py.tmpl` | `.claude/hooks/write_scope_guard.py` |
| `hooks/session-bootstrap` | `hooks/claude/session_start_bootstrap.py.tmpl` | `.claude/hooks/session_start_bootstrap.py` |
| `hooks/precompact-checkpoint` | `hooks/claude/precompact_checkpoint.py` | `.claude/hooks/precompact_checkpoint.py` (verbatim) |
| `hooks/session-learnings-notice` | `hooks/claude/session_learnings_notice.py` | `.claude/hooks/session_learnings_notice.py` (verbatim) |
| `hooks/context-monitor` | `hooks/claude/context_monitor.py` | `.claude/hooks/context_monitor.py` (verbatim) |
| `hooks/prompt-scan-guard` | `hooks/claude/prompt_scan_guard.py` | `.claude/hooks/prompt_scan_guard.py` (verbatim) |
| `hooks/human-gated-commands` | `hooks/claude/human_gated_commands.py.tmpl` | `.claude/hooks/human_gated_commands.py` |
| `hooks/guarded-write-paths` | `hooks/claude/guarded_write_paths.py.tmpl` | `.claude/hooks/guarded_write_paths.py` |
| `hooks/migration-notice` | `hooks/claude/migration_notice.py.tmpl` | `.claude/hooks/migration_notice.py` — **skip when `{{MIGRATIONS_DIR}}` is empty** |
| `hooks/lint-on-save` | `hooks/claude/lint_on_save.py.tmpl` | `.claude/hooks/lint_on_save.py` — **skip when `{{LINT_CHECK_COMMAND}}` is empty** |
| `hooks/settings-fragment` | `hooks/settings-fragment.json.tmpl` | deep-merged into `.claude/settings.json` (never copied as a file) |
| `githooks/pre-commit` | `githooks/pre-commit` | `.githooks/pre-commit` (verbatim) |
| `scripts/install-git-hooks` | `scripts/install-git-hooks.sh` | `scripts/install-git-hooks.sh` (verbatim) |
| `governance/claude-section` | `governance/CLAUDE.section.md.tmpl` | managed block inside `CLAUDE.md` (repo root) |
| `governance/agents` | `governance/AGENTS.md.tmpl` | `AGENTS.md` (repo root) |
| `governance/patterns` | `governance/PATTERNS.md.tmpl` | `PATTERNS.md` (repo root) |
| `governance/agent-registry` | `governance/agent-registry.md.tmpl` | `.agentic/guides/agent-registry.md` |
| `policy/ai-policy`, `policy/escalation-policy`, `policy/safety-policy` | `policy/<name>.md.tmpl` | `.agentic/guides/policy/<name>.md` |
| `guides/<name>` | `guides/standards/<name>.md`, or `<name>.md.tmpl` when one exists | `.agentic/guides/standards/<name>.md` (rendered if `.tmpl`, else verbatim) |
| `agents/<name>` | `agents/core/<name>.md.tmpl` or `agents/qa/<name>.md.tmpl` | `.agentic/agents/<name>.md` + two synthesized pointers (below) |
| `commands/pipeline-orchestrator`, `commands/dispatch` | `commands/core/<name>.md.tmpl` | `.claude/commands/<name>.md` (commands are canonical there — the exception noted in `agent-registry.md.tmpl`) |
| `sdlc/config` | `sdlc/config.json.tmpl` | `.agentic/agentic-sdlc/config.json` |
| `sdlc/project` | `sdlc/project.md.tmpl` | `.agentic/guides/project.md` |

Ordered steps:

1. **Hooks.** Render/copy per the map. Two installer-side conditionals:
   - `hooks/human-gated-commands` and `hooks/guarded-write-paths` are
     scaffolded whenever `hooks/settings-fragment` is in the union even if no
     preset lists them — the fragment wires
     `python3 .claude/hooks/human_gated_commands.py` and
     `.../guarded_write_paths.py`, and a wired-but-missing PreToolUse hook
     script blocks every tool call (`python3 <missing>` exits 2). With empty
     lists both hooks are safe no-ops.
   - **Hand-off (c), git-sync opt-in**: when `answers.git_sync_mode` is
     `warn-only`, after substituting `{{DEFAULT_BRANCH}}`/`{{ENV_CHECK_COMMANDS}}`
     into `session_start_bootstrap.py`, replace this exact block inside
     `git_sync_notes()`:

     ```python
         code, out = run_git("merge", "--no-edit", f"origin/{DEFAULT_BRANCH}")
         if code == 0:
             notes.append(f"[git-sync] git merge origin/{DEFAULT_BRANCH} (on branch `{branch}`) — ok")
         else:
             run_git("merge", "--abort")
             notes.append(
                 f"[git-sync] merge of origin/{DEFAULT_BRANCH} into `{branch}` FAILED (aborted): {out}"
             )
         return notes
     ```

     with:

     ```python
         code, out = run_git("rev-list", "--count", f"HEAD..origin/{DEFAULT_BRANCH}")
         if code == 0 and out and out != "0":
             notes.append(
                 f"[git-sync] branch `{branch}` is {out} commit(s) behind origin/{DEFAULT_BRANCH} "
                 "— auto-merge is off (warn-only); merge manually when ready."
             )
         return notes
     ```

     Then `python3 -m py_compile .claude/hooks/session_start_bootstrap.py` to
     prove the patch applied cleanly. Journal `template:
     "hooks/session-bootstrap"` either way.
   Also append these local-state paths to the target's `.gitignore`
   (append-if-absent, idempotent — the review stamp committed to a repo would
   make a fresh clone believe a diff was already approved):
   `.claude/.review-stamp`, `.claude/checkpoints/`, `.agentic/state/`.
2. **Settings deep-merge.** Merge the rendered fragment into
   `.claude/settings.json`: objects merge recursively; **arrays are
   set-unions, append-if-absent** (never reorder or drop existing entries);
   scalar conflicts keep the existing value and are reported. Add
   interview-provided extra `{{SECRET_DENY_PATTERNS}}` as
   `Read(<pattern>)` entries into `permissions.deny` (the three defaults are
   already baked into the fragment). **Pruning rule**: drop any hook command
   entry whose script file was not scaffolded (disabled gate, or
   `migration_notice.py` skipped for empty `{{MIGRATIONS_DIR}}`). **Show the
   user a unified diff of `.claude/settings.json` (old → merged) and get
   confirmation BEFORE writing** — this is a hard mature-repo rule even on
   fresh installs.
3. **Git hooks** — only when `githooks/pre-commit` is in the preset union
   (the ba-po, pm-delivery, security, data, and design unions exclude the git layer; installing the
   native hook there would reference an absent
   `.claude/hooks/precommit_review_gate.py`). Copy `.githooks/pre-commit` +
   `scripts/install-git-hooks.sh`,
   then run `bash scripts/install-git-hooks.sh`. The script is the documented
   chaining mechanism: a pre-existing foreign `pre-commit` (no `agentic-os:`
   marker) is preserved as `pre-commit.local` and chained after the gate —
   never overwritten. If it reports an existing `.local` conflict, surface
   that to the user verbatim.
4. **Governance.**
   - `CLAUDE.md`: render `CLAUDE.section.md.tmpl` (it already carries the
     `<!-- agentic-os:begin v{{AGENTIC_OS_VERSION}} -->` /
     `<!-- agentic-os:end -->` markers). No `CLAUDE.md` ⇒ create it with the
     block as its body. Existing `CLAUDE.md` ⇒ append the block at the end
     (or replace an existing agentic-os block between markers); **never touch
     content outside the markers**. Write it with init's merge rule ("How
     journal and file writes happen"): a `CLAUDE.md` agentic-os created stays
     `managed`; one that pre-existed is merged under `expect_sha256` and stays
     user-owned.
     The block must promise only what this union installs (the same
     must-not-index principle as `{{QA_GUIDE_ROWS}}`); three derived
     substitutions enforce that:
     - `{{WRITE_SCOPE_RULE}}` — when `hooks/write-scope-guard` is in the
       union, the bullet citing `.claude/hooks/write_scope_guard.py` as the
       enforcement layer; otherwise the same rule without the hook citation
       (`**Respect your \`write_scope\` absolutely.** Writing outside it is an
       orchestration error — stop and escalate.`). Never empty.
     - `{{REVIEW_GATE_SECTION}}` — the "Blind code review before every
       commit" section, **only when `hooks/precommit-review-gate` and
       `githooks/pre-commit` are both in the union**; else the empty string
       (a preset with no git layer must not mandate a pre-commit gate it
       does not install). When the union has the gate but not
       `agents/blind-code-reviewer` (the devops union), emit the variant
       whose workflow step asks for an independent review of the staged
       diff instead of instructing a spawn of the uninstalled agent. The
       non-empty value ends in a blank line so the empty value collapses
       without leaving double blank lines.
     - `{{QUALITY_GATES_SECTION}}` — the "Quality gates" section, **only
       when `guides/quality-gates` is in the union**; else the empty string.
       Substitute it (and `{{REVIEW_GATE_SECTION}}`) **before** the
       scalar/list pass — the section body contains `{{GATE_COMMANDS}}`,
       which must still render.
   - `AGENTS.md`: absent ⇒ write the rendered file whole (owner `managed`).
     Present ⇒ wrap the rendered content in the same begin/end markers and
     append; content outside markers is untouched.
     Substitute `{{FLEET_INVARIANTS}}` (the "Fleet invariants" numbered list)
     under the same promise-only-what-is-installed contract, **renumbered
     contiguously** so a dropped invariant leaves no gap: the write-scope
     invariant is always present but cites
     `.claude/hooks/write_scope_guard.py` only when `hooks/write-scope-guard`
     is in the union (else it states the rule as stop-and-escalate with the
     humans in the loop as the enforcement layer); the instruction-quality
     invariant renders **only when `hooks/instruction-gate` is in the union**
     (its repair path names the `instruction-auditor` iff
     `agents/instruction-auditor` is in the union, else a human re-grade); the
     blind-review invariant renders **only when `hooks/precommit-review-gate`
     and `githooks/pre-commit` are both in the union** (mirroring
     `{{REVIEW_GATE_SECTION}}`); the orchestrator-only-spawning, read-only
     gate-agent, output-contract, and escalation-over-improvisation invariants
     render in every install (every preset ships `hooks/subagent-gate`, so its
     citation stays). Never empty.
   - `PATTERNS.md`: absent ⇒ write. Present ⇒ **collision prompt** (step 6).
     Substitute `{{QA_GUIDE_ROWS}}` with the `test-design-pattern` + `flaky-protocol`
     index rows **only if those guides are in the install** (the `qa` preset), else
     the empty string — the index must never link a guide the preset did not install.
     Substitute `{{OPS_GUIDE_ROWS}}` the same way: the `incident-triage.md` index
     row iff `guides/incident-triage` is in the union (the `devops` preset), else
     the empty string. Substitute `{{SEC_GUIDE_ROWS}}` the same way: the
     `threat-modeling.md` index row iff `guides/threat-modeling` is in the union
     (the `security` preset), else the empty string. Substitute
     `{{DATA_GUIDE_ROWS}}` the same way: the `data-pipeline-design.md` index row
     iff `guides/data-pipeline-design` is in the union (the `data` preset), else
     the empty string. Substitute `{{DESIGN_GUIDE_ROWS}}` the same way: the
     `experience-design.md` index row iff `guides/experience-design` is in the
     union (the `design` preset), else the empty string. (Same principle as
     agent-registry row pruning below.)
     Substitute `{{CORE_GUIDE_ROWS}}` under the same contract: one index row per
     guide of `git-workflow`, `code-quality`, `quality-gates`,
     `instruction-quality-rubric`, `qa-strategy-stub` — **only the ones whose
     `guides/<name>` ID is in the union**, in that fixed order, each row ending in
     a newline. A union installing none of the five renders the empty string; the
     static working-with-agents and evidence-integrity rows (installed by every
     preset) keep the table non-empty.
     Substitute `{{BA_PO_GUIDE_ROWS}}` under the same contract again: one index
     row per installed guide of `guides/ba-po-operating-model` and
     `guides/mcp-onboarding` (the `ba-po` preset — these reach `PATTERNS.md` only
     in multi-role unions, since ba-po alone does not install
     `governance/patterns`), else the empty string.
   - `agent-registry.md` → `.agentic/guides/agent-registry.md`, then apply
     **hand-off (b), row pruning**: the template documents that "the installer
     removes rows whose preset is not installed" — delete every row of the
     orchestration matrix whose *owning asset* (agent contract or command
     file) is not in the resolved union. Concretely: qa-preset rows
     (`test-case-generator`, `test-automation-author`, `test-case-syncer`,
     `test-failure-triage`, `work-item-creator`) go unless `qa` is installed;
     the `dispatcher` row goes unless `agents/dispatcher` is in the union;
     `security-reviewer` / `pr-pipeline-gate` rows go unless their agent IDs
     are in the union; the `incident-triage` row goes unless
     `agents/incident-triage` is in the union; the `threat-modeler` row goes
     unless `agents/threat-modeler` is in the union; the `pipeline-designer` row
     goes unless `agents/pipeline-designer` is in the union; the
     `experience-designer` row goes unless `agents/experience-designer` is in
     the union; the
     `pipeline-orchestrator.md` / `dispatch.md` rows go unless the matching
     command ID is in the union; skill-owned rows (Owning asset of the form
     ``the agentic-sdlc `<name>` skill``) go unless `<name>` is in the
     union's `sdlc_skills` set (the union of every installed preset's
     `sdlc_skills` array); blueprint-owned rows (Owning asset of the form
     ``the agentic-qe `<id>` blueprint``) go unless `<id>` is in the union's
     `qe_blueprints` set, by the same rule and for the same reason — a row
     naming an asset this install did not select is a promise the repo cannot
     keep. Never prune the
     `blind-code-reviewer` or `instruction-auditor` rows when their agents
     install. **Never prune the `<!-- generated-agent-rows -->` marker row**
     (the one with an empty "Owning asset" cell, below the curated rows) —
     this list is exhaustive, that row is not an omission from it. It isn't
     a routable intent at all, so "owning asset not in the resolved union"
     does not apply to it the way it applies to the real rows above; pruning
     it here would delete the one anchor Phase 5 step 6 needs to append
     generated-agent rows later in this same install.
     Substitute `{{ORCHESTRATION_STYLE_RULE}}` (the "Multi-step work" bullet
     under § Orchestration rules) with the variant matching the installed
     command set — the bullet must not name a default the union does not
     install: both commands ⇒ the mode-dependent default rule (`strict`
     installs default to `dispatch`; `gated-autonomous`/`autonomous` default
     to `pipeline-orchestrator`); `commands/dispatch` only ⇒ "goes through
     `dispatch` — the only orchestration command in this install; each step
     is user-invoked."; `commands/pipeline-orchestrator` only ⇒ "goes through
     `pipeline-orchestrator` — the only orchestration command in this
     install."; neither ⇒ "is orchestrated by the human — this install has no
     orchestration command." Never empty.
5. **Policies, guides, sdlc adapters.** Render/copy per the map.
   **Existing-guide rule (hard)**: a destination guide file that already
   exists is **skipped** and journaled with `owner: "user"` and the *current*
   file's sha256 — the upgrade skill then knows never to touch it.
   **`quality-gates.md` is rendered, not copied**: substitute `{{GATE_ENTRIES}}`
   with one gate block per `GATE_COMMANDS` line —
   `### <cmd>` / **Run**: `` `<cmd>` `` / **Pass**: exits 0 / **Fail**: non-zero
   exit, fix the cause / **Skip if**: never — the command serving as both name and
   `Run`. If `GATE_COMMANDS` is empty, write a one-line instruction to add a gate,
   never a blank registry (`code-quality.md` treats this file as the canonical gate
   catalogue and forbids relying on an empty one).
   **`ai-policy.md` `{{ENFORCEMENT_LAYER_ROWS}}`**: substitute with the
   hook-backed rows of the "Enforcement layers" table — pre-commit review
   stamp (**only when `hooks/precommit-review-gate` and `githooks/pre-commit`
   are both in the union**), output-contract gate (iff `hooks/subagent-gate`),
   write-scope guard (iff `hooks/write-scope-guard`), instruction-quality gate
   (iff `hooks/instruction-gate`) — in that fixed order, each emitted row
   ending in a newline so absent rows collapse without breaking the GFM table.
   The two soft/settings rows stay in the template, so the table is never
   empty. The instruction-gate row nests `{{SCORECARD_PATH}}`; substitute this
   variable **before** the scalar/list pass so it still renders. A policy that
   lists an enforcement layer the union does not install is the same defect
   class `{{REVIEW_GATE_SECTION}}` exists to prevent.
   **`ai-policy.md` `{{AUTONOMY_OVERRIDES}}`**: substitute with one bullet per
   Screen-4 capability the user set **stricter** than its active-mode cell. Only a
   `recommend-only` answer can tighten (→ `gated`); a `yes` answer is never stricter
   than a cell that already permits the action, so it yields no bullet. Bullet shape:
   `- **<capability>** — gated (tightened from the active mode's `<default level>`).
   <one line on what that means for an agent.>` — write the mode's **actual name**
   and the cell's **actual level** (`allowed`/`gated`/`never`) as literal text, not
   `{{…}}` tokens: this block is itself the value substituted for
   `{{AUTONOMY_OVERRIDES}}`, so a token you leave inside it may not be resolved
   again. When nothing was tightened (every `--defaults` install, and any interview
   that accepted the mode defaults), substitute the single line `_No per-repository
   overrides — every capability follows the active mode's row above._`
   **Hand-off (a)**: when the `qa` preset is in the union, create an empty
   ledger at `docs/flaky-ledger.md` if absent (it is referenced by
   `.agentic/guides/standards/flaky-protocol.md`) with just:

   ```markdown
   # Flaky-test ledger

   | Spec | Work item | First seen | Root cause | Fix / re-enable condition | Status |
   |---|---|---|---|---|---|
   ```
6. **Collision prompt (all other name collisions).** Any destination file that
   exists, is not journaled, and is not covered by the managed-block or
   existing-guide rules ⇒ AskUserQuestion per file:
   **skip (default)** → journal `owner: "user"`; **rename** → write ours as
   `ao-<name>` alongside (journal the `ao-` path, owner `managed`);
   **overwrite** → a confirmed `install.apply` of the bytes shown; the file
   stays user-owned. Never overwrite silently.
7. **Templated-agent pointers.** For every `agents/<name>` in the union, after
   rendering the canonical contract to `.agentic/agents/<name>.md`, synthesize
   the two thin pointers exactly per the pointer formats in
   `PLUGIN/generators/agent-generator.md` (§ "2. Claude agent pointer" and
   § "3. Command pointer"): `.claude/agents/<name>.md` (frontmatter `name`,
   `description`, `tools` — `Read, Grep, Glob` for read-only gates, plus
   `Edit, Write, Bash` for writers — `model: inherit`; body points at the
   canonical contract) and `.claude/commands/<name>.md` (arguments + read-first
   list + write scope + ≤8-bullet digest). Pointers are thin — never restate
   the rule set. Owner `managed`, `template: "derived"`.
8. **Seed the instruction-quality scorecard** — ALWAYS runs when
   `hooks/instruction-gate` is in the union, regardless of whether Phase 5 has
   anything to generate (a qa-only union has `generated: []` but still spawns
   governed agents). Rationale: `instruction_gate.py` blocks the spawn of any
   agent whose checked files (its canonical contract, its
   `.claude/agents/<name>.md` pointer, `CLAUDE.md`/`AGENTS.md`/`PATTERNS.md`,
   and every `.agentic/guides/*.md` the contract cites) are absent from the
   scorecard — without seeding, a fresh install spawn-blocks the entire
   fleet. Create `docs/audits/instruction-scorecard.json` and seed one entry
   for **each** of: every canonical contract landed in
   `{{AGENTS_CANONICAL_DIR}}`, every `.claude/agents/<name>.md` pointer,
   `CLAUDE.md`, `AGENTS.md`, `PATTERNS.md`,
   `.agentic/guides/agent-registry.md`, and every scaffolded
   `.agentic/guides/**/*.md` file. Entry shape:

   ```json
   {"content_sha256": "<sha256 of the RENDERED file on disk>",
    "composite_score": 100,
    "source": "template-inherited"}
   ```

   Template content ships pre-audited (validated by the repo's CI acceptance
   matrix before release), so inheriting a
   passing score is sound; any local edit makes the entry stale by hash, the
   stale-notice hook flags it, and the gate then blocks until the file is
   re-graded via the instruction-auditor. Phase 5 step 5 later **overwrites**
   the entries of generated files with their real audited scores.
9. Journal every written file (`sha256`, `template`, `owner`) and set
   `phase: "scaffold"`.

## Phase 5 — Generate (one subagent per gen/* slot)

Skip entirely when the union's `generated` set is empty (any all-no-code
union — qa, ba-po, pm-delivery, portfolio, security, data, design). Otherwise:

1. **Applicability filter — capability-driven** (the flip from Stage 1: this
   now reads `journal.stack_discovery.capabilities` directly, not the matched
   profile's prose list — this is what makes a non-curated stack's `full`-mode
   discovery produce real writer agents instead of nothing). By the time this
   step runs, Phase 2 Screen 6 has already resolved every entry that was in
   `unresolved` to a definite answer — including "none of these, it doesn't
   apply" as a valid, definite answer — so every capability's `applies`/
   paradigm here is either a high-confidence discovery finding or a direct
   human decision, never a guess. Per-slot rule (see the table's
   Applicability column). A capability with `applies: false` skips its
   slot(s) silently (a true fact, not a gap); journal every skipped slot in
   `follow_ups` regardless of why, so `/agentic-doctor` can report what was
   and wasn't generated. There is no `generic-fallback.md` special case
   anymore — a repo with zero applicable capabilities (e.g. a genuinely
   stateless service) simply produces `generated: []` for this install, the
   same shape any of the seven no-code unions already produces;
   `generic-fallback.md` becomes a documentation stub pointing here (Stage 3
   cleans up its wording).
2. **Slot definitions** (installer-owned; the generator narrows `write_scope`/
   `forbidden_paths` to real directories, never widens):

   | Slot | Kind | Purpose | Applicability | write_scope seed | forbidden seed |
   |---|---|---|---|---|---|
   | `gen/schema-architect` | writer | migrations/schema + access-control DDL | `persistence.applies` and `paradigm != external-or-none` | `{{PERSISTENCE_WRITE_SCOPE}}` | `capabilities.server_writes.write_scope`, `capabilities.ui.write_scope` |
   | `gen/api-author` | writer | server-side mutation/endpoint idiom | `server_writes.applies` | `capabilities.server_writes.write_scope` | `{{PERSISTENCE_WRITE_SCOPE}}`, `capabilities.ui.write_scope` |
   | `gen/component-generator` | writer | UI components/views per the repo's rendering paradigm | `ui.applies` and `paradigm != none` (covers both `component-framework` and `template-engine` — e.g. Rails views/Hotwire count, per `stack-profiles/rails.md`) | `capabilities.ui.write_scope` | `{{PERSISTENCE_WRITE_SCOPE}}`, `capabilities.server_writes.write_scope` |
   | `gen/migration-validator` | read-only gate | deterministic PASS/FAIL migration review | `persistence.applies` and `paradigm == migration-managed` (a `model-defined-no-migration` stack has no migration files to validate — no migration gate, not a degraded one) | `[]` (readonly) | `**` |
   | `gen/i18n-agent` | writer | locale/message catalogs in lockstep | `i18n.applies` | `capabilities.i18n.write_scope` | everything else |
   | `gen/stack-guides` | writer (guides) | stack coding guides cited by the agents | always | `.agentic/guides/{data,api,development,architecture}/` | agents, hooks, app code |

   All `capabilities.*` paths above are `journal.stack_discovery.capabilities.<cap>.<field>` after Screen 5's reconciliation. Only persistence's write location has a registered `{{VAR}}` (`{{PERSISTENCE_WRITE_SCOPE}}`, `templates/VARIABLES.md`) — Stage 1 introduced it specifically because `gen/schema-architect`'s slot seed predates capability-driven applicability and was already a named variable (`{{MIGRATIONS_DIR}}**`) before this stage. `server_writes`/`ui`/`i18n` write locations never had a named variable to begin with — they were "per stack profile" prose seeds — so this stage reads their journal paths directly rather than minting three more single-use `{{VAR}}`s for values only the Phase 5 subagent prompt ever consumes (step 3, input block 1 passes the whole record already).

3. **Spawn** (parallel, one subagent per slot). Prompt = the full text of
   `PLUGIN/generators/agent-generator.md` (for `gen/stack-guides`:
   `PLUGIN/generators/guide-generator.md`) with its `{{VAR}}` placeholders
   substituted, then append the input blocks it defines: (1) `journal.stack_discovery`
   — the structured record from Phase 1 step 4, not the raw profile file (in
   `confirm-only` mode the record was itself derived from
   `PLUGIN/generators/stack-profiles/<profile>.md`, so this is a strict
   superset of what was passed here before Stage 1), (2) the slot
   definition row above, (3) the exemplar —
   `PLUGIN/generators/exemplars/schema-architect.md` for writer slots against
   a DB/API stack, `PLUGIN/generators/exemplars/test-automation-author.md` for
   test-authoring slots, (4) the rubric **as scaffolded in Phase 4** at
   `.agentic/guides/standards/instruction-quality-rubric.md`. Run
   `gen/stack-guides` **first** (generated agent contracts cite its guides),
   then the agent slots in parallel.
4. **Audit loop** (per generated contract): spawn an auditor subagent whose
   prompt is the scaffolded `.agentic/agents/instruction-auditor.md` contract,
   target = the generated canonical contract. Grade against the rubric.
   - `composite_score ≥ 95` → accept.
   - Below → regenerate with the auditor's findings appended to the generator
     prompt, **at most 2 retries**.
   - Still below after retries → **install anyway** (deliberate policy — a below-threshold generated agent must never block the whole install):
     record the file in `docs/audits/instruction-scorecard.json` with
     `"gate_threshold": <achieved score>` so
     `.claude/hooks/instruction_gate.py` gates at the achieved level instead
     of hard-blocking; print a visible warning; append a follow-up entry to
     `journal.follow_ups` ("regenerate <name> to ≥95").
5. **Scorecard update.** The scorecard file already exists (Phase 4 step 8
   seeded every templated asset). Here, **overwrite/add entries for generated
   files only**, in the shape `instruction_gate.py` reads:
   `{"files": {"<rel path>": {"content_sha256": "<sha256>", "composite_score": <n>, "gate_threshold": <n, only when relaxed per decision 6>, "source": "..."}}}`.
   Three kinds of generated file, two scoring rules:
   - **The generated canonical contract** (`{{AGENTS_CANONICAL_DIR}}<name>.md`) and
     **every generated `.agentic/guides/**/*.md` guide** — their **real audited**
     `composite_score` (from step 4 for a contract, the guide-generator's evidence
     audit for a guide), plus `gate_threshold` when relaxed per decision 6.
     `source: "generated"`.
   - **The `.claude/agents/<name>.md` pointer** — a thin derived file (frontmatter
     + "read the canonical contract"); step 4 audits the *contract*, never the
     pointer, so there is nothing to grade independently. **Inherit the canonical
     contract's `composite_score` (and `gate_threshold`, if it shipped relaxed)
     verbatim**; `source: "derived-from-contract"`. This is the generated analogue
     of Phase 4's `template-inherited` pointer seeding: `instruction_gate.py` checks
     the pointer's *own* entry on every spawn (`own_pointer` in `check_paths`), so it
     must carry a score, and a thin pointer's quality is entirely its contract's.

   Never touch the `template-inherited` entries for files this phase did not produce.
6. **Registry rows** (you, the orchestrator, do this — **never** a generator
   subagent: slots run in parallel per step 3 and `.agentic/guides/agent-registry.md`
   is one shared file, so a parallel per-slot append would race). Skip this
   step if `.agentic/guides/agent-registry.md` wasn't scaffolded (Phase 4).
   After every slot in this pass has an audited contract (accepted, retried,
   or installed degraded per step 4 — never skip a slot here just because it
   scored low), for each **writer or gate** slot that actually applies this
   run (`gen/stack-guides` doesn't get a row — it's not dispatchable, it only
   feeds the other contracts):
   - **Regeneration case**: if a row already cites this slot's exact
     `{{AGENTS_CANONICAL_DIR}}<name>.md` path in the "Owning asset" column,
     **replace that row** — never leave a stale duplicate from a prior
     install/upgrade pass.
   - **Fresh case**: otherwise, insert a new row directly below the table row
     whose first cell is the literal `<!-- generated-agent-rows -->` marker
     (a real, mostly-empty table row in `agent-registry.md.tmpl`,
     `templates/governance/agent-registry.md.tmpl` — not a standalone
     comment line; never remove or edit that marker row itself) — or below
     the last row this step already inserted in this same pass, when
     generating more than one slot at once, so multiple fresh rows land in
     slot-processing order rather than each pushing the previous one down —
     in the existing
     table's column order:
     `| <intent> | {{AGENTS_CANONICAL_DIR}}<name>.md | owner: generated; <note> |`
     - `<intent>`: paraphrase the slot's Purpose from the table above into
       the same style as the table's other rows — don't copy Purpose
       verbatim, its wording doesn't match this table's convention. Example:
       Purpose `"migrations/schema + access-control DDL"` (for
       `gen/schema-architect`) → intent `"Design/modify persistence
       schema"`.
     - `<note>`: one line — the single most operationally significant
       trigger from the generated contract's own `## Escalate to human`
       section. If it lists several, pick the one that fires on every
       invocation (e.g. a permanent risk flag from `escalation-policy.md`'s
       `escalate_on` list) over a conditional one; don't try to summarize
       the whole list. **Escape any literal `|` in the sourced text as
       `\|`** (or reword around it) — both `<intent>` and this field land
       inside a GFM table cell, and an unescaped pipe opens an extra cell.
       The row still renders (GFM does not break the table, and later rows
       survive), but every cell past the table's column count is **silently
       discarded** — so the note is truncated with no error anywhere, which
       is worse than a visible break.
   Read each generated contract's actual triggers/escalation section for the
   note — don't invent one. This is what makes `pipeline-orchestrator.md`
   (which spawns agents by reading this exact table) actually able to
   discover generated writer agents automatically instead of only via
   explicit `/slash-command` invocation.
6b. **Guide-index rows** (you, the orchestrator, not a generator subagent — same
   race reason as step 6: `PATTERNS.md` is one shared file). Skip if `PATTERNS.md`
   wasn't scaffolded (Phase 4). Unlike the agent rows in step 6, these are
   **fully derived** — one row per generated stack guide, its label fixed by the
   guide's path — so they are *rebuilt*, never hand-edited, and `/agentic-upgrade`
   regenerates them from the journal the same way (no three-way split needed).

   **Rebuild** the contiguous run of table rows directly below the row whose first
   cell is the literal `<!-- generated-guide-rows -->` marker (a real, mostly-empty
   table row in `templates/governance/PATTERNS.md.tmpl` — not a standalone comment;
   never remove or edit the marker row itself): delete whatever rows are there, then
   emit one `| <label> | [`<path>`](<path>) |` row, **in this table's order**, for
   each guide in this fixed set that `gen/stack-guides` produced this run — i.e.
   whose file is present on disk. `gen/stack-guides` reduces an absent domain to a
   short stub rather than skipping it (`generators/guide-generator.md`), so a stub
   is a real file and still earns its row; only a guide never produced at all is
   omitted:

   | Guide path | Label |
   |---|---|
   | `.agentic/guides/data/database-patterns.md` | Database (schema, migrations, access control) |
   | `.agentic/guides/api/api-patterns.md` | API (endpoints, validation, response envelope) |
   | `.agentic/guides/development/development-practices.md` | Development practices (layout, auth, data flow) |
   | `.agentic/guides/development/security-patterns.md` | Security (trust boundaries, secrets, authz) |
   | `.agentic/guides/architecture/architecture.md` | Architecture (system layout, module boundaries) |

   The label is fixed by path, not paraphrased, precisely so an upgrade can
   reproduce the exact same row from the journal without re-reading the guide.
7. Journal every generated file with `owner: "generated"`, `template:
   "gen/<slot>"` — generator subagents return content and the orchestrator
   writes it with `install.apply`; the index-file re-stamps below are likewise
   `install.apply` of the mutated content, never a direct write. If step 6 changed `.agentic/guides/agent-registry.md` or step 6b
   changed `PATTERNS.md` this pass, **each** changed index file needs **two**
   re-stamps — both against its current on-disk `sha256` **after** the mutation,
   since Phase 4 journaled and scored it *before* that mutation and neither stamp
   self-updates:
   - **Journal**: re-record its `sha256` (`owner: "managed"`, `template`
     unchanged). Skipping this makes `/agentic-upgrade` see `current sha !=
     recorded sha` on every future run and treat the file as user-modified.
     Both index files are handled specially by `/agentic-upgrade` rather than
     left as an ordinary managed-file diff-and-ask, because a plain "overwrite
     with `NEWRENDER`" strips their generated rows (the template has none):
     see `skills/agentic-upgrade/SKILL.md` § Agent registry (preserved via a
     three-way split — the rows carry hand-authored intent) and § Guide index
     (regenerated from the journal — the rows are fully derived from the
     generated-guide set).
   - **Scorecard**: update its `docs/audits/instruction-scorecard.json`
     entry's `content_sha256` to match, keeping `composite_score: 100` and
     `source: "template-inherited"` — the appended rows follow this step's
     strict mechanical format, not free-form prose, so they don't need a
     fresh `instruction-auditor` pass the way a generated contract does.
     Skipping this leaves the *old* pre-mutation hash on record;
     `.claude/hooks/instruction_gate.py`'s SubagentStart check treats that
     as "graded content went stale" for **every** agent whose contract cites
     this guide (`dispatcher.md` does, unconditionally) and hard-blocks its
     spawn — on every install that generates at least one writer/gate slot,
     immediately, until a human happens to run `/instruction-auditor`.
   Set `phase: "generate"`.

## Phase 6 — Verify

Invoke the `agentic-doctor` skill (same plugin). It writes
`.agentic/agentic-os/doctor.json`. Treat any `failures` entry as work to fix
before declaring the install done; `pending_restart` entries are expected on
first install (Phase 3 notice).

## Phase 7 — Final report

Set `phase: "done"`, stamp `agentic_os_version`, and report: presets
installed, HITL mode, files written (managed/user/generated counts), relaxed
generated agents (if any), pending-restart plugins, and the doctor verdict.
Also report MCP status (`configured`, `deferred`, `without-mcp`, or
`unavailable`), the selected-role capabilities, and three first-task prompts
appropriate to the role set. For `ba-po`, include examples involving Excel,
Power BI, customer requirements, and team clarification questions.
Remind the user: review the diff, then commit it themselves; run
`bash scripts/install-git-hooks.sh` once per fresh clone.
