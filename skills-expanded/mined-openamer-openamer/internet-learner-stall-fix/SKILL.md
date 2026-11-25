---
name: internet-learner-stall-fix
description: Use when internet_learner cycles all report rejected.
---

# Internet Learner stall fix
## Older root causes (15./16.09.26) — moved to references/

Per-class narratives for J–Z, AA–AG (15./16.09.26) live in
`references/root-causes-archive.md`; the rules are in the code, covered by
`tests/scripts/test_internet_learner_gate.py`. Two entries are NOT mere history:

- **Root cause T** — the Darwin autopilot rewrites `internet_learner.py`
  WHILE you edit it. Re-read the file before every patch, and verify your
  change survived after the next autopilot pass.
- **class 160 (23.09.26)** — an off-topic result PAGE is not a source for the query: root cause AG's recommended fix point, implemented (`is_off_topic_page`). Full entry in `references/root-causes-archive.md`. AG is partially fixed, NOT closed.
- **class 164 (23.09.26)** — a NON-ENGLISH distillate reaches the STORED row: `security-learn: Anwendungsmöglichkeiten ...` = a German Azure call-center paragraph as the `a` under an unrelated ENGLISH `u` (the SECONDARY `deep_learn`/smart_route door, `internet_learner.py` ~L5860 — the distill prompt does not constrain language). Measured 2/300 buffer rows; the same string was refused 15x in `buffer_junk` and appears 5x in the learn log over 8 days. NO code fix shipped: the language rule is already forbidden (Chinese Q&A-portal doctrine, `_is_qa_portal_chrome`) and an `a`-keyed near-duplicate rule is MEASURED-AND-REJECTED (`buffer_store.py` ~L3641) because the legitimately-repeating vLLM doc cycles would be deleted to save 2 rows. Full entry in `references/root-causes-archive.md`.
- **Root cause AG** — `deep_learn` ranks the WRONG page; deliberately
  unpatched. Do not 'fix' it on a rejection alone.

