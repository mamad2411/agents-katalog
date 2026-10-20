---
name: org-config
description: "Team org policy setup for Topia. Use during /topia finalize or when configuring .topia/org/org.md — asks structured questions and writes team roles, policies, approval flows, and governance level so guardian and readiness enforce your rules."
metadata:
  author: topia
  version: "1.0.0"
  layer: L2
  model: sonnet
  group: quality
  tools: "Read, Write, Edit, Glob, Grep"
  emit: org.configured
---

# org-config

## Purpose

Turn `.topia/org/org.md` from a template into **your team's real policy file**. `guardian` and `readiness` read this at compile time and inject an `<ORG-POLICY>` block into their hooks — so commit-time gates match how your team actually works.

**For teams:** commit `org/org.md` (under `.topia/`) so every developer and every agent session shares the same rules. Solo devs can still run this to set governance level and security defaults.

<HARD-GATE>
Do NOT delete any of the five required sections: `## Teams`, `## Roles`, `## Policies`, `## Approval Flows`, `## Governance Level`. Empty tables are allowed; missing headings break the parser.
</HARD-GATE>

## Triggers

- `/topia org-config` — manual invocation
- Called from `/topia finalize` after machine-wide setup (Step 2b)
- Auto-suggest when `org.md` still contains template placeholders (`_(lead`, `Organization: topia`, `_(team slug)_`)

## Calls (outbound)

- None required — this skill writes policy only

## Called By (inbound)

- User: `/topia org-config`
- `/topia finalize` command flow
- `tut` skill when user asks to configure team policy

## Output

- `.topia/org/org.md` — updated in place (preserve YAML frontmatter)
- `.topia/org/.configured` — timestamp flag (optional, write after successful save)

## Output Format

```text
Org policy configured for <org-name>

Governance: <loose|moderate|strict>
Reviewers: <N> required | security files need security reviewer: <yes|no>
Deploy: <window> | staging before prod: <yes|no>

Written: .topia/org/org.md
Teams: commit .topia/org/ so guardian/readiness enforce these rules in CI.

Refresh hooks if gates feel stale:
  node "<topia>/compiler/bin/topia.js" setup --global --preset gentle --yes
```

After writing, tell the user to re-run hook compile if they use terminal hooks:

```bash
node "<topia>/compiler/bin/topia.js" setup --global --preset gentle --yes
```

Claude-only users who finalized in chat: hooks pick up org policy on next `topia build` / plugin reload; if gates feel stale, run `/topia finalize` again or the setup command above.

## Executable Steps

### Step 1 — Load current file

1. `Read` `.topia/org/org.md`. If missing, copy structure from the plugin template at `skills/` repo path `.topia/org/org.md` or create from [`docs/ORG-CONFIG.md`](../../docs/ORG-CONFIG.md) example.
2. Note whether placeholders remain — if the file is already customized and user did not pass `--force`, confirm before overwriting.

### Step 2 — Interview (use AskUserQuestion)

Ask in **2–3 rounds** (multiSelect where noted). Adapt wording for solo vs team based on answers.

**Round A — Who are you?**

1. **Org / project name** (free text) — updates `# Organization: …` and frontmatter `name`
2. **Team shape** (single choice):
   - Solo developer (minimal teams table)
   - Small team (2–10, one engineering group)
   - Multi-team org (eng + frontend + security, etc.)

**Round B — Governance**

3. **Governance level** (single choice):
   - **Loose** — gates advise only; fast iteration
   - **Moderate** — block on HIGH/CRITICAL security and missing evidence (recommended for most teams)
   - **Strict** — block on most findings; regulated / high-risk

4. **Code review** (multiSelect or follow-ups):
   - Minimum reviewers (0 / 1 / 2)
   - Self-merge allowed? (yes / no)
   - Security-tagged files need security reviewer? (yes / no)

**Round C — Security & deploy (teams)**

5. **CVE response SLA** — 7 days HIGH/CRITICAL vs 30 days vs custom
6. **Production deploy window** — unrestricted / weekdays only / custom hours
7. **Staging required before production?** (yes / no)

**Round D — Roles (if team)**

8. Who maps to **maintainer** vs **contributor**? (short list or "use defaults")
9. Any **admin** override role? (name or "none")

Skip questions the user marks "defaults" — use Moderate governance and single-reviewer defaults.

### Step 3 — Write org.md

1. Update frontmatter `name` and `description` with org/project name.
2. Fill `## Teams` table — at least one row for small/multi team; for solo, one row "Core" with lead "self".
3. Fill `## Roles` with admin / maintainer / contributor / reviewer rows matching Round D.
4. Update `## Policies` subsections (Code Review, Security, Deployment, Branching) from Round B/C.
5. Set `## Governance Level` to chosen level; update the bullet list under it to match (enforce vs advisory per gate).
6. Keep `## Approval Flows` — at least one flow (Feature launch); add Hotfix if they deploy to production.

Use `Write` or `Edit` — preserve markdown tables and section order.

### Step 4 — Confirm and flag

1. Print a **short summary**: governance level, reviewers, deploy rules, what guardian/readiness will now enforce.
2. Write `.topia/org/.configured` with ISO timestamp.
3. Remind teams: `git add .topia/org/` and commit so CI and teammates share policy.
4. Link [`docs/ORG-CONFIG.md`](../../docs/ORG-CONFIG.md) for later edits.

## Constraints

1. MUST preserve all five section headings (`Teams`, `Roles`, `Policies`, `Approval Flows`, `Governance Level`) — empty tables are fine; missing headings break the parser.
2. MUST write to **project** `.topia/org/org.md`, never the plugin cache template.
3. MUST confirm before overwriting a customized `org.md` unless the user passed `--force`.
4. MUST NOT store secrets, API keys, or PII in `org.md` — it is committed to git.
5. MUST remind the user to refresh hooks (`topia setup --global`) after policy changes.

## Sharp Edges

| Edge | Impact | Mitigation |
|------|--------|------------|
| Editing `org.md` alone does not refresh hooks | HIGH | Tell user to run `topia setup --global --preset gentle --yes` or `/topia finalize` after save |
| Plugin cache `org.md` is a template, not live policy | MEDIUM | Always resolve project `.topia/org/org.md`; link `docs/ORG-CONFIG.md` for manual edits |
| Solo dev picks "multi-team" by mistake | LOW | Round A shapes later questions — offer "use defaults" to skip team tables |
| Governance level mismatch with team appetite | MEDIUM | Summarize what guardian/readiness will block before writing |

## Done When

- [ ] All five section headings present and parser-valid
- [ ] No template placeholders like `_(lead name` remain unless user explicitly kept them
- [ ] User saw summary of what gates will change
- [ ] `.topia/org/.configured` written (unless `--dry-run`)

## Cost Profile

- **Model:** `sonnet` — structured interview + markdown table authoring.
- **Tokens:** ~2k–4k across 2–3 AskUserQuestion rounds plus one Write.
- **Latency:** user-paced (interview); file write is sub-second.
- **Side effects:** writes `.topia/org/org.md` and optional `.topia/org/.configured`.
