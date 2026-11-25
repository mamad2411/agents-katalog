---
name: remediating-dependabot
description: Remediates GitHub Dependabot alerts for mflux in one dependency-security change. Use when auditing, clamping, or upgrading Python dependencies in pyproject.toml and uv.lock, or when validating whether a branch will close Dependabot findings before opening a PR.
---

# Remediating Dependabot

Resolve actionable Dependabot alerts with the smallest compatible dependency update and prove the local lock is outside every reported vulnerable range.

## Scope

- Use `gh api` as the source of truth for open alerts in `mflux-community/mflux`.
- Keep dependency changes in `pyproject.toml` and `uv.lock` unless compatibility requires source changes.
- Preserve supported Python and platform markers.
- Avoid unrelated package upgrades when regenerating the lock.
- Treat dependency optionality or loading refactors as separate work unless explicitly requested.

## Workflow

1. Confirm the current branch and working tree before editing.
2. Fetch all open Dependabot alerts, following pagination:

   ```bash
   gh api --method GET --paginate \
     -H "Accept: application/vnd.github+json" \
     repos/mflux-community/mflux/dependabot/alerts \
     -f state=open
   ```

3. Group alerts by manifest, package, severity, vulnerable range, and first patched version. Distinguish direct requirements from transitive lock entries.
4. Inspect `pyproject.toml`, `uv.lock`, supported Python versions, and platform markers before choosing a fix.
5. Prefer, in order:
   - removing dependencies that are no longer needed;
   - raising a direct lower bound to the first secure compatible release;
   - upgrading only affected transitive packages in the lock;
   - adding or changing environment markers only when compatibility actually differs by Python or platform.
6. Use one requirement when a release supports the full project matrix. Do not introduce overlapping marker-specific requirements without evidence that they are necessary.
7. Regenerate the lock with targeted upgrades:

   ```bash
   uv lock --upgrade-package <package> [--upgrade-package <package> ...]
   ```

8. Review the lock diff. Explain large platform-specific resolver changes, especially PyTorch CUDA package transitions, rather than assuming they are accidental.

## Security verification

Do not infer alert closure solely from package names or Dependabot's hosted UI.

1. Run lock and advisory checks:

   ```bash
   uv lock --check
   uv audit --preview-features audit-command
   ```

2. Parse every resolved version in `uv.lock` and compare it with every open alert's `security_vulnerability.vulnerable_version_range`. Canonicalize names with `packaging.utils.canonicalize_name` and use `packaging.specifiers.SpecifierSet` so matching follows Python package name and version semantics.
3. Confirm that each alert is resolved by either:
   - no matching package remaining in the lock; or
   - every matching locked version falling outside the vulnerable range.
4. Run Dependabot Core against the local checkout before opening a PR:

   ```bash
   tmp_dir="$(mktemp -d)"
   trap 'rm -rf "$tmp_dir"' EXIT
   job="$tmp_dir/job.yml"
   output="$tmp_dir/output.yml"

   # Build the security job at "$job" before running these commands.
   dependabot graph uv mflux-community/mflux --local "$PWD"
   dependabot update --local "$PWD" -f "$job" -o "$output" --pull=false --timeout 20m
   ```

   `graph` is experimental and may return an incomplete dependency list. Both commands snapshot the directory passed to `--local`, including modified and untracked files, so confirm that the working tree contains only the intended updater input.

   Build the temporary `uv` security job from the exact package names and advisory ranges returned by GitHub. Parse the YAML output rather than relying on the command's exit status:

   ```bash
   uv run python - "$output" <<'PY'
   import sys

   import yaml

   with open(sys.argv[1]) as output_file:
       actions = {entry["type"] for entry in yaml.safe_load(output_file)["output"]}

   if "mark_as_processed" not in actions:
       raise SystemExit("Dependabot did not mark the job as processed")

   pull_request_actions = actions & {"create_pull_request", "update_pull_request"}
   if pull_request_actions:
       raise SystemExit(f"Dependabot still proposes actions: {sorted(pull_request_actions)}")
   PY
   ```

   Do not pin Dependabot CLI to one release. Verify the installed CLI exposes the commands and flags used here before running the job.
5. Keep temporary Dependabot job and output files outside the committed change, and remove them after verification.
6. If the hosted alert remains open while the local lock is already outside its vulnerable range, report it as pending or stale until GitHub rescans. Do not force an unnecessary upgrade just to change the lock entry.

## Project verification

Run the repository workflows after the lock is secure:

```bash
just lint
just lint-justfile
just typecheck
just test-fast
just test
just build
git diff --check
```

Use `uv lock --upgrade --dry-run` to check that a fresh universal resolution succeeds. It may report unrelated newer releases; do not add them unless they are needed for the remediation.

## Reporting

Report:

- total open findings expected to close, grouped by severity and package;
- direct requirement changes and noteworthy lock-only changes;
- packages removed from the lock;
- exact results from range comparison, Dependabot Core, `uv audit`, and project checks;
- any alerts whose final hosted closure depends on GitHub rescanning the merged lockfile.
