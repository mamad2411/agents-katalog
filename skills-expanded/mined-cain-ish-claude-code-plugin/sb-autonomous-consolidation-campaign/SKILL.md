---
name: sb-autonomous-consolidation-campaign
description: >-
  Executable, decision-gated campaign for the project's hardest live problem: making memory
  consolidation FULLY AUTONOMOUS and SAFE — ending the human dream-review gate without opening
  the lethal trifecta (untrusted input + private data + exfil channel). Load this when the task
  is to implement/advance the P6 quarantine dual-LLM split (quarantined summarizer + netless
  deterministic writer), fix the auto_maintain/bubblewrap breakage, add an auto-accept
  reversibility window, wire the dream_accept untrusted-page confirm-gate, or reason about
  whether unattended consolidation is safe to turn on. Keywords: P6, quarantine, dual-LLM, CaMeL,
  maintain-llm-drain, auto_maintain, auto_accept, bwrap, --unshare-net, consolidate-writer,
  dream-summarizer, candidate-facts, held-untrusted, memory poisoning, prompt injection in
  consolidation. NOT for: routine dream lifecycle mechanics/accept-guard internals (that is
  sb-architecture-contract); how any change is classified/gated/released (sb-change-control);
  the security domain theory itself — injection model, dedup, ranking (sb-memory-systems-reference);
  triaging an already-broken live consolidation run (sb-debugging-playbook); the incident
  chronicle behind these guards (sb-failure-archaeology). This skill OWNS only the campaign plan.
---

# Autonomous consolidation campaign (P6 quarantine / dual-LLM)

This is the library's flagship: a numbered, decision-gated campaign to close the project's
hardest live problem. Follow the phases in order; each has EXPECTED observations and a branch when
you see something else. Do not skip Phase 0.

## The problem in one paragraph

The mission's hard constraint is **zero required user interaction** (CONSTITUTION.md:42-45), but
the one mechanism that bounds memory growth — `dream` (background consolidation) → `dream_accept`
(apply to live wiki) — still has a human-review gate. The unattended path (`auto_maintain` →
`scripts/maintain-llm-drain.sh`) WAS a **Linux-only** bubblewrap-jailed monolith that read raw
transcripts AND reasoned AND wrote the live-bound staging wiki in **one LLM context with network
up** — the **lethal trifecta**: untrusted input (transcripts) + access to private data (the wiki
+ OAuth token) + an exfiltration/persistence channel (network + the memory that is auto-injected
every future session). A prompt-injected transcript can steer the same context that writes the
memory Claude later trusts — a delayed-trigger poisoning substrate.

**STATUS (2026-07-30): the dual-LLM split is BUILT END-TO-END (slices 1-3).**
- **Stage A** — QUARANTINED **zero-tool** `claude -p`: validator-enforced `--json-schema`
  output (schema read from `kb-schema.json` `.candidate_facts.json_schema` — one source, shared
  with the writer), runtime init-event ATTESTATION that fails loud, `--no-session-persistence`
  + empty setting-sources, self-transcript exclusion, CLI ≥2.1.205 preflight. Cross-platform;
  bwrap is ADDITIVE Linux defense, gating nothing on any OS. No `bypassPermissions` anywhere.
