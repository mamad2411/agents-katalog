---
name: notion-workflow
description: MUST USE for Notion project tracking — databases, views, statuses, specs linked to git, solo/small-team workflows. Triggers on Notion setup, sprint board, or "track projects in Notion."
---

# Notion Workflow

Notion excels at **shared visibility** — databases with single source of truth for status, specs, and decisions. Keep engineering detail in git; Notion holds outcomes, links, and lightweight process.

## When This Skill Applies

- Small team project hub
- Spec + ticket hybrid without full Jira
- Personal OKRs + project list
- Customer/project CRM-lite
- Agent updating status after ship

## Severity Model

| Level | Signal | Action |
|-------|--------|--------|
| **N0** | Secrets/credentials in Notion pages | Delete + rotate |
| **N1** | Two conflicting status boards; no owner field | Consolidate |
| **N2** | Stale >30d items not archived | Hygiene |
| **N3** | View clutter | Simplify |

Cross-ref: `task-triage` for priority; `weekly-review` for bet tracking; Atlassian plugin if enterprise Jira needed.

## Phase 0 — Database Architecture

Recommended **Projects** database:

| Property | Type | Purpose |
|----------|------|---------|
| Name | title | |
| Status | select | Idea / Active / Blocked / Done |
| Priority | select | P0–P3 |
| Owner | person | |
| Repo | url | GitHub |
| Target date | date | |
| Spec | relation | → Docs db |

Separate **Docs** db for specs/ADRs (relation back to project).

## Phase 1 — Views (2025–2026)

- **Board** by Status — daily standup
- **Table** filtered Active — `task-triage` input
- **Timeline** — target dates
- **My work** — filter Owner = me
- **Done last 7d** — `weekly-review` evidence

Avoid duplicating same data in pages + db — database is canonical.

## Phase 2 — Spec Page Template

```markdown
# [Feature name]

**Project:** @Projects
**Status:** Draft / Approved / Shipped

## Problem
## Success metrics
## Scope (in / out)
## Git
- Branch:
- PR:

## Open questions
```

Link to engineering `to-spec` output — don't rewrite twice; paste or embed link.

## Phase 3 — Rituals

| Ritual | Notion action |
|--------|----------------|
| Daily | Update Active item status; comment blockers |
| Triage | Re-prioritize P0–P3; archive Done |
| Weekly | Review Done view; set 3 bets on Projects |

## Phase 4 — Integrations

- GitHub PR links in Spec — manual or automation (Notion API, Zapier, `github-workflow` integrations plugin)
- Do not sync full codebase — link only
- MCP Notion: read/update pages when authorized

```bash
# If using Notion API (server-side token in env — never in page)
curl -s "https://api.notion.com/v1/databases/$DB_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" | jq '.title'
```

## Phase 5 — Permissions & Hygiene

- Guest access minimal; internal pages default private
- Archive Done >90d to cold database
- Naming: `[P0] Feature — short name` in title for scanability

## Output Template

```markdown
## Notion Workflow: [workspace area]

**Verdict:** ✅ / 🔶 / ❌

### Databases
| Db | Rows | Issue |

### Views to create/fix
- ...

### Migration steps
1. ...

### Field definitions
- Status meanings:

### Integrations
- GitHub:
- Agent update policy:
```

## Anti-Patterns

- **Notion as code repository**
- **Duplicate project trackers** (Notion + GitHub Projects + spreadsheet)
- **50 status columns** — nobody updates
- **Pasting API keys** in code blocks in specs
- **No Done archive** — board slow and demoralizing

## Cross-References

| Skill | Use when |
|-------|----------|
| `obsidian-notes` | Private deep notes |
| `to-tickets` | Break spec into tasks |
| `daily-plan` | Pull today's Active rows |

## Cursor Kit Templates

- `integrations` plugin for GitHub/Notion MCP

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

