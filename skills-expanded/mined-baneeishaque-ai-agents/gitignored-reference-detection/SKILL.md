---
name: gitignored-reference-detection
description: Detect and remediate references to gitignored files in committed markdown — local paths that exist on the author's machine but break when the repo is cloned standalone.
category: Portability
---

# Gitignored Reference Detection

When a committed markdown file links to or references a local file that is
gitignored, that reference breaks for anyone who clones the repo standalone
(the target file is not in the commit history). This skill detects such
references and replaces them with stable public URLs, ensuring the artifact
remains navigable after clone.

## When to use

- You committed a markdown file that links to a file in a gitignored
  directory (e.g., `.claude/skills/<tool>/SKILL.md`).
- An AI tool reports a broken or inaccessible reference in a skill you are
  editing.
- You are auditing a skill or rule file before publication and want to
  ensure every cross-reference survives a standalone clone.
- A review points out that a path "works on my machine" but fails for
  other team members.

## What the skill owns

- Detecting whether a referenced file path falls under a `.gitignore` rule.
- Determining the public hosted URL for a gitignored local skill (when the
  skill originates from an open-source repository).
- Replacing the local path reference with the public URL in committed
  markdown.
- Verifying that the replacement URL is resolvable and points to the
  expected content.

## What the skill does NOT own

- Authoring or auditing `.gitignore` rules — see
  [`gitignore-rules`](../gitignore-rules/SKILL.md) for that.
- Deciding what to redact in public-scope files — see
  [`redaction-portability`](../redaction-portability/SKILL.md).
- General path relativization within a repo — see
  [`redaction-portability` §3](../redaction-portability/SKILL.md#3-path-handling-protocol).

## Environment & Dependencies

- **Git**: Required for `git check-ignore -v`. Verify with `git --version`.
- **Python 3.12+**: Required for the bundled script. Verify with `python3 --version`.
- **curl**: Optional, used to verify public URLs resolve. Verify with `curl --version`.

## Detection workflow

### Step 1 — Identify suspect references

For each markdown file under audit, find all link targets that point to
paths on the local filesystem:

```bash
# Find markdown links to local paths
grep -rnE '\]\(\.\.?/' .agents/skills/<skill>/SKILL.md
```

Also check for bare path references in code blocks or prose:
- `` `path/to/file` ``
- `<workspace-root>/path/to/file`

### Step 2 — Check gitignore status

For each suspect path, resolve the full path relative to the repo root and
run:

```bash
git check-ignore -v <relative-path>
```

If the path is gitignored, the output shows which `.gitignore` rule covers
it and the line number:

```text
.gitignore:123:.claude/skills/playwright-cli/	.claude/skills/playwright-cli/SKILL.md
```

If the path is NOT gitignored, the command exits with code 1 and no output.

**Automated scan**: Use the bundled helper script to audit all markdown
files under a given path:

```bash
python3 scripts/detect-gitignored-refs.py --path .agents/skills/<skill>/SKILL.md
```

Or scan an entire directory:

```bash
python3 scripts/detect-gitignored-refs.py --path .agents/skills/
```

### Step 3 — Find the public hosted URL

If the gitignored file originates from an open-source project or a known
public repository, find its stable hosted URL:

1. Check the project's published documentation or the source repository's
   `SKILL.md` location.
2. Prefer a permanent URL (tagged release or `main`/`HEAD` branch path on
   the canonical hosting platform).
3. Verify the URL resolves:

   ```bash
   curl -s -o /dev/null -w '%{http_code}' "https://github.com/..."
   ```

   Expected: `200`.

### Step 4 — Replace the reference

Replace the local path in the markdown link with the public URL:

```diff
- [`tool-name`](.claude/skills/tool-name/SKILL.md)
+ [`tool-name`](https://github.com/owner/repo/tree/branch/path/to/SKILL.md)
```

If the reference occurs in prose (not a link), wrap it in a link:

```diff
- using the `tool-name` skill
+ using the [`tool-name`](https://github.com/owner/repo/tree/branch/path/to/SKILL.md) skill
```

### Step 5 — Verify

1. Confirm the replaced URL resolves (Step 3).
2. Confirm no remaining local-path references exist for the same file:

   ```bash
   grep -n '<old-local-path>' <file>
   # should return nothing
   ```

3. Confirm the gitignored path is no longer referenced:

   ```bash
   git check-ignore -v <old-relative-path>
   # still gitignored (that's fine) — what matters is no committed file links to it
   ```

## Script

[`scripts/detect-gitignored-refs.py`](scripts/detect-gitignored-refs.py) —
scans committed markdown files for link targets and inline paths that
resolve to gitignored locations, and outputs a report with suggested
remediations.

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| Repository-specific composer skills | Invoke Step 1–Step 5 of this base skill during their post-drafting audit, applying the detection to their own file paths and resolving with the relevant public URLs for their dependencies. |

## Related Skills

- [`gitignore-rules`](../gitignore-rules/SKILL.md) — authoring and auditing `.gitignore` rules
- [`redaction-portability`](../redaction-portability/SKILL.md) — broader portability rules for public-scope artifacts
- [`mrt-configuration-debug`](../mrt-configuration-debug/SKILL.md) — concrete example: references a gitignored `playwright-cli` local path resolved to public URL
- [`git-commit-dangling-link-audit`](../git-commit-dangling-link-audit/SKILL.md) — sibling audit: classifies IGNORED targets (link audit delegates them out)