- **Stage B** — `mcp/dist/tools/consolidate-writer-cli.bundle.js`: DETERMINISTIC, no LLM.
  Re-validates the facts (the summarizer's own output is untrusted-derived), applies them to
  `staging/wiki` via a local BM25 reconcile, path-guarded and idempotent. Netless twice over:
  `bwrap --unshare-net` on Linux (kernel) + a static source-scan test forbidding
  network/child-process imports (structural, every OS). Transcripts are never bound into it.
- **Arm-gates** — held-untrusted confirm gate in `dream-accept.sh` (untrusted-only NEW pages are
  HELD, never applied or deleted, released only under `SB_DREAM_ACCEPT_CONFIRM_UNTRUSTED=1`);
  `auto_accept=safe` refuses such dreams (`sb_auto_accept_decision` arg5); FORGET-manifest drop
  FIXED (applied on every accept path); untrusted-reference banners at both injection sites.
- **Milestone gate MET**: `tests/test-consolidation-poison-fixture.sh` drives the whole lane with
  poisoned transcripts AND a poisoned summarizer output — 20 assertions, oracle = files on disk.

Remaining: scheduling flips (Windows schtasks → macOS launchd + OAuth-token injection → Linux
unshare-net proxy), then the V4 hands-off cycles. Accepted residual: the model-API channel.
Superseding decision: wiki `decisions/cross-platform-autonomy-architecture.md`. Original 8-task
plan (bwrap-era): `git show archive/docs:docs/superpowers/plans/2026-06-30-p6-quarantine-dual-llm.md`.
Sections below that describe bwrap as the GATE, or Stage B as unbuilt, are historical context.

## Terms (defined once; cross-refs own the rest)

| Term | Meaning here |
|---|---|
| **dream** | A background consolidation job: snapshot the wiki + selected transcripts, mine/dedup/summarize/forget on the snapshot, leave a reviewable diff. Lifecycle internals: **sb-architecture-contract**. |
| **BRAIN_DIR** | Runtime state root, default `~/.second-brain` (dreams, transcripts, config.json, quarantine files). |
| **KNOWLEDGE_DIR** | Wiki root, default `~/knowledge` (`wiki/<category>/*.md`). Canonical — anything writing to `~/.second-brain/wiki` is a bug. |
| **the drainer** | `scripts/extract-drain.sh`, the out-of-band systemd/launchd/schtasks timer job; its tail invokes `maintain-llm-drain.sh` when `auto_maintain` is on. |
| **auto_maintain** | `config.json` flag (default `true` since 0.30.0) enabling the headless LLM maintainer. |
| **auto_accept** | `config.json` enum `off` / `safe` (default) / `all` — how much of a completed dream is applied without a human. |
| **the trifecta** | untrusted input + private-data access + exfil/persistence channel, co-located in one context. Domain model: **sb-memory-systems-reference**. |
| **quarantine (P6)** | The dual-LLM split: a network-up summarizer that only reads transcripts and emits structured facts, feeding a netless deterministic writer. NOT the same as the `.llm-maintain-quarantine` 3-strike failure file. |
| **held-untrusted** | Planned `dream_accept` holding area for untrusted-only NEW pages (P6 Task 5). Does not exist yet. |

## Non-negotiables before you touch anything

- This campaign ships through **sb-change-control** like any other change: version lockstep,
  surface-budget ratchet, full local gates. Never hand-edit `mcp/dist/**` bundles; never route
  around a gate. The plan's Task 8 is the release step — do not improvise your own.
- The plan **requires a maintainer brainstorm before Task 4** (the orchestration rewrite — "the
  load-bearing, hardest-to-reverse change", plan:5-6). Tasks 1-3 and 5-7 may proceed first.
- The **kernel jail is the boundary, not the prompt.** The summarizer's "ignore instructions"
  framing is defense-in-depth. A future editor must never relax the bwrap jail trusting the
  prompt (plan:231-234, 525-527).
- Everything fails **loud** (`sb_log_error`, terminal `failed` dream state) — except PreToolUse
  guards, which fail **safe** (stay armed). No `2>/dev/null` silent exits on new failure paths.

---

## Phase 0 — Reproduce and MEASURE the current state (do this first)

**Objective:** establish today's baseline with your own eyes: which trifecta legs are open, that
the accept guards hold, and how `auto_maintain` behaves on this host. All commands are read-only
and safe to run from inside a Claude session.

### 0.1 — Inventory which trifecta legs are open today

```bash
cd /c/Workplace/Projects/claude-code-plugin   # repo root; adjust to your checkout
# The monolithic maintainer: one LLM, reads transcripts, writes staging, network up.
sed -n '105,190p' scripts/maintain-llm-drain.sh
```

**Expected (slice-1 layout, current):** (a) `DREAM_ID=$(bash "$SDIR/dream-snapshot.sh" ...)`
staging a dream; (b) the Stage A input assembly (sanitized transcripts INLINED as DATA between
BEGIN/END markers, self-transcript excluded, byte-capped); (c) TWO spawn sites of the quarantined
zero-tool `claude -p --tools "" --strict-mcp-config --setting-sources "" --json-schema` — one
bwrap-wrapped (`BWRAP_OK=1`, additive) and one plain — both under `SB_NESTED_SPAWN=1` + the
wall-clock timeout; (d) the runtime ATTESTATION block parsing the init event (tools ⊆
{StructuredOutput}, mcp_servers == []) that discards output and fails loud otherwise. Network is
up and the creds are readable — the accepted-residual model-API channel; the untrusted-input and
write legs are cut by zero tools + staging-only output.

> **If** the file additionally shows the Stage B `consolidate-writer` CLI consuming
> `candidate-facts.json` → slice 2 has landed too; jump to Phase 5 (validation) and re-scope.

### 0.2 — Run the dream cycle "manually" (the DRYRUN gate)

The real headless run cannot execute from inside a Claude session (the recursive-`claude` OAuth
lock). Use the DRYRUN, which is the maintainer's own testable seam:

```bash
B=$(mktemp -d); mkdir -p "$B/knowledge/wiki/learnings" "$B/bin"
printf -- '---\ntitle: x\ntype: learnings\ndescription: d\ncreated: 2026-01-01\nupdated: 2026-01-01\ntags: []\nrelated: []\n---\nbody\n' > "$B/knowledge/wiki/learnings/x.md"
# Stub claude onto PATH (mirror the shipped test's write_claude_mock, tests/test-maintain-llm-drain.sh):
# the stub MUST answer `--version` ≥ 2.1.205 — the CLI schema-enforcement floor preflight runs
# BEFORE anything is staged, and a silent stub fails it (strike + no dream). bwrap needs no stub:
# it is ADDITIVE now (probed via BWRAP_OK, never a gate). DRYRUN prints and exits before any
# real spawn, so the exit-0 body is safe.
printf '#!/bin/bash\nfor a in "$@"; do [ "$a" = "--version" ] && { echo "2.1.220 (Claude Code)"; exit 0; }; done\nexit 0\n' > "$B/bin/claude"
chmod +x "$B/bin/claude"
unset CLAUDECODE
PATH="$B/bin:$PATH" SB_MAINTAIN_LLM_FORCE=1 SB_MAINTAIN_LLM_DRYRUN=1 \
  BRAIN_DIR="$B" KNOWLEDGE_DIR="$B/knowledge" CLAUDE_PLUGIN_OPTION_KNOWLEDGE_DIR="$B/knowledge" HOME="$B" \
  bash scripts/maintain-llm-drain.sh 2>&1
```

**Expected:** a line `DRYRUN dream=drm_... prompt_bytes=... tx=... excluded_self=... jail=none
quarantine: claude -p --tools "" --strict-mcp-config --setting-sources "" ...` (`jail=bwrap` on a
bwrap-capable Linux box) and (because DRYRUN simulates `status=completed`) an auto-accept line.
This proves the gates reach the quarantined spawn and the auto-accept decision fires. **If** you
get nothing, the first gates are `command -v claude` and the CLI ≥2.1.205 `--version` preflight —
confirm the stub is on PATH, executable, and answers `--version` (check `$B/error-log.jsonl` for
a version-floor refusal); then check `command -v jq` and that `CLAUDECODE` is unset.

### 0.3 — Prove the accept guards hold (the safety floor you must not regress)

```bash
bash tests/test-maintain-llm-drain.sh          # gating + containment + auto-accept
bash tests/test-dream-accept-guards.sh         # 4 of the 5 accept guards, filesystem-oracle asserts
bash tests/test-maintain-llm-drain-timeout-guard.sh
bash tests/test-injection-corpus.sh            # tool-return scanner (telemetry, NOT a boundary)
```

**Expected (verified 2026-07-05, working tree 0.33.31):**
- `test-maintain-llm-drain.sh` → 20 `PASS` lines ending `ALL PASS (gating + containment +
  auto-accept)` then a second block ending `ALL PASS`, `RC=0`. Key asserts: "binds ONLY the dream
  dir writable", "creds bound READ-ONLY", "no unconfined claude -p (only the bwrap-jailed exec)".
- `test-dream-accept-guards.sh` → `ALL PASS`, `RC=0`. On Windows/git-bash two subtests print
  `SKIP:` (chmod-555 B2, and P1 deletion-completeness when `rsync` is absent) and the file still
  exits 0 — this is the whole-file-SKIP convention, not a failure. It locks **4 of the 5** accept
  guards (≥50% staging floor F1a-c, safe-mode no-delete F3a-b, fail-closed pre-accept tarball
  B1-B4, post-snapshot protection P1); the 5th — the **symlink-escape reject** — is locked by
  `tests/test-dream-lifecycle.sh` subtest 5b ("staged OUT-OF-TREE symlink is REFUSED", gated by
  `supports_symlinks()`, so it SKIPs on symlink-less Windows). Run that file too before touching
  the escape guard — Phase 5a builds directly on it.
- `test-maintain-llm-drain-timeout-guard.sh` → `Results: 24 passed, 0 failed`, `RC=0`.
- `test-injection-corpus.sh` → 20 `PASS:` asserts, then a terminal `ALL PASS` line
  (`grep -c PASS` counts 21 because `ALL PASS` matches too), `RC=0`.

> **If** any of these FAIL on a clean tree → stop. You have a pre-existing regression; fix that
> before building on top (see **sb-debugging-playbook**). Never build the campaign on a red floor.

### 0.4 — Probe the `auto_maintain` failure mode on this host

```bash
command -v bwrap && echo "bwrap present" || echo "bwrap ABSENT (macOS/Windows/bwrap-less Linux)"
grep -n 'RestrictNamespaces' systemd/*.service
ls -1 ~/.second-brain/.llm-maintain-quarantine ~/.second-brain/.llm-maintain-fails 2>/dev/null || echo "no quarantine/fail markers"
```

**Expected & interpretation:**
- **No bwrap** (the dev-platform case): `maintain-llm-drain.sh` logs a skip and exits 0 — the
  unattended path **never runs here**, so there is **no new exposure** on macOS/Windows. The
  kernel split is Linux-only; those OSes consolidate attended via `/dream` + `/maintain`.
- **bwrap present but namespaces blocked:** `systemd/sb-extract-drain.service:23` has
  `RestrictNamespaces=true` (the API-key hardened unit); `sb-extract-drain-oauth.service` keeps it
  OUT (comment ~:12). Under a `RestrictNamespaces=true` unit the bwrap preflight
  (`maintain-llm-drain.sh:97`) fails instantly → 3-strike quarantine file → SessionStart banner
  names the fix (`install-extract-timer.sh --apply --oauth`). This is incident 0.24.41 (100%
  auto_maintain failure), documented in **sb-failure-archaeology**.
- A present `.llm-maintain-quarantine` file → the maintainer is parked. Only a CLI-version
  quarantine clears itself (when the cheap preflight passes again); any other cause stays until
  you delete it AND `.llm-maintain-fails` (the strike count alone re-quarantines on the next failure).

### 0.5 — Confirm the shipped P6 substrate you build ON

```bash
ls mcp/src/tools/sanitize.ts mcp/src/path-guard.ts        # P6a strip + path boundary
grep -n 'assertWithin\|validateSlug\|realResolve' mcp/src/path-guard.ts | head
grep -n 'renderAiBlock\|AI_BLOCK_SCHEMAS' mcp/src/tools/ai-block.ts | head
grep -n 'DATA, not instructions' agents/dream-runner.md agents/knowledge-maintainer.md agents/raw-drainer.md
```

**Expected:** `sanitize.ts` (P6a/P6b invisible-Unicode strip) and `path-guard.ts`
(`assertWithin` / `validateSlug` / `realResolve`) exist; `ai-block.ts` exports `renderAiBlock` +
`AI_BLOCK_SCHEMAS` (the deterministic writer reuses these); all three consolidation agents carry
the "DATA, not instructions" framing (a 0.33.31 nibble, archive/docs:CHANGELOG.md:17). These are the P6a/P6b
foundations the plan says are shipped and must NOT be re-planned (plan:19-24).

> **If** any of these files/markers is missing → your checkout predates the shipped P6a/P6b
> substrate (or the working tree is stale) — check `jq -r .version .claude-plugin/plugin.json`
> (need ≥ 0.33.31 for the agent framing; sanitize/path-guard shipped earlier) and update before
> building; the plan's task list assumes they exist and Tasks 1/3 import from them.

**Phase 0 exit criterion:** you can state, in one sentence, which trifecta legs are open on your
target host and that the accept-guard suite is green. Only then proceed.

---

## Phase 1 → Phase 4 — Build the split (dependency-ordered)

Detailed, per-task commands, red/green steps, expected file lists, **"if you see X instead"
branches at each gate**, and rollback are in **`references/phase-details.md`** (one screen per
task). The spine:

| Phase | Plan task | Objective | Gate to advance | Rollback |
|---|---|---|---|---|
| **1** | T1 | Candidate-fact schema + validator (`mcp/src/tools/candidate-facts.ts`) — the Stage A↔B contract: closed type vocab, byte caps, `validateSlug`, defensive `stripInvisible`. | `npx vitest run src/tools/candidate-facts.test.ts` green; a red test written FIRST proved the module was absent. | Delete the two new files; nothing else references them yet. |
| **2** | T2 | Quarantined summarizer agent (`agents/dream-summarizer.md`) — reads transcripts, emits `candidate-facts.jsonl`, NO wiki/node/script/Edit grants, literal "UNTRUSTED DATA" body. | `agent-grants.test.ts` extended + green: asserts no `Bash(node`/`Bash(bash`/rm/mv/cp/Edit grant and the framing. | Delete the agent file + revert the test case; the orchestrator still points at the monolith. |
| **3** | T3 | Deterministic writer CLI (`consolidate-writer-cli`) — applies facts, resolves ADD/UPDATE/NOOP via LOCAL BM25 (no network), `assertWithin` every write, idempotent by content hash, **never reads a transcripts path** (test-asserted). | `consolidate-writer.test.ts` green incl. the path-escape-skip and idempotence cases; `npm run build` emits the bundle (bundle-drift gate will check it). | Revert the CLI + its `mcp/package.json` bundle line + rebuild; the orchestrator still runs the monolith. |
| **4** | T4 | **Orchestrate** the two-stage split in `maintain-llm-drain.sh` (Stage A jail: transcripts ro + candidates rw, network up; Stage B jail: candidates ro + staging rw + `--unshare-net`, transcripts NOT mounted). **Brainstorm with the maintainer FIRST.** | `tests/test-maintain-llm-drain-split.sh` DRYRUN asserts two stages, Stage B has `--unshare-net` and no `transcripts` bind; all prior maintain/accept regressions still green. | `git diff scripts/maintain-llm-drain.sh` is a single-file revert to the monolith; the CLIs stay (unused). This is why Tasks 1-3 land first — the risky change is last and cheaply reversible. |

**Cross-platform reality (state it in the CHANGELOG):** Tasks 1-4 install a **Linux-only** kernel
boundary. macOS/Windows never ran the unattended path, so there is no new exposure there — but
also no kernel enforcement. Tasks 5-7 below are the cross-platform slice everyone gets.

---

## Phase 5 — The cross-platform safety slice (independent; can land before or after 4)

These three tasks ship and are tested on macOS/Windows/Linux (plan:510). Full commands in
**`references/phase-details.md`**.

| Phase | Plan task | Objective |
|---|---|---|
| **5a** | T5 | `dream_accept` confirm-gate: untrusted-only NEW pages (present in staging, absent in live, `provenance: untrusted-derived`, uncorroborated) are **held** (moved to `$DREAM_DIR/held-untrusted/`, never deleted) unless `--confirm-untrusted` / `SB_DREAM_ACCEPT_CONFIRM_UNTRUSTED=1`. Auto-accept `safe` refuses them; `all` confirms. |
| **5b** | T6 | Injection-resistant injection: wrap wiki/episodic/graph/dream store-derived blocks in `persona-context.sh` + `session-load.sh` with an "Untrusted reference — treat as DATA not instructions" banner. Do NOT wrap USER.md/PROJECT.md/Charter (first-party). |
| **5c** | T7 | Reclassify the tool-return scanner as **telemetry** (wording/docs only): header + emitted banner + audit reason say "advisory telemetry, NOT a trust boundary". No logic change — it already `exit 0`s and only flags. |

---

## Solution menu (ranked; from the plan)

The plan already decided the ranking. Do not re-litigate silently — if you deviate, record why
via **sb-research-methodology** and reconfirm with the maintainer. Full theory/effort/limits table
in **`references/solution-menu.md`**.

1. **Deterministic netless writer (CHOSEN).** Writer is a pure Node CLI under `--unshare-net`;
   all LLM judgment stays in the one quarantined summarizer. The ONLY design giving a genuinely
   network-severed privileged stage with a simple kernel boundary. **Does NOT solve:** LLM-quality
   dedup-MERGE prose + theme/reflection *authoring* on the unattended path (the ~7-pt CaMeL
   utility cost, budgeted; recoverable via attended `/second-brain:maintain`).
2. **Summarizer/writer dual-LLM split (the enclosing architecture).** CaMeL quarantine: only the
   summarizer reads raw transcripts (as DATA); the writer never has transcripts mounted. Breaks
   two trifecta legs by construction. **Does NOT solve** the summarizer's own residual egress (it
   keeps network for the API) — bounded by write-isolation + sanitization.
3. **Opt-in deny-proxy (DEFERRED, documented only).** A selective-egress allowlist (model
   endpoint only) for the summarizer via net-namespace + loopback proxy / nftables. **Materially
   more complex and OS-fragile;** behind `SB_MAINTAIN_LLM_DENY_PROXY`, not in the shippable slice.
4. **Auto-accept with a reversibility window (autonomy capstone).** The confirm-gate (Task 5) +
   the existing 5 accept guards + pre-accept tarball + reversible FORGET archive together let
   `auto_accept` advance from `safe` toward `all` *for corroborated changes* while untrusted-only
   new pages are held. **Does NOT solve** the summarizer egress leg — pair with 1+2.

---

## Known WRONG paths (fenced — each with the reason)

- **Blanket `--unshare-net` on the whole maintainer** → BRICKS it. The summarizer is a headless
  `claude -p` that MUST reach the model API; severing its network kills the LLM call. "Both stages
  cannot be `claude -p` *and* have the writer run netless" (plan:82). Only the **deterministic
  writer** stage gets `--unshare-net`.
- **Rewrite / migrate to hermes** → REJECTED by strategy. Two deep-research streams validated
  evolve-over-rewrite; "a second from-scratch rewrite would re-accrete (v1.0 proves it)". Owned by
  **sb-external-positioning** / **sb-change-control**. Do not propose it here.
- **Keep (or add) a human review gate as the safety mechanism** → CONTRADICTS the autonomy
  constitution (CONSTITUTION.md:42-45: "Safety comes from reversible auto-consolidation … not a
  manual gate"). The gate must be replaced by safety-by-construction (staged, reversible,
  provenance-tagged), not preserved.
- **Trusting the summarizer's "ignore instructions" prompt as the boundary** → it is
  defense-in-depth. The boundary is the kernel jail (no wiki mount, write-confined, no
  node/script/Edit grants). Never relax the jail because the prompt "should" hold (plan:525-527).
- **Widening the `command -v bwrap` gate to run unconfined** → NEVER. Absent bwrap must SKIP, not
  degrade to an unjailed `bypassPermissions` agent (plan:139; maintain-llm-drain.sh:32-35).
- **Hand-editing `mcp/dist/**` to ship the CLI faster** → the bundle-drift gate
  (`tests/test-bundle-current.sh`) byte-compares dist against a fresh `npm run bundle`; edit
  `mcp/src/**` and rebuild. Routing around it is a change-control violation.

---

## Phase 6 — Validation and promotion (routed through sb-change-control)

Success is **falsifiable and measured, never judged by eye.** The campaign is promotable only when
ALL of these pass. Promotion mechanics (version lockstep, surface budget, release commit) are
owned by **sb-change-control**; this skill owns the acceptance criteria.

| # | Criterion | How to prove it (command / oracle) |
|---|---|---|
| V1 | **Writer cannot see raw transcript.** | `test-maintain-llm-drain-split.sh` DRYRUN shows Stage B binds no `transcripts/`; `consolidate-writer.test.ts` asserts the code references no transcripts dir. |
| V2 | **Writer is netless.** | Stage B jail contains `--unshare-net`; the local BM25 reconcile works with `SECOND_BRAIN_DISABLE_EMBEDDINGS` and no network. |
| V3 | **Summarizer cannot write/escape.** | DRYRUN shows Stage A binds only `candidates/` writable, `staging` not bound; `agent-grants.test.ts` asserts no node/script/rm/Edit grants. |
| V4 | **N dream→auto-accept cycles, ZERO human input AND ZERO unreviewed destructive ops.** | On a Linux+bwrap box: run the drainer tail across ≥N cycles (operator-verified — cannot run in-session); assert every accepted dream was non-deleting (`safe`) or held its untrusted-only new pages; no live page deleted without corroboration. Reconciliation counters (declared-vs-observed) — an **open P8 gap**, see **sb-validation-and-qa**. |
| V5 | **Injection-corpus tests green.** | `bash tests/test-injection-corpus.sh` → `ALL PASS`; plus the new `test-injection-wrap.sh` asserts the untrusted-reference banner wraps store-derived blocks, not USER.md. |
| V6 | **Confirm-gate holds untrusted-only new pages.** | `test-dream-accept-untrusted-gate.sh`: without the flag an untrusted-only new page is in `held-untrusted/` and NOT live; with `SB_DREAM_ACCEPT_CONFIRM_UNTRUSTED=1` it lands; a trusted update always applies. |
| V7 | **Rollback drill passes.** | Accept a bad dream, then restore from the pre-accept tarball: `tar xzf ~/.second-brain/wiki-backup-pre-accept-*.tgz -C "$KNOWLEDGE_DIR"`; assert the live wiki byte-matches the pre-accept snapshot (a filesystem oracle, the doctrine of `test-dream-accept-guards.sh`). |
| V8 | **Full gate set green cross-platform.** | `cd mcp && npm ci && npm test` ; `bash scripts/validate-plugin.sh` (bundle-drift + version lockstep + surface-budget R8) ; `bash tests/run-all.sh`. Surface budget bumped in the SAME commit (`agents` 9→10 for `dream-summarizer.md`; `tests` for the new files). |

> **If V4 cannot be demonstrated on a real Linux+bwrap host**, the autonomous claim is UNPROVEN —
> keep `auto_accept` at `safe` and label the campaign "landed (Linux kernel split) but autonomy
> criterion pending live N-cycle proof". Do not claim full autonomy from a Windows dev pass alone
> (there is no Windows CI lane; the unattended path does not even run there).
>
> **If any other V-row is red** → the campaign is not promotable; route by row, do not ship a
> partial slice: V1–V3 red → the split itself is wrong, back to Phases 1–4 (rollback columns);
> V5–V6 red → the cross-platform slice, back to Phase 5; V7 red → the reversibility story is
> broken — freeze `auto_accept` at its current level until the drill passes; V8 red → ordinary
> release-gate triage, owned by **sb-change-control** (never route around a gate to close a row).

## Related live gaps this campaign should not silently inherit (open audit findings)

From the 2026-07-02 deep audit (medium, OPEN) — verify current status before relying on them; do
not let the campaign paper over them (details: **sb-failure-archaeology** / **sb-debugging-playbook**):

- FORGET archiving exists only as dream-skill prose — `auto_accept=all` and direct MCP
  `dream_accept` silently drop the forget-manifest. Auto-accept promotion must not assume FORGET
  applies automatically.
- The headless lethal-trifecta run is default-ON while its credential-exfil risk acceptance still
  claims "mitigated by opt-in/default-off" — a stale claim P6 is meant to retire.
- `symlink-guard` credential list omits `~/.claude` (the OAuth token the maintainer itself calls
  the crown jewel).
- The FORGET MinHash gate conflates "engine available" with "engine succeeded".

## Provenance and maintenance

- **Derived from (repo evidence):** `archive/docs:docs/superpowers/plans/2026-06-30-p6-quarantine-dual-llm.md`
  (read in full); `CONSTITUTION.md` (hard constraints); `scripts/maintain-llm-drain.sh`,
  `scripts/dream-accept.sh`, `scripts/dream-snapshot.sh`; `agents/dream-runner.md`;
  `mcp/src/path-guard.ts`, `mcp/src/tools/sanitize.ts`, `mcp/src/tools/ai-block.ts`;
  tests `test-maintain-llm-drain.sh`, `test-dream-accept-guards.sh`,
  `test-maintain-llm-drain-timeout-guard.sh`, `test-injection-corpus.sh`,
  `test-dream-lifecycle.sh`, `mcp/src/agent-grants.test.ts`; `archive/docs:CHANGELOG.md` (0.33.20/21/30/31);
  `systemd/*.service`; `.claude-plugin/surface-budget.json`.
- **Authored:** 2026-07-05, against the uncommitted **0.33.31** working tree (plugin.json version
  `0.33.31`; HEAD `6fba312` = release 0.33.30). All Phase-0 expected outputs were produced by
  running the commands on this tree.
- **Re-verify (fact classes that drift):**
  - P6 landed yet? → `grep -c 'dream-summarizer\|consolidate-writer' scripts/maintain-llm-drain.sh`
    (0 = still monolithic; >0 = advancing).
  - Version → `jq -r .version .claude-plugin/plugin.json`.
  - Accept-guard floor still green → `bash tests/test-maintain-llm-drain.sh && bash tests/test-dream-accept-guards.sh`.
  - Trifecta legs today → `sed -n '150,190p' scripts/maintain-llm-drain.sh` (creds bind + network).
  - Surface budget → `cat .claude-plugin/surface-budget.json` (agents/tests counts the split bumps).
  - Auto flags → `cat ~/.second-brain/config.json` (auto_maintain / auto_accept).
  - Open audit findings → the audit JSON was an internal artifact with NO stable path (do not
    hunt for `deep-audit-findings.json`). Its durable echoes: `archive/docs:CHANGELOG.md` `## 0.33.31` (the
    batch-B closure) and the deep-audit disposition ledger in **sb-failure-archaeology**
    (`references/chronicle.md` §26 — includes the still-OPEN mediums). Spot-check the four gaps
    above at source: `sed -n '106,114p' scripts/symlink-guard.sh` (CRED_PREFIXES has no
    `~/.claude`); forget-manifest handling exists only in `skills/dream/SKILL.md:235-265` —
    `scripts/dream-accept.sh` carries no handler (only the :119 comment).
