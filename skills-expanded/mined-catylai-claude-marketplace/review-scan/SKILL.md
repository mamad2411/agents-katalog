---
name: review-scan
description: "Runs the deterministic linter and secret-scan pass, with no model tokens, over the files a branch changed. It writes diff-scoped findings to .code-review/SCAN.json and a summary that lists every skipped tool. Use when asked what the linters say about a branch, before a judgement review, or as a CI step whose output a later review reads. Not a full review or a gate (use review, or /code-review for a quick pass). Claude Code only: needs a git checkout and a shell."
argument-hint: "[base-ref] [--detectors a,b]"
allowed-tools: Bash(bash "${CLAUDE_PLUGIN_ROOT}/pipeline/review-scan.sh" *), Bash(python3 -m json.tool */.code-review/SCAN.json), Bash(git symbolic-ref *), Bash(git rev-parse *), Read, Grep, Glob
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# review-scan

Arguments: `$ARGUMENTS`

Linters and secret scanners find grep-shaped defects better and cheaper than a model reading files.
This skill runs them over the changed files only and leaves business logic, authorization and design
to the `review` pipeline.

## Run it

Take the first argument that does not start with `--` as the base ref, and pass any other flags
through. With no base, use the first of these that resolves: `git symbolic-ref --short
refs/remotes/origin/HEAD`, then `git rev-parse --verify --quiet origin/main`, then `origin/master`.
If none resolves, ask the user for one. Write the ref literally into the command, because shell
variables do not persist between calls:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/pipeline/review-scan.sh" --base <base> [--detectors a,b]
```

It is the same invocation locally and in CI. The script writes to `<root>/.code-review/`, where
`<root>` is the output of `git rev-parse --show-toplevel`, whatever directory the session started in;
read the outputs there.

| Flag | Default | Notes |
| --- | --- | --- |
| `--base <ref>` | required by the script | merge base: `origin/main` locally, a CI-supplied base SHA in CI |
| `--source <ref>` | `HEAD` | the branch under review |
| `--out <dir>` | `.code-review` | the workspace the rest of the pipeline reads |
| `--detectors a,b` | chosen from the changed files | `python`, `shell`, `terraform`, `iac-policy`, `deps`, `comments`, `secrets`, `impact` |
| `--max-findings N` | `150` | truncates lowest severity first, and records that it did |
| `--fail-under N` | from `pyproject.toml` / `setup.cfg` / `.coveragerc` | coverage threshold |
| `--quiet` | off | suppresses progress on stderr |

Exit status is 0 whenever the scan completed, whatever it found. Findings are reported, not
enforced, so a linter missing from a runner image cannot fail a pipeline. A non-zero exit means the
scan itself could not run (bad ref, not a git repository). Report the stderr line and stop.

## Outputs

All under `--out`:

| File | Contents |
| --- | --- |
| `SCAN.json` | the findings, in the shape defined by `${CLAUDE_PLUGIN_ROOT}/pipeline/schemas/agent-contract.schema.json`. This is what a reviewer reads |
| `SCAN.raw.json` | the same before diff scoping; check it when an expected finding is missing |
| `SCAN-SUMMARY.md` | counts by tool and severity, and the `SKIPPED:` list |
| `raw/<tool>.json` | each tool's native output |
| `raw/<tool>.skipped` | one line saying why a tool did not run |

Each finding carries `severity` (`BLOCKER`, `MAJOR`, `MINOR`, `NIT`), `in_diff` (`true`/`false`) and
`confidence` (`HIGH`, `MEDIUM`, `LOW`), plus `id`, `category`, `location`, `title`, `evidence`,
`recommendation` and `ux_impact`.

## Reading the output

1. **Findings are on changed lines.** `pipeline/filter-carried-findings.py` keeps only findings on
   the new side of the diff's `@@` hunks, so existing lint debt stays out. If
   `scan_meta.diff_scoped` is `false`, the filter did not run and you are looking at unfiltered
   debt. Say so.
2. **Skipped tools matter as much as findings.** A scan with half its tools missing looks like a
   clean scan unless the gaps are stated. Report "scanned with k of n tools" from
   `scan_meta.tools_run` and `scan_meta.tools_skipped`.
3. **Some tools supply no severity.** Their findings default to `MINOR`, recorded in
   `scan_meta.notes`. Judge those on the rule, not the severity.

## Detectors

| Detector | Tools | Notes |
| --- | --- | --- |
| `python` | ruff, bandit, mypy, pylint | ingests `raw/pytest.json` and `raw/coverage.json` if CI drops them in; never runs the suite |
| `shell` | shellcheck | `.sh`/`.bash`/`.zsh`, plus extensionless files with a shell shebang |
| `terraform` | terraform fmt, tflint, checkov, tfsec | `.tf`/`.tfvars`/`.hcl`; `terraform validate` is never run because it needs `init` |
| `secrets` | gitleaks, trivy | runs whenever anything changed; gitleaks runs with `--redact`, trivy masks secret values itself |
| `deps` | built in | unpinned dependencies; an action on a tag or a `:latest` base is MAJOR, a caret range beside a lock file is a NIT |
| `comments` | built in | commented-out code blocks, and `TODO`/`FIXME`/`XXX` with no issue reference; both NIT |
| `iac-policy` | built in | Terraform, CI pipelines, Makefiles and `.sql` migrations: `-target` in automation, `dynamodb_table` locking, environment-variable defaults, undocumented variables, OIDC trust without `:sub`, `StringLike` without a wildcard, `iam:PassRole` on `"*"`, non-concurrent `CREATE INDEX`; never BLOCKER |
| `impact` | git grep | removed, renamed or re-signatured symbols with consumers outside the diff; NIT |

That is 7 detectors over 11 external tools, plus `git grep` and two built-in checks. A detector named in `--detectors` that is not
bundled is recorded as a skip. TS/JS files get `secrets` and `impact` only, and the scan records that
as a skip too.

### Test and coverage input

`detectors/python.sh` reads two files if CI has already written them:

- `raw/coverage.json`: coverage.py's own JSON, as `--cov-report=json` writes it.
- `raw/pytest.json`: this scanner's own summary, `{failed: [{nodeid, file, line, message}], rc: int}`.
  Derive it from a JUnit XML report with the standard library.

## Verify

```bash
python3 -m json.tool <root>/.code-review/SCAN.json
```

If it parses, read `SCAN-SUMMARY.md` and report:
- the finding counts by severity
- whether `diff_scoped` is true
- which tools were skipped, and why

If it does not parse, report that the scan did not complete and quote the script's stderr.

## Without a checkout

The scan needs a git repository and a shell. If neither is available, say so. For a pasted diff,
offer `/code-review` instead, and do not present a model reading as a linter result.
