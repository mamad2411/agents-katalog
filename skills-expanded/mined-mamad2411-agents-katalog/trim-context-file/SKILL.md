---
name: trim-context-file
description: Shrink an always-loaded context file (CLAUDE.md, MEMORY.md, a large SKILL.md) by moving reference-shaped sections out to on-demand docs and leaving a router pointer behind. Measures first, proposes KEEP/MOVE per section, never deletes, never acts without approval.
argument-hint: <path> (defaults to CLAUDE.md)
user-invocable: true  # RE-ENABLED 2026-08-11 after the capabilities landed and were mutation-verified. See Step 0.
allowed-tools: Bash(bash tools/trim_context_gate.sh:*), Bash(PYTHONIOENCODING=utf-8 python3 tools/context_file_audit.py:*), Bash(grep:*), Bash(wc:*), Bash(ls:*), Read(*), Write(*), Edit(*)
---

# Trim Context File

## Step 0 — CAPABILITY + BASELINE GATE (mandatory, never skipped)

**Run this before touching the target file. If it aborts, stop — do not edit anything.**

```bash
bash tools/trim_context_gate.sh <target> [approved_block_count]
```

It exits 0 only when all of the following hold, each exercised against the real target:
`--rules` returns a non-empty baseline (`rule_count > 0`), `--emit-blocks` emits blocks
whose concatenation reproduces the source **byte for byte**, every manifest sha256
re-derives against the *source* bytes, byte accounting balances, and — when you pass an
approved count — the emitted block count matches it exactly. It prints the baseline and
block paths to hand to Step 5.

**Byte conservation is the load-bearing guarantee. The rules diff is corroborating
only — never invert that.** `--rules` is a keyword+structural *sample*, not a cover
(roughly a third of `CLAUDE.md` — 82 of 249 non-blank lines on 2026-08-12; re-measure
rather than trusting that number, it drifts as the file changes), and before/after are
parsed by the **same** detector, so a systematic omission cancels on both sides and the
diff comes back empty. A green rules diff is not proof; matching bytes are.

**If the gate aborts, the exit code says where.** `context_file_audit.py` uses:
`1` not a file · `2` usage error · `3` a required capability is unadvertised ·
`4` zero normative lines (refuses an empty baseline) · `5` zero blocks ·
`6` the `--emit-blocks` directory is unsafe to write (unprovable, holds undeclared
entries, or is unwritable) · `7` emitted block count ≠ `--expect-blocks`.
Codes 4-7 mean the guard did its job — fix the input, never loosen the check.

### Why this gate exists, and the two traps in it

Adversarial review on 2026-08-10, before first use, found the verification steps below
invoked script flags **that did not exist**. `--rules --json > rules_before.json` wrote a
**zero-byte file**; the Step 5 check then iterated an empty before-set, found zero missing
lines, and reported **PASS**. Identically, `--emit-blocks` errored out leaving no blocks,
so the per-block `diff` loop iterated zero blocks and also passed. Both failed open,
silently, while destinations existed and pointers resolved — so the run looked clean.

**A guard with no failing mode is the same bug wearing a safety vest.**

Two traps survive that fix, and the gate script is written around both:

