---
name: orchestra-intake
description: >
  Classify and file every newly installed skill, plugin, MCP, connector, or agent into the right
  orchestra — never archive. Use whenever the user installs/adds a new repo, skill, plugin, MCP
  server, or agent ("I installed X", "added Y", "npx skills add Z", "new repo", "set up this MCP",
  "just got this connector"). Runs the security scan, classifies the tool, places it in an
  orchestra with usage notes, logs the assignment, and reports back. This is the self-organizing
  layer of the orchestra system.
---

# Orchestra Intake — File New Tools, Never Archive

When the user adds anything new to the ecosystem, this skill files it into the right orchestra so it
is used at 100% efficiency from day one. **Nothing gets dumped undifferentiated; nothing gets
archived on arrival.**

## Process (run for every new install)

### 1. Security scan FIRST (mandatory, no exceptions)
Run the 5-step `~/.claude/workflows/import-security-scan.md`:
source verification → code scan → npm/socket check → skill/MCP source review → SAFE/CAUTION/REJECT.
- **REJECT** → do not install/keep. Tell the user why. Stop.
- **CAUTION** → surface the risk, get the user's explicit go before filing.
- **SAFE** → proceed to classify.

### 1b. Bulk-install fixture check (MANDATORY after any `npx skills add <repo>`)
`npx skills add` walks the **entire repo tree** and installs every `SKILL.md` it finds —
including test fixtures. After adding any multi-folder repo, inspect `~/.agents/.skill-lock.json`
for entries whose `skillPath` contains **`tests/`, `fixtures/`, `examples/`, or `.test-client/`**.
Those are NOT real skills — quarantine them to `~/.claude/_archive/` and remove their lock entries.
**A security-scanner's repo is the most dangerous to bulk-install from: its test suite contains
malware by design** (e.g. snyk/agent-scan shipped a malicious `base-trading-agent` fixture that
loaded a prompt-injection into the roster for 20 days — see
`docs/learnings/2026-05-21-malicious-skill-from-scanner-fixtures.md`). Also flag the multi-folder
`--skill=` quirk: targeted flags are IGNORED on multi-folder repos, so the WHOLE repo lands — prune after.

### 2. Identify what it is
- Skill (`SKILL.md`) · Plugin (package w/ agents/skills/commands) · MCP server (settings.json) ·
  Connector (claude.ai) · Agent (`~/.claude/agents/`).
- Read its description/frontmatter to understand WHAT it does and WHEN it triggers.

### 3. Classify into an orchestra
Match the tool's purpose to one (or more) of the 22 orchestras in
`~/.claude/rules/orchestra-system.md`. Decision aid:

| If the tool is about… | File into |
|---|---|
| code, framework, deploy, testing | ① BUILD |
| UI, design, visual, animation | ② DESIGN |
| research, scraping, intel | ③ RESEARCH |
| social, campaigns, brand | ④ MARKETING |
| copy, writing, content | ⑤ CONTENT |
| search ranking, schema, AI-answers | ⑥ SEO+GEO |
| leads, prospecting, CRM, sales | ⑦ LEAD GEN |
| product strategy, PRD, discovery | ⑧ PRODUCT |
| video, image gen, media | ⑨ VIDEO+MEDIA |
| metrics, analytics, experiments | ⑩ ANALYTICS |
| memory, graphs, notes, search | ⑪ KNOWLEDGE |
| docs, decks, spreadsheets | ⑫ DOCUMENTS |
| paid ads, PPC | ⑬ PAID ADS |
| automation, workflows, ops | ⑭ AUTOMATION |
| AI/ML, agents, MCP-building | ⑮ AI/ML |
| iOS, Swift, mobile | ⑯ iOS/SWIFT |
| planning, PM, sprints | ⑰ PLANNING |
| conversion, retention, pricing | ⑱ GROWTH |
| investing, valuation, finance | ⑲ PERSONAL FINANCE |
| strategy, exec counsel, board-level advice | ⑳ EXECUTIVE ADVISORY |
| verification, QA gates, evidence review | ㉑ AUDIT |
| security, pentest, detection, hardening | ㉒ CYBERSECURITY |
| off-domain vertical/game/XR | ⓪ RESERVE BENCH (dormant) |

- A tool can join **multiple** orchestras (e.g. an MCP useful to BUILD + AI/ML). List all.
- If genuinely off-domain (a new vertical/game/XR tool), file to **Reserve Bench** — installed,
  dormant, named-invoke only. Do NOT archive.
- If no orchestra fits and it's clearly valuable, propose a NEW orchestra to the user.

### 4. File it
- Add the tool to the relevant orchestra's roster in `~/.claude/rules/orchestra-system.md`
  (First Chair if core to the orchestra, Section if supporting).
- If it needs a trigger, add it to the router's quick table in
  `~/.claude/skills/orchestra-router/SKILL.md`.

### 5. Log the assignment
Append to `~/.claude/docs/learnings/orchestra-assignments.md`:
`YYYY-MM-DD · <tool> · type · → Orchestra(s) · why · scan result`

### 6. Refresh the skill index (mandatory)
After filing, rebuild the skill discovery index so the new tool is immediately visible
to `skill-selector`'s semantic retrieval. Run this before reporting back:

```bash
~/.claude/scripts/build-skill-index.sh --no-embed
```

This takes ~10-30 seconds (writes stubs + updates `.orchestra-scan.md`). The full vector
re-embed happens automatically at next session start via the SessionStart hook, or
immediately with `qmd embed` if you want retrieval now.

**Why this is mandatory:** `skill-selector` uses qmd semantic search over the stub index
to find the best skill. A newly-filed skill won't be discoverable until the index is rebuilt.
The "no skill wasted" guarantee only holds if the index stays current.

### 7. Tell the scriber + report back
Per the skills-protocol, inform the scriber so it's documented, then report to the user:
```
✅ Filed <tool> → <Orchestra> (<role>). Security: SAFE. Triggers on: <phrases>.
   Now part of your <orchestra> team alongside <related tools>.
   Skill index refreshed — discoverable via semantic retrieval immediately.
```

## Principles
- **Never archive on install.** Filing > archiving. Even off-domain tools stay live on the bench.
- **Security scan is non-negotiable.** Nothing is filed before it passes.
- **Explain the why.** Every assignment is logged with reasoning so it survives sessions.
- **Keep the constitution current.** The orchestra-system.md rule is the source of truth — update it.
