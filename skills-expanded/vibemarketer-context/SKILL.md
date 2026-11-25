---
name: vibemarketer-context
description: "When the user wants to set up or update VibeMarketer context for a DTC brand, business goals, attribution targets, Triple Whale or Northbeam targets, paid social account, product, offer, UGC workflow, Meta Ads analysis, KPI reporting, creative taxonomy, reporting preferences, customer language, unit economics, or brand positioning. Use this before meta-performance-analyst, paid-social-kpi-exporter, ugc-script-writer, and creative-angle-lab."
metadata:
  version: 1.0.0
---

# VibeMarketer Context

Create and maintain the shared context file that other VibeMarketer skills read before doing work.

Canonical file: `.agents/vibemarketer-context.md`

Fallbacks to check first:

- `.codex/vibemarketer-context.md`
- `.claude/vibemarketer-context.md`
- `.agents/product-marketing.md`

## Workflow

1. Check whether a context file already exists.
2. If it exists, read it, distinguish real answers from `Unknown` placeholders, summarize what is captured, and ask what needs updating.
3. If it does not exist, draft it from available source material before asking questions.
4. Prefer source material in this order: store URL or landing page copy, product pages, reviews, ads library notes, customer research, Meta Ads exports, creative briefs, offer docs, brand guidelines.
5. Run the Minimum Useful Context check below to identify high-impact unknowns.
6. Ask one concise onboarding pass for the highest-impact missing information. Do not turn setup into a long interview unless the user asks.
7. Preserve existing values unless the user explicitly changes them.
8. Save the file to `.agents/vibemarketer-context.md` with a context status and a visible skipped-items list.

## Onboarding Mode

Treat this skill like onboarding, not report generation. The goal is to collect enough context for downstream skills to stop guessing while keeping setup lightweight.

The context file has three valid states:

- `Context status: Draft` means basic brand/account identity is still missing.
- `Context status: Usable` means the skills can run, but some skipped items should be shown as caveats or prompts in downstream work.
- `Context status: Complete` means no meaningful skipped items remain.

Do not block onboarding on every field. Instead, flag skipped fields clearly so the user knows what they are choosing to leave out and how it may affect reports, scripts, or creative analysis.

Use progressive passes:

1. **Essentials:** brand, category, store URL, market, language, currency, product, offer.
2. **Goals:** primary growth goal, source-of-truth metric, targets, scale/cut/hold rules.
3. **Data:** Meta connector, attribution platform, Triple Whale/Northbeam/Shopify availability, data freshness.
4. **Reporting:** operating cadence, date range, comparison range, decision metric, and drilldown limits.
5. **Creative/UGC:** creative taxonomy, top creative selection, visual analysis provider, UGC script language/count/format, swipe library.

Ask concise questions in groups. Keep the first onboarding pass to at most 6 grouped questions. Unknowns may remain `Unknown`; important skipped fields must also appear in `## Skipped Context Items`. Do not invent category-specific taxonomy, avatars, hooks, or motifs before the user provides the category or source material.

## Minimum Useful Context

Try to capture these fields from the user or reliable source material during the first onboarding pass:

- **Brand:** name, category, store URL or landing page, primary market, primary language, currency.
- **Business goals:** primary growth goal, primary efficiency metric, decision metric hierarchy, and source-of-truth targets if known.
- **Decision rules:** scale rule, cut rule, hold rule, and learning rule. If the user has no rules yet, note that downstream skills should use conservative defaults.
- **Data sources:** Meta account or connector status, source-of-truth attribution platform, account currency, data freshness, and known caveats.
- **Reporting:** operating cadence, default date range, comparison range, primary report decision metric, campaign/ad set/ad drilldown limits.
- **Creative/UGC:** top creative source/count, visual analysis provider, default script language/count/length, and swipe library preference.
- **Customer:** primary customer, main jobs/pains/outcomes, and top objections.

All fields are optional except basic brand/account identity. If high-impact fields remain unknown, keep the context `Usable`, not blocked, and list them in `## Skipped Context Items`.

Do not ask about CSV, XLSX, Google Sheets, or workbook output formats in the first onboarding pass unless the user specifically mentions KPI exports or spreadsheet workflows. Those are optional `paid-social-kpi-exporter` preferences, not required brand context.

When a useful field is missing:

1. Write a short "Captured so far" summary.
2. Ask one grouped follow-up pass for the highest-impact gaps.
3. If the user does not answer or wants to skip, save `Context status: Usable` and include `## Skipped Context Items`.
4. If the user explicitly says a field is not applicable, write `Not applicable` instead of `Unknown`.
5. If the user explicitly says they do not know yet, write `Unknown - skipped for now` and list the downstream impact.

## Context To Capture

Use this structure:

