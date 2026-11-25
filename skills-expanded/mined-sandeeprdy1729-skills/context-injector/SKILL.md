---
name: context-injector
description: >
  Persistent context management skill that ends the 'let me explain again' tax.
  Activates when the user is frustrated by having to re-explain their role,
  project, stack, or constraints at the start of every session — or when
  Claude's answers feel generic because they're missing context.
  Builds a structured context template, scores what's missing, injects relevant
  context per question type, and detects when responses suggest that context
  has drifted or been forgotten.
  Use when user says: let me explain my situation, again, as I mentioned, you
  keep forgetting, you don't know my context, I have to re-explain this every
  time, your answer is too generic, this doesn't apply to my situation, give me
  a more personalised answer, I've already told you, set up context, save my
  context, remember this, I need you to know about my project.
  Do NOT activate for: one-off questions where context is irrelevant,
  factual questions with no personal dimension, code debugging where
  the code itself is the context.
  First response: "Context Injector active. Let's build your context template
  so I stop answering for a generic user. Run /build to start."
license: Apache 2.0
---

# Context Injector

The default Claude session starts from zero. The user spends 5–10 minutes
re-explaining who they are, what they're building, who their audience is, and
what constraints they're working under. Claude acknowledges this and then
immediately gives an answer that ignores half of it.

The real problem is not memory — it is that the context never gets structured
enough to be reliably applied. This skill builds a structured context template,
scores its quality, and injects the right context per question type.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/build` | Interactive context template builder (role, project, stack, audience, constraints) |
| `/score` | Score the current context template — what's missing that would change answers most |
| `/inject <question>` | Show what context would be injected for a given question type |
| `/drift` | Audit the last N responses for signs that context was forgotten |
| `/reset` | Clear the stored context template |
| `/review` | Display the current context template for editing |
| `/update <field> <value>` | Update a specific field in the context template |
| `/assume` | List what Claude is currently assuming about the user in the absence of context |
| `/apply <question>` | Answer a question right now through the lens of the built context — skip the generic answer |
| `/deepen <dimension>` | Drill deeper into any context dimension with more specific questions |
| `/freshness` | Show when each dimension was last updated; flag dimensions that are stale or thin |
| `/next` | Given what's been built so far, what single context dimension would most improve the next answer |

---

## HIGH-LEVEL WORKFLOW

```text
User wants to stop re-explaining their context
    │
    ├─ Phase 1: Context Template Builder
    │     Collect structured context across 5 dimensions
    │
    ├─ Phase 2: Context Quality Scorer
    │     Identify what's missing and how much it would change answers
    │
    ├─ Phase 3: Dynamic Injection
    │     Route the right subset of context per question type
    │
    ├─ Phase 4: Drift Detection
    │     Flag when responses suggest context was forgotten
    │
    └─ Phase 5: Iteration
          Update the template when context changes; propagate changes
          After /build: immediately offer to answer the user's first question through context
          After drift: identify which dimension drifted and ask 1 targeted update question
