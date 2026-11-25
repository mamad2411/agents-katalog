---
name: extract
description: Turn a repeatable workflow observed this session into a PROPOSED reusable skill — draft it, evaluate it against the rubric, and stage it for your approval. Never writes into skills/. Opt-in; not wired into the default pipeline. Use when a Stop candidate appears or a workflow felt worth keeping.
---

# /extract — propose a skill, evaluate it, stage it

Goal: capture a repeatable workflow as a *candidate* skill a human can review and promote.
This closes the loop the Stop detector opens — it never auto-creates a skill (the v0.1
staging rule). The output is a **proposal**, not a live skill.

> **Opt-in.** No default-pipeline skill or hook invokes `/extract`. Running it is always
> explicit and changes no baseline behavior. (v0.3 AC-E4; preserves the staging rule.)

## When to run
- A Stop candidate landed in `.claude/skills-staging/candidates.md` (the detector found a
  tool/skill subsequence that recurred this session), or
- you just did something repeatable/non-obvious worth keeping.

## Do this
1. **Read the evidence.** Open `.claude/skills-staging/candidates.md` for the detected
   sequence + recurrence count. Cross-check what actually fired in
   `.claude/traces/<date>.jsonl` (skills, subagents, MCPs). Skim the relevant transcript
   span to recover the *purpose* — the sequence names the steps, not why.
2. **Draft the skill.** Write a candidate `SKILL.md` with valid frontmatter (`name`,
   `description`) and numbered steps that capture the workflow. Pick a `name` that does
   **not** collide with an existing `skills/*/SKILL.md`.
   - Write it ONLY to `.claude/skills-staging/<slug>/SKILL.md`. **Never** create or edit
     anything under `skills/` (or any live skill dir).
3. **Evaluate it (deterministic gate):**
   ```
   node scripts/eval/extract-rubric.js .claude/skills-staging/<slug>/SKILL.md
   ```
   It scores five criteria and exits **0** (all PASS, none manual — not reachable until the
   AC-E3 benchmark lands) · **1** (a check FAILED) · **2** (no FAIL, MANUAL criteria remain).
   - **R1–R3** are deterministic (frontmatter present · ≥2 steps · name not a duplicate).
   - **R4** (genuinely reusable?) is always **MANUAL** — the script never auto-approves a skill.
   - **R5** (empirical value) is **result-driven**: if `/benchmark` produced
     `.claude/eval/benchmarks/<name>.json` for this draft, R5 reports PASS/FAIL from it;
     otherwise it degrades to MANUAL. Run `/benchmark --component <draft-name>` to close it.
4. **On FAIL (exit 1):** fix the draft (add frontmatter, add steps, or rename to avoid the
   collision) and re-run. Do not stage a draft that FAILs.
5. **Adjudicate MANUAL (exit 2 — the expected happy path):** judge R4/R5 yourself with
   evidence — is this a workflow you'd actually reach for again, distinct from existing
   skills? Record the verdict + reasoning in `.claude/skills-staging/<slug>/eval.md`
   alongside the draft.
6. **Stage for approval. Stop there.** Tell the user the proposal is staged at
   `.claude/skills-staging/<slug>/` (draft + eval note) and that promoting it into `skills/`
   is their explicit call. Do **not** promote it yourself.

## Security & trust
- `extract-rubric.js` runs **no shell** and never executes the draft's body — an ` ```eval `
  fence inside a draft is inert text to it, so there is no check output to leak.
- `--list` is the safe inspect path: `node scripts/eval/extract-rubric.js --list <draft>`
  prints the parsed name/description + which criteria are deterministic vs. MANUAL.
- The Stop detector and this skill record only tool/skill **names** (from the trace, which
  stores no args) — never session content, commands, or secrets.

## Notes
- Self-contained: rubric + detector are pure Node, no companions (mgrep/graph/context7).
- The AC-E3 benchmark (`/benchmark`, fork + worktree, pass@k/pass^k) feeds the R5 seam in
  `extract-rubric.js`: it reads the benchmark artifact if present, else R5 stays MANUAL and
  never blocks.

## Exit criterion
A proposal (`SKILL.md` draft + `eval.md`) is staged under `.claude/skills-staging/<slug>/`,
the rubric shows no FAIL, and every MANUAL criterion is adjudicated with evidence. Promotion
into `skills/` remains a human decision — never automatic.
