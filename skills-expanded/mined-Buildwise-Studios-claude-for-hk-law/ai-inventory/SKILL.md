---
name: ai-inventory
description: >
  Per-system inventory for Hong Kong AI governance — track each AI system's
  sector (PCPD / SFC / HKMA / IA / cross-border), risk tier (high / medium /
  low), and applicable HK regulatory framework. Sector and risk are assessed
  per system, not per company. Use when the user says "ai inventory", "add
  an ai system", "what systems do we have", "classify this ai system",
  "hk ai register", or "ai system registry".
argument-hint: "[list | add | edit <id> | classify <id> | show <id>]"
---

# /ai-inventory

## When this runs

The user wants to manage their AI system inventory under Hong Kong's evolving
AI governance framework. The core idea the skill exists to enforce: **sector
and risk are per-system, not per-company.** A single organization may have
different obligations for System A (governed by PCPD guidance) vs System B
(governed by SFC or HKMA guidelines). Each combination triggers a different
set of obligations. The inventory exists so those assessments are tracked
where you can find them — the obligations themselves are derived in
conversation, not from a table.

## What to do

1. **Read the config.** Read
   `~/.claude/plugins/config/claude-for-hk-law/ai-governance-legal/CLAUDE.md`.
   If it doesn't exist or still has `[PLACEHOLDER]` markers, direct the user
   to `/ai-governance-legal:cold-start-interview` first.

2. **Read the inventory.** Inventory lives at
   `~/.claude/plugins/config/claude-for-hk-law/ai-governance-legal/ai-systems.yaml`.
   If it doesn't exist, create it with an empty `systems:` list when the
   first `add` runs.

3. **Dispatch on the argument:**

   - No argument, or `list` → show the inventory table (see **List** below).
   - `add` → run the **Add** flow.
   - `edit <id>` → show the current record, ask what to change, update one
     field, confirm, write.
   - `classify <id>` → run the **Classification walk-through** on an
     existing record, updating sector, risk_tier, and tier_basis.
   - `show <id>` → show the full record.

4. **On list, offer the dashboard:**
   "Want the full dashboard? Filter by status / sector / risk / data nexus.
   Say the word."

5. **Close every action with a hook into the lawyer's work.**
   After any write, say:
   > Recorded. When you're ready to walk through obligations for this
   > system, just ask — I'll do it in-conversation and flag where the
   > PCPD / SFC / HKMA guidance mapping needs your verification. I don't
   > derive obligations from a table because the framework is complex and
   > still evolving.

## List format

Render as a compact table:

| ID | Name | Owner | Status | Data nexus | Sector | Risk tier | Next review |
|----|------|-------|--------|------------|--------|-----------|-------------|
| sys-001 | Resume screening | HR / Jamie | in_production | yes (PDPO) | PCPD | high | 2026-08-01 |
| sys-002 | Chatbot assistant | IT / Priya | in_production | yes | PCPD | low | 2026-12-01 |
| sys-003 | AI trading algo | Trading / Mike | in_production | no | SFC | high | 2026-07-15 |

Under the table, show counts by sector and risk tier, and a line: "N systems flagged for review within 30 days."

## Add flow (interview)

Ask, one field at a time (or accept a paste). The required fields are
`name`, `owner`, `description`, `status`, `sector`. The rest can be
deferred — say so explicitly: "you can come back to classification with
`/ai-governance-legal:ai-inventory classify <id>`."

1. **Name.** Short label for the system.
2. **Owner.** Person or team accountable for it day-to-day.
3. **Description.** One or two sentences. What does it do, and against
   what data?
4. **Status.** `planned | in_development | in_production | deprecated`.
5. **Sector / regulator.** Which HK regulatory regime primarily governs?
   - `PCPD` — personal data processing, PDPO obligations
   - `SFC` — AI in financial markets, investment advice, trading
   - `HKMA` — RegTech, banking AI, credit decisions
   - `IA` — insurance AI, underwriting
   - `cross-border` — affects Mainland China, EU, or other jurisdictions
   - `none` — no specific HK regulatory framework yet
6. **Proceed to classification?** Offer to run the walk-through now, or
   skip and come back later.

Assign an ID: `sys-NNN` where NNN is the next integer in the file.

## Classification walk-through

The walk-through produces `sector`, `risk_tier`, `tier_basis`. Bases are
tagged `[verify against current HK regulator guidance]` — not because the
skill is hedging, but because HK's AI governance framework is evolving and
sector-specific. The lawyer owns verification.

### Step 1: Sector classification

> **Which HK regulator's guidance primarily governs this system?**

- **PCPD** — Systems that process personal data in Hong Kong. The PCPD has
  issued guidance on AI ethics, AI model governance, and the responsible
  use of AI (see PCPD's Guidance on the Ethical Development and Use of
  Artificial Intelligence and its Guidance Note on the Use of AI in
  Human Resources). Recent PDPO amendments address automated decision-making
  and data portability.
- **SFC** — AI systems used in financial services regulated by the SFC,
  including robo-advisory, algorithmic trading, and AI-assisted investment
  advice. See SFC's circulars and guidelines on AI governance in financial
  markets.
