---
name: setup-github-project
description: Creates or reconciles a lightweight GitHub Projects V2 planning system linked to a repository, using repository labels plus native parent/sub-issue relationships for phase, epic, specification, and implementation-ticket conventions. Use when the user asks to set up, configure, connect, or standardize a GitHub Project for a repository or planning document.
---

# Set Up a GitHub Project

Create a repository-linked GitHub Project using the operating model in [REFERENCE.md](REFERENCE.md).

## Non-negotiable approval gate

Before any local or GitHub write:

1. Read repository instructions, planning documents, issue-tracker conventions, and label documentation.
2. Inspect the repository, authentication, labels, existing issues, and existing Projects read-only.
3. Present every resolved default and exact write target to the user.
4. Identify inferred, absent, or conflicting values, plus every setting expected to require browser control and the documented CLI/API gap responsible.
5. Wait for explicit approval or requested changes.

Approval applies only to the presented configuration. Repeat the gate if a material choice changes. Do not create a Project, link a repository, create issues, or write repository files before approval.

## Preflight

Run `scripts/preflight.ps1` before `inspect.ps1` or any GitHub write. Treat its JSON result as a gate:

1. If `Ready` is `false`, report every entry in `Missing` with its matching corrective action from `Guidance`.
2. Ask the user to resolve the prerequisite or explicitly authorize the proposed corrective action.
3. Stop setup. Do not continue discovery commands that depend on the missing prerequisite.
4. Rerun preflight after the user acts. Continue only when `Ready` is `true`.

Preflight must confirm Git, a GitHub remote or explicitly supplied `OWNER/REPO`, GitHub CLI 2.94.0 or newer, authenticated repository access, Project API access, and that Issues and Projects are enabled. Handle a missing planning source separately during discovery: describe what could not be derived and ask the user for the source or an explicit scope decision rather than inventing phases or epics.

## Discovery

Resolve, without inventing:

- Repository from the current workspace's Git remote.
- Project owner from the repository owner; ask if ownership is ambiguous.
- Project title from the repository name.
- Phases and epics from the GDD, product plan, roadmap, or equivalent.
- Existing labels `phase`, `epic`, `spec`, `ready-for-agent`, and `ready-for-human`, reusing them when present.
- Existing specs, phase issues, epics, tickets, Projects, native parent/sub-issue relationships, and duplicates.

Default to a private GitHub Projects V2 Project linked to one repository. Reuse an existing matching Project only after approval.

Run `scripts/preflight.ps1 -Repository OWNER/REPO` first, then run `scripts/inspect.ps1 -Repository OWNER/REPO` only after preflight succeeds.

## Approved execution

After approval:

1. Create or reuse and link the Project.
2. Keep Status options `Todo`, `In Progress`, and `Done`.
3. Ensure repository labels `phase`, `epic`, `spec`, `ready-for-agent`, and `ready-for-human` exist exactly once.
4. Create only source-supported Phase and Epic issues; search for duplicates first.
5. Attach every Epic as a native sub-issue of exactly one Phase, and every implementation ticket as a native sub-issue of exactly one Epic.
6. Add Phase issues, Epics, and implementation tickets to the Project. Keep specification issues outside the Project and native hierarchy.
7. Set Status only; do not require custom hierarchy fields such as `Work Type`, `Phase`, `Epic`, or equivalents.
8. Give each specification issue the `spec` label and no readiness label. Link it from its Epic's `Specification` section; never use a specification as a parent of implementation tickets.
9. Configure the views and workflows in [REFERENCE.md](REFERENCE.md), including auto-add on `phase`, `epic`, and the two readiness labels plus native auto-add of sub-issues. Exclude `spec` from auto-add.
10. Reconcile `docs/agents/github-project.md` from [templates/github-project.md](templates/github-project.md), preserving repository-specific details when they do not conflict with the contract.
11. Add a concise pointer to `docs/agents/github-project.md` in the repository's root `AGENTS.md`. Preserve all unrelated instructions and avoid duplicate pointers.
12. Verify the finished system and report inconsistencies.

Use the following tool order for every GitHub operation:

1. Use a dedicated `gh` command when available.
2. Otherwise use `gh api graphql` when the public GraphQL API supports the write.
3. Otherwise use `gh api` against a documented REST endpoint. Create saved views through the Project views REST API with the explicit supported API-version header.
4. Use authenticated browser control only after confirming that neither the CLI nor a documented public write API supports the exact setting. Before opening the browser, tell the user which setting remains and which API capability is absent.

Do not treat the absence of a dedicated `gh project` subcommand as proof that browser use is required. Announce necessary browser use and avoid the tab the user is actively operating.

## Safety and reconciliation

- Never expose tokens or credentials.
- Never invent phases, epics, dates, estimates, or parent relationships.
- Never silently close, reopen, split, reparent, or rewrite issues for tidiness.
- Prefer splitting cross-epic tickets; dominant-parent assignment requires user direction.
- Report closed-parent/open-child inconsistencies without resolving them automatically.
- Labels alone do not establish hierarchy. Always reconcile both the label and the native parent issue.
- Make every operation idempotent by inspecting before creating or updating.

## Verification

Run `scripts/verify.ps1 -Repository OWNER/REPO -Owner OWNER -ProjectNumber N` for a read-only structural report, then complete the UI checks in [REFERENCE.md](REFERENCE.md). Summarize created, reused, changed, skipped, and unresolved items.
