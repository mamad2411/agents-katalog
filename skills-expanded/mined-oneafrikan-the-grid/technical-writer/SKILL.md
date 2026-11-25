<!--
  SKILL.md — Technical Writer operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific stack or project.
-->

# Skill: Technical Writer

## Invocation

```
/technical_writer <documents and/or the change to document>
```

Or picked up from a Signal Protocol entry / PR assigned to technical-writer. With
no scope given, audit the repo's documents against its code.

---

## Step 1 — List documents and their sources of truth

Pair each document with what it must be verified against:

| Document | Verify against |
|---|---|
| README (setup, usage) | entry points, package manifests, scripts, actually running the commands |
| CLAUDE.md / agent guidance | code layout, scripts, test and build config |
| API table / reference | route definitions, handlers, schemas |
| Env var reference | where the code or compose file reads each variable, `.env.example` |
| Command reference | scripts, Makefile, CLI definitions, `--help` output |
| Architecture / onboarding | actual modules, services, compose/deploy config |
| Changelog | git history, tags |
| Agent briefs (`.claude/agents`, skills) | the tools, paths and commands they cite |

Also list hand-synced mirrors (copies kept in sync by hand) by name.

## Step 2 — Read everything fully

- Read each document end to end, then the code it describes.
- Read the real code, compose, and config; do not take another document's word.
- Run commands where feasible.

## Step 3 — Build the discrepancy list

For each mismatch record: document, claim, what the code shows, fix.

- Check status words in both directions: "planned" that now exists, "exists" that does not.
- Check counts, names, paths, flags, defaults, versions.
- If the code looks wrong instead of the doc, mark it for the owning dev role; no doc edit.

## Step 4 — Fix with minimal edits

- Edit every affected document in the same pass, mirrors included.
- Change only the wrong sentence, row, or command; keep each document's voice and structure.
- Add no sections for things that do not exist.
- Re-run edited commands where feasible.

## Step 5 — Report

- One line per fix: file, what changed, what it was verified against.
- List code defects flagged, with the dev role they route to.
- If everything already matched, state that and make no edits.

---

## Checklist

- [ ] Every claim checked against code, not another doc
- [ ] "Planned" and "exists" correct in both directions
- [ ] All affected documents and mirrors updated together
- [ ] Commands copy-pasteable and run where feasible
- [ ] No cosmetic edits, no speculative sections
