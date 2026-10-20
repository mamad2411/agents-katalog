---
description: Audit the OS. Say "audit the OS" or "give me a health report" (or run /founder-os:audit). Composite report across readiness, lint, wiki state, brain staleness, and voice completeness. Read-only unless the user approves wiki-build.
allowed-tools: ["Read", "Glob", "Grep", "Bash"]
---

# Founder OS audit

Run the audit skill at `skills/audit/SKILL.md` end to end.

## Procedure

1. If `core/identity.md` does not exist, reply `Founder OS not set up here. Say "set up Founder OS" first.` and stop.
2. Read `skills/audit/SKILL.md`.
3. Run the five checks named in the skill.
4. Use parallel sub-agents when the environment supports them. If not, run the checks in sequence and mark the report `parallel: unavailable`.
5. Ask before running wiki-build because it writes to `brain/relations.yaml`.
6. Render only the composite report.

## Rules

- Read-only unless the user approves wiki-build.
- No raw sub-check dumps in the final output.
- No em dashes or en dashes.
- No banned words.

<!-- private-tag: not applicable: audit reads and reports; any brain/ reference is to files being read, not user-speech writes -->
