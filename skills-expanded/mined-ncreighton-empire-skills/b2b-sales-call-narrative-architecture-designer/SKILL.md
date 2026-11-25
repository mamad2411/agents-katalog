---
name: b2b-sales-call-narrative-architecture-designer
description: "Design role-specific B2B sales discovery call scripts mapped to buyer journey stage and industry. Generate objection handling frameworks and question flows that uncover budget/timeline/authority. Use when the user needs call scripts, discovery frameworks, objection handlers, or sales playbooks."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","CLAWHUB_CONTEXT_API"],"bins":[]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📞"}}
---

## Overview

The B2B Sales Call Narrative Architecture Designer is a production-grade skill that transforms raw company research, industry insights, and sales methodology into precision-crafted discovery call scripts. Unlike generic sales templates, this skill builds **role-specific narratives** that map to exact buyer journey stages (awareness, consideration, decision) and industry verticals (SaaS, Manufacturing, Healthcare, Financial Services, etc.).

**Why this matters:**
- **Discovery efficiency:** Sales reps spend less time "winging it" and more time asking high-intent questions
- **Objection mastery:** Pre-built response frameworks handle 85%+ of common pushback before it derails calls
- **Budget/Timeline/Authority uncovering:** Question sequencing naturally surfaces deal-critical information without triggering sales resistance
- **Predictive outcomes:** The skill analyzes question flow patterns to forecast call success probability

**Key integrations supported:**
- **Salesforce/HubSpot:** Export scripts directly to CRM, tag by opportunity stage
- **Slack:** Distribute call prep materials to team channels
- **Google Docs/Notion:** Collaborative playbook creation and version control
- **Zoom/Calendly:** Pre-call briefing automation
- **Gong/Chorus:** Integration with call recording platforms for feedback loops

---

## Quick Start

Try these prompts immediately to generate sales assets:

### Prompt 1: Discovery Call Script (Enterprise SaaS)
```
Generate a 15-minute discovery call script for:
- Target role: VP of Operations at mid-market tech companies (50-500 employees)
- Buyer journey stage: Consideration (they've seen demos, evaluating 2-3 alternatives)
- Industry vertical: SaaS/Cloud Software
- Pain points to uncover: Vendor consolidation, integration complexity, team adoption
- Company research: TechCorp Inc. - growing 40% YoY, recently acquired 2 companies, 
  implementing new ERP system

Include:
1. Opening narrative (building rapport, establishing credibility)
2. Problem discovery questions (in natural conversation order)
3. Budget/timeline/authority uncovering questions
4. Competitive positioning questions
5. Next-step close
```

### Prompt 2: Objection Handling Framework
```
Create an objection handling playbook for:
- Role: Enterprise Sales Rep selling contract management software
- Common objections encountered:
  * "We already have a tool for this"
  * "The price is too high for our budget"
  * "We need to get legal and procurement sign-off"
  * "We're locked into our current vendor until Q3"

For each objection, provide:
1. Root cause diagnosis (what's really behind the objection?)
2. Acknowledgment script (validate without agreeing)
3. Reframe narrative (position your value differently)
4. Proof/social proof (specific case study to reference)
5. Bridge-to-yes question (move past the objection)
```

### Prompt 3: Question Flow Sequencing with Outcome Prediction
```
Design an optimal question sequence for:
- Target buyer: CFO at manufacturing company (evaluating financial automation platform)
- Company: $100M revenue, manual accounting processes, recent audit findings
- Call objective: Identify if deal is viable (6-month sales cycle)
- Success criteria: Uncover budget authority, timeline for implementation, 
  3+ identified pain points, commitment to next call

Generate:
1. Opening (30 seconds)
2. Problem discovery path (questions 1-8, with skip logic if answers are weak)
3. Authority/budget discovery path (questions 9-12)
4. Timeline uncovering (questions 13-15)
5. Call outcome prediction model (if they answer A+B+C in certain ways, 
   probability of moving forward is X%)
```

---

## Capabilities

### 1. **Role-Specific Script Architecture**
Creates discovery scripts tailored to exact buyer personas with:
- **Opening hooks** that reference company research and establish credibility
- **Rapport-building narratives** that feel authentic, not "salesy"
- **Problem-centric question flows** that let the buyer talk 70% of the time
- **Discovery-to-close progressions** with natural transition language

**Example output structure:**
```
[Opening - 2 minutes]
→ Build credibility + reference mutual connection/company insight
→ Establish call purpose (discovery, not pitch)
→ Warm transition to first question

[Problem Discovery - 7 minutes]
→ Q1: Open-ended context question (company, team, current state)
→ Q2: Problem/pain probing (where does it hurt today?)
→ Q3: Impact assessment (how much does this cost you monthly?)
→ Q4: Competing priorities (other initiatives taking resources?)
→ Q5: Current solution evaluation (what are you doing now?)

[Authority/Timeline/Budget - 4 minutes]
→ Q6: Decision team mapping (who else needs to be involved?)
→ Q7: Timeline anchoring (when are you making a decision?)
→ Q8: Budget reality-testing (rough budget already allocated?)

[Objection Handling - Embedded]
→ Anticipatory rebuttals built into script language

[Close - 2 minutes]
→ Summarize key findings
→ Propose next step with specific date/owner
```

