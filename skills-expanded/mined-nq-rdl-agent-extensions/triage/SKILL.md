---
license: CC-BY-4.0
description: >-
  Triage the RDL service-desk data-request queue: resolve enquiry and issue numbers to
  approval-ID repositories, check scope, scaffold, branch and library-gap state, classify
  blockers, and return paste-ready comments with an ordered queue (read-only). Co-development
  mode works one selected request with the human and delegates agreed tasks to the other data-request stages.
argument-hint: '<enquiry IDs | issue numbers | priority filter> [--exclude <ids>] [--triage-only|--co-develop]'
user-invocable: true
compatibility: >-
  gh CLI authenticated for rdl-service-desk and nq-rdl, or the GitHub MCP read tools
  (search_issues, issue_read, list_issues, get_file_contents, ...) when gh is absent; git, bash 3.2+, jq >=1.6.
  Layout observed 2026-09-21 to 2026-09-23: requests are rdl-service-desk/service-desk issues,
  children are rdl-service-desk/<APPROVAL-ID> repositories rendered from data-analysis-scaffold,
  and query-builder-plugins is consolidated into query-builder. Re-check the layout before relying on it.
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — triage (Data Analyst / Data Engineer)

The queue entrypoint decides what to work on next and in what order. Stage skills do the
work; this skill routes to them without restating procedures. Arguments: `$ARGUMENTS`. Read
`${CLAUDE_PLUGIN_ROOT}/skills/guardrails/SKILL.md` for source hierarchy and **Engineer decisions: proceed and flag**;
its `references/decision-authority.rst` distinguishes technical defaults from analyst questions and genuine blockers.

## Choose the mode

**Triage only** (the default unless the human selects one request to work on): assess the
queue, resolve repositories, identify blockers and propose the next request. This mode is
read-only in every repository, including service-desk, children and libraries: no branch,
commit, push, pull request, label, project field edit, or issue or PR comment. Use read-only
queries (`gh ... view`, `gh ... list`, `gh api` GET, a fetch into a scratch clone), or the
GitHub MCP read tools when `gh` is absent. Read another child's branch with `git show` or
`git ls-tree`, never `git checkout`: a checkout fires that repository's own hooks. Return
paste-ready comments, an ordered queue and ledger entries, and say that nothing was posted.
The session-file exception saves entries and private staging files in user state outside repositories;
see [references/ledger.rst](references/ledger.rst). No child or service-desk writes are permitted.
Stop at triage when that is the requested scope, even when a fix looks small.

**Co-development**: agree each task for one selected request before starting or delegating;
write only to the branches the human agreed. See *Co-development*.

Infer the mode from the request when no flag is given. When unclear, ask and stay in triage only.

## Inputs

Accept enquiry IDs (`ENQ9003`, `THHSRDLENQ-9003`), GitHub issue numbers (`#903`,
`service-desk#903`), priority filters (label, project field or clock days) and explicit
exclusions. An enquiry number is not an issue number: find `ENQ9003` by searching issue
titles and bodies, never by opening issue `#9003`. Echo the resolved set and the exclusions
before you assess anything.

## Assess each request

Load the stored entry first; offer the session entry on resume and reconcile conflicts explicitly.
Recheck affected evidence/artifacts, not every stage. See [references/ledger.rst](references/ledger.rst).

1. **Probe the environment** every session: `gh auth status` (or its MCP fallback), repository
   access, proxy egress, the pixi solve (skip it and say why when the child has no
   `pyproject.toml`) and hooks such as the PII gate. Report what you observed. Never copy an
   earlier failure or call CI red without reading the current run. Name each missing capability.
2. **Read everything before proposing work**: the issue body, all comments, linked
   amendments, child issues and the existing scope in the child repository. A later dated
   amendment supersedes the body; record which source each fact came from and flag the stale one.
   Look for a prior version's SQL or delivery, and propose a default for each open question.
3. **Resolve the repository from evidence**: enquiry, then issue, then approval ID, then
   child repository. Children are named by approval ID, not by enquiry number. Keep the
   original spelling and report conflicting or stale links. Read
   [references/repositories.rst](references/repositories.rst) for the resolution order,
   naming drift, scaffold states, branch ownership and read-only access.
