---
name: fte-capacity-sizing
description: Estimates the FTE capacity, role mix, seniority, utilization, and delivery load required for agency scopes, campaigns, CRM programs, media operations, or retained services. Applies a 70/30 AI-to-human operating model where 70% of task volume is handled by AI agents and 30% requires human judgment. Use when asked to size a team, build a staffing plan, estimate headcount, design a pod structure, check capacity, or determine if a fee can support a team. Also trigger when someone says "how many people do we need?", "can we staff this?", "is this team right-sized?", "what's the capacity gap?", "build me a resource plan", or when the agency-request-intake-router or scope-audit routes here due to capacity concerns. Even casual phrasing like "do we have enough people?", "who works on this?", or "is the team big enough?" should activate this skill.
---

# FTE Capacity Sizing

Translate any agency scope — SOW, retainer, campaign brief, or informal request — into a concrete staffing model with role-by-role FTE allocation, utilization analysis, seniority validation, and financial viability assessment against the proposed fee.

## The 70/30 Operating Model

This skill operates on a foundational principle: **70% of agency task volume is handled by AI agents (Claude skills, MCP flows, automated pipelines) and 30% requires irreducible human judgment, creativity, and relationships.** This is not aspirational — it is the operating assumption built into every calculation.

What this means in practice:
- A deliverable requiring 8 gross hours doesn't need 8 human hours — it needs 8 × (1 - AI rate) human hours
- A monthly report with 85% AI automation needs only 1.2 human hours (AI generates the report, a human reviews and presents)
- A creative concept with 20% AI rate still needs 12.8 human hours of 16 total (creativity remains human-led)
- The FTE count reflects the human core, not the full task volume
- Read `references/hour_benchmarks.md` → section "The 70/30 Operating Model" for the full rationale and empirical basis

## Quick Reference

| Resource | Purpose | Usage |
|----------|---------|-------|
| `scripts/capacity_calculator.py` | Core calculation engine — takes deliverables JSON, applies AI rates, calculates FTE, models utilization, assesses financials | `python capacity_calculator.py --input deliverables.json --fee 25000 --client "AcmeAuto MX" --output capacity.json` |
| `references/hour_benchmarks.md` | Industry hour benchmarks per deliverable type, AI automation rates, the 70/30 model rationale, common staffing patterns | Read for effort estimation when building the deliverables input |
| `references/role_catalog.md` | Role definitions, AI vs. human responsibility matrix, seniority minimums, pod configurations | Read when determining discipline assignment and seniority requirements |

### How to Use the Script

When the user provides scope information, follow this workflow:

1. **Extract deliverables** from the scope document or conversation
2. **Build a deliverables JSON** array using hour benchmarks from `references/hour_benchmarks.md`
3. **Run the calculator** to get quantitative results
4. **Layer qualitative analysis** — the script provides numbers, you provide judgment on team dynamics, client complexity, and market context

```python
import sys
sys.path.insert(0, "<skill-path>/scripts")
from capacity_calculator import CapacityCalculator

deliverables = [
    {"name": "Social posts (12/mo)", "quantity_per_month": 12, "hours_per_unit": 1.5,
     "task_type": "copy_variations", "discipline": "creative", "seniority": "mid"},
    {"name": "Monthly report", "quantity_per_month": 1, "hours_per_unit": 8,
     "task_type": "reporting", "discipline": "data", "seniority": "mid"},
    {"name": "Weekly optimization", "quantity_per_month": 4, "hours_per_unit": 3,
     "task_type": "bid_optimization", "discipline": "media", "seniority": "mid"},
    {"name": "Client status call", "quantity_per_month": 4, "hours_per_unit": 2,
     "task_type": "client_relationship", "discipline": "account", "seniority": "mid"},
]

calc = CapacityCalculator(deliverables, monthly_fee=15000, client_name="FreshBrew")
result = calc.calculate()

# result.total_fte_required, result.ai_pct, result.margin_pct, result.roles, etc.
```

**Calibration note**: The script uses fixed benchmark hours and AI rates. Real-world effort varies by client complexity, platform maturity, and team experience. Use the script's output as a starting point and adjust based on context. If the user provides actual time-tracking data, use those numbers instead of benchmarks.

