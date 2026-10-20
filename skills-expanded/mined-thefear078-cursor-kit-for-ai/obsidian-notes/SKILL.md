---
name: obsidian-notes
description: MUST USE for Obsidian vault workflows — atomic notes, wikilinks, daily notes, MOCs, capture from dev sessions. Triggers on PKM setup, linking docs, or "organize my notes" in Obsidian.
---

# Obsidian Notes

Obsidian is a **local-first graph of thoughts**. Optimize for fast capture, deep linking to code/decisions, and weekly MOC maintenance — not folder hierarchy perfection.

## When This Skill Applies

- Setting up dev knowledge vault
- Linking ADRs, specs, meeting notes
- Daily note habit with `daily-plan`
- Migrating from Notion/markdown chaos
- Agent handoff into durable notes

## Severity Model (Vault Health)

| Level | Signal | Action |
|-------|--------|--------|
| **V0** | Secrets in vault synced to public git | Remove + rotate |
| **V1** | No daily capture; orphan notes >50% | MOC + inbox sweep |
| **V2** | Duplicate MOCs; broken links | Link hygiene hour |
| **V3** | Aesthetic plugins | Optional |

Cross-ref: `notion-workflow` for team-shared tracking; `handoff` for session exports; `weekly-review` archives.

## Phase 0 — Vault Structure (Minimal)

```text
vault/
  00-inbox/          # fleeting captures
  01-daily/          # YYYY-MM-DD.md
  02-projects/       # one note per project + link to repo
  03-areas/          # eng, product, health
  04-resources/      # refs, snippets
  05-archive/
  MOC-home.md        # map of content index
```

Folders are shallow — **links carry structure**.

## Phase 1 — Note Types & Templates

### Daily note

```markdown
# {{date}}

## Plan
- [[daily-plan output]]

## Log
- 

## Links created
- 
```

### Project note

```markdown
# Project: [[repo-name]]

**Repo:** path/url
**Status:** active/paused
**Related:** [[MOC-engineering]]

## Current bet
## Decisions
## Open questions
```

### Decision (ADR-lite)

```markdown
# ADR: [title]
**Date:** | **Status:** accepted

## Context
## Decision
## Consequences
```

## Phase 2 — Linking Discipline (2025–2026)

- Prefer `[[wikilinks]]` over folders for discovery
- One concept per note — merge monsters split
- Link **on create** not "later cleanup"
- Use aliases for acronyms: `[[Row Level Security|RLS]]`
- Embed queries (Dataview) optional — start manual MOC

```markdown
## MOC-engineering
- [[schema-design]] skill notes
- [[Project API v2]]
- [[ADR postgres vs neon]]
```

## Phase 3 — Capture from Dev Sessions

After `session-context` or `handoff`:

1. Create/update project note "Session YYYY-MM-DD"
2. Link commits/PRs as plain URLs
3. Tag `#session` `#todo` sparingly (tags ≠ structure)

## Phase 4 — Plugins (Judicious)

| Plugin | Use |
|--------|-----|
| Daily notes | Auto open today |
| Templates | Consistency |
| Git | Private vault only; `.gitignore` attachments |
| Dataview | MOC automation when >100 notes |

Avoid plugin overload — sync conflicts hurt more than features help.

## Phase 5 — Hygiene Ritual (Weekly, 30m)

- Empty `00-inbox` → file or delete
- Update MOC-home top 5 active projects
- Fix broken links report
- Archive completed projects

Pair with `weekly-review` output pasted into Sunday daily note.

## Output Template

```markdown
## Obsidian Setup / Review: [vault name]

**Verdict:** healthy / 🔶 needs hygiene / ❌ secrets risk

### Structure
- Folders:
- MOCs:

### Actions
1. Create templates: ...
2. Link notes: ...

### Recommended notes to create
- [[...]]

### Sync/git
- Remote:
- Secrets scan: clean/ issue
```

## Anti-Patterns

- **Deep folder trees** — notes hard to find
- **Vault in public GitHub** with `.env` snippets
- **Duplicate project notes** — merge with redirect link
- **PDF-only knowledge** — not linkable
- **Never revisiting MOC** — graph rots

## Cross-References

| Skill | Use when |
|-------|----------|
| `notion-workflow` | Team-visible status |
| `research` | Cite sources into literature notes |
| `architecture` | ADR storage |

## Cursor Kit Templates

- Link plugin README skills as literature notes

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