**This SKILL.md is at its 100 KB cap.** New root causes go into
`references/root-causes-archive.md` -- append **LF** (that file is LF-native;
a CRLF append flips ~60 lines) -- and only a ONE-LINE pointer is added here.
AW/AY (77-85), 96/97 (AZ), 98, 122 -> MEASURED-AND-REJECTED,
102/103, 109/110, 113-115, 118, 123/124 (GitHub releases-row + slide-nav
chrome; leaked into KTA competitor_gap), BF (deterministic `deep_learn`,
291/300), BC (NON-FIX) and BG/126 (a platform's own client-SDK family: stored
3x -- the sentence DRIFTS, so exact `_is_duplicate` missed it; same-`u` Jaccard
MEASURED-AND-REJECTED, 0.24-0.33 vs a legitimate 0.40) in
`references/root-causes-archive.md`. BE/BC/BF NAMED only, never written.
**134** (a newsroom INDEX page is not an article — a card's country tag welded
to the next card's headline; PAGE-level rule, text-level cannot see it) is
archived there too.
**138** (an ALL-CAPS nav lockup welded to prose AND repeated in Title Case — a
competitor's "Platform Demo" banner stored TWICE; the discriminator is the CASE
SHIFT, not a vendor literal, so the rule generalises. WELD alone = 26 prose FPs,
CASE-SHIFT alone = 2; the pair = 0 over ~4,600 real texts) is archived there too.
**165** (a site sidebar label run welded to its announce line; M1 >=2 distinct nav labels AND M2 the announce line -- each alone MEASURED-AND-REJECTED; also: concurrent writers collide on the CLASS NUMBER, build your commit in a worktree off origin/main) is archived there too.
**139** (a landing-page marketing-SLOGAN clause; the row had already been a
`duplicate` for a WEEK — the buffer rotates ~200 rows/day vs a 300-row cap so
exact `_is_duplicate` is a same-window guard, not a permanent one, and the leak
came back. Also: an EOL normaliser is NOT idempotent on an already-CRLF block —
guard `\r\r\n == 0`, and `git add` under global `core.autocrlf=true` stores an
LF blob: `git rm --cached` + `-c core.autocrlf=false add`) is archived there too.
TWO warnings stay live because they are behavioural, not history:

- run `which_rule_matches.py` BEFORE touching a rule -- the AJ/AQ/AR trap has
  fired FOUR times: your own control trips a PRE-EXISTING `_NAV_CHROME`
  marker, so add the topic-matched hostile control first. Probe the FULL stored
  string (300 chars) -- a truncated copy prints a false `INDIVIDUAL MATCHED: none`.
- never sync this LF-native archive with a text-patch tool: `patch` expanded a
  literal `\r` and corrupted the file at an UNCHANGED byte count. Append pure
  bytes, then assert byte-exact equality with the install copy.
- never wire a gate on a rejection alone (measured-and-rejected = delete the
  signature, keep the rows).

**109/110 (20.09.26)**: own-artifact echo family + 3 harness limits (probe
false-`SKIP`s mixed-case candidates; scores `a` ONLY, so no pair-rule is
measurable; `search_files` can NOT read `AppData/Local` → `grep`.
Pair-rule MEASURED-AND-REJECTED (archive).

CF/130-132 (22.09.26): source-tally CTA + date-stamp strip + credit byline; FIXED, refs/.
133 (22.09.26): doc-site product-nav weld; ALL 4 bare forms REJECTED, 3 two-token welds FIXED, refs/.
135/136 (22.09.26): arXiv submitter WELD + aggregator card header (needs a TitleCase-continuation test; 1+2 FPs without it), found by eyeballing the buffer tail -- FIXED, refs/.
149 (23.09.26): a nav-menu WELD run into a card title drawn TWICE; the discriminator is nav-run>=3@60 AND an ADJACENT exact repeat (d<=L) -- repeat-alone=88 ep FPs, nav-alone=13 prose FPs, pair=0/0; FIXED, refs/.
155 (23.09.26): a raw vLLM server LOG LINE stored as knowledge (`apiserver pid=` / `[scheduler.` / `INFO d-d h:mm:ss`); bare `\bpid=\d+` and `max model len` MEASURED-AND-REJECTED; FIXED, refs/. TRAP: `purge_buffer_rows.py` defaults to `--text-key a`, so a signature in `u` reports a false "nothing to drop".
156 (23.09.26): a HALLUCINATED LLM query (`neural duhmer: ...`) stored OFF-TOPIC tutorial prose -- no chrome gate can catch it, the defect is upstream in `_llm_novel_query`; a lexicon-free rule was MEASURED AND REJECTED (53/800 real headlines), so row purged + COUNT FIRST; refs/.
162 (23.09.26): a DECIMAL POINT is not a sentence terminator -- the extractor stored `... vulnerability (CVSS 3.` while the page continues `3.9) affecting ...`. NOT the class-85 NON-FIX: repair = pure WIDEN of the extractor boundary, never a reject gate. 21 extends / 0 shortens; FIXED, refs/.

**116/117 (20.09.26)**: no gate class at all -- step -1 found a whole
TESTED-BUT-UNCOMMITTED batch (AV again): `dry_run` never reached
`world_model.prune`, MSYS `OPENAMER_HOME` made a phantom tree, `prune()`
re-normalised 250M times, one 5 s health probe burned a slot. NEW TRAP: the
repo's `test_no_hardcoded_paths` rejects a path LITERAL in a DOCSTRING --
describe the MSYS form in prose. The mirror is TWO-WAY (live was AHEAD), so a
repo->live copy would have DELETED fixes -- union first. See archive.

**111/112 (20.09.26)**: 81 = own-artifact plan THIRD title → WIDEN the class-80
regex, not a new helper; 82 = German nav WELD + colon headline; the news ticker
has NO clean discriminator → signature delete. The 109/110 rows were still in
the buffer: a written verdict is not a cleanup. Also: `skill_manage(write_file)`
REPLACES a reference file — restore from the repo copy. See archive.

**119/120 (20.09.26)**: no learner gate in either — 119 was `self_improve.py`'s P2
rule deleting the `CYCLE_SECONDS` assignment it guards (`920131e54`, RED→GREEN
3/3); 120 was a 3-tree drift round with **9 drifts pointing BOTH ways** (4 files
live-AHEAD with a half-applied `chat_default` migration, 5 live-BEHIND incl.
`tool_server.py` which had LOST two utf-8 captures — ported up as `3a0ca2912`).
TWO live traps, both re-confirmed: (1) an autocrlf-off commit in a `git worktree`
still summarises a whole-file rewrite (423+/432- for 14+/23-) because the blobs
are LF and the worktree CRLF — **census the CR bytes in the BLOB**, and
`git diff --stat HEAD~1 HEAD` vs `--ignore-cr-at-eol` is the clean read; (2) the
mirror is two-way and the same tree can be ahead on one file and behind on
another in one run — `verify_three_copies.py` compares against the repo WORKTREE,
which sits on a foreign branch 36 commits behind, so its MISMATCH lines are
branch noise; `git cat-file blob origin/main:<f>` is the only truth. Also: a
`newline="\n"` cleanup silently flipped `online_buffer.jsonl` CRLF→LF (text-mode
`append` means CRLF is the store's contract) and 2 more `Share a lesson you
learned`-family echo rows were finally removed by signature (294→292, the 16
genuine answers asserted intact). See archive.

**121 (20.09.26)**: rotation exhaustion RE-CONFIRMED for the third round --
last 60 `duplicate` rejects 60/60 the identical `(u, a)`, 0 with a novel `u`;
57 recent `junk` candidates attribute ONLY to pre-existing helpers, zero novel
shapes -> no gate change. Same trap as 119/120 (see archive).

**128 (21.09.26)**: 121 re-confirmed (0/60 novel `u`) and the MECHANISM measured
-- `.il_seen_queries` is 800 entries but only **177 distinct**, and the avoid
window (`_recent_queries`, n=60) is **7.5% of the ledger** while **95% of the 623
real repeats are >60 entries apart** (median gap 67, mean 96). Widening `avoid`
to the full ledger is MEASURED-AND-REJECTED: only 2/8 cycle keywords still yield
a live headline vs 8/8 at n=60. Domain saturated, not broken. See archive.

## Counting the rejections — `buffer_junk.jsonl` rows have NO `ts`
`internet_learn_log.jsonl` rows carry `ts/source/result/elapsed_s`; the audit
rows in `buffer_junk.jsonl` carry ONLY `reason/u/a`. So a `ts`-prefix filter
against the audit file silently returns **zero** — live 22.09.26 that made a
busy day look like "the rejections never reached `store()`", which is wrong.
Count by **append order** (the file is append-only: the last N audit rows are
the most recent N rejections), and only then match a rate shift.
Also: `diagnose_learn_rates.py` counts a row as REJECTED for ANY non-"learned"
result, so `no insight` (shallow+deep both returned nothing) lands in the
rejected bucket. A rate drop can be **fewer candidates**, not a stricter gate --
distinguish the two before designing a rule.

## Trigger
`python internet_learner.py --once` (or the cron) reports
`cycle_x: rejected, not trained (shallow + deep read both gated)` on EVERY cycle,
and `online_buffer.jsonl` stays pinned at its cap (300 rows).

## Diagnose (fast)
-1. **BEFORE anything else: `git status --porcelain scripts/training tests/scripts`
   + `git diff --stat` in the repo.** A previous cron session can die after
   applying + testing a gate fix but BEFORE committing; the log then looks like
   "nothing new" while the working tree already carries the next class (root
   cause AV). Finish/verify/commit that work first, and re-sync ALL THREE test
   copies (the laptop one is often synced while `openamer-agent` is not).
0. Run the packaged rates table — this ONE table tells you whether it is a
   systemic regression (rate down across ALL cycles) or normal rotation noise
   (one weak source, or `duplicate` at the 300-row cap):

       python skills/software-development/training-scripts-hygiene/scripts/diagnose_learn_rates.py \
              --training-dir <live training dir>

   (lives in the sibling `training-scripts-hygiene` skill, alongside the other
   learner probes; formerly hand-written as scratch `_probe_rates.py` — bundled
   17.09.26 after the same table was re-derived yet again; see root cause U.)
   **Read the per-DAY table, not just the 7d one.** `--days 7` smooths a step
   change: on 17.09.26 the 7d row showed a healthy 70-77% while per-day showed
   the 13.09 gate-tightening (100% → ~48-68%, stable since) — a regime change
   and a fresh decline look identical in the aggregate. And the final per-day
   row is a PARTIAL day (cut at the current hour): never read it as a decline
   without saying so. `--json` for machine use.
1. `tail -5 internet_learn_log.jsonl` — confirm all cycles rejected.
2. `tail -100 buffer_junk.jsonl` — count reasons. `duplicate` = root cause A,
   `junk` on SERP-shaped text = shallow-path noise (fine), nav text = cause C.
3. `wc -l online_buffer.jsonl` + `cat .il_rotation` — cap reached?
4. Probe one query: run `deep_learn(q)` and print the result; if it returns page
   nav ("Generation RunPod SkyPilot ...") → root cause C.

## Root cause AH — ticker chrome + README changelog bullets, BOTH in one cron run (live 17.09.26)

Cron run started with the documented `cycle_e_competitors: rejected` line. The
rate check said **65% (last 20) / 57% (last 80) vs 82.6–82.9% all-time** — the
U/V signature — so U/V were verified present (`_fair_share_window` → 5 slices /
4000 chars ABCDE, `_search_urls(k=6)` → 6/6/6/6/6/6, `k2 != k6` 2/3) and the
file size was **stable** across the whole probe (no Darwin writer). No gate
change was warranted for the rejection itself: it was rotation noise.

**Both leaks below were found the cheapest way — run `--once`, then read the
tail of `online_buffer.jsonl` and eyeball the `u`/`a` pairs.** Neither showed up
in `buffer_junk.jsonl` (they were never rejected).

| cycle | u | a |
|---|---|---|
| `cycle_f_multi_domain` | Multi-domain learning (Walmart investors reject AI workplace report …) | `Walmart investors reject AI workplace report as automation expands in the US - The Economic Times Benchmarks CLOSED Nifty 23,118.` |
| `cycle_h_efficiency` | Efficiency learning (VPTQ: Extreme low-bit Quantization for real LLMs): How do agents run leaner? | `Inference: low decode overhead, best throughput, and TTFT News [2024-10-14] 🚀 Add Rocm support [2024-10-6] 🚀 Try it on Google Colab [2024-10-5] 🚀 Add free Huggingface Demo : Huggingface Demo [2024-10-4] ✏️ Updated the VPTQ tech report and fixed typos.` |

Both are 129 / 251 chars **with digits** → the `>=90` length trust AND the
technical-signal gate both fired; no existing marker matched.

**Markers added (data-only, BOTH files — the Q/R/S pitfall).** Commits
`1f5a17cbc` (ticker) and `95d4aa156` (changelog):

| marker | where | measured |
|---|---|---|
| `closed nifty` | both | 1 hit, and it IS the leak → 0 FP |
| `the economic times benchmarks` | both | 1 hit, IS the leak → 0 FP |
| `add free huggingface demo` | both | 2 hits (same row duplicated), BOTH the leak → 0 FP |

**Candidates measured and REJECTED — the topic-word trap again:**
| candidate | why rejected |
|---|---|
| `nifty` (bare) | 1 hand FP + 1 live FP: `Benchmarks from the Nifty index showed a 2% gain…`, `…encompassing Nifty 100 intraday and daily price data…` |
| `benchmarks closed` (bare) | 1 hand FP: `The agent benchmarks closed-source and open-weight models on the same harness.` |
| `add rocm support` | 1 hand FP: `Add ROCm support for AMD GPUs to the inference backend.` |
| `try it on google colab` | 1 hand FP: `You can try it on Google Colab without installing anything locally.` |
| `low decode overhead` | 1 hand FP: `The agent benchmarked low decode overhead and best throughput on TTFT.` |
| `best throughput, and ttft` | 1 hand FP (declarative on the same topic) |

A **structural alternative** measured clean and is a candidate for a future
class-wide detector: **`>=3` bracketed dates `\[\d{4}-\d{1,2}-\d{1,2}\]` → 2
hits, 0 FP both corpora** (`>=2` was rejected: 2 live FPs on the `[2024-10-18]
🌐 Open source community contributes…` row). Same for `>=2` rocket-emoji
bullets (2 hits, 0 FP). Not needed for these single leaks — prefer the tight
literal while only one row shape is live.

**Cleanup + verify (the standard shape):** both leaks removed **by signature**
(`is_junk` would drop the 12-row baseline), census 297/13 → 296/12, then
297/14 → 295/12, 0 unparsable, 53 structural-connection rows preserved.
`pytest tests/scripts/test_internet_learner_gate.py -q` → **42 passed**
(new `test_market_ticker_chrome_…` and `test_readme_changelog_bullet_list_…`,
each asserting BOTH gates plus prose counter-cases); `tests/scripts` →
**182 passed**. Two commits pushed.

### Trap that cost a cycle here: `patch` DELETED my own previous marker
Patching `_NAV_CHROME` with `old_string = '    "the economic times benchmarks",'`
**replaced that line** with the new block — the nifty marker vanished, leaving
only the changelog one. The probe caught it (`nifty marker line: []`). When
appending to a tuple with `patch`, anchor on the **line BEFORE** the insertion
point (or just use the byte-level AST-anchored script). Fix was a 3-line
re-insert, then `ast.parse`. Always re-grep every marker you believe is in the
file after any `patch`/`write_file` on these modules.
Related: after an insert, **all hardcoded line numbers shift** — the second
`_NAV_CHROME` edit asserted `lines[371] == b")"` and blew up with the previous
comment text. Re-derive the anchor with `ast` each time; never reuse a line
number from an earlier probe.

## Verify a writer-gate change like this (what "0 collateral" looks like)
1. `is_junk(bad) == True` on the exact leaked strings, `False` on 3 real prose
   samples + the engine's own baseline row.
2. Re-scan the whole buffer: flagged set must grow by **exactly** the leaked
   rows (live: 24 → 26, i.e. 2 new hits), then drop back to **24** after deleting
   them (`flagged: 26 -> 24`, the historical baseline).
3. `openamer-repo/.venv/Scripts/python.exe -m pytest tests/scripts/test_internet_learner_gate.py -q`
   → `12 passed` (added `test_writer_gate_agrees_on_the_new_chrome_and_binary_shapes`,
   which asserts BOTH gates on both shapes). Suite grew with each shape:
   **`23 passed` as of 16.09.26** (root cause Y added
   `test_german_dictionary_serp_chrome_is_gated_on_both_paths`, which asserts the
   leak is gated on BOTH paths AND that two real `…;` vLLM/quantization rows stay
   clean — the one-directional version would pass the wrong fix).
4. Sync the two modules into `openamer-repo/scripts/training/` (they must be
   byte-identical to the laptop copies — `diff` first), commit, push.
5. Run 3–4 × `--once`. Post-fix live: 1 learned / 2 rejected, where both
   rejections were `junk` (SERP-shaped deep-read fallback) and `duplicate`
   (buffer at cap) — **read `tail -6 buffer_junk.jsonl` before calling it a
   regression.**

## Root cause AI — company/Wikipedia infobox FINANCIAL label chain (live 17.09.26)

Second cron run of the day. Started on the documented `cycle_d_docs: rejected`
line. Rate: last 10 50 % / last 20 50 % / last 80 50 % vs **all-time 82 %**
(n=1711) = the U/V signature, so U/V were verified **before** inventing anything:
`_search_urls(k=6)` → `6,6,6,6,6,6`; `_fair_share_window` → 5 slices / 4000
chars; file size **stable** over 30 s (no Darwin writer). No gate change was
warranted for the rejection — rotation noise. `buffer_junk` last 40:
`21 junk / 18 duplicate / 1 no-tech-signal`, all documented shapes.

The find came from the buffer tail, twice:

**1. Two root-cause-AG rows (NOT gate leaks — deleted, no code change):**
| cycle | u | a |
|---|---|---|
| `cycle_g_security` | Security learning (Detecting prompt injection attacks …) | `Kraków – Wikipedia, wolna encyklopedia — Kraków jest położony … ; Oficjalny serwis BIP …` |
| `cycle_h_efficiency` | Efficiency learning (Pushing the Limits of LLM Quantization via the Linearity Theorem) | `November 5, 2025 Share 2 Min Read Photo by Abid Shah on Unsplash Amazon has issued a cease-and-desist letter to Perplexity …` |

Both measured `writer=False extract=False` — **topically unrelated whole
articles**, i.e. the documented root cause AG (deep_learn ranks the wrong page).
Do NOT invent a gate for these: the `Kraków` row is a Polish SERP pair and the
Amazon row is a news lede, so any "news-ness"/"encyclopedia" marker would be a
topic word. Removed by signature (`wolna encyklopedia`, `on unsplash`) →
300 → 298 rows.

**2. A REAL leak the very next `--once` produced — the infobox (this root cause).**
```
u = Competitor intelligence: JetBrains IDEs Go AI: Coding Agent, Smarter Assistance, Free Tier
a = CEO [ 1 ] Revenue 15,065,029,000 Czech koruna (2024) Operating income
    2,041,654,000 Czech koruna (2024) Net income 2,479,110,000 Czech koruna
    (2024) Total assets 17,426,568,000 Czech koruna (2024) Number of
    employees 2,800 [ 2 ] Website jetbrains .
```
248 chars **with digits** → the `>=90` long-prose trust AND the technical-signal
gate both fired; `_is_nav_list` wants ≥6 TitleCase tokens with no comma, so a
mixed label chain never matched. Commit `aaf11271e`.

### Marker selection was the whole cost — every literal is a topic-word trap
| candidate | buffer hits | HAND-prose FP | verdict |
|---|---|---|---|
| `operating income` | 1 | **3** | REJECTED |
| `czech koruna` | 1 | **3** | REJECTED |
| `revenue [\d,]{6,}` | 1 | **1** | REJECTED |
| `ceo \s*\[\s*1\s*\]` | 1 | 1 | REJECTED |
| `\(\s*20\d\d\s*\)\s*operating income` | 1 | 1 | REJECTED |
| `number of employees…website` | 1 | 0 | ok but narrower need |
| **structural: ≥2 (label, year-paren)** | **1 (the leak)** | **0/13** | **SHIPPED** |

`grouped-numbers >= 3` also scored clean on the buffer (1 hit / 0 FP) but is
**useless as a corpus scan**: on RAW JSON lines it reads 437/437 and 3056/3056
(the JSON has lots of long numbers). Scan the **text fields** — then it is 7/3056
on `longterm_episodes`, all in unrelated X-batch report texts.

### The fix — structural, in BOTH gates
`buffer_store.is_financial_infobox(text)` = `len(_FINANCIAL_LABEL_RE.findall) >= 2`
where `_FINANCIAL_LABEL_RE = (revenue|operating income|net income|total assets|
number of employees)[^()\n]{0,30}\(\s*(?:19|20)\d\d\s*\)`, cap `len <= 1200`.
An infobox row *repeats* `Label <huge grouped number> … (yyyy)`; real prose does
not. Wired into `buffer_store._is_nav_chrome` (writer gate → covers
`active_learn` / `online_learning`) AND called from `internet_learner._is_junk`
via the lazy `from buffer_store import …` sibling idiom (logic, not a page
phrase → **no `_JUNK_RE` mirror**, exactly like `is_contact_block`).

Measured: leak `writer=True extract=True`; **0 FP on 13 hostile counter-cases**
including `Llama 2 (2023) and Llama 3 (2024) improved long-context reasoning`,
`GPT-4 (2023) scored 91.2% while GPT-5 (2024) reached 95.1%`,
`Total assets ( 2023 ) were 17,426,568,000 koruna at the end of the year.`,
`Number of employees grew to 2,800 ( 2024 ) across the Czech and German offices.`
(only a deliberately infobox-shaped synthetic — `Revenue 2024 ( 2024 )` ×3 —
flags, which is correct); 0 hits over 3,056 `longterm_episodes` texts.

Cleanup by signature (`czech koruna`): **299/13 → 298/12** (baseline), 53
structural-connection rows preserved, 0 unparsable, CRLF intact.
`pytest tests/scripts/test_internet_learner_gate.py -q` → **46 passed** (new
`test_financial_infobox_label_chain_is_gated_on_both_paths` asserts BOTH gates on
the leak + 11 prose counter-cases); `pytest tests/scripts -q` → **186 passed**.

### Mechanical traps that cost the most time here
- **The `_is_nav_chrome` wire anchor must be the two-line form.** `"    if
  _is_package_index_chrome(text):\n        return True"` — a **one-line**
  anchor silently matched 0 times and the apply script aborted on the assert.
  Build the anchor as `crlf("…\n        return True")`, not as a bare line.
- **Appending a test needs a separator.** `raw.rstrip(b"\r\n") + TEST` glues the
  new `def` onto the previous line's tail → `SyntaxError: invalid syntax` at
  `assert not IL._is_junk(meta), metadef test_…`. Use
  `body + b"\r\n\r\n\r\n" + TEST.replace("\n","\r\n").encode() + b"\r\n"`.
- **`git status` in this repo is NOISY with foreign cron paths** (`tools/mcp_tool*`
  deletions, `reports/darwin-*`, `.bugbot/bugbot.log`, `scripts/auto-code-review.py`).
  Always `git add` the three explicit paths and check `git diff --cached
  --name-only` before committing — never `git add -A`.
- Live re-verify after the fix: 3 × `--once` → 2 learned / 1 rejected. The
  rejected one and the two learned rows all measured `writer=False extract=False`;
  the remaining off-topic row (`Physics … antiprotons`) is root cause AG again,
  which stays deliberately unpatched.

## Root cause AL — FOUR chrome classes in ONE cron run, and the pitfall that a NEW rule can break an OLD test (live 17.09.26)

Cron run began with the documented `cycle_c_github: rejected` line. Rate said
**50 % (last 20) / 51 % (last 80) vs 81 % all-time (n=1780)** — the U/V
signature — so U/V were verified BEFORE inventing anything (`_search_urls(k=6)`
→ 6; `deep_learn` k2/k6 on 4 diverse queries → 2/4 identical windows, and the
2 `False` cases were query-dependent content artifacts, not the dead-code bug).
`buffer_junk` last 25 = `duplicate` at the 299/300 cap + documented junk shapes
= rotation noise. **No gate change was warranted for the rejection itself.**

The whole find came from the prescribed cheapest method — run `--once`, read the
BUFFER TAIL, eyeball `u`/`a` — repeated after each fix. All four rows passed
BOTH gates and NONE ever appeared in `buffer_junk.jsonl`.

| class | helper | measured |
|---|---|---|
| 33 | `_is_news_card_stub` — card headline + glued relative-date label + truncated counter tail (`... misalignment Sep 17 7.`) | 1 hit, IS the leak / 0 FP / 0 le |
| 34 | `_is_relative_time_nav_chain` — relative-time bullet ANDed with `For You / Latest / Trending` nav labels | 1 hit, IS the leak / 0 FP / 0 le |
| 35 | `_is_date_heading_listing` — date-stamped headline listing (blog archive) | 2 hits, BOTH leaks / 0 FP / 0 le |
| 36 | `_is_repo_tab_statbar_chrome` — `Code Issues Releases` tab chain ANDED with a `\d+ MiB <Lang> \d` stat bar | 1 hit, IS the leak / 0 FP / 0 le |

Class 33 is only 70 chars, so the `>=90` long-prose trust never applied — a
reminder that the trust is not the only way chrome gets in. Its anchor is the
TAIL (`$`), because a bare `<Mon> <day>` is an ordinary date.

### THE PITFALL — a broad new structural rule can re-flag an OLD test's counter-case prose
For class 35 my first rule was `>=3 full dates` OR `>=2 dates AND slash-category
breadcrumb`. It measured **clean on the live buffer (2 hits, both leaks) and on
every hand-written control** — and then `pytest` went RED on
`test_blog_archive_listing_is_gated_on_both_paths` (class 24), whose counter-case
prose is

    `...posts under headings like Insights July 17, 2026 and News May 29, 2026,
     but the agent should parse the article body.`

Two full dates + TitleCase labels → my rule flagged real prose.

**Rule: candidate markers must be run against the EXISTING gate test suite's
counter-case prose, not only against your hand controls + the live corpus.**
Hand controls and the live buffer agreed with the broken rule; the repo's own
regression corpus caught it in 3 s. So: apply, then run
`test_internet_learner_gate.py` BEFORE the cleanup/commit, and treat a new
red as YOUR rule being wrong, not the old test being stale.

The fix that survived: discriminate on **Title-Case density** of a title
listing, not on the date count —
`len(_FULL_DATE_RE.findall(t)) >= 2 AND upper_words >= 8 AND upper/total >= 0.5`
(measured 0 buffer FPs, 0 ctrl FPs, 0/3,056 le, and the class-24 leak is still
gated by its own rule). `_TITLE_WORD_RE = r"[A-Za-z][A-Za-z'./-]*"`.

### THE OTHER PITFALL — appending a test with `rstrip("\r\n")` causes EOL churn
`txt.rstrip("\r\n") + "\r\n\r\n\r\n" + TEST` normalises the file's LAST line,
which was one of the 58 pre-existing **lone-LF** lines in
`test_internet_learner_gate.py` (that file is NOT pure CRLF — it has 58 lone LFs
at HEAD; do not "fix" them). Result: `git numstat` showed `48 added, 1 removed`
and the lone-LF census went 58 → 57. Correct approach — **pure byte append**:
`open(p,"wb").write(open(p,"rb").read() + TEST.replace("\n","\r\n").encode())`,
then assert `numstat` has **0 removed** and the lone-LF count is **unchanged**.

Note the gate modules themselves ARE pure CRLF (2597/1340 lines, 0 lone LF),
while the test file is not — check each file's census separately.

### Session shape that worked here
Fix 33+34 and 35+36 in two passes, but the loop is the same: measure → apply to
BOTH gates in all 3 copies → re-scan buffer → **run pytest** → cleanup by
signature → append test (pure bytes) → mirror to the laptop test copy → commit
with a msg FILE (backticks in a `-m` string get eaten by git-bash:
`command substitution: syntax error near unexpected token '<'`) → push.
Result: `56 passed` gate file, `212 passed` `tests/scripts`, post-fix live
cycles 2/3, 2/4 and 3/3 learned with no chrome in the tail.

The AM run (three classes, 37–39) confirmed the loop scales: one measure → apply
→ pytest → cleanup → test → commit cycle per class, `59 passed` / `215 passed`,
3 pushes, and only the alias trap above cost extra rounds.

## Root cause AM — THREE chrome classes in ONE cron run, and the `re` vs `_re` alias trap (live 17.09.26)

Cron run began on the documented `cycle_c_github: rejected` line. Rate said
**54.5 % for the partial day (12 ok / 10 rej) vs 81–83 % all-time** — inside the
documented band, so no gate change was warranted for the rejection itself. The
file size was **stable** over 20 s (`91496` both samples) → no Darwin writer;
`.il_rotation` = 1803. All three finds came from the prescribed cheapest method:
run `--once` a few times and read the BUFFER TAIL (`u`/`a`), repeated after each
fix. All three rows passed BOTH gates and NONE was ever in `buffer_junk.jsonl`.

| class | helper | measured |
|---|---|---|
| 37 | `_is_hn_feed_listing_chrome` — a repeated aggregator feed row: relative time + `\| N comments` + points + headline, **>=2 occurrences** | 1 hit, IS the leak / 0 FP / 0 le |
| 38 | `_is_marketing_hero_cta_chrome` — landing-page hero: availability line + nav CTA + tagline + `[*]` marker + brag opener `With over` / `Mit über` | 3 hits, ALL THREE the same page hero / 0 FP on 26 controls / 0 le |
| 39 | `_is_platform_selector_listing_chrome` — `macOS Apple Silicon (arm64)`-style selector within 200 chars of `r/<name> community` | 1 hit, IS the leak / 0 FP on 21 controls / 0 le |

**Class 37 — the discriminator is REPETITION, not the parts.** The single-occurrence
form `\b(?:minutes?|hours?|days?|weeks?|months?)\s+ago\s*\|\s*\d{1,5}\s*comments\b`
flagged the control `The review took 2 days ago | 4 comments per reviewer were
recorded.` → REJECTED as the shipped rule. `>=2` findall measured 1 buffer hit
(the leak), 0/12 controls, 0/3,056 episodes. `by <user> N days ago` and bare
`\d+ comments` were also rejected (real prose + 3 live episodes).

**Class 38 — one page hero stored THREE times in one buffer** (once in German via
`cycle_e_competitors`, twice in English at rows 17/87). Tell: rows 17 and 87 were
**byte-identical**; always group the flagged rows before designing a marker, or
you will write a marker for one third of the leak. The looser
`(?:Read docs|Doku lesen)[\s\S]{0,120}?\[\*\]` form was REJECTED on measurement
(3 control FPs: `Read docs to learn how the [*] wildcard expands in glob
patterns.`, `Doku lesen hilft, weil [*] die Pflichtfelder kennzeichnet.`,
`Read docs and [*] will be replaced by the matched text.`). Only the
`[*]`-adjacent brag opener survived.

**Class 39 — class 34's rule needs the `For You / Latest / Trending` labels;
this shape has none.** Platform selector + `DISABLED` + `…` + upvote count +
`r/... community` + relative time + forum title. Candidates A3/A4 (tighter
anchors) also measured clean; A2 (`r/<name> community`, the widget's own label)
shipped as the most specific. The `(arm64...)` + relative-time form was
REJECTED — 3 control FPs.

### THE PITFALL — `internet_learner.py` uses `re`, `buffer_store.py` uses `re as _re`
Copy-pasting one helper into both files raises `NameError: name 're' is not
defined` (or `_re`, in the other direction) **at import time**, which shows up as
a `pytest` collection error, not a gate failure. This cost two extra apply/fix
round-trips in one run (once for class 37 in `buffer_store`, once for class 38 in
`internet_learner`). Before writing the helper, grep the target file's import
alias:
```
grep -n "^import re" <file>     # `import re` vs `import re as _re`
```
Ship the constant with the correct alias per file — or avoid the issue entirely
by writing `import re`-free helpers. Never assume the two modules agree.

### Also: build the anchor with CRLF, and expect it to be the blank-line-separated two-line form
`"    if _is_relative_time_nav_chain(t):\r\n        return True\r\n"` is the
reliable insertion anchor (LF-only anchors match 0 times on these pure-CRLF
modules). Anchor on the PREVIOUS class's call, not on a line number — every
insert shifts the file.

Cleanup + verify (the standard shape, per class): remove leaks by signature with
the CRLF-split reader (`split("\r\n")`, never `readlines()`), assert the dropped
count, rewrite with `newline=""` + one record per CRLF. Live censuses:
300/7 → 299/7 (cls 37), 300/7 → 297/7 (cls 38), 300/7 → 299/7 (cls 39); **7 is
the baseline** writer-flagged count in this buffer (rows 5, 9, 19, 27, 29, 36, 45
= pre-existing SERP/listing shapes — do NOT "clean" those), 53
structural-connection rows preserved, 0 unparsable every time.
`pytest tests/scripts/test_internet_learner_gate.py -q` → **56 → 57 → 58 → 59
passed**; `pytest tests/scripts -q` → **212 → 213 → 214 → 215 passed**. Three
commits pushed. Post-fix live cycles: 2/3, then 1/3 where both rejects were
honest (`duplicate` at the 300 cap) — **read `buffer_junk` before calling a
rejection a regression.**

## Root cause AP — the learner's OWN deep-read prompt echoed back as a bullet chain (class 42, live 17.09.26)

Cron run began on the documented `cycle_g_security: rejected` line. Rate said
**30 % (last 10 and last 20) vs 80 % all-time (n=1828)** — the U/V signature —
so U/V were verified BEFORE inventing anything: `_search_urls(k=6)` → **6/6 on
all 5 diverse queries**; `_fair_share_window` → **5 slices**; buffer size
byte-stable (`90761` both samples) → no Darwin writer. `buffer_junk` last 25 =
`duplicate` at the 298/300 cap + documented `junk` shapes = rotation noise, so
**no gate change was warranted for the rejection itself**. Writer-gate census
**0 of 298** → the buffer was clean at entry.

**The leak was CREATED BY THIS RUN** — a reminder that "buffer was clean at
entry" does not survive six `--once` cycles. After 6 rejects the 7th cycle
(and the 8th) learned, and the 8th stored the learner's own task template:

    "\n   - Input is a list of daily paper submissions with titles, authors, and
     brief tags/counts\n   - I need to identify the single most valuable technical
     insight for an autonomous AI agent from these paper titles/descriptions\n
     - Output must be a sin"

190 chars **with digits** → the `>=90` length trust AND the technical-signal
gate both fired. **Do not read a `learned` line as success** — this one's log
line (`efficiency-learn: "\n - Input is a list of daily paper submissions …`)
was visibly suspicious, but the skill's rule stands: read the BUFFER tail
`u`/`a` pairs, because the stored form is what trains.

Why every existing marker missed it:
- `_INSTRUCTION_OPENER_RE` is **START-anchored** (`^\s*\**\s*…`) — this text
  opens with a `"` + newline, so the anchor never lands, even though `I need to`
  is literally in its alternation.
- `_is_nav_list` wants ≥6 TitleCase tokens with no comma — a mixed task-frame
  bullet chain is neither.

### The discriminator is the BULLET CHAIN, not the phrase
`_is_prompt_echo_bullet_chain(text)` = `>= 2` bullets each opening with a
task-frame word, via `_PROMPT_ECHO_BULLET_RE`:
`(?:^|[\r\n])\s*[-*•]\s+(?:Input\b|Output\b|I need to\b|I must\b|I should\b|The task\b|Identify the\b|Steps?\b|Constraints?\b|Format\b)`
Wired into BOTH gates (extraction `internet_learner._is_junk` + writer
`buffer_store._is_nav_chrome`) in all 3 copies — the AH both-files rule.

**Every single-phrase candidate was measured and REJECTED:**

| candidate | buffer | hand FP | verdict |
|---|---|---|---|
| `\bInput is a list of\b` | 1 = leak | **3** (`Input is a list of tokens…`, `The input is a list of papers…`, `In the benchmark, input is a list of 512 sequences…`) | REJECTED |
| `\bI need to identify the single\b` | 1 = leak | 1 | REJECTED |
| `\bfor an autonomous AI agent from these\b` | 1 = leak | 0 | ok but narrower than the class |
| `\bpaper submissions with titles\b` | 1 = leak | 1 | REJECTED |
| **bullet-triad (`>=2` task-frame bullets)** | **1 = leak** | **0** | **SHIPPED** |

Measured clean the strong way — **my rule ALONE**, not `_is_nav_chrome`:
1/300 buffer (= the leak), **0/3,056** `longterm_episodes`, **0/591** string
literals extracted from the gate test file, 0/13 hand controls.

### PITFALL — `_is_nav_chrome` FPs are NOT your rule; test YOUR helper in isolation
The first verify loop measured `control FPs writer=0 learner=1` and
`test-literal FPs: 35`, `episode FPs: 74/3056`. That looked like massive
collateral. It was not: the 35 and the 74 came from **pre-existing** markers
(GitHub repo-listing rows, `_NAV_CHROME` phrases like `Let Chat …`, date
headings) that those corpora legitimately trip. Only the learner control
(`I need to identify the single most valuable technical insight from the
report.`) was mine — and the diagnostic showed
`_INSTRUCTION_OPENER_RE.match(ctrl) == True` (pre-existing rule), while
`_is_prompt_echo_bullet_chain(ctrl) == False`. **Always probe the new helper
directly**; a corpus FP count through the composite gate tells you nothing
about your change. Same lesson as the AJ/AI control-corpus pitfall, third
occurrence — the skill now says: isolate first, diagnose which rule matched
second, only then conclude.

### Also — a `learned` cycle can hide the leak behind a clean-looking tail
After the cleanup, the post-fix cycles gave 1 learned of 3 (`cycle_c_github`,
real MAF content, `writer=False extract=False`) — read the buffer, not the
log, and re-run the census **after** every fix (`299` records, 0 unparsable,
53 structural rows, writer-gate 0).

Cleanup + verify (standard shape): leak removed by signature
(`Input is a list of daily paper submissions with titles`,
`I need to identify the single most valuable technical insight for an autonomous AI agent`),
**300 → 299** records, `0 unparsable`, CRLF intact, **53** structural-connection
rows preserved, writer-gate census **0**. Test appended as **pure bytes**
(lone-LF census 58 → 58 for the repo file, 0 → 0 for the laptop copy), and the
3 CODE copies + repo test verified byte-identical via `md5sum` (repo ==
laptop == openamer-agent: `230f36de…` learner, `70170f3e…` store).
`pytest tests/scripts/test_internet_learner_gate.py -q` → **61 → 62 passed**
(new `test_prompt_echo_bullet_chain_is_gated_on_both_paths` asserts BOTH gates
on the leak + 10 prose counter-cases); `pytest tests/scripts -q` →
**217 → 218 passed**. Commit `bb0d00ae2`, `numstat` **93 added / 0 removed**
(no EOL churn), pushed `HEAD:main` from the foreign branch
`fix/28-respawn-test-psutil-hermetic` (`merge-base --is-ancestor main HEAD` →
FF_SAFE), `origin/main` re-read = `bb0d00ae2…`, `git branch -r --contains`
confirms `origin/main`.

## Root cause AO — an EXISTING strip-helper whose guards were one variant too narrow (class 41, live 17.09.26)

Cron run began on the documented `cycle_h_efficiency: rejected` line. Per-day rate
37–60 % (15:00 hour partial, 0/4) vs 81 % all-time → inside the documented band, so
**no gate change was warranted for the rejection itself**; `buffer_junk` last 20 =
`12 duplicate` (buffer at 297–300 cap) + `6 junk` + `2 no-tech-signal`, all
documented shapes. Buffer tail was clean (0 of 298 writer-flagged).

**The leak came from running `--once` and reading the BUFFER TAIL — twice in a row.**
`cycle_b_papers` learned a row whose LOG LINE showed the chrome
(`Yash Thakker CoreWeave NVIDIA Sep 17, 2026 · 8 min read Databricks Deploys GPT-6 (56.2s)`)
even though the STORED text was clean — so *do not judge a cycle by its log line*.
The stored rows that *had* leaked were two `min read` blog cards:

| u | a (stored) |
|---|---|
| `Latest research insight: Breaking the 1.58-bit Barrier …` | `AI Agents 11 min read AI Agent Cost Benchmarks: Tokens, Latency, and Dollars per Task Original 2026 benchmark: …` |
| `AI model exit strategy` (fresh) | `Start the challenge Blog 18 April 2026 / 24 min read 8 best open-source AI agent frameworks on GitHub in 2026 The best …` |

### THE LESSON — check whether an EXISTING helper's GUARDS are too narrow before writing a new class
The repo already had `_strip_trailing_read_time_header` (17.09.26, class-40 era) for
exactly this family. Both live rows still got through because of TWO guards:
1. `body[:1].isupper()` — row 2's body starts with a **digit** (`8 best open-source …`).
2. `_BLOG_HEAD_DATE_RE.search(head)` required a dateline — row 1's head is a bare
   category label (`AI Agents`) with **no date at all**.

So the fix was to **relax two guards**, not to add a 4th chrome class. Guard 2's
replacement keeps a structural discriminator: without a dateline the head must be a
short (≤4 words) **pure-TitleCase label chain with no lowercase words**. Real prose
that merely mentions a read time sits inside a sentence and carries lowercase words,
so it stays untouched. New constant `_BLOG_HEAD_LOWER_RE = re.compile(r"\b[a-z]{2,}\b")`.

Measured (0-collateral proof): 2/2 leaks stripped with a **byte-identical body**;
**0 of 3,056** `longterm_episodes`; **0** hand-written prose controls; and — the
strongest form — a **pre/post module diff of `_clean_insight` output on all 8 control
strings = 0 diffs** (load the backup module with `importlib` and compare, instead of
only asserting the new behaviour).

**Do not treat a `min read` control that `_clean_insight` returns `""` for as YOUR
regression** — two of the 8 controls already returned `""` pre-edit (short non-tech
signal). Always diff old-vs-new module output before hunting a regression you did not
cause. The 2 hand-written "hostile" controls (`Machine Learning 5 min read The study
found that quantization helps.`) ARE correctly stripped — they are chrome-shaped by
construction, so a harness that lists them as `ctrlFP` is reporting the intended
behaviour, not a bug.

### PITFALL — the strip helper was applied to the LAPTOP copy only, so the REPO test went red
The first apply pass edited only `AppData/Local/openamer-laptop/scripts/training/internet_learner.py`;
`pytest` in `openamer-repo` then failed the new test because the repo copy still had
the old guards. **After any apply, `md5sum` all THREE copies before running pytest** —
one red suite here was purely a missing sync, not a wrong rule. (Standard: Repo=SoT,
laptop=LÄUFT, openamer-agent=older copy; all three must be byte-identical.)
The repo file is pure CRLF and the laptop copy too, so the same
`norm(s) = s.replace("\n", eol)` script applies to all three unchanged.

Cleanup + verify (standard shape): 2 chrome rows **plus the documented root-cause-AG
off-topic row** (`Databricks Deploys GPT-6 …`) removed by signature → **300 → 297**,
`0 unparsable`, CRLF intact, **53** structural-connection rows preserved, writer-gate
census **0 of 297**. The cleanup script's `assert len(dropped) == 2` fired on the
third row — **keep that guard and widen it deliberately** after identifying the extra
row, rather than deleting the assert.
`pytest tests/scripts/test_internet_learner_gate.py -q` → **60 → 61 passed** (new
`test_midtext_read_time_header_without_dateline_is_stripped`, appended as pure bytes:
42 added / 0 removed, lone-LF census 58 → 58); `pytest tests/scripts -q` →
**216 → 217 passed**. Commit `0cc459b21`, pushed `HEAD:main` (branch was again
`fix/28-respawn-test-psutil-hermetic`; `merge-base --is-ancestor main HEAD` → FF_SAFE,
`git branch -r --contains` confirms `origin/main`).
Post-fix live: 3 × `--once` → all rejected; `buffer_junk` shows honest reasons
(`duplicate` at the cap + already-gated shapes) and the buffer tail is 0-of-297
writer-flagged. **Read `buffer_junk` before calling a rejection a regression** — again.


## Moved to references/ (same content, loaded on demand)

- `references/root-cause-an-mid-text-byline-published-dd-mon-y.md` — Root cause AN — mid-text byline + `Published <dd Mon yy>` he; Root cause AQ — TWO chrome classes in ONE cron run + the imp; Root cause AR — THREE chrome classes in ONE cron run, and th; Root cause AU — FIVE chrome classes in ONE cron run (67–71),; Not every rejection is a regression — check the reason first; Root cause AI — rate drift with rejects rotating = NO fix ne; …
- `references/root-cause-as-six-chrome-classes-in-one-cron-run.md` — Root cause AS — SIX chrome classes in ONE cron run (58–63), ; Root cause AT — THREE chrome classes in ONE cron run (64–66); Root cause AT — moved to references/; Root cause AV — TWO classes (75, 76) + the "a previous cron 
