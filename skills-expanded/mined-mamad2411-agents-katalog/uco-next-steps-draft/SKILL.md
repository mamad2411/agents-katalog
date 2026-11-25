---
name: uco-next-steps-draft
description: Draft UCO next step updates based on recent account activity. Saves local drafts for review before pushing to Salesforce. Use when reviewing use case progress, preparing for 1:1s, or updating Salesforce UCO next steps.
user-invocable: true
---

# UCO Next Steps Draft

Analyze recent account activity from the account overview and suggest updated next steps for each Use Case Object (UCO). Saves draft suggestions to `uco-update-drafts.md` in each account folder for review before pushing to Salesforce.

**Key difference from `/uco-next-steps`**: This skill is local-first — it reads from your local `account-overview.md` files (synced via `/account-sync`) and writes drafts locally. Nothing touches Salesforce until you explicitly push with `/uco-updates`. This makes it safe to run speculatively and review at your own pace.

## Capabilities

- Read the account overview and engagement timeline to understand recent activity
- Analyze what has changed since the current UCO next steps were written
- Draft concrete, actionable next step suggestions per UCO using Salesforce `Demand_Plan_Next_Steps__c` format
- Suggest MEDDPIC field updates when evidence exists in the timeline (Metrics, Exec Sponsor, Authority, Compelling Event)
- Suggest health and stage changes when activity warrants it
- Use discriminating terms per UCO to prevent context mixing across UCOs at the same account
- Save drafts locally for review — never writes directly to Salesforce
- Skip accounts that were already analyzed in the past 12 hours
- Drafts are formatted for direct use with `/uco-updates` to push to Salesforce

## Arguments

- `/uco-next-steps-draft <account-name>` — Generate suggestions for a single account (e.g., `/uco-next-steps-draft halton-healthcare`)
- `/uco-next-steps-draft --all` — Generate suggestions for all account folders in the working directory

## Workflow

### Step 1: Resolve Target Accounts

Parse the user's arguments:

- If a specific account name is given, target only that folder
- If `--all` is specified, scan the working directory for subdirectories, **excluding**: `.obsidian`, `.claude`, `.claude-plugin`, and any hidden directories (starting with `.`)

For each target account folder:

1. Check if `uco-update-drafts.md` already exists in the folder
2. If it exists, read the `> Generated:` timestamp line at the bottom of the file
3. **If the timestamp is less than 12 hours old, SKIP this account** and report: `{account}: Skipped — last generated {X} hours ago`
4. If no file exists, or the timestamp is older than 12 hours, proceed

### Step 2: Read Account Context

For each account that passes the 12-hour check:

1. Read `account-overview.md` from the account folder
2. Extract:
   - **UCO table** — all UCOs with their current stage, health, products, target go-live, onboarding date, and current next steps
   - **Engagement Timeline** — all dated entries, focusing on the most recent activity
   - **Existing Artifacts** — any new docs, slides, or deliverables
   - **Key Contacts** — who is engaged (include titles where available)
   - **Bottom Line** — the strategic assessment
   - **Risks & Concerns** — any flagged blockers or risks
   - **Open Questions** — unresolved items

### Step 2.5: Extract Discriminating Terms per UCO

**This step prevents context mixing when an account has multiple UCOs.**

For every UCO at the account, extract 3-6 discriminating terms that uniquely identify it. Use the UCO Name and any description fields as inputs. Strip generic words (the account name itself, "Databricks", "Phase", "Project", "Use Case", "Platform").

**Examples:**
| UCO Name | Discriminating Terms |
|---|---|
| Halton - Streaming ETL for Real-Time Analytics | `["streaming", "ETL", "Kafka", "real-time", "Delta Live Tables"]` |
| Halton - Migration from Legacy Hadoop | `["Hadoop", "migration", "lakehouse", "HDFS", "legacy"]` |

When analyzing timeline entries in Step 3, score each entry against UCO discriminating terms:
- **2+ term matches** → HIGH confidence attribution to that UCO
- **1 term match** → MEDIUM confidence (note in draft)
- **0 matches or ties** → account-level signal, do not attribute to a specific UCO

### Step 3: Analyze and Draft Suggestions

For each UCO in the account:

1. **Compare current next steps** against recent timeline activity:
   - Have any of the current next steps already been completed? (e.g., "schedule architecture session" but a session already happened)
   - Has new information emerged that changes priorities? (e.g., a blocker was resolved, a competitor entered, a new contact was identified)
   - Are there time-sensitive items approaching? (e.g., go-live date within 3 months, RFP deadline)

2. **Draft updated next steps** using the Salesforce `Demand_Plan_Next_Steps__c` format:
   ```
   Mon-DD - INITIALS - Update text
   ```
   For example: `Mar-16 - MN - Architecture review scheduled for week of Mar 23 with Sunny Gurm (VP Data Engineering)`

   Each next step should be **concrete and actionable** — include who (with title), what, and by when where possible.

   Use the UCO stage framework to guide what actions are appropriate:
   - **U1** (Qualifying): Schedule discovery call to validate pain and confirm willingness to engage
   - **U2** (Scoping): Architecture session, POC planning, partner assessment, define success criteria, confirm stakeholder availability
   - **U3** (Evaluating): POC execution, technical validation, success criteria tracking, deploy workspace, schedule kickoff
   - **U4** (Confirming): Confirm technical win, align on production timeline, commercial negotiation, procurement, security review
   - **U5** (Onboarding): Review initial DBU consumption, deployment, enablement, confirm go-live date, schedule check-in
   - **U6** (Live): Monitoring, expansion, value realization

   Reference specific timeline events or artifacts that support the suggestion.

   **Fallback**: If no timeline signals were attributed to a UCO (HIGH or MEDIUM), draft a forward-looking next step based on the existing Salesforce next steps and stage-appropriate motion from the table above. **Never write "no activity found" or "no signals" in the next steps text** — always produce a concrete action.

