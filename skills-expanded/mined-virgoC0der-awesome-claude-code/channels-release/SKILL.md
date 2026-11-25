---
name: channels-release
description: Create and publish verified normal Release Train tickets for AfterShip Feed, AfterShip Affiliates, and Listing/Platform Products services through clime. Use when the user asks to release or deploy one of these domains to staging and/or production. Do not use for hotfix, rollback, or restart tickets.
---

# Channels Release

Create a normal `release` ticket from live CMDB, Release Train, and App Center data. Preserve the user's exact service, environment, and version scope. Creating a draft, publishing a ticket, and completing an actual deployment are separate outcomes.

Read [references/profiles.md](references/profiles.md) after the requested domain or service is known. Use its product and checklist mappings as exact-match hints, not as authority over live data.

## Hard boundaries

- This workflow is for `release` only. Route hotfix, rollback, and restart requests to the generic `rt-create-ticket` skill.
- Never add production because a tag is a release tag or because a prior ticket included production. Only an explicit user request authorizes a production task.
- A staging-only request must produce only staging deploy and staging rollback tasks. After creation and publication, require `has_production_env=false` on readback.
- Do not infer a product from a service name. `prod-af-mcp-server` belongs to `AfterShip Feed`, not `AfterShip Affiliates`.
- Never fuzzy-match a service, environment, artifact, product, or checklist. A missing or ambiguous exact match is blocking.
- Do not claim a service is deployed merely because the Release Train ticket was published. Confirm an App Center publish record for the ticket/task and wait for `status=success`.

## Preflight

Run:

```bash
which clime
clime release-train version
clime app-center version
clime release-train auth status --output json
clime app-center auth status -O json
```

Require `release-train >= 1.0.3` and `app-center >= 1.1.0`. Older App Center versions can accept `-r` but fail artifact queries with `ListArtifactsInput.CIName ... required`; the working artifact selector is `-c <ci-name>`.

If a CLI is missing, outdated, or logged out, stop and tell the user. Do not install, replace, update, or log in without their approval. The current official manifest is `https://files.am-usercontent.org/AfterShip-CLI/common/plugins.yaml`; do not silently reuse obsolete `.me/.../common/install.sh` sources.

## Inputs

Collect only fields that cannot be recovered reliably:

- requested domain or exact service name;
- exact environments and version/tag for each service;
- JIRA issue IDs;
- co-editor emails.

Use the current Git identity only as a proposed co-editor when it is an `@aftership.com` address and a recent same-product ticket used the same address. Surface the inferred value in the dry-run.

Never invent a JIRA key. A PR or tag without a JIRA key may be associated with a Jira issue only when current Jira search and the release content give one unique, strong match; otherwise ask.

## Resolve live data

### Product and Jira

Use the profile product name/ID only when the live App Center CD result returns the same `product_name`. Otherwise resolve exactly:

```bash
clime cmdb product list --name '<product-name>' --output json
clime release-train jira summary <ISSUE_ID...> --output json
```

Use CMDB `acid` as `product_id`. Build `jira_issues`, `reason`, `prd`, and `jira_ticket_change_log` from the Jira response.

### Service, environment, artifact, and rollback

For every service:

```bash
clime app-center cd list -n '<service>' -O json
clime app-center ci list -s '<service-or-repo>' -O json
clime app-center env list -a '<service>' -O json
clime app-center artifact list -c '<ci-name>' -i '<version>' -O json
clime app-center publish list -a '<service>' -e '<environment>' -O json
```

Required checks:

- CD name is an exact unique match, `application_id > 0`, and `is_release_controlled=true`.
- Environment name and `env_category` both equal the requested environment.
- Artifact selection uses an exact equality check on `image_tag` or `github_tag`; do not trust `-i` to filter the returned page by itself.
- Artifact `status=success`, ID is positive, commit is non-empty, and the tag/version is exact.
- Rollback uses the newest successful publish record for the same service and environment.
- Every deploy task has exactly one rollback task with the same application and environment.

