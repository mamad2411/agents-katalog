---
name: scm-steward
version: 1.0.0
description: Use when the Owner asks about repo hygiene, SCM debt, zombie worktrees, stale branches/claims/stashes, PR or issue aging, or periodic 형상관리 점검/정리.
triggers:
  - scm
  - hygiene
  - steward
  - 형상관리
dependencies:
  - scripts/scm_steward.py
  - scripts/worktree_lifecycle_gate.py
  - scripts/inflight_overlay.py
registry_id: scm-steward
template_path: src/agent_runtime/templates/project/skills/scm-steward/SKILL.md
---

# SCM Steward

Periodic hygiene loop that detects, reports, and (after approval) cleans SCM
debt across worktrees, branches, stashes, claims, PRs, issues, and generated
views -- before a human has to notice it.

## When To Run

1. Session start (W0 visibility): one read-only report alongside the session
   baseline so debt is visible before new work begins.
2. Periodic loop: scheduled run (cron / Owner-invoked `/scm-steward`) at
   least once per working day during active parallel waves.
3. On demand: before closeout, before a release cut, or whenever the Owner
   asks "what is dirty right now?".

## Required Sequence (report -> approve -> execute)

1. Report (read-only, non-blocking, always exit 0):

   ```powershell
   python scripts/scm_steward.py report
   ```

   Sections: `[worktrees]` zombies/merged branches (worktree_lifecycle_gate)
   plus in-flight branch divergence (inflight_overlay), `[claims]` stale
   leases, `[stashes]` un-reclaimed archive stash refs with recovery
   guidance, `[github]` PR aging/drafts and issues missing work-item
   registration, `[views]` generated-view drift (`--check` modes of the
   backlog board, work-item classifier, evidence index). Use `--json` for
   machine-readable output and `--skip-gh` when offline.

2. Review findings with the Owner. Reporting never blocks any gate or hook.

3. Clean only what was approved:

   ```powershell
   python scripts/scm_steward.py clean --approve <worktrees|claims|stashes|github|views|all>
   ```

   - `worktrees`: delegates to `worktree_lifecycle_gate` cleanup (local-only,
     retention/PRESERVE/dirty guards apply).
   - every other section only PRINTS the exact commands it would run
     (`gh pr close`, `gh issue close`, `git branch -D`, regenerate commands).
   - `clean` without `--approve` reports and changes nothing.

4. Execute gh mutations only behind the Owner gate:

   ```powershell
   python scripts/scm_steward.py clean --approve github --execute-gh
   ```

## gh Helpers (dry-run by default)

- Task branch push -> draft PR (title = task id, body = claim handoff link):

  ```powershell
  python scripts/scm_steward.py pr-open --task TASK-AR-NNN
  ```

- Closeout merge -> PR comment + close:

  ```powershell
  python scripts/scm_steward.py pr-close --pr <number> --task TASK-AR-NNN
  ```

- W3 adjacent-problem intake <-> gh issue create/close sync:

  ```powershell
  python scripts/scm_steward.py issue-sync --intake-title "<problem>" --intake-ref BUG-00X
  ```

## Owner-Gated Boundaries

- `--execute-gh` is Owner-gated: never run gh mutations (PR create/close,
  issue create/close) or remote pushes without explicit Owner approval in
  the current session. Default is always dry-run printing.
- Archive stash refs (`archive/stashes/*`) are preservation evidence from
  session closeout; deletion commands are print-only and require the Owner
  to confirm the content was reclaimed first.
- Merge execution and release actions stay out of scope (merge queue and
  release council own them).
- Unregistered issues are never closed; they get registration guidance
  (BACKLOG.md / agents/lead_engineer/tasks/) instead.