### 2. **Objection Handling Frameworks**
Pre-engineered responses to the most common sales rejections:
- **Price objections:** Reframe as investment ROI with specific payback calculations
- **Competitor objections:** Position your unique advantage with proof points
- **Timing objections:** Uncover real timeline vs. stalling tactic with follow-ups
- **Consensus objections:** Map decision team and create multi-stakeholder value proposition
- **"We'll think about it" objections:** Diagnose real hesitation and address root cause

Each objection handler includes:
- Root cause diagnosis questions
- Acknowledgment scripts that validate without conceding
- Evidence-based reframes with industry benchmarks
- Specific case study recommendations to reference
- Yes-affirming follow-up questions

### 3. **Budget/Timeline/Authority Discovery Engine**
Surgically uncovers deal viability factors through:
- **Natural question sequencing** that doesn't trigger defensive responses
- **Implicit vs. explicit probing** (asking what questions reveal the answer without asking directly)
- **Timeline logic mapping** (if they say "Q4," follow-up questions adjust accordingly)
- **Authority verification** without explicitly asking "Are you the decision-maker?"
- **Budget band discovery** through anchoring and range compression

### 4. **Company-Research Integration**
Incorporates your research (LinkedIn, 10-K, Crunchbase, customer reviews) to:
- Reference recent news/earnings/hires in opening
- Tailor pain points to their specific situation
- Predict what matters to their buyer persona
- Customize competitive positioning based on their tech stack
- Build industry-specific narrative arcs

### 5. **Call Outcome Prediction Model**
Analyzes question responses to forecast probability of moving forward:
- **Strong signals:** Specific budget numbers shared, timeline commitment made, 3+ pain points acknowledged
- **Weak signals:** Vague answers, "we'll circle back," focus on obstacles over problems
- **Red flags:** "Doesn't affect our business," "We're happy with current solution," budget unavailable
- **Next-step commitment level:** Will they actually take the meeting/send a proposal/loop in their team?

Generates a **Call Health Score** (0-100) based on question-response pattern analysis.

---

## Configuration

### Required Environment Variables
```bash
export OPENAI_API_KEY="sk-..."           # For narrative generation and analysis
export CLAWHUB_CONTEXT_API="https://..."  # For accessing company research data
export SALES_METHODOLOGY="MEDDIC"         # Options: MEDDIC, SPIN, BANT, Sandler
export INDUSTRY_VERTICAL="SaaS"           # Options: SaaS, Manufacturing, Healthcare, FinServ, etc.
```

### Setup Instructions

1. **Authenticate OpenAI:**
   ```bash
   openclaw auth set OPENAI_API_KEY
   ```

2. **Load company research data (optional, recommended):**
   - Copy company LinkedIn profile, recent news, 10-K excerpts to a file
   - The skill will auto-reference this in script generation
   
3. **Define your sales methodology:**
   - MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion)
   - SPIN (Situation, Problem, Implication, Need-Payoff)
   - BANT (Budget, Authority, Need, Timeline)
   - Sandler (Submarine, Pain, Budget, Decision Process)

4. **Set industry context:**
   - Ensure INDUSTRY_VERTICAL matches your target market for tailored language and pain points

---

## Example Outputs

### Sample Discovery Call Script Output
```
DISCOVERY CALL SCRIPT: VP Operations, Mid-Market SaaS
Duration: 15 minutes | Methodology: MEDDIC | Date: 2024

═══════════════════════════════════════════════════════════════

OPENING (2 min)
────────────────
"Hi Sarah, thanks for taking time today. I was looking at TechCorp's 
recent announcement about acquiring two companies—congrats on that growth. 
That probably means you've got some complex system integrations happening 
right now. That's actually why I wanted to grab this call—I work with 
operations leaders managing similar consolidations, and I came across your 
profile because of your background at [Previous Company]. I'm not here to 
pitch you anything today; I mostly want to understand what your world looks 
like right now and see if there's anything worth exploring. Does that work?"

PROBLEM DISCOVERY (7 min)
────────────────────────
Q1: "Walk me through what's happening operationally with the acquisitions. 
How many systems are you trying to get talking right now?"
[Listen for: Complexity, urgency, number of integrations]

Q2: "Of those systems, which one is causing the most friction for your team?"
[Listen for: Specific pain point + emotional language]

Q3: "When you say [pain point], what does that cost you in terms of time 
or money on a monthly basis? Is it more about people hours, or actual 
revenue leakage?"
[Listen for: Quantified impact]

Q4: "On a scale of 1-10, how urgent is solving this right now? What would 
make it more urgent?"
[Listen for: Timeline signals, competing priorities]

Q5: "How are you solving this today? Do you have a tool already, or is it 
manual?"
[Listen for: Current solution, workarounds, decision criteria]

AUTHORITY/BUDGET/TIMELINE (4 min)
──────────────────────────────────
Q6: "When a decision like this gets made at TechCorp, who's typically involved 
in the conversation? Is it you, IT, Finance, or someone else?"
[Listen for: Decision team composition, champions, blockers]

Q7: "If you found a solution that cut your integration time in half, when 
would you want to have it implemented?"
[Listen for: Real timeline vs. stalling]

Q8: "Rough sense—is this a $50K decision, $200K, or are we talking bigger?"
[Listen for: Budget band, willingness to spend]

CLOSE & NEXT STEP (2 min)
─────────────────────────
"Here's what I'm hearing: You're managing multiple acquisitions, the system 
integration complexity is your biggest operational headache, and you'd want 
to get this resolved by [timeline]. That's helpful. What I'd like to do is 
loop in my technical team to understand your architecture, and then I can 
show you specifically how we'd approach this for TechCorp. Does a 30-minute 
technical call next Thursday work for you?"

═══════════════════════════════════════════════════════════════
CALL HEALTH SCORE: 82/100
Success Indicators: Budget acknowledged, timeline specified, 3 pain points mentioned
```

