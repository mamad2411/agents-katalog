---
name: forge-onboard-project
description: Onboard a GitLab project as a forge target (webhook, CI variables, runner, harness template include) and verify with forge doctor --project. Use when connecting a new repository to forge.
---

# forge-onboard-project: wire a GitLab project to forge

Authorization rule: CI is RCE — a human approves the execution profile
BEFORE the first run (ADR-0002/0011). The agent prepares everything and
executes only what the user has approved.

1. **Baseline check**: `uv run python -m forge.doctor --project <id>` —
   fix `project.*` failures step by step. Never print CI variable values.
2. **Webhook** (Settings → Webhooks): point to the forge app
   (`http://<host>:8420/webhook`), secret = `GITLAB_WEBHOOK_SECRET`,
   events: Notes, Merge Request, Pipeline, Job. LAN hosts require the
   admin setting `allow_local_requests_from_web_hooks_and_services`.
3. **CI variables** (Settings → CI/CD → Variables; masked where possible):
   `FORGE_BOT_TOKEN` (bot PAT with write to `factory/*` branches, project-
   scoped) + the harness credential for the chosen backend
   (`ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_BASE_URL` for claude-code,
   `ZAI_API_KEY` for opencode, `FORGE_GROK_AUTH` for grok). Optional:
   `FORGE_HARNESS_HTTPS_PROXY` when the runner network throttles AI streams.
4. **Runner**: at least one active docker-executor runner must serve the
   project (`doctor` checks this). Shell runners are not acceptable for
   harness execution (ADR-0002).
5. **Harness template** (human-applied, one line in `.gitlab-ci.yml`):

   ```yaml
   include:
     - remote: 'https://raw.githubusercontent.com/forcewake/forge/main/ci/templates/grok.gitlab-ci.yml'
   ```

   The job runs only when forge triggers a pipeline with `FORGE_RUN_ID`.
6. **Per-project config** (optional `.forge.yml` on the default branch):
   implementer backend and tighten-only overrides; env
   `FORGE_IMPLEMENTER_BACKEND=ci_harness` is the forge-side default.
7. **Smoke**: run the pipeline manually with `FORGE_SMOKE=1` (or the
   template's manual job) and confirm the harness job completes.
8. Re-run `forge doctor --project <id>` → exit 0. Then the first live run:
   `/implement` → review the plan → `/go <run-id>`.