3. **Check for MEDDPIC signal updates** — scan the timeline and artifacts for evidence that any of these fields should be updated. Only suggest when there is **concrete evidence**, never guess:
   - **Metrics** (`Metrics__c`): multipicklist — Cost Reduction, Customer Experience, Data Pipeline Efficiency, Data Quality, Innovation Enablement, Productivity Improvement, Revenue Growth, Scalability, Security & Compliance, Time to Market
   - **Metrics Notes** (`MetricsNotes__c`): specific KPIs or quantified outcomes mentioned in meetings/emails
   - **Exec Sponsor** (`Business_Exec_Sponsor__c`): VP/C-level contact identified as sponsor in meetings or notes
   - **Authority** (`AEAuthority__c`): Influencer, Technical Decision Maker, Economic Decision Maker, Executive Sponsor, Practitioner, Unknown
   - **Compelling Event** (`Compelling_event_Urgency__c`): deadlines, contract expirations, RFPs, regulatory dates mentioned in timeline

4. **Flag stage and health changes** if activity warrants:
   - Stage should advance if criteria are met (e.g., customer agreed DB is a fit → U3, POC started → U3, tech win → U4)
   - Health should change if new risks emerged (→ Yellow/Red) or blockers were resolved (→ Green)
   - **Never override a Red health flag to Green without HIGH-confidence evidence**

5. **Track source failures** — if the account overview appears stale (last synced > 7 days ago), note this in the draft so the user knows to run `/account-sync` first.

6. **Draft format** for each UCO:

   ```markdown
   ### {UCO Name} — {Current Stage}

   **Signal attribution:** {N} HIGH, {N} MEDIUM, {N} unattributed

   **Current next steps:** {what's in the overview today}

   **Suggested next steps entry:**
   ```
   Mon-DD - MN - {update line 1}
   Mon-DD - MN - {update line 2}
   ```

   **Rationale:** {1-2 sentences explaining why, referencing specific timeline events}

   **Stage change?** {Yes → suggest new stage with reasoning / No — still appropriate}

   **Health change?** {Yes → suggest new health with reasoning / No — still appropriate}

   **MEDDPIC updates?**
   - {field}: {suggested value} — Evidence: {what you saw in the timeline}
   - _(or "No MEDDPIC updates suggested" if no evidence found)_
   ```

### Step 4: Write Draft File

Write the suggestions to `{account_folder}/uco-update-drafts.md` with the following format:

```markdown
# {Account Display Name} — UCO Update Drafts

> These are suggested next step updates based on recent account activity.
> Review and edit, then push to Salesforce via `/uco-updates`.

---

### {UCO 1 Name} — {Stage}

**Signal attribution:** {N} HIGH, {N} MEDIUM, {N} unattributed

**Current next steps:** {what's in the overview today}

**Suggested next steps entry:**
```
Mon-DD - MN - {update line 1}
Mon-DD - MN - {update line 2}
```

**Rationale:** {why, referencing timeline events}

**Stage change?** {Yes → new stage / No}

**Health change?** {Yes → new health / No}

**MEDDPIC updates?**
- {field}: {value} — Evidence: {source}

---

### {UCO 2 Name} — {Stage}

...

---

> Generated: {YYYY-MM-DD HH:MM} {timezone}
```

**IMPORTANT**: The `> Generated:` line must be the last line of the file and must include the full datetime with timezone (e.g., `> Generated: 2026-03-16 17:30 EDT`). This is used for the 12-hour skip check.

### Step 5: Report Summary

After all accounts are processed, output a summary:

```
## UCO Next Steps Drafts

### {Account Name}
- {UCO Name}: {1-line summary of key suggestion} [{N} HIGH, {N} MEDIUM signals]
- {UCO Name}: {1-line summary} [SF only — consider running /account-sync first]
- Status: Draft saved / Skipped (last run X hours ago)

### {Next Account}
...

Review drafts in each account folder at `uco-update-drafts.md`.
To push updates to Salesforce: `/uco-updates`
```

## Examples

### Single account
```
/uco-next-steps-draft halton-healthcare
```
Reads the Halton Healthcare overview, analyzes recent timeline activity against current UCO next steps, and saves draft suggestions to `halton-healthcare/uco-update-drafts.md`.

### All accounts
```
/uco-next-steps-draft --all
```
Iterates all account folders, skipping any analyzed in the past 12 hours, and generates draft next step updates for the rest.

### Weekly review workflow
```
/account-sync --all
/uco-next-steps-draft --all
```
First sync all accounts with latest activity, then generate UCO next step suggestions based on the fresh data.
