---
name: skill-promotion-pipeline
description: "Turn a large pile of collected third-party or candidate agent skills into a small, curated, licence-clean registry, one reviewed batch at a time: capture sources immutably with provenance, cluster duplicates, rate from the bodies, agree each batch's shape with the human, fan out writers on disjoint files, gate with an independent default-REJECT verifier and fix waves, record every verdict in an append-only decision ledger, rebuild the index, and prove no citation dangles. Ships a stdlib Python gate script with seeded-failure tests. Use when asked to curate, promote, dedupe, consolidate or import skills from skill packs, marketplaces or scraped collections: 'promote these skills', 'which of these skills are worth keeping', 'merge duplicate skills', 'clean up our skills folder', 'import this skill pack', 'build a skills registry', 'is this skill safe to ship licence-wise'."
---

# Skill Promotion Pipeline

A procedure for turning hundreds or thousands of collected skills (skill packs, marketplace
downloads, scraped repos, your own drafts) into a registry of a few dozen skills you would stake
your name on. It runs in **batches**. Each batch ends with a verifier's ACCEPT, one row per
decision in an append-only ledger, and gates that prove every claim of provenance still resolves.

Three beliefs drive every step:

1. **One skill per capability, not one folder per upstream skill.** Most good candidates are
   *merges* into something you already have. Twenty-seven upstream skills about one cloud
   platform should become two skills plus two folds, not twenty-seven folders.
2. **Nothing ships without a clear licence and an independent verifier.** The writer never
   verifies its own work. The verifier starts from REJECT.
3. **A gate that can pass while checking nothing is not a gate.** Read the count, not just the
   exit code. "Checked 0" is a failure.

## When to use / not

Use it when you have many more candidate skills than you want, from mixed sources and licences,
and you need a defensible record of what was kept, merged or skipped, and why.

Do not use it for writing one new skill from scratch (use your normal skill-authoring flow), or
for a registry of fewer than ~10 candidates. There the ledger and gates cost more than they save.
Still apply the licence rule and the independent review.

## What it creates in your repo

All paths are relative to the **registry root** (the folder that holds your curated skills). The
bundled script creates what it needs. Full schemas: `references/layout-and-schemas.md`.

| Path | What it is | Who writes it |
|---|---|---|
| `archive/objects/<id>/` | Immutable copy of each captured skill tree (`id` = content hash) | `pipeline.py capture` only |
| `archive/manifest.jsonl` | One row per captured tree: origin, licence (detected), size, stub flag | `capture` |
| `archive/clusters.json` | Normalised name -> object ids | `clusters` |
| `archive/ratings.jsonl` | One rating per cluster (quality, suggested verdict, merge target) | rater agents, validated |
| `archive/cache/` | Derived shingle cache for `overlap`, keyed by object id. Safe to delete | `overlap` |
| `<category>/<skill>/SKILL.md` | A curated skill | writer agents |
| `<category>/<skill>/skill.yaml` | Sidecar: `version`, `sources:` (archive files drawn from), `provenance:` (clusters folded in) | orchestrator (new skills), writers (merges) |
| `decisions.jsonl` | **Append-only decision ledger**: one row per cluster per batch | `ledger-append` only |
| `registry-index.json` | Generated index of curated skills | `index` only |
| `work/batch-NNN/` | The batch's shape, briefs, writer outputs, verifier reports | orchestrator |

Keep `archive/` out of anything you publish if its contents are not yours to redistribute.

## The gate script

`scripts/pipeline.py` (Python 3 stdlib; uses PyYAML for strict parsing if installed). Run
`python scripts/test_pipeline.py` once in a new repo: 26 tests prove each gate passes on good
input and fails on seeded bad input.

```
python scripts/pipeline.py --root <registry> capture <src> --origin <url-or-label>
python scripts/pipeline.py --root <registry> clusters
python scripts/pipeline.py --root <registry> status [--list open]
python scripts/pipeline.py --root <registry> ledger-append work/batch-001/decisions.json --batch 001
python scripts/pipeline.py --root <registry> provenance [--deep]
python scripts/pipeline.py --root <registry> index
python scripts/pipeline.py --root <registry> overlap <category>/<skill>
```

Adjust the script path to wherever this skill is installed. Relative `FILE` and `SKILL_DIR`
arguments are tried against the current directory first, then against `--root`, so the
commands above work from any directory.

