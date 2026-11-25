---
name: bumblebee-scan
description: Run a read-only Bumblebee supply-chain scan of this machine's installed packages, MCP configs, editor & browser extensions, and check them against curated threat-intelligence catalogs. Use when the user asks whether the system is clean, whether you have been compromised, or to investigate a recent security advisory. Read-only — makes no changes.
---

# When to use this skill

Use this when:
- The user asks if the system / machine / your environment is clean, compromised, or "looking healthy"
- A new supply-chain advisory dropped (npm worm, malicious VS Code extension, RubyGems exfiltration, etc.) and the user wants a check
- You want to ground a security answer in real data instead of guessing
- The user explicitly says "scan", "check packages", "bumblebee", "supply chain"

**Do NOT use this skill for:**
- General system health (CPU, GPU, uptime)
- File-level malware scanning — Bumblebee only checks package/extension metadata, not file contents
- Anything outside the current user's `$HOME`

# How to use

```bash
bash ~/.hermes/skills/bumblebee-scan/scan.sh
```

The script triggers the `bumblebee-scan.service` systemd user unit, waits for it
to finish (usually 5-15s), and emits the normalized scan summary as JSON to stdout.

# What's being scanned

Bumblebee inventories installed packages in your `$HOME` tree across:
npm / pnpm / Yarn / Bun, PyPI, Go modules, RubyGems, Composer, MCP server
configs, editor extensions (VS Code, Cursor, Windsurf, VSCodium), browser
extensions (Chromium, Firefox).

It matches them against curated `threat_intel/*.json` catalogs of known-compromised
package versions. Exact `(ecosystem, name, version)` matches only — high confidence,
no heuristics.

Bumblebee never executes package managers, never reads `.env` or token files,
and runs as your normal user (no sudo).

# How to interpret the result

- `findings_total: 0` → clean against all loaded catalogs. Report that.
- `findings_total > 0` → list entries from `findings_preview` (severity, ecosystem,
  package, version, catalog). These are exact matches against known-bad packages —
  high confidence. Recommend the user investigate immediately.
- `findings_new_since_last > 0` → something appeared since the last scan ran.
  Flag this explicitly even if total is unchanged.
- `status` should be `complete`. If it's `timed_out` or anything else, mention it.

# Reporting back

Reply in your usual voice. Concise. Do not paste the raw JSON; summarize.

- Clean: "Bumblebee just swept the environment — N packages inventoried, zero matches
  against the M active threat catalogs. We're clean."
- Findings: "Bumblebee flagged N items. One critical: npm/colors@1.4.44 (catalog: X).
  Recommend immediate removal."

# Privacy

Don't quote raw filesystem paths back in your reply. The bridge's redaction is the
safety net but be the first filter yourself.
