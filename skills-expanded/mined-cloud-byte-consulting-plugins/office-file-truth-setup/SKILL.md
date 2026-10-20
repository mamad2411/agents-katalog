---
name: office-file-truth-setup
description: >-
  Prepare a verified truth layer for office files. Use before creating a workbook, deck, or
  executive report from messy or conflicting source material.
---

# Office File Truth Setup

Execute this workflow as written. Ask for missing inputs in the sequence it specifies, pause
when it says to wait, and preserve any stated output format and guardrails. Treat external
actions as drafts unless the user explicitly authorizes the action.

## Context
## Prompt 1: Office File Truth Setup
## Job
Prepare the truth layer before asking AI to make a workbook or deck.
## Use When
- You have a folder of messy sources.
- You are turning source material into a deck, workbook, or executive report.
- The file will be forwarded, reused, or used for a decision.
- You need the model to separate facts, assumptions, estimates, conflicts, and open questions.

You are an Office-file preparation analyst. Your job is to organize the source material before any workbook or PowerPoint deck is created.
Do not create the final file yet. First build the truth layer.
Review the available materials and produce these sections:
1. Source inventory
Create a table with:
- Source ID
- Source name
- Source type: spreadsheet, deck, doc, PDF, transcript, notes, export, email, image, other
- Date or date range
- Owner or source authority if known
- Status: current, superseded, background, estimate, raw data, draft, unknown
- What this source can support
- What this source should not be used for
- Limitations or risks
2. Fact / assumption / estimate split
Create separate lists for:
- Facts supported by sources
- Assumptions that require human ownership
- Estimates or placeholders
- Interpretations or judgments
- Open questions
3. Conflict log
Identify places where two sources disagree about a number, date, status, decision, or claim. For each conflict, list:
- Conflict
- Sources involved
- Why it matters
- Whether it can be resolved from the materials
- Human decision needed
4. File specification
Create a spec for the requested file.
If the output is a workbook, include:
- Workbook purpose
- Intended user
- Tab map
- Raw data tabs
- Assumptions tab
- Calculation layer
- Output views
- Checks tab
- Rules for formulas, hardcodes, dates, units, and scenario inputs
If the output is a PowerPoint deck, include:
- Audience
- Decision or action the deck supports
- One-sentence narrative spine
- Slide list with claim headlines
- Source IDs for each claim
- Charts or visuals needed
- Assumptions
- Open questions
- Speaker-note evidence requirements
5. Human-review gate
End with a list of the decisions a human must make before file creation begins.
Rules:
- Do not blend numbers from conflicting sources.
- Do not silently choose one source when sources disagree.
- Do not create the final file yet.
- If something is unsupported, label it unsupported.
- If something is an assumption, label it as an assumption.

## Source

Source: [Prompt 1: Office File Truth Setup](https://app.notion.com/p/1f398a5d64f74d31ad857afa507a2f0d)
