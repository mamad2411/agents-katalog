---
name: entity-compliance
description: >
  Entity compliance tracker — initialize, report upcoming deadlines, update
  status, run health audit, export to CSV. Maintains a compliance-tracker.yaml
  built from the entity table, calculates filing deadlines by entity and
  jurisdiction, and surfaces what's due in the next 30/60/90 days. Use when
  user says "entity compliance", "filing deadlines", "annual reports due",
  "entity tracker", "what filings are due", "entity health", or "good standing".
argument-hint: "[--init | --report [--days N] | --update [--from-report] | --sweep | --audit | --export [--format csv|table]]"
---

# /entity-compliance

1. Load `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/CLAUDE.md` → `## Entity Management` (entity table, jurisdictions, company secretarial provider).
2. Route to the correct mode below based on flag:
   - No flag or `--init`: Mode 1 — initialize tracker from entity table
   - `--report`: Mode 2 — surface upcoming deadlines and overdue items
   - `--update`: Mode 3a (manual) or 3b (--from-report upload) — update status
   - `--sweep`: Mode 3c — walk through unknown/overdue items one by one
   - `--audit`: Mode 4 — full health audit
   - `--export`: Mode 5 — produce CSV or table export
3. Read/write `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/entities/compliance-tracker.yaml`.
4. After any update: show summary of changes and next action.

---

## Purpose

Annual returns, financial statements, directors' reports, and significant controllers registers — every HK company and every foreign jurisdiction has its own filing schedule under the Companies Ordinance (Cap 622) and its own consequences for missing the deadline. This skill maintains a single YAML tracker that knows what's due, when, and for which entity. It's lightweight by design: the tracker is a file you own, Claude updates it on command, and you export it when you need to share it.

## Important: deadline reference caveat

> The filing deadlines in this skill's reference table reflect publicly available requirements as of the skill's build date. HK filing requirements and due dates can change via legislative amendments. **Always confirm deadlines with the Companies Registry (HK) or directly with the relevant registry before relying on them for compliance purposes.** If you use a corporate services provider, their compliance calendar is authoritative for your specific entities — use this tracker to organize and surface their data, not to replace it.

## Jurisdiction assumption

> This tracker computes deadlines against the jurisdiction of formation / registration recorded per entity. Filing rules, due-date mechanics, and fee structures vary materially by jurisdiction. If an entity's actual footprint differs from what's in `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/CLAUDE.md` (undisclosed foreign registration, dissolved entities, jurisdictional changes, international filings managed by a local agent), the output may not apply as written — confirm with the corporate services provider or local counsel for that jurisdiction.

## Entity-type disambiguation (especially HK)

> The filing calendar depends on **entity type**, not just jurisdiction. Treating a "HK company" as a single bucket is a common error — HK private companies limited by shares, public companies, and companies limited by guarantee have different filing obligations under Cap 622. Confirm the entity type from the entity table before computing or reporting a deadline.
>
> **HK Companies Ordinance (Cap 622) — the key filings:**
>
> - **HK private company limited by shares:** Annual return (Cap 622 s. 662) due within 42 days after the anniversary of incorporation or the date of the last annual return. Annual financial statements and directors' report (Cap 622 s. 429-433) — must be prepared within 6 months of the financial year-end for private companies. Significant controllers register (Cap 622 Part 17A) — maintain and update with changes within 7 days.
> - **HK public company (listed or unlisted):** Same annual return obligations plus filing of annual report and accounts with HKEX (if listed). Financial statements must be prepared within 4 months of the financial year-end (Cap 622 s. 429, for listed companies) or 6 months (unlisted public companies).
> - **HK company limited by guarantee:** Annual return (Cap 622 s. 662) due on anniversary. Simplified financial reporting requirements per Cap 622 s. 434 for small guarantee companies.
> - **Foreign companies registered in HK (Part 16 Cap 622):** Must file annual returns (Cap 622 s. 788), financial statements (Cap 622 s. 791), and notification of changes.
>
> A HK private company limited by shares does NOT file an annual return on a fixed calendar date — it's anniversary-based. Writing a fixed March 1 deadline for a HK company would be incorrect. If the entity table records a HK entity without a type, flag it as `type_unknown` and ask the user to confirm before computing any deadline.
>
> The same entity-type discipline applies to every other jurisdiction with divergent filing regimes by entity type. When the reference table for a jurisdiction is populated, make sure it is indexed by entity type, not just by jurisdiction.

---

## Tracker file

Lives at `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/entities/compliance-tracker.yaml`. Structure:

```yaml
# Entity Compliance Tracker
# Generated: [date]
# Last updated: [date]
# Disclaimer: deadlines are reference only — confirm with registered agent or Companies Registry (HK) / other relevant registry

metadata:
  company: "[Company Name]"
  generated: "[date]"
  last_updated: "[date]"
  last_audit: "[date or null]"

custom_jurisdictions:   # manually added — jurisdictions not in built-in reference table (e.g. BVI, Cayman)
  []                    # populated when a new jurisdiction is encountered

entities:
  - name: "[Entity Name]"
    type: "[private company limited by shares / public company / company limited by guarantee / registered branch / other]"
    place_of_incorporation: "[Hong Kong / BVI / Cayman / other]"
    formation_date: "[date or null]"
    status: "[active / dormant / dissolving]"
    registered_agent: "[corporate services provider / in-house / other]"
    notes: ""

    jurisdictions:
      - state: "[state]"
        qualification: "[domestic / foreign]"
        qualified_date: "[date or null]"
        agent_managed: false   # set true for international entities where a local agent handles compliance
        local_agent: "[name or null]"
        filings:
          - type: "[Annual Return / Financial Statements / Directors' Report / Annual Confirmation / other]"
            due_date: "[YYYY-MM-DD]"
            due_basis: "[fixed date / anniversary month / other]"
            last_filed: "[date or null]"
            last_fee: "[amount or null]"
            status: "[current / due_soon / overdue / unknown]"
            confirmed_good_standing: "[date or null]"
            notes: ""
```

Status values:
- `current` — filed for current period, nothing due within 90 days
- `due_soon` — due within 90 days
- `overdue` — past due date with no filed date recorded
- `unknown` — no information; needs manual confirmation

---

## Mode 1: Initialise

Run when no tracker exists, or with `--rebuild` to regenerate from scratch.

### Step 1: Load entity table

Read `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/CLAUDE.md` → `## Entity Management` → Entity table. If the entity table
is populated (from org chart upload at cold-start), use it directly. If not,
ask the user to either run the cold-start module or provide the entity list.

### Step 2: For each entity × jurisdiction, confirm the filing requirements

For each entity, confirm the current filing schedule with the corporate services provider or the relevant registry. Filing schedules change (some jurisdictions move from fixed dates to anniversary-based schedules and back, fee structures are revised, filing categories are reclassified). Do not rely on a cached schedule. The tracker below records the dates you confirm; update them when your registered agent sends reminders.

For each jurisdiction where the entity is registered (domestic or foreign):

1. Ask the user whether they have a current compliance report from the registered agent — that's the most authoritative source.
2. If not, ask the user what they know (filing type, due-date basis, last filed date, typical fee). Record what they provide.
3. For anything the user does not know, flag the entity × jurisdiction entry as `unknown` — do not populate dates from a cached reference. The user's next step is to confirm with the registered agent or relevant registry.

**Capture details in the tracker rather than a reference table:**

> I don't have filing requirements for [Jurisdiction] in the reference table.
> Let me capture them so we can track this going forward.
>
> For [Entity] in [Jurisdiction]:
> 1. What type of filing is required? (Annual return, confirmation statement, financial
>    statements, annual return, or something else?)
> 2. When is it due? (Fixed date like May 1, anniversary month, or other?)
> 3. What's the typical fee? (Approximate is fine — or "unknown".)
> 4. Who is your registered agent or local filing agent there?

Store the answer in a `custom_jurisdictions` block in the tracker:

```yaml
custom_jurisdictions:
  - jurisdiction: "[State / Country]"
    jurisdiction_type: "[US state / Canada province / EU member state / other]"
    filings:
      - type: "[filing type]"
        due_basis: "[fixed: MM-DD / anniversary month / other description]"
        typical_fee: "[amount or unknown]"
        notes: "[any other relevant information — e.g., local agent required, filing in local language]"
    added_by: "manual"
    added_date: "[date]"
```

This custom definition is then applied to all entities in that jurisdiction.
Future `--init` runs and entity additions will use it automatically.

**International jurisdictions specifically:**

International filings vary enormously by jurisdiction. Always go through the
custom definition flow above — confirm the filing type, cadence, and fee with
the local filing agent or registered office agent before populating the tracker.

For international entities, also ask:
- Is there a local filing agent or registered office agent handling compliance?
  If yes, note the agent name — the tracker can flag when to follow up with them
  rather than calculating due dates independently.
- Is the entity required to file any group-level reports in this jurisdiction
  (e.g., country-by-country reporting, beneficial ownership registers,
  economic substance filings)?

Flag international entities with a local agent as `agent_managed: true` in the
tracker. The report mode will list them separately with a note to confirm status
with the local agent rather than showing a calculated due date.

For anniversary-based filings: calculate from the formation_date in the tracker.
If formation_date is null: set status to `unknown` and flag for confirmation.

### Step 3: Write the tracker