## Trigger Conditions

Activate this skill when:

- The user needs to size a team for a scope, retainer, or campaign
- The user asks how many FTEs, what roles, or what seniority is needed
- The `scope-audit` flags capacity risk and routes here
- The `agency-request-intake-router` identifies a capacity question
- The user wants to check if a fee can support the required staffing
- The user is building a proposal and needs the team section
- The user asks about utilization or workload balance

## Sizing Process

Work through all seven steps. Each builds on the previous one.

### Step 1 — Parse Scope into Deliverables

Read the scope and decompose it into individual deliverables. For each deliverable, capture:

- **Name**: What it is (e.g., "12 Instagram posts per month")
- **Quantity per month**: How many units per month
- **Hours per unit**: Effort per unit (use `references/hour_benchmarks.md` if not provided)
- **Task type**: Classification for AI rate lookup (e.g., `reporting`, `bid_optimization`, `creative_concept`)
- **Discipline**: Which team owns it (account, strategy, creative, media, crm, data, pm, production, tech)
- **Seniority**: Minimum seniority required (junior, mid, senior, director)

If the scope doesn't specify hours, use the benchmarks. If it doesn't specify disciplines, infer from deliverable type. If seniority isn't stated, use the minimums from `references/role_catalog.md`.

### Step 2 — Apply the 70/30 AI Split

For each deliverable, apply the AI automation rate to calculate net human hours:

```
Net human hours = Gross hours × (1 - AI automation rate)
AI hours = Gross hours × AI automation rate
```

The AI rate depends on the task type. See `references/hour_benchmarks.md` for the full rate table. If a task type isn't listed, estimate based on the AI Rate Guide matrix:
- Data-driven and repetitive → 70-90%
- Structured with some judgment → 40-65%
- Strategy and creative → 20-35%
- Relationships and crisis → 5-15%

### Step 3 — Aggregate by Role

Group deliverables by discipline. For each role, sum:
- Total gross hours per month
- Total human hours per month (after AI reduction)
- Total AI hours per month

### Step 4 — Calculate FTE per Role

Convert human hours to FTE using utilization-adjusted capacity:

```
Available hours = 168 hrs/month × utilization target
FTE required = Human hours / Available hours
```

Utilization targets by seniority:
- Junior: 80% → 134.4 available hrs
- Mid: 75% → 126.0 available hrs
- Senior: 65% → 109.2 available hrs
- Director: 50% → 84.0 available hrs

### Step 5 — Assess Utilization Risk

Flag roles where:
- **Utilization > 95%**: Overstretched — burnout risk, no buffer for ad hoc work
- **Utilization > 85%**: At capacity — limited flexibility
- **FTE < 0.15**: Fragmented — too small to justify dedicated headcount, consider shared or AI-first

### Step 6 — Validate Seniority

Check each deliverable against minimum seniority requirements. Flag mismatches where a junior is assigned strategy work or a mid-level person handles executive presentations. See `references/role_catalog.md` → "Seniority Minimums by Task" for the full matrix.

### Step 7 — Financial Viability

If a monthly fee is provided, calculate:

```
Total monthly cost = Σ (FTE per role × monthly cost per FTE at that seniority)
Margin = (Fee - Cost) / Fee × 100
```

Use cost benchmarks from `references/hour_benchmarks.md` → "Role Cost Benchmarks."

Issue a verdict:
- **Viable**: Margin ≥ 30% (target)
- **Tight but viable**: Margin 15-30%
- **Underfunded**: Margin 0-15%
- **Non-viable**: Negative margin

## Output Format

Produce the capacity model in TWO forms: first as an **inline visual artifact** (rendered in chat via the Visualizer), then as a **structured markdown report** below it.

### Visual Artifact (Primary)

Render the capacity model as an inline HTML widget using the Visualizer. The widget should display:

- A **header bar** color-coded by verdict: green (Viable), amber (Tight), orange (Underfunded), red (Non-viable)
- A **top metrics row** with 4 cards: Total FTE, AI/Human split (as "70/30" style ratio), Monthly cost, Margin %
- A **role allocation table** — one row per role showing: discipline, seniority, gross hrs, human hrs, AI hrs, FTE, utilization %, status badge (OK/Overstretched/Fragmented)
- A **stacked bar** showing the AI vs. human hour breakdown visually (green for AI, blue for human)
- An **alerts section** listing utilization risks and seniority gaps with severity badges
- An **action footer** with `sendPrompt()` buttons:
  - "Run margin simulation for [client] with this staffing model" → routes to `margin-simulation`
  - "Generate scope change order to reduce deliverables" → routes to `change-order-generator`
  - "Draft executive memo with team recommendation" → routes to `executive-growth-memo`

Use CSS variables for light/dark mode. Keep it compact — a staffing dashboard card, not a spreadsheet.

### Markdown Report (Secondary)

After the visual artifact, produce the full capacity model as markdown:

```
## 👥 FTE CAPACITY MODEL — [Client / Project Name]

### Staffing summary
[2-3 sentences: total FTE, AI/human split, verdict, key risk]

### The 70/30 split
| Metric | Value |
|--------|-------|
| Total gross hours/month | [X] |
| AI-operated hours (70% target) | [X] ([Y]%) |
| Human hours (30% target) | [X] ([Y]%) |
| Total FTE required (human) | [X] |

### Role-by-role allocation
| Role | Seniority | Gross hrs | Human hrs | AI hrs | FTE | Utilization | Status |
|------|-----------|-----------|-----------|--------|-----|-------------|--------|
[One row per role]

### Utilization risk
[Table: role | issue | severity | recommendation]

### Seniority gaps
[If any: deliverable | assigned | minimum | recommendation]

### Financial viability
| Metric | Value |
|--------|-------|
| Monthly fee | $[X] |
| Monthly team cost | $[X] |
| Margin | [X]% |
| Verdict | [Viable / Tight / Underfunded / Non-viable] |

### Required vs. funded capacity
[If underfunded: which roles are the gap, what to cut or renegotiate]

### Recommendations
[Numbered list of specific actions]
```

### When Information Is Incomplete

If the user provides only a partial scope or verbal summary:
- Use benchmark hours from `references/hour_benchmarks.md` for estimation
- Note assumptions explicitly (e.g., "Assumed 8 hrs/report based on industry benchmark")
- Mark uncertain fields with `⚠️ Estimated — [basis]`
- Recommend providing the full SOW or time-tracking data for a precise model

## Examples

**Example 1 — Small social retainer:**

User: "We need to size a team for a social-only retainer: 12 posts/month on Instagram and TikTok, monthly report, weekly client call. Fee is $10,000/month."

→ 0.8 FTE total (0.3 Creative mid, 0.2 Account mid, 0.15 Data mid, 0.15 PM mid). AI handles 68% of hours. Margin: 42%. Verdict: Viable.

**Example 2 — Underfunded full-service:**

User: "Client wants full-service digital: media planning, creative production, CRM journeys, monthly reporting, QBRs. Fee: $18,000/month."

→ 2.1 FTE required across 6 disciplines. Cost: $22,400/month. Margin: -24%. Verdict: Non-viable. Recommendation: reduce scope or increase fee by $6,000+.

**Example 3 — Capacity check:**

User: "Our media team is already at 90% utilization. Can we take on this new $15K/month account that needs 3 campaigns per month?"

→ New account requires 0.4 FTE media. Current team at 90% → would push to 120%. Risk: Critical. Recommendation: hire 0.5 FTE media mid or redistribute existing workload with AI automation uplift.

## Skill Chaining

This skill frequently connects to:

| Condition | Next skill |
|-----------|-----------|
| Fee can't support required team | `margin-simulation` to model alternatives |
| Scope needs reducing to fit budget | `change-order-generator` |
| Team recommendation needs leadership summary | `executive-growth-memo` |
| Staffing model is set, campaign ready to launch | `campaign-launch-qa` |
| Utilization is critical, need weekly monitoring | `weekly-control-tower` |
