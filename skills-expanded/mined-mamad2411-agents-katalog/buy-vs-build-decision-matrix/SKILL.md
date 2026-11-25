---
name: Buy vs Build Decision Matrix
description: Evaluates build-vs-buy decisions using 7 dimensions (strategic fit, cost, time, risk, differentiation, control, learning). Includes 3-year TCO calculator with learning weights.
version: 1.0.0
dependencies: python>=3.8
---

# Buy vs Build Decision Matrix

## Overview

The build-vs-buy decision is **not** primarily about cost. It's about strategic alignment, competitive differentiation, and opportunity cost. This skill provides a systematic framework for making these decisions with rigor.

**When to use this skill:**
- Before committing to building a major feature or platform component
- When evaluating third-party tools or services
- When opportunity cost is high (e.g., solo founder, small team)
- When decision has long-term strategic implications

## The 7 Dimensions

### 1. Strategic Fit & Differentiation

**Question:** Is this a core competency or competitive differentiator?

**Framework:**

| Category | Build | Buy |
|----------|-------|-----|
| **Core Differentiator** | Must build | Never buy |
| **Strategic Enabler** | Probably build | Maybe buy if best-in-class |
| **Commodity** | Never build | Always buy |

**Example (AI coding agent context):**

- **Core Differentiator:** LLM orchestration, prompt engineering, agent reasoning
  - **Decision:** BUILD (this is your moat)

- **Strategic Enabler:** Authentication, user management
  - **Decision:** BUY (Supabase Auth) — not differentiated but must be solid

- **Commodity:** Email delivery, payment processing
  - **Decision:** BUY (Postmark, Stripe) — zero competitive value

**Red Flags for "Buy":**
- Vendor lock-in prevents future differentiation
- Third-party tool becomes customer-facing (your brand = their UX)
- Vendor roadmap conflicts with your strategy

### 2. Total Cost of Ownership (3-Year)

**Components:**

```
TCO = Development + Maintenance + Opportunity Cost + Switching Cost
```

**Build Costs:**
- Initial development (engineering time × rate)
- Ongoing maintenance (bug fixes, updates, security patches)
- Infrastructure (hosting, monitoring, scaling)
- Opportunity cost (what else could you build?)

**Buy Costs:**
- Subscription fees (month 1 → year 3)
- Integration cost (API integration, data migration)
- Training/onboarding
- Vendor lock-in risk (switching cost if you outgrow tool)

**TCO Calculator:** See `scripts/tco_3y_calc.py` for detailed model.

**Example (simplified):**

**Scenario:** Build vs Buy authentication system

| Cost Category | Build | Buy (Supabase Auth) |
|---------------|-------|---------------------|
| **Initial Dev** | $15K (3 weeks) | $2K (3 days integration) |
| **Annual Maintenance** | $8K/year | $0 (vendor maintains) |
| **Infrastructure** | $500/year | $0 (included) |
| **Subscription** | $0 | $600/year (Pro plan) |
| **Opportunity Cost** | $30K (could build 2 features instead) | $0 |
| **3-Year Total** | **$60.5K** | **$3.8K** |

**Verdict:** BUY (16x cheaper, not differentiated)

### 3. Time to Market

**Question:** How soon do you need this capability?

**Analysis:**

- **Build Time:** Estimate in story points, convert to calendar weeks
- **Buy Time:** Integration time (typically 1-5 days for SaaS tools)
- **First-Mover Advantage:** Is speed critical? (Launch window, competitive pressure)

**Example:**

- **Build:** Custom analytics dashboard = 8 SP = 4 weeks
- **Buy:** Integrate Mixpanel = 0.5 SP = 2 days
- **Market Context:** Competitor launching in 6 weeks
- **Verdict:** BUY (speed matters more than custom features)

### 4. Risk & Uncertainty

**Categories:**

**Execution Risk (Build):**
- **High:** Team has never built this before (e.g., real-time collaboration)
- **Medium:** Team has adjacent experience (e.g., built REST APIs, now need GraphQL)
- **Low:** Team has done this multiple times (e.g., CRUD APIs)

**Vendor Risk (Buy):**
- **High:** Startup with <2 years runway, unknown reliability
- **Medium:** Mid-market vendor, some customers, unclear longevity
- **Low:** Established vendor (Stripe, AWS, Cloudflare)

**Risk Mitigation:**

| Risk Type | Mitigation |
|-----------|------------|
| **Execution (Build)** | Prototype/spike (2-3 days), validate feasibility |
| **Vendor (Buy)** | Contract escape clauses, data export plan, multi-vendor strategy |

### 5. Control & Flexibility

**Question:** How much control do you need over behavior, data, and roadmap?

**Control Spectrum:**

| Build | Buy (API) | Buy (No-Code SaaS) |
|-------|-----------|-------------------|
| Full control | Medium control | Low control |
| Custom behavior | Constrained by API | Constrained by UI |
| Own your data | Data via API | Vendor owns data |

