---
name: audit-pii
description: Pre-commit PII gate for the public repo. Regenerates the denylist, runs the deterministic scan over changed public files, then dispatches a fresh subagent for a semantic PII pass that catches real names/companies/emails the denylist misses. Run before committing or pushing public artifacts (tests, skills, framework, docs, tool code).
argument-hint: "(no args — scans staged + unstaged changes to public files)"
user-invocable: true
allowed-tools: Read(*), Glob(*), Grep(*), Bash(PYTHONIOENCODING=utf-8 python3 tools/gen_pii_denylist.py:*), Bash(PYTHONIOENCODING=utf-8 python3 tools/check_public_pii.py:*), Bash(git status:*), Bash(git diff:*), Bash(git ls-files:*), Bash(git check-ignore:*), Task
---

# Audit PII — Pre-Commit Public-Repo Leak Gate

The job-search OS repo (`claude-job-search-os`) is **public**. This skill is the
commit-time gate that stops a real contact, pipeline/target company, email, or phone
number from shipping into a public artifact (tests, `.claude/skills/`, `framework/`,
`docs/`, tool code/comments, top-level `*.md`).

Two layers, by design (per `feedback_generalize_examples_in_public_artifacts`):

- **Deterministic** (`tools/check_public_pii.py`, always-on PreToolUse hook + re-run here):
  high-precision exact match against the gitignored denylist. Catches known tokens.