```

---

## PHASE 1 — CONTEXT TEMPLATE BUILDER

The template covers 5 dimensions. Collect them through guided questions, not a form dump.
Ask one dimension at a time. Don't make the user fill in a YAML file.

### Dimension 1: Role

What the user does professionally or in the context of this work.

**Prompts:**
- "What's your role? (e.g., solo founder, senior engineer at a startup, freelance designer)"
- "What does a normal day look like for you in this role?"
- "What decisions do you make frequently?"

**What to capture:**
- Title and type (technical / non-technical / mixed)
- Organisation type (solo / startup / enterprise / freelance)
- Level of authority (builds things themselves vs delegates vs directs)
- Decision-making context (time pressure, resource constraints, approval chains)

### Dimension 2: Project

What they're currently working on that they'll be asking about.

**Prompts:**
- "What project are you working on right now?"
- "What stage is it at? (idea / prototype / live product / scaling)"
- "What's the goal for the next 4–8 weeks?"

**What to capture:**
- Project name and type (SaaS / API / content / research / personal / org-wide)
- Current stage (0→1 / 1→10 / maintenance / legacy)
- Near-term goal (ship v1 / hit first 100 users / refactor / document / decide)
- Biggest current constraint (time / money / skills / clarity / org buy-in)

### Dimension 3: Stack

Technical or tool context that affects what answers are relevant.

**Prompts:**
- "What's the tech stack? (or: what tools are you using?)"
- "What can't you change? (locked-in decisions, existing systems)"
- "What are you considering changing?"

**What to capture:**
- Primary language(s) and framework(s)
- Hosting / infrastructure
- Key third-party dependencies
- Hard constraints (can't migrate, existing contracts, team skill lock-in)
- Preferred tools for common tasks (testing, deployment, monitoring)

### Dimension 4: Audience

Who the user's work is ultimately for.

**Prompts:**
- "Who is the end user of what you're building?"
- "What do they know? What do they not know?"
- "What do they care most about?"

**What to capture:**
- User type (developer / non-technical user / enterprise buyer / consumer / internal team)
- Sophistication level (beginner / intermediate / expert)
- Key pain (what they are hiring the product/content/service to do)
- What would make them stop using it

### Dimension 5: Constraints

What limits the user's options — the context that most changes Claude's answers.

**Prompts:**
- "What are you not willing to do? (or can't do)"
- "What have you already tried that didn't work?"
- "What would make an otherwise-good answer not useful for you?"

**What to capture:**
- Hard nos (technologies, approaches, vendors to avoid)
- Already-tried solutions
- Budget, time, or team constraints
- Quality bar for "good enough" (perfection vs ship fast)
- Audience constraints (can't use jargon, must work in a certain format)

### Template output format

```yaml
CONTEXT TEMPLATE
──────────────────────────────────────────────────────────────────
ROLE
  Title         : [role]
  Org type      : [solo / startup / enterprise / freelance]
  Tech level    : [builder / director / mixed]
  Decision style: [fast and reversible / slow and high-stakes]

PROJECT
  Name          : [project]
  Type          : [SaaS / API / content / research / other]
  Stage         : [0→1 / 1→10 / maintenance / legacy]
  Near-term goal: [one sentence]
  Constraint    : [biggest current constraint]

