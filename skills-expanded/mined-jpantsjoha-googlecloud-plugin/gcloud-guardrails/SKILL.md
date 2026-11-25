---
name: gcloud-guardrails
description: "Command-level safety rules for every gcloud CLI call an agent plans, proposes or runs: validate leaf syntax with gcloud help, dry-run first, reduce output, scope project and location explicitly, run one command at a time, and stop for human authorisation on a fixed denylist (IAM changes, deletes, billing, organizations, KMS, IaC apply, API enablement, CLI installation). Applies alongside every service skill. Does not cover client-library code or raw REST calls. Use this for how a gcloud command is built and executed; use gcp-security instead to review a design's security posture. Use when the user mentions: gcloud command, run gcloud, gcloud syntax, gcloud flags, gcloud dry run, validate gcloud, gcloud safety, destructive gcloud."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "gcloud command, run gcloud, gcloud syntax, gcloud flags, gcloud dry run, validate gcloud, gcloud safety, destructive gcloud"
  "googlecloud-plugin/required-scopes": ""
  "googlecloud-plugin/mcp-servers": "gcloud"
---

# gcloud Guardrails

The command-level half of [ADR-004](../../architecture/decisions/ADR-004-safe-by-default-billable.md). Service skills say *what* to run; this skill says *how* any `gcloud` command is built, checked and executed. It applies whether the command runs in a local shell or through the `gcloud` MCP server's `run_gcloud_command` tool.

Remembered `gcloud` syntax is stale. Commands, flags and flag values change between SDK releases, and a plausible flag that no longer exists is the most common agent failure with this CLI.

## The four-step plan

Every `gcloud` task, whether executed now or written up as a plan, follows these steps in order. A plan that omits step 1 is incomplete.

1. **Validate syntax** — run `gcloud help <group> <resource> <verb>` on the exact leaf command. Help on a parent group (`gcloud help compute`) does not validate a leaf.
2. **Verify parameters** — confirm required flags, the flags the user named, and whether the command supports `--dry-run` or `--validate-only`.
3. **Dry run** — if either flag is supported, run it before the real command and show the result.
4. **Classify, then propose or execute** — see *Authorisation* below. Read-only commands run under the execution rules. Everything else is proposed with its effect and waits for a named human to authorise it.

`gcloud help` is the authority for syntax. Do not substitute web search or recall. Use the Developer Knowledge MCP for *concepts* (which service, which role), not for flag spelling.

## Execution rules

| Rule | Why |
|------|-----|
| One `gcloud` command per call. No `&&`, `;`, pipes, redirection or `$(...)`. Through the `gcloud` MCP server, pass `args` as an array without the leading `gcloud` (`["run", "services", "list", "--project=PROJECT_ID"]`). | Each step must be inspectable and its exit code attributable. |
| Pass `--project=PROJECT_ID` on every project-scoped command, using the project settled by `gcp-project-context`. Never rely on the active configuration. Commands that act on no session project need none: `help` and `--help`, `config`, `auth`, `components`, `info`, `init`, `meta`, `topic`, `version`; and `projects`, `organizations` and `billing`, which name their target explicitly (a project ID, organization or billing account) rather than using a session project. Changes to billing and organizations remain on the `gcloud-guardrails` denylist. | The active project is ambient state the user may not be looking at, and on a multi-project machine it is often not the one they mean. |
| Pass the location flag (`--region`, `--zone`, `--location`) the resource needs. | An omitted location triggers an interactive prompt, which hangs a non-interactive agent. |
| Add `--quiet` to commands that would prompt, only once the command is read-only or authorised, and never to a denylisted command. | `--quiet` accepts defaults, including "yes" to destructive prompts. It is never a way round authorisation. |
| Add `--async` to long-running operations that support it, then poll with `describe`. | Avoids tool-call timeouts on cluster or instance creation. |
| Preserve every flag the user specified in each proposed command. | Dropping `--project` or `--impersonate-service-account` silently retargets the command. |

