---
name: sync-inno-factory-knowledge
description: Walk every project in the Innovation Factory ledger, extract new lessons and best practices from their lessons-learned files, CLAUDE.md, and recent git history, and merge them into the shared knowledge base at /Users/felix/Projects/innovation-factory. Non-destructive — shows a diff before writing. Use periodically (monthly, or after any project ships a milestone) to keep the knowledge base current.
---

# sync-inno-factory-knowledge

Pulls lessons + practices from every project registered in the Innovation Factory ledger into the shared knowledge base.

**Knowledge base:**
- `/Users/felix/Projects/innovation-factory/best-practices.md`
- `/Users/felix/Projects/innovation-factory/lessons-learned.md`
- `/Users/felix/Projects/innovation-factory/innovation-factory.md` (ledger)

---

## What the sync does

For each project in the ledger:

1. **Read the project's `lessons-learned.md`** (if any, common paths: `docs/lessons-learned.md`, `lessons-learned.md`).
2. **Read the project's `CLAUDE.md`** — look at the Constraints section for emerging patterns.
3. **Scan recent git history** (`git log --since="<last sync>" --pretty=format:"%h %s"`) for commits that look like bug fixes, security fixes, or preventive refactors. Keywords: `fix:`, `security:`, `postmortem`, `lesson`, `revert`, `emergency`.
4. **Identify new entries** — anything dated after the last sync timestamp recorded in `innovation-factory.md` § Version history.
5. **Categorize** by the existing sections in `best-practices.md` / `lessons-learned.md` (Architecture, Database, Auth, Deployment, Testing, Frontend, Accessibility, i18n, Mobile, Project hygiene).
6. **Promote** — if a lesson has fired in ≥2 projects, propose promoting it to `best-practices.md` and shortening the entry in `lessons-learned.md`.
7. **Show a diff before writing.** Use `TaskCreate` or just present the proposed changes in-chat. User confirms.
8. **Write** the approved changes. Update `innovation-factory.md` § Version history with a new row: `YYYY-MM-DD | Synced from <projects>: +N lessons, +M practices, K promotions.`

---

## Operating rules

1. **Non-destructive.** Never delete existing entries. Demoting a lesson after promotion means leaving a one-line stub that references the best practice.
2. **One row per concrete incident.** Don't summarize multiple bugs into one row — each was a real thing that bit.
3. **Keep the project column accurate.** If a lesson first fires in civion-resilience and is later confirmed in maki-tulum, add a second row or expand the project column to `civion-resilience, maki-tulum`.
4. **Dedupe honestly.** If a lesson is already in the file, don't add it again. If the phrasing in the source is better, update in place.
5. **Respect the format.** The tables have fixed columns — don't invent new ones. If the project's source uses different columns, map them.
6. **Don't sync project-specific details** that aren't portable. "Our Saneamiento config file lives at `packages/config/tax.ts`" is not a lesson. "Tax rates should live in a single config file" is.

---

## Typical run

```
User: /sync-inno-factory-knowledge

You:
  1. Read innovation-factory.md ledger → civion-resilience + maki-tulum registered.
  2. Read /Users/felix/Projects/innovation-factory/innovation-factory.md § Version history — last sync 2026-04-18.
  3. For each project:
     a. Read its lessons file if present
     b. git log --since="2026-04-18" in its root
     c. Skim CLAUDE.md constraints section
  4. Propose:
     - +3 new lessons under "Deployment" (from civion-resilience)
     - +1 new lesson under "Database" (from maki-tulum — first for that project)
     - Promote 1 lesson from lessons-learned.md §Testing to best-practices.md §Testing (fired in both projects now)
  5. Show the proposed diff inline.
  6. On confirmation, write the files.
  7. Append Version history row.
```

---

## What to skip

- Commits that only touch formatting, deps, or copy.
- Lessons that are already in the shared file (dedupe by root-cause substring).
- Project-specific implementation notes (file paths, vendor names unless they're a lesson *about* that vendor).
- Anything that's clearly domain-specific gossip and doesn't generalize.

---

## Edge cases

- **Project not using the lessons-learned format.** Fall back to CLAUDE.md constraints + git log keywords. Flag in the run summary that the project should adopt the format.
- **No new entries since last sync.** Still append a version-history row: `YYYY-MM-DD | Sync — no changes.` Keeps the cadence visible.
- **Conflicts.** If the same lesson exists in two phrasings, prefer the more specific one. Ask the user if ambiguous.
- **New project discovered** (e.g., user registered it but hasn't run `/sync-inno-factory-knowledge` yet). Include it. Flag first-time projects so their entries are easier to review.

---

## After syncing

Report back:
- How many entries added, promoted, updated.
- Which projects contributed.
- Any projects that are missing a `lessons-learned.md` and should adopt it.
- Any proposed promotions the user declined — note in the run summary so the sync doesn't re-propose them next time (use `innovation-factory.md` § "Rejected promotions" if needed).