Generate `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/entities/compliance-tracker.yaml` with all entities and their
calculated filing requirements. Set initial status:
- `current` if last_filed is within the current filing period
- `due_soon` if due within 90 days and no last_filed for current period
- `overdue` if due date has passed and no last_filed for current period
- `unknown` if formation_date is missing or state is not in reference table

Show a summary after generating:

```
Entity compliance tracker initialized.

Entities: [N]
Total jurisdictions: [N]
Filings tracked: [N]

Status summary:
  ✅ Current:   [N]
  ⏰ Due soon:  [N] (next 90 days)
  🔴 Overdue:   [N]
  ❓ Unknown:   [N] (confirm with registered agent)

Run /corporate-legal:entity-compliance --report to see what's due.
```

---

## Mode 2: Report

Surfaces upcoming deadlines and flags overdue items. Default: next 90 days.

```
/corporate-legal:entity-compliance --report [--days 30|60|90|180]
```

Output format:

```
ENTITY COMPLIANCE REPORT — [date]
[Company Name]

🔴 OVERDUE ([N]):
  [Entity] / [State] / [Filing type] — was due [date]

⏰ DUE WITHIN [N] DAYS ([N]):
  [Entity] / [State] / [Filing type] — due [date]  [registered agent]
  [Entity] / [State] / [Filing type] — due [date]

✅ RECENTLY FILED ([N] in last 90 days):
  [Entity] / [State] / [Filing type] — filed [date]

❓ UNKNOWN STATUS ([N]):
  [Entity] / [State] / [Filing type] — no information; confirm with registered agent

🌐 AGENT-MANAGED ([N]):
  [Entity] / [Country] / [Filing type] — managed by [local agent]; confirm status directly
  [Entity] / [Country] — no local agent recorded; add one with --update

GOOD STANDING:
  Last confirmed: [date]
  Entities with confirmed good standing: [N] of [total]
  Entities not confirmed in last 12 months: [list]
```

If the tracker covers more than ~10 entities, or any time the user asks: offer the dashboard (see CLAUDE.md `## Outputs → Dashboard offer for data-heavy outputs`). Shape the offer for this output — counts by filing status (overdue / due soon / filed / unknown), counts by good-standing state, and a sortable entity table with jurisdiction, filing type, and next due date.

---

## Mode 3: Update

Updates one or more entities in the tracker. Three sub-modes:

### Consequential-action gate (file SOI / annual report)

**Before directing or confirming a filing:** Read `## Who's using this` in `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/CLAUDE.md`. If the Role is **Non-lawyer**:

> Filing an annual return, financial statements, or other statutory filing with the Companies Registry (HK) or other relevant registry has legal consequences — it's a formal representation from the entity, it carries fees, and missed or incorrect filings can cause loss of good standing or strike-off. Have you reviewed this with an attorney (or a qualified corporate services provider) before filing? If yes, proceed to record the filing. If no, here's a brief to bring to them:
>
> - Entity, jurisdiction, filing type, and due date
> - What the tracker says about the last filing (date, fee, director/company secretary information last reported)
> - Open questions (is the director/company secretary information still accurate; has the registered office changed; has the business address changed)
> - What could go wrong (out-of-date director information, missed deadline triggering late fees or strike-off (Cap 622 s. 744-746), fee calculation error)
> - What to ask the attorney (is a filing actually needed this year; are there any charter amendments or officer changes that need to be reflected; who should sign)
>
> If you need to find an attorney, solicitor, barrister, or other authorised legal professional: contact your professional regulator (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent) for a referral service.

Do not record a new `last_filed` date past this gate without an explicit yes. Tracker reads, deadline reports, and "what's due soon" output do not require the gate.

### 3a: Manual update

```
/corporate-legal:entity-compliance --update
```

Attorney tells Claude what was filed:
> "We filed the annual return (NAR1) for [Entity] on March 1. Fee was $105."

Claude updates:
- `last_filed` → March 1 date
- `last_fee` → $450
- `status` → `current`
- `last_updated` in metadata

### 3b: Registered agent report upload

```
/corporate-legal:entity-compliance --update --from-report
```

User uploads a corporate services provider, legal secretarial firm, or similar compliance
report (PDF, CSV, or Excel). Claude reads it and updates matching entities:

From the report, extract for each entity:
- Filing type and due date
- Last filed date (if present)
- Good standing status and date confirmed
- Any flags or warnings from the agent

Match report entities to tracker entities by name (flag near-matches for
confirmation — "Acme Holdings Ltd" vs. "Acme Holdings Limited" are probably
the same entity).

After processing:
```
Updated [N] entities from report.

Matched: [N]
Unmatched (in report, not in tracker): [list — may need to add to entity table]
Not in report (in tracker, no update): [list — status unchanged]
```

### 3c: Bulk status sweep

```
/corporate-legal:entity-compliance --sweep
```

Walks through each entity with `unknown` or `overdue` status and asks for
current information one at a time:

> [Entity] / [State] / [Filing type] — currently showing as [status].
> Has this been filed? If yes, when and what was the fee?

Updates tracker after each confirmation. Produces a completion summary.

---

## Mode 4: Health audit

```
/corporate-legal:entity-compliance --audit
```

Broader review beyond just filing status. Surfaces:

**Filing compliance:**
- Overdue items (from report mode)
- Unknown status items

**Entity health:**
- Entities marked as `dormant` — flag for review: should these be dissolved?
  Carrying dormant entities costs money (annual fees, registered office and company secretary fees)
  and creates ongoing compliance obligations.
- Entities with formation_date older than 5 years and status `dormant` — flag
  as dissolution candidates.
- Entities missing formation_date — flag as data gap.

**Good standing gaps:**
- Entities with no `confirmed_good_standing` date — unknown whether in good
  standing; risk if a transaction requires a certificate on short notice.
- Entities with `confirmed_good_standing` older than 12 months — stale; worth
  refreshing, especially if M&A or financing is anticipated.

**Foreign qualification gaps:**
- Based on `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/CLAUDE.md` entity table: are there states in the company's
  operational footprint (offices, employees) where entities are not foreign
  qualified? This requires the attorney to confirm operational presence —
  Claude can flag the question but cannot determine presence independently.

**Intercompany agreement gaps:**
- From `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/CLAUDE.md`: if intercompany agreements are marked as partial or no,
  flag which entity relationships likely need agreements (parent-subsidiary
  services, IP licenses, loans).

Output format:

```
ENTITY HEALTH AUDIT — [date]

FILING COMPLIANCE
  Overdue: [N]
  Unknown status: [N]
  Action: run --sweep to confirm unknown items

DORMANT ENTITIES ([N])
  [List of dormant entities with age and annual carrying cost if known]
  Dissolution candidates (>5 years dormant): [list]

GOOD STANDING
  No record: [N] entities
  Stale (>12 months): [N] entities
  Consider refreshing before: [any upcoming transactions or contract renewals if known]

POTENTIAL GAPS
  Foreign qualification: [flag question — confirm operational presence in:]
    [list of states from `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/CLAUDE.md` footprint not in tracker as qualified]
  Intercompany agreements: [status from `~/.claude/plugins/config/claude-for-hk-law/corporate-legal/CLAUDE.md`]

RECOMMENDED ACTIONS
  1. [Highest priority action]
  2. [etc.]
```

---

## Mode 5: Export

```
/corporate-legal:entity-compliance --export [--format csv|table]
```

Produces a flat export suitable for sharing with finance, legal ops, or
outside corporate services provider or local agent. Default: CSV.

CSV columns:
`Entity Name, Entity Type, State of Formation, Formation Date, Status,
Registered Agent, Jurisdiction, Qualification Type, Filing Type, Due Date,
Last Filed, Last Fee, Good Standing Confirmed, Notes`

One row per filing per jurisdiction. Multiple rows per entity (one per
jurisdiction × filing type combination).

If `--format table`: produce a markdown table suitable for pasting into
a report or Slack message, showing only the next 90 days of filings.

---

## What this skill does not do

- It does not file anything. Output is a tracker and a to-do list; filing
  is done by the attorney, outside counsel, or corporate services provider.
- It does not pull good standing certificates. It tracks when certificates
  were last confirmed; obtaining them is manual or via the relevant registry.
- It does not determine whether foreign registration is required in a given
  jurisdiction. That analysis depends on facts about business activity that the
  attorney must confirm.
- It does not replace a corporate services provider for companies with complex
  multi-entity structures. Corporate secretarial firms and legal service
  providers have dedicated compliance teams and direct registry relationships.
  This skill is best suited for smaller organizations without such support,
  or as a lightweight layer on top of provider data for organizations that do
  have support.
- The filing deadline reference table is not legal advice and may not reflect
  current requirements. Confirm all deadlines before relying on them.


## Formula injection defense

Before writing any cell in Excel, Sheets, or CSV output, neutralize formula injection. Counterparty-sourced text (contract quotes, party names, registered agent data, CLM exports) is attacker-controlled. A cell starting with `=`, `+`, `-`, `@`, `	`, `
`, or `
` will be interpreted as a formula or break the row structure.

- **Prefix with a single quote:** `'=SUM(A1:A10)` → `=SUM(A1:A10)` (displayed as text, not executed)
- **Applies to every cell that contains text sourced from a document, a tool result, or a user paste.** Column headers you control and computed values you produce are safe.
- **CSV: also escape embedded commas, double quotes, newlines** (RFC 4180 quoting).
- This is not optional. A spreadsheet your user opens in Excel that triggers a macro or exfiltrates data via DDE is a supply-chain attack on your user.
