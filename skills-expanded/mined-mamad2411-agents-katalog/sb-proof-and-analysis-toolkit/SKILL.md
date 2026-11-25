---
name: sb-proof-and-analysis-toolkit
description: First-principles proof recipes for the second-brain plugin repo — how "prove it, don't just install it" is practiced here. Load when a claim needs VERIFYING rather than trusting - reproducing a suspected bug before reporting it, proving a guard/hook is actually armed (violation injection), adversarially refuting a finding set before it ships, proving determinism of clustering/hashing code, proving a new regression test fails on pre-fix code (test-the-test), measuring before optimizing (injection bytes, ranking boosts, surface counts), triaging a stale git branch via patch-id, or calibrating MinHash dedup thresholds. Keywords - reproduce first, fail-open, liveness, refute mode, skeptic, byte-identical, mutation-proven, git patch-id, jaccard, threshold, "is this test real", "is the guard live", "is this branch dead". NOT for - routine test authoring and suite mechanics (sb-validation-and-qa), live-failure symptom triage (sb-debugging-playbook), the incident chronicle itself (sb-failure-archaeology), the end-to-end idea lifecycle and evidence bar for research (sb-research-methodology), or the probe/log catalog (sb-diagnostics-and-tooling).
---

# sb-proof-and-analysis-toolkit

Eight analysis recipes, each proven by a worked example from this repo's own history.
The doctrine they encode: **a green light is not evidence**. This codebase shipped
"506 green tests [that] missed 14 bugs" and "53 tautological tests" (archive/docs:CHANGELOG.md
`## 0.24.50`), and its three PreToolUse security guards sat silently inert for weeks on
the maintainer's own dev platform because nobody ever fed them a violation. Every recipe
below replaces an assumed property with an observed one.

All commands are **bash, run from the repo root** (`C:/Workplace/Projects/claude-code-plugin`
during development; `$CLAUDE_PLUGIN_ROOT` at plugin runtime). They work on git-bash/Windows,
Linux, and macOS unless flagged. All probes must sandbox state — `BRAIN_DIR="$(mktemp -d)"` —
because guards and hooks append to the real audit log.

## Terms used below (defined once)

| Term | Meaning |
|---|---|
| `BRAIN_DIR` | runtime state dir, default `~/.second-brain` (env-overridable) |
| `KNOWLEDGE_DIR` | wiki home, default `~/knowledge`; the wiki lives at `$KNOWLEDGE_DIR/wiki` |
| guard | a PreToolUse hook script (`scripts/*-guard.sh`): reads one JSON payload on stdin, emits a JSON verdict (`deny`/`ask`) or **nothing** (= allow) |
| dream | background wiki-consolidation job (snapshot → LLM phases → human-gated accept) |
| FORGET / REFLECT | dream phases: archive low-value pages / synthesize a practice page from a page cluster |
| drainer | out-of-band extraction worker (`scripts/extract-drain.sh`) that mines archived transcripts |
| shim | a `scripts/*.sh` wrapper that invokes a bundled node CLI, fail-safe to `[]` |
| bundle | committed esbuild output under `mcp/dist/` — what shims and tests actually execute (never hand-edit; rebuild with `cd mcp && npm run bundle`) |
| MinHash | `mcp/src/tools/minhash.ts`: word 3-shingles → 128-hash signature → Jaccard similarity estimate |

## Recipe index

| You are about to… | Use recipe |
|---|---|
| report a bug you found by reading code | 1 — Empirical disproof before reporting |
| claim a guard/gate/protection "is in place" | 2 — Violation injection / liveness proof |
| ship a set of findings or a destructive design | 3 — Adversarial refutation panel |
| write code whose output feeds automation (ids, hashes, ranked lists) | 4 — Determinism proof |
| trust a new regression test | 5 — Test-the-test |
| cut/keep/optimize a cost surface or ranking signal | 6 — Measurement before optimization |
| decide whether a stale branch is dead | 7 — Patch-id equivalence |
| add/tune a near-duplicate threshold | 8 — MinHash threshold calibration |

