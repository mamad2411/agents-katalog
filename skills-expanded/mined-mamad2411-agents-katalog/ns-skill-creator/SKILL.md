---
name: ns-skill-creator
description: (NS) Create or improve project-local agent skills in a NextStage harness project — draft SKILL.md under .agents/skills/, run evals, then harness sync. Use whenever the user asks to create a skill, add a custom skill to this project, author SKILL.md, iterate on skill evals/benchmarks, or optimize skill descriptions — even if they say "make a skill for our repo" or "skill-creator". Do NOT use for contributing to the nextstage-brasil/skills catalog (that repo has its own maintainer workflow in AGENTS.md).
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
depends:
  - ns-harness
---

# Skill Creator (harness projects)

Create and improve **project-local skills** in the active harness project. The eval loop, description optimization, and bundled scripts come from the upstream **skill-creator** (anthropics/skills) — this skill only overrides **where files are saved** and runs **`harness sync`** after each create/update.

## Harness discovery

Resolve paths per `../ns-harness/references/harness-discovery.md`:

| Variable             | Value                                                     |
| -------------------- | --------------------------------------------------------- |
| `{product_root}`     | Repo or monorepo product folder (where `AGENTS.md` lives) |
| `{skills_canonical}` | `{product_root}/.agents/skills/`                          |

If `{harness_root}` is missing, tell the user to run `npx @nextstage-brasil/harness` first — this skill expects a harness-scaffolded project.

## Step 0 — Load upstream skill-creator

Harness init installs the anthropics skill-creator bundle (scripts, eval-viewer) at `{skills_canonical}/skill-creator/`, then installs this wrapper as `ns-skill-creator`.

For the full upstream workflow, read:

- `~/.agents/skills/skill-creator/SKILL.md` when installed globally, or
- [anthropics/skills — skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)

Use upstream for: intent capture, interview, SKILL.md anatomy, eval/benchmark loop, `eval-viewer/generate_review.py`, description optimization (`run_loop.py`), and scripts under `{skills_canonical}/skill-creator/scripts/`.

Apply the **path overrides** and **post-create sync** below on top of upstream instructions.

## Path overrides (project)

| Artifact                            | Path                                      | Notes                                                    |
| ----------------------------------- | ----------------------------------------- | -------------------------------------------------------- |
| New/edited skill                    | `{skills_canonical}/<kebab-case-name>/`   | `name` frontmatter must match directory                  |
| `SKILL.md`                          | `{skills_canonical}/<name>/SKILL.md`      | English unless the team defines otherwise in `AGENTS.md` |
| `references/`, `scripts/`, `evals/` | Under the skill directory                 | See `references/project-layout.md`                       |
| Eval workspace                      | `{product_root}/skill-creator-workspace/` | `iteration-N/eval-<id>/` per upstream                    |
| Upstream tooling                    | `{skills_canonical}/ns-skill-creator/`       | `scripts/`, `eval-viewer/` from anthropics bundle        |

**Never** save project skills to `skills/` at repo root (that layout is for the nextstage-brasil/skills **catalog** repo only).

## Project conventions

Read `references/project-layout.md` when drafting. If `{product_root}/AGENTS.md` defines language or skill conventions, follow them.

Summary:

- Pushy `description` in frontmatter for triggering (per upstream guidance).
- Keep `SKILL.md` under ~500 lines; move detail to `references/`.
- `evals/evals.json` — 2–3 realistic prompts when evals add value.
- Declare `depends:` in frontmatter only when the skill references other installed skills (e.g. `ns-harness`).

## Workflow

Follow upstream ns-skill-creator stages (capture intent → draft → eval → improve → repeat). At each write step, use the **path overrides** above.

## Post-create — harness sync

After skill files are written or materially updated, run from `{product_root}`:

```bash
npx @nextstage-brasil/harness sync
```

This regenerates Claude skill symlinks (`.claude/skills/`) so Claude Code discovers the new skill. Cursor reads `.agents/skills/` directly.

Use `npx @nextstage-brasil/harness sync --check` in CI when verifying adapters are up to date.

Report sync results to the user. Do not claim the skill is discoverable until sync completes successfully.

## Description optimization

After the skill is stable, offer upstream description optimization per upstream ns-skill-creator (`run_loop.py`). Use the model ID from the active session. Update `{skills_canonical}/<name>/SKILL.md` frontmatter, then run `harness sync` if needed.