If a location is unknown, discover it read-only first (for example `gcloud run services list --project=PROJECT_ID --format="value(metadata.name,region)" --limit=20`), then ask the user if more than one candidate remains.

## Data reduction

Unbounded output exhausts the context window and hides the answer. Every `list` and every `describe` of a large resource carries at least one of:

- **Projection** — `--format="json(name,status,createTime)"` or `--format="value(name)"`
- **Limit** — `--limit=N`
- **Server-side filter** — `--filter="status=RUNNING AND labels.env=prod"`

Never run a bare `list`. To learn a resource's field names before projecting, fetch one record: `gcloud <group> <resource> list --project=PROJECT_ID --limit=1 --format=json`.

## Authorisation

Permission is decided by what a command does, not by how it is spelt. The default is **stop and ask**.

| Class | Examples | Rule |
|-------|----------|------|
| **Read-only** | `help`, `list`, `describe`, `get-iam-policy`, `config list`, `logging read`, `--dry-run`, `--validate-only` | Run under the execution rules. |
| **Consequential** — anything that creates, changes, stops, removes or bills | `create`, `deploy`, `update`, `patch`, `set-*`, `stop`, `reset`, `resize`, `rm`, `remove`, `disable`, `import`, `apply` | Propose the exact command and its effect, then wait for a named human to authorise it. |

When unsure which class a command is, treat it as consequential. A cost-warning comment or a successful dry run is information for the human, not approval. Authorisation covers the exact command shown; a changed flag needs a fresh yes.

## Denylist — never autonomous, never `--quiet`

These are consequential commands with outsized blast radius. In addition to the rule above: never chain them into a plan as a step that "will run", never add `--quiet` to them, and route IAM changes through the `iam` skill and the security gate.

| Command pattern | Risk |
|-----------------|------|
| Any IAM change: `add-iam-policy-binding`, `remove-iam-policy-binding`, `set-iam-policy`, `iam roles create/update`, `iam service-accounts keys create` | Privilege escalation or lock-out. Route through the `iam` skill and the security gate. |
| `gcloud * delete`, `gcloud storage rm`, any other remove or purge | Irreversible destruction. |
| `gcloud billing *` | Service disruption or unbounded cost. |
| `gcloud organizations *`, `gcloud resource-manager folders *` | Changes reach every project beneath. |
| `gcloud kms *` (destroy, disable, rotate) | Can make data permanently unreadable. |
| `gcloud infra-manager deployments apply` | Autonomous IaC change with no review. |
| `gcloud services enable` | Enabling an API can start billing. Assume needed APIs are on; if a call fails with a disabled-API error, report it and ask. |
| Installing or updating the `gcloud` CLI or its components | Host modification. Ask first. |

Billable creates that are not on the denylist (a Cloud Run deploy, a VM) still need authorisation, and the proposal carries the ADR-004 comment and cost warning:

```bash
# Billable action — confirm cost before running
gcloud run deploy SERVICE --image=IMAGE --region=REGION --project=PROJECT_ID --quiet
```

## Worked example

User: "Create a Cloud SQL Postgres instance for staging."

1. `gcloud help sql instances create`
2. Required: instance name, `--database-version`, `--tier` or `--cpu`/`--memory`, `--region`. No `--dry-run` support.
3. No dry run available — say so.
4. Consequential and billable, not on the denylist. Propose it and wait for authorisation:

```bash
# Billable action — confirm cost before running
gcloud sql instances create INSTANCE_NAME \
  --database-version=POSTGRES_16 \
  --tier=db-custom-1-3840 \
  --region=REGION \
  --project=PROJECT_ID \
  --async
```

Then `gcloud sql operations list --instance=INSTANCE_NAME --project=PROJECT_ID --limit=1 --format="value(name,status)"` to track it.

## References

- `references/upstream.md` — provenance of these rules
- Google Cloud SDK reference: https://cloud.google.com/sdk/gcloud/reference