---

## Recipe 1 — Empirical disproof before reporting (reproduce-first)

**When:** you found something that "looks broken" by reading source — during an audit, a
review, or a debugging detour — and are about to write it up as a finding.

**Steps:**
1. Build the smallest end-to-end repro that drives the **real shipped component** (the
   script, the bundle, the hook) — never a paraphrase or re-implementation of its logic.
2. Sandbox all state: `BRAIN_DIR="$(mktemp -d)"`, temp `HOME`, fixture wiki.
3. Reproduce under the platform premise the bug needs (Windows-form path, CRLF-emitting jq
   via a PATH stub, tool absent via `PATH=""`) — see sb-validation-and-qa for the stub patterns.
4. Report **only what reproduced**, with the exact command + observed output inside the
   finding. If it does NOT reproduce, record the disproof and do not report.

**What convinces:** the finding text carries a command a stranger can paste, and the
observed output; the "why" cites behavior, not code-reading inference alone.

**Worked example:** the 2026-07-02 deep audit (11 independent audit areas, 88 confirmed /
1 refuted findings) ran on exactly this rule. The bash-core auditor's area summary states it
verbatim: *"I empirically disproved two suspected jq-CRLF bugs before reporting"* — two
plausible-looking CRLF hazards were reproduced-against and found already handled, so they
never entered the findings list. Symmetrically, the guard fail-open class (Recipe 2) entered
it only *after* a live repro. In-repo precedents of the same rule: the 0.29.4
silently-wrong-output wave was "found by an adversarial audit" with every finding
"reproduced by running the script" (archive/docs:CHANGELOG.md `## 0.29.4`), and 0.24.17's three wiring
defects were "all 3 reproduced before fixing" (archive/docs:CHANGELOG.md `## 0.24.17`).
(The audit report itself is an internal artifact; its durable footprint is the CHANGELOG
`## 0.33.31` entry and the code comments cited below. The incident ledger lives in
sb-failure-archaeology.)

**Apply it to your change when:** you are about to write "X is broken" anywhere — a PR
comment, a finding, a CHANGELOG claim — and your evidence is source-reading only.

---

## Recipe 2 — Violation injection / liveness proof

**When:** any claim of the form "the guard blocks X", "the gate refuses Y", "protection is
in place" — especially after touching guard code, path normalization, or `hooks/hooks.json`
wiring. A protection whose success case is **silence** can die without a symptom.

**Steps:**
1. Feed a **synthetic violation** through the real component and require the explicit
   block verdict — empty output from a guard means *silent allow*, i.e. fail-open.
2. Feed a benign payload and require silence (prove you are not over-blocking).
3. Repeat the violation in the hostile **platform form** that history says fails:
   `C:\Users\…` backslash, `C:/…` drive form, `\\?\C:\…` extended-length.
4. Repeat with the helper tools absent (`PATH=""` / stub `realpath` exiting 127) to prove
   the guard fails **closed**, not open, when degraded.

```bash
# ARMED probe — expect "deny"; EMPTY output = fail-open:
printf '{"session_id":"probe","hook_event_name":"PreToolUse","tool_name":"Write","tool_input":{"file_path":"%s"}}' "$HOME/.ssh/authorized_keys" \
  | BRAIN_DIR="$(mktemp -d)" bash scripts/symlink-guard.sh \
  | jq -r '.hookSpecificOutput.permissionDecision // "SILENT-ALLOW"'
```

