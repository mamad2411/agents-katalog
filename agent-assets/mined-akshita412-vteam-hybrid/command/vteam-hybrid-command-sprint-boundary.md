<!-- agent-notes: { ctx: "mandatory sprint boundary: retro + sweep + gate + passes", deps: [CLAUDE.md, docs/methodology/personas.md, docs/methodology/phases.md, docs/tech-debt.md, docs/performance-budget.md], state: active, last: "coordinator@2026-02-28" } -->
Run the mandatory sprint boundary workflow for: $ARGUMENTS

This is the **canonical end-of-sprint process**. It must be run at every sprint boundary — it is NOT optional and should NOT require the user to trigger it manually. When Grace detects that the sprint's work is complete (all sprint items are Done or explicitly deferred), this workflow triggers automatically.

---

## Step 0: GitHub Board Access Pre-Flight (Blocking)

Before any sprint boundary work, verify GitHub board access is functional. If any check fails, **STOP immediately** — do not proceed to the retro or any subsequent step. Report the specific failure and ask the user to fix it.

1. **GitHub CLI authentication:**
   ```bash
   gh auth status
   ```
   If this fails: "GitHub CLI is not authenticated. Please run `gh auth login` and try again."

2. **Project board configured:** Check that `CLAUDE.md` has a `project-number` and `project-owner` set (not commented out / not blank). If missing: "No project board is configured in CLAUDE.md. Run `/kickoff` to set one up, or add the project-number and project-owner manually."

3. **Board accessible:**
   ```bash
   gh project field-list <NUMBER> --owner <OWNER> --format json
   ```
   If this fails: "Cannot access project board #<NUMBER>. Check that the project exists, is linked to this repo, and you have write access. Fix this before continuing."

4. **All 5 statuses exist:** From the field list output, confirm the Status field has Backlog, Ready, In Progress, In Review, and Done options. If any are missing: "Board is missing required status options. Fix this before continuing (see `/kickoff` Phase 5 Step 2)."

Only proceed to Step 1 after all checks pass.

---

## Step 1: Sprint Retro (Automatic)

Run `/retro` inline. This is not a suggestion — it happens now, as part of this workflow. The retro will:

1. Reflect on the sprint.
2. Create a retrospective document in `docs/retrospectives/`.
3. Create GitHub issues labeled `process-improvement` for every identified problem.
4. Update `CLAUDE.md` with lessons learned.

**Do not skip this step.** Do not ask the user if they want a retro. Just run it.

### Wei / Debate Protocol Compliance Audit

As part of the retro, audit whether the Architecture Gate was followed this sprint:

1. **List ADRs created or modified this sprint** (check `docs/adrs/` for files with dates in this sprint's range).
2. **List debate tracking artifacts** (check `docs/tracking/*-debate.md` for this sprint).
3. **Cross-reference:** For every ADR, verify a corresponding debate artifact exists. Flag any ADR that lacks a Wei debate.
4. **Scan for unrecorded decisions:** Review the sprint's commits and code changes for architectural decisions that were made *without* an ADR (new patterns, new integrations, new packages, data model changes). Flag each one.
5. **Report in the retro document:**
   - "**Architecture Gate compliance:** X/Y ADRs had Wei debates tracked. Z architectural decisions were made without ADRs."
   - For each gap, note: which decision, what Wei could have challenged, and whether a retroactive ADR + debate should be scheduled.
6. **Create process-improvement issues** for any gaps found — these feed into Step 3's gate, ensuring they're addressed before the next sprint.

---

## Step 1b: Board Health & Status Compliance Audit

Audit the project board for configuration issues and status transition violations.

### Board Configuration Check

```bash
# Verify all 5 required statuses exist
gh project field-list <NUMBER> --owner <OWNER> --format json
```

Confirm the Status field has options: **Backlog, Ready, In Progress, In Review, Done**. If any are missing:
- **BLOCKING:** Add the missing statuses immediately (see `/kickoff` Phase 5 Step 2 for GraphQL commands).
- Create a `process-improvement` issue: "Board missing required status options."
- This is a root cause for status transition violations — fix it before auditing transitions.

### Status Transition Compliance

```bash
# List all items and their current statuses
gh project item-list <NUMBER> --owner <OWNER> --format json
```

For every item marked **Done** this sprint:
1. Verify it passed through **In Progress** before reaching In Review/Done.
2. Verify it passed through **In Review** before reaching Done.
3. Flag any item that jumped directly from Ready/In Progress → Done (skipping In Review).

**Report in the retro document:**
- "**Board compliance:** X/Y items followed the full status flow. Z items skipped statuses."
- For each violation: which issue, what status was skipped, and why (if known).
- Create `process-improvement` issues for systemic violations.

---

## Step 2: Backlog Sweep

After the retro, sweep the entire backlog to catch orphaned or user-created issues:

1. **List ALL open issues** on the repo: `gh issue list --state open --json number,title,labels,assignees --limit 500`.
2. **Categorize every issue:**
   - **Current sprint (done):** Issues labeled `sprint:N` (current sprint) that are Done → verify they're closed. Close any that aren't.
   - **Current sprint (not done):** Issues labeled `sprint:N` that are NOT Done → these must be explicitly addressed: carry forward to next sprint, or defer with rationale.
   - **Prior sprint (still open):** Issues labeled `sprint:M` where M < N → these are **orphans**. Flag each one. They must be carried forward, re-triaged, or closed with explanation.
   - **No sprint label:** Issues with no `sprint:*` label → these are either user-created or fell through the cracks. Triage each one: assign to next sprint, add to backlog, or close with explanation.
3. **Report findings** to the user:
   - "Sprint N complete: X issues closed, Y carried forward, Z orphans found, W new/unassigned issues triaged."
   - List each non-closed issue with its disposition.
4. **Get user confirmation** on the triage decisions before applying labels.

This step is critical because it:
- Catches issues that were never picked up
- Picks up issues the user created directly on the repo (allowing user influence on the backlog)
- Prevents work from silently disappearing between sprints

---

## Step 3: Process-Improvement Gate

Before the next sprint can begin, verify that process-improvement issues from the retro have been addressed:

1. **List process-improvement issues:** `gh issue list --label "process-improvement" --state open --json number,title`.
2. **For each open process-improvement issue:**
   - If it can be resolved now (e.g., updating a process doc, adding a checklist), resolve it immediately.
   - If it requires sprint work, it MUST be included in the next sprint — add `sprint:N+1` label.
   - It cannot simply be ignored or deferred indefinitely.
3. **Gate check:** If any process-improvement issue is neither resolved nor scheduled for the next sprint, **block sprint start** and flag to the user.

---

## Step 4: Technical Debt Review

Review the technical debt register (`docs/tech-debt.md`):

1. **Log new debt:** Any shortcuts or known issues from this sprint get added to the register.
2. **Escalation check (hard constraint):** Any debt open for 3+ sprints is **automatically P0 for the next sprint**. This is not a suggestion — escalated items MUST be included as P0 in the next sprint's plan. Grace has authority to enforce this over Pat's prioritization. The only override is an explicit user decision to defer.
3. **Review with Pat:** Which non-escalated debt items should be paid down next sprint? Pat decides based on risk and business value. Pat CANNOT deprioritize escalated items below P0 or label them as stretch goals.

---

## Step 5: Periodic Passes (when warranted)

Not every sprint needs these. Grace decides based on how much code and dependencies changed this sprint. Run them if significant changes occurred, or at minimum every 3 sprints and before any release.

### Dead Code Pass (Vik)
- Sweep for unreachable functions, unused exports, orphaned tests, unused dependencies, commented-out code.
- Report findings. Unused dependencies flagged to Pierrot for SBOM cleanup.

### Dependency Health Pass (Pierrot)
- Check for abandoned packages (no updates > 12 months), major version drift, single-maintainer risk.
- Update SBOM with findings.
- Flag concerning dependencies to Pat for prioritization.

---

## Step 5b: Operational Baseline Audit (Ines + Diego) — Mandatory

Unlike the periodic passes in Step 5, this audit runs **every sprint**. It checks product health, not just process health.

### Ines: Operational Concerns Audit

Invoke Ines to audit the codebase against the applicable concerns in `docs/process/operational-baseline.md`. For each concern in the applicability matrix that applies to this project type:

1. **Logging coverage** — Is a logging module configured? Do significant operations log at appropriate levels? Do `--verbose`/`--debug` flags work (if applicable)?
2. **Error pattern consistency** — Does an error module/pattern exist? Is it followed consistently across modules? Are user-facing errors actionable?
3. **Debug support** — Can a developer diagnose failures from logs alone, without a debugger attached?
4. **Config health** — Is config validated at startup? Do invalid values produce clear messages? Is `.env.example` or equivalent current?
5. **Graceful degradation** — Do external calls have timeouts? Do failures produce user-friendly messages?

### Diego: README "5-Minute Test"

Invoke Diego to verify the README quick-start by **executing it**, not just reading it:

1. Execute the quick-start commands against the current codebase (install deps, run the tool).
2. If external tools are unavailable or require credentials, run the project's own entry point (e.g., `npm start -- --help`, `python main.py --help`) to verify it bootstraps without errors.
3. For commands that cannot be executed, verify them by reading — but document which steps were execution-verified vs. read-verified.
4. If any step fails or requires undocumented knowledge, flag it as a **P1 defect**.

### Report

Append findings to the sprint retro document:

```markdown
## Operational Baseline Audit — Sprint N

### Ines: Operational Concerns
| Concern | Status | Finding |
|---------|--------|---------|
| Logging | Foundation / Below / N/A | ... |
| Error UX | Foundation / Below / N/A | ... |
| ...     | ...    | ...     |

### Diego: README 5-Minute Test
- **Result:** Pass / Fail
- **Issues found:** [list or "None"]
```

### Gate

If **3 or more** applicable concerns are below Foundation level AND the project is past sprint 2, this is a **blocking gate**. Grace creates P1 work items for each below-Foundation concern and includes them in the next sprint. This mirrors the tech debt escalation pattern — it's enforceable, not advisory.

---

## Step 5c: Visual Smoke Test (Dani + Playwright) — Web Apps Only

**Skip this step** if the project is a CLI, library, or backend-only service with no UI.

For web-app projects (Dash, Next.js, React, Svelte, etc.), verify that the product actually renders:

1. **Start the application** — run the project's start/dev command.
2. **Navigate to each registered page/route** using Playwright (`browser_navigate`).
3. **Take a screenshot** of each page (`browser_take_screenshot`).
4. **Check browser console** for errors (`browser_console_messages`) — JavaScript errors, failed network requests, React/framework warnings.
5. **Invoke Dani** to review the screenshots for obvious visual issues (broken layouts, missing content, unstyled components, accessibility red flags).

### Report

Append findings to the sprint retro document:

```markdown
### Dani: Visual Smoke Test
- **Pages checked:** [list of routes/pages]
- **Console errors:** [count, or "None"]
- **Visual issues:** [list, or "None"]
- **Screenshots:** [attached or "available on request"]
```

### Gate

If any page fails to render or has JavaScript errors, this is a **blocking finding**. Grace creates a P0 work item for the next sprint. Visual issues (broken layout, missing content) are P1.

**Why this exists:** The portfolio-manager project shipped 3 sprints of Dash UI code without anyone opening a browser. All code-centric gates passed. This step catches the "Invisible UI" anti-pattern — see `docs/process/gotchas.md`.

---

## Step 6: Archive Tracking Artifacts

Archive completed tracking artifacts from this sprint:

1. **Create archive directory:** `docs/tracking/archive/sprint-N/` (where N is the current sprint number).
2. **Move completed artifacts:** Move all tracking artifacts with status `Complete` from `docs/tracking/` to the archive directory. Keep any `Active` or `Blocked` artifacts in place — they carry forward.
3. **Verify links:** If any active artifacts reference archived ones in their **Prior Phase** field, update the path to the archive location.

This prevents the tracking directory from growing unbounded while preserving the audit trail.

---

## Step 7: Next Sprint Setup

Once the gate passes:

1. **Create `sprint:N+1` label** if it doesn't exist.
2. **Carry forward items:** Apply `sprint:N+1` label to all carried-forward issues.
3. **Include tech debt items** that Pat prioritized for paydown.
4. **Sprint planning:** Invoke Pat for prioritization of the next sprint's backlog. For each item, identify whether it requires the Architecture Gate (see CLAUDE.md § Architecture Gate) and note it in the sprint plan.
   4b. **Product context refresh:** Pat reads `docs/product-context.md` and the retro document from Step 1. If priorities have shifted, proxy decisions were corrected by the human, or the retro surfaced product-level insights, Pat updates `docs/product-context.md`. Log changes in the Correction Log table.
5. **Update board:** Move next-sprint items to **Ready** status on the project board using the board status commands (see `docs/integrations/github-projects.md`). Each item transitions individually — do not batch-update.
6. **Announce:** Summarize the next sprint's scope to the user. Include which items require the Architecture Gate (ADR + Wei debate before implementation).

---

## Step 8: Clean-Tree Gate (Mandatory, Terminal)

This step is the **final gate** of the sprint boundary. It runs after ALL other steps and ensures nothing was left behind.

```bash
git status --porcelain
```

**If the working tree is clean:** Sprint boundary is complete. Report success.

**If the working tree is dirty:** The boundary is NOT complete. This catches late file operations — archive deletions, code reviews, tracking artifact moves — that weren't included in earlier commits.

1. **Show the dirty files** to the operator: list every unstaged/untracked change.
2. **Stage and commit them:**
   ```bash
   git add -A
   git commit -m "chore: sprint-N boundary cleanup — stage orphaned changes"
   ```
3. **Re-check:** Run `git status --porcelain` again.
4. **If STILL dirty:** STOP. Refuse to declare the boundary complete. Surface the remaining dirty files to the user and ask them to resolve manually.

**Why this gate exists:** Sprint boundary workflows involve many file operations across multiple steps (archival, artifact creation, code reviews, backlog triage). Commits that run before or independently of all file operations leave deletions unstaged and new files untracked. Without this gate, every sprint boundary is a coin-flip on whether late-written artifacts get orphaned into the next session. This is a structural fix — do NOT remove it.
