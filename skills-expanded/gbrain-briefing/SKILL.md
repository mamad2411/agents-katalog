---
name: gbrain-briefing
description: Compile a daily briefing from brain state. Covers active deals, open threads, people in play, and what needs attention.
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: [gbrain]
---

# Briefing Skill

## Briefing structure

1. **Overview** — `gbrain stats` to get brain state at a glance.

2. **Active deals** — `gbrain list --type deal --tag active`
   For each: `gbrain get <slug>` → State + deadlines + what's changed.

3. **Open threads** — Scan recently updated pages for Open Threads with time-sensitive items:
   ```bash
   gbrain list --limit 30  # recently updated
   gbrain get <slug>       # for each, check Open Threads section
   ```

4. **People in play** — `gbrain list --type person --limit 20`
   Prioritize: pages updated in last 7 days, tagged with `active` or `follow-up`.

5. **Recent brain changes** — `gbrain list --limit 20` sorted by updated_at.
   What was ingested, what's new, what changed.

6. **Stale alerts** — Pages that haven't been updated in 30+ days but have open threads.

## Output format

```markdown
# Brain Briefing — YYYY-MM-DD

## Active Deals
- **[Company](companies/slug)** — status, next step, deadline

## Open Threads
- **[Person](people/slug)** — what needs to happen

## People in Play
- **[Name](people/slug)** — current context

## Recent Activity
- Updated: slug, slug, slug

## Needs Attention
- Stale pages, unresolved threads
```

## Delivery

Write briefing to the brain:
```bash
cat briefing.md | gbrain put sources/briefing-$(date +%Y-%m-%d)
```