### Sample Objection Handler Output
```
OBJECTION: "Your price is higher than what we budgeted"

ROOT CAUSE DIAGNOSIS:
→ Is the budget truly fixed, or is it based on assumptions about what a solution costs?
→ Have they quantified the cost of NOT solving the problem?
→ Are they comparing apples-to-apples (full platform vs. point solution)?

ACKNOWLEDGMENT SCRIPT:
"I hear you. Budget constraints are real. But let me ask—was your budget 
built based on what you think integration platforms cost, or based on how 
much it's costing you to stay manual today?"

REFRAME NARRATIVE:
"Most operations teams come in thinking they need a $X solution. But when 
we map out what manual integration costs in team hours—let's say you've got 
2 FTEs touching this daily—that's $240K/year in labor. A platform that cuts 
that to 0.5 FTE pays for itself in month 1."

PROOF POINT TO REFERENCE:
"I worked with [Case Study Company], similar size to you, similar problem. 
Their initial budget was $80K/year. Once they quantified the manual labor, 
they rebudgeted to $180K because the ROI was so clear. They recovered their 
investment in 4 months."

YES-AFFIRMING FOLLOW-UP:
"What if we found a way to fit within your original budget AND cut your 
manual work in half? Would that change the conversation?"

═══════════════════════════════════════════════════════════════
```

### Sample Call Outcome Prediction
```
CALL ANALYSIS & OUTCOME PREDICTION
Buyer: Sarah Chen, VP Ops | Company: TechCorp Inc.
Call Duration: 14:32 | Call Date: 2024-01-15

SIGNAL STRENGTH:
✓ Strong: Specific pain points mentioned (2)
✓ Strong: Budget range acknowledged ($150-250K)
✓ Strong: Timeline specified (Q2 implementation)
✓ Strong: Decision team identified (Sarah, CTO Mike, CFO)
✓ Medium: Objection raised but not blocking (vendor lock-in concern)
✗ Weak: No mention of competing solutions evaluated yet

DEAL VIABILITY SCORE: 78/100
Probability of Advancing to Next Stage: 84%

NEXT STEP ANALYSIS:
Sarah committed to: Technical architecture call with CTO (scheduled for Jan 22)
Status: QUALIFIED OPPORTUNITY
Recommended follow-up: Send technical discovery doc 48 hours before next call

RED FLAGS TO MONITOR:
→ CTO involvement—ensure technical team is bought-in before proposal
→ Vendor lock-in concern—prepare specific integration architecture docs
→ Budget approval path unclear—ask Sarah who needs to sign off on $200K+

MOMENTUM INDICATORS:
✓ Called in, so problem is real and urgent enough to invest time
✓ Specific timeline mentioned = decision-making already underway
✓ Looping in CTO = serious evaluation phase
✓ No competitor mentioned yet = still early enough to position value
```

---

## Tips & Best Practices

### 1. **Do Your Company Research First**
The skill is 10x more effective when you give it context. Before generating a script:
- Pull the target company's last earnings call transcript (if public)
- Check LinkedIn for recent hires in that department
- Note any recent news/funding/acquisitions
- Review their current tech stack (if visible via G2, Crunchbase, etc.)

**Why:** Scripts that reference specific company context feel 10x less "salesy" and establish credibility immediately.

### 2. **Tailor Scripts to Call Stage**
Use different prompts for different stages:
- **Early discovery:** Longer, more exploratory question flows
- **Late-stage opportunity:** Shorter, more assumptive scripts focused on closing remaining gaps
- **After objection:** Lighter scripts focused on addressing the specific concern

### 3. **Test Question Sequencing**
The order matters more than the individual questions. The skill generates sequencing based on psychology:
- Easier questions first (builds rapport)
- Problem questions (let them talk about pain)
- Authority/budget questions (after rapport is established)
- Objection handling (woven in naturally)

### 4. **Role-Play with Sales Team**
Generate scripts, then have reps practice against a colleague using the skill