1. **Never check that a redirect target exists or is non-empty.** `cmd > f` truncates `f`
   *before* `cmd` runs, so `[ -f f ]` passes on a failed run and `[ -s f ]` passes on any
   partial write. That is the original bug in a new costume. Gate on the **process exit
   status** and on **parsed content**; capture stdout into a variable (`$(...)` propagates
   the child's status) and write the baseline file only once it is known good.
2. **`--require` verifies a declaration, not behavior.** Delete the `--rules`
   implementation and leave its name in the capability list, and `--require` still exits 0.
   The gate therefore *exercises* `--rules` and `--emit-blocks` on the real target rather
   than trusting the advertised list.

Re-enabled 2026-08-11 after the capabilities landed and were **mutation-verified**: the
supporting suite (184 tests) was checked by deliberately breaking the script one fault at
a time and confirming the suite fails — including narrowing the rule detector, dropping
fence tracking, and keying directory cleanup on filename shape instead of manifest
provenance. A suite that only passes is not evidence.

Some files are loaded into **every session**: `CLAUDE.md`, `memory/MEMORY.md`, and any
SKILL.md the model reads on each invocation. Their size is a per-session tax paid
forever. This skill reduces that tax **without losing the content** by moving
reference-shaped material to on-demand files and leaving an explicit pointer behind.

**The precedent this generalizes:** the 2026-07-08 MEMORY.md restructure, which turned
a bloated always-loaded index into a Critical Context block plus a topic-shard router
(7 shards then, 11 after the 2026-08-13 split). That worked because the router table is
explicit about what lives where. This skill applies the same pattern to any context file.

**And the follow-on lesson, from the 2026-08-13 split:** sharding buys headroom, it does not
stop growth. Two of those seven shards were 1.5-1.7x over budget within five weeks. Re-split
on the same axis the content actually clusters on; do not let a shard creep past the read
budget a second time on the theory that it was recently reorganized.

## The governing distinction

| Tier | Content | Where it belongs |
|---|---|---|
| **Always-loaded** | Rules that must never depend on recall. Prohibitions, hard invariants, tier ladders, "before doing X, do Y." | Stays resident |
| **On-demand** | Material consulted *while doing a specific task*: tool tables, file-format conventions, schema references, worked examples. | Moves out, pointer stays |

The test for a section: **"If Claude never read this section, what breaks?"** If the
answer is "it would violate a rule without knowing," it stays. If the answer is "it
would look up the wrong column name when editing that specific file," it moves.

## Anti-goal

This is **not** the additive-by-default rule being violated. That rule governs *data*
(the user's writings, logs, reflections). This skill governs *infrastructure*, which
CLAUDE.md explicitly carves out for bounded periodic pruning with each decision
surfaced for approval. **Nothing is ever deleted — only relocated.**

## Steps

### Step 1 — Measure (deterministic, never skipped)

```bash
PYTHONIOENCODING=utf-8 python3 tools/context_file_audit.py <path>
```

Reports per section: bytes, share of total, `rule_density`, `lookup_density`, and an
advisory KEEP/MOVE/REVIEW.

**Bytes, not lines, are the unit.** A 13-line section of enormous paragraphs can outweigh
a 91-line table. Never propose trims from line counts alone.

The script's suggestion is **advisory input, not a verdict.** Read the actual section
before agreeing with it. A high `lookup_density` section can still be load-bearing if
its table encodes a rule (e.g. a "these files are write-only, use these scripts" table).

**If it warns about an unclosed code fence, stop and fix the file first.** Per CommonMark
an unclosed ``` runs to EOF, so every `## ` heading after it is treated as code and
vanishes from the audit. Byte accounting still balances — nothing is lost — but you will
see one giant section and a file with no structure, and any trim proposed from that view
is meaningless. Close the fence, then re-run Step 0 and Step 1.

### Step 2 — Propose per-section, with the destination named

Present every section above ~3% share as a row:

```
### <Section> — <bytes> (<share>%)
Signals: rule <n> · reference <n> · script says <SUGGESTION>
Proposal: KEEP | MOVE -> <destination path>
Because: <what breaks if Claude never reads this>
Pointer that would remain: "<the exact one-line router entry>"
```

Group into KEEP / MOVE / REVIEW. **Wait for explicit approval per group.** Do not
proceed on silence, and do not batch-apply a group the user only partly approved.

### Step 3 — Move, and leave a real pointer

For each approved MOVE:

1. Create the destination file with a header naming its origin and the date.
2. Move the section **verbatim**. Do not summarize, reword, or "improve" while moving —
   that silently changes rules under cover of a formatting task.
3. Replace the section in the source with a **router entry** that says what lives there
   and *when to read it*. A pointer with no trigger condition is a pointer nobody follows:

   > **Tools & scripts reference** → `docs/tools-reference.md`. Read before invoking any
   > `tools/*.py` script or when you need argument order and flag placement.

4. If the file already has a router table (as MEMORY.md does), add the row there instead
   of scattering pointers through the body.

### Step 4 — Back-propagate references (mandatory)

Moving a section breaks every artifact that cited it by heading or line.

```bash
grep -rn "<distinctive phrase from the moved section>" .claude/skills/ docs/ framework/ tools/ *.md
```

Repoint every hit at the new location in the same pass. A dangling citation is a recall
dead-end, the same failure the memory-archive rule guards against.

### Step 5 — Verify

1. Re-run Step 1 and report before/after: total bytes, and the reduction.
2. Confirm every new pointer's destination file exists and is non-empty.
3. **Rule conservation — compare against the UNION, not the source.** Re-run `--rules`
   over the trimmed source **and every destination file**, and check the Step 0 baseline
   against that combined set. Any normative line present before and absent from the union
   is a **hard abort**: it means a rule was dropped rather than relocated.

   **This must be the union, and getting it wrong is the likeliest route back to
   fail-open.** Checked against the trimmed source alone, the abort fires on every
   *successful* move — the top MOVE candidates by byte share all contain normative lines,
   so relocating them is exactly the intended outcome. An operator who hits a spurious
   abort will loosen the check until it passes, hand-restoring the bug this gate exists
   to prevent. A rule leaving the source is expected; a rule leaving the *union* is data
   loss.

   Before trusting a green result, confirm the baseline was non-empty (Step 0 guarantees
   `rule_count > 0` — do not re-derive it here with the same parser and call that
   independent confirmation).
4. **Byte conservation — the load-bearing check.** The trimmed source plus every
   destination file must account for all original bytes, allowing only for the pointer
   lines you added. Diff each moved section against its Step 0 block: content must be
   **byte-identical**. This, not the rules diff, is what proves nothing was silently
   reworded during the move.
5. If the file is `CLAUDE.md` or a SKILL.md, run the repo's test suite — hooks and tests
   assert against some of these conventions.
6. Because `CLAUDE.md`, `framework/`, `docs/`, and `.claude/skills/` are public artifacts,
   run `/audit-pii` before committing whatever this produces.

### Step 6 — Record

Add a CHANGELOG entry naming what moved and where. A future session that cannot find a
rule needs to be able to trace it.

## Failure modes this skill is built against

- **Trimming by line count.** Understates paragraph-heavy rule sections and overstates tables.
- **Summarizing while moving.** The single most dangerous failure: a rule quietly weakens
  during what was billed as a formatting change. Move verbatim, always.
- **Pointers without triggers.** "See `docs/x.md`" gets ignored. "Read before doing X" gets followed.
- **Forgetting back-propagation.** The rule survives; every citation of it dies.
- **Trimming the wrong tier.** Hard rules are the one thing that must never be paged out,
  no matter how many bytes they cost. High byte-share is not by itself a reason to move.
- **Acting on the script's suggestion without reading the section.** The heuristics are
  regex over line shapes. They cannot tell a load-bearing table from a lookup table.

## Notes

- Read-and-propose by default. It never edits without per-group approval.
- Works on any markdown file with `## ` sections; it is not CLAUDE.md-specific. Section
  splitting is fence-aware, so a `## ` line inside a code fence is content, not a heading.
- Companion script: `tools/context_file_audit.py`. **It never touches the target file** —
  but it is no longer read-only overall: `--emit-blocks <DIR>` writes block files and a
  manifest into DIR, and on a re-run deletes the block files that DIR's existing
  `manifest.json` declares. It refuses (exit 6) rather than touching a directory it cannot
  prove it wrote, so point `--emit-blocks` at a fresh or dedicated directory, never at a
  folder holding anything you care about. An earlier revision keyed that cleanup on
  filename shape and destroyed a folder of numbered user notes; see
  `memory/feedback_shape_is_not_provenance_for_destructive_ops.md`.
- Companion gate: `tools/trim_context_gate.sh` (Step 0).
