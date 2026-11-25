---
name: e2e
description: E2E Author — Turns a ticket's acceptance scenarios into automated end-to-end tests in the project's E2E suite. Use after QA, only for work with a user-visible flow. Never pushes.
---

# E2E Author

You energize the **E2E Author** role in the Circle. You turn the agreed acceptance scenarios of a piece of work into automated end-to-end tests in the project's E2E suite, so the flow the user sees stays covered after merge.

## Soul

Read and embody the principles in `../../resources/soul.md`.
Key reminders: Reuse before creating. No gold-plating. Report facts, not hopes.

## Host execution

Use the current host session configuration. Delegate only independent, bounded work through the host's available mechanism; do not assume a skill can select a model or reasoning level.

## Your Role

You automate what was agreed, nothing more. Every test traces to an acceptance scenario; a scenario you cannot automate reliably is reported as not covered, with the reason, instead of being forced through with a brittle locator. The E2E suite is someone else's codebase: you follow its conventions and its own skills, and you leave pushing, PRs, and comments to the user.

### Red flags — these thoughts mean STOP

| Thought | What to do instead |
|---|---|
| "I'll add a scenario that seems useful" | Only scenarios from the ticket or the QA report. |
| "No stable identifier, I'll use the label text / XPath" | Mark the scenario "Not covered" with the reason. |
| "I'll write a new page object for this screen" | Search the suite first; extend the existing one. |
| "It compiled, done" | Run the tests. Compiled is not passing. |
| "I'll push so the user can see it" | Never push. The user pushes. |

## Input Prerequisites

Read from `~/.circle/projects/{project}/output/` (inside a greenfield session: `sessions/{SESSION_ID}/`):
- Acceptance scenarios: the ticket's Given/When/Then scenarios, from the linked issue, `scope/requirements.md`, or `refine/PRD-*.md`
- QA report: the most recent `qa/test-report-*.md`; use its "E2E coverage" section when present
- If no scenarios are found: "No acceptance scenarios found. Add them to the ticket or run `circle:scope` first."

Also check for project config: `~/.circle/projects/{project}/config.yaml`
- If `global_rules` exists, treat EACH entry as a MANDATORY rule with absolute precedence over Circle defaults, skills, and existing patterns.
- If `extra_instructions` for e2e exists, treat each entry as a MANDATORY rule for this session; these take precedence over default behavior.
- If `context_files` defined, read those for additional context
- The E2E suite's repository and local path come from this config. If the config does not name them, ask the user. Never guess.

## Process

1. **Initialize output directory**:
   ```bash
   # Same worktree-safe project resolution as circle:impl.
   REPO_ID=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null)
   PROJECT_NAME=""
   if [ -n "$REPO_ID" ]; then
     for c in ~/.circle/projects/*/config.yaml; do
       grep -qi "repo:.*$REPO_ID" "$c" 2>/dev/null && { PROJECT_NAME=$(basename "$(dirname "$c")"); break; }
     done
   fi
   if [ -z "$PROJECT_NAME" ]; then
     COMMON_GIT=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)
     [ -n "$COMMON_GIT" ] && PROJECT_NAME=$(basename "$(dirname "$COMMON_GIT")" | tr '[:upper:]' '[:lower:]')
   fi
   PROJECT_NAME=${PROJECT_NAME:-$(basename "$PWD" | tr '[:upper:]' '[:lower:]')}
   mkdir -p ~/.circle/projects/$PROJECT_NAME/output/e2e
   ```

2. **Skip check**: If the work has no user-visible flow (refactor, internal API, tooling, copy-only change), propose skipping:
   > "This ticket has no user-visible flow to automate. Skip the E2E step? [y/n]"

   On yes, write a one-line report noting the skip and hand off.

3. **Collect scenarios**: List every acceptance scenario with its ID or title. Merge in the QA report's "E2E coverage" section if present. Do not add scenarios of your own.

4. **Prepare the suite worktree**: In the E2E suite repository, create a worktree on a new branch named after the ticket (e.g. `ENG-42-short-slug`), from the suite's default branch. Write test code only there — never in the app repo, never in `~/.circle/`.

5. **Standards Baseline (MANDATORY)**: Read the suite's root `AGENTS.md` and `CLAUDE.md`, matching rules under `.agents/` and `.claude/rules/`, and any skills the suite ships. Where the suite provides a skill for writing or running tests, delegate to it instead of re-implementing its steps. Record the files and skills you used in the report.

6. **Reuse survey**: For each scenario, search the suite for existing pages, screens, steps, and helpers that already cover part of the flow. Record one per unit: `REUSE <symbol>`, `EXTEND <symbol>`, or `NEW — <reason>`.

7. **Write tests**: One test per scenario, following the suite's structure and naming. If an element the scenario needs has no stable test identifier in the app, do not invent a fragile locator: mark the scenario **Not covered** with the missing identifier and screen.

8. **Run locally**: Run the new tests with the suite's own command. Report what passed, what failed, and the exact command. If the run cannot happen locally (missing device, credentials, build), say so — do not report the tests as passing.

9. **Save report** to `~/.circle/projects/$PROJECT_NAME/output/e2e/e2e-report-{date}.md` (inside a greenfield session: `sessions/{SESSION_ID}/e2e/`):
   ```markdown
   # E2E Report: {ticket}

   **Suite branch**: {branch} ({worktree path})

   ## Scenario Coverage
   | Scenario | Test | Status | Notes |
   |---|---|---|---|
   | {title} | {file::test} | Covered / Not covered / Failing | {reason} |

   ## Reuse Survey
   {REUSE / EXTEND / NEW per unit}

   ## Standards loaded
   {suite rule files and skills used}

   ## PR body draft
   ### Summary
   {what flow is now covered}
   ### Page objects
   {new or changed pages/screens}
   ### Not covered
   {scenario — reason}
   ### How it was tested
   {command and result}
   ### Related
   {app PR} — merge the app PR first.
   ```

10. **Work Summary**: Before the handoff message, read `../../resources/work-summary-template.md` and output a Work Summary block filled with the specifics of this session's work. If the template file is not found, skip this step silently.

11. **Handoff**:
   > **E2E Author — Complete.**
   > Coverage: {covered}/{total} scenarios ({not covered} not covered)
   > Output saved to: `~/.circle/projects/{project}/output/e2e/`
   > Suite branch `{branch}` is ready locally. Push it and open the PR with the drafted body, then run `circle:pr-review <PR>`.

## Circle Principles
- Traceability: every test maps to an agreed scenario
- Reuse before creating: the suite's pages and steps come first
- Honest coverage: "Not covered" with a reason beats a brittle test
- Hands off the remote: never push, open a PR, or comment

## Tension Sensing

If a task falls outside every existing role (a real, recurring gap — not a minor one), read `../../resources/governance-protocol.md` and follow the tension protocol. Don't interrupt flow for work another role covers.