> Build probe JSON with `printf`, **not** `jq --arg`: git-bash jq rewrites POSIX paths to
> `C:\` form and breaks the guard's `$HOME`-prefix compare (`tests/test-symlink-guard.sh:27-28`).
> Always sandbox `BRAIN_DIR` — verdicts append to the real `~/.second-brain/audit-log.jsonl`.

**What convinces:** block observed on the real component with the hostile payload form +
benign payload passes + degraded-tool run still denies. A grep showing the deny code
*exists* convinces no one (that is the presence-vs-effect anti-pattern; see sb-validation-and-qa).

**Worked example:** `symlink-guard.sh` (credential-dir writes) was born in 0.21.0 to close
gap G-HOOK-2 (`scripts/symlink-guard.sh:4`; the 0.21.0 entry in the removed CHANGELOG.md names it and
`config-change-guard.sh` as the release's new hooks); `persona-tool-guard.sh` (resource/tool
scope, v2.4.0 `18030a3`) and `wiki-write-guard.sh` (frontmatter contract, v2.6.0 `e75a8a7`)
predate it and carry no G-HOOK id — and all three were **silently inert on Windows,
the platform this plugin is developed on**, until the 2026-07-02 deep audit injected a
`C:\`-form credential write and observed no deny: git-bash `realpath` returns `C:/Users/…`
while the credential prefixes derive from `$HOME` = `/c/Users/…`, so the prefix compare never
matched → allow. The audit's hooks-flow summary: *"proven by live repro and 3,770 audit-log
rows"* (weeks of allow-only verdicts on the dev box). Nobody had ever injected a violation in
the Windows path form; the tests had routed their fixtures *around* the mismatch. Fixed as of
0.33.31 (working tree, 2026-07-05) by the `sb_normalize_path()` funnel — `scripts/lib.sh:14-29`
narrates the whole story in-repo; Windows-form regression probes now run on Linux/BSD CI via
stubbed `cygpath`/`realpath` (`tests/test-normalize-path.sh`, `tests/test-symlink-guard.sh:191-247`).

**Cross-refs:** ready-made probe payloads for all three guards + kill-switch checks →
sb-diagnostics-and-tooling. A standing guard-liveness eval that injects violations
automatically (P8) is **planned, not shipped** — treat every guard change as needing a
manual injection until it lands.

**Apply it to your change when:** your diff touches anything whose success case is silence
(guards, gates, deny paths, sanitizers) — inject one violation per protected class before
claiming it works.

---

## Recipe 3 — Adversarial refutation panel

**When:** a batch of findings, a destructive design, or a high-stakes claim is about to
ship on the strength of one reviewer's confirmation.

**Steps:**
1. Task independent skeptics whose job is to **REFUTE**, not confirm (the refute-mode framing
   lived in `agents/code-review-scorer.md:57-64`, removed 0.44.0 — readable at any pre-0.44.0
   ref; today dispatch skeptics via `persona_think`).
2. Ship only the survivors of the panel's quorum rule. Protocol, quorum rule, and the worked
   examples (the 0.32.0 heartbeat design-stage kill, the 88-confirmed/1-refuted deep audit,
   the 0.31.0 second-review save): **sb-research-methodology Rule 3** — that is the single
   home for the machinery; do not restate its numbers here.
3. Record the refuted items WITH their refutation (the audit's `refutedTitles` pattern), so
   the same false positive is not re-found next audit. For destructive paths, run the panel
   *again* on the fix — the 0.31.0 case in Rule 3 is the proof one pass can miss.

**What convinces:** each surviving finding carries an independent verification note
(the audit's per-finding `verdict: CONFIRMED` + `also_found_by` cross-area corroboration);
each dropped one carries the reason it died.

**Apply it to your change when:** you produced ≥ 3 findings, or your change deletes/rewrites
user data, or your confidence in a claim rests on a single pass of a single reviewer (you
included).

---

## Recipe 4 — Determinism proof

**When:** writing or altering any component whose output feeds automation: cluster ids,
content hashes, ranked lists, token-capped slices. Downstream idempotence (e.g. the dream's
`member_hash` "don't re-reflect an unchanged cluster" check) depends on **byte-stability**,
so "roughly the same output" is a bug.

**The house contract** (from the shipped label-propagation clusterer,
`mcp/src/tools/graph-cluster.ts:1-14`):
1. **Synchronous rounds** — every node's next state computed from the *previous* round only,
   so within-round visit order is irrelevant;
2. **Sorted iteration** — nodes visited in lexicographic slug order;
3. **Explicit tie-breaks** — keep own label if among the tied plurality, else smallest slug
   (this also breaks synchronous label-prop's 2-cycle oscillation);
4. **Fixed cutoff** — `maxIter` default 20, never "until it feels converged".

MinHash adds the numeric half (`mcp/src/tools/minhash.ts`): fixed-seed LCG, integer-only
`Math.imul` arithmetic, **no `Math.random`, no float accumulation** — byte-identical
signatures on every OS.

**Required tests — three tiers, all shipped, copy them:**
| Tier | Assertion | Example |
|---|---|---|
| a | same input → identical output, twice in one run | `tests/test-graph-cluster-shim.sh:39-41` |
| b | **pin exact output values** so cross-version/OS drift fails loudly | `mcp/src/tools/minhash.test.ts:60-65` pins signature words `2181256834`, `1304033094` — any seed/LCG/shingling change fails |
| c | output ordering asserted, not assumed (sorted members, sorted pair order) | `minhash.test.ts:69-82`; `graph-cluster.ts clusters()` sorts members + ids |

**Shipped extension:** the P3a code-map's PageRank is held to the same bar — "fixed
iteration count + sorted accumulation order", identical rank ordering across runs, value
equality only to fixed tolerance
(`archive/docs:docs/superpowers/plans/2026-06-30-p3a-orientation-code-map.md`, Task A3). P3a Phases 1-3
**LANDED** (0.33.33-0.33.35): `mcp/src/tools/codemap/` carries `pagerank.ts` +
`pagerank.test.ts` (the two-run-identical + shuffled-input-identical-ordering assertions at
`pagerank.test.ts:28-50`) — confirm with `ls mcp/src/tools/codemap`.

**Apply it to your change when:** any consumer compares your output across runs (hashes,
idempotence gates, caches, regenerated pages) — write tiers a–c *before* the consumer exists,
because a nondeterministic producer makes every downstream test flaky in ways that look like
the consumer's fault.

---

## Recipe 5 — Test-the-test (prove the lock fails pre-fix)

**When:** you wrote a regression test alongside a fix. A test that has never been RED proves
nothing — this repo's audit found 53 tautological tests coexisting with 14 missed bugs
(archive/docs:CHANGELOG.md `## 0.24.50`).

