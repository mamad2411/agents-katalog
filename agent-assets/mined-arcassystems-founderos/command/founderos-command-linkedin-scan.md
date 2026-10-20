---
description: Turn your own LinkedIn export into a ranked outreach worklist, free and local. Fires on "scan my LinkedIn network", "rank my LinkedIn connections", "who in my network fits my ICP", "build my outreach list from my connections", or a dropped LinkedIn export ZIP (or run /founder-os:linkedin-scan <export.zip or folder>). Scores every connection locally against an ICP you set and writes a ranked CSV plus an interactive HTML, with an anonymised demo view safe to share. No scraper, no automated actions, message content never read.
argument-hint: "<export.zip | export-folder> [--icp my-icp.yaml]"
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# LinkedIn network scan

One-command entry point for the `linkedin-network-scan` skill. Point it at your LinkedIn data export and get back a ranked worklist plus an interactive page, scored locally against an ICP you control. The raw CSVs never enter the conversation - a deterministic, LLM-free script collapses them to a compact digest first.

Argument: `$ARGUMENTS` - the path to the export ZIP or unzipped export folder, with an optional `--icp <file>`. If no path is given, ask for one.

## Procedure (in order)

1. Read the skill at `skills/linkedin-network-scan/SKILL.md` and follow it end to end. The skill owns the flow: the export gate, the ICP choice, the local run, and reading only the compact digest.

2. The whole run is one command the skill issues:

   ```
   python skills/linkedin-network-scan/scan.py <export> <output-folder> --icp <icp.yaml>
   ```

   - `<output-folder>` MUST be outside any git repo - it holds real names and profile URLs. The user's home directory or Desktop is fine.
   - `--icp` is optional. Two example ICPs ship with the skill (sales / partnership and career / talent). Omit it for the permissive default and say so.

3. After the run, read ONLY `network-scan.md` (the compact ranked digest). Do not read the CSV, the JSON, or the raw export - that is the token waste this skill exists to avoid. Then summarise: how many connections were read, how many qualified, how many replied before, and how many invitations are pending. Point the user at `network-scan.html` (anonymised demo, safe to record and share) and `network-scan-full.html` (real names and links, local only).

4. If the run prints a freshness warning (export older than ~30 days), relay it and the re-pull steps before treating the worklist as current.

## Rules

- This command is a thin trigger. All logic lives in the skill. Do not duplicate the steps here.
- The scoring engine is deterministic and free-plan only - no scrapers, no paid tools, no API calls. Only optional narrative or synthesis afterward uses the session's own Claude.
- Never analyse an export the user did not personally download. Refuse on consent grounds.
- Output files hold real names and URLs. Tell the user to keep the output folder local and never commit it.
- If the skill file is missing, reply: `LinkedIn scan skill not found at skills/linkedin-network-scan/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.
- No em dashes or en dashes. Hyphens only with spaces.