## Roles

| Role | Does | Never does |
|---|---|---|
| **Human** | Agrees each batch's shape; rules on licence questions and anything outward-facing (publish, push, delete) | - |
| **Orchestrator** (you) | Runs the script, picks the batch, writes briefs, owns shared files (ledger, index, new skills' `skill.yaml`) | Writes skill content it will later judge |
| **Raters** | Rate clusters from the bodies into `ratings.jsonl` | Write anywhere but their one output file |
| **Writers** | Write their assigned files only; triage their clusters inside the agreed shape | Touch shared files or another writer's files |
| **Verifier** | Independent, default-REJECT review of the whole batch | Fix anything |
| **Fixers** | Fix listed defects on disjoint files, with evidence per item | Accept the verifier's claims unchecked |

**Parallel agents are optional.** If your agent runtime can spawn subagents, run raters, writers
and fixers in parallel waves of at most ~10 (above that, rate limits kill runs mid-shard). If a
wave dies on a session or rate limit, **resume** each agent (its research is in its context)
instead of respawning. Without subagents, run the roles sequentially. The verifier must still
be a **fresh context** (a new session) that did not write the batch. That one is not optional.

## The pipeline

### Stage 1: Capture (once per source)

`capture <src> --origin <url>` copies every folder containing a `SKILL.md` (or `--marker` for
packs that use another filename) into `archive/objects/<id>/`, and appends a manifest row. It is
idempotent: re-capturing the same tree adds nothing.

- The licence is detected **by the script**, walking UP from each tree to the nearest licence
  file (stopping at the repo root). A bundled third-party tree with its own licence therefore wins
  over the pack's root licence. A permissive file that also names a restrictive or
  source-available licence (Elastic, SSPL, Commons Clause, PolyForm, GPL...) is labelled
  `mixed:...` and is never clear. Never let an agent assert a licence.
- Trees over `--max-bytes` (default 5 MB) are recorded but not stored. They cannot be cited.
- **The archive is immutable.** Never edit an object. `provenance --deep` re-hashes every object
  and fails on any change.
- Record the origin as a URL where one exists. It is the only provenance a public reader can follow.

### Stage 2: Cluster

`clusters` groups objects by normalised name (`DB_Migrations` and `db-migrations` together).
Name clusters are a starting point, not a verdict. One name can hold unrelated skills (a
"review" cluster may contain a code-review skill, a memory audit and a CLI sub-command). Triage
splits them and records the split in the ledger `note`.

### Stage 3: Rate (optional for small archives; essential for large ones)

Raters read each cluster's **bodies** (up to 3 objects, largest first) and output one JSON line
per cluster: quality 1-5, verdict `promote | merge | skip`, `merge_target`, a one-sentence
summary of what the body *actually* contains, `stale`. Rubric, brief template and shard
validation: `references/rating.md`.

- **Pilot one shard first**, read it, tighten the brief, then fan out. The first shard shows
  where raters misread the bar (e.g. skipping good niche skills because no category fits).
- Validate every shard before merging it: each input cluster exactly once, schema valid,
  every `merge_target` exists. Fix defects by hand, never by re-rating blind.

### Stage 4: Measure, then pick the batch

`status` gives per-cluster coverage with **explicit precedence**: a ledger verdict beats an
archived member cited in some curated skill's `sources:`, which beats open.

- **Measure coverage by provenance, never by folder names.** Promotion renames and merges, so
  "1,800 candidates vs 220 curated skills" can overstate the real backlog threefold.
- Filter the open pool to: licence-clear, archive-backed (stored), quality >= 4, not a stub
  (`marker_bytes` under ~200 is usually a path stub or pointer).
- Batch **by theme** (one platform, one domain), not by score. A themed batch lets writers see
  every overlapping source at once. Aim for 20-60 clusters.
- **Exclude regardless of rating** anything whose purpose is removing model safety behaviour,
  jailbreaks, credential harvesting or similar. Log them as `skip` with the reason.

### Stage 5: Agree the SHAPE with the human (gate)

Before any writer runs, propose the batch's shape in a few lines and get an explicit yes:

```
Batch 004 (theme: <platform>), 27 open clusters, all MIT:
  NEW  dev/<platform>-platform       base SKILL.md + 20 references/<product>.md
  NEW  agents/<platform>-agents      agent SDK + MCP server + OAuth
  FOLD ci-cd -> dev/ci-cd-pipelines; testing -> dev/test-quality
  SKIP 10 generic q2-3 clusters (listed)
Alternatives considered: 27 folders (rejected: one skill per capability), 3 skills.
```

Offer the alternatives you rejected. The human picks. Write the approved shape to
`work/batch-NNN/shape.md` and do not re-litigate it inside the batch. A fixed shape also lets
writers own disjoint files, which removes a separate triage wave.

### Stage 6: Write (disjoint files)

Give each writer an exact file list (no two writers share a file) and the brief in
`references/writer-brief.md`. Its core rules:

- **Fold, don't paste.** Rewrite in the target's voice and structure. Keep the upstream's real
  value: error text -> cause -> fix catalogs, limits tables, non-obvious gotchas, minimal correct
  code. Cut marketing, "when to use" boilerplate, template dumps and changelog noise.
- **Assume every upstream is stale.** Read all copies in the cluster and keep the most current.
- **Verify against the real API, not memory.** For every code block in a typed ecosystem, give
  writers the real published types up front and require a strict type-check before they report.
  `npm view` (and similar) checks *version numbers*, not *APIs*: a batch can bump every pin and
  still ship removed exports, changed signatures and a forgeable auth check. Procedure:
  `references/code-verification.md`.
- If a fact cannot be verified, write "verify against current docs". Do not assert it.
- Licence-unclear source (none found, Elastic, BSL, proprietary, copyleft into a permissive
  registry): **copy nothing**. Writing fresh from the vendor's own docs is allowed. Say so in the note.
- Frontmatter: `name` == folder name; `description` <= 1024 chars, says what AND when, and is
  double-quoted if it contains `: ` (strict YAML rejects it unquoted).
- Merges: append the cluster to `provenance:`, the archive files actually drawn from to
  `sources:`, bump `version` minor **once per batch**.
- Shell hygiene: delete only paths you created, **by exact name**. Never `rm` with globs, never in
  shared temp directories. Remove `__pycache__` you caused.
- Each writer reports a JSON list, one row per assigned cluster:
  `{cluster, verdict, target, files, sources, note}`.

The orchestrator then assembles `skill.yaml` for NEW skills from the writers' rows (union of
`sources`, sorted `provenance`). Refuse to assemble if any cluster is reported twice or any
source path does not exist.

