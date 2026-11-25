---
name: sg-create-policy
description: Guided flow for creating (and adjusting) a StackGuardian policy with the create_policy / update_policy tools — walks the user through scope (which workflows), the rule source (inline Tirith document, marketplace policy template, or a git repo of Rego/Tirith), the verdict mapping (block / warn / require approval), and approvers, then creates the policy. Use when the user wants a guardrail, a policy, a compliance check on Terraform plans, a cost limit, or an approval gate on infrastructure changes.
---

# Create Policy — Guided Flow

Create a StackGuardian policy with the `create_policy` tool.
Follow the steps IN ORDER. Never ask the user to type ids from memory —
fetch options with the listed tools and present choices. In user-facing
messages use plain language; never surface parameter names like
`enforcedOn`, `onFail`, `policyInputData`.

A policy is a named set of RULES. Each rule checks one thing (a Tirith
document, a Rego repo, or a marketplace template) and says what happens
when it trips. The policy as a whole is attached to a SCOPE.

## Step A — What should the policy check?

Ask what the user wants to enforce. Map it to a rule source:

1. **Marketplace template** (first choice when one fits): call
   `search_marketplace_templates(templateType='IAC_POLICY', searchQuery=<topic>)`
   and `get_subscription(['IAC_POLICY'])`. Present names + descriptions;
   the pick's pinned `ResourceId` ('/owner/name:N') becomes
   `{"type": "template", "templateId": ...}`. Always pin a numeric
   revision.
2. **Inline Tirith document** for a specific Terraform-plan or cost check
   the user describes (e.g. "S3 buckets must be private", "EC2 monthly cost
   under 100"). Build `{"type": "inline", "document": {...}}` with
   `meta.required_provider` = `stackguardian/terraform_plan` (plan checks)
   or `stackguardian/infracost` (cost checks); evaluators with a unique
   `id`, `provider_args`, and a `condition` from Equals / NotEquals /
   ContainedIn / NotContainedIn / Contains / NotContains / GreaterThan /
   GreaterThanEqualTo / LessThan / LessThanEqualTo / IsEmpty / IsNotEmpty /
   RegexMatch; and an `eval_expression` over the ids. Show the user the
   check in words before calling.
3. **Git repository** of Rego (`kind: OPA_REGO`, needs `opaQuery`, e.g.
   `main.allow` — never `data.main.allow`, never `main.deny`) or a
   `tirith.json` (`kind: SG_POLICY_FRAMEWORK`). Ask whether the repo is
   private; if so, the credential is a connector or secret POINTER —
   offer the org's VCS connectors (the tool returns `availableVcsConnectors`
   on a miss). Never put a raw token in `auth`.

Rule `name` is a slug (letters, digits, `_`, `-`).

## Step B — What happens when a rule trips?

Ask per rule and set `onFail`:
- "block the deployment" → `FAIL`
- "just warn" → `WARN`
- "pause for someone to approve" → `APPROVAL_REQUIRED` → go to Step D
Leave `onPass` as `PASS` unless the user explicitly wants otherwise.

## Step C — Where does it apply?

Offer exactly these options and set `enforcedOn`:
- **Whole organization** → `["*"]`. Confirm explicitly: it applies to every
  workflow and stack.
- **Workflow group(s)** → resolve with
  `search_orchestrator_resources(resourceTypes=['WORKFLOW_GROUP'], searchQuery=...)`;
  pass the ResourceName or the last segment of the ResourceId. Nested
  groups are covered by their parent.
- **Specific workflow(s)** → `search_workflows(searchQuery=...)`; pass the
  full `/wfgrps/<group>/wfs/<workflow>` path (a bare workflow name never
  matches).
- **Cloud connector(s)** → `/integrations/<connector>`: every workflow
  deploying through that account/subscription/project.

`enforcedOn` is required; never default it silently.

## Step D — Approvals (only if any rule uses APPROVAL_REQUIRED)

Ask who may approve (user emails) → `approvers`, and how many must
approve → `numberOfApprovalsRequired` (0 means all of them). Both are
required together. Note to the user: an approval that fires on a
workflow's last step is skipped by the platform, so plan-only workflows
never pause.

## Step E — Name, describe, create

Ask for a name (letters, digits, `_`, `-`; it becomes the permanent id),
an optional description and tags. Before calling `create_policy`, check
`search_policies(searchQuery=<name>)` for duplicates. Then call
`create_policy(resourceName, rules, enforcedOn, description, tags,
approvers, numberOfApprovalsRequired)`.

Relay the response's `summary` sentences and `warnings` to the user in
plain language. On an error with an `available*` list, present the options
and re-call — never guess.

## Adjusting a policy later

Use `update_policy(policyId, ...)`:
- change scope: `addEnforcedOn` / `removeEnforcedOn` (or `enforcedOn` to
  replace the whole scope);
- change rules: `addRules` / `replaceRules` (by rule name) / `removeRules`;
- change approvers: `approvers` + `numberOfApprovalsRequired` together;
- rename / describe / tag: `resourceName`, `description`, `tags`.
The response's `changed` map shows exactly what moved. Find the policy
first with `search_policies`.