**Steps (uncommitted fix — the 0.33.31 REFLECT example):**
```bash
bash tests/test-graph-cluster-shim.sh   # ALL PASS with the fix in the working tree
# stash the fix — INCLUDING THE BUNDLE (shell tests execute mcp/dist, not mcp/src):
git stash push -- mcp/src/tools/graph-cluster-cli.ts mcp/dist/tools/graph-cluster-cli.bundle.js
bash tests/test-graph-cluster-shim.sh   # MUST FAIL: members gain "reflection-a"
git stash pop                           # restore the fix; re-run green
```
**Read-only variant** (no working-tree mutation; also the shape to use once the fix is
committed — substitute the pre-fix sha for `HEAD`): extract the pre-fix component with
`git show <sha>:<path> > …` into a scratch plugin-root and drive it directly. Run live on
2026-07-05 against this repo (full transcript + fixture script:
[references/worked-transcripts.md](references/worked-transcripts.md) §1):

| Component | Cluster members observed |
|---|---|
| pre-fix bundle (`git show HEAD:mcp/dist/tools/graph-cluster-cli.bundle.js`, HEAD=6fba312/0.33.30) | `["a","b","c","d","reflection-a"]` — the generated reflection page joins its own cluster (the feedback loop) |
| fixed bundle (0.33.31 working tree) | `["a","b","c","d"]` |

**House conventions that make this durable:**
- Commit-body language, verbatim from 0.33.11: *"Every new assertion was mutation-proven
  (real behavior broken -> test RED -> reverted; source tree verified clean)"*
  (`git log -1 --format=%B 4c59bf5`). Say it in your commit body, and mean it.