### Stage 7: Verify (independent, default-REJECT)

A fresh-context verifier reviews the whole batch with `references/verifier-brief.md`. It starts
at REJECT and moves to ACCEPT only if every check passes with evidence:

1. Licence: `overlap <skill>` for each touched skill. It compares every file against the skill's cited sources AND against every stored archive file whose licence is not clear, cited or not, because a writer who copies from a tree it was told not to copy from will not cite it. Low overlap with permissive sources, near zero with unclear ones. Every source's licence re-read, not trusted from the brief. A flagged match may be waived only by the verifier, from the shared phrases the gate prints, only when they are functional text (commands, identifiers, quoted errors) and never prose. The waiver is recorded in the round report and the ledger note, never done by raising the threshold (see "Waiving an overlap finding" in the verifier brief).
2. Provenance: `provenance` passes, and every listed source was actually used.
3. Correctness: spot-check claims and code against the **real** package types / official docs. Security-relevant code (auth, token checks, signature verification, access control) is checked line by line.
4. Frontmatter and index: `index` passes.
5. Scope: writers stayed inside their file lists. Nothing outside the batch changed.

Findings are classed **blocking** (wrong, insecure, licence problem) or **fix** (quality), each
with file, line, evidence and a suggested correction.

### Stage 8: Fix waves until ACCEPT

- Fixers get disjoint files and the finding list. Ask for **evidence per item**, not agreement.
  Fixers who re-check find extra bugs; ones who take the verifier's numbers on trust find none.
- **A verifier's suggested fix is a claim, not a patch.** Type-check or test it before applying.
  The last blocker in a round is often the verifier's own snippet copied verbatim.
- A fixer may dispute a finding with evidence. The orchestrator rules on evidence, not on who said it.
- Re-verify the fixed files (the verifier may be the same agent, resumed). Cap at **3 rounds**. A
  batch still REJECTed after round 3 ends `exhausted` (see terminal states): shrink the batch or
  escalate to the human.

