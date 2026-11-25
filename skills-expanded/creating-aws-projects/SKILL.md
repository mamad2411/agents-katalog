---
name: creating-aws-projects
description: "Use when starting a new AWS application in Terraform: an HTTP API on Lambda, and later ECS web services, SQS workers, Step Functions APIs or EC2 services; choosing the pattern, runtime profile and inputs; rendering the tested Copier template; and checking the result. Not for changing an existing deployed project or for EKS."
---

# Creating AWS projects

Render a tested template; do not hand-write the pattern. The template carries the application stub, Terraform, IAM, logs, alarms, dashboard, runbook, mocked tests and probes, and the checks below prove the render is intact.

## Workflow

1. **Inspect first.** If the directory already holds a project, stop: these templates create new projects only. Read what the repo already uses (language, IaC tool, CI runner, existing modules) and do not ask what you can read.
2. **Pick the pattern.** `references/patterns.md` lists what exists and when each fits. Only patterns with a template can be rendered. For anything else, say it is not supported yet.
3. **Check the runtime profile.**
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/profiles.py" resolve <pattern> <runtime> <architecture> <packaging> --region <aws_region>
   ```
   The last three arguments come from the pattern's profile: `python3.13 arm64 zip` for `apigw-lambda` and `sqs-lambda-worker`, `python3.13 arm64 container` for `ecs-web`, `python3.13 arm64 ami` for `alb-ec2`, `asl-jsonpath managed definition` for `apigw-step-functions`, and `none managed module` for `network`.
   Exit 0 only. FAIL or UNVERIFIED means the combination is untested or past its runway: tell the user. Do not render a different runtime and call it supported. Read `references/runtime-selection.md` before proposing a new profile.
4. **Gather answers.** One question per turn, only for what has no sensible default: name, environment, account ID, alarm email, state backend. For `apigw-lambda`, ask whether the API may be public, and why. For `sqs-lambda-worker`, ask how long one message takes and how many retries it deserves. For `ecs-web`, ask which secrets the app reads (names only, never values: they go in `secret_names`), why the service may have no authentication, and whether a WAF, load balancer access logs or another deployment strategy are required: Express Mode offers none of them, so say the template does not fit. For `apigw-step-functions`, ask whether the workflow always ends within 25 s; if not, say the template does not fit. For `alb-ec2`, ask why the software needs a VM rather than a container, and for a certificate ARN. For `ecs-web` and `alb-ec2`, ask which network to use: a `network` project or subnet IDs from the platform team. The templates do not use the default VPC. If there is no network, offer to render the `network` template first, as its own project. Write the answers to a JSON file.
5. **Render.**
   ```bash
   uv run --with copier==9.19.1 python "${CLAUDE_SKILL_DIR}/scripts/render.py" <pattern> ./my-service --answers answers.json
   ```
   It refuses an existing destination (exit 3), refuses a failing profile, and leaves nothing behind when Copier rejects the answers. Report the `template_revision` it prints.
6. **Install the harness** with the `aws-iac-team-harness` skill (`apply_harness.py`). The next step fails without it: the harness files and the `AGENTS.md` section are what make the next agent that changes the project run the same checks.
7. **Check.**
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/check_new_project.py" ./my-service
   ```
   Every line must be PASS. Fix FAILs in the template inputs, not by editing generated files to satisfy a check. UNVERIFIED means a tool or the network was missing: install it and rerun; do not report it as passing.
8. **Report** what was generated, the check's last line, and what is not yet proven: nothing is deployed, and the profile stays `candidate` until a sandbox deploy is verified with `verify_deployment.py`.

`${CLAUDE_SKILL_DIR}` is this skill's folder; Codex doesn't set it, so use the folder this file is in.

## Do not

- Render into an existing project, or merge a template into one by hand.
- Add a runtime, architecture or region to a template's choices without a profile and its evidence.
- Generate placeholder `import {}` or `moved {}` blocks: a new project has nothing to migrate.
- Treat a clean check as proof the service works: that is what the sandbox verification is for.