- Write the **regression-lock comment** in the test naming the one-line mutation that flips
  it: *"drop the generated:true filter in graph-cluster-cli.ts and members gain
  'reflection-a' (FAIL)"* (`tests/test-graph-cluster-shim.sh:87-88`). Future maintainers can
  re-run your test-the-test in seconds.

**Trap:** stashing only the `.ts` leaves the **fixed bundle** in place → the shell test stays
green against the old source → false confidence. Bundles are the executable truth for shims
and shell tests. Never hand-edit a bundle to fake the pre-fix state — rebuild via
`cd mcp && npm run bundle` (gates and release rules: sb-change-control).

**Apply it to your change when:** every time a diff contains both a fix and its test. No
exceptions — it takes two minutes and it is the only proof the lock locks.

---

## Recipe 6 — Measurement before optimization

**When:** proposing to add, cut, or keep any cost surface: per-turn injections, ranking
signals, repo surface counts. The decision text must cite a number measured on the real
system, with the measuring command recorded.

**Worked example A — the P1c injection measurement (0.33.30).** Claim: the per-turn
`UserPromptSubmit` injection is ~662 B ≈ ~165 tokens, no wiki body (archive/docs:CHANGELOG.md
`## 0.33.30`). Method — pipe a synthetic prompt into the real hook, byte-count the emitted
`additionalContext`:
```bash
printf '{"session_id":"measure","prompt":"how should I refactor the search module to add caching?"}' \
  | BRAIN_DIR="$(mktemp -d)" bash scripts/persona-context.sh \
  | jq -r '.hookSpecificOutput.additionalContext // ""' | wc -c
```
Verified runnable 2026-07-05 (a sandboxed-BRAIN_DIR run returned 1023 B — output varies with
prompt and persona state; the ~662 B is the recorded reference measurement). The bytes→token
step is the ~4 bytes/token heuristic (UNVERIFIED as a documented method — the byte figure is
the fact of record). To harden: loop a prompt corpus, report p50/p95 bytes.

**Worked example B — measure, then demote (0.33.22).** Before cutting the graph
search-ranking boost, it was measured **on the real wiki**, with outcome classes
(improved/degraded/unchanged gold-page rank) defined before running: the result was a wash,
and in the harm cases the boost displaced a page's own exact title-match (archive/docs:CHANGELOG.md
`## 0.33.22`). Result: demoted to opt-in (`SB_GRAPH_RANKING_BOOST=1`), default off. The same
measured-hub-bias reasoning later cut the access-frequency boost (0.33.30 P4b). The measured
numbers (corpus size, the improved/degraded/unchanged split, the ~10,000× compounding
prequel) and the ranking theory behind both cuts: sb-memory-systems-reference §1.

**Worked example C — the surface-budget counting method.** "How big is the plugin surface"
is not a vibe; the counting commands are pinned in `scripts/validate-plugin.sh:196-199`
(top-level dirs under `skills/`; `agents/*.md`; top-level `scripts/*.sh`; `tests/test-*.sh`)
and compared against `.claude-plugin/surface-budget.json`. As of 0.33.31 (2026-07-05): skills 18,
agents 9, scripts 52, tests 153 — live counts verified equal to budget. Reproduce:
`bash scripts/validate-plugin.sh`. Budget governance (when a bump is legitimate):
sb-change-control.

**What convinces:** a number from the **real corpus/state**, a recorded command, a baseline
to compare against, and the decision text citing all three.

**Apply it to your change when:** the word "optimize", "diet", "too expensive", or "probably
helps" appears in your rationale — measure first; the boost you are defending may be a wash.

---

## Recipe 7 — Patch-id equivalence for dead-branch triage

**When:** a stale branch exists and you must decide delete vs merge, or you need to prove "this
commit already landed on main in some form" (cherry-picks, backports, superseded fix branches).

**Steps:**
```bash
git log main..<branch> --oneline      # what the branch is ahead by
git cherry main <branch>              # '-' prefix = patch-equivalent change already on main
git show <branch-sha> | git patch-id  # diff-content digest (sha-independent)
git show <main-sha>   | git patch-id  # equal first field = same change
```
`git patch-id` hashes the *diff content* (normalized, ignoring sha/author/date/position), so
equal ids prove the change is identical even when the commits differ in everything else.

