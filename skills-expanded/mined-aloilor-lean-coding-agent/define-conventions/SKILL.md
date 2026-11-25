---
name: define-conventions
description: "Create or update a repo's docs/conventions/ by grilling the user on rules the repo cannot show: coding standards and style, architecture boundaries, data access, authorization, API design, excellent code to imitate, how testing works and should work, deployments and environments, branching, reviews, and releases. Scans the repo for evidence, treats it as evidence rather than authority, and writes only non-obvious rules the user confirmed. Use whenever the user wants to create, define, set up, update, or audit project conventions, team rules, coding standards, testing rules, deployment notes, or branching and release conventions, or after setting up the Lean Coding Agent baseline in a project. Not for glossary or ADR work on its own, or for editing AGENTS.md."
---

# Define Conventions

Reach a shared understanding with the user about how work should be done in this repo, then write down only what an agent could not safely work out alone. `AGENTS.md` already tells agents when to read `docs/conventions/`, so leave `AGENTS.md` and `CLAUDE.md` alone.

| File | Covers | Grill guide |
| --- | --- | --- |
| `CODING-STANDARDS.md` | Coding style, architecture boundaries, exemplars, code to avoid copying, generated files, dependencies, data access and schema, secrets and logging, authorization and input trust, API design and compatibility | [references/CODING-STANDARDS.md](references/CODING-STANDARDS.md) |
| `TESTING.md` | What must pass, how testing works and should work, test environments, local setup traps | [references/TESTING.md](references/TESTING.md) |
| `DEPLOYMENT.md` | Environments and URLs, how deploys happen, migration rollout, rollback, hotfixes, incidents, flags, observability | [references/DEPLOYMENT.md](references/DEPLOYMENT.md) |
| `CHANGE-PROCESS.md` | Branching, commits, PRs, reviews, releases, docs that change with code | [references/CHANGE-PROCESS.md](references/CHANGE-PROCESS.md) |

Create a file only when it has content. Add another file, such as `SECURITY.md`, only when the grill produces enough rules on one topic to justify loading it separately. In a monorepo, keep one root `docs/conventions/` and name the package inside any rule that applies to only one. `GLOSSARY.md` and `adr/` belong to `lean-grill-with-docs`.

## Whose Word Counts

The repo is evidence and the user is the authority. Many people wrote this code, some of it badly or in a hurry, so the most common pattern is not automatically the right one.

- **You may propose rules the repo does not follow yet.** Only the user can adopt them.
- **Scope any rule the code does not follow yet**, or agents will either distrust it or start migrating code unprompted: "New code does X. `legacy/` does Y; don't copy it and don't migrate it unless asked."
- **The person answering can be wrong too.** Say at the start that the result is a proposal the team should review like any other change. "I don't know" is a valid answer: write nothing for it and list it as an open question in the final report.

## What Earns A Line

Keep a line only if a competent agent, reading the repo for its task, would otherwise guess wrong, spend real effort finding it, or copy the wrong pattern. Everything in these files costs tokens on every read, and agents follow what they read, so a useless line is worse than a missing one. There is no length limit, only this test.

| Fails | Passes |
| --- | --- |
| Tests run with `npm test`. | `test:integration` must also pass before merge, though CI skips it. |
| Use meaningful variable names. | Services return `Result`; only controllers turn errors into HTTP responses. |
| We use GitHub Actions. | Merging to `main` deploys to stage automatically; prod needs a manual approval. |

These limits apply to every line you write:

- **Already documented elsewhere.** First question whether it deserves a place here at all. If it does, state the rule in one line and stop.
- **No links or "see X" to repo documents.** Each rule has to stand alone. Allowed: plain-text code paths when the rule is about that code, external URLs that are themselves the fact (a stage URL), and skills named without a link.
- **No secrets.** Name environment variables, never values. Before recording an internal hostname, account ID, or non-public URL, ask, and offer the git-ignored `AGENTS.override.md` instead, because these files are committed.
- **Rules for agents.** Write terse imperative bullets under topic headings, with no intro text, overviews, or directory maps. Say "none" only where absence is useful, such as "There is no stage environment."

## Commands

Read-only lookups such as `git log`, `rg`, and file reads are fine. Never run migrations, seeds, deploys, publishes, installs, or anything else that changes state. Run a test or build only after the user says yes for that specific command, because tests can touch databases and other shared state. Record a command only if the user stated or confirmed it. If config and the user disagree, ask.

## Process

1. **Check the grill is available.** This skill depends on `$lean-grill-with-docs`. If it is not in the session, read `.agents/skills/lean-grill-with-docs/SKILL.md`. If neither exists, stop and tell the user to install it with `npx skills add aloilor/lean-coding-agent`.
2. **Scan.** Read `docs/conventions/`, `README`, `CONTRIBUTING`, `docs/`, CI config, and whatever the guides list under "Look at". If convention files already exist, follow **Updating** below.
3. **Agree the agenda.** Say the result is a proposal, then show the areas you plan to grill and let the user drop any or add their own. Ask what agents or new contributors keep getting wrong that the list misses, because the guides can only prompt for what they name. Grill an added topic with the area it fits best, or give it its own file if it fits none. An area that seems not to apply, like deployment for a library, gets one confirming question and is then skipped with no file.
4. **Grill one area at a time**, in this order: change process, testing, deployment, coding standards. Coding standards comes last so exemplar review benefits from the earlier rules. For each area, read its guide and run `$lean-grill-with-docs` on that area alone, so a round stays a size someone can answer. Always ask what agents may do alone in that area.
5. **Keep evidence from anchoring the answer.** The grill words questions so "yes" accepts your recommendation, which turns bad code into policy if the recommendation comes from frequency. On questions about what should be true, show the split ("12 files do X, 3 do Y") and recommend on quality. When no candidate is good, ask an open question.
6. **Draft and confirm each area before moving on.** Re-test every line against **What Earns A Line**, show the draft, and write the file once the user confirms. Writing per area means stopping halfway keeps finished work.
7. **Report in chat.** List files changed, rules added, changed, and removed, and open questions. Leave everything uncommitted so the team can review it.

## Updating

When the user names an area ("update testing"), grill only that area.

With no area named, audit first, read-only: do recorded paths, symbols, and scripts still exist, did new tooling or areas appear, and do existing lines break **What Earns A Line** or the no-link rule? Then grill only what you found.

- Treat existing content as human-confirmed unless it comes from an older layout, and show the current rule before asking about changing it. The person running this may not know why it was written.
- Code that drifted from a rule is a question, not a correction, because the code may be what's wrong.
- Change or remove a confirmed rule only after a yes.
- An older layout shows up as `WORKFLOWS.md`, `(inferred: ...)` markers, or `None.` under fixed headings. It was written mostly from scans, so treat its content as evidence and grill it before keeping it. Propose where each kept rule moves and delete the old file only after a yes.
