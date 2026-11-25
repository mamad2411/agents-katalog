---
name: swarm-skill-forge
description: Author new high-quality skills that trigger reliably and stay lean. Use when creating or editing a skill, packaging a workflow as a skill, or deciding whether something should be a skill at all.
---

# swarm-skill-forge — skill authoring

A skill is packaged judgment: instructions a future agent follows *instead of* its
defaults. Write one only when that trade is worth it.

## Gate: should this be a skill?

- Recurring task with a non-obvious right way → skill.
- Single fact or preference → memory note. Project convention → CLAUDE.md/AGENTS.md line.
- One-off → nothing. When in doubt, don't — catalogs rot.
- **Overlap check first:** `ls` the installed skills; if an existing skill covers 70% of
  the job, extend it instead of adding a sibling (two skills for one job = router
  confusion).

## Structure

```markdown
---
name: kebab-case-verb-or-domain
description: <what it does> + <every trigger phrasing a user might use>. The
  description IS the router — write it for the model deciding whether to load.
---
# Name — one-line job
Gate / when NOT to use.
Numbered steps, imperative, each observable ("run X, expect Y").
Rules the defaults would get wrong.
Worked example (input → output).
```

- Platform-agnostic markdown only — it must read the same via Claude Code skills and a
  Codex AGENTS.md index.
- **Portable on its own (NFR-C4):** the folder must work when copied out alone, with no
  vault, no `swarmvault.py`, and no siblings installed. Name peer skills by what they add,
  never as a prerequisite, and give every vault-backed path a local fallback ("`voice.md` in
  the vault, else `.writing/voice.md`"). Skills *about* the vault are the exception.
  **Degrade, don't downgrade:** write the vault path first and fullest, then the fallback.
  A skill weakened so a lone copy can satisfy it has failed this rule, not passed it.
- Heavy reference material (> ~150 lines) → `references/*.md`, loaded on demand; the
  SKILL.md tells the reader *which* reference to load *when*.
- Machine-lane style for checklists/tables; prose where nuance matters.

## Verify before shipping (skills are code — test them)

1. **Trigger dry-run:** write 3 paraphrases of how a user would ask; does the
   description clearly fire for them — and clearly NOT fire for near-misses?
2. **Toy walk:** execute the skill on a small real case; every step must be doable
   without information the skill forgot to mention.
3. **Altitude check:** delete every line the model would do correctly anyway — a skill
   states only what defaults get wrong.

## Ship

Project skills → `.claude/skills/<name>/` + an AGENTS.md index line (name, description,
when-to-use, path) for Codex. Contributions to SwarmVault itself → canonical `skills/`
+ a CREDITS.md entry if the technique has an upstream.

---
*Influences: superpowers writing-skills; Pocock's writing-great-skills — see CREDITS.md.*