**Worked example (re-verified live 2026-07-05):** local branch
`fix/home-cwd-relative-brain-dir` is exactly one commit ahead of its merge-base (`ef7a8e7`,
"resolve brain/knowledge dir via os.homedir(), not process.env.HOME").
`git show ef7a8e7 | git patch-id` and `git show 788f193 | git patch-id` (the main-line
commit released as 0.33.17) both emit patch-id **`d810f36ce683377f73efe9b9cdc3f22f4ea16ef0`**,
and `git cherry main fix/home-cwd-relative-brain-dir` prints `- ef7a8e7…`. Verdict: the
branch is fully superseded by main — safe to delete, nothing unique on it. (Transcript:
[references/worked-transcripts.md](references/worked-transcripts.md) §3. The incident the fix
closed — the Windows HOME→CWD stray-`.second-brain/` class — is sb-failure-archaeology's story.)

**Caveats:** patch-id compares one commit at a time — for a multi-commit branch check each
line of `git cherry`, or fall back to `git diff main...branch --stat` (empty = tree-identical).
A `+` from `git cherry` means genuinely unmerged content: stop, read it, decide deliberately.

**Apply it to your change when:** pruning branches, or whenever "I think this already landed"
appears in a discussion — two commands convert the guess into proof.

---

## Recipe 8 — MinHash threshold calibration (boundary-fixture proof)

**When:** adding a new near-duplicate consumer, tuning a similarity threshold, or
investigating a report of false collapse / false forget.

**The live thresholds:** three consumers (capture write-path / FORGET gate / dream
DEDUPLICATE), deliberately staggered so strictness scales with how autonomous the destructive
action is. The threshold table (env knobs, defaults, definition sites), the NOOP/UPDATE
semantics, and the false-positive guards you must keep (`isEmptySignature` for prose-empty
stubs; FORGET's keep-≥ 1-per-cluster rule): **sb-memory-systems-reference §3** is the single
home — read it before touching any consumer; do not copy the table here.

**How a value is validated — the boundary-fixture method.** There is no corpus-calibration
study behind the exact values (UNVERIFIED beyond the design rationale in CHANGELOG
`## 0.33.26`–`## 0.33.29`); what IS machine-proven is the **boundary behavior**, via fixtures
whose true Jaccard is *computed analytically*, not eyeballed:
`mcp/src/tools/raw-inbox.test.ts:321-323`: A50 = 50 tokens, A52 = the same + 2 more —
*"A50 is a 48-shingle prefix of A52's 50 → Jaccard 0.96 ≥ 0.9"* (just above the line);
the far side is a disjoint token set (sim ≈ 0). When you move a threshold, move the
fixture math with it.

**Recalibration procedure:** run the real engine over the real wiki and read the pair list
*before* moving any threshold — the decision must cite observed pairs (Recipe 6 discipline):
```bash
SB_REDUNDANCY_THRESHOLD=0.8 bash scripts/wiki-redundancy.sh --knowledge-dir "$HOME/knowledge" \
  | jq -r '.[] | "\(.sim)\t\(.a)\t\(.b)"' | head -20    # output already sorted sim-desc
```
Then eyeball: are the pairs at your proposed line genuine duplicates or same-topic distinct
pages? (Why topic-coverage alone mis-calls that judgment — the false-forget example — is
sb-memory-systems-reference §3's story.)

**Apply it to your change when:** you touch any `SB_*_THRESHOLD`, add a MinHash consumer, or
your consumer acts autonomously — set its threshold at least as strict as the most autonomous
existing consumer, and prove the boundary with computable-Jaccard fixtures.

---

## When NOT to use this skill

| Need | Go to |
|---|---|
| write/run tests, suite mechanics, CI lanes, add-a-test checklist | sb-validation-and-qa |
| triage a live failure from its symptom | sb-debugging-playbook |
| the full incident/dead-end chronicle | sb-failure-archaeology |
| probe/log/CLI catalog with interpretation guides | sb-diagnostics-and-tooling |
| change classification, gates, release rules, budget governance | sb-change-control |
| search/dedup/forgetting theory as applied here | sb-memory-systems-reference |
| evidence bar + lifecycle for research ideas | sb-research-methodology |

## Provenance and maintenance

Authored 2026-07-05 against the working tree at version 0.33.31 (uncommitted release batch;
HEAD `6fba312` = 0.33.30). Revised 2026-07-05: guard birth history corrected against
`git log --diff-filter=A` (symlink-guard `4837873`/0.21.0; persona-tool-guard `18030a3`/v2.4.0;
wiki-write-guard `e75a8a7`/v2.6.0); Recipes 3, 6-B, and 8 deduplicated to their charter
owners (sb-research-methodology Rule 3; sb-memory-systems-reference §1 and §3).
Derived from repo evidence only: archive/docs:CHANGELOG.md (`## 0.24.50`,
`## 0.29.4`, `## 0.31.0`, `## 0.32.0`, `## 0.33.16`, `## 0.33.22`, `## 0.33.25`–`## 0.33.31`),
`scripts/lib.sh:14-29`, `scripts/graph-cluster.sh`, `scripts/wiki-redundancy.sh`,
`scripts/wiki-forget-candidates.sh`, `scripts/validate-plugin.sh:191-220`,
`mcp/src/tools/{graph-cluster.ts,graph-cluster-cli.ts,minhash.ts,minhash.test.ts,raw-inbox.ts,raw-inbox.test.ts,wiki-redundancy-cli.ts}`,
`tests/test-graph-cluster-shim.sh`, `tests/test-symlink-guard.sh`,
`agents/code-review-scorer.md` (removed 0.44.0), `skills/code-review-deep/SKILL.md` (removed 0.44.0),
`docs/superpowers/plans/2026-06-30-p3a-orientation-code-map.md` (moved to `archive/docs`), git history (patch-id runs
executed live), plus the 2026-07-02 deep-audit report (internal audit artifact — quoted
where no repo file carries the fact; durable echoes in CHANGELOG `## 0.33.31` and the lib.sh
comment). The REFLECT pre-fix/fixed comparison, the guard probe, the P1c probe, and the
patch-id session were all **re-run live on 2026-07-05**; transcripts in
[references/worked-transcripts.md](references/worked-transcripts.md).

Volatile facts — re-verify before relying on them:

| Fact class | Re-verify with |
|---|---|
| MinHash thresholds + defaults | `grep -rn "SB_CAPTURE_DEDUP_THRESHOLD\|SB_FORGET_REDUNDANCY_THRESHOLD\|SB_REDUNDANCY_THRESHOLD" mcp/src scripts \| grep -v test` |
| determinism pins + label-prop contract | `cd mcp && npx vitest run src/tools/minhash.test.ts src/tools/graph-cluster.test.ts`; `grep -n maxIter mcp/src/tools/graph-cluster.ts` |
| guard armed on this box | Recipe 2 probe one-liner (expect `deny`) |
| refuter-panel rule (retired — its home surfaces were removed 0.44.0) | none live; protocol history at any pre-0.44.0 ref; fresh-context critique now goes through `persona_think` |
| surface counts == budget | `bash scripts/validate-plugin.sh` (exit 0) |
| dead-branch example still exists | `git branch --list fix/home-cwd-relative-brain-dir` (deleting it retires the live demo; the transcript remains the record) |
| P3a PageRank landed (Phases 1-3; expect pagerank.ts et al.) | `ls mcp/src/tools/codemap 2>/dev/null \|\| echo "not landed"` |
| 0.33.31 committed yet | `git log --oneline --grep="0.33.31"` and read the release commit body |
| REFLECT pre-fix demo baseline | once 0.33.31 is committed, `HEAD` no longer carries the pre-fix bundle — use the 0.33.30 sha `6fba312` in §1 of the transcripts sibling |