- **Semantic** (this skill's subagent): high-recall judgment pass. Catches *new* names
  not yet on the denylist, ambiguous brand-words the denylist deliberately skips
  (e.g. real companies that are also dictionary words), emails, phone numbers, and
  any other identifying detail. This is the layer the deterministic hook cannot do.

Run this **before every commit or push that touches public files.** It is the
commit-flow step — there is no separate git pre-commit hook.

## Boundary (KEEP vs SCRUB)

Per `memory/feedback_nick_pii_redaction_boundary`:

- **KEEP (public-safe):** real employers/schools (Zuora, McKinsey, Tuck, Duke, Yahoo,
  ESPN), public-figure authors (Ali Rohde, Ryan Holiday, Molly Graham), generic
  products (Notion, Stripe, Anthropic, GitHub), Nick's own handle/name where already
  public, Raphael attribution.
- **SCRUB (leak):** pipeline/target companies, recruiter and contact names, real
  emails/phones, side-venture names, donor/WPI work, anything sealed.
- **Ambiguous → flag, don't auto-edit.** Surface it and let Nick decide.

## Steps

### Step 0 — Check for non-main ref exposure on the public remote

```bash
git ls-remote origin
```

Only `HEAD` and `refs/heads/main` should be present. Any other ref — most
commonly `refs/pull/N/head` from a merged/closed PR — can serve gitignored or
sealed file content from that PR's tree/history even when `main` is clean,
because deleting a branch or force-pushing `main` does **not** remove pull
refs. If any non-`main` ref appears, flag it as a **blocking** finding: the
only reliable fix is to delete and recreate the repo from the current clean
`main` (pull refs do not survive repo recreation). A GitHub Support
sensitive-data-removal request is the fallback if recreation isn't viable.
Origin: 2026-07-07 fable-audit finding, confirmed live and remediated
2026-07-08 via delete-and-recreate (`memory/audit-2026-07-07.md`).

### Step 0b — Full-tree + history + remote-ref sweep (mandatory before any squash, filter-repo, or force-push)

The routine Step 1 scope (changed/staged files in the working tree) is correct for a normal commit, but is **insufficient** before any history-rewriting or snapshot-publishing operation — a squashed-snapshot force-push, `git filter-repo`, or branch recreation publishes or exposes *every* file and *all* history, not just what you touched this session. A changed-file-only scan gives a false all-clear in that scenario. See `memory/feedback_pii_sweep_must_cover_siblings_and_history.md`.

Before any such operation, sweep three axes (not just the file you edited):

1. **All tracked files, not just changed ones:** `git grep -in <name>` across the whole working tree for each denylist token and any newly-known real entity.
2. **Git history, not just the working tree:** `git grep -in <name> $(git rev-list --all)` (inline `$(...)`, not a pre-expanded shell variable — that has silently returned empty before) and `git grep <name> origin/<branch>` per remote branch.
3. **Contextual variants, not just exact tokens:** quoted strings, path-embedded fragments (e.g. `therapy-<name>-transcript.md`), case variants. For short single-word company/person tokens that could also appear as a substring of an unrelated common word, use word-boundary matching (`grep -wE "\b<token>\b"`) rather than plain substring — plain substring produces false positives that both cause false alarms and can corrupt unrelated content if fed into a `--replace-text` scrub.

Surface every hit and triage by hand for a small set. Do not report "clean" from a changed-files-only scan when the operation touches the full history/tree.

### Step 1 — Refresh the denylist and run the deterministic scan

```bash
PYTHONIOENCODING=utf-8 python3 tools/gen_pii_denylist.py --repo-root .
```

Then collect the changed **public, non-gitignored** files:

```bash
git status --porcelain
```

For each changed/untracked path, keep it if:
- `git check-ignore -q <path>` returns non-zero (NOT ignored).

**That single condition IS the definition of a public artifact.** Anything git does not
ignore reaches the public remote on the next `git add -A`. `tests/`, `.claude/skills/`,
`.claude/workflows/`, `framework/`, `docs/`, `examples/`, `plugins/`, `tools/*.{py,md,sh}`
and top-level `*.md` are the common cases, and `check_public_pii.py` keeps them as a fast
path — but **do not use that list as the test.** It has under-covered twice: 2026-08-13
(`.claude/workflows/*.js`, tracked and public, never once scanned by the always-on hook)
and 2026-08-18 (`.claude/settings.json`, tracked, plus a stray `.claude/settings.json.bak`
that was untracked, NOT gitignored, and one `git add -A` from shipping). Both times the fix
had been to append another prefix, which treats the symptom.

Skip everything else (private `data/**`, gitignored caches, `output/**`, the denylist).
If the public-file set is empty, report "No public files changed — nothing to audit" and stop.

Sweep them in ONE command with `--scan`, which runs the hook's own word-boundary
matcher over a path list and applies the same public/gitignored/binary filters:

```bash
git status --porcelain | awk '{print $2}' \
  | PYTHONIOENCODING=utf-8 python3 tools/check_public_pii.py --scan --stdin-paths
```

Or pass paths directly: `... check_public_pii.py --scan path/a.md path/b.py`.
Exit 2 = denylist hits (in `hits[]`); exit 1 = it scanned **zero** files, which is a
failure, not a pass; exit 0 = clean.

**Exit 3 = an ambiguous-tier match has no verdict, and the audit is not done.** Each
entry of `ambiguous_unresolved[]` is `FILE:TOKEN`: a pipeline company name that is also
an ordinary word, found in that file. `ambiguous_hits[].lines` gives the line numbers.
Open each one and decide:

- it refers to the real company: replace it with a placeholder and rerun;
- it is the ordinary word: rerun with `--accept-ambiguous FILE:TOKEN`, once per entry.

There is no way to accept a token for every file, because the same word is a placeholder
in one file and the real company in another. A verdict lasts for one run and is never
stored. Report the entries you accepted in the audit summary. An accept that matched
nothing comes back in `ambiguous_accept_unused[]`; treat it as a typo to fix.

**Never hand-roll this sweep with `grep`.** Hand-rolled greps default to substring
matching, and a short brand token then fires inside unrelated common words — a 2026-08-12
pre-push sweep produced ~190 such false hits before being redone. Worse, a substring
sweep feeding a `git filter-repo --replace-text` scrub corrupts unrelated content. If you
genuinely must grep, use word boundaries: `grep -E '\b(tok1|tok2)\b'`. See
[[feedback_replace_all_substring_check]].

Collect the `hits[]` entries into the findings list.

### Step 2 — Dispatch a FRESH subagent for the semantic pass

Spawn one subagent (Task tool, `general-purpose`) over the candidate files. Give it
ONLY the file list, the file contents, and the KEEP/SCRUB boundary above — do **not**
give it the denylist (you want an independent judgment pass that catches what the
denylist missed, per the anti-anchoring rule in CLAUDE.md / Multi-Agent Design).

Subagent instructions:
> You are a PII reviewer for a PUBLIC code repository. Below are changed files. Find
> every piece of real personal/company identifying information that should not be in a
> public repo: real person names, pipeline/target company names, email addresses, phone
> numbers, physical addresses, side-venture names. Apply this boundary: KEEP real
> employers/schools/public-author names/generic products [list]; SCRUB everything else.
> **A real name/company used as an EXAMPLE, test fixture, code comment, or "Origin:"
> provenance note is STILL a leak — "it's just an example" is NOT a reason to mark it
> clean.** Flag it exactly as you would a live reference.
> For each finding return: file, line, exact text, type, KEEP/SCRUB/AMBIGUOUS, and a
> suggested generic placeholder that preserves the example's intent. Return structured
> findings only. If a file is clean, say so. Do not edit anything.

**Why the anti-rationalization line is mandatory:** subagents systematically rationalize a real name in an example/test/Origin-note as "benign illustrative data" and report false-clean — fired 3x in one session (2026-06-15) before this line existed. See `memory/feedback_pii_subagents_rationalize_examples.md`.

### Step 3 — Verify, merge, present, and gate

**Bound by `framework/review-findings-protocol.md`.** This skill already distrusts the subagent's
*clean* verdicts (see the cross-check below). The same distrust applies to its *positive* findings,
and that half was missing until 2026-08-14.

**3a — Verify each SCRUB/AMBIGUOUS finding before it gates anything.** For each one:

1. **Open the file at the cited line and quote it.** The subagent's paraphrase is not the line.
2. **Establish the token is a real entity, not a house placeholder.** This repo uses a fictional
   cast (`Jordan Lee <jordan@example.com>`, Acme AI, Northwind, `company.com`) across many public
   skill files. Grep the token repo-wide before believing it: a name appearing in nine skills beside
   `example.com` addresses is the placeholder persona, not a leak. **Cross-check first names against
   the FULL denylist entry** — a first-name collision with a real contact is not a leak.
3. **Establish exposure state, because it sets the remediation, not just the urgency.** Run
   `git grep -n "<token>" origin/main` and `git log -S "<token>"`. *Already on the public remote* and
   *staged for the next commit* are different problems: the first is a history question, the second a
   working-tree scrub. Do not report the second as the first, or the reverse.
4. **Check whether the finding's evidence is itself public.** A date or oblique reference that
   resolves to a company only via a gitignored tree (`coaching/`, `data/`, `output/`) is not
   walkable by a public reader. Verify with `git check-ignore -v <path>` and
   `git ls-tree -r origin/main --name-only`.

**Assign your own SCRUB/AMBIGUOUS/CLEAR verdict.** The subagent's is an input. It has been wrong in
both directions: false-clean on real names in examples (2026-06-15, 3x) and false-positive on a
placeholder that collided with a real first name (2026-08-14).

**3b — Merge and present.** Merge deterministic hits (Step 1) with your *verified* SCRUB + AMBIGUOUS
findings. De-duplicate by (file, text). Present grouped by file:

```
## PII Audit — N file(s) scanned

### <path>
- ⛔ SCRUB  L<line>  "<text>"  (<type>) → suggest: "<placeholder>"
- ⚠️ AMBIGUOUS  L<line>  "<text>" → your call (likely KEEP because ...)

[If clean:] ✅ <path> — clean
```

**No ledger table here, deliberately** — this gate runs before every public commit, and a
mandatory table on a high-frequency path is the kind of ceremony that gets skipped, which
costs more than it buys. `framework/review-findings-protocol.md` requires a ledger of
ledger-*bearing* surfaces; this one carries the obligation in the cheaper form below.

**What is still mandatory: show the disagreements and the refusals inline.** For any finding
where your verdict differs from the subagent's, add one line under that file:

```
- ↩︎ REFUTED  "<text>"  — subagent said SCRUB; <the evidence that refuted it>
```

That single line preserves the only thing the table existed to expose. **A run where you
refuted nothing and every verdict matched the subagent's is a relay, not a review** — say so
plainly in that case rather than reporting a clean pass, because a semantic agent that is
right six times out of six has not been observed yet (2026-08-14: two of six were wrong).

- **Any *verified* SCRUB finding in a file this commit touches = do not commit yet.** Offer to
  apply the generic-placeholder fixes (re-read + Write/Edit each file), then re-run to confirm green.
- **A SCRUB finding already on the public remote is NOT a commit gate** when the pending commit
  does not touch those lines — pushing adds no new exposure. Report it as a separate standing item
  with its remediation options (scrub-forward, which leaves history; or scrub plus history rewrite,
  which is what the July delete-and-recreate cost). Blocking a clean commit on a two-month-old
  public string is the overstated-severity failure, and it trains the gate to be ignored.
- **AMBIGUOUS findings** are surfaced for Nick's decision, never auto-edited.
- **Known and accepted.** A small set of example-URL hostnames in `apply/SKILL.md` and
  `generate-cv/SKILL.md` were reviewed on 2026-08-14 and accepted by Nick as-is. Do not re-gate a
  commit on them; surface a one-line note instead. **The list itself lives in the gitignored
  `memory/reference_accepted_public_pii_exceptions.md`** — enumerating them here, in a public file,
  with the reasoning for why each was a real entity, would disclose more than the strings already do.
  A bare hostname in an examples block reads as a placeholder; a note confirming it was a genuine
  target does not.
- **The structural gap behind that entry is worth knowing.** `gen_pii_denylist.py` harvests from
  `networking.md`, `job-pipeline.md` and `scan-targets.yaml`, so an entity that was researched and
  archived without ever entering any of those is invisible to the deterministic layer **by
  construction** — `output/archive/` holds several. The semantic pass is load-bearing there, not a
  backstop, and a green Step 1 alone does not cover it.
- **Two more gaps were found and CLOSED on 2026-09-01, both by a live leak rather than by reasoning.**
  (a) *Components.* A multi-token company was emitted only as the whole phrase plus its slug, and
  `find_pii` matches a phrase literally — so a public file naming ONE word of a two-word company was not
  a hit. 171 of 470 entries were multi-token. Distinctive components now reach BLOCK, ordinary-English
  ones the WARN tier, and a person contributes a surname but never a bare first name (the fictional cast
  would otherwise turn every placeholder into a block). (b) *Retired targets.* The list was rebuilt from
  CURRENT `data/` each run, so a company that left `scan-targets.yaml` lost its coverage while its name
  stayed in files written while it WAS a target — exactly how a retargeted-away company sat on the public
  remote on neither tier. Tokens now accumulate in a gitignored `tools/.pii-denylist-retired.txt`, merged
  into every rebuild and hand-prunable. See [[feedback_coverage_must_outlive_the_source_it_was_derived_from]].
- **What is still NOT covered, and is the next thing to build.** A single-token company whose name is an
  ordinary English word still routes to WARN, which on the write path reaches nobody. That rule
  ([[feedback_pii_denylist_drops_common_word_company_names]]) tripped its 2nd-fire gate on 2026-09-01 and
  its fix — an allowlist of actual target names that bypasses the dictionary filter — is **owed, not
  built**. Do not read the two closures above as covering it.
- **Calibration for how much the deterministic layer is worth on the semantic class.** On 2026-09-01 it
  scanned all 523 tracked files and returned **zero BLOCK hits**, in the same minute that a semantic pass
  found **nine real leaks** in six public skill files — a date-plus-outcome fingerprint, a verbatim
  sentence from a sent email, an industry vertical, and a real company published with its rank in the
  target list. None contained a denylisted token. **Never report a green Step 1 as "the public tree is
  clean."**
- **Pipeline membership does NOT imply BLOCK-tier coverage — the second gap, found 2026-08-14.**
  `gen_pii_denylist.py` routes single-token company names that are also ordinary English words to
  `tools/.pii-denylist-ambiguous.txt` (WARN) instead of the BLOCK denylist, so matching them will not
  false-positive on ordinary prose. That reasoning is sound, but **a PreToolUse WARN is exit 0 +
  stderr, which Claude Code does not surface** (`tools/HOOK_AUTHORING.md` L77). So for this class of
  company the always-on hook detects the token, prints a correct warning, and **nobody reads it**.
  A live pipeline company reached two public files that way; it was caught by hand at staging, not
  by the hook.

  Two consequences for this skill: (1) never conclude "not on the denylist" from grepping the BLOCK
  list alone — check the ambiguous list too, and prefer *running* the hook over inspecting either;
  (2) **`ambiguous_hits[]` from Step 1 is the only place this tier becomes visible.** Treat a
  non-empty `ambiguous_hits[]` as requiring an explicit verdict per entry, not as advisory noise —
  this skill is the reader that the write-path warning never had.
- **Treat a subagent "clean" verdict as a hypothesis, not a conclusion.** Cross-check
  its clean calls against the deterministic denylist scan (Step 1) and a direct grep
  for known real entities (recent `data/networking.md` / `data/job-pipeline.md` names,
  Origin-note dates that name a real person/company). Do not accept "clean" purely on
  the subagent's say-so — the failure mode this guards against is a confidently-wrong
  all-clear, which is worse than no check at all. See
  `memory/feedback_pii_subagents_rationalize_examples.md`.
- **All clean** → report `✅ PII audit clean — safe to commit.` and stop.

### Step 4 — On fix-and-recommit

If Nick approves fixes, apply them, re-run Steps 1–3 once, and confirm a fully green
pass before handing back to the commit flow. The deterministic hook will also fire on
each Write/Edit as a backstop.

## Notes

- This skill READS and proposes; it does not commit or push.
- The denylist is regenerated each run so newly-added contacts/pipeline rows are covered
  by the deterministic layer immediately.
- Origin: 2026-06-11, hook+subagent promotion of `feedback_generalize_examples_in_public_artifacts`.
  Pairs with `tools/check_public_pii.py` (the always-on reflex) and
  `tools/gen_pii_denylist.py` (the token source).