### Stage 9: Record

In this order, stopping at the first failure. The ledger comes last, because an appended
batch cannot be taken back. A batch whose gates are red must never reach it.

1. `index`. It refuses on name/folder mismatch, missing or over-long description, bad YAML.
2. `provenance --deep`. Every citation resolves, nothing checked 0, archive unmodified.
3. `ledger-append work/batch-NNN/decisions.json --batch NNN`. It refuses a batch already
   logged, a cluster decided twice, a skip without a reason, or a target without a `SKILL.md`.
   The ledger is never edited. A later re-decision is a new row in a later batch, and it supersedes.
4. `status`. Confirm the batch's clusters moved from open to curated/skipped.

Then report (see below). Committing, publishing or pushing is the human's call.

## Terminal states (every batch ends in exactly one)

| State | Meaning |
|---|---|
| `accepted` | Verifier ACCEPT, ledger appended, index + provenance green |
| `blocked` | Waiting on a human ruling (licence, shape, publishing). Nothing half-logged |
| `exhausted` | 3 verify rounds without ACCEPT. Batch shrunk or escalated, rejected files listed |
| `clean no-op` | Open pool has nothing that clears the bar. One line saying so |

Never log a batch the verifier has not accepted.

## Hard rules (each one cost a real batch)

1. **Triage from bodies, never from index summaries.** Catalog summaries described content the
   object did not contain in ~10% of one batch.
2. **Upstream quality scores and byte counts lie.** Path stubs of 50-85 bytes and router skills
   scored top marks.
3. **Licence-clear before promoting.** An OSI-looking skill can live in an Elastic-licensed repo.
   A pack under MIT can bundle trees under other licences. No licence file means all rights reserved.
4. **Discover by the file every member has** (`SKILL.md`), never by an optional sidecar. A
   classifier keyed on `skill.yaml` silently misfiled everything that lacked one, and the counts
   still looked plausible.
5. **Make precedence explicit.** "First match wins" over a directory walk is a rule nobody chose.
6. **Read counts, not exit codes.** Two provenance gates in one real registry passed for days
   while checking zero citations.
7. **Shape first, then fan out.** Deciding the shape with the human before any agent ran made the
   writers' work disjoint and removed a whole triage wave.
8. **Type-check the code, not the version number.** See Stage 6.
9. **The builder never verifies its own work.** Separate context, default-REJECT.
10. **Agents clean up only what they created, by exact name.** One glob `rm` in a shared temp dir
    destroyed files no one could identify afterwards.
11. **Honest limits in every report.** "Type-checked" is not "run against the live service".
    Say which one happened.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| One new folder per upstream skill | One skill per capability; most candidates are merges or skips |
| Rating by name or catalog summary | Read the body; record what it actually contains |
| Agent-asserted licence | Script-detected licence from the nearest licence file |
| Bumping version pins and calling it current | Real types + strict type-check; official docs for limits and status |
| Writer self-review, or verifier who "mostly agrees" | Fresh context, default-REJECT, evidence per finding |
| Applying the verifier's snippet unchecked | Type-check / test every correction, whoever wrote it |
| Editing the ledger to fix a past verdict | Append a new row in a later batch |
| Editing an archived object to "clean it up" | Never. Clean in the curated skill; the archive is evidence |
| Unbounded fix loops | 3 rounds, then `exhausted` and a smaller batch |

## Report (end of every batch)

Lead with what changed and what needs a decision:

```
Batch NNN (<theme>): <terminal state>
Decisions: N new / N merge / N skip  ->  skills touched: <list with versions>
Verifier: R1 REJECT (x blocking, y fix) -> R2 ... -> ACCEPT
Gates: index <n> skills; provenance <n> citations / 0 dangling; overlap max <x>%
Needs a human: <licence questions, held material, publish decision>
Honest limits: <what was type-checked vs run live; what was not verified>
```

## References

- `references/layout-and-schemas.md`: every file's schema, the script's behaviour per subcommand
- `references/rating.md`: quality/verdict rubric, rater brief template, shard validation
- `references/writer-brief.md`: copy-and-fill brief for writer agents
- `references/verifier-brief.md`: default-REJECT verifier brief and fixer brief
- `references/code-verification.md`: giving writers real typings; strict type-checking code blocks per ecosystem
