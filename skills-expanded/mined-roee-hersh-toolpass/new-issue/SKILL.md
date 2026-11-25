---
name: new-issue
description: Write and open a well-scoped GitHub issue for toolpass (an integration, a feature, a good first issue or a bug). Use when asked to open, draft or suggest issues.
---

# Writing a toolpass issue

Argument: the idea, e.g. `/new-issue Linear integration` or `/new-issue 3 good first issues`.

## Before writing

1. Search open and closed issues for duplicates. If one exists, link it instead of opening a new one.
2. Read the parts of the repo the issue touches, so every name in the issue is real: action names from
   `toolpass catalog <integration>`, resource forms from `docs/integrations/<name>.md`, file paths that
   exist. Never invent an API endpoint; if unsure how the vendor exposes something, say so in the issue.
3. For a batch ("3 good first issues"), pick work that is small, self-contained and useful now
   (docs, examples, tests, a missing action), not the hardest items on the roadmap.

## Shape

Title: `Integration: <Product>`, or an imperative summary (`Helm chart`, `Example: calling toolpass from an MCP tool`).

Body, in this order, leaving out sections that do not apply:

- **Goal**: one or two sentences on the question toolpass should answer or the thing a user gets
  ("may this user acknowledge incidents on this service").
- **How**: the vendor API calls that answer it for a *named user*, and how the email maps to the
  vendor's identity. Say which cases must be `unknown` (conditions, missing scopes, info the
  credential cannot see); `deny` only when the system positively says no.
- **Credential**: the read-only credential and the minimum scopes, and what a narrower credential
  cannot see.
- **Resources**: the `type:id` forms and the actions, following existing integrations' naming.
- **Scope** for non-integration work: a short bullet list of what is in and what is out.
- A link to [docs/development/integration-authoring.md](https://github.com/roee-hersh/toolpass/blob/main/docs/development/integration-authoring.md) for
  integrations: docs page, fake-upstream tests, vendor API description in `test/specs/fetch.sh`.
- For roadmap integrations, a line linking the epic (#19).

Keep it short enough to read in a minute. No marketing language.

## Labels

- `integration` for a new system; `good first issue` + `help wanted` for small, well-scoped work a
  newcomer can finish without deep context; `bug` for defects.

## Opening

Open the issue with the GitHub tools (not a local file), end the body with the Claude Code
attribution footer, and reply with the issue link and a one-line summary per issue.
