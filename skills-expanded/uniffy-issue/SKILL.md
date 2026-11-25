---
name: uniffy-issue
description: |
  Create or refine GitHub issues in `uniffy-io/uniffy` using the project's title, template, dependency, project, and image-attachment conventions. Use when asked to create, open, file, draft, report, rename, or track a bug, feature, security issue, or performance issue in this repository, including requests that begin with `[BUG]`, `[FEATURE]`, `[SECURITY]`, or `[PERFORMANCE]`. Skip for pull requests, commit messages, implementation plans that do not need a tracking issue, other repositories, or general GitHub CLI questions.
---

# Uniffy Issue Creation

Codifies the issue conventions for the `uniffy-io/uniffy` repo. Apply every time you draft, refine, or post an issue.

## Title format

`[TYPE] Domain: short description`

- `TYPE` is one of `BUG`, `FEATURE`, `SECURITY`, `PERFORMANCE`.
- `Domain` is CamelCase, named after the vertical slice (backend `src/uniffy/domains/<x>/` and frontend `src/ui/src/features/<x>/` share the name). Omit the `Domain:` segment only if the change is genuinely cross-cutting with no dominant domain.
- Keep titles under ~80 chars. Detail goes in the body, not the title.

Examples:
- `[BUG] Agents: cannot read images sent in chat`
- `[FEATURE] Chat: app-wide messenger dock`
- `[FEATURE] Agents: rooms domain tools`

## Templates

Four issue forms live in `.github/ISSUE_TEMPLATE/`:

| File | Use for |
|---|---|
| `bug.yml` | Defects in existing functionality |
| `feature.yml` | New functionality or significant enhancement |
| `security.yml` | Hardening, audit findings, dependency CVEs (NOT active exploits - those email `admins@uniffy.io`) |
| `performance.yml` | Slowness, high resource use, scalability |

When creating via `gh issue create --body`, write the body in the shape the matching template expects (same section headings + order). When the user files via the web UI, the template renders automatically.

## Labels

None. Issues in this repo carry no labels: the title prefix carries the type and domain, and the `Area` body section carries the areas. Do not add labels even though `domain:*` and `area:*` labels still exist in the repo.

## Body sections (FEATURE template - the gold standard)

```
## Summary
One paragraph. What and why in one breath. No fluff.

## Motivation
User need, business driver, technical gap. The "so what".

## User Story
As a <role>, I want <capability> so that <outcome>.

## Scope

In:
- bullet of every behaviour the change must produce
- include concrete file paths and module names when known
- include acceptance-checkable items

Out:
- explicit non-goals (deferred to v2, separate issue, won't fix)
- prevents scope creep during execution

## Acceptance Criteria
- [ ] each criterion phrased as a verifiable check
- [ ] every Scope-In bullet should produce at least one box
- [ ] include tests, migrations, docs updates, telemetry as boxes
- [ ] always include rule-driven boxes that apply to the change

## Area
backend / frontend / mobile / proto / infra

## Alternatives Considered
- **Option name.** One-line description. Rejected: reason.
- Three to five alternatives is typical. Show the road not taken.

## Additional Notes - First-Glance Pointers
Where the change lands in the codebase. File paths, class names, line numbers.
Hidden constraints, performance bars (see backend rules' Performance-Critical
Domains for chat/agents), prerequisite refactors.
```

For BUG: replace Motivation/Scope/Acceptance with Steps to Reproduce / Expected / Actual / Severity / Environment.
For SECURITY: Category / Severity / Impact / Reproduction-or-Evidence / Suggested Mitigation / References.
For PERFORMANCE: Current Measurement (numbers + how measured) / Target (threshold + why) / Reproduction / Profiling Evidence / Suspected Cause.

## Pre-creation recon (mandatory for non-trivial issues)

Before writing the body, do enough recon to make "Additional Notes - First-Glance Pointers" accurate. Verify the gap is real:

1. Search the affected domain with `rg` and `rg --files` to confirm the claimed missing behaviour really is missing - never assert "code does not handle X" without searching.
2. Read the key files referenced in the body. Cite `file_path:line_number`.
3. Cross-check `.agents/rules/<domain>.md` for established patterns.
4. Check `.agents/local/plans/backlogs/` and any available project memory for relevant state, prior decisions, or feedback rules.

If the user says "first analyse" or "don't create yet", deliver findings as a regular response and wait for the go-ahead. Otherwise proceed to create after recon.

## Creating via gh CLI

```bash
gh issue create \
  --title "[FEATURE] Domain: title" \
  --body "$(cat <<'EOF'
## Summary
...
EOF
)"
```

After creation, capture the issue number from the URL output. Then:

1. **Link blockers** via GraphQL (gh CLI has no native flag):
   ```bash
   # Get node ids
   gh api graphql -f query='query { repository(owner:"uniffy-io", name:"uniffy") { issue(number:<blocked>) { id } } }' --jq '.data.repository.issue.id'
   gh api graphql -f query='query { repository(owner:"uniffy-io", name:"uniffy") { issue(number:<blocker>) { id } } }' --jq '.data.repository.issue.id'
   # Create the dependency
   gh api graphql -f query='mutation { addBlockedBy(input: { issueId: "<blocked-id>", blockingIssueId: "<blocker-id>" }) { issue { number } } }'
   ```
   Use the native dependency, NOT a plain comment or markdown link. The dependency shows in the sidebar and filters like `is:open is:issue -blocked:*`.

2. **If the user wants an image attached**: `gh` CLI cannot upload binary attachments. Two paths:
   - Default: create the issue without the image, tell the user to drag-drop it into the issue in the browser, and preserve its temporary path for handoff.
   - Persistent: commit the image to a tracked location and reference via raw URL. Only with explicit user OK - polluting the repo for an issue asset is rarely worth it.

## Style and content rules

Apply `AGENTS.md`, the relevant `.agents/rules/`, and these issue-specific conventions when drafting body text:

- **No emojis anywhere.** Not in titles, bodies, commit messages, or PR descriptions.
- **Single hyphens only.** Never use em dashes or double hyphens; use ` - ` or a comma to separate clauses.
- **Cite file:line** for "where this lands" pointers. Never invent paths. If you cannot verify, say "look around `domains/<x>/`" instead of fabricating a specific file.
- **No comments-style narration**. Body sections describe the work, not the conversation that led to it. Do not write "as discussed", "per the user", "from our chat earlier".
- **Acceptance Criteria boxes must be verifiable**. "Works correctly" is not a criterion. "`SUM(token_estimate)` query returns under 50ms p95 on 100k-row session" is.
- **Honor explicit compatibility direction.** If the current instructions rule out backward compatibility and the issue introduces a breaking shape, scope it as "update all call sites", not "add a compatibility shim".
- **Rules-driven boxes**: when an issue touches a domain with rules in `.agents/rules/<x>.md`, fold the relevant rules into the acceptance criteria so they cannot be forgotten in implementation. Examples: chat changes must keep hot reads through Valkey caches; agents changes must populate `token_estimate` at INSERT; UI changes must use the theme system + responsive breakpoints + `useDocumentTitle`.

## Renaming existing issues

When asked to rename to follow the convention:
```bash
gh issue edit <num> --title "[TYPE] Domain: new title"
```
Apply the title convention above to both issues and PRs.

## Working backwards from a screenshot

If the user shares a screenshot showing a bug or feature request:
1. Inspect the image with the available image viewer.
2. Recon the relevant code path.
3. Draft the body with concrete pointers.
4. Create the issue.
5. Tell the user how to attach the image (gh limitation).

## Defaults summary

| Field | Default |
|---|---|
| Repo | `uniffy-io/uniffy` |
| Project | `V1 Roadmap` (org project number 3, owner `uniffy-io`). New issues join it automatically; never run `item-add`. Effort lives there as `Size` (XS to XL) and `Estimate` (working days), set only when asked |
| Native dependency | Use `addBlockedBy` GraphQL when one issue blocks another |
| Image attach | Tell user to drag-drop in browser (gh limitation) |