```markdown
# VibeMarketer Context
Last updated: YYYY-MM-DD
Context status: Usable
Context confidence: Medium

## Skipped Context Items
| Item | Why It Matters | Downstream Behavior |
| --- | --- | --- |
| ... | ... | ... |

## Brand
Name:
Category:
Store URL:
Primary market:
Primary language:
Currency:
Brand voice:
Compliance constraints:

## Product And Offer
Hero product:
What it does:
Primary offer:
Price:
AOV:
Gross margin:
Contribution margin:
Breakeven CAC:
Target CPA:
Target ROAS:
Refund or return considerations:

## Business Goals
Primary growth goal:
Primary efficiency metric:
Decision metric hierarchy:
Target TW NCROAS:
Target Northbeam ROAS:
Target Meta ROAS:
MER target:
Blended CAC ceiling:
Contribution margin target:
Scale rule:
Cut rule:
Hold rule:
Learning rule:
Budget constraints:
Cash flow constraints:
Inventory constraints:

## Customer
Primary customer:
Jobs to be done:
Core pains:
Desired outcomes:
Objections:
Customer language:
- "..."

## Proof
Reviews:
Testimonials:
Claims allowed:
Claims to avoid:
Before/after evidence:

## Funnel
Landing page:
Conversion event:
Email/SMS capture:
Upsells:
Known conversion issues:

## Paid Social Account
Platforms:
Meta ad account ID:
Attribution setting:
Campaign structure:
Current budget:
Scaling constraints:
Known winners:
Known losers:

## Attribution And Data Sources
Primary source of truth:
Attribution platform:
Triple Whale shop/account:
Triple Whale metrics used:
Northbeam client ID:
Northbeam attribution model:
Northbeam attribution window:
Northbeam accounting mode:
Shopify/backend source:
Meta connector:
Meta ad account ID:
Meta account currency:
Data freshness:
Known tracking caveats:

## AI And Analysis Providers
Preferred visual analysis provider:
Preferred text analysis provider:
Available LLM APIs:
Available MCP servers:
Default creative analysis model:
Default text synthesis model:
Cost/latency constraints:
Data privacy constraints:

## Creative System
Current creative formats:
Creator/persona types:
Hooks that worked:
Angles that worked:
Angles to avoid:
Creative refresh cadence:
Raw asset locations:
Top creative selection rule:

## Creative Taxonomy
Awareness levels:
Avatars:
Angle families:
Hook types:
Proof types:
Offer frames:
Creative formats:
Creator archetypes:
Visual motifs:

## Creative Angle Lab Preferences
Default creative source:
Top creatives to analyze:
Video analysis method:
Static image analysis method:
Portfolio report format:
Per-creative report format:
Expansion output format:

## UGC Script Writer Preferences
Default script language:
Default script count:
Default script length:
Default creator persona:
Default output format:
Swipe library path:
Local swipe folder:
Use Gemini for local reference videos:
What not to copy:

## Reporting Preferences
Reporting cadence:
Default date range:
Default comparison range:
Primary report decision metric:
Use Meta ROAS as:
Use Triple Whale as:
Campaign drilldown limit:
Ad set drilldown limit:
Ad drilldown limit:
Dashboard owner:
Alert thresholds:
Decision meeting cadence:
Report caveats to include:
Report sections to prefer:

## KPI Exporter Preferences
Daily KPI destination:
Spreadsheet format:
Google Sheets mode:
CSV export preference:
Workbook owner:
```

## Quality Bar

- Capture numbers when available. Do not settle for "good ROAS" if target ROAS or breakeven CAC can be estimated.
- Capture optimization goals in the user's actual language, such as `Optimize for TW NCROAS >= 1.5`.
- Keep target lines machine-readable so scripts can load them, especially `Target TW NCROAS:`, `Target Northbeam ROAS:`, `Target Meta ROAS:`, `MER target:`, `Blended CAC ceiling:`, and `Target CPA:`.
- Keep preference lines machine-readable, especially `Primary report decision metric:`, `Use Meta ROAS as:`, `Default script language:`, `Swipe library path:`, `Top creatives to analyze:`, `Ad set drilldown limit:`, and `Ad drilldown limit:`.
- Capture decision rules with explicit thresholds and sample-size guardrails when the operator has them.
- Capture report customization plainly, such as `Use Triple Whale ROAS for profitability decisions and Meta ROAS only as a platform diagnostic`.
- Keep reporting cadence separate from spreadsheet/export format. Cadence affects all operating reads; CSV/XLSX/Google Sheets preferences belong under `KPI Exporter Preferences`.
- Capture UGC/script defaults so the script writer does not need to re-ask for language, count, format, or swipe library location.
- Preserve customer wording verbatim.
- Separate facts from assumptions.
- Mark unknowns as `Unknown`, not as invented guesses, but do not hide important unknowns. List them in `## Skipped Context Items`.
- Use `Not applicable`, `No special constraints`, or `No target yet` when the user gives that explicit answer.
- Keep `## Skipped Context Items` visible until the user fills or intentionally removes those items.
- Keep the document concise enough that other skills can read it quickly.

## Handoff

When saved, tell the user that VibeMarketer skills will use `.agents/vibemarketer-context.md` automatically. If skipped items remain, summarize the top 3 and explain that downstream skills will use caveats/defaults for those areas.

Always finish with `Recommended next steps`, choosing 2-4 options based on the context:

- If Meta and attribution data are connected, recommend `meta-performance-analyst` next to produce `performance-analysis.md`.
- If a fresh performance pack already exists, recommend `creative-angle-lab` on the highest-spend or most strategically important creatives.
- If creative opportunities or swipe patterns are already known, recommend `ugc-script-writer` for creator-ready scripts.
- If the user asked for daily/weekly dashboards, spreadsheet history, or scheduled reporting, recommend `paid-social-kpi-exporter`.
- If key skipped items materially affect the next step, recommend filling those specific items first.

Keep the handoff practical. Include the exact next prompt the user can send, for example:

```text
Use meta-performance-analyst with the current vibemarketer-context and latest active-spend Meta + Triple Whale data.
```
