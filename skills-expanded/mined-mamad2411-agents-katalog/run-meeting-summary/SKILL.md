---
name: run-meeting-summary
description: 'Manual-invocation skill — run only when the user explicitly asks for "run-meeting-summary" or invokes it as a slash command. Do not auto-trigger on adjacent topics. Resolve meeting artifacts from loose requests, pasted text, local files, or provider connectors; draft a company-safe Obsidian summary; require a submit/edit/discard review gate before writing.'
---

# run-meeting-summary

Turn a meeting artifact into a concise Dark Matter work summary that is safe to share across the company, then let the user review, edit, and explicitly submit it to Obsidian.

## Core contract

This skill is provider-agnostic. It must work from:

- Loose natural language, such as "import my last meeting from Granola", "import my last one-on-one with John Doe", "summarize yesterday's nixmac sync", or "import my latest MeetJamie note".
- A pasted transcript, rough notes, or existing meeting summary.
- A local file path, exported markdown/text/PDF, or provider URL.
- Any available meeting connector or local export, including Granola, Fireflies/Firefly, MeetJamie/Jamie, Google Meet notes, Zoom transcripts, Google Docs, Slack huddles, or calendar-linked notes.

Do not require the user to paste an artifact or provide an explicit path if the request gives enough provider, participant, title, or time hints to search available sources.

## Workflow

1. Resolve the source artifact.
   - Prefer an explicit pasted artifact, file path, or URL when present.
   - If the user gives a loose request, extract provider hints, participant names, title hints, date ranges, and meeting type hints.
   - Search available connectors, local exports, calendar metadata, and likely provider folders using those hints.
   - If there is one high-confidence match, proceed without asking.
   - If there are multiple plausible matches, show a short picker with date, title, provider, and participants.
   - If there is no match, say what was checked and ask for an export, paste, path, or narrower hint.
   - Never invent meeting content from a title, calendar event, or memory.

2. Normalize the source.
   - Identify provider, source path or URL, meeting date, title, participants, and whether the input is a transcript, rough notes, or already a summary.
   - If possible, compute a stable source fingerprint from the raw artifact or provider ID.
   - Do not persist the raw transcript or source artifact by default.

3. Check for duplicates before drafting.
   - Search the likely target project area first, then the broader Dark Matter project area.
   - Compare source fingerprints, provider IDs, source URLs, meeting date plus title, and distinctive headings.
   - If a likely duplicate exists, show it and ask whether to update that note, create a separate note, or stop.

4. Produce a company-safe summary.
   - If the source is already a summary, improve structure and run the safety policy anyway.
   - If the source is a transcript or rough notes, convert it to a brief work summary.
   - Preserve decisions, action items, open questions, project context, and follow-up owners when supported by the source.
   - Remove private, personal, gossip-adjacent, and non-work material under the safety policy.
   - Do not include direct quotes unless they are clearly work-product and safe for broad internal sharing.

5. Choose the Obsidian destination.
   - Resolve the vault from `DM_OBSIDIAN_VAULT`, then the operator's configured Obsidian vault if discoverable.
   - Do not assume a particular teammate's local vault path.
   - Use the existing project structure. Do not create new top-level folders.
   - Prefer these destinations:
     - `Projects/darkmatter/nixmac/` for nixmac meetings.
     - `Projects/darkmatter/Titan/` for Titan meetings.
     - `Projects/darkmatter/USDC/` for USDC or stablecoin meetings.
     - `Projects/darkmatter/general/` for cross-company or unclear Dark Matter meetings.
   - If the vault structure differs, inspect `INDEX.md` and nearby project notes before choosing.

6. Present a review gate.
   - Show the proposed destination path.
   - Show duplicate-check results.
   - Show a safety report listing removed categories, not removed sensitive details.
   - Show the exact draft note.
   - Offer three clear choices: submit, edit, or discard.

7. Submit only after explicit approval.
   - If the user says submit, save the exact approved note to Obsidian.
   - If the user edits or asks for changes, revise the note and rerun the safety policy before presenting it again.
   - If the user discards, do not write anything.

## Safety policy

Use `reference/safety-policy.md` as the detailed policy. The summary must exclude:

- Personal life details, relationships, family matters, health details, finances, travel logistics, or anything unrelated to work.
- Gossip, rumors, venting, speculation about motives, or conversational color about teammates.
- Feedback about a named teammate unless it is already formalized as neutral work process, a decision, or an action item.
- Compensation, HR-sensitive details, recruiting-sensitive details, personnel decisions, or interpersonal conflict.
- Customer, user, candidate, or counterparty PII.
- Credentials, API keys, secrets, private URLs, wallet-private material, account IDs, phone numbers, email addresses, and physical addresses.
- Legal strategy, privileged material, investor-sensitive material, or incident-response details unless the user explicitly chooses an appropriate restricted destination.
- Direct quotes that preserve avoidable personal or sensitive context.

When uncertain, omit the detail and keep the work-relevant conclusion.

## Note format

Use `reference/obsidian-template.md` as the base format. Default frontmatter:

```yaml
---
type: meeting
origin: meeting-summary
state: working
people: []
tags:
  - meetings
created: YYYY-MM-DD
updated: YYYY-MM-DD
meeting_date: YYYY-MM-DD
---
```

Put source and safety metadata in the body, not custom frontmatter fields, unless the target folder already has a stronger local convention.

## Review gate format

Before writing, present:

```markdown
Destination: Projects/darkmatter/<project>/YYYY-MM-DD <slug>.md
Duplicate check: <none found | possible duplicate at ...>
Safety check: <passed with removals | passed with no removals | needs user decision>

Removed categories:
- <category only>

Draft:
<full note>

Reply with:
- submit
- edit: <changes>
- discard
```

Do not save until the user explicitly chooses `submit` or otherwise clearly asks you to write the note.

## Manual evaluation

Use the files in `fixtures/` to sanity-check behavior before changing this skill:

- `fixtures/unsafe-transcript.md`
- `fixtures/already-summary.md`
- `fixtures/duplicate-note.md`
- `fixtures/expected-rubric.md`

The skill passes when it can resolve a loose request, produce a safe summary, detect a plausible duplicate, avoid retaining raw artifacts, and present a review gate before writing.
