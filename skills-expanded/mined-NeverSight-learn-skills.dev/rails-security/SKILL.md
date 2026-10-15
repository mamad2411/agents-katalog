---
name: rails-security
description: "Run a multi-agent security review of Rails application code. Use when the user asks for a Rails security review or audit, or raises a specific concern — authorization/IDOR/tenant isolation, XSS/SQL injection/SSRF, vulnerable gems/Brakeman/bundle audit, or prompt injection in AI features."
---

## Boundaries

Review Rails application code as it runs in development: the repository plus commands you can run locally — `bin/rails routes`, `bundle exec brakeman`, `bundle audit`, the test suite. Server, cloud, container, CI, and network configuration are out of scope; when a finding depends on them, note the dependency and move on.

The whole workflow inspects and reports. No agent edits reviewed files, applies patches, commits, or begins remediation. Reproduce claims only with non-mutating commands. Review only code the user owns or is authorized to audit.

## Confirm agents

Run every lens as a blind agent: fresh context, no prior conclusions, no lens passes in the delegator context. Use the runtime's native subagent abstraction. When no mechanism can create blind agents, stop and return an execution-unavailable response naming the missing capability.

Complete this step when one mechanism can create a blind agent per lens.

## Resolve scope

Resolve explicit scope first. Otherwise resolve, in order: pending changes against `HEAD` including staged, unstaged, and relevant untracked files; a branch from its merge-base; an associated pull request; a recent commit. When the user asks to audit the app rather than a change, the scope is the whole application: `app/`, `lib/`, `config/`, `db/`, routes, and lockfiles.

Complete this step when the exact diff, range, or file set can be stated.

## Select lenses

Each lens is one rubric file in `references/lenses/`:

- `access-control` — authentication, authorization, tenant isolation, sessions, CSRF, webhooks
- `injection` — SQL, XSS, command, SSRF, file paths, deserialization, redirects, headers
- `dependencies` — Brakeman, bundle audit, importmap/npm audit, version and advisory triage
- `ai` — prompt injection, tool abuse, RAG leakage, unsafe model output

Honor explicit lens names before named sets before the default set. Accept `simple` and `lightweight` as aliases for `quick`.

```yaml
quick:
  - access-control
  - injection
default:
  - access-control
  - injection
  - dependencies
full:
  - access-control
  - injection
  - dependencies
  - ai
```

Add `ai` to any set when the scope contains LLM, agent, embedding, or model-tool code (a grep for the patterns in `references/lenses/ai.md` decides); when `full` was selected and that grep finds nothing, drop `ai` and record why under coverage. Load only the selected lens files.

Complete this step when the selection has one interpretation.

## Run the quorum

Give every lens an identical task packet — scope, changed files, stack (Rails/Ruby versions, auth and authorization libraries), read-only flag, finding contract — plus its one lens rubric. Require every finding to carry: title, `file:lines`, severity, claim, trigger, impact, evidence, fix. Create one blind agent per lens, concurrently when capacity allows, sequentially otherwise. Where the worker mechanism offers acceptance gates, disable them: the lenses are the acceptance layer.

Wait for every lens to return, fail, or time out. A missing lens contributes only a coverage limitation — never agreement or a clean bill. Return an execution failure when no lens returns a usable result.

Complete this step when every selected lens has a usable result or a recorded failure reason, and at least one usable result exists.

## Synthesize and verify

Merge findings by root cause. Remove speculative, style-only, and — for diff scopes — pre-existing claims the change does not touch. Trace every critical and high finding through source, safeguards, and tests; reproduce when proportionate with a failing request spec, `rails runner` read, or request against a development server. Assign each finding `verified`, `unverified`, or `rejected`, recording the method.

Complete this step when every finding is merged, verified, held as an open question, or rejected.

## Report

Severity meanings:

- `critical`: exploitable as written — auth bypass, cross-tenant read/write, remote code execution, committed production secrets.
- `high`: dangerous sink or missing control on sensitive data or actions, likely exploitable.
- `medium`: missing abuse control, weakened defense-in-depth, or absent tests on a sensitive denied path.
- `low`: minor hardening or worthwhile improvement.

Render the report exactly in this template — each section once, in this order, omitting Consider and Open questions when empty:

```markdown
## Verdict

<One sentence: for a diff, **Merge**, **Merge after fixes**, or **Do not merge**; for an app audit, the overall posture — with the deciding reason.>

Scope: <range or app · files> · Lenses: <usable/selected> (<mechanism>)

## Do next

- [ ] `path/to/file:lines` — <imperative action> (finding 1)

## Findings

### 1. <Concrete failure in plain words> — <severity>

- **Where:** `path/to/file:lines` — <function or block name>
- **What:** <claim and trigger, at most two sentences>
- **Impact:** <who gains what access or capability, one sentence>
- **Fix:** <one imperative sentence>
- **Verification:** <verified/unverified · method>

## Consider

- `path/to/file:lines` — <one-line low-severity suggestion>

## Open questions

- <Unverified claim> — <the evidence that would settle it>

## Coverage

<Lenses dropped or failed, out-of-scope dependencies noted, limitations — two or three lines.>
```

Do next lists every verified critical and high finding ordered by severity, one imperative line each; findings are numbered in Do next order. Every Do next item and finding carries an exact `file:lines` location — when a lens supplied only a file or block name, resolve the line numbers from source before reporting.

Complete this step when the report matches the template and every finding has a severity, verification status, `file:lines`, and one-sentence fix.
