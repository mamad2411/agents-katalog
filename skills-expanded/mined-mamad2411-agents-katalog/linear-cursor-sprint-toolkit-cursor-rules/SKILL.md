# AI Rules for This Repo

Guidelines for AI assistance in this repository.

---

## Private Files

Files starting with `.team-lead` are **private** and gitignored.

- Do not include content from private files in generated documents
- When referencing team members, use only info from `docs/team-roster.md`
- You may reference the existence of private files, but not their contents

---

## Folder & File Conventions

### Meetings
- Path: `meetings/cycle-XX/` (e.g., `cycle-18`, `cycle-19`)
- Files: `YYYY-MM-DD-[type].md` (e.g., `2026-01-16-standup.md`)

### Focus Notes
- Path: `focus/YYYY-MM/`
- Purpose: Team lead's personal priorities (me-centered, separate from team meetings)

### Key References
- `docs/team-roster.md` — factual team info (source of truth)
- `docs/processes/sprint-calendar.md` — ceremony schedule
- `docs/references/ticket-prioritization.md` — priority definitions

---

## Linear CLI

Use npm scripts to query Linear:
- `npm run issues:inprogress` — current work in flight
- `npm run triage` — items needing triage
- `npm run issue -- TICKET-XXX` — fetch ticket details

---

## Sprint Operations

- **Standups:** Customize your schedule (e.g., Mon–Thu live, Friday async)
- **Sprint length:** 2 weeks (cycles)
- **Definition of Done:** Deployed to prod, verified, metrics established

---

## Document Generation

When creating documents:
- Keep team member references factual (role, timezone, focus area)
- Focus on tickets and process, not individuals
- Check `docs/team-roster.md` for availability constraints

---

## Customization

This is a template repository. Customize these files for your team:
- `docs/team-roster.md` — Your team members
- `docs/processes/sprint-workflow.md` — Your ceremony times
- `package.json` — Your team member Linear query scripts
- `.cursor/commands/*.md` — Your team-specific workflows

---

**Last Updated:** [Update this date when you modify rules]
