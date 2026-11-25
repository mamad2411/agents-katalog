---
name: weeder
description: Measure and reduce a Skill's token footprint (always-loaded description + on-trigger SKILL.md body) without regressing routing accuracy or losing instructions. Use when a SKILL.md feels oversized, repeats rules, or has a vague description that might mis-route.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/bin/weeder *), Bash("${CLAUDE_SKILL_DIR}/bin/weeder" *)
---

# weeder

!`"${CLAUDE_SKILL_DIR}/bin/weeder" mode --banner`

Agents that do not expand the line above (e.g. Codex): run
`<this-skill-dir>/bin/weeder mode --banner` first and follow it.

The description loads every session; the SKILL.md body loads on every
trigger. **Never optimize on token count alone**: a shorter SKILL.md that
routes worse or drops an instruction is a regression. Every step below
produces before/after evidence. Run all commands as
`python3 <this-skill-dir>/scripts/weeder.py <cmd>`.

1. **Audit:** `audit <skill_dir>`. Token counts per section (description
   vs. body, chars/4 estimates unless calibrated), duplicate rules, filler,
   movable background/examples. Read all of it; `optimize` acts on only part.
2. **Mechanical pass:** `optimize <skill_dir> --out <skill_dir>-optimized`.
   Moves background/examples sections into `references/` with a pointer.
   Lossless and reversible, so it's safe to always apply; it does not touch
   the description or duplicates.
3. **Judgment pass, in the `-optimized` copy:** shorten the description
   (keep concrete trigger nouns/verbs), state each duplicated rule once
   where the workflow needs it, cut only instructions that are genuinely
   obvious to a capable agent; don't cut something just because it's short. Optional structured help: `suggest <skill_dir> --assist slight --json`,
   then `apply-suggestion <skill_dir> --answer <answer.json> --out <skill_dir>-optimized`
   (see `references/llm-assist.md`; an assisted answer gets no free pass).
4. **Routing:** `test-routing <skill_dir> --examples <examples.json> [--competing <other_skill_dir> ...]`
   on both original and copy. `examples.json` = `{"positive": [...],
   "negative": [...], "ambiguous": [{"prompt":, "expected": "trigger"|"no_trigger"|"either"}]}`;
   if none exists, write 5-10 real triggers, a few unrelated prompts and
   borderline cases. Always pass sibling skills as `--competing`.
   Limits of this lexical proxy: `references/routing-heuristic.md`.
5. **Function:** `test-function <skill_dir> <skill_dir>-optimized` checks
   every never/must/do-not sentence survives (in SKILL.md or a reference).
   A MISSING constraint is a hard blocker, not a warning.
6. **Report:** `diff <skill_dir> <skill_dir>-optimized --examples <examples.json> --competing ...`.
7. **Accept only if** routing accuracy after >= before (minus a small
   tolerance: a couple of points of a lexical proxy is noise) AND
   constraint preservation is 100%. Otherwise do another pass in step 3;
   don't lower the bar to make a bad result pass.

With the plugin, prefer delegating the whole workflow to the `weeder`
agent (it preloads this skill and returns only the report) so the audit
output stays out of your context.

Classification rules and why step 3 isn't automated:
`references/classification.md`.