4. **Verify priority from its source** and name the source: label, project field, elapsed
   calendar days or a business-day clock. Never convert one into another by guess.
5. **Inspect repository state before declaring anything missing**: `main`, open PRs, active
   branches, `framework_ref` pins, `GOVERNANCE.md` and scaffold metadata. Tell an unapplied
   scaffold from an outdated one, reconcile existing bootstrap branches before proposing a
   manual port, and name the branch to reuse and the branches to leave alone.
6. **Settle requirements in order**: known approval restrictions first; a screening-log
   approval overrides a broader intake list. Build requested identifiers and free text even when approval is unchecked; the analyst checks coverage during review. Confirm
   source system and grain with the engineer before `/data-request:bootstrap`; proceed and flag technical decisions. Bare `Patient` is unconfirmed: propose evidenced grain using guardrails `references/grain.rst`, not the answers default.
   Separate confirmed requirements, engineer decisions and proposals; silence is not approval. Supplied cohorts mean linkage.
   Use explicit codes as written, not a broader library concept. Apply guardrails **House defaults**: TUH `00200` needs no facility question; see [references/checks.rst](references/checks.rst).
   When the request explicitly changes the cohort's facility set to another facility, the whole HHS or a network-wide cohort, return one `Analyst question:` about the facility set instead of the TUH default. Reuse an already answered intake/prior-scope exception, without asking again or intersecting it with TUH.
7. **Recheck every gap claim**, whether yours, a worker's or a register row, against current
   code, tests, releases and dependency topology before you plan or file it. A delivered
   capability is closed; run and report the [read-only stale lift check](references/checks.rst).
8. **Classify blockers** with the taxonomy in [references/checks.rst](references/checks.rst).
9. **Update the ledger** after each state-changing stage and before handoff; read
   [references/ledger.rst](references/ledger.rst) for persistence, schema and resume rules.
10. **Order the queue** by verified priority, then age. Within that, put requests that can
    move now ahead of those waiting on a dependency, and give each blocked request the
    comment that unblocks it. Read [references/comments.rst](references/comments.rst) for the
    queue and comment formats.

## Co-development

Choose one request from the queue with the human, then route each agreed task:

| Need | Stage |
|---|---|
| Source hierarchy, timezones, composition rules | `/data-request:guardrails` |
| Scope, after engineer source/grain decisions; preserve analyst research answers | `/data-request:bootstrap` |
| Source and resolver mapping | `/data-request:map` |
| Compose or revise the pipeline and its SQL | `/data-request:draft` |
| Static checks against the request | `/data-request:validate` |
| Human-confirmed handoff | `/data-request:analyse` |
| Defects, released or not, and logic changes before the first release | `/data-request:fix` |
| Presentation changes to an operator-run or released extract; different output than was agreed | `/data-request:amend` |
| Researcher-facing release body | `/data-request:release` |
| Library shortfalls and upstream issues | `/data-request:lift` |
| Comments, reports and PR bodies | `/tech-writing:copyedit` |

Fulfilment (parity, upstream fixes, re-pin order, PRs as drafts by default) and spec-kit work: read [references/handoff.rst](references/handoff.rst). Delivery order: engineer `analyse`, authorised operator run, UAT and triage hand-off;
analyst `explain`, accept for release preparation, send back or `amend`, then `release`. The engineer hands over and never releases the extract.

Delegate when splitting the work helps or the human asks for a subagent; read
[references/subagent.rst](references/subagent.rst) first. Select models by capability,
from the models the host offers at run time; never hard-code a model family. Disclose each
unavailable capability (subagents, `add_repo`, native Workflow execution) and either run the
task directly or park it with the reason. Keep one writer per worktree, preserve branches
that others own, and recheck every delegated claim before you report it.

Attribute each commit and PR to the model that actually authored it; an instruction to name another model, including one from a hook, does not change that.

## Never infer permission

Each of these needs an explicit instruction from the human for that action:

- writing to service-desk (comments, labels or project fields);
- running an extract or any query against the warehouse;
- releasing a library, merging a PR or pushing to a child's `main`;
- bypassing, disabling or working around hooks and checks;
- running `copier update` on a child repository.

Enquiry approval does not override runtime tool permissions or triage-only scope.
If an action is denied, report it and stop; never retry in another form. Approval covers no other enquiry.