**When Control Matters:**
- **High:** Customer data (privacy, compliance), core product logic
- **Medium:** Internal tools, analytics
- **Low:** Commodity utilities (email, payments)

**Example:**

- **AI Agent Reasoning:** Need full control over prompt chaining, context management
  - **Decision:** BUILD

- **Usage Analytics:** Need basic dashboards, don't need custom queries
  - **Decision:** BUY (PostHog, Mixpanel)

### 6. Learning & Capability Building

**Question:** Does building this make your team stronger in strategically valuable ways?

**Learning Value:**

| Scenario | Learning Value | Decision Bias |
|----------|---------------|---------------|
| **Core tech stack** (e.g., LLM orchestration) | High | BUILD |
| **Adjacent capability** (e.g., real-time sync) | Medium | LEAN BUILD (unless time-critical) |
| **Commodity** (e.g., email delivery) | None | BUY |

**Caution:** "Learning" is not a justification if:
- The capability is not strategically valuable long-term
- Opportunity cost is high (could learn more valuable skills instead)
- Team already has this expertise

### 7. Ecosystem & Community

**Question:** Is there a vibrant ecosystem, or will you be alone?

**Ecosystem Signals:**

**For Build:**
- Open-source libraries with active maintenance
- StackOverflow questions, tutorials, community support
- Hiring pool (can you find engineers with this skill?)

**For Buy:**
- Vendor has integrations with your stack
- Strong customer community (Slack, forums)
- Regular product updates, transparent roadmap

**Red Flags:**

- **Build:** Dead libraries, no community, hard to hire
- **Buy:** Vendor lacks integrations, poor support, declining usage

---

## Decision Matrix Template

```json
{
  "decision": "Build vs Buy: Authentication System",
  "date": "2025-10-18",
  "context": "Solo founder, need to launch MVP in 8 weeks",
  "evaluated_by": ["pe-designer", "sde-iii", "finance-consultant"],

  "dimensions": {
    "strategic_fit": {
      "category": "commodity",
      "score_build": 2,
      "score_buy": 8,
      "rationale": "Auth is not a differentiator. Supabase is best-in-class."
    },
    "tco_3yr": {
      "build_cost_usd": 60500,
      "buy_cost_usd": 3800,
      "score_build": 1,
      "score_buy": 10,
      "rationale": "Buy is 16x cheaper over 3 years."
    },
    "time_to_market": {
      "build_weeks": 3,
      "buy_weeks": 0.4,
      "score_build": 2,
      "score_buy": 10,
      "rationale": "Need to launch in 8 weeks. Can't afford 3-week auth build."
    },
    "risk": {
      "execution_risk_build": "medium",
      "vendor_risk_buy": "low",
      "score_build": 5,
      "score_buy": 9,
      "rationale": "Supabase is established, YC-backed. Build risk: team has no OAuth2 experience."
    },
    "control": {
      "control_needed": "medium",
      "score_build": 10,
      "score_buy": 7,
      "rationale": "Supabase gives API control, data export. Acceptable."
    },
    "learning": {
      "learning_value": "low",
      "score_build": 3,
      "score_buy": 8,
      "rationale": "Building OAuth2 teaches nothing strategic. Time better spent on AI agent logic."
    },
    "ecosystem": {
      "score_build": 6,
      "score_buy": 10,
      "rationale": "Supabase has huge community, integrations. Build: would use Passport.js (mature but generic)."
    }
  },

  "weights": {
    "strategic_fit": 0.25,
    "tco_3yr": 0.20,
    "time_to_market": 0.20,
    "risk": 0.15,
    "control": 0.10,
    "learning": 0.05,
    "ecosystem": 0.05
  },

  "weighted_scores": {
    "build_total": 3.85,
    "buy_total": 8.75
  },

  "recommendation": "BUY",
  "confidence": "high",
  "rationale": "Buy scores 8.75 vs Build's 3.85 (2.3x advantage). Auth is commodity, Supabase is mature, time-to-market is critical, and cost savings are massive. No strategic reason to build.",

  "decision_record": "decisions/ADR-005-use-supabase-auth.md",

  "reversibility": {
    "switching_cost_usd": 5000,
    "switching_time_weeks": 2,
    "lock_in_risk": "low",
    "rationale": "Supabase uses standard JWT. Can migrate to Auth0 or self-hosted if needed."
  },

  "assumptions": [
    "Team has no OAuth2 expertise (true as of Oct 2025)",
    "Supabase pricing remains stable (<$100/month for first year)",
    "Auth is not a competitive differentiator (validated via customer interviews)"
  ],

  "triggers_for_reversal": [
    "Supabase raises prices >3x",
    "Supabase shuts down or gets acquired by competitor",
    "Customer demands on-prem auth (enterprise pivot)"
  ]
}
```

---

## The Learning Weights System