Artifacts, publish records, checklist templates, and staging/production environment properties are always live data. A `.ci-cd.yaml` or personal App Center cache may skip stable ID discovery only; it must not decide release control, environment scope, artifact, rollback, or checklist contents.

## Checklist selection

Query current templates every time:

```bash
clime release-train ct list --product-id=<product_id> --output json
```

For a normal release, require:

- pre-release: at least one `security`, `qa`, `po`, and the relevant `fe` and/or `be` segment;
- post-release: at least one relevant `fe` and/or `be` segment.

Use the profile's preferred exact names only when the live template is `reviewed_status=pass`, unexpired, and has the expected segment/stage. Copy current `todo_name`, `description`, and `owners`; never copy old ticket todos.

Do not select templates containing `紧急`, `hotfix`, or `do not use` for a normal release. For mixed FE/BE services, include both relevant pre-checks and both relevant post-checks when available.

`qa-hotfix-approval-list` is hotfix-only. For this normal release workflow, use:

```json
{"qa_approval":{"approvers":[]}}
```

Also keep `approval.approvers=[]`.

## Build and validate the payload

Use `clime release-train ck release --show-example` as the current payload-shape authority; draft creation accepts the same structure. Populate all values from live results. Set:

- `release_type=release`;
- `name=<product_name> - release - <YYYYMMDD>`;
- `has_tasks=true`;
- `is_duplicated=false`;
- deploy tasks' `images[]` from the target artifact;
- rollback tasks' `images[]` from the latest same-environment successful publish.

Write two-space JSON to `/tmp/rt-ticket-<timestamp>.json`, then run the validator using its absolute path from this skill directory:

```bash
python3 <skill-dir>/scripts/validate_ticket.py /tmp/rt-ticket-<timestamp>.json --allowed-env staging
```

Pass one `--allowed-env` flag per explicitly requested environment. Never add `production` to this command unless the user explicitly requested production.

## Confirmation and execution

Before creating, show:

- product, ticket type/name, Jira, co-editors;
- exact service/environment/version/artifact/commit;
- exact rollback service/environment/version;
- checklist names and QA approval;
- whether any production task exists;
- the full JSON path and exact create command.

Accept only `yes`, `y`, `确认`, `确定`, `ok`, or `执行`. Then run in a TTY because the CLI has its own `Confirm? [y/N]` prompt:

```bash
clime release-train ck create --from-file /tmp/rt-ticket-<timestamp>.json --output json
```

Send `y` only after the user's explicit confirmation. After a successful creation, always return the ticket ID and this clickable canonical App Center URL, even when the CLI response has an empty `jira_ticket_url`:

```text
https://app.automizely.org/v2/release-train/tickets/detail?id=<ticket_id>
```

Read the ticket back and verify the service/version/environment and production flag. Include the same URL again after a later publish result.

Creating a draft does not authorize publishing it. Ask separately. After an explicit publish confirmation, run in a TTY and answer the CLI confirmation:

```bash
clime release-train ck publish --product-id <product_id> --ticket-id <ticket_id> --output json
```

Read back the ticket. `is_draft=false` and `status=ready to deploy` mean the ticket was published, not that deployment succeeded. Check App Center:

```bash
clime app-center publish list -a '<service>' -e '<environment>' -O json
```

Report separately: ticket published, deployment record created, deployment in progress, or deployment succeeded.

In the verified `release-train 1.0.6` CLI, `ck publish` submits the ticket but does not expose a command that starts an App Center deployment. If the ticket is `ready to deploy` and no matching App Center publish record exists, stop and report that boundary. Only operate the Release Train/App Center UI when the user explicitly asks to continue the actual deployment.

## Failure handling

- Preserve complete CLI error text and the exit code.
- Do not retry a mutation with guessed IDs or a different environment.
- If an interactive command stopped at its confirmation prompt without a ticket ID/success line, it did not prove success; rerun in a TTY only under the existing user confirmation.
- After a successful full resolution, refresh the personal service cache with non-sensitive stable IDs. Never cache artifacts, publish records, checklist data, secrets, or credentials.
