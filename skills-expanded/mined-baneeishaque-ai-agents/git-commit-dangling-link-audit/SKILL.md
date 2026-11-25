---
name: git-commit-dangling-link-audit
description: >-
  Composer — pre-commit audit of markdown relative links: classify every link
  target as EXISTS / GIT_ONLY / DANGLES (missing from BOTH working tree and
  index) / IGNORED; for each DANGLES, invoke opencode-session-path-attribution
  to reproduce which session moved the path, then offer FOLD / RESOLVE-NOW /
  KEEP-AS-IS to the user. Never mutates files or runs git commit.
category: Git
---

# Git Commit Dangling-Link Audit (v1)

## Goal

Industrialized answer to the incident this suite grew from: "is this markdown
link still alive in the commit I am about to make?" A file may exist on disk
because an uncommitted reorder keeps it reachable — while the same link
DANGLES in the committed tree snapshot. This composer scans every relative
markdown link, classifies it against BOTH the working tree and the git
index, reproduces the responsible session for each DANGLES, and hands the
user a decision — it never writes or commits itself.

## Composition

- [`detect-dangling-links.py`](scripts/detect-dangling-links.py) — the
  deterministic scan (own script; needs no base).
- [`opencode-session-path-attribution`](../opencode/opencode-session-path-attribution/SKILL.md)
  — drift-gate evidence: which session touched the target path.
- [`opencode-installed-plugin-lookup`](../opencode/opencode-installed-plugin-lookup/SKILL.md)
  — transitive: locates the logger before attribution.

## Classification

| Class | Condition | Pre-commit action |
| --- | --- | --- |
| `EXISTS` | target on disk | OK |
| `GIT_ONLY` | absent on disk, present in git index | OK |
| `DANGLES` | absent from both tree and index | AUDIT (this skill) |
| `IGNORED` | on disk but gitignored | delegated out |

Links are extracted from NON-gitignored `*.md` files. Fenced code blocks and
inline code are skipped; only path-shaped targets (containing `.` or `/`)
are considered; `http://`, `file://`, `#`, `mailto:` are skipped.

## Protocol (BOLD = gate)

1. **Scope gate** — run before finalizing `git add` for any commit that
   touches or moves paths (rename/reorder/docs).
2. **Preview-sweep gate** — consult existing `docs/*_commit-preview*.md`
   and `scratch/commit-preview*` FIRST; reuse a prior plan if it covers the
   same movement — do not re-forensically bisect.
3. **Drift gate** — for each `DANGLES`: `git status --porcelain` on the
   target path; SIBLING-DRIFT (moved, uncommitted) → invoke
   `opencode-session-path-attribution` (Base #1) with `--path <target>`
   to attach an evidence card (session id, timestamp, tool, exact command).
4. **Decision gate (user gate)** — FOLD (fix in current commit) vs
   RESOLVE-NOW (dedicated commit + retarget) vs KEEP-AS-IS (record
   rationale). Always wait for the user.
5. **Prompt gate** — never mutate files, never `git add`, never `git
   commit`; emit evidence + invite list and wait.
6. **Verify + preview-sync gate** — re-run the scan after resolution
   (0 DANGLES on the fixed links), write findings back into the LIVE commit
   preview and re-lint it (markdownlint-cli2).

## CLI (deterministic scan)

```bash
python3 scripts/detect-dangling-links.py [--root <dir>] [--json]
```

| Flag | Meaning |
| --- | --- |
| `--root` | directory to scan (default `.`) |
| `--json` | emit one JSON array instead of JSONL |
| `--output` | write to file instead of stdout |

Exit: `0` no DANGLES, `1` ≥1 DANGLES, `2` usage. Diagnostics on stderr,
payload on stdout only.

## Prohibited Actions

- No file writes, no `git add`, no `git commit`, no `mv` — resolve via the
  user's decision only.
- Do not re-implement session attribution — delegate to Base #1.

## Related Skills

- [`opencode-session-path-attribution`](../opencode/opencode-session-path-attribution/SKILL.md)
  — evidence card provider (drift gate)
- [`deleted-files-audit`](../deleted-files-audit/SKILL.md) —
  complementary audit: deleted-by-move path is the dangling subclass
- [`gitignored-reference-detection`](../gitignored-reference-detection/SKILL.md)
  — sibling audit for IGNORED-target delegation
