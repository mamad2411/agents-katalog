---
name: aws-iac-team-harness
description: "Use when a Terraform-on-AWS repository needs checks every agent and developer must pass: installing or updating the harness (fmt, validate, TFLint, Checkov with graph policies, mocked terraform tests), recording legacy findings in a baseline, adding the reference GitHub Actions plan/approve/apply workflow with plan provenance, or verifying a deployed Lambda/API against the checkout. Not for writing new infrastructure from scratch (use creating-aws-projects)."
---

# AWS IaC team harness

The harness turns rules into checks that fail. It installs scripts and config under `harness/` and one section of `AGENTS.md`, and never edits the project's Terraform.

Hooks provide feedback; authority comes from IAM and protected CI. The agent's role must not be able to apply.

## Install or update

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/apply_harness.py" /path/to/project [--workflows] [--dry-run]
```

`${CLAUDE_SKILL_DIR}` is this skill's folder; Codex doesn't set it, so use the folder this file is in.

- Writes `harness/{check,baseline,plan_summary,plan_provenance,verify_deployment}.py`, `harness/.tflint.hcl`, `harness/checkov/*.yaml` and the harness section of `AGENTS.md`. `harness/lock.json` records what it wrote.
- A rerun updates files nobody edited and reports edited ones as `conflict` (exit 1) instead of overwriting them. Merge a conflict by hand, or delete the file and rerun.
- `--workflows` adds `.github/workflows/harness-checks.yml` and `terraform-deploy.yml`. Leave it off when the project deploys through Atlantis, HCP Terraform or another runner: wire `harness/check.py` and `harness/plan_summary.py` into that runner instead. Never run two apply paths for one state.

Before telling the user the workflows are ready, go through the administrator checklist in `references/deployment-workflows.md` with them: branch protection, environment reviewers, the two OIDC trust policies, repository variables, private visibility. YAML cannot enforce any of these.

## Check

```bash
python harness/check.py .                 # every root
python harness/check.py . --changed infra/main.tf   # only the affected roots
```

Per root: `fmt`, `init -backend=false`, `validate`, `tflint`, `checkov` once per environment file (`*.tfvars` in `envs/`, `env/` or `environments/`, or each `--var-file`), `terraform-test`; plus `app-tests` when `app/tests` exists. Last line: `harness check: PASS|FAIL|UNVERIFIED (...)`. Exit 0/1/2.

UNVERIFIED means the check could not run: a tool is missing, `init` failed (network, provider constraint), a root has no environment file (Checkov would guess variable values; name one with `--var-file`), or no `tests/*.tftest.hcl`. It is never a pass. `init` needs network for providers and modules; run checks sequentially, because Terraform's plugin cache is not safe for concurrent use.

Coverage, and why each custom check exists: `references/coverage.md`.

## Adopt a repository with existing findings

A person (not the agent) records today's findings:

```bash
python harness/baseline.py record . --owner TEAM --reason "pre-harness, TICKET-1" --expires 2027-05-01
```

Each entry tolerates one finding (check ID + root + resource). A new instance of the same rule still fails, as does a new finding that replaces a fixed one. Rules are never disabled. Expired entries stop tolerating. `baseline.py prune` removes entries whose finding is gone. Review `harness/baseline.json` changes like code.

## Record a false positive

Some findings are wrong for the code. For example, tflint reports a data source as unused when it exists only for its `postcondition`. The baseline is for old findings, not for code that is right. A reviewer, not the agent, suppresses such a finding where it occurs, with the reason on the line above:

```hcl
# Exists only for the postcondition: every subnet must be in var.vpc_id.
# tflint-ignore: terraform_unused_declarations
data "aws_subnet" "private" {
```

The general form is `# tflint-ignore: <rule>`; for Checkov, `#checkov:skip=<ID>: <reason>` inside the resource, or an entry in `.checkov.yaml` for a rule that does not apply to the whole project. Name one rule, never `all`, and review the line like code.

## Verify a deployment

```bash
uv run --with boto3 python harness/verify_deployment.py verify . \
  --profile sandbox --expect-account 123456789012 --expect-region us-east-1
```

Order: target (exit 3 before any request if the credentials or Terraform outputs point elsewhere) → artifact (deployed `CodeSha256` = local package = `app/`) → probes from `.verify/probes.json` (signed when the API uses IAM, plus an unsigned request that must be rejected) → logs found by request ID with the correlation ID → trace, alarms, alerting (reported, not deciding the exit: traces are sampled, alarms lag, a confirmed subscriber is not a delivered message).

Exit 0 PASS, 1 FAIL, 2 UNVERIFIED (for example, logs not in yet: rerun, do not report a pass), 3 wrong target. Paste the last line as evidence.

After a sandbox teardown, `verify_deployment.py residue --project-tag NAME --environment ENV ...` lists anything still tagged with the project.

## Windows

Checkov's `checkov.cmd` runs the first `python` on PATH. With uv/pipx installs that python usually lacks Checkov; point the launcher at the tool environment's `python.exe`, or pass `--checkov`.
