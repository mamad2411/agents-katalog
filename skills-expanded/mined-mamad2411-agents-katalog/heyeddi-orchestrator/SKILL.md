---
name: heyeddi-orchestrator
description: Discover HeyEddi skills, auto-sync .heyeddi/ (skill names + index), cross-pillar opinions, and suggest @skills. Use at session start, after reinstalling skills, or when connecting heyeddi-product, ux-flow-auditor, and heyeddi-design on a route.
version: 2.0.0
---

# HeyEddi Orchestrator

**Skill discovery and workspace sync** — routes work to the right `@skill`, refreshes `.heyeddi/`, and **keeps product, UX, and design pillars in sync**.

## When to use

- Session start on a HeyEddi project (`.heyeddi/` present or greenfield app request)
- User asks "what skills do we have?" or "which skill should handle this?"
- Before a multi-step pipeline (intake → scaffold → design → handoff → QA)
- **Any time one pillar runs** — bookend with `load_workflow_context` / `append_pillar_opinion`
- After `@heyeddi-intake` — confirm `skill-routing.json` before downstream work

## Automatic `.heyeddi/` upkeep

**You do not need a manual sync command.** Every HeyEddi skill tool call runs auto-sync first:

1. **Migrates** v1 skill names in `.heyeddi/` → v2 `heyeddi-*` (routing JSON, index, docs)
2. **Refreshes** `.heyeddi/skills-index.{json,md}` when missing or after migration changes

Reinstall skills (`npx skills add`) and keep working — the next `@heyeddi-intake`, `@heyeddi-product`, or orchestrator tool updates `.heyeddi/` automatically.

Optional explicit full sync (includes workflow scaffold): `sync --project-root .`

## Cross-pillar sync (mandatory for product · UX · design)

Read **`reference/cross-pillar-workflow.md`**.

```
init_workflow_sync                    (once per project)
load_workflow_context --route /path   (start of pillar session)
… @heyeddi-product | @ux-flow-auditor | @heyeddi-design work …
append_pillar_opinion --pillar …      (end — triggers sibling opinions)
```

## Skill discovery pipeline

```
load_catalog / suggest_skills   → auto-sync runs first
read one SKILL.md               → follow that skill's pipeline
```

If `.heyeddi/docs/intake/skill-routing.json` exists, **follow route order**.

## Tools

| Script | Purpose |
|--------|---------|
| *(auto)* | Every tool — migrate skill names + refresh index when needed |
| `sync.py` | Optional full sync + workflow scaffold |
| `migrate_heyeddi.py` | Migrate v1 `@skill` names in `.heyeddi/` only |
| `write_skills_index.py` | Scan → `.heyeddi/skills-index.*` (runs migrate first) |
| `load_catalog.py` | Read cached index |
| `suggest_skills.py` | Rank skills for a prompt |
| `suggest_next_skill.py` | Next @skill + command after any skill finishes |
| `init_workflow_sync.py` | Scaffold `.heyeddi/docs/workflow/` |
| `load_workflow_context.py` | Sibling opinions + checklist for route |
| `append_pillar_opinion.py` | Log opinion; request UX/design/product response |

## When the task is complete — suggest next skills

When you have **finished the user's request** for this skill (not after every tool call or subagent phase), suggest what to run next:

1. Run:

   ```bash
   python .agents/skills/heyeddi-orchestrator/scripts/suggest_next_skill.py --current-skill heyeddi-orchestrator --project-root .
   ```

   Add `--route /path` if you worked a specific route.

2. Include the script's **`### Next step`** block in your **final** reply. The user copies the **Prompt** line into chat (e.g. `@heyeddi-design craft /settings`).

Pass `--mode shape` (or `craft`, `audit`, etc.) when you know which sub-command just finished.

See `@heyeddi-orchestrator` → `reference/next-skill-handoff.md`.

## Related

- `@heyeddi-product` · `@ux-flow-auditor` · `@heyeddi-design` — three pillars
- `@heyeddi-intake` — upstream intake
- `reference/next-skill-handoff.md` — next-skill block when a pipeline task completes
- `docs/cross-pillar-workflow.md` — hub summary
