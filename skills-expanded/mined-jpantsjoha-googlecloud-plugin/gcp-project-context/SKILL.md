---
name: gcp-project-context
description: "Works out which Google Cloud project a task targets before any project-scoped command runs. Reads every source — exported variables (CLOUDSDK_CORE_PROJECT, GOOGLE_CLOUD_PROJECT, GCP_PROJECT_ID, GCLOUD_PROJECT), the repository's .env and .env.local, and the active gcloud configuration — then proceeds when they agree, asks the user to pick when they disagree, and tells the user how to set one when none exists. Built for machines with several projects. Only for commands that act on a project: documentation lookups, best practices, patterns, policies, designs and reviews need no project, so skip this skill for them. Use this to decide the project; use gcloud-guardrails for how each command is then built and run. Use when the user mentions: which project, gcp project, project id, wrong project, switch project, multiple projects, gcloud init, set project, project not set."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "which project, gcp project, project id, wrong project, switch project, multiple projects, gcloud init, set project, project not set"
  "googlecloud-plugin/required-scopes": ""
  "googlecloud-plugin/mcp-servers": "gcloud"
---

# GCP Project Context

## When this applies — and when it does not

Only when a command will read or change resources inside a project: `gcloud` calls such as `run services list` or `sql instances create`, Terraform plans and applies, and running code that calls Google Cloud APIs.

It does **not** apply to, and you must not ask for a project for:

- fetching or corroborating documentation (the `developer-knowledge` server, `google-skills-catalog`);
- best practices, patterns, approaches, guidelines and policies; validating assumptions;
- designs, ADRs, Well-Architected and security reviews of a plan;
- `gcloud` commands that act on no project: `help` and `--help`, `config`, `auth`, `components`, `info`, `init`, `meta`, `topic`, `version`; and `projects`, `organizations` and `billing`, which name their target explicitly (a project ID, organization or billing account) rather than using a session project. Changes to billing and organizations remain on the `gcloud-guardrails` denylist.

Most work with this plugin is in the second group. Reach for this skill at the first project-scoped command, not at the start of the conversation.

Running a command against the wrong project is the cheapest mistake to make and one of the most expensive to clean up. Settle the project once per session, before the first project-scoped command, and carry the answer into every project-scoped command as `--project=PROJECT_ID` (see `gcloud-guardrails`).

## Enforcement in Claude Code

The plugin ships a `PreToolUse` hook (`hooks/hooks.json` → `scripts/gcloud_project_guard.py`). It blocks a project-scoped `gcloud` call that lacks `--project` — through the MCP server or the shell, judging each invocation in a chained or `sh -c` command on its own flags — and returns what the sources say: one project to retry with, the choices to put to the user, or a pointer to `gcloud init`. A `gcloud` call inside a command substitution or `eval` cannot be checked and is blocked outright. `--billing-project` does not count as a project. While sources disagree, even an explicit `--project` is held until the user has chosen that project in the session: the latest message they typed, or answer they selected, that names any candidate must name exactly that one, without negation. This stops the agent settling a conflict by quietly picking the gcloud default. Shell forms the hook cannot parse but that would run `gcloud` (command substitution, `eval`, `ssh`, deep `sh -c` nesting) are blocked outright. It is a guard against shortcuts, not a security boundary: it reads the session transcript, which a process with write access to your files could alter. The hook needs `python3`; without it Claude Code reports a hook error and the call proceeds. Clients without hooks rely on this skill alone.

## Step 1 — Collect every source

Collect all of them; do not stop at the first one found. All checks are read-only.

| Source | How to read it | Who uses it |
|--------|----------------|-------------|
| `CLOUDSDK_CORE_PROJECT` | `printenv CLOUDSDK_CORE_PROJECT` | `gcloud` — overrides its configuration |
| `GOOGLE_CLOUD_PROJECT`, `GCP_PROJECT_ID`, `GCLOUD_PROJECT` | `printenv NAME` | Client libraries, Terraform, the application |
| Repository `.env`, `.env.local` | Read **only** lines whose key is one of the four names above | The application when it runs |
| Active gcloud configuration | `gcloud config configurations list --filter=is_active=true --format="value(name)"` and `gcloud config get-value project` | `gcloud`, and the plugin's `gcloud` MCP server |

Never print, copy or summarise any other line of a `.env` file: it usually holds secrets.

In this plugin's repository, `python3 scripts/preflight.py --json` collects the same sources, validates each ID and returns `resolved`, `conflict` or `missing`.

Discard a value that is not a project ID: 6–30 characters of lowercase letters, digits and hyphens, starting with a letter, optionally with a legacy domain prefix (`example.com:my-project`). An unexpanded `${GCP_PROJECT_ID}` or `(unset)` is a configuration fault to report, not a project.

With `CLOUDSDK_CORE_PROJECT` exported, `gcloud config get-value project` echoes the variable and hides what the configuration stores. Read the stored value with the variable removed: `env -u CLOUDSDK_CORE_PROJECT gcloud config get-value project`.

These discovery commands act on no project, so they take no `--project`.

## Step 2 — Decide

| Distinct valid IDs | Action |
|--------------------|--------|
| **One** | State it with its sources — "Using `my-proj` (from `.env` and gcloud config)" — and proceed. Confirm it once before the first consequential command. |
| **Two or more** | **Ask.** Show each ID with every source that names it, say which one `gcloud` would use today (`CLOUDSDK_CORE_PROJECT` if set, else the active configuration), and let the user pick. Do not guess, and do not run any project-scoped command until they answer. |
| **None** | Stop project-scoped work and tell the user how to set one (Step 4). Read-only work that needs no project can continue. |

Once chosen, the project holds for the session. If the user names a different project later, repeat Step 2 for that request.

## Step 3 — Target the choice explicitly, every time

Every project-scoped invocation names the chosen project itself; ambient configuration never decides.

- **gcloud** — `--project=PROJECT_ID` on every project-scoped command, even when the active configuration matches. The plugin's `gcloud` MCP server inherits `CLOUDSDK_CORE_PROJECT` or the active configuration, which may differ from the choice.
- **Terraform** — pass it (`-var="project_id=PROJECT_ID"`, or the variable the configuration defines) or confirm the provider block pins the same ID.
- **Client libraries and the application** — set the variable they read on the command itself (`GOOGLE_CLOUD_PROJECT=PROJECT_ID python app.py`).
- **Anything that cannot be pointed at a project explicitly** — stop, show the user which project it would use, and run it only once that matches the choice.

This sits beneath, not instead of, `gcloud-guardrails`: consequential commands still need a named human's authorisation.

## Step 4 — Help the user make it stick

Offer these; do not run them without a yes, since each changes the user's configuration:

```bash
# No project anywhere: guided setup (login, project, default region)
gcloud init

# One default project on this machine
gcloud config set project PROJECT_ID

# Several projects: one named configuration each, switched explicitly
gcloud config configurations create PROJECT_NAME
gcloud config set project PROJECT_ID
gcloud config configurations activate PROJECT_NAME

# Pin a repository to its project (read by the app and by this skill)
echo 'GOOGLE_CLOUD_PROJECT=PROJECT_ID' >> .env
```

When sources conflicted, recommend aligning them to the chosen ID, so the next session resolves without a question.

## References

- `references/README.md`
- gcloud configurations: https://cloud.google.com/sdk/docs/configurations
