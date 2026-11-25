---
name: transcript-to-action-plan-email
description: turn an sbdc client meeting transcript into a neoSerra-ready follow-up email from a maryland sbdc consultant, with actionable checklists and the required section headers (next steps, accomplishments since our last meeting, notes, relevant links). use when the user uploads/pastes a transcript (txt/docx/pdf) and wants a detailed client recap plus a follow-up menu of tailored deliverable options, including an option to map outcomes to nexus/neoserra milestones and counseling dropdown selections.
---

# Transcript To Action Plan Email

## Quick start
1. If the user provides a transcript file, read it (docx/pdf/txt).
2. If python is available, run `scripts/transcript_extract.py` to produce a JSON bundle.
3. Draft the client email using the required headers and tone.
4. After the email, output a **Follow-up Menu** table with lettered options.

## Workflow

### Step 1: confirm inputs
- If no transcript is provided, ask the user to upload/paste the transcript.
- If the transcript is partial (e.g., only highlights), proceed but note that the summary is based on partial content.

### Step 2: extract useful structure (prefer script)
If python execution is available:
- Save the transcript to a local file path.
- Run:
  - `python scripts/transcript_extract.py --input <path>`
- Use the JSON output as a guide (urls, client id candidates, gist sentences, milestone keyword hits).

If python is not available:
- Extract urls and any client id code manually.
- Continue with best-effort categorization.

### Step 3: identify client metadata
Best-effort extract:
- client first name (for greeting)
- client company name
- client id code (e.g., "HO1024")

Rules:
- If the id code is missing, use "Client ID".
- If company name is missing, use "Client Company".
- Do not block drafting on missing metadata; use placeholders and proceed.

### Step 4: draft the email
Follow the format rules in `references/email_format.md`.

Hard requirements:
- professional tone, no emojis.
- include these section headers exactly and in this order:
  1) Next Steps
  2) Accomplishments Since Our Last Meeting
  3) Notes
  4) Relevant Links

Content requirements:
- Next Steps: prioritize the client’s actions; use checklist-style items and include enough detail to execute.
- Accomplishments: call out progress since last meeting; highlight any milestone(s) using the milestone list in `references/milestones.md`.
- Notes: capture the meeting content; include mini-checklists for any process/method/tactic discussed.
- Relevant Links: include links mentioned/shared; one per bullet with short label if possible.

Milestone handling:
- If the transcript suggests a milestone, include it as a clearly labeled bullet under **Accomplishments Since Our Last Meeting**.
- If ai tools were implemented or improvements were realized due to ai, include the corresponding ai milestone(s) from `references/milestones.md`.

### Step 5: append the consultant signature block
- If the user provides a signature block, paste it.
- Otherwise, insert `[Consultant Signature Block]` placeholder.

### Step 6: provide a follow-up menu
After the draft email, output `Follow-up Menu` as a table following `references/followup_menu.md`.

Hard requirements:
- letter each option.
- always include option **A**: "Map this directly to Nexus/NeoSerra milestone and counseling dropdown selections and auto-generate the exact NeoSerra dropdown selections".
  - if the dropdown taxonomy is not available, label the selections as **best-effort** and suggest adding the taxonomy to `references/neoserra_taxonomy_placeholder.md`.
- always include at least one option explicitly labeled **high value, minimum effort**.

## Output template

### Email
- Provide the full email draft from subject line through signature block.
- Do not include analysis or internal reasoning.

### Follow-up menu
- Provide immediately after the email.
- Encourage the user to pick an option letter to continue.

## Resources
- `scripts/transcript_extract.py`: extract urls, id candidates, gist sentences, and milestone keyword hits.
- `references/email_format.md`: required headers, subject format, and tone.
- `references/milestones.md`: milestone definitions to highlight in accomplishments.
- `references/followup_menu.md`: rules and table structure for follow-up menu.
- `references/neoserra_taxonomy_placeholder.md`: place to paste dropdown lists for exact mapping.