- **HKMA** — AI systems used by authorized institutions (banks) for
  credit scoring, fraud detection, RegTech compliance, and customer-facing
  services. See HKMA's Principles on the Use of AI for AIs and RegTech
  guidance.
- **IA** — AI in insurance underwriting, claims processing, and customer
  service.
- **cross-border** — Systems deployed outside HK (Mainland China, EU,
  US) need to comply with those jurisdictions' AI regulations in addition
  to HK guidance.
- **none (unregulated)** — AI systems with no specific HK regulatory
  framework. General common law, contract, and negligence principles apply.

**Dual-sector flag.** If a system crosses regulatory domains (e.g., a bank's
AI credit scoring system that processes personal data), it may be governed
by BOTH PCPD and HKMA guidance. Flag this and recommend coordinated review.

### Step 2: Risk tier

> **What is the potential impact if this AI system causes harm?**

Check in order:

**A. High risk.** Systems that:
- Make or materially influence decisions affecting individuals' legal rights
  or significant interests (employment, credit, insurance, access to services)
- Process special categories of personal data (health, biometric, criminal
  records)
- Operate in regulated sectors (financial services, insurance, critical
  infrastructure) under SFC/HKMA/IA guidance
- Are used for automated decision-making without meaningful human review
- Could cause significant financial, reputational, or physical harm if wrong

If matched → `high`. Flag for full AI impact assessment per PCPD guidance
and any applicable sector-specific requirements.

**B. Medium risk.** Systems that:
- Assist human decision-making but do not make automated decisions
- Process personal data but do not make consequential decisions
- Are customer-facing but with human review in the loop
- Operate in unregulated sectors with moderate privacy/data implications

If matched → `medium`. Moderate assessment recommended.

**C. Low risk.** Systems that:
- Are internal productivity tools with no personal data processing
- Perform purely internal administrative functions
- Are non-customer-facing and produce no consequential outputs
- Have no data nexus triggering PDPO or sector regulation

If matched → `low`. Light assessment sufficient.

**D. Prohibited or restricted practices.** While HK has no AI-specific
prohibition framework equivalent to the EU AI Act, certain AI practices may
violate existing Hong Kong law:
- Unlawful discrimination under the Sex Discrimination Ordinance (Cap. 480),
  Disability Discrimination Ordinance (Cap. 487), etc.
- Unauthorized biometric data collection under the PDPO
- Misleading or deceptive AI practices under the Trade Descriptions
  Ordinance (Cap. 362)
- Criminal offenses (fraud, forgery) committed via AI systems

If any of these apply, flag as `high` and route to legal review immediately.

Write the tier. Write `tier_basis` in one sentence, citing the applicable
HK guidance or ordinance, tagged `[verify against current HK law/guidance]`.

### Step 3: Recommendations

Offer three next steps:
1. "Want me to walk through obligations for this system under HK
   PCPD / SFC / HKMA guidance? I'll do it in conversation."
2. "Want to run `/ai-governance-legal:aia-generation` to produce a full
   impact assessment?"
3. "Want to set a next review date? I'll add it to the inventory."

## Record format

```yaml
systems:
  - id: sys-001
    name: "Resume screening tool"
    owner: "HR / Jamie"
    description: "Filters inbound CVs against job criteria"
    status: in_production          # planned | in_development | in_production | deprecated
    sector: pcpd                   # pcpd | sfc | hkma | ia | cross-border | none
    data_nexus: true               # processes personal data (PDPO applies)
    cross_border_nexus: false      # affects individuals outside HK
    risk_tier: high                # high | medium | low
    tier_basis: "PCPD guidance on AI in HR — high risk due to automated employment-related decision-making [verify against current PCPD guidance]"
    obligations_assessed: false
    obligations_note: "To assess: PDPO DPP obligations (transparency, consent, data accuracy), PCPD AI ethics principles"
    next_review: "2026-08-01"
    review_trigger: "on substantial modification or annually"
    created: "2026-06-03"
    updated: "2026-06-03"
```

## Why this skill does NOT auto-derive obligations

The inventory stores sector, risk tier, and the basis for each. It does NOT
contain a hardcoded sector × risk → obligations table.

When the user asks "what are my obligations for System X?", the skill
does the analysis **in conversation**, tagged `[verify]`, and routes to
`/ai-governance-legal:aia-generation` for the formal impact assessment
if needed.

This is deliberate:
- HK's AI governance framework is still evolving across multiple regulators.
- Confident-and-wrong on a compliance obligation ends up in a board memo.
- The inventory is a registry for the lawyer. The lawyer owns the
  obligation analysis.

## Guardrails

- **Never classify silently.** The classification walk-through must be
  visible; do not auto-classify from a system description.
- **`[verify]` tags stay.** They are not hedging — they are the point.
  Do not strip them in outputs.
- **Flag dual-sector systems.** When a system crosses regulatory domains,
  prompt the user to coordinate review across applicable regulators.
- **Don't declare obligations from a table.** If asked, do the analysis
  in conversation and route to `/aia-generation` for anything that needs
  a formal record.
