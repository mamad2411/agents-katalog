---
name: git-jq-pretty-json-filter
description: Composer skill that installs the jq-pretty Git clean+textconv filter for keeping minified JSON files pretty-printed inside Git so GitHub web and local diffs render line-by-line; pairs with narrow .gitattributes patterns (no wildcards) and delegates pre-filter backfill to git-clean-filter-renormalize-backfill.
category: Git-Hygiene
---

# Git jq-pretty JSON Filter (v1)

Tools that rewrite JSON files (VS Code, Copilot, build systems) often emit
minified output. Once committed, minified JSON renders as a single useless
line in `git diff` and on the GitHub web diff viewer. The only way to get
beautiful line-by-line diffs in **both** GitHub web and local `git diff`
is to store the blob in pretty form (textconv-only solutions don't reach
GitHub).

This skill installs a Git **clean filter** that pretty-prints matching JSON
files on `git add` (storing pretty) while keeping the working tree
untouched (`smudge = cat`), and a matching **diff textconv** so even
pre-filter blobs render pretty in `git diff`.

***

## 1. The filter spec

The literal Git config block this skill installs (verbatim):

```ini
[filter "jq-pretty"]
    clean = jq --indent 4 .
    smudge = cat
    required = true
[diff "jq-pretty"]
    textconv = jq --indent 4 .
    cachetextconv = true
```

Semantics:

- `clean` = `jq` → stored blob is pretty (4-space indent).
- `smudge` = `cat` → identity on checkout; working tree stays in
  whatever form the writing tool produced.
- `required = true` → fail loud on missing `jq` rather than silently
  storing minified.
- `diff.textconv` → `git diff` renders pretty even for blobs that
  predate the filter (works without rewriting history).
- `cachetextconv = true` → cache the prettified view for speed.

## 2. Environment & Dependencies

- `jq` on PATH (any recent version — `--indent 4` has been stable since 1.5).
- `git` >= 2.18.
- `python3` >= 3.12 (stdlib only).

## 3. Delivery options

Git deliberately refuses to honor filter configuration that ships in a
cloned repository (security — the clean script is arbitrary code). The
filter config must reach `git config` on the developer's machine through
one of these three paths:

### 3.1 Per-clone local config (explicit, lowest setup, highest friction)

Run [`scripts/install_jq_pretty_config.py`](scripts/install_jq_pretty_config.py)
with `--target .git/config` (or any file then `git config --local include.path`).
Drawback: every fresh clone needs the same one-time setup.

### 3.2 Symlinked global config (recommended for trusted private repos)

If the developer already maintains `$HOME/.gitconfig` as a symlink to a
tracked `.gitconfig` inside a configurations repository (a pattern
covered by the sibling `dev-env-private-config-symlink` skill in the
`ai-agents` repo), then committing the filter block to that tracked
`.gitconfig` instantly activates it on every machine where the symlink
exists — zero per-clone setup.

### 3.3 Global `include.path` (one-time per machine)

`git config --global include.path <abs/path/to/jq-pretty-fragment>`
loads the filter from a tracked fragment file. One-time setup per
machine, not per clone.

## 4. Narrow pattern mandate (no wildcards)

Each minified-JSON path family gets its OWN explicit `.gitattributes` line
of the form:

```text
<narrow-pathspec> filter=jq-pretty diff=jq-pretty
```

Wildcards like `**/*.json` or bare `*.json` are FORBIDDEN. Reasons:

1. **JSONC trap**: VS Code's `settings.json` and `keybindings.json` are
   JSONC (comments + trailing commas). `jq` REJECTS them. A wildcard
   would pull them in and every `git add` would fail.
2. **Already-pretty files**: most VS Code `storage.json`-class files
   are already pretty; matching them wastes the filter.
3. **Surfaceability**: when a new minified-JSON path family appears, it
   should require an explicit one-line addition (visible in PR review)
   rather than being silently swept up by a wildcard.

[`scripts/append_gitattributes_pattern.py`](scripts/append_gitattributes_pattern.py)
enforces this mandate: it refuses patterns starting with `**`, bare
`*.ext` patterns, or single-segment patterns without a `/`.

## 5. Worked-example patterns

Concrete narrow patterns established for a VS Code Insiders user-config
tracking repository:

