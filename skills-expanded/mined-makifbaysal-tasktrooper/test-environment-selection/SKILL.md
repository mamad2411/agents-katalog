---
name: test-environment-selection
category: qa
description: Use before booting anything - choosing local (start_task_preview or a workspace boot), the task's preview or stage, confirming the build is the PR head, and what to do when nothing can run
---
# Test Environment Selection

## Overview

Before executing a single scenario, decide WHERE the product will run, in this order:

1. **Backend, worker or full-stack repository: local.** DB rows, logs and third-party stubs are only observable there. First choice `start_task_preview` — it checks out the task branch in the task workspace, detects how to run it, starts it, stops a stale server, and returns a `localhost` URL for the browser tools; call it again if the URL isn't there yet. Only when it cannot run the project (e.g. a backend+frontend pair, or a worker it doesn't detect), boot by hand (backend-manual-testing).
2. **Frontend-only repository: the task's own preview, else local.** When the component is deployed with a per-branch `preview` environment, `get_task_preview` returns it — use it when `status: "ready"` AND `built_from_pr_head: true`. Anything else (`building`, `built_from_pr_head: false`, `error`, `canceled`, `none`, or an empty list) is not the code under test: fall back to `start_task_preview`.
3. **Stage.** Used when the repository is configured for stage verification, or when the app cannot boot locally (managed secrets, heavy infra the workspace lacks) — always after confirming stage is actually running the PR head (see Stage rules).

**Production is never a test environment.** No scenario is ever executed against the prod base URL or prod data — not a "harmless" GET, not seeding, not cleanup.

## How to decide

1. Identify the repository shape (backend/worker/full-stack vs frontend-only) and apply the order above.
2. Read the repository settings (`list_repositories`): `build_command`, `test_command`, `verify_command` — and any comment the developer left on the task (a clean run leaves none). These are the project's declared way of running and checking itself. `get_project_brief` has the same information plus what each component talks to.
3. If neither a usable preview nor a local boot nor stage works, you are blocked — see below.

## Preview rules

- **Address.** Use `open_url` in the browser (`browser_navigate`) — for a protected preview it carries the bypass and sets a cookie, so the pages it links to load too. For HTTP requests (curl, an API client) use `branch_url` (or `url` when there is none) and send every header in `request_headers` on every request.
- **Protected without a bypass.** When the entry notes that the preview is behind Vercel Deployment Protection with no Protection Bypass for Automation, the preview answers every automated request with a login page. Do not report that page as a failure. Test locally instead and leave one comment asking the human to add "Protection Bypass for Automation" in the Vercel project (Settings → Deployment Protection).
- **Never write the bypass secret** — nor `open_url`, which contains it — into a comment, test case, document or bug report: it opens the project's previews to whoever reads it. Refer to "the preview bypass" instead.
- **A preview is not prod, but its backing services may be.** If the preview talks to a shared database or a third-party account, avoid destructive scenarios there exactly as on stage; they run locally only.
- **Put the preview's `branch_url` and short `commit_sha` in every `review_criterion` note** — the next reader needs to know exactly what ran, and a pass writes no comment to say it elsewhere.

## Stage rules

- **Confirm the change is actually there before testing.** `list_deployments` (env=stage) shows the commit of the latest deploy — it must equal the PR head from `get_task_pull_request`. `get_environment` says whether stage is bound at all. Not equal → wait for the stage deploy that started when the task entered `ready_for_qa` (`get_pipeline_status` shows its progress); never test the old build.
- **Stage is shared.** Namespace your test data (`qa-<task-key>-...` prefixes, test-data-and-stubs), avoid destructive scenarios (mass deletes, migrations, load tests) — those run locally only — and clean up what you created.
- The stage `base_url` is for requests; the `health_url` is only a liveness probe.

## When none is possible

If there is no usable preview, the app cannot boot in the workspace (including via `start_task_preview`) AND no stage target exists (or it isn't running the PR head), do not fake a verdict and do not read the code as a substitute. Apply the blocker triage (qa-verify-before-verdict): the project cannot boot from its own documented commands → `need_revision` with the failing command and its output, a developer-fixable defect. A blocker only a human can lift (no stage configured at all, a credential you don't have) → one `ask_user` question with concrete options, not a `need_revision` the developer cannot act on.

## Red Flags

- A connection string or base URL in your commands points at prod → stop immediately.
- "I'll just check this one thing on prod" → no. Preview, local or stage, always.
- Testing a preview or stage whose commit is not the PR head → the verdict describes an earlier version.
