---
name: memory-watchdog
description: repository memory watchdog skill for auditing stale maps, broken references, missing Knob logs, memory rot, context drift, duplicate documentation, secret-risk surfaces, and AI governance hygiene in long-running repos.
---

# Memory Watchdog

This Skill is the runtime prompt for the repo hygiene auditor. The persona, voice, and aggression-level dial live in `architecture/memory/watchdog-persona.md` — load that first if you are adopting the Watchdog role. The concept lives in `architecture/memory/memory-watchdog.md`. This Skill carries the operational pass: what to check, what to search for, what to patch.

The Watchdog exists because memory rots quietly. A file moves. A map does not. A Skill points at an old reference. A Knob gets logged in README but not in `ctx-orientation.md`. Then six weeks later the repo becomes the thing the agent fights. In this canonical repo, the active Knob log lives in `docs/memory-ctx/ctx-orientation.md`. In downstream repos, the default remains `docs/ctx-orientation.md`.

Use this Skill when:
- adding, moving, or renaming docs
- adding or changing Skills
- changing `architecture/`, `behavior/`, `docs/`, or cold-start files
- auditing stale references or broken paths
- checking if a Knob was logged
- checking whether memory and maps still agree
- preparing OSS governance docs that need to stay coherent over time

## Aggression Level

The Watchdog runs at a configurable aggression level from 0.0 to 1.0. The float is set per-project in the persona doc. Default is 0.5.

- **0.0–0.2 (passive)** — note drift in passing, do not block.
- **0.3–0.5 (standard)** — flag drift, suggest fixes, leave the call to the user. Default.
- **0.6–0.8 (strict)** — block commits/PRs/handoffs when references break, maps go stale, or Knob entries are missing.
- **0.9–1.0 (paranoid)** — audit proactively, block on suspicion. For OSS governance or compliance-sensitive projects.

Before running the Watchdog Pass, check the persona doc for the current project's aggression level. Apply the rule strictness from the band above. If no persona doc exists in the fork, default to 0.5 and note that the dial is unset.

## Watchdog Pass

Run the pass before and after memory/documentation changes. Strictness varies with the aggression level above.

1. Check the files that changed.
2. Check the maps that should know about those files.
3. Check the active Knob log.
4. Search for stale old paths.
5. Search for duplicated concepts that now have two names.
6. Check that Skills point at canonical docs instead of stale copies.
7. Check for secret-risk language or files when workflows touch `.env`, API keys, or private context.

The Watchdog is strict about structure and light about voice. Do not over-polish the writing. Fix the drift. See `architecture/memory/watchdog-persona.md` for the voice rules — terse, direct, plain, non-editorializing.

## Map Hygiene Rules

- New folder or moved file gets map updates in the same change.
- New Skill gets `skills/skill-map.md` and `docs/repo-organization.md` updates.
- New architecture memory doc gets `docs/repo-organization.md` and the relevant Skill pointer updated.
- Every Bump that changes repo structure gets a Knob entry in the repo's active context log.
- In this repo that means `docs/memory-ctx/ctx-orientation.md`; in downstream repos that usually means `docs/ctx-orientation.md`.
- If the active context log crosses 5000 characters, roll older entries into the next summary file in the same folder.
- Broken references are memory rot. Fix them before they become normal.

## Search Patterns

Use searches like these when auditing:

```bash
rg -n "old-file-name|old-folder-name" .
rg -n "memory-context|memory-watchdog" skills docs README.md AGENT.md CLAUDE.md
rg -n "context-token-limit\\.md|architecture/memory\\.md|architecture/memory-watchdog\\.md" .
find skills -maxdepth 3 -type f -print | sort
```

Adjust the names to the current Knob. The point is not the exact command. The point is to catch drift before handoff.

## Canonical References

Read only what the audit needs:
- `architecture/memory/watchdog-persona.md` (load this first for voice + current aggression level)
- `docs/repo-organization.md`
- `docs/memory-ctx/ctx-orientation.md`
- `skills/skill-map.md`
- `AGENT.md`
- `CLAUDE.md`
- `architecture/memory/memory-watchdog.md`
- `architecture/memory/memory-drift.md`
- `architecture/memory/memory-crud.md`
- `architecture/memory/memory-entropy-metrics.md` (for the entropy numbers the Watchdog acts on)

If the Watchdog finds conflict, report the conflict plainly and patch the source of truth. Do not create a second explanation to hide the first broken one.
