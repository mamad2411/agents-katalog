---
name: finding-skills
description: Find and install agent skills through agentstack — search the library/catalog/registry, pull from any skills repo (owner/repo, git URLs, local dirs), and judge quality by scan verdicts, pins, and provenance instead of install counts. Use when the user asks "how do I X", "is there a skill for X", or wants a capability added.
---

# Finding skills

Use this skill when the user is looking for a capability that might exist as
an installable skill — "how do I work with PDFs here", "find a skill for
code review", "add the pdf skill from anthropics/skills" — or when you wish
you had domain instructions you don't have.

## Where skills come from

1. `agentstack search <query>` — the user's central library, the embedded
   catalog, and the official MCP Registry, in one pass. Results marked
   `(in manifest)` are already installed.
2. **Any skills repo on GitHub/GitLab** — the ecosystem publishes SKILL.md
   directories, and `agentstack add skill` speaks its conventions:

```bash
agentstack add skill anthropics/skills --list        # inspect a repo's skills
agentstack add skill anthropics/skills --skill pdf   # preview one (dry run)
agentstack add skill owner/repo@pdf                  # same, alias spelling
agentstack add skill https://github.com/o/r/tree/main/skills/pdf
agentstack add skill ./local-skill
agentstack more lib add owner/repo --skill pdf            # into the central library
```

Everything previews first. The dry run fetches into transient staging,
scans the content, and shows the manifest diff plus the exact digest that
would be pinned — nothing persistent changes until a human re-runs with
`--write`.

## Judge quality by evidence, not popularity

There are no install counts here, on purpose. The signals that matter:

- **Scan verdict** — the preview shows per-skill findings. High-severity
  findings (hidden Unicode) block the add; warnings deserve a read before
  you recommend proceeding.
- **Pin + provenance** — after a write, the lockfile pins the exact commit
  and content checksum, and `agentstack more explain <name>` shows where a skill
  came from and whether its content still matches its pin.
- **Description quality** — a skill without a frontmatter description is
  invisible to search and to agents; treat that as a smell.

## Rules for agents

- Propose, don't apply: run the dry run, show the user the preview, and let
  them re-run with `--write`. Never pass `--allow-flagged` yourself — a
  blocked scan finding is the user's decision.
- Prefer the central library for skills the user will want across repos
  (`agentstack more lib add …`, then reference by name in profiles); prefer the
  project manifest for repo-specific skills.
- After a write in a gateway-served (zero-files) project, remind the user
  that trust re-gates on the edit: they run `agentstack trust .` themselves
  — never run it for them.
- When nothing suitable exists, say so and offer to help directly; a new
  skill directory with a `SKILL.md` (name + description frontmatter) is all
  it takes to make the solution reusable.
