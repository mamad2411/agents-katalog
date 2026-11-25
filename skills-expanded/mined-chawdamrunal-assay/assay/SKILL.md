---
name: assay
description: Pre-install security advisor. Activate when the user mentions installing a Claude Code plugin, MCP server, or any third-party agent tool. Offer to run an Assay scan against the target before they install.
---

# Assay pre-install advisor

When the user is about to install a Claude Code plugin or MCP server — or when they ask whether a specific plugin is safe — proactively offer to scan it first using the `assay` binary.

## When to activate

- User says "install <plugin name>" or "add MCP server <name>"
- User asks "is <plugin> safe?" or "should I install this?"
- User clones or downloads an unfamiliar Claude Code plugin or MCP server source

## What to do

1. **Confirm the user wants a scan.** Ask "Want me to scan it with Assay first? (~$0.10-0.50 in tokens, but it'll catch credential exfiltration, prompt injection in tool descriptions, and capability-vs-claim mismatches.)"
2. **If yes, run the scan.** Shell out to `assay scan <target>`. The target is:
   - For a GitHub URL: download to a temp dir first, then scan that path
   - For an already-cloned local path: scan it directly
   - For a marketplace-named plugin: tell the user we don't yet auto-resolve marketplace names; ask them for the source path
3. **Show the verdict.** Assay writes `audit.md` and `audit.json` to `~/.assay/scans/<target>/<scan-id>/`. Summarize:
   - The verdict (SAFE / CAUTION / UNSAFE)
   - The top 1-3 findings if any
   - A link to the full report path
4. **Help the user decide.** If UNSAFE: recommend against installing and explain why. If CAUTION: surface the medium-severity findings and let them decide. If SAFE: green light, but note what Assay can't yet check (dynamic execution, runtime behavior).

## What NOT to do

- Don't run `assay scan` without asking — it costs the user real tokens.
- Don't claim a scan is "complete safety verification". Assay is a static analyzer; it doesn't catch runtime threats yet (Ring 2 work).
- Don't replace the user's judgment. Present the verdict + findings; the install decision is theirs.

## Reference

The 12 threat classes Assay hunts for are documented at:
`<repo-root>/docs/threat-model-2026.md`

If the user wants to understand what Assay IS scanning for, point them there.
