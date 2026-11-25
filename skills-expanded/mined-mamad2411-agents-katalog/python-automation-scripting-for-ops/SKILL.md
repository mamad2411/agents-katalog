---
name: python-automation-scripting-for-ops
description: >
  Builds Python-based ops automation and cloud SDK tooling (boto3 and
  similar), including argument parsing, structured logging, packaging a
  script as an installable/reusable CLI, and unit testing with mocked
  cloud calls. Use when the user asks to "write a Python script to
  automate X," "use boto3 to do Y," "turn this script into a proper CLI,"
  "add logging/argument parsing to this script," or "test this
  automation script without hitting real AWS/cloud APIs."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# Python Automation Scripting for Ops

## Purpose

Python is the usual escalation point once a task outgrows what a shell
script can cleanly express: real data structures, cloud SDK calls with
pagination/retries, structured error handling, and logic worth unit
testing. The operational payoff of doing this well is that an automation
script stops being a one-off "ran it once from someone's laptop" artifact
and becomes a reusable, testable CLI tool — with predictable arguments,
machine-parseable logs, and a test suite that runs without touching real
cloud resources — that can be trusted in CI or handed to another engineer.

## When to use

- Automating a cloud operations task (tagging resources, rotating
  credentials, reconciling inventory, bulk remediation) via `boto3` or an
  equivalent cloud SDK.
- Turning an ad hoc script into a proper CLI with subcommands, `--help`,
  and predictable exit codes.
- Adding structured (JSON) logging so a script's output is ingestible by
  a log pipeline instead of only human-readable text.
- Packaging a script so it's installable (`pip install .`) and runnable as
  a console command, rather than invoked as `python path/to/script.py`.
- Testing automation logic — especially cloud API interactions — without
  making real API calls in CI.
- Deciding whether a task belongs in a shell script or has grown enough to
  justify Python — see
  [shell-scripting-best-practices](../shell-scripting-best-practices/SKILL.md)
  for the shell-side equivalent and the crossover point.

## Prerequisites & environment

- Python ≥ 3.10 recommended (structural pattern matching, better error
  messages); anything ≥ 3.9 works for the patterns here — confirm the
  target runtime (e.g. an older Lambda runtime or bastion host image)
  before relying on very recent syntax.
- `boto3`/`botocore` (or the relevant cloud SDK) pinned in
  `requirements.txt`/`pyproject.toml`, plus credentials supplied via the
  SDK's standard credential chain (environment variables, an assumed IAM
  role, instance/task metadata) — never hardcoded in source.
- `pytest` plus `moto` (mocks AWS services at the API layer) or
  `unittest.mock` for testing without live cloud calls.
- `ruff` (or `flake8` + `black`) for lint/format, and `mypy` if the
  codebase uses type hints (recommended for anything beyond a trivial
  script).
- A virtual environment (`venv`, `uv`, or `pipx` for installed CLIs) so
  dependencies are isolated from system Python.

## Step-by-step guidance

1. **Parse arguments explicitly** with `argparse` (standard library, no
   extra dependency) rather than hand-rolling `sys.argv` parsing:
   ```python
   import argparse

   def build_parser() -> argparse.ArgumentParser:
       parser = argparse.ArgumentParser(
           prog="tag-stale-volumes",
           description="Tag unattached EBS volumes older than N days for review.",
       )
       parser.add_argument("--region", required=True, help="AWS region, e.g. us-east-1")
       parser.add_argument("--min-age-days", type=int, default=30)
       parser.add_argument(
           "--dry-run",
           action="store_true",
           help="Report what would be tagged without making changes.",
       )
       parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
       return parser
   ```

