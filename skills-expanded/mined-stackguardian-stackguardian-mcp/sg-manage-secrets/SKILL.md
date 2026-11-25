---
name: sg-manage-secrets
description: Guided flow for creating, rotating and deleting StackGuardian vault secrets with the create_secret / update_secret / delete_secret tools, and for wiring the resulting '/secrets/<name>' or '${secret::<name>}' reference into a workflow. Use when the user wants to store a credential, token, password, SSH key or API key for workflows to use, rotate an existing secret, remove one, or when create_workflow / update_workflow reports a missing secret.
---

# Manage Secrets — Guided Flow

A StackGuardian secret is an org-wide, KMS-encrypted vault entry with a
name and a value. It has no description, tags or type, and its value can
never be read back. Workflows use it by reference. Follow the steps IN
ORDER. Never surface parameter names like `resourceName` or `secret.value`
to the user; speak of "the secret's name" and "the value".

## Handling the value

- Ask the user to paste the value once, then pass it to the tool
  immediately. Do not repeat it back, summarise it, or store it anywhere
  else in the conversation.
- Pass it verbatim: whitespace and newlines are preserved. An SSH private
  key must keep its trailing newline. Other multiline material (JSON,
  certificates for some step types) is safer base64-encoded — the tool warns
  when a value is multiline or contains `$name`, which the Terraform step
  would expand.
- The tool never returns the value. If the user later asks what a secret
  contains, say the platform cannot read it back; they can only rotate it.

## Step A — Create

1. Ask for a name: letters, digits, `_` and `-` only, up to 71 characters,
   case-sensitive (`API_KEY` and `api_key` are different secrets). Suggest
   an upper-snake-case name that matches how it will be used.
2. Call `create_secret(resourceName=<name>, secret={"value": <value>})`.
3. On `nameTaken`, ask whether the user wants to rotate the existing secret
   (→ Step B) or choose another name. On a case-only-collision warning,
   confirm they really want two distinct secrets.
4. Relay `warnings` in plain language and hand back the two reference forms
   from the response:
   - `secretId` (`/secrets/<name>`) for a workflow environment variable
     (`environmentVariables: [{"varName": "X", "secretId": "/secrets/<name>"}]`
     in `create_workflow` / `update_workflow`), git source `gitAuthRef`,
     policy git `auth`, private docker image auth.
   - `interpolation` (`${secret::<name>}`) inside a plain-text env var
     value, IaC input, webhook secret or approval-webhook secret.
5. If `search_orchestrator_resources(resourceTypes=['SECRET'])` does not
   show it right away, that is indexing lag, not a failure.

## Step B — Rotate

1. Find the exact name: `search_orchestrator_resources(resourceTypes=['SECRET'],
   searchQuery=<hint>)`, or use the `availableSecrets` list a tool error
   returns. Names are case-sensitive.
2. Ask for the new value and call
   `update_secret(resourceName=<name>, secret={"value": <value>})`.
3. Tell the user: workflows pick up the new value at their next run; runs
   already in progress keep the old one. Only ADMIN or OPS roles can rotate;
   a 403 means the caller's role cannot.

## Step C — Delete

1. Call `delete_secret(resourceName=<name>)` WITHOUT `confirmDelete` first.
   The error response carries `referencingWorkflows` (workflows whose
   plain-text env vars mention the secret) and `sweepCoverage`.
2. Show the user the list and say plainly that the sweep cannot see
   `VAULT_SECRET` env vars, git/policy/docker auth pointers or IaC inputs,
   so they should check those themselves. Deleting is permanent and every
   workflow still referencing the secret fails at its next run.
3. Only after an explicit yes, call
   `delete_secret(resourceName=<name>, confirmDelete=true)`.

## Wiring a new secret into a workflow

After Step A, if the user's goal was "use this in workflow X", continue with
the `sg-update-workflow` skill (environment variables) or `sg-create-workflow`,
passing the `secretId` form. `create_workflow` verifies the reference
exists and, if not, names `create_secret` in its error — that is the
signal to come back to Step A.
