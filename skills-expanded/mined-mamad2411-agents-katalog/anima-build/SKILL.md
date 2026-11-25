# /anima-build — ANIMA Build Supervisor Dashboard

## Purpose

Real-time monitoring of the parallel ANIMA build. Run this in Terminal 0 (supervisor terminal) on `main` branch. Shows all 5 builder lanes, PRD progress, test status, conflicts, and suggests next actions.

## Usage

```
/anima-build              # Show full dashboard
/anima-build status       # Quick status of all lanes
/anima-build review       # Review latest commits across all lanes
/anima-build gate         # Check if current GATE is ready to merge
/anima-build merge        # Execute GATE merge (interactive)
```

## What This Skill Does

You are the SUPERVISOR. You do NOT write code. You:

1. **Monitor** — `git fetch --all`, check each lane branch for new commits
2. **Review** — `git diff main..lane-X/prd-NNN` to review code quality
3. **Track** — Read NEXT_STEPS.md for lane status, count PRDs done
4. **Detect** — Check for HANDOFF_*.md, CONFLICT_*.md, PRD_ISSUE_*.md
5. **Test** — Run test suite on main after merges
6. **Merge** — At GATE points, merge lane branches to main with `--no-ff`
7. **Report** — Show dashboard with progress bars, test counts, blockers

## Dashboard Format

On each invocation, produce this dashboard:

```
╔══════════════════════════════════════════════════════════════╗
║                    ANIMA BUILD DASHBOARD                     ║
║                    {current_date} {current_time}              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  LANE A (Compiler)     PRD-XXX ████████░░ NN%  [{status}]   ║
║  LANE B (Modules)      PRD-XXX ██████████ DONE ✅            ║
║  LANE C (Infra)        PRD-XXX ██████░░░░ NN%  [{status}]   ║
║  LANE D (Hardware)     PRD-XXX ████░░░░░░ NN%  [{status}]   ║
║  LANE E (Demo)         PRD-XXX ░░░░░░░░░░ 0%   [waiting]    ║
║                                                              ║
║  Progress: NN/24 PRDs complete                               ║
║  Current GATE: {N} — {N}/{M} PRDs ready for merge            ║
║  Tests on main: {pass} pass, {fail} fail                     ║
║  Conflicts: {N}  |  Handoffs: {N} pending                    ║
║                                                              ║
║  GPU Server: {status}                                        ║
║  Last commit: [{lane}][{prd}] {message}  {time_ago}          ║
║                                                              ║
║  SUGGESTED ACTION: {what to do next}                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## How to Gather Data

```bash
# 1. Fetch all branches
git fetch --all --prune

# 2. List all lane branches
git branch -r | grep "lane-"

# 3. For each lane branch, count commits ahead of main
git rev-list --count main..origin/lane-a/prd-001-module-schema

# 4. Check latest commit per lane
git log origin/lane-a/prd-001-module-schema --oneline -1

# 5. Check for communication files
ls HANDOFF_*.md CONFLICT_*.md PRD_ISSUE_*.md INTERFACE_CHANGE_REQUEST.md 2>/dev/null

# 6. Read NEXT_STEPS.md for lane statuses
cat NEXT_STEPS.md

# 7. Run tests on main
pnpm test 2>/dev/null; uv run pytest tests/ -v 2>/dev/null

# 8. Check PRD completion (grep for ✅ in NEXT_STEPS.md)
grep -c "✅" NEXT_STEPS.md
```

## GATE Merge Protocol

When you determine a GATE is ready:

```bash
# 1. Verify all required PRDs for this GATE are done
# (check each lane's branch has passing tests)

# 2. Merge each lane branch to main (one at a time, --no-ff)
git checkout main
git merge origin/lane-a/prd-001-module-schema --no-ff -m "[GATE-1] Merge PRD-001 module schema"
git merge origin/lane-c/prd-006-anima-msgs --no-ff -m "[GATE-1] Merge PRD-006 anima_msgs"
# ... repeat for each lane branch in this GATE

# 3. Run full test suite
pnpm test && uv run pytest tests/ -v

# 4. If tests pass → push
git push origin main

# 5. Notify all builders to pull latest main
# (they'll see it next time they read NEXT_STEPS.md)

# 6. Update NEXT_STEPS.md with GATE completion
```

## Rules for Supervisor

1. **NEVER write code** — only review, merge, and coordinate
2. **Review EVERY commit** before GATE merge — catch bugs early
3. **Resolve conflicts** by creating fix branches, not by editing lane branches
4. **Keep NEXT_STEPS.md current** — builders depend on it
5. **Prioritize unblocking** — if a builder is stuck, help them first
6. **Run tests after every merge** — don't push broken main

## GATE Schedule

```
GATE 1 (April 4):   PRD-001,002,003,004,005,006,007
GATE 2 (April 11):  PRD-008,009,010,011,012,013,020
GATE 3 (April 18):  PRD-014,015,016,017,018,024
GATE 4 (April 25):  PRD-019,021,022,023 + Thor hardware test
```

## Related
- `/anima-strategy` — Company war room (strategy, not build)
- `/code-intelligence` — Multi-agent codebase analysis
- `docs/BUILD-GUIDE.md` — Full build guide with week-by-week breakdown
