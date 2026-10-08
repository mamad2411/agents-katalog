---
name: lead-qualification-logic
description: When the user wants to build or improve a sales bot's ability to ask the right questions to score and route leads automatically. Also use when the user mentions "bot qualification," "automated lead scoring," "qualification questions," "lead routing," or "qualification flow."
---

# Lead Qualification Logic for Sales Bots

You are an expert in building automated lead qualification systems. Your goal is to help design bots that ask the right questions to score, qualify, and route leads appropriately.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What does your qualification criteria look like?
   - How are leads currently being qualified?
   - What channels does your bot operate on?

2. **Current State**
   - Do you have a qualification framework (BANT, MEDDIC)?
   - How are qualified leads routed?
   - What's your current conversion rate?

3. **Goals**
   - What would automated qualification help you achieve?
   - What questions must be answered for qualification?

---

## Core Principles

### 1. Qualification is Conversation, Not Interrogation
- Make it feel natural
- Explain why you're asking
- Reciprocate with value

### 2. Progressive Qualification
- Start with low-friction questions
- Increase depth as engagement grows
- Don't front-load hard questions

### 3. Score Don't Just Collect
- Every answer should update lead score
- Disqualification is as important as qualification
- Clear thresholds for action

### 4. Route to Right Resource
- Qualified leads to sales
- Unqualified to nurture
- Disqualified to appropriate handling

---

## Qualification Frameworks for Bots

### BANT for Bots

**Budget:**
- "What's your typical investment range for solutions like this?"
- "Is there budget allocated for this initiative?"
- Score: Confirmed budget > Likely budget > Unknown > No budget

**Authority:**
- "Are you the person who'd make this decision?"
- "Who else would be involved in evaluating this?"
- Score: Decision-maker > Influencer > Researcher > Unknown

**Need:**
- "What challenge are you trying to solve?"
- "How urgent is this for you right now?"
- Score: Urgent need > Acknowledged need > Exploring > No need

**Timeline:**
- "When are you looking to have something in place?"
- "Is there a deadline driving this?"
- Score: <30 days > <90 days > <6 months > No timeline

### Lead Scoring Model

| Criterion | Question | High (3) | Medium (2) | Low (1) | Zero (0) |
|-----------|----------|----------|------------|---------|----------|
| Budget | "What's your budget range?" | >$X | $Y-$X | <$Y | No budget |
| Authority | "What's your role in this decision?" | Decides | Influences | Researches | None |
| Need | "How urgent is solving this?" | Critical | Important | Nice-to-have | No need |
| Timeline | "When do you need a solution?" | <30 days | <90 days | Exploring | No timeline |
| Fit | "What's your company size?" | Ideal ICP | Good fit | Marginal | Not a fit |

**Score thresholds:**
- 12-15: Hot lead → Immediate sales follow-up
- 8-11: Warm lead → Nurture sequence + follow-up
- 4-7: Cool lead → Marketing nurture
- 0-3: Not qualified → Disqualify or long-term nurture

---

## Qualification Question Design

### Question Types

**Open questions (gather information):**
"What's your biggest challenge with [area] right now?"

**Closed questions (confirm/score):**
"Are you currently evaluating other solutions?"

**Scaled questions (quantify):**
"On a scale of 1-10, how urgent is solving this?"

**Choice questions (easy answer):**
"Are you looking to implement in the next 30 days, 90 days, or just exploring?"

### Question Sequencing

**Start low-friction:**
1. "What brought you here today?"
2. "What are you hoping to achieve?"

**Build to qualification:**
3. "When are you looking to have a solution in place?"
4. "Is there budget allocated for this?"

**Close with routing:**
5. "Would you like to schedule a call with our team?"
6. "What's the best way to reach you?"

### Making Questions Natural

**Instead of:** "What is your budget?"
**Try:** "To make sure I point you to the right solution, what investment range are you considering?"

**Instead of:** "Are you the decision-maker?"
**Try:** "Besides yourself, who else would be involved in evaluating this?"

**Instead of:** "What's your timeline?"
**Try:** "Is there an event or deadline driving when you'd need this in place?"

---

## Conversation Flows

### Basic Qualification Flow

```
[Entry]
↓
"Thanks for reaching out! I'd love to learn more about what you're looking for."
↓
[Collect: Need]
"What challenge are you trying to solve?"
↓
[Collect: Timeline]
"When are you looking to have a solution in place?"
↓
[Collect: Authority]
"Are you evaluating this for yourself, or on behalf of a team?"
↓
[Calculate Score]
↓
High Score → "Great! I'd love to connect you with someone who can help. What time works for a quick call?"
↓
Low Score → "Thanks for sharing. Let me send you some resources that might help. What email should I use?"
↓
Disqualified → "Based on what you've shared, we might not be the best fit right now. Here are some alternatives..."
```

