---
name: usage-monitor-token-cleanup
description: Measure the context this repo loads every session (CLAUDE.md, memory, skills), report evidence-backed cleanup candidates with estimated savings, and apply only what the user approves. Use to save tokens, trim context, clean up memory or shrink CLAUDE.md.
---

# Usage Monitor Token Cleanup

Measure first, propose with evidence, ask item by item, apply only what was approved, measure again. Nothing is changed before the user picks it.

## Targets

| Target | Loaded | Path |
|---|---|---|
| Project instructions | every session | `CLAUDE.md` |
| Global instructions | every session | `~/.claude/CLAUDE.md` |
| Memory index | every session | `~/.claude/projects/<project-key>/memory/MEMORY.md` |
| Memory files | on demand | same folder, `*.md` |
| Skill descriptions | every session | `.claude/skills/*/SKILL.md` frontmatter |
| Skill bodies | when invoked | `.claude/skills/*/SKILL.md` |

`<project-key>` is the absolute repo path with `:`, `\` and `/` replaced by `-`.

## Workflow

1. **Measure.** Run the read-only script and keep its output as the baseline:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\usage-monitor-token-cleanup\scripts\measure_context.ps1
   ```
   Tokens are `chars / 3.5` — label them as an **estimate** everywhere; this is not the tokenizer's count.

2. **Analyze.** Every finding carries the evidence that justifies it (line numbers, command output, file names). No evidence, no finding.
   - **Project `CLAUDE.md`** — it dominates the budget. For each heavy section or first-level bullet the script lists:
     - Narrative that is history, not rule: measurements, "a primeira versão", dated incidents, run ids, how a bug was found. Candidate action: **move** it to the plan in `docs/planos/` that already covers the subject (the script lists linked plans) or to a new `docs/<area>.md`, and leave in `CLAUDE.md` the rule in 1–3 lines plus the link. The *why* must survive in the destination — moving is allowed, deleting a decision is not.
     - Duplication: the same rule stated in two sections, or restating `docs/design-system/` / `server/README.md`. Candidate action: keep one owner, link from the other.
     - Rules the tests already enforce (e.g. `ArchitectureRulesTest`) can be shortened to the rule plus the test name, never removed.
   - **Memory**:
     - Broken pointers and orphan files (script output).
     - `project_*` memories citing issues: run `gh issue view N --json state,title` for each; a memory whose issues are all closed and whose pending work is done is a candidate for deletion.
     - Memories that duplicate `CLAUDE.md`, the repo, or git history (the memory rules say not to store those).
     - Memories naming a file, function or flag: `Grep` for it; if it no longer exists, the memory is stale.
   - **Global `CLAUDE.md`**: rules redundant with the project file, or conflicting with it. Report conflicts; never resolve them silently — the global file is the user's personal instruction set.
   - **Skills**: descriptions over ~300 chars (paid every session), and bodies that repeat `CLAUDE.md` instead of pointing to it.

3. **Report.** One table, sorted by estimated savings:

   | # | Target | Finding | Evidence | Est. tokens saved | Proposed action | Reversible? |
   |---|---|---|---|---|---|---|

   Reversibility: repo files are reversible through git; memory and `~/.claude/CLAUDE.md` live **outside** git and are not.

4. **Ask.** Use `AskUserQuestion` with `multiSelect: true`, one option per finding (batch in groups of up to 4 options per question, up to 4 questions per call). Before offering to delete or rewrite anything outside git, show its full current content in the report so the user decides on what they actually read.

5. **Apply only the approved items.**
   - Repo files: `Edit`, preserving line endings (`CLAUDE.md` is CRLF in the working copy).
   - Memory: delete the file **and** its line in `MEMORY.md`; when merging, update the surviving file and remove the other pointer.
   - Anything not selected stays untouched, including items the user did not answer.

6. **Measure again** with the same script and report before/after per target.

7. **Do not commit.** Commit only when the user asks, through `usage-monitor-commit-push`. Content moved from `CLAUDE.md` to `docs/` goes in the same commit as the removal, so no decision exists in neither place.

## Guardrails

- Never edit production code, tests, or build files.
- Never shorten a rule without the user approving that specific item.
- Never "summarize" a decision in a way that loses its reason without moving the reason somewhere.
- Never delete a memory whose issues you did not check with `gh`.
- If a finding is a judgment call (e.g. whether a passage is rule or history), say so in the Evidence column.