STACK
  Languages     : [list]
  Frameworks    : [list]
  Hosting       : [where it runs]
  Hard limits   : [what can't change]
  Preferred tools: [testing, deployment, monitoring]

AUDIENCE
  Type          : [developer / consumer / enterprise / internal]
  Sophistication: [beginner / intermediate / expert]
  Core pain     : [what they hire the product to solve]
  Churn signal  : [what would make them leave]

CONSTRAINTS
  Hard nos      : [what not to suggest]
  Already tried : [what didn't work]
  Budget/time   : [relevant limits]
  Quality bar   : [ship fast vs polished]
──────────────────────────────────────────────────────────────────
```

---

## PHASE 2 — CONTEXT QUALITY SCORER

After the template is built, score it by impact — not completeness.

**Scoring principle:** A missing field is high-impact if answering a common question
differently with and without that field would produce materially different advice.

### Impact scoring per dimension

| Field | High impact if missing because… |
| --- | --- |
| Tech level | Beginner vs expert answers are completely different |
| Stage (0→1 vs scaling) | Early advice (speed, validation) vs late advice (reliability, process) |
| Hard limits | Recommending something they can't use wastes the whole answer |
| Already tried | Recommending something that failed wastes trust |
| Audience sophistication | Jargon vs plain language; detail level |
| Near-term goal | Tactical vs strategic framing; urgency level |
| Budget/time | "Ideal" vs "good enough given 2 hours this week" |

**Scorer output format:**

```text
CONTEXT QUALITY SCORE
──────────────────────────────────────────────────────────────────
  Score: 7/10  — usable but 3 high-impact fields are missing

  COMPLETE (won't change answers much if filled in)
    ✓ Role and org type
    ✓ Project type and stage
    ✓ Stack and hard limits

  MISSING — HIGH IMPACT
    ✗ "Already tried" — without this, I may recommend what you've already
      ruled out. Add 1–2 things you tried that didn't work.
    ✗ "Near-term goal" — I'm answering for a general goal. With this,
      I can prioritise the right type of advice.
    ✗ "Audience sophistication" — affects tone and detail level significantly.

  OPTIONAL (won't change most answers)
    ○ Churn signal
    ○ Hosting preference
──────────────────────────────────────────────────────────────────
```

---

## PHASE 3 — DYNAMIC INJECTION

Not all context is relevant to every question. Inject the right subset.

### Context routing by question type

| Question type | Primary context to inject | Secondary |
| --- | --- | --- |
| Technical (how do I build X) | Stack, hard limits, tech level | Stage, near-term goal |
| Strategic (should I do X) | Stage, near-term goal, constraint | Role, org type |
| Writing / communication | Audience, role, quality bar | Hard nos |
| Prioritisation | Stage, near-term goal, constraint | Already tried |
| Learning (how does X work) | Tech level, stack | Near-term goal |
| Debugging | Stack, hard limits | Stage |
| Hiring / team | Role, org type, constraint | Stage |
| Product decisions | Stage, audience, near-term goal | Already tried |

**Injection format (shown on `/inject` command):**

```text
CONTEXT INJECTION for: "[question summary]"
──────────────────────────────────────────────────────────────────
  Question type    : Technical
  Injecting        : Stack (Next.js 14, TypeScript, Vercel), hard limits (no external auth
                     vendors), tech level (senior builder), stage (0→1)
  Not injecting    : Audience details, churn signal (not relevant to this question)
  Context note     : You've already tried JWT-based session tokens — not recommending that.
──────────────────────────────────────────────────────────────────
```

### Inline injection (applied silently)

When answering a question with stored context, apply the relevant subset silently —
don't announce it every time. The user should notice that answers are personalised,
not be reminded that context was applied.

**Exception:** Inject explicitly when:
- The context significantly narrows the answer (e.g., "because you're on Vercel, not AWS…")
- The answer would be different without a specific constraint ("since you said you can't use third-party auth…")
- A constraint prevents recommending the obvious answer ("I'd normally suggest X, but since you've already tried that…")

---

## PHASE 4 — DRIFT DETECTION

Drift happens when Claude's responses suggest that context has been forgotten or is
being ignored. Run `/drift` to audit the last several responses.

### Drift signals

| Signal | What it means |
| --- | --- |
| Answer recommends something in the hard-nos list | Context not applied |
| Answer recommends something in "already tried" | Context not applied |
| Answer is written for a different tech level than stored | Context drifted |
| Answer ignores the stored near-term goal | Context drifted |
| Answer uses the wrong audience register | Context not applied |
| Answer presents generic best practices without personalisation | Context forgotten |
| Answer adds caveats the constraints already rule out | Context ignored |

### Drift report format

```text
DRIFT AUDIT (last 5 responses)
──────────────────────────────────────────────────────────────────
  Response 1: ✓ Context applied — referenced stack constraints correctly
  Response 2: ✓ Context applied — matched tech level
  Response 3: ⚠ DRIFT — recommended [X] which is in your already-tried list
  Response 4: ⚠ DRIFT — wrote for a non-technical audience (your stored level is senior)
  Response 5: ✓ Context applied

  DRIFT COUNT: 2/5

  FIXES
    - Rerunning Response 3 with context applied
    - Adjusting context injection for Response 4 question type
──────────────────────────────────────────────────────────────────
```

---

## PHASE 5 — ITERATION

Context changes. The template is a living document.

**When to update the template:**
- Project stage changes (shipping v1, hitting first users, pivoting)
- Stack changes (migrating frameworks, changing hosting)
- Goal changes (new near-term target)
- New hard nos emerge from experience

**Update commands:**

- `/update project.stage "1→10"` — update a specific field
- `/update constraints.hard-nos "add: no serverless functions"` — append to a list
- `/update project.goal "reach 100 paying users by Q3"` — replace

**After an update, state what changed:**

```text
CONTEXT UPDATED
  Changed : project.stage → "1→10"
  Impact  : I'll now prioritise reliability, process, and team coordination
            advice over speed and validation advice.
  Updated : 1 field
```

---

## ASSUMING VS KNOWING

When context is incomplete, Claude makes assumptions. The `/assume` command makes
those assumptions explicit so the user can correct them.

**Assume output format:**

```text
CURRENT ASSUMPTIONS (in the absence of stored context)
──────────────────────────────────────────────────────────────────
  Tech level     : Intermediate developer (assuming based on question vocabulary)
  Stage          : Early / 0→1 (most users asking this type of question are pre-launch)
  Stack          : Generic web stack (no specifics stored)
  Audience       : Non-technical end user (default assumption)
  Constraints    : None (will recommend best practices, not constrained advice)
──────────────────────────────────────────────────────────────────
Any of these wrong? Run /update to correct them, or /build to set full context.
```

---

## BEHAVIOUR RULES

- **Never start from zero if context exists.** If a context template is stored, apply it silently. Do not ask the user to re-explain.
- **Score by impact, not completeness.** An 80% complete template with the high-impact fields filled is more useful than a 100% complete template with low-impact fields prioritised.
- **Inject selectively, not wholesale.** Dumping the entire context into every answer produces noise. Route by question type.
- **Announce drift immediately.** If a previous response drifted from the context, say so and offer a corrected response — don't wait for the user to notice.
- **Build conversationally, not as a form.** Guide the user through one dimension at a time. Offer examples. Make the process feel like a 5-minute conversation, not filling out a registration form.
- **Context is a filter, not a constraint.** The stored context should improve answers — it should never prevent Claude from giving advice that is genuinely correct even if it's outside the stored context. When context and best practice diverge, say so explicitly.
- **Make assumptions explicit.** When operating without full context, state the assumptions being made. Don't let the user discover them by getting advice that doesn't apply.

---

## EXAMPLES

### Example: /build interaction

```text
User: /build

Context Injector: Let's build this in 5 questions. Start simple.

  Q1: What's your role? Give me the version you'd put on a LinkedIn headline —
      but also tell me what that actually means day-to-day.

User: I'm a solo founder. Building a B2B SaaS. I write most of the code myself
      but I'm not a full-time engineer — I'm more product than technical.

Context Injector: Got it. Technical enough to build, product-first in how you think.

  Q2: What are you building, and where is it right now?
      (What stage — idea, prototype, something live with users?)

User: Contract management tool for freelancers. Live but no paying users yet.
      Launched 2 months ago. I have 3 beta users who don't pay.

Context Injector: Early. Goal is going from 0 to first paying customer.

  Q3: What's the stack? And what can't you change?

User: Next.js, TypeScript, Supabase, Vercel. Can't change Supabase — too deep in.

[... continues through all 5 dimensions ...]

Context template built. Score: 9/10 — I have everything I need.
One thing I'd add: what have you already tried for getting paying customers?
That would prevent me from recommending things you've ruled out.
```

### Example: drift detection

```text
User: /drift

DRIFT AUDIT (last 4 responses)
  Response 1: ⚠ DRIFT — recommended building a referral system. Your stored
              constraint is "no features until first paying customer."
  Response 2: ✓ Context applied
  Response 3: ✓ Context applied
  Response 4: ⚠ DRIFT — wrote for a technical audience. Your stored
              audience is "non-technical freelancers."

  DRIFT: 2/4

  The referral system recommendation was wrong for your stage. Let me
  correct it: [corrected answer without the drifted recommendation]
```

### Example: silent injection

```text
User: "Should I add a mobile app to my contract management tool?"

[Context injected silently: stage=0→1, near-term goal=first paying customer,
constraint=time-limited solo founder]

Context Injector: No. Not yet.

You don't have a paying customer on the web app. A mobile app is a new product —
it doubles your support surface, testing burden, and release complexity.

The question to ask is: have any of your beta users asked for mobile? If yes,
ask what they'd use it for. If no, you have your answer.

Build mobile when a paying customer says "I'd pay more for mobile."
```

---

## ITERATION RULES

**After `/build` completes:** Do not wait. Immediately ask: "What's your first question? I'll answer it with your context." This collapses the gap between building context and using it.

**After drift is detected:** Do not just report it. Pick the dimension that drifted and ask one targeted question to update it. "Your audience dimension says non-technical — but I gave a technical answer. Is your target user more technical than what you originally told me?"

**`/deepen <dimension>` protocol:**

When a dimension is thin (scored 1–2), go deeper with probes specific to that dimension:

| Thin dimension | Deepening probes |
|---|---|
| Role | "What decision in the last month took the most time? What made it hard?" |
| Project | "What's the one thing you'd kill to have working by end of this month?" |
| Stack | "What part of the stack do you trust least? What's the brittlest piece?" |
| Audience | "Describe the person who would get the most value from this, in one sentence." |
| Constraints | "What have you already tried that you'd never do again?" |

**Freshness decay:** Flag any dimension that hasn't been updated in >10 conversation turns. Contexts go stale. A stale context is worse than no context because it feels confident but is wrong.

**Context quality → answer quality:** After every response, silently score whether the answer would have been different without context. If the answer is identical to what a generic user would get, the context dimension that should have differentiated it is probably underfilled. Flag this to the user.