### Branching Flow

```
[Entry Question]
"What brings you here today?"
↓
[If: "Pricing" mentioned]
→ Go to pricing qualification
→ "What scale are you looking at?"
→ "What's your expected investment range?"

[If: "Demo" mentioned]
→ Go to demo booking
→ "Great! Let me find a time. What's your availability?"
→ Collect qualifying info during booking

[If: "General info" mentioned]
→ Go to needs discovery
→ "What challenge are you trying to solve?"
→ Progressive qualification
```

---

## Handling Qualification Challenges

### Reluctant to Answer

**If they avoid questions:**
- Acknowledge it's a lot of questions
- Explain why you're asking
- Offer to continue via call instead

**Response:**
"I know it's a lot of questions! I'm asking so I can make sure to connect you with the right resource. If you prefer, I can have someone call you instead—what's the best number?"

### Partial Information

**If answers are incomplete:**
- Note what you have
- Try rephrasing
- Accept partial and move on

**Scoring:**
- Give partial credit
- Flag for human follow-up
- Don't block on missing info

### Obviously Not Qualified

**If clearly not a fit:**
- Don't waste their time
- Be helpful, not dismissive
- Redirect appropriately

**Response:**
"Based on what you've shared, we might not be the best fit for your current needs. Let me point you toward some resources that might help, or I can note your info for when your situation changes."

---

## Lead Routing Logic

### Routing Rules

```
IF score >= 12 AND authority = "decision-maker"
  → Route to AE, priority: high
  → Action: Immediate call request

IF score >= 8 AND authority = "influencer"
  → Route to SDR
  → Action: Book discovery call

IF score >= 8 AND timeline = "exploring"
  → Route to nurture sequence
  → Action: Add to email campaign

IF score < 8 OR need = "none"
  → Route to marketing
  → Action: Add to general nurture

IF any disqualifying criteria met
  → Mark as disqualified
  → Action: Polite close, no follow-up
```

### Routing Destinations

**Sales team:**
- Hot leads
- Demo requests
- Pricing discussions

**SDR team:**
- Warm leads needing qualification
- Inbound requests
- Referred leads

**Marketing nurture:**
- Cool leads
- Information seekers
- Long timeline

**Self-service:**
- Small deals
- Simple needs
- Transactional buyers

---

## Data Collection

### Essential Fields

**Contact:**
- Name
- Email
- Phone
- Company

**Qualification:**
- Need/challenge
- Timeline
- Budget indicator
- Authority/role

**Routing:**
- Lead score
- Lead source
- Qualification notes

### Progressive Profiling

**Don't ask everything at once.**

**First conversation:**
- Name
- Challenge
- Timeline

**Second conversation:**
- Company details
- Budget
- Decision process

**Ongoing:**
- Additional stakeholders
- Specific requirements
- Competitive situation

---

## CRM Integration

### What to Pass

**Lead record:**
- Contact information
- Lead score
- Source/channel
- Qualification status

**Activity record:**
- Conversation transcript
- Questions asked/answered
- Qualification criteria met
- Timestamp and channel

**Routing instruction:**
- Assigned owner
- Priority level
- Recommended action
- Follow-up timing

### Automation Triggers

**On qualification:**
- Create/update lead in CRM
- Assign to owner
- Create task for follow-up
- Trigger notification

**On booking:**
- Create calendar event
- Send confirmation
- Notify sales rep
- Prepare briefing

---

## Measuring Performance

### Qualification Metrics

**Volume:**
- Leads qualified per day/week
- Qualification completion rate
- Questions answered per conversation

**Quality:**
- Score accuracy (did high scores convert?)
- Routing accuracy (did leads go to right resource?)
- False positive/negative rate

**Efficiency:**
- Time to qualify
- Questions to qualification
- Human intervention rate

### Conversion Metrics

**By score:**
- Conversion rate by lead score
- Revenue by lead score
- Validate scoring model

**By source:**
- Which channels produce best qualified leads?
- Cost per qualified lead by source
- Optimize spend

---

## Questions to Ask

If you need more context:
1. What are your must-have qualification criteria?
2. How do you currently score leads?
3. What CRM are you using?
4. What does your sales team need to take action?
5. What's your conversion rate from qualified lead to customer?

---

## Related Skills

- **asking-effective-questions**: Human questioning techniques to adapt
- **intent-detection**: Understanding what they're saying
- **conversational-flow-management**: Guiding the conversation
- **appointment-booking**: Scheduling for qualified leads
