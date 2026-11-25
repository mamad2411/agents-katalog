---
name: "fw-adopt"
description: "Attach the current coding agent's FireWeave standing loop to a repo that is already initialised (harness, credentials, agent-instructions present). Writes only agent standing instructions + hooks — never re-scaffolds the harness, never rotates the project API key. Use when a teammate clones an initialised repo and opens Claude Code / Cursor / another agent that was not present at initialise time, or when the user asks to \"adopt this repo\", \"install FireWeave for my agent\", or invokes `/fireweave:adopt`. `--check` reports the wanted-vs-present diff without writing."
---
> Interaction: there is no skill-callable prompt tool — gate each decision by STOP and ask the user to pick a labelled option (or move the gate into the bundled MCP server via Elicitation).

# Adopt (attach my agent to an already-initialised repo)

Run when the **repo is already FireWeave-initialised** and this machine's coding agent is
missing the standing loop (HARD ORDER + hooks). Typical cases:

1. Repo was initialised before team-agent selection existed (Cursor-only disk detect) — teammate opens Claude.
2. First init selected `teamAgents` but a new agent joins later that was not in the set.
3. Second machine / fresh clone lost executable bits or local-only drift (rare).

Greenfield `/fireweave:initialise` now asks which agents the **team** uses and writes those standing
loops up front — prefer that path for new repos. Use `adopt` when the harness is already in place
and only this agent's loop is missing.

`/fireweave:initialise --reinit` still re-scaffolds credentials/harness — do **not** use it just to add
an agent loop.

**Harness-skipping by design.** `adopt` does **not** scaffold `fw-harness`, does **not**
call `record_rollout_env_contract`, does **not** re-enumerate environments, and does **not**
author, retire, or otherwise touch rollout-ready manifests or change stamps — those are
server-owned and belong to the feature loop, not to attaching an agent. If the repo is not
initialised → PARK and send the user to `/fireweave:initialise`.

`--check` runs Steps 0–3 and reports the wanted-vs-present diff; writes nothing.

## Step 0 — Auth + repo-bind precondition (fail closed, allowlist)

**SCN-16 — PARK writes nothing.** Do not create or modify any FireWeave path until every gate below passes. On any PARK, leave the working tree unchanged for this run.

Run `mcp_rollout-server_ensure_auth` with
`{ cwd: <absolute open-workspace root> }` (required when known — MCP process
cwd is often not the repo). `ok: false` → `fw login` and PARK.
Continue **ONLY** when `repo_binding.bound === true` **and**
`repo_binding.orgMatch !== false`. Missing / undefined `repo_binding` → PARK
as unbound. On `orgMatch: false`: switch profile (`fw profile use`) or
`select_project` with `{ cwd }` if the bind is stale — do not blindly rebind.
**Do not write FireWeave files while unbound.** A profile alone does NOT mean
this repo is bound to a project.

Then run the tool-manifest check via `mcp_rollout-server_list_registered_tools`.

## Steps

