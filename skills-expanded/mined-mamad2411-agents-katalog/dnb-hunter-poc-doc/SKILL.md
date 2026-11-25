---
name: dnb-hunter-poc-doc
description: Create POC documentation for DNB Hunter team customer engagements
user-invocable: true
---

# DNB Hunter POC Document Generator

This skill creates comprehensive Proof of Concept (POC) documentation for DNB Hunter team customer engagements with Databricks. It gathers data from Salesforce UCOs, collaborates with you to fill gaps, and produces a polished Google Doc.

## Quick Start

**Invoke the `dnb-hunter-poc-doc` agent** to handle the full POC documentation workflow:

```
Task tool with subagent_type='fe-dnb-hunting:dnb-hunter-poc-doc' and model='opus'
```

Pass the user's request with available sources. The agent will:
1. Parse UCO URLs, account name, notes, or existing Google Docs
2. Gather data from Salesforce (UCO details, account team, contacts)
3. Select the appropriate template (table-based by default, narrative if requested)
4. Collaborate with you to fill gaps (contacts, cloud platform, timeline, success criteria)
5. Display the full draft for your review before generating the Google Doc
6. Generate a Google Doc and save it to the DNB Hunter Drive folder

## Two Template Options

### Table-Based (Default)
Structured format with tables for business case, contacts, timeline, workload details (objectives/tasks/docs/success criteria), and an evaluation tracker. Best for POCs with multiple workload categories (DE, BI, ML, GenAI).

### Narrative
Prose-driven format with POC Plan (objective, business case, architecture, day-by-day execution plan, success criteria) and Implementation Guide (step-by-step technical instructions). Best when you want a concise, scannable document with a day-by-day plan.

**To use narrative:** Say "narrative", "narrative-style", "day-by-day plan", or similar when invoking the skill.

## Source Types

| Source Type | Identifier Format | Example |
|-------------|-------------------|---------|
| Salesforce UCO URL | `/UseCase__c/{ID}/view` | `https://databricks.lightning.force.com/lightning/r/UseCase__c/aAv8Z000000ArXXXXX/view` |
| Plain UCO ID | `aAv...` | `aAv8Z000000ArXXXXX` |
| Google Doc | URL or Doc ID | `https://docs.google.com/document/d/...` |
| Account Name | Company name | `Acme Corp` |
| Free-text notes | Text | Customer contacts, cloud platform, requirements |

## Example Invocations

```
User: Create a POC doc for Acme Corp. Here are the UCOs: https://databricks.lightning.force.com/lightning/r/UseCase__c/aAv8Z000000ArXXXXX/view
--> Agent queries Salesforce, gathers context, creates table-based POC doc

User: Build a narrative POC doc for BigCo evaluating Databricks SQL. Notes: Contact is Jane Smith (VP Eng, jane@bigco.com). Target cloud: AWS. Timeline: Mar 1 - Mar 14.
--> Agent uses narrative template with day-by-day execution plan

User: /dnb-hunter-poc-doc
--> Interactive mode: agent prompts for UCO URLs, account name, and context
```

## Pre-Requisites

### Salesforce Access
The agent uses `sf` CLI to pull UCO and account details. Ensure authentication is active via the `salesforce-authentication` skill.

### Google Access
The agent uses `markdown_to_gdocs.py` to create the Google Doc. Ensure authentication is active via the `google-auth` skill.

## Document Structure

### Table-Based Template
1. Header — `[Customer Name] + Databricks`
2. Business Case — quantifiable problems and consequences
3. Key Contacts — Databricks and customer roles
4. POC Timeline — Plan, Deploy, POC, Executive Summary phases
5. POC Architecture — current and future state diagrams
6. Workload Details — objectives, tasks, Databricks docs, success criteria (per workload category)
7. Evaluation Tracker — criteria matrix

### Narrative Template
1. POC Plan — header, objective, business case, key contacts, current/proposed architecture, execution plan (day-by-day), success criteria, risks, estimated cost, deliverables, beyond the POC
2. Implementation Guide — step-by-step technical instructions organized by day/phase

## Resources

- `resources/SECTION_GUIDANCE.md` — General section guidance (applies to all templates)
- `resources/POC_DOC_TEMPLATE_TABLE.md` — Table-based document template (default)
- `resources/POC_DOC_TEMPLATE_NARRATIVE.md` — Narrative document template
- `resources/SECTION_GUIDANCE_NARRATIVE.md` — Additional guidance specific to narrative template
- `agents/dnb-hunter-poc-doc.md` — Agent implementation details
