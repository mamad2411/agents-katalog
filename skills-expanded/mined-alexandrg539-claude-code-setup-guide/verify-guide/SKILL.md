---
name: verify-guide
description: |
  Re-verifies this guide against the latest official Claude Code sources and updates
  version stamps. Use when asked to update, re-verify, or check the guide for staleness,
  or when a Claude Code version newer than the one in chapter frontmatter has shipped.
allowed-tools: Read, Grep, WebFetch, Bash(python3 scripts/validate_guide.py*), Bash(npm view *), Bash(curl -s https://raw.githubusercontent.com/*), Bash(curl -sL https://code.claude.com/docs/*), Bash(claude --help), Bash(claude * --help)
---

# Verify Guide Against Official Sources

Evidence-first procedure (refined after the October 2026 pass, which found five flipped defaults and four broken samples after three months without verification).

1. **Delta.** Read `claude_code_version` from any chapter's frontmatter. Get the latest release: `npm view @anthropic-ai/claude-code version`. Fetch the official changelog (`https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`) and cut the entries newer than the stamped version into a scratch file.
2. **Snapshot sources.** For every page in every chapter's "Sources (official)" block, save the raw markdown (`https://code.claude.com/docs/en/<page>.md`; the page index is `https://code.claude.com/docs/llms.txt`) into a scratch directory with the date. Also save `anthropics/claude-code-action` `action.yml`, the official marketplace `marketplace.json`, and GitHub API / npm / PyPI state for every third-party item the guide names. Quote from snapshots, not from memory.
3. **Ledger.** Open a ledger file (claim | old | new | source file | verbatim quote | version | status). Every edit needs a row; a claim that cannot be verified in one attempt is dropped from the guide, not kept.
4. **Map and edit.** Map changelog entries to chapters via the README TOC. Edit in dependency order (Ch. 15 → 4 → 2 → 1/3 → 7 → 6/5 → 8/9 → 10/17 → 11/12 → 13/14 → 16 → README/llms.txt/templates). Bug fixes without behavior changes need no edits. Annotate changed behavior with `(2.1.xxx+)`; prune older history to one line; no star counts for third-party projects ("active as of <month year>" + link).
5. **Test samples.** Feed every `command` hook in Ch. 7 and Ch. 16 a pass and a block stdin fixture (branch hooks: inside a temp worktree too); parse every JSON/YAML sample (the validator does this); check every GitHub Actions `with:` key against `action.yml`; check CLI flags against `claude --help`; confirm model aliases with one `claude -p … --output-format json` call per alias if the model table changed.
6. **Blind re-check.** Have a fresh agent (not a fork, no ledger access) verify each edited chapter against the snapshots and report disagreements; resolve each against the ledger.
7. **Consistency.** grep for stale tokens (old model names, old version stamps, removed commands); keep frontmatter `read_when`, the README "Read when" column and llms.txt annotations in sync; update `verified` and `claude_code_version` on all chapters, the README header and the llms.txt stamp (Ch. 16 contains a sample frontmatter inside a code fence — never bulk-edit it); add What's-New rows for meaningful changes.
8. **Dogfood.** Run the README self-configuration procedure in a scratch project on the new CLI version in its default permission mode; anything that diverges from the text goes back to step 4.
9. Run `python3 scripts/validate_guide.py` and `python3 scripts/validate_guide.py --links`; fix anything reported.
10. Report: version delta, chapters changed, claims corrected, claims dropped, samples tested. Do not push without explicit user approval.