2. **Set up structured logging early**, so every run's output is both
   human-readable locally and machine-parseable in a log pipeline:
   ```python
   import json
   import logging
   import sys

   class JsonFormatter(logging.Formatter):
       def format(self, record: logging.LogRecord) -> str:
           payload = {
               "level": record.levelname,
               "message": record.getMessage(),
               "logger": record.name,
           }
           if record.exc_info:
               payload["exc_info"] = self.formatException(record.exc_info)
           return json.dumps(payload)

   def configure_logging(level: str) -> logging.Logger:
       logger = logging.getLogger("tag_stale_volumes")
       logger.setLevel(level)
       handler = logging.StreamHandler(sys.stderr)
       handler.setFormatter(JsonFormatter())
       logger.addHandler(handler)
       return logger
   ```
   Logging to stderr (not stdout) keeps stdout free for the script's
   actual data output, mirroring the same convention covered in
   [shell-scripting-best-practices](../shell-scripting-best-practices/SKILL.md).

3. **Wrap cloud SDK calls with explicit error handling and pagination**,
   since `boto3` raises `botocore.exceptions.ClientError` for API errors
   and requires paginators for any list operation that can exceed one
   page:
   ```python
   import boto3
   from botocore.exceptions import ClientError

   def find_stale_unattached_volumes(ec2_client, min_age_days: int, logger: logging.Logger):
       paginator = ec2_client.get_paginator("describe_volumes")
       cutoff = datetime.now(timezone.utc) - timedelta(days=min_age_days)
       stale = []
       try:
           for page in paginator.paginate(Filters=[{"Name": "status", "Values": ["available"]}]):
               for volume in page["Volumes"]:
                   if volume["CreateTime"] < cutoff:
                       stale.append(volume)
       except ClientError as err:
           logger.error("failed to list volumes", extra={"error": str(err)})
           raise
       return stale
   ```

4. **Never make destructive/mutating calls without a dry-run path
   surfaced by default expectations**:
   ```python
   def tag_volume(ec2_client, volume_id: str, dry_run: bool, logger: logging.Logger) -> None:
       tags = [{"Key": "stale-review", "Value": "true"}]
       if dry_run:
           logger.info("would tag volume", extra={"volume_id": volume_id, "tags": tags})
           return
       ec2_client.create_tags(Resources=[volume_id], Tags=tags)
       logger.info("tagged volume", extra={"volume_id": volume_id, "tags": tags})
   ```
   > **Warning:** Any script that tags, deletes, stops, or modifies cloud
   > resources in bulk should default new/unfamiliar invocations to
   > `--dry-run`, log exactly what it *would* do, and require an explicit
   > flag (not a default) to actually mutate state — the same
   > review-before-apply discipline as a Terraform plan or CloudFormation
   > change set.

5. **Retry transient failures with backoff**, not a bare loop — `botocore`
   already retries some errors internally (configurable via
   `Config(retries={"max_attempts": ...})`), but application-level retry
   logic (e.g. around a multi-call workflow) should back off explicitly:
   ```python
   import time
   from botocore.config import Config

   def make_client(service: str, region: str):
       return boto3.client(
           service,
           region_name=region,
           config=Config(retries={"max_attempts": 5, "mode": "standard"}),
       )
   ```

6. **Structure the script as an installable package with a console entry
   point** once it's more than a single-file utility:
   ```
   tag_stale_volumes/
     pyproject.toml
     src/
       tag_stale_volumes/
         __init__.py
         cli.py
         aws.py
     tests/
       test_aws.py
       test_cli.py
   ```
   `pyproject.toml` (excerpt):
   ```toml
   [project]
   name = "tag-stale-volumes"
   version = "0.1.0"
   dependencies = ["boto3>=1.34"]

   [project.scripts]
   tag-stale-volumes = "tag_stale_volumes.cli:main"

   [build-system]
   requires = ["setuptools>=68"]
   build-backend = "setuptools.build_meta"
   ```
   After `pip install -e .`, the script runs as `tag-stale-volumes --region
   us-east-1 --dry-run` from anywhere, with `--help` generated
   automatically by `argparse`.

