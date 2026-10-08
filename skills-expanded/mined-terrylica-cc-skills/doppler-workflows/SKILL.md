---
name: doppler-workflows
description: Manage credentials and secrets through Doppler for publishing and deployment workflows. Use whenever the user needs to publish Python packages.
allowed-tools: Read, Bash
---

# Doppler Credential Workflows

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- Publishing Python packages to PyPI
- Rotating AWS access keys
- Managing credentials across multiple services
- Troubleshooting authentication failures (403, InvalidClientTokenId)
- Setting up Doppler credential injection patterns
- Multi-token/multi-account strategies

## Quick Reference

## Core Pattern: Doppler CLI

**Standard Usage:**

```bash
doppler run --project <project> --config <config> --command='<command>'
```

**Why --command flag:**

- Official Doppler pattern (auto-detects shell)
- Ensures variables expand AFTER Doppler injects them
- Without it: shell expands `$VAR` before Doppler runs → empty string

---

## Quick Start Examples

### PyPI Publishing

```bash
doppler run --project claude-config --config dev \
  --command='uv publish --token "$PYPI_TOKEN"'
```

### AWS Operations

```bash
doppler run --project aws-credentials --config dev \
  --command='aws s3 ls --region $AWS_DEFAULT_REGION'
```

---

## Best Practices

1. Always use --command flag for credential injection
2. Use project-scoped tokens (PyPI) for better security
3. Rotate credentials regularly (90 days recommended)
4. Document with Doppler notes: `doppler secrets notes set <SECRET> "<note>"`
5. Use stdin for storing secrets: `echo -n 'secret' | doppler secrets set`
6. Test injection before using: `echo ${#VAR}` to verify length
7. Multi-token naming: `SERVICE_TOKEN_{ABBREV}` for clarity

---

## Reference Documentation

For detailed information, see:

- [PyPI Publishing](./references/pypi-publishing.md) - Token setup, publishing, troubleshooting
- [AWS Credentials](./references/aws-credentials.md) - Rotation workflow, setup, troubleshooting
- [Multi-Service Patterns](./references/multi-service-patterns.md) - Multiple PyPI packages, multiple AWS accounts
- [AWS Workflow](./AWS_WORKFLOW.md) - Complete AWS credential management guide

**Bundled Specifications:**

- `PYPI_REFERENCE.yaml` - Complete PyPI spec
- `AWS_SPECIFICATION.yaml` - AWS credential architecture

---

## Using mise [env] for Local Development (Recommended)

For local development, mise `[env]` provides a simpler alternative to `doppler run`:

```toml
# .mise.toml
[env]
# Fetch from Doppler with caching for performance
PYPI_TOKEN = "{{ cache(key='pypi_token', duration='1h', run='doppler secrets get PYPI_TOKEN --project claude-config --config prd --plain') }}"
```

> **Do NOT use mise `[env]` for GitHub tokens (ADR 2026-06-21).** GitHub
> multi-account auth is driven by the repo's `origin` host-alias
> (`git@github.com-<account>:…`), not mise. A token resolves fresh per-repo via
> `~/.claude/tools/bin/gh-token-for-repo`; an ambient `GH_TOKEN` outranks the
> isolated gh profile and 401s after a rotation. The `.secrets/gh-token-*` files are
> deleted.

**When to use mise [env]** (for non-GitHub secrets like `PYPI_TOKEN`):

- Per-directory credential configuration
- Credentials that persist across commands (not session-scoped)

**When to use doppler run:**

- CI/CD pipelines
- Single-command credential scope
- When you want credentials auto-cleared after command

See [`mise-configuration` skill](../../../itp/skills/mise-configuration/SKILL.md) for complete patterns.

---

## PyPI Publishing Policy

<!-- ADR: 2025-12-10-clickhouse-skill-documentation-gaps -->

For PyPI publishing, see [`pypi-doppler` skill](../../../itp/skills/pypi-doppler/SKILL.md) for **LOCAL-ONLY** workspace policy.

**Do NOT** configure PyPI publishing in GitHub Actions or CI/CD pipelines.

---

## Troubleshooting

| Issue                      | Cause                            | Solution                                              |
| -------------------------- | -------------------------------- | ----------------------------------------------------- |
| 403 on PyPI publish        | Token expired or wrong scope     | Regenerate project-scoped token, update in Doppler    |
| InvalidClientTokenId (AWS) | Access key rotated or deleted    | Run AWS key rotation workflow, update Doppler         |
| Variable expands empty     | Using `$VAR` without --command   | Always use `--command='...$VAR...'` pattern           |
| Doppler CLI not found      | Not installed                    | `brew install dopplerhq/cli/doppler`                  |
| Wrong config selected      | Ambiguous project/config         | Specify both `--project` and `--config` explicitly    |
| mise [env] not loading     | Not in directory with .mise.toml | `cd` to project directory or check mise.toml path     |
| Secret retrieval slow      | No caching configured            | Use mise `cache()` with duration for repeated access  |
| Token length mismatch      | Copied with extra whitespace     | Trim token: `echo -n 'secret' \| doppler secrets set` |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
