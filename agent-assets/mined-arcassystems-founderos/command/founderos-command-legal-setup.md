---
description: Set up the legal-compliance skill for your jurisdiction. Walks through jurisdiction selection, source loading, and deadline capture into context/compliance.md. Run once at install; re-run after a fiscal year change or move.
argument-hint: "(no arguments)"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebFetch"]
---

# Legal & Compliance Setup

Interactive wizard that wires the `legal-compliance` skill to your jurisdiction. Run once at install, or after a material change (fiscal year, jurisdiction, business structure).

This command is a thin trigger - the heavy lifting lives in `skills/legal-compliance/SKILL.md`.

## Procedure

1. **Verify install.** If `core/identity.md` does not exist, reply: `Founder OS not set up here. Say "set up Founder OS" first.` and stop.

2. **Read the legal-compliance skill** at `skills/legal-compliance/SKILL.md`. If it is missing, reply: `legal-compliance skill not found. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.

3. **Run the interview.** Ask ONE question at a time. Wait for the answer before moving on.

### Q1 - Jurisdiction

Ask: "What jurisdiction does your business operate under? Examples: UAE, UAE-DIFC, UAE-ADGM, US-Delaware-LLC, UK-Ltd, IN-Karnataka-Pvt-Ltd, SG-Pte-Ltd, AU-Pty-Ltd. If you operate across multiple, name your primary one - we can add others later."

Map the answer to a folder slug (lowercase, dash-separated). Examples:
- "UAE" or "Dubai mainland" → `uae`
- "DIFC" → `uae-difc`
- "Delaware LLC" → `us-delaware-llc`
- "UK Ltd" → `uk-ltd`

Check whether `skills/legal-compliance/references/<slug>/` already exists.

- **UAE / UAE-Dubai-Mainland / UAE-Abu-Dhabi-Mainland:** maps to existing `references/uae/` folder. Skill is ready to answer.
- **UAE-DIFC / UAE-ADGM:** also uses `references/uae/` (each domain file has DIFC/ADGM sections). Note in the response that DIFC/ADGM are separate common-law regimes and the skill flags them on every answer.
- **Anything else:** the folder does NOT exist. Continue to Q2.

### Q2 - (Non-UAE only) Confirm scaffold creation

If the jurisdiction folder does not exist:

Tell the user: "I don't have a reference set for `<jurisdiction>` yet. The skill ships with UAE as the worked example - your jurisdiction needs the same shape, populated with your country's gazetted sources. I'll create an empty scaffold under `references/<slug>/`. To start answering questions, you'll need to load at least three sources (tax authority, business law, labour law). Want to proceed? (yes / no)"

If yes:
- Copy `skills/legal-compliance/references/_template/README.md` to `skills/legal-compliance/references/<slug>/README.md`
- Copy `skills/legal-compliance/references/_template/sources.yml.template` to `skills/legal-compliance/references/<slug>/sources.yml`
- Edit the new `sources.yml`: replace `<YOUR-JURISDICTION>` with the slug, set `last_full_review:` to today's date, leave the example sources commented for the user to fill via `/founder-os:legal-add-source`.

If no: tell the user "OK - run `/founder-os:legal-setup` again when you're ready. The skill will refuse to answer legal questions for `<jurisdiction>` until the scaffold exists." and stop.

### Q3 - Write jurisdiction to identity

Show: "I'll add `jurisdiction: <slug>` to your `core/identity.md`. This tells the legal-compliance skill which folder to load. Proceed? (yes / no)"

If yes:
- Read `core/identity.md`
- If it has no `jurisdiction:` field, append it under the appropriate section (look for a "Business" or "Operating" section; if none, add a new line near the top)
- If it has one, ask whether to replace it
- Write the change

If no: skip this step but warn that the skill will keep asking for jurisdiction on every invocation until identity is updated.

### Q4 - Fiscal year end

Ask: "When does your fiscal year end? Examples: Dec 31, March 31, May 31. Used to calculate corporate tax and audit deadlines."

Capture as MM-DD format (e.g., `12-31`, `03-31`).

### Q5 - Business structure / license type

Ask: "What's your business structure? Examples: UAE mainland LLC, DMCC FZ-LLC, US Delaware LLC, UK private limited (Ltd), Indian private limited. Drives which obligations apply (Emiratisation, BOI filings, transfer pricing)."

Capture verbatim. Do not try to map to a token.

### Q6 - Active obligations capture

Ask, ONE at a time:

1. "Do you have a trade license or company registration that needs annual renewal? If yes, what's the next renewal date?" (YYYY-MM-DD or "skip")
2. "Do you file VAT/GST/sales tax returns? If yes, what's the next filing date?" (YYYY-MM-DD or "skip")
3. "Are you registered for corporate tax? If yes, what's the filing deadline this year?" (YYYY-MM-DD or "skip")
4. "Any team visas / work permits expiring in the next 12 months? If yes, list the earliest 1-3 dates." (YYYY-MM-DD list or "skip")
5. "Any contracts with auto-renewal clauses where you'd want a 30-day heads-up? If yes, list 1-3 contract names + renewal dates." (free text or "skip")

For each "yes" answer: prepare an entry for `context/compliance.md`.

### Q7 - Write context/compliance.md

If `context/compliance.md` already exists, read it. Append new entries; do not overwrite existing.

If it does not exist:
- Read the template at `skills/legal-compliance/templates/compliance.md.template`
- Replace `{{JURISDICTION}}` with the slug, `{{FISCAL_YEAR_END}}` with the MM-DD captured in Q4, `{{TODAY}}` with today's date
- Populate the "Upcoming Filings & Renewals" block with the entries from Q6
- Write to `context/compliance.md`

### Q8 - (Non-UAE only) Surface the next step

If a non-UAE scaffold was just created, tell the user:

"Scaffold ready at `references/<slug>/`. Three sources to add before the skill can answer questions:

1. Your tax authority (e.g., the IRS, HMRC, IRAS, ATO)
2. Your country's business law / Companies Act
3. Your country's labour law / Employment Act

Add each via `/founder-os:legal-add-source <url-or-pdf>`. The skill will tell you which source it's missing the first time you ask a question it can't answer.

Until at least one source is loaded, the skill will refuse to answer legal questions for `<slug>` (won't make up law)."

### Q9 - Confirm

Show a one-screen summary:

```
Legal-compliance setup complete.

Jurisdiction: <slug>
Fiscal year end: <MM-DD>
Business structure: <free text>
Reference folder: skills/legal-compliance/references/<slug>/
Compliance tracker: context/compliance.md (<N> deadlines captured)

Next:
- Ask any legal question - the skill will load <slug> references and answer.
- Run /founder-os:legal-update quarterly to refresh source freshness.
- Add new sources via /founder-os:legal-add-source <url>.

The SessionStart hook will surface any compliance.md deadline within 30 days.
```

## Rules

- Ask ONE question at a time. Wait for the answer.
- If the user dumps multiple answers in one reply, parse all of them and skip ahead. Confirm what you captured in one line.
- If the user says "skip" on any question, leave that field empty and continue. Do not push back.
- Never invent jurisdiction-specific law during setup. If asked "what are my obligations?", reply: "I'll know once we load your jurisdiction's sources. Add them by saying "add a legal source" and I can advise."
- No em dashes or en dashes anywhere in output.

<!-- private-tag: not applicable: writes structured compliance scaffolding from a template; not user-provided speech content -->
