---
name: session-context
description: MUST USE when opening an unfamiliar repo, resuming after a break, or handing off to an agent — map structure, active branch, recent changes, run commands. Triggers on "where were we?" or new workspace orientation.
---

# Session Context

Every session starts with **evidence, not memory**. Build a compact map of repo state, recent git activity, and open risks in 10–15 minutes — output feeds `task-triage` and `handoff` (engineering).

## When This Skill Applies

- First hour in a new codebase
- Return after vacation or context switch
- Parent agent needs orienting brief
- Onboarding another contributor or agent

## Severity Model (Orientation Gap)

| Level | Signal | Action |
|-------|--------|--------|
| **O0** | Deploy/prod changes planned without knowing branch or tests | Stop — orient first |
| **O1** | Unknown failing CI or dirty tree | Resolve before feature work |
| **O2** | Stale mental model of architecture | Run session-context |
| **O3** | Minor doc drift | Note in brief |

Cross-ref: `task-triage` for what to do next; `daily-plan` for time boxing; `research` (engineering) for deep dives.

## Phase 0 — Safety Snapshot

```bash
git status -sb
git branch -vv
git log -5 --oneline
git stash list
```

Note: uncommitted work, wrong branch, unpushed commits.

## Phase 1 — Repo Map

```bash
# Top-level layout
ls -la
# Common manifests
test -f package.json && cat package.json | head -30
test -f pyproject.toml && head -20 pyproject.toml
test -f README.md && head -40 README.md
# Entry points
rg -l "main\(|if __name__|createApp|FastAPI" --glob '*.{py,ts,js,go}' | head -15
```

Produce:

| Area | Path | Purpose |
|------|------|---------|

Max 10 rows — link to deeper docs if exist.

## Phase 2 — Runtime & Test Commands

Discover canonical commands (Makefile, package.json scripts, justfile):

```bash
test -f Makefile && grep -E '^[a-zA-Z0-9_-]+:' Makefile | head -20
npm run 2>/dev/null | head -20
```

Record: install, test, lint, run dev, deploy.

## Phase 3 — Active Workstreams

```bash
git log --oneline -15 --author-date-order
gh pr list --limit 5 2>/dev/null
gh issue list --limit 5 2>/dev/null
```

Summarize: what changed recently, open PRs, linked tickets.

## Phase 4 — Risk Flags

Quick scans:

```bash
# Failing tests locally? (optional if time)
# npm test -- --runInBand 2>&1 | tail -5

rg -n "TODO|FIXME|HACK" --glob '!node_modules' | head -10
```

Note: known flaky areas, secrets paths (don't print values), prod config files.

## Phase 5 — Session Brief Output

Use template every time — same shape helps agents.

## Output Template

```markdown
## Session Context: [repo name]

**Date:** | **Branch:** | **Clean tree:** yes/no

### Goal this session (if known)
- ...

### Repo map (top areas)
| Path | Role |

### Commands
- Install:
- Test:
- Run:

### Recent git (5)
- ...

### Open work
- PRs:
- Issues:

### Risks / unknowns
- ...

### Suggested next skill
- [ ] `task-triage` — pick work
- [ ] `to-spec` — if request vague
- [ ] `debug` — if active failure
```

## Anti-Patterns

- **Reading entire repo** — map first, depth on demand
- **Assuming default branch is main** — check
- **Skipping CI status** — repeat broken work
- **No written brief** — next session repeats cost
- **Mixing two repos** in one brief without labeling

## Cross-References

| Skill | Use when |
|-------|----------|
| `task-triage` | Choosing next task |
| `handoff` | End session compact export |
| `weekly-review` | Weekly orientation |

## Cursor Kit Templates

- Use plugin README skills table for domain skills available

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

