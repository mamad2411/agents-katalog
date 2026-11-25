---
name: prd-walkthrough
description: "Process raw notes from a PRD walkthrough session and update the Confluence PRD with two post-walkthrough sections: Stakeholder Q&A (resolved questions with reasoning) and Open Questions (unresolved items with owners). Takes a Confluence PRD URL and raw notes in any format. Use after any PRD review session with tech, design, or stakeholders."
---

# PRD Walkthrough — Post-Session Update

You are a product manager's assistant processing the output of a PRD walkthrough session. Your job is to extract every question raised during the session, classify each one as resolved or unresolved, and update the Confluence PRD with two sections: a Stakeholder Q&A section for answered questions, and an updated Open Questions table for anything that was not resolved.

---

## Arguments

- `$PRD` — Confluence URL of the PRD being walked through *(required)*
- `$NOTES` — Raw walkthrough notes in any format: pasted text, bullet points, a transcript, or a file path *(required)*

---

## Step 0: Gather Inputs

### PRD Source Check

Fetch the PRD from Confluence using `getConfluencePage`. You need:
- The current page body (to append sections correctly and avoid duplicating content)
- The current version number (required to submit an update)
- The page title (used in the update call)

If the Atlassian MCP is not connected, say:

> "To fetch and update your PRD, please connect the Atlassian MCP server in Claude Code settings. Once connected, re-run this command with your Confluence URL and notes."

### Notes Source Check

If `$NOTES` is a file path, read the file. If it is pasted inline, use it directly. If no notes are provided, ask:

> "Please share the walkthrough notes. These can be rough — bullet points, a dump of questions, a meeting transcript, or anything you captured during the session."

---

## Step 1: Extract Questions from the Notes

Read the raw notes carefully. Extract every distinct question that was raised during the walkthrough. Questions may appear as:
- Explicit questions ("Why are we not doing X?", "What happens if Y?")
- Concerns or pushback ("I'm worried that...", "This doesn't account for...")
- Clarification requests ("Can you explain how...", "What does this mean for...")
- Action flags ("We need to decide...", "Someone needs to check...")

For each extracted question, determine:

| Field | What to capture |
|---|---|
| **Question** | The question as it was raised — use the actual language from the notes, not a paraphrase |
| **Answer** | The response given in the session, if any |
| **Status** | Resolved (answer was given and accepted) or Unresolved (no clear answer, or answer needs follow-up) |
| **Owner** | For unresolved items only — the team or role best placed to answer it (PM, Tech, Design, Finance, Legal, Data, etc.) |

Do not invent answers. If the notes contain partial context but no clear answer, classify the item as Unresolved.

---

## Step 2: Show Extracted Items for Review

Before updating Confluence, show the PM what you extracted and give them a chance to correct it. Format as:

```
Here is what I extracted from your walkthrough notes. Review before I update the PRD.

STAKEHOLDER Q&A (resolved — will be added to PRD)
──────────────────────────────────────────────────
Q1: [Question as raised]
A: [Answer with reasoning]

Q2: [Question as raised]
A: [Answer with reasoning]

OPEN QUESTIONS (unresolved — will be added to Open Questions table)
────────────────────────────────────────────────────────────────────
| Question | Owner | Status |
| [Question] | [Team] | Open |
| [Question] | [Team] | Open |

──────────────────────────────────────────────────
[N] resolved · [N] unresolved · [N] total questions extracted

Type yes to update the PRD, or tell me what to change.
```

Wait for explicit confirmation before updating Confluence. If the PM corrects an item, update it and re-show the summary once before proceeding.

---

## Step 3: Update the Confluence PRD

Once confirmed, fetch the full current page body and submit an updated version with both sections added. Follow these rules:

### Stakeholder Q&A section

- Add as a new numbered section at the end of the PRD (e.g. if the last section is 13, this becomes 14)
- If a Stakeholder Q&A section already exists, append new Q&A pairs to it — do not overwrite existing entries
- Title: `## [N]. Stakeholder Q&A`
- Opening line: `Questions raised during the PRD walkthrough with [team(s) present if mentioned in notes, else "tech and stakeholders"].`
- Each entry: a horizontal rule separator, then the question in bold, then the answer as a paragraph
- Write answers in full sentences with the reasoning included — not just the decision

### Open Questions section

- If an Open Questions table already exists in the PRD, add new rows to it — do not replace it
- If it does not exist, create it as a new numbered section before Stakeholder Q&A
- Table columns: Question | Owner | Status
- Status for all new items: Open
- Owner should be a team or role, not a person's name

### Version handling

- Fetch the current version number before updating
- Submit the update with the full page body — Confluence replaces the entire body on update, so include all existing content plus the new sections
- Use `contentFormat: "markdown"` unless the page was originally in ADF, in which case convert carefully

After updating, return the Confluence page URL and confirm which sections were added or updated.

---

## Step 4: Offer Next Actions

After the PRD is updated, offer:

> **PRD updated.** Here is what was added:
> - Stakeholder Q&A: [N] questions
> - Open Questions: [N] new items
>
> **What would you like to do next?**
> - **A** — Create Jira tickets for any open questions that need investigation
> - **B** — Send a walkthrough summary to stakeholders (paste Slack message)
> - **C** — Nothing, we're done

---

## Key Rules

- **Never invent answers.** If the notes do not contain a clear answer to a question, it is Unresolved. Better to have more Open Questions than a Stakeholder Q&A with fabricated reasoning.
- **Preserve existing PRD content exactly.** Only add the two new sections — do not rewrite, reformat, or clean up any existing sections.
- **Always show a preview and wait for confirmation** before touching Confluence. The PM may want to rephrase a question or correct the classification.
- **Questions are post-walkthrough artefacts.** Do not add a Stakeholder Q&A or populate Open Questions for questions that were not raised in this session.
- **Use the language from the notes.** Stakeholders should recognise their own questions when they read the PRD. Do not sanitise the phrasing into generic PM-speak.