7. **Test with mocked cloud calls, not live infrastructure.** Use `moto`
   to simulate AWS at the API layer so tests run offline, deterministically,
   and in CI without real credentials:
   ```python
   import boto3
   from moto import mock_aws
   from tag_stale_volumes.aws import find_stale_unattached_volumes

   @mock_aws
   def test_finds_only_stale_unattached_volumes():
       ec2 = boto3.client("ec2", region_name="us-east-1")
       ec2.create_volume(AvailabilityZone="us-east-1a", Size=10)
       stale = find_stale_unattached_volumes(ec2, min_age_days=0, logger=test_logger)
       assert len(stale) == 1
   ```
   For non-AWS SDKs or code paths `moto` doesn't cover, fall back to
   `unittest.mock.patch` on the client object directly, asserting the
   exact calls made (`assert_called_once_with(...)`) rather than only the
   final return value.

## Best practices

- Set explicit, meaningful exit codes (`sys.exit(1)` for a handled
  failure, a distinct code for "partial success," `0` only on full
  success) so calling automation can branch on outcome, not just
  presence/absence of a traceback.
- Keep `main()` thin — argument parsing and orchestration only — and push
  actual logic into importable, unit-testable functions/modules; a script
  that's all one `if __name__ == "__main__":` block can't be tested
  without invoking the whole CLI.
- Use type hints throughout and run `mypy` in CI; ops scripts that
  manipulate structured API responses benefit disproportionately from
  catching a wrong-shape assumption at lint time instead of at 2am in
  production.
- Never hardcode credentials, account IDs, or region names as literals in
  source — take them as arguments/environment variables
  (`AWS_PROFILE`, `--region`) so the same script runs safely across
  accounts/environments without code changes.
- Pin dependency versions (`boto3>=1.34,<2`) and run `pip-audit` or
  equivalent in CI so a script's own dependencies don't become the
  vulnerability.
- Prefer `pathlib.Path` over string path manipulation, and
  `subprocess.run([...], check=True)` (list form, not `shell=True`) when a
  script must shell out — avoids the injection/quoting hazards covered in
  [shell-scripting-best-practices](../shell-scripting-best-practices/SKILL.md).
- When a script's job is really "configure existing hosts" rather than
  "call a cloud API," reconsider whether
  [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md)
  is a better fit than a bespoke Python/SSH script — Ansible already
  solves inventory, idempotency, and parallel execution for that shape of
  problem.

## Common pitfalls

- **Symptom:** A script that lists cloud resources only processes the
  first 50-100 items and silently misses the rest.
  **Fix:** The underlying `list_*`/`describe_*` API call is paginated and
  the script called it once instead of using a paginator (as in step 3).
  Always use `client.get_paginator(...)` for list/describe operations
  and iterate every page rather than assuming a single response is
  complete.

- **Symptom:** A bulk remediation script mutates far more resources than
  intended on its first real run.
  **Fix:** It shipped without a `--dry-run` default expectation and
  wasn't run in dry-run mode first. Add the dry-run path (step 4), run it
  once and inspect the log output for exactly what would change, and only
  then re-run with mutation enabled — the cloud-tooling equivalent of
  reviewing a Terraform plan or CloudFormation change set first.

- **Symptom:** Tests pass locally but the CI job fails with
  `NoCredentialsError` or, worse, someone notices a test accidentally
  created real cloud resources.
  **Fix:** Tests were calling the real SDK client instead of a mocked one.
  Wrap AWS-touching tests in `@mock_aws` (or patch the client), and add a
  CI safeguard (no real credentials injected into the test job at all) so
  a missing mock fails loudly with `NoCredentialsError` instead of quietly
  hitting production.

- **Symptom:** A `ClientError` from a transient throttling response
  (`ThrottlingException`/`RequestLimitExceeded`) crashes the whole script
  instead of retrying.
  **Fix:** Confirm `botocore`'s built-in retry config is set to a
  reasonable `max_attempts` with `mode: "standard"` (step 5) — the
  default retry behavior varies by SDK version and prior configuration.
  For explicit application-level retries around a multi-step operation,
  add exponential backoff rather than a single bare retry.