```text
vscode-insiders-configuration/visual-studio-code-user-settings/profiles/*/extensions.json filter=jq-pretty diff=jq-pretty
vscode-insiders-configuration/visual-studio-code-user-settings/workspaceStorage/*/chatEditingSessions/*/state.json filter=jq-pretty diff=jq-pretty
vscode-insiders-configuration/visual-studio-code-user-settings/workspaceStorage/*/GitHub.copilot-chat/debug-logs/*/system_prompt_*.json filter=jq-pretty diff=jq-pretty
vscode-insiders-configuration/visual-studio-code-user-settings/workspaceStorage/*/GitHub.copilot-chat/debug-logs/*/tools_*.json filter=jq-pretty diff=jq-pretty
vscode-insiders-configuration/visual-studio-code-user-settings/workspaceStorage/*/GitHub.copilot-chat/debug-logs/*/models.json filter=jq-pretty diff=jq-pretty
```

## 6. Backfill of pre-filter blobs

When the filter is installed AFTER files were committed minified, the
existing stored blobs are unaffected — they will keep rendering as
single-line diffs on GitHub web until re-staged. Delegate the backfill
to the base skill
[`git-clean-filter-renormalize-backfill`](../git-clean-filter-renormalize-backfill/SKILL.md)
with the SAME pathspec(s) used in `.gitattributes`. That skill ships the
renormalize + dirty-skip + audit triad.

## 7. Operational Logic

1. **Install jq** (`brew install jq` / `apt install jq` / etc.).
2. **Choose delivery option** (§3) and run
   [`scripts/install_jq_pretty_config.py`](scripts/install_jq_pretty_config.py)
   against the appropriate target gitconfig file.
3. **Append the narrow pattern(s)** via
   [`scripts/append_gitattributes_pattern.py`](scripts/append_gitattributes_pattern.py).
4. **Commit** `.gitattributes` (and `.gitconfig` if delivered via §3.2)
   via [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
   — one commit per concern (filter install, attribute additions,
   backfill should be distinct commits).
5. **Backfill** any pre-filter blobs via the base skill (§6).
6. **Verify** that GitHub web (or `git diff`) renders matching files
   line-by-line.

## 8. Scripts

| Script | Purpose | Tier |
| --- | --- | --- |
| [`scripts/install_jq_pretty_config.py`](scripts/install_jq_pretty_config.py) | Idempotent install of `[filter "jq-pretty"]` + `[diff "jq-pretty"]` into a target gitconfig | Python 3.12+ stdlib |
| [`scripts/append_gitattributes_pattern.py`](scripts/append_gitattributes_pattern.py) | Idempotent narrow-pattern appender with wildcard refusal | Python 3.12+ stdlib |

Per [`scripting-language-selection-rules.md`](../../../ai-agent-rules/scripting-language-selection-rules.md)
§1, Python 3.12+ is the Tier 1 default. Wildcard refusal regex and
idempotent key probing are both Python-strength tasks (§3.3).

## 9. Composition Rationale

This skill is the **composer**; the base skill is
[`git-clean-filter-renormalize-backfill`](../git-clean-filter-renormalize-backfill/SKILL.md).
The split exists because the renormalize + dirty-skip + audit triad is
filter-agnostic and reusable by any future clean-filter installation
(LFS, prettier, secret-scrub, line-ending normalization). Inlining the
backfill logic here would violate the SSOT contract.

## 10. Related Skills

- [`git-clean-filter-renormalize-backfill`](../git-clean-filter-renormalize-backfill/SKILL.md) — base; pre-filter blob backfill.
- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
  — commit each concern (install / pattern / backfill) atomically.
- [`git-pre-execution-safety-stash`](../git-pre-execution-safety-stash/SKILL.md) — safety stash before backfill.
- `dev-env-private-config-symlink` (sibling `ai-agents` repo) — symlink-based
  delivery of `~/.gitconfig` from a tracked private repo (Delivery §3.2).

## 11. Traceability

Originated in a session on a private VS Code configurations repository.
GitHub web diffs of profile `extensions.json`, copilot debug-log JSONs,
and per-session `state.json` files were unreadable single-line minified
blobs; the filter+attributes pair plus pre-filter backfill made every
subsequent diff (web and local) line-by-line readable.