| Step                              | Action                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1 — Bound gate**                | Read `.fireweave/project.json`. **The repo is initialised iff the pointer carries identity — `projectId` (or `projects{}`).** Do not read `rolloutReady` and do not branch on `version`: the block is a shape fact, not an initialisation fact, and `rolloutReady.initialized` no longer exists. (It used to gate this step; a block that never wrote the key was indistinguishable from `initialized: false`, so `adopt` PARKed on healthy repos and the standing-loop hooks no-opped on them — same defect, three doors.) Else PARK: _"this repo is not initialised — run `/fireweave:initialise` first"_ — **write nothing.** **`adopt` never initialises.** Confirm `.fireweave/agent-instructions.md` exists; if missing on an initialised repo → PARK toward `/fireweave:initialise --reinit` (genuine drift, not an adopt case) — **write nothing.** **Why PARK here but WARN for a missing build-gate (N4):** every standing loop points at `agent-instructions.md`, so attaching HARD ORDER / hooks that link a missing SoT is not useful; the build-gate is orthogonal to standing instructions and does not justify a key-rotating `--reinit`. Note `mcp.mode`, `installedInto[]`, and whether `teamAgents` is **absent** (pre-teamAgents initialisation — Step 5 will seed) or **present**.                                                                                                                                                                                                                                                                                               |
| **2 — Choose agents**             | Detect coding-agent markers (`.claude/`, `.cursor/`, …). Then one `a stop-and-ask user prompt` (multi-select) for **this** machine. **V1 full-materialize:** `cursor`, `claude` only. Other hosts are link-only experimental (optional second ask). Host detection alone is unreliable. Empty selection → re-ask once; if still empty → PARK (write nothing).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **3 — Diff**                      | For each selected agent, compute wanted-vs-present against the **Write matrix** below. Report what is missing / stale before writing. **Also read-only check shared build-gate:** note whether `.fireweave/hooks/rollout-build-gate.mjs` and `.fireweave/hooks/rollout-build-gate.sh` exist. If either is **missing** → **WARN** (do **not** PARK, do **not** force `--reinit` / key rotate) — standing-loop writes still proceed; adopt must not re-copy build-gate from platform source. If the `.sh` exists but is non-executable → note mode-bit repair for Step 4. On `--check` → stop here (write nothing; still report build-gate status).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **4 — Write standing loop**       | **First write step.** Write **only** missing/stale standing-instruction artifacts for the selected agents (templates below). **Merge, never replace** `.cursor/hooks.json` / `.claude/settings.json`. Upsert `CLAUDE.md` / `AGENTS.md` FireWeave blocks by stable marker. Scripts: overwrite from template, `chmod +x`. Repair `rollout-build-gate.sh` mode bits only when the file exists but is non-executable — **do not re-copy** `.mjs`/`.sh` from platform source. Do **not** change `mcp.mode`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **5 — Bookkeeping (server-side)** | `installedInto[]` and `teamAgents` are **repo-scoped server state**. Write them with `mcp_rollout-server_update_repo_state` — one call, `{ fields: { installedInto: [...], teamAgents: [...] } }` — never by hand-editing `project.json`. Both are **set-valued and UNION on merge**, which is exactly what a second machine adopting concurrently needs: send only what this run added and the server folds it in. The write is online-only and fails closed; on `refused` → PARK and report, do not fall back to editing the file. It writes **no file at all** — not `rolloutReady.installedInto[]`, not `rolloutReady.teamAgents`, in any repo — so `fw sync` is how this worktree sees the merged row back. Append written paths (sorted, deduped). **Union** selected agents (sorted, deduped). **When `teamAgents` is absent**, first **derive** the existing set exactly as `/fireweave:initialise --reinit` rule 2 — agents implied by `installedInto[]` paths, plus disk markers that already carry FireWeave standing-loop artifacts (HARD ORDER / FireWeave rule / intent-gate — **not** bare `.cursor/` or `.claude/` alone) — then union the selection into **that** derived set; never into a bare `[]` (N3 — first adopt must not drop other agents already wired). A **present** array (including `[]`) is authoritative: union into it as-is (post-`--remove` present-`[]` stays intentional). Record per-machine adopt fact in gitignored `.fireweave/local.json` as `adopt: { agents, at, skillVersion }` — do **not** write credential / env / capability / `mcp.mode` fields. |
| **6 — Verify**                    | `mcp_rollout-server_detect_rollout_ready` + `mcp_rollout-server_reconcile` with `phase: "build"`. Assert each written script is executable.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **7 — Reload notice**             | Name **only** the agents whose reloadable artifacts were written this run (from this run's `installedInto[]` appends): Cursor → Developer → Reload Window; Claude Code → hooks apply on the next session. If Step 3 warned that build-gate files are missing, surface that warning again (standing loops are attached; build-gate restore still needs `/fireweave:initialise --reinit` when the user wants harness repair — not required to finish adopt). If `mcp.mode` is `cursor-plugin` and the adopting agent is **not** Cursor → **notice only** (do not run): non-Cursor hosts may need `fw mcp install` for MCP transport. Standing instructions ≠ MCP wiring. `--reinit` remains available for harness/credential drift — prefer `adopt` for standing-loop-only gaps.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

Every clarification uses `a stop-and-ask user prompt`.

## Write matrix

| Agent                                                              | Artifacts `adopt` ensures                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `claude`                                                           | `CLAUDE.md` HARD ORDER block (template below); `.claude/hooks/rollout-intent-gate.sh` (chmod +x); `.claude/hooks/rollout-build-gate-stop.sh` (chmod +x) — the build gate itself, without which Claude has only an advisory reminder; `.claude/settings.json` → merge `SessionStart` + `UserPromptSubmit` + `Stop` (templates below)                                                                                                          |
| `cursor`                                                           | `.cursor/rules/fireweave-rollout-ready.mdc`; `.cursor/hooks.json` `sessionStart`/`stop` entries; `.cursor/hooks/fireweave-rollout-{session,stop}.sh` (chmod +x); FireWeave skills under `.cursor/skills/` copied **from the installed plugin bundle only** (never from `packages/fw-plugins/` platform source), each as a **whole directory** — never `SKILL.md` alone, or initialise arrives without its `harness/**` templates (C27 below) |
| `cline` / `codex` / `opencode` / `copilot` / `gemini` / `windsurf` | **Link-only experimental** — agent-instructions link / thin rule only; do not invent full HARD ORDER templates                                                                                                                                                                                                                                                                                                                               |

Shared: `.fireweave/hooks/rollout-build-gate.{mjs,sh}` — existence checked in Step 3 (missing → WARN, continue writes); Step 4 may repair `.sh` mode bits only.

**V1 completeness:** Claude and Cursor rows must be fully materialised. Link-only rows are optional and cheap.

**Skill copies are COPIES, not links (C27).** `.cursor/skills/<skill>/` is a
real file copy of the installed plugin bundle; nothing refreshes it automatically.

**Where the installed plugin bundle is:** the directory containing the `SKILL.md`
you are executing right now. `adopt` runs from the bundle, so the skills root is
its parent — `<dir of this SKILL.md>/..`. Resolve it that way rather than searching
the filesystem, and never substitute the `packages/fw-plugins/` platform source.

**Copy whole DIRECTORIES, not just `SKILL.md`.** A skill is its directory: the
initialise skill ships `harness/**` (the harness `.tpl` files its Step 4 generates
from). A copy that took only `SKILL.md` leaves the next agent running initialise
in this repo with no templates to read, and it hand-writes a harness instead.
Copy `<skill-dir>/**`, never `<skill-dir>/SKILL.md` alone — and take
`<skill-dir>` from the bundle as it is named there, since hosts rename it
(`initialise`, `fw-initialise` on Cursor, `fw_initialise` on Codex).

Copy the **whole** FireWeave skill set (`initialise`, `adopt`, `safe-rollout`,
`migrate-harness`, `cleanup`), not just the one you were thinking about — a
half-refreshed set is a repo where `safe-rollout` reads the seam and `cleanup`
still tries to delete files. Overwrite stale copies rather than skipping them on
"already present": a repo whose data migrated to fw-server while its skill copies
stayed behind has an agent authoring manifest files into a tree where the gate no
longer reads them, and **nothing errors to say so**. Stale readers fail loudly;
stale instructions fail silently. Then say so in the Step 7 reload notice — a user
who is not told their copied skills changed has no reason to reload.

## Idempotency and merge rules

- Second run is a **no-op** apart from refreshing a stale HARD ORDER / script template. Report "already current" when the diff is empty.
- `.claude/settings.json` and `.cursor/hooks.json`: **read → merge → write**. Dedupe hook entries by `command`. Never emit a file containing only FireWeave entries.
- `CLAUDE.md` / `AGENTS.md`: locate the FireWeave block by the stable marker `FireWeave rollout-ready — HARD ORDER`; replace in place; otherwise append. Do not reorder surrounding user content.
- Scripts: overwrite from the templates below, then `chmod +x`.

## Do not

- Call `record_rollout_env_contract`, or ask about cloud secrets. (Nothing in FireWeave mints a
  credential any more — both key families are issued by the operator in the portal — so there are
  no keys for adopt to rotate either.)
- Scaffold or rewrite `fw-harness`, `fw-tracker`, or entrypoint wiring.
- **Never** touch `.fireweave/rollout-ready/**` (server-owned) or register rollouts.
- Blind-copy `.cursor/**` into `.claude/**` — generate each host from the templates below (Cursor and Claude shapes differ).
- Write repo-local `mcp/rollout-server/` or `.cursor/mcp.json` launcher entries.
- Change `rolloutReady.mcp.mode` (host transport is initialise's job).
- Run while unbound or on a non-initialised repo.
- Write any file on PARK (Steps 0–3).

---

## Cursor rule template

Write `.cursor/rules/fireweave-rollout-ready.mdc`:

```markdown
---
description: FireWeave rollout-ready — mandatory conventions for every feature change in an initialised repo
alwaysApply: true
---

# FireWeave rollout-ready (promote-not-wrap)

Read [.fireweave/agent-instructions.md](.fireweave/agent-instructions.md).

## HARD ORDER — every user-facing or flag-gated feature

1. **FIRST** author the manifest with `mcp_rollout-server_upsert_rollout_manifest` `{ feature, manifest, baseContentHash }` (Manifest contract in agent-instructions) + mint `chg_`/`stmp_` + apply the stamp policy (per-surface stamps by default — append each stamp to its own surface's `FW_STAMPS`; one shared stamp only when single-project + every surface's harness is surface-aware). **FireWeave stores the manifest — do not write a manifest file yourself.**
2. Implement behind the harness control point (`fw.controlPoints.getBooleanValue(<key>, false, ctx)`) with `// @fireweave-controlpoint <key>` at each evaluation site.
3. **BEFORE done** call `mcp_rollout-server_assert_dev_checklist` with `{ feature }` — PARK on any block (includes dummy metrics with no emit sites). Also `reconcile` phase `build`.
4. Backfill after coding is forbidden. Do not write repo-local `mcp/`.
5. **Absence has names.** `never-authored` is the only one that means author a manifest. `not-fetched` → `fw sync`; `not-authorized` → the manifests are withheld, not absent (`fw login` / ask an admin); `server-unavailable` → retry; `queued` → you already authored it, drain `.fireweave/.queue/`. Never author to clear the last four.

## Ship path

`/fw-rollout` promotes existing rollout-ready work only. If `assert_dev_checklist` fails, finish the package first — there is no wrap-from-scratch path.
```

---

## CLAUDE.md rollout-ready block

Upsert this block near the top of `CLAUDE.md` (replace any prior one-line FireWeave pointer). Do not merely link `.fireweave/agent-instructions.md` — inline the order:

```markdown
## 🔴 FireWeave rollout-ready — HARD ORDER (this repo is initialised)

This repo is FireWeave rollout-ready ("promote, not wrap"). For **every user-facing
OR flag-gated OR behavior-changing** change — including internal/ops/observability
wiring — the rollout-ready package comes **FIRST, while you write code**, never as a
backfill after the feature is built. Backfill breaks promote-not-wrap and is forbidden.

**Classify the task first, in one line:** `change` (you will modify observable
behaviour) · `inquiry` (explain / locate / review) · `brainstorm` (nothing written
yet) · `infra-only` (config, docs, formatting, no behaviour delta). Only `change`
runs the steps below. A keyword hook surfaced this reminder; it cannot tell
`fix the checkout bug` from `how do I fix this typo` — you can. **When the class
is genuinely unclear, treat it as `change`:** skipping wrongly ships unflagged
behaviour that is invisible until nothing can be promoted or rolled back, while
running wrongly costs a few tool calls. Re-classify the moment a brainstorm
starts writing code.

1. **FIRST** — author the rollout-ready manifest by calling
   `mcp_rollout-server_upsert_rollout_manifest` `{ feature, manifest, baseContentHash }`
   (Manifest contract in [.fireweave/agent-instructions.md](.fireweave/agent-instructions.md)).
   **FireWeave stores the manifest — do not write a manifest file yourself.**
   `baseContentHash` is required and nullable (`null` = "no row yet"); on `conflict`,
   re-apply on top of `current` and retry with `currentContentHash`. Mint
   `chg_<ULID>` + `stmp_<ULID>`, and apply the stamp policy — per-surface stamps by default (append each stamp ONLY to its own surface's `FW_STAMPS`); one shared stamp only when the change is single-project and every participating surface's harness is surface-aware.
2. Gate the new behavior behind the harness control point (`fw.controlPoints.getBooleanValue(<key>, false, ctx)`) and add
   `// @fireweave-controlpoint <key>` at each evaluation site **as you write it**.
3. **BEFORE calling the task done** — run `mcp_rollout-server_assert_dev_checklist`
   `{ feature }` (PARK on any block) + `detect_rollout_ready` + `reconcile` phase `build`.
4. Do **not** open a PR / declare done until `assert_dev_checklist.pass === true`.
   Ship only via `/fireweave:safe-rollout` (promotes; never wraps).
5. **Absence has names — only `never-authored` means author one.** `not-fetched` →
   run `fw sync`. `not-authorized` → the manifests are **withheld, not absent**;
   `fw login` or ask an org admin. `server-unavailable` → retry. `queued` → you
   already authored it and it is waiting in `.fireweave/.queue/`; drain it. Never
   author a manifest to clear any of those four — you would displace a contract you
   cannot currently see.

If a request looks like feature work and you have NOT done step 1, stop and do it
first. If you are unsure whether a change qualifies, it does — err toward wrapping.
```

---

## Cursor hooks

**Merge** FireWeave hooks into `.cursor/hooks.json` — **never replace** the whole file. Existing events (`beforeMCPExecution`, `afterFileEdit`, …) must survive.

1. Read existing `.cursor/hooks.json`, or start with `{ "version": 1, "hooks": {} }`.
2. Under `hooks.sessionStart`, append (if not already present by `command`):
   `{ "command": ".cursor/hooks/fireweave-rollout-session.sh" }`
3. Under `hooks.stop`, append (if not already present by `command`):
   `{ "command": ".cursor/hooks/fireweave-rollout-stop.sh" }`
4. Write the merged JSON back. Do **not** paste a hooks.json that contains only FireWeave entries.

Write `.cursor/hooks/fireweave-rollout-session.sh` (executable):

```bash
#!/usr/bin/env bash
# Inject rollout-ready context when this repo is initialised.
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
proj="$root/.fireweave/project.json"
inst="$root/.fireweave/agent-instructions.md"
if [[ ! -f "$proj" ]]; then exit 0; fi
bound="$(node -e "
const fs = require('node:fs');
const j = JSON.parse(fs.readFileSync(process.argv[1], 'utf8'));
// Bound iff the pointer carries identity — the same rule the build-gate wrapper
// uses. Nothing about the \`rolloutReady\` block is consulted: a repo that has one
// and a repo that does not are equally initialised, and a block that never wrote
// \`initialized\` used to drop this reminder with no signal at all.
process.stdout.write(j.projectId || j.projects ? 'yes' : 'no');
" "$proj")" || exit 1
[[ "$bound" == "yes" ]] || exit 0
summary="FireWeave rollout-ready repo: follow .fireweave/agent-instructions.md on every feature change (anchor + manifest + stamp before /fw-rollout)."
if [[ -f "$inst" ]]; then
  summary="$summary See agent-instructions for harness paths and dev checklist."
fi
printf '%s\n' "{\"additional_context\":$(node -e "console.log(JSON.stringify(process.argv[1]))" "$summary")}"
```

Write `.cursor/hooks/fireweave-rollout-stop.sh` (executable):

```bash
#!/usr/bin/env bash
# After agent work, nudge when rollout-ready artifacts drift.
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
gate="$root/.fireweave/hooks/rollout-build-gate.sh"
# No gate ⇒ nothing to run. A gate that is PRESENT but not executable used to
# mean the same thing SILENTLY — a repo that believes it is gated and is not.
# Say so, and run it through bash rather than skipping the check. Likewise never
# discard the gate's stderr: a wrapper that refuses to run explains itself there.
if [[ ! -f "$gate" ]]; then exit 0; fi
if [[ ! -x "$gate" ]]; then
  echo "fireweave-rollout-stop: $gate is not executable — running it via bash. Repair with: chmod +x $gate" >&2
fi
out="$(mktemp)"
err="$(mktemp)"
trap 'rm -f "$out" "$err"' EXIT
# Capture the gate's stderr — never discard it. A wrapper that refuses to run
# (unreadable or identity-less pointer) exits non-zero with an explanation there
# and NO JSON on stdout; `2>/dev/null` turned that into the generic
# "drift detected" line, which reads as an ordinary finding rather than as
# "this repo is not being gated".
if bash "$gate" >"$out" 2>"$err"; then exit 0; fi
findings="$(node -e "const j=JSON.parse(require('fs').readFileSync(process.argv[1],'utf8')); console.log((j.findings||[]).filter(f=>f.severity!=='info').map(f=>f.fix?f.message+' Fix: '+f.fix:f.message).join('; '))" "$out" 2>/dev/null || true)"
if [[ -z "$findings" ]]; then
  findings="the gate produced no verdict: $(tr '\n' ' ' <"$err")"
fi
msg="FireWeave rollout-ready drift: ${findings}. Complete anchor + manifest + fw-tracker stamp per .fireweave/agent-instructions.md, then run reconcile phase build."
printf '%s\n' "{\"followup_message\":$(node -e "console.log(JSON.stringify(process.argv[1]))" "$msg")}"
```

Record `.cursor/hooks.json`, `.cursor/hooks/fireweave-rollout-session.sh`, `.cursor/hooks/fireweave-rollout-stop.sh`, `.cursor/rules/fireweave-rollout-ready.mdc` in `installedInto[]` when written.

---

## Claude Code hook

Three artifacts, all **required and committed**:

**1. The hook script** — `.claude/hooks/rollout-intent-gate.sh` (executable, `chmod +x`). It MUST:

- Emit Claude Code's injection JSON — `{ "hookSpecificOutput": { "hookEventName": <event>, "additionalContext": <reminder> } }` — a **bare `echo` is not reliably injected**; use the JSON form.
- Fire on **SessionStart** (empty prompt → surface the standing reminder unconditionally) and **UserPromptSubmit** (narrow to feature-intent keywords: `add|implement|feature|feat|fix|ship|build|wrap|change|refactor|rollout|flag`).
- Be **fail-open** — `set -uo pipefail` (not `-e`), guard every `node`/`cd`, and `exit 0` on any error.
- Read `.fireweave/project.json` and decide on **project identity** (`projectId` / `projects`) — the same rule as the build-gate wrapper. Never read the `rolloutReady` block: a block that never wrote `initialized` is indistinguishable from `initialized: false`, and both used to no-op this reminder in silence on repos `adopt` exists to serve. No-op only when the pointer carries no identity.
- **Prompt source (HARD):** Claude Code `UserPromptSubmit` sends a JSON payload on **stdin** (not `$1`). Parse stdin first (`prompt` / `user_prompt` / `userPrompt` / `message`); fall back to `$1` then `CLAUDE_USER_PROMPT`. Do **not** rely on argv alone — that silently skips the keyword filter.

```bash
#!/usr/bin/env bash
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd)" || exit 0
proj="$root/.fireweave/project.json"
[[ -f "$proj" ]] || exit 0
bound="$(node -e "try{const j=JSON.parse(require('node:fs').readFileSync(process.argv[1],'utf8'));process.stdout.write(j.projectId||j.projects?'yes':'no')}catch{process.stdout.write('no')}" "$proj" 2>/dev/null)" || exit 0
[[ "$bound" == "yes" ]] || exit 0
# UserPromptSubmit: JSON on stdin. SessionStart: empty → always remind.
prompt=""
if [[ ! -t 0 ]]; then
  stdin="$(cat 2>/dev/null || true)"
  if [[ -n "$stdin" ]]; then
    prompt="$(node -e "try{const j=JSON.parse(process.argv[1]);const p=j.prompt??j.user_prompt??j.userPrompt??j.message??'';process.stdout.write(typeof p==='string'?p:JSON.stringify(p))}catch{}" "$stdin" 2>/dev/null || true)"
  fi
fi
[[ -z "$prompt" ]] && prompt="${1:-${CLAUDE_USER_PROMPT:-}}"
msg="FireWeave rollout-ready repo (promote-not-wrap). FIRST classify this task in one line — change | inquiry | brainstorm | infra-only — because this reminder fired on a KEYWORD match and the keyword cannot tell 'fix the checkout bug' from 'how do I fix this typo'. Only 'change' runs the package; when genuinely unclear treat it as change (skipping wrongly ships unflagged behaviour, running wrongly costs a few tool calls). For a change task the rollout-ready package comes FIRST — author the manifest via upsert_rollout_manifest (FireWeave stores it; do not write a manifest file yourself) + mint chg_/stmp_ + append each stamp to its own surface's FW_STAMPS (one shared stamp only when single-project + every surface's harness is surface-aware), add // @fireweave-controlpoint <key> as you code, then assert_dev_checklist + reconcile(build) before done. No backfill. Absence has names: only never-authored means author one; not-fetched=fw sync, not-authorized=withheld not absent, queued=drain .fireweave/.queue. Ship via /fireweave:safe-rollout. See .fireweave/agent-instructions.md."
if [[ -n "$prompt" ]] && ! echo "$prompt" | grep -qiE '\b(add|implement|feature|feat|fix|ship|build|wrap|change|refactor|rollout|flag)\b'; then exit 0; fi
node -e "console.log(JSON.stringify({hookSpecificOutput:{hookEventName:process.argv[2]||'UserPromptSubmit',additionalContext:process.argv[1]}}))" "$msg" "${HOOK_EVENT:-}" 2>/dev/null || printf '%s\n' "$msg"
exit 0
```

**2. The settings wiring** — merge (never replace) into `.claude/settings.json`. Use a **fail-open guarded command**:

```json
"SessionStart": [
  { "hooks": [ { "type": "command",
    "command": "[ -f .claude/hooks/rollout-intent-gate.sh ] && HOOK_EVENT=SessionStart bash .claude/hooks/rollout-intent-gate.sh || true" } ] }
],
"UserPromptSubmit": [
  { "hooks": [ { "type": "command",
    "command": "[ -f .claude/hooks/rollout-intent-gate.sh ] && HOOK_EVENT=UserPromptSubmit bash .claude/hooks/rollout-intent-gate.sh || true" } ] }
],
"Stop": [
  { "hooks": [ { "type": "command",
    "command": "[ -f .claude/hooks/rollout-build-gate-stop.sh ] && bash .claude/hooks/rollout-build-gate-stop.sh || true" } ] }
]
```

**3. The build-gate stop hook** — `.claude/hooks/rollout-build-gate-stop.sh` (executable, `chmod +x`), wired on **Stop**. Without it Claude Code has NO build gate: the intent gate is advisory (it reminds, it never checks), so on a Claude-only host the manifest ⇄ anchor check simply does not happen and nothing says so. Cursor has run this gate on every stop since initialise; this is the parity. It MUST:

- Honour `stop_hook_active` from the stdin payload — blocking twice loops the agent against a gate it may not be able to clear (a `fw sync` finding needs a network the session may not have).
- Emit `{ "decision": "block", "reason": <findings> }` on failure and **nothing at all** on success.
- Filter `severity: "info"` findings out of the reason — the manifest-source line is diagnostics, not drift.
- Be fail-open on everything except a gate that ran and failed. The one fail-open that is now **visible** is a gate present but not executable: that used to skip the check silently, which is a repo that believes it is gated and is not.

```bash
#!/usr/bin/env bash
# Claude Code Stop-hook parity for the rollout-ready build gate.
#
# Cursor has run this gate on every stop since initialise. Claude Code ran only
# the ADVISORY intent gate (a reminder on SessionStart / UserPromptSubmit), so a
# Claude-only host had no build gate at all — the manifest ⇄ anchor check simply
# did not happen, and nothing said so. This closes that asymmetry.
#
# Fail-open on everything EXCEPT a gate that ran and failed: a missing node, a
# missing gate, an unreadable temp file must never wedge a session. The one
# fail-open that is now VISIBLE is a gate present but not executable — that used
# to skip the check silently, which is a repo that believes it is gated and is
# not.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd)" || exit 0
gate="$root/.fireweave/hooks/rollout-build-gate.sh"

# Claude sets `stop_hook_active` once this hook has already blocked. Blocking a
# second time loops the agent against a gate it may not be able to clear (e.g.
# `fw sync` needs a network this session does not have).
payload="$(cat 2>/dev/null || true)"
case "$payload" in
  *'"stop_hook_active":true'* | *'"stop_hook_active": true'*) exit 0 ;;
esac

[ -f "$gate" ] || exit 0
if [ ! -x "$gate" ]; then
  echo "rollout-build-gate-stop: $gate is not executable — running it via bash. Repair with: chmod +x $gate" >&2
fi

out="$(mktemp 2>/dev/null)" || exit 0
err="$(mktemp 2>/dev/null)" || exit 0
trap 'rm -f "$out" "$err"' EXIT
# Capture the gate's stderr — never discard it. A wrapper that refuses to run
# (unreadable or identity-less pointer) exits non-zero with an explanation there
# and NO JSON on stdout; `2>/dev/null` turned that into the generic
# "drift detected" line, which reads as an ordinary finding rather than as
# "this repo is not being gated".
if bash "$gate" >"$out" 2>"$err"; then exit 0; fi

reason="$(node -e "
const j = JSON.parse(require('node:fs').readFileSync(process.argv[1], 'utf8'));
console.log((j.findings || []).filter((f) => f.severity !== 'info').map((f) => (f.fix ? f.message + ' Fix: ' + f.fix : f.message)).join('; '));
" "$out" 2>/dev/null || true)"
if [ -z "$reason" ]; then
  reason="the gate produced no verdict: $(tr '\n' ' ' <"$err")"
fi
msg="FireWeave rollout-ready build gate FAILED: ${reason} Complete the rollout-ready package per .fireweave/agent-instructions.md — author the manifest via upsert_rollout_manifest, add // @fireweave-controlpoint at each evaluation site, append the stamp to its surface's FW_STAMPS — then re-run the gate. If a finding says \`fw sync\`, this worktree has no server projection and absence is NOT evidence: fetch it rather than authoring over a contract you cannot see."
node -e "console.log(JSON.stringify({ decision: 'block', reason: process.argv[1] }))" "$msg" 2>/dev/null \
  || printf '%s\n' "$msg"
exit 0
```

Record `CLAUDE.md`, `.claude/hooks/rollout-intent-gate.sh`, `.claude/hooks/rollout-build-gate-stop.sh`, and `.claude/settings.json` in `installedInto[]` when written. Claude Code needs the `CLAUDE.md` block (standing text), the intent gate (a reminder) and the stop gate (the check) — they are three different jobs and no two of them substitute for the third.

---

## Tool manifest

```json
{
  "SKILL_EXPECTED_TOOL_MANIFEST": [
    { "name": "ensure_auth", "server": "rollout-server" },
    { "name": "select_project", "server": "rollout-server" },
    { "name": "list_registered_tools", "server": "rollout-server" },
    { "name": "detect_rollout_ready", "server": "rollout-server" },
    { "name": "reconcile", "server": "rollout-server" },
    { "name": "update_repo_state", "server": "rollout-server" }
  ]
}
```