**Problem:** Default weights may not match your decision-making style.

**Solution:** Track decisions, identify patterns, adjust weights over time.

### How It Works

1. **Baseline Weights** (industry standard):
   ```json
   {
     "strategic_fit": 0.25,
     "tco_3yr": 0.20,
     "time_to_market": 0.20,
     "risk": 0.15,
     "control": 0.10,
     "learning": 0.05,
     "ecosystem": 0.05
   }
   ```

2. **Track Decisions:** Log each build-vs-buy decision with:
   - Weighted scores (using current weights)
   - Actual decision made
   - Factors that influenced final call

3. **Analyze Patterns** (quarterly):
   - "When I chose Build despite Buy scoring higher, which dimension did I weight heavily?"
   - "When I chose Buy, was TCO or time-to-market more important?"

4. **Adjust Weights:**
   - If you consistently override matrix for "strategic_fit" → increase weight
   - If you never consider "learning" → decrease weight to 0.01

**Script:** `scripts/decision_tracker.py` logs decisions and suggests weight adjustments.

**Example:**

After 10 decisions, pattern emerges:
- Founder overrode matrix 3 times to BUILD when "strategic_fit" was high
- Founder never overrode for "learning" (doesn't care about skill-building)

**Adjusted Weights:**
```json
{
  "strategic_fit": 0.35,  // ↑ from 0.25
  "tco_3yr": 0.25,        // ↑ from 0.20 (solo founder is cost-sensitive)
  "time_to_market": 0.20, // unchanged
  "risk": 0.10,           // ↓ from 0.15 (founder is risk-tolerant)
  "control": 0.05,        // ↓ from 0.10 (comfortable with third-party APIs)
  "learning": 0.02,       // ↓ from 0.05 (not a factor)
  "ecosystem": 0.03       // ↓ from 0.05 (cares less about community)
}
```

---

## TCO Calculator (3-Year Model)

**Script:** `scripts/tco_3y_calc.py`

**Inputs:**
- Engineering rate ($/hour)
- Estimated build time (story points)
- Vendor pricing (per month/year)
- Infrastructure costs
- Maintenance burden (% of initial build time per year)
- Opportunity cost (what else could you build?)

**Output:**
```json
{
  "build": {
    "initial_dev": 15000,
    "year1_maintenance": 8000,
    "year2_maintenance": 8000,
    "year3_maintenance": 8000,
    "infrastructure_3yr": 1500,
    "opportunity_cost": 30000,
    "total_3yr": 60500
  },
  "buy": {
    "integration": 2000,
    "year1_subscription": 600,
    "year2_subscription": 600,
    "year3_subscription": 600,
    "total_3yr": 3800
  },
  "savings_buy": 56700,
  "roi_buy": 14.9
}
```

---

## Decision Workflow

1. **Trigger:** Team identifies build-vs-buy decision
2. **COS invokes this skill** → assigns specialists:
   - PE-designer: evaluates strategic fit, control, ecosystem
   - Finance-consultant: calculates TCO, ROI
   - SDE-III: estimates build effort, assesses risk
3. **Specialists submit position memos** (may disagree)
4. **Dissent-moderator creates options matrix** (if disagreement exists)
5. **COS synthesizes into decision matrix JSON**
6. **Founder makes final call** (may override matrix based on intuition)
7. **Decision logged** → `scripts/decision_tracker.py` for weight learning

---

## Quality Checklist

Before finalizing decision:

- [ ] All 7 dimensions scored (1-10 scale)
- [ ] TCO calculated (3-year horizon)
- [ ] Weights sum to 1.0
- [ ] Assumptions explicitly stated
- [ ] Reversibility assessed (switching cost, lock-in risk)
- [ ] Triggers for reversal defined (when to revisit decision)
- [ ] ADR created (if decision is architectural)

---

## Common Mistakes

❌ **Cost-Only Analysis:** "Buy is cheaper, so we buy."
✅ **Multi-Dimensional:** Consider strategic fit, control, time.

❌ **Ignoring Opportunity Cost:** "Build only costs $20K."
✅ **Full TCO:** "$20K build + $30K opportunity cost = $50K true cost."

❌ **Static Weights Forever:** Using defaults for every decision.
✅ **Learning Weights:** Adjust based on your decision patterns.

❌ **No Reversal Plan:** "We'll buy and never revisit."
✅ **Reversibility Check:** "We'll buy now, build if Vendor raises prices 3x."

---

## Output Files

1. **Primary:** `buy_build.json` - Full decision matrix with scores
2. **Supporting:** `decisions/ADR-###.md` - Architecture Decision Record
3. **Tracking:** `decisions/decision_log.csv` - Logged for weight learning

---

## References

See `scripts/tco_3y_calc.py` for TCO model implementation
See `scripts/decision_tracker.py` for weight learning system
See `templates/buy-vs-build-template.json` for JSON schema