- **Symptom:** A script that ran fine for months breaks after a routine
  dependency update, with a cryptic error from deep inside `botocore`.
  **Fix:** Dependencies were unpinned (or pinned too loosely), so a minor
  version bump changed default behavior (e.g. a retry mode default, or a
  response shape). Pin `boto3`/`botocore` to a tested range in
  `requirements.txt`/`pyproject.toml` and bump deliberately with a
  changelog check, not implicitly via `pip install --upgrade`.

## Worked example

**Scenario:** A CLI that finds EBS volumes unattached for more than N
days and tags them for review, dry-run by default behavior enforced via
tests, packaged as an installable console command.

`src/tag_stale_volumes/aws.py`:
```python
from datetime import datetime, timedelta, timezone
import logging

from botocore.exceptions import ClientError


def find_stale_unattached_volumes(ec2_client, min_age_days: int, logger: logging.Logger):
    paginator = ec2_client.get_paginator("describe_volumes")
    cutoff = datetime.now(timezone.utc) - timedelta(days=min_age_days)
    stale = []
    try:
        for page in paginator.paginate(Filters=[{"Name": "status", "Values": ["available"]}]):
            stale.extend(v for v in page["Volumes"] if v["CreateTime"] < cutoff)
    except ClientError as err:
        logger.error("failed to list volumes", extra={"error": str(err)})
        raise
    return stale


def tag_volume(ec2_client, volume_id: str, dry_run: bool, logger: logging.Logger) -> None:
    tags = [{"Key": "stale-review", "Value": "true"}]
    if dry_run:
        logger.info("would tag volume", extra={"volume_id": volume_id})
        return
    ec2_client.create_tags(Resources=[volume_id], Tags=tags)
    logger.info("tagged volume", extra={"volume_id": volume_id})
```

`src/tag_stale_volumes/cli.py`:
```python
import boto3

from .aws import find_stale_unattached_volumes, tag_volume
from .logging_setup import configure_logging
from .args import build_parser


def main() -> int:
    args = build_parser().parse_args()
    logger = configure_logging(args.log_level)
    ec2 = boto3.client("ec2", region_name=args.region)

    stale = find_stale_unattached_volumes(ec2, args.min_age_days, logger)
    logger.info("found stale volumes", extra={"count": len(stale)})

    for volume in stale:
        tag_volume(ec2, volume["VolumeId"], args.dry_run, logger)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

`tests/test_aws.py`:
```python
import logging
import boto3
from moto import mock_aws

from tag_stale_volumes.aws import find_stale_unattached_volumes, tag_volume

logger = logging.getLogger("test")


@mock_aws
def test_only_returns_available_volumes():
    ec2 = boto3.client("ec2", region_name="us-east-1")
    ec2.create_volume(AvailabilityZone="us-east-1a", Size=10)
    stale = find_stale_unattached_volumes(ec2, min_age_days=0, logger=logger)
    assert len(stale) == 1


@mock_aws
def test_dry_run_does_not_call_create_tags(monkeypatch):
    ec2 = boto3.client("ec2", region_name="us-east-1")
    called = {"count": 0}
    monkeypatch.setattr(ec2, "create_tags", lambda **kw: called.__setitem__("count", called["count"] + 1))
    tag_volume(ec2, "vol-example123", dry_run=True, logger=logger)
    assert called["count"] == 0
```

Run:
```bash
pip install -e ".[dev]"
ruff check src/ tests/
mypy src/
pytest tests/ -v
tag-stale-volumes --region us-east-1 --min-age-days 30 --dry-run
```

## Cross-references

- [shell-scripting-best-practices](../shell-scripting-best-practices/SKILL.md)
- [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md)
- [aws-cloudformation-templates](../aws-cloudformation-templates/SKILL.md)
