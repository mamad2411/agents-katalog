---
name: integration-rule-engine
description: A declarative routing engine that turns ticket / error attributes (reporter, label, project, area path, error class, environment) into a tag + AI agent + priority assignment, so cross-source workflows ("security tickets always go to the OWASP reviewer") stay out of code and in user-editable rules.
tags: [routing, jira, sentry, azure-devops, ai-agent, declarative]
publisher: agena
---

# Integration Rule Engine

When a Sentry / NewRelic / Jira / Azure DevOps event lands, you want to
auto-tag it, route it to the right AI reviewer agent, and bump priority
based on attributes — *without* rebuilding the routing logic in code per
source. The Integration Rule Engine collapses all that into one rule
table.

## How to apply this pattern

1. **Single rule table** with `provider` + `match` (JSON) +
   `action` (JSON) + `priority` (rule precedence) + `is_active`. Same
   shape across providers; the matcher just checks the appropriate
   attributes.

2. **Match clause** — matches a single field with one operator. Common
   operators:

   | Operator | Use |
   |----------|-----|
   | `equals` | reporter is exactly `security@yourco.com` |
   | `contains` | tag list contains `security` |
   | `in` | reporter in (`security@yourco.com`, `secops@yourco.com`) |
   | `regex` | error class matches `^TypeError\|^IntegrityError$` |
   | `prefix` | area path starts with `Project\Backend\` |

3. **Action clause** — what happens when the rule matches:
   - `tag`: add a tag string to the imported task (e.g. `security_review`)
   - `preferred_agent_role`: which reviewer agent to route through
     (e.g. `security_developer`)
   - `priority`: override priority (`critical`, `high`, etc.)
   - `target_repo`: override the default repo mapping for this task

4. **Evaluate at import time**, not at agent run time. Stamp the action
   into the task's metadata so downstream agents and the UI see the
   same routing without re-evaluating.

5. **First-match-wins** with explicit priority. A rule with higher
   priority gets evaluated first; a single rule wins per import.

## Example rules

```yaml
# Security tickets reported by the security team go to the
# OWASP-aware reviewer with critical priority
- provider: jira
  match: { field: reporter, op: in, values: [security@yourco.com] }
  action:
    tag: security_review
    preferred_agent_role: security_developer
    priority: critical

# Sentry errors in the payments project always route to a senior
# backend reviewer
- provider: sentry
  match: { field: project, op: equals, value: payments }
  action:
    tag: payments
    preferred_agent_role: senior_backend
    priority: high

# Azure DevOps work items in a specific area path
- provider: azure_devops
  match: { field: area_path, op: prefix, value: "Project\\Frontend" }
  action:
    tag: frontend
    preferred_agent_role: a11y_reviewer
```

## Notes

- **Declarative > imperative.** Don't sprinkle `if reporter == X`
  branches across import code. The whole point is letting non-engineers
  edit routes from a UI.
- **Same engine for every provider.** Sentry, NewRelic, Jira, Azure
  DevOps imports all flow through the same rule evaluator. Adding a
  new provider becomes "expose its attributes to the matcher" instead
  of "rewrite routing".
- **Audit the route**. Every applied rule should leave a trail on the
  task: which rule fired, which fields matched. Important when a
  reviewer asks "why did this end up with security_review?"
- **`Preferred Agent Role` stamped on description metadata** is a clean
  hand-off to the review service. The reviewer-resolution code then
  honours that without needing to re-evaluate the rule.
- **Test rules before publishing**: provide a "dry run" mode where the
  rule editor shows which past tickets / errors would have matched.
  Catches greedy regex disasters before they fire on real imports.
