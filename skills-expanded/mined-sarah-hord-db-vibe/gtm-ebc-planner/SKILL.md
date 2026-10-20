---
name: gtm-ebc-planner
description: Create Executive Briefing Center (EBC) planning documents. Gathers account data from Salesforce, Logfood, Glean, and web research to generate professional EBC plans with quadrant selection, speaker matching, and agenda generation. Outputs to Google Docs. Uses a role-based speaker database that resolves actual people at runtime via databricks-org. Distinct from account-review-deck which produces a standalone QBR/EBC slide deck — this skill generates a full multi-phase planning document (Google Doc) with optional presentation generation via /fe-html-slides:html-slides.
user-invocable: true
---

# EBC planning document generator

Create professional Executive Briefing Center (EBC) planning documents by gathering data from multiple sources, selecting the appropriate EBC quadrant, matching Databricks speakers to agenda topics, and generating a formatted Google Doc.

**Announce at start:** "I'm using the EBC planner skill to create your Executive Briefing Center planning document."

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Salesforce** - Run `/salesforce-authentication`
2. **Databricks** - Run `/databricks-authentication`
3. **Google** - Run `/google-auth`

**Dependencies:** This skill requires the `fe-google-tools` plugin (for `/google-docs` and `/google-calendar` skills), the `fe-salesforce-tools` plugin (for `/salesforce-authentication`), and optionally the `fe-html-slides` plugin (for `/fe-html-slides:html-slides` presentation generation).

**CRITICAL: Reading Google Docs**
When you need to read any Google Doc URL (docs.google.com), you MUST use the `/google-docs` skill. **NEVER use fetch or WebFetch for Google Docs** - they will fail.

## Best practices

Read `resources/EBC_BEST_PRACTICES.md` at the start of every EBC planning session and again during Phase 6 refinement. Apply its principles throughout — particularly:
- **Dual objectives** — Every EBC must serve both customer and sales objectives. Surface both during discovery.
- **Customer-first flow** — Open the agenda with the customer's voice, not a corporate pitch.
- **80/20 rule** — Target 80% discussion, 20% presentation. Include engagement hooks in every session.
- **Narrative arc** — Structure the day as Opening → Rising Action → Climax → Resolution.
- **Customization tiers** — Match planning depth to lead time (Tier 1: 4-6 weeks, Tier 2: 2-4 weeks, Tier 3: < 2 weeks).
- **Discussion leaders, not presenters** — Speakers facilitate dialogue. Prep sessions are non-negotiable.
- **Follow-up cadence** — Same-day thank-you, week 1 action items, 30/90-day tracking.
- **Avoid product dump syndrome** — Pick 2-3 pillars that map to customer objectives, not the entire catalog.

## Workflow

### Phase 1: Discover (conversational)

Ask the user for the following information. Use `AskUserQuestion` for structured choices and conversation for free-text inputs. Gather all required inputs before proceeding.

**Required inputs:**

| Input | Description | Example |
|-------|-------------|---------|
| Account name | Customer account name | "Acme Corp" |
| EBC date(s) | Proposed date and duration | "March 20, 2026 - Half Day" |
| Location | Where the EBC will be held | "Melbourne, Customer Site" |
| Customer attendees | Names, titles, and any background info | "Jane Smith, VP Data & Analytics" |
| Purpose | Primary goal of the EBC (1-2 sentences) | "Re-establish strategic partnership with new leadership" |
| Objectives | 3-5 desired outcomes | "Build exec relationship, Address BRAG status..." |
| Areas of interest | Topics the customer cares about | "Compound AI, Data Governance, Real-time Analytics" |
| AI/Data maturity | Estimated maturity stage if known (or leave for auto-assessment) | "Stage 3 — Defined, early ML in production" |
| Customer asks | Top 3 things the customer wants from us | "Investment commitment, Use case acceleration" |

**Optional inputs:**

| Input | Description | Default |
|-------|-------------|---------|
| Databricks attendees | Pre-selected speakers | Auto-matched from speaker database |
| EBC type override | Skip quadrant auto-detection | Auto-detected from account data |
| Additional context | Google Docs, Slack threads, etc. | Gathered from Glean |

### Phase 2: Research (3 parallel agent teams)

Once Phase 1 discovery is complete, launch three parallel research subagents simultaneously. Each team gathers a distinct category of intelligence. All three teams run in parallel to minimize total research time.

#### Team A: Account Intelligence (subagent)

This team gathers structured account data from Salesforce and Logfood.

##### Salesforce account data

**First, resolve the Salesforce target org** (required for all `sf` CLI commands):

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  SF_TARGET_ORG=$(sf org list --json 2>/dev/null | jq -r '.result.nonScratchOrgs[0].username // empty')
fi
echo "Using SF org: $SF_TARGET_ORG"
```

If `SF_TARGET_ORG` is empty, ask the user to run `/salesforce-authentication` first.

**IMPORTANT — JSON output handling:** Do NOT pipe `sf` output through `python3 -c "import json..."`. The `--json` flag already produces structured JSON. Read the JSON output directly — if the command fails, the output will not be valid JSON and a Python pipe will crash. Use `jq` for any post-processing if needed.

```bash
# Step 1: Get Account ID and details
sf data query --target-org "$SF_TARGET_ORG" --query "SELECT Id, Name, BRAG_Status__c, Industry, BillingCity, BillingState, Website FROM Account WHERE Name LIKE '%ACCOUNT_NAME%' LIMIT 5" --json
```

**Account ID resolution:** If the query returns multiple accounts (common with parent/child accounts or regional entities), present the results to the user and ask them to confirm which Account ID to use. If the query returns zero results, ask the user for the Salesforce Account ID directly (they can find it in the Salesforce URL).

Once you have a confirmed `ACCOUNT_ID`, run the remaining queries **in parallel**:

```bash
# Get Databricks Account Team (SA, AE, CSM, etc.)
sf data query --target-org "$SF_TARGET_ORG" --query "SELECT User.Name, User.Email, TeamMemberRole FROM AccountTeamMember WHERE AccountId = 'ACCOUNT_ID'" --json

# Get Customer Contacts (key stakeholders)
sf data query --target-org "$SF_TARGET_ORG" --query "SELECT Id, Name, Title, Email, Department FROM Contact WHERE AccountId = 'ACCOUNT_ID' AND Title != null ORDER BY Title LIMIT 30" --json

# Get Use Cases
sf data query --target-org "$SF_TARGET_ORG" --query "SELECT Id, Name, Stages__c, Implementation_Status__c FROM UseCase__c WHERE Account__c = 'ACCOUNT_ID' ORDER BY Stages__c DESC" --json

# Get Opportunities
sf data query --target-org "$SF_TARGET_ORG" --query "SELECT Id, Name, Amount, StageName, CloseDate FROM Opportunity WHERE AccountId = 'ACCOUNT_ID' AND IsClosed = false ORDER BY Amount DESC LIMIT 10" --json
```

From this data, compute:
- **Databricks account team** - Identify the assigned AE, SA, CSM, and any specialists. These people are **automatic includes** in the EBC attendee list.
- **Customer stakeholder map** - From contacts, identify executives (VP+), technical leaders, and key practitioners. Cross-reference with the customer attendees provided by the user.
- **Production use cases (U6)** count
- **Pipeline use cases (U1-U5)** count
- **Account tier** and BRAG status
- **Key opportunities** and renewal info

##### Consumption data from Logfood

Use the `logfood-querier` skill or `databricks-query` with the `logfood` profile:

```sql
-- Monthly consumption and MRR
SELECT
    usage_date,
    sku,
    SUM(dbu_dollars) as dbu_dollars,
    SUM(dbus) as dbus
FROM main.gtm_data.c360_consumption_monthly
WHERE account_id = 'SALESFORCE_ACCOUNT_ID'
AND usage_date >= DATE_ADD(CURRENT_DATE(), -6)
GROUP BY usage_date, sku
ORDER BY usage_date DESC, dbu_dollars DESC

-- Active workspaces
SELECT COUNT(DISTINCT workspace_id) as workspace_count
FROM main.gtm_data.c360_consumption_monthly
WHERE account_id = 'SALESFORCE_ACCOUNT_ID'
AND usage_date >= DATE_ADD(CURRENT_DATE(), -3)
```

From this data, compute:
- **Current MRR** (most recent month total)
- **Top SKUs** by percentage of spend
- **Active workspace count**
- **Growth trajectory**

##### Team A output spec

Account metrics, team members, contacts, use cases, opportunities, MRR, SKUs, workspaces, growth trajectory.

#### Team B: Market Intelligence (subagent)

This team gathers internal and external intelligence about the customer's market position, competitive landscape, and strategic context.

##### Internal context from Glean

Search Glean for relevant internal documents:

```
# Account strategy and plans
Search: "ACCOUNT_NAME account plan strategy"

# Past EBCs or exec meetings
Search: "ACCOUNT_NAME EBC executive briefing"

# Technical architecture
Search: "ACCOUNT_NAME architecture technical"

# Recent activity and issues
Search: "ACCOUNT_NAME escalation issue blocker"
```

**IMPORTANT:** When Glean returns Google Doc URLs, use the `/google-docs` skill to read them.

Extract:
- Account plan highlights
- Previous EBC materials (if any)
- Known technical challenges
- Competitive landscape
- Key internal documents to reference

##### Internal intelligence (Glean)

Search Glean for recent customer activity, competitive intelligence, and strategic context beyond what's in the account plan:

```
# Recent engagements and activity
Search: "ACCOUNT_NAME recent engagement meeting briefing"

# Competitive and technology landscape
Search: "ACCOUNT_NAME Microsoft Snowflake competitor technology"

# Regulatory, compliance, or risk issues
Search: "ACCOUNT_NAME compliance regulatory risk"

# Migration and infrastructure projects
Search: "ACCOUNT_NAME migration infrastructure modernization"

# AI and data strategy
Search: "ACCOUNT_NAME AI data strategy initiative"

# Missed engagements or escalations
Search: "ACCOUNT_NAME cancelled escalation issue"
```

Extract:
- Recent executive engagements (especially missed or cancelled ones - these signal follow-up opportunities)
- Active technology evaluations or migrations (competitive threats and opportunities)
- Compliance or regulatory pressure points (these often become the highest-urgency use cases)
- Known governance gaps or pain points
- Internal intelligence on competitor activity

##### External intelligence (web search)

Use `WebSearch` to gather public information about the customer:

```
# Recent news and strategy
Search: "COMPANY_NAME news strategy CURRENT_YEAR"

# Regulatory and legal actions
Search: "COMPANY_NAME ACCC regulatory lawsuit penalty CURRENT_YEAR"
Search: "COMPANY_NAME compliance regulatory action"

# Technology and AI investments
Search: "COMPANY_NAME AI technology investment partnership"
Search: "COMPANY_NAME digital transformation cloud"

# Executive profiles
Search: "EXEC_NAME COMPANY_NAME title role background"

# Financial performance
Search: "COMPANY_NAME annual results revenue growth"

# Industry trends
Search: "INDUSTRY data AI trends CURRENT_YEAR"
```

Focus on:
- **Regulatory and legal actions** - lawsuits, fines, regulatory investigations (these create urgent compliance use cases)
- **Technology partnerships** - cloud deals, AI platform investments, vendor selections (competitive context)
- **AI maturity signals** - number of models in production, AI headcount, publicised AI initiatives
- **M&A activity** - acquisitions, mergers, divestitures that may affect data strategy
- **Financial performance** - revenue, growth metrics, digital/e-commerce trends
- **Executive backgrounds** - career history, areas of expertise, and "hot buttons"
- **Industry-specific trends** - sector data and AI adoption patterns

##### Synthesise findings

After gathering internal and external intelligence, synthesize findings into EBC-relevant insights:

1. **Identify the #1 most urgent issue** - Regulatory actions, competitive threats, or business pressures that should anchor the EBC narrative
2. **Map findings to use cases** - Connect news items to specific Databricks capabilities and demo opportunities
3. **Flag relationship context** - Note any missed engagements, cancelled briefings, or escalations that this EBC should address
4. **Update competitive positioning** - Adjust messaging based on discovered technology partnerships or vendor selections
5. **Identify conversation landmines** - Topics to avoid or handle carefully (e.g. active litigation, sensitive personnel changes)

Write findings to the document as a "Recent developments and market context" section (see template).

##### Team B output spec

Regulatory context, competitive landscape, financial performance, technology investments, industry trends, relationship context.

#### Team C: People Intelligence (subagent)

This team researches individual attendees and identifies sensitive topics that could affect the EBC.

##### Deep attendee research

For EACH confirmed customer attendee, conduct systematic web research using parallel subagents (one subagent per 2-3 attendees). This is critical for producing personalized, high-quality attendee profiles.

**Search pattern for each attendee:**
```
WebSearch: "[NAME] [COMPANY] LinkedIn profile"
WebSearch: "[NAME] [COMPANY] conference talk OR keynote OR presentation"
WebSearch: "[NAME] [COMPANY] interview OR podcast OR article"
WebSearch: "[NAME] LinkedIn career history"
WebSearch: "[NAME] data OR AI OR technology" (if relevant to their role)
```

**Extract and document for each person:**
- **Education:** Degrees, universities, certifications
- **Career history:** Chronological progression with specific companies, roles, and approximate dates
- **Recent activity:** Conference talks, interviews, podcasts, blog posts, LinkedIn articles — with URLs
- **Industry involvement:** Board memberships, advisory roles, associations, awards
- **Key quotes:** Published opinions on AI, data, technology, or their industry
- **Known initiatives:** Projects they've led or championed (from press releases, case studies)

**Critical checks during research:**
- **Verify employment status.** If a person's LinkedIn shows a different company or "Open to Work", flag them as potentially departed. Search for "[NAME] leaves [COMPANY]" or "[COMPANY] [TITLE] departure".
- **Check for recent leadership changes.** Search "[COMPANY] CTO departure" or "[COMPANY] leadership change [YEAR]" to identify org changes that may affect the attendee list.
- **Flag unconfirmed attendees** in the output with a clear note for the account team.

**Output format:** Structure the research into the enriched attendee profile format used in the EBC template (Background, Recent online activity with links, EBC focus).

##### Sensitive topics identification

Research potential sensitive topics that could derail or damage the EBC:

**Web research:**
```
WebSearch: "[COMPANY] regulatory action OR lawsuit OR investigation [YEAR]"
WebSearch: "[COMPANY] leadership departure OR restructure [YEAR]"
WebSearch: "[COMPANY] controversy OR scandal OR criticism [YEAR]"
WebSearch: "[COMPANY] layoffs OR cost cutting [YEAR]"
```

**Internal research (Glean/Salesforce):**
```
Glean: "[COMPANY] escalation OR sensitive OR risk OR blocker"
Salesforce: Check for open support escalations or blockers
```

**Categorize findings into the Sensitive Topics table:**
- Topic name
- Context: specific details about why it's sensitive
- Handling approach: avoid, address carefully with specific language, redirect to positive framing

**Common sensitive topic categories:**
- Regulatory/legal exposure (lawsuits, fines, audits)
- Leadership instability (departures, restructuring)
- Competitive positioning (don't disparage specific competitors the customer uses)
- Financial pressure (layoffs, cost cuts, contract scrutiny)
- Prior Databricks issues (support escalations, failed POCs, missed commitments)

##### Team C output spec

Enriched attendee profiles (Background, Recent activity with links, EBC focus), sensitive topics table, departure flags.

#### Research synthesis checkpoint

When all three teams complete, present a research summary to the user before proceeding. This is the last point where the user can add context or correct findings before strategic decisions are made.

### Phase 3: Synthesize (intelligence → strategy)

This phase takes the outputs from all three research teams and makes the strategic decisions that shape the entire EBC.

#### 1. AI maturity assessment

Read `resources/AI_MATURITY_STAGING.md` and assess the customer's maturity stage based on data gathered across all three research teams:

- **U6 use case count** and diversity
- **MRR** and growth trajectory
- **SKU diversity** (how many platform capabilities in use)
- **GenAI signals** (any AI/ML use cases, POCs, or production deployments)
- **Workspace count** and activity

Present the assessment to the user:

```
AI/Data Maturity Assessment: Stage 3 — Defined
Key signals: 12 U6 use cases, $65K MRR, 3 SKUs in use, early ML but no GenAI
EBC implication: Balance consolidation with forward-looking AI. GenAI readiness
will be the "wow" moment. Avoid overwhelming with advanced agent capabilities.
```

Allow the user to adjust if they have additional context. This assessment directly shapes content depth in Phase 4 (agenda design).

#### 2. Quadrant selection

Read the quadrant guidance from `resources/QUADRANT_GUIDANCE.md` and determine the appropriate EBC quadrant based on:

1. **Databricks penetration** - MRR, use case count, workspace count
2. **Executive advocacy** - BRAG status, relationship health, engagement level

Present the recommended quadrant to the user with rationale:

```
Based on account data:
- Penetration: HIGH (28 U6 use cases, $127K MRR, 81 workspaces)
- Advocacy: LOW (BRAG Red, Amber exec relationship)

Recommended: Q3 - Value Recovery
Rationale: High platform adoption but at-risk executive relationships. Focus on
demonstrating existing value and re-establishing strategic partnership.
```

Allow the user to override if they disagree.

#### 3. Narrative thesis

Distill all research into a single narrative thesis — the one sentence that captures why this EBC matters right now and what the day should achieve. This thesis anchors every subsequent design decision.

Example: "Coles has lost its CTO and is under ACCC scrutiny — this EBC must rebuild executive trust with the new leadership while demonstrating governance maturity that addresses their regulatory exposure."

#### 4. Executive summary draft

Produce the executive summary content using the narrative thesis as the organizing principle:
- **Account snapshot** (one paragraph with key metrics)
- **"Why this EBC matters"** (the strategic moment and what's at stake)
- **Warning notes** (2-4 bullet points: attendee risks, competitive sensitivities, regulatory exposure)
- **EBC type with rationale**
- **"Three things to get right"** — the three highest-impact actions, each tied to a specific person or competitive dynamic
- **Key metrics line**

#### 5. User alignment checkpoint

Present the synthesis to the user: maturity assessment, quadrant recommendation, narrative thesis, and executive summary draft. Get explicit approval before proceeding to design. This prevents wasted work on an agenda built from wrong assumptions.

### Phase 4: Design (speakers + agenda + engagement)

With the strategy locked, design the EBC experience. This phase combines speaker selection, agenda construction, engagement planning, and demo design into a single coherent design pass.

#### 1. Speaker matching

##### Auto-include account team members

From the `AccountTeamMember` data gathered in Phase 2 Team A, automatically include the following roles as Databricks attendees:
- **Account Executive (AE)** - Welcome, relationship, commercial discussion
- **Solutions Architect (SA)** - Technical sessions, demos, deep dives
- **Customer Success Manager (CSM)** - Value delivered, adoption, next steps

Cross-reference these names with the speaker database (`resources/SPEAKER_DATABASE.json`). If an account team member exists in the speaker database, use their topic expertise for session assignment. If they don't exist in the database, include them with their role-appropriate sessions.

##### Match additional speakers to topics

Read the speaker database and match additional speakers to agenda topics based on:

1. **Topic expertise** - Speaker's areas of knowledge
2. **Quadrant fit** - Speakers appropriate for the EBC type
3. **Industry relevance** - Speakers with industry-specific experience
4. **Seniority matching** - Match speaker seniority to customer attendees (use `seniority_matching` from the database)

**Important:** Do not double-assign the account SA to sessions already covered by a specialist speaker, and vice versa. The account SA typically handles technical deep dives and demos for topics they own, while specialist speakers are brought in for niche expertise the account SA doesn't cover.

Present proposed speaker assignments and allow the user to modify:

```
Proposed Databricks attendees:

Account team (auto-included):
| Speaker | Role | Sessions |
|---------|------|----------|
| [AE Name] (AE) | Account Owner | Welcome, commercial wrap |
| [SA Name] (Sr. SA) | Account SA | Technical deep dive, demo |

Additional speakers (from speaker database):
| Speaker | Topic | Rationale |
|---------|-------|-----------|
| [Exec Name] (MD/Dir) | Welcome & Partnership Vision | Exec-to-exec with customer VP |
| [Specialist Name] (Dir) | Industry Value Narrative | Industry-specific expertise |
```

##### Persona alignment and objection preparation

Read `resources/PERSONA_GUIDE.md` and map each confirmed customer attendee to a persona type. Ensure each primary persona has at least one tailored moment designed for them in the agenda.

Read `resources/OBJECTIONS_GUIDE.md` and identify the 2-3 most likely objections for each discussion leader's session. Include these in the speaker prep materials so they are prepared to handle them constructively.

#### 2. Global speaker discovery

After matching local speakers, identify relevant global and international speakers who could add strategic value to the EBC. This is especially important for Q3 (Value Recovery) and Q4 (Strategic Co-Innovation) EBCs where senior executive or industry-specialist presence signals investment commitment.

##### Identify candidate global speakers

Read the speaker database (`resources/SPEAKER_DATABASE.json`) and filter for speakers where `region` is `"apj"` or `"global"`. Match candidates based on:

1. **Topic relevance** - Do the speaker's topics align with the EBC areas of interest?
2. **Industry match** - Does the speaker have expertise in the customer's industry?
3. **Quadrant fit** - Is the speaker appropriate for the selected EBC quadrant?
4. **Seniority signal** - Would their seniority level send the right message to the customer?

If the speaker database doesn't have a strong match, search Glean for additional candidates:

```
# Global industry leaders
Search: "Databricks global VP INDUSTRY_NAME"

# AI/Product leadership
Search: "Databricks VP AI product leader"

# Regional executives
Search: "Databricks APJ executive SVP"
```

##### Check calendar availability

For each candidate global speaker, use the `/google-calendar` skill to check availability around the EBC dates. **Note:** Calendar visibility depends on the user's Google Workspace permissions — some speakers' calendars may not be accessible. If a calendar check fails or returns no data, flag it to the user and suggest they reach out to the speaker directly to confirm availability.

1. **Check the speaker's calendar** for the EBC date and surrounding days (travel buffer)
2. **Look for existing ANZ travel** - If the speaker is already travelling to the region around the EBC dates, they're a strong candidate
3. **Check for conflicts** - All-day events, other EBCs, or travel to other regions

```
For each global speaker candidate:
- Check calendar for EBC_DATE +/- 3 days
- Flag: "Available", "In region (existing travel)", "Conflict", or "Requires travel"
```

##### Present recommendations

Present global speaker recommendations to the user with availability status:

```
Suggested global speakers:

| Speaker | Title | Relevance | Availability |
|---------|-------|-----------|-------------|
| [Global Industry VP] | Global industry insights | In region around EBC dates |
| [APJ Regional Exec] | Exec partnership signal | Available - no conflicts |
| [Global Product VP] | Product roadmap | Requires travel from US |

Recommendation: [Global Industry VP] is in the region and brings global
credibility. [APJ Exec] can join for welcome/close. [Global Product VP]
would require significant coordination but would be high-impact for a
topic-focused EBC.
```

Allow the user to select which global speakers to include. Add selected speakers to the Databricks attendees list.

**Tips for global speaker coordination:**
- Global speakers based in the US need 2-3 weeks minimum lead time for ANZ travel
- APJ-based speakers travel the region frequently - check for existing trips
- For Q4 co-innovation EBCs, having a global industry or product leader is a strong differentiator
- If a global exec can't attend in person, consider a video dial-in for a specific agenda slot

#### 3. Agenda generation

Generate a proposed agenda following the **narrative arc structure** from `resources/EBC_BEST_PRACTICES.md`:

Read `resources/AGENDA_TEMPLATES.md` for time-blocked starting templates (half-day and full-day). Adapt the template based on the customer's quadrant, maturity stage, and persona mix — never use the template verbatim.

1. **Opening** (20-30 min) — Executive welcome, introductions, then a **customer voice session** where the customer shares their strategic priorities while Databricks listens. This is NOT a Databricks pitch.
2. **Rising Action** — Strategic vision, platform overview, industry trends and peer insights. Match content to the selected quadrant framework.
3. **Climax** — Deep-dive demos, co-creation workshops, whiteboard architecture sessions. This is where the platform becomes tangible.
4. **Resolution** — Mutual action planning, executive commitments, defined next steps.

**Agenda rules:**
- Never go more than 60 minutes without a break or format change
- Alternate strategic and technical sessions to maintain energy across mixed audiences
- Build in 10-15% buffer time for organic discussion
- Half day = ~4 hours, full day = ~7 hours
- Every session must include a **customer engagement hook** — a pre-planned open-ended question to spark dialogue (80% discussion, 20% presentation)
- For each session, note the **discussion leader** (not "presenter"), their engagement hook, and what success looks like
- End with concrete, owned action items — not vague next steps

#### 4. Personalized engagement hooks

For each agenda session's engagement hooks, reference SPECIFIC findings from the attendee research:

**Good engagement hook:** "Caroline, at the SAP NOW AI Tour you talked about evolving mycoles Assistant into an agentic platform — let me show you how Databricks' agent framework provides the orchestration layer for exactly that kind of evolution."

**Bad engagement hook:** "Caroline, what are your thoughts on AI adoption?"

**Rules for engagement hooks:**
1. Every hook must reference a specific fact from the attendee research (a talk, article, quote, initiative, or career detail)
2. Use the person's first name in the hook text
3. Connect the reference to what Databricks will demonstrate in that session
4. Each customer attendee should have at least 2 personalized hooks across the agenda
5. Hooks should feel like genuine interest, not surveillance — reference public information naturally

Present the draft agenda for user review and refinement.

#### 5. Demo plan

Plan demos alongside the agenda with:
- **Industry context** — use customer-relevant data and scenarios
- **Engagement hooks** — tie each demo to a specific attendee's known interest or initiative
- **Backup options** — plan a backup demo for every live demonstration in case of technical issues
- **Before/after framing** — show the customer's current state vs. what's possible with Databricks

#### 6. Design checkpoint

Before proceeding to artifact generation, verify all quality criteria are met. Read the quality gate checklist from `resources/EBC_TEMPLATE.md` (Quality gate section) and confirm each item. Flag any gaps to the user before proceeding.

**Critical checks:**
- Every agenda item maps to at least one customer objective
- Each primary persona has a tailored moment
- AI maturity stage is reflected in content depth
- Backup demos are planned for every live demonstration
- Discussion leaders have engagement hooks and objection preparation

**Enrichment quality checks:**
- [ ] Each customer attendee profile includes: education, career history with specific companies, at least one recent activity with a link
- [ ] Executive summary is present with all subsections (snapshot, why it matters, warnings, three things to get right)
- [ ] Engagement hooks in each agenda session reference specific attendee research (not generic questions)
- [ ] Sensitive topics section has at least 2 identified topics with handling approaches
- [ ] Attendee departure risks are flagged with "requires confirmation" notes
- [ ] Discussion leader prep references specific attendee tidbits (not just role-based assumptions)

### Phase 5: Generate (produce artifacts)

#### 1. Write markdown

Write the EBC planning document to `./ebc_plan_<account_slug>.md` **in the current project folder** using the template from `resources/ebc_template.md`.

Populate all sections with gathered data:
- Header with EBC metadata
- **Executive summary** — from Phase 3 synthesis. Includes:
  - Account snapshot (one paragraph with key metrics)
  - "Why this EBC matters" (the strategic moment and what's at stake)
  - Warning notes (2-4 bullet points: attendee risks, competitive sensitivities, regulatory exposure)
  - EBC type with rationale
  - "Three things to get right" — the three highest-impact actions, each tied to a specific person or competitive dynamic
  - Key metrics line
- **Customer attendees** — enriched profiles from Phase 2 Team C research. Each attendee gets:
  - Full career narrative (not a table row — a paragraph with degrees, companies, roles)
  - Recent online activity with clickable links (talks, articles, interviews)
  - Tailored EBC focus referencing their known interests and background
  - An "Attendees requiring confirmation" table for anyone whose status is uncertain
- Account context metrics table
- AI/Data maturity assessment with stage rationale
- Recent developments and market context (from Phase 2 Team B research)
- Purpose and objectives
- Dual objectives (customer objectives AND account team objectives)
- Areas of interest with relevance and ownership
- Customer asks with response strategies
- Proposed agenda with timing, speakers, and format
- Demo plan with industry context and backup options
- Competitive context and positioning notes
- Databricks attendee table with roles
- Discussion leader prep checklist (per speaker: engagement hooks, success criteria, backup)
- **Sensitive topics** — from Phase 2 Team C research. Table with Topic, Context, and Handling columns.
- Post-EBC follow-up cadence (same-day through 90-day milestones)
- Quality gate checklist (all items checked)
- Success metrics checklist
- Key internal documents with links
- Pre-EBC preparation checklists

#### 2. Convert to Google Doc

**For a new document** (first run):

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input ./ebc_plan_<account_slug>.md \
  --title "[Account Name] EBC Planning Document"
```

**For regenerating an existing document** (clear first, then rewrite):

```bash
# Step 1: Clear existing content to avoid duplicates
uv run python3 ~/.claude/plugins/cache/fe-vibe/gtm-ebc-planner/*/skills/gtm-ebc-planner/resources/fix_ebc_doc.py \
  --doc-id <DOC_ID> \
  --clear

# Step 2: Write fresh content
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input ./ebc_plan_<account_slug>.md \
  --doc-id <DOC_ID>
```

**IMPORTANT:** The markdown-to-gdocs converter appends to existing documents. When regenerating a document, always run `fix_ebc_doc.py --clear` first to avoid duplicate content.

**Note:** This step requires the `fe-google-tools` plugin to be installed (provides `markdown_to_gdocs.py`).

#### 3. Post-process

Run the post-processing script to add person chips and status colors:

```bash
uv run python3 ~/.claude/plugins/cache/fe-vibe/gtm-ebc-planner/*/skills/gtm-ebc-planner/resources/fix_ebc_doc.py \
  --doc-id <DOC_ID> \
  --mentions '{"@Person Name": "person.name@databricks.com"}'
```

Build the mentions map from:
- Databricks attendees (look up emails via Glean people search)
- Customer attendees (use names only, no chips needed)

#### 4. Presentation deck

After the Google Doc is complete, **always offer to generate the EBC presentation deck**. This is the **actual presentation shown to the customer during the EBC** — not a summary of the planning document. Most users will want this.

```
The EBC planning document is ready. Next, I'll generate the presentation
deck that will be shown to the customer during the briefing. This creates
a self-contained HTML slide deck with joint branding.

Shall I proceed? (If you'd prefer to skip the deck, let me know.)
```

Invoke `/fe-html-slides:html-slides` with a presentation brief (requires the `fe-html-slides` plugin — if unavailable, skip this phase and note the dependency to the user). Instruct it to use the **customer's branding as primary** with **Databricks as an accent**. The presentation should look and feel like the customer's brand — their colours, typography, and visual identity should dominate, with Databricks red/coral used sparingly as a secondary accent. Research the customer's brand identity (logo, colours, fonts) from their website or brandfetch.com. The customer logo should appear first (before the Databricks logo) in any logo bar to signal "this is their briefing".

**Logo sourcing (critical):** Always use the customer's **real logo**, never a fabricated text placeholder. Source it in this priority order: (1) Wikimedia Commons SVG — use the API `https://commons.wikimedia.org/w/api.php?action=query&titles=File:COMPANY_logo.svg&prop=imageinfo&iiprop=url&format=json` to get the direct SVG URL, then fetch and inline it, (2) fetch from the customer's website header/nav, (3) brandfetch.com, (4) Clearbit Logo API (`https://logo.clearbit.com/DOMAIN`) as last resort. For the Databricks logo, always use the inline SVGs from BRAND_SYSTEM.md — never external URLs. See BRAND_SYSTEM.md "Customer / Partner Logo Guidelines" for full details.

**CRITICAL: Before invoking `/databricks-slides`, read `resources/EBC_BEST_PRACTICES.md` — specifically the "Applying Best Practices to Slide Generation" section — and include its rules in the presentation brief.** The slide generation skill does not have access to this file, so you must pass the guidance forward explicitly.

The presentation must follow the **narrative arc structure** and **EBC best practices slide design rules**:

##### Slide structure (15 slides)

1. **Title slide** — Joint-branded: "[Customer Name] x Databricks Executive Briefing" with date and location. Include both logos.
2. **Welcome & agenda** — Brief introductions, session flow, and ground rules ("this is a conversation, not a presentation")
3. **Customer landscape** — Acknowledge the customer's business context, strategic priorities, and industry trends (from Phase 2 Team B research). This shows we've done our homework and frames the conversation around *their* world.
4. **Voice of the Customer** — A facilitation slide with open-ended questions and maximum whitespace. Frame as: "This is your session. We're here to listen." **This must come before any Databricks content.** Never open with a corporate pitch.
5. **Partnership today** — Where we are together: current platform footprint, production use cases, value delivered. Use specific numbers from Salesforce and Logfood — not generic stats.
6-8. **Use case acceleration / Platform as enabler** — One section per area of interest from the agenda. Each should:
   - Frame the business challenge from the customer's perspective using the customer's own language
   - Present Databricks capabilities as **customer problem solvers**, not product features (say "What it solves for [Customer]" not "What Databricks does")
   - Use clean before/after comparisons or max 3-card value propositions — never complex multi-layer architecture diagrams
   - Never use Databricks product terminology on business-outcome slides (no "Unity Catalog", "Mosaic AI", "Lakeflow" — instead say "unified governance", "AI factory", "automated pipelines")
9-11. **Deep-dive topic sessions** — Matched to customer's stated areas of interest. Each should:
   - Include a relevant customer story or industry proof point — reference companies in the same industry, at similar scale
   - Where possible, name-drop executives the audience may know personally; frame as "where [Person] built the playbook" not generic "Company X achieved Y"
   - Leave space for discussion (these are conversation starters, not monologues)
12. **Vision & roadmap** — Forward-looking partnership vision aligned to the selected quadrant. For Value Recovery, emphasize unlocking more from what's already deployed. For Art of Possible, paint a picture of what's achievable.
13. **Proof points & social proof** — Peer credibility with named executives and specific outcomes from similar companies
14. **Co-creation planning** — Reframe from "here's our plan" to **"let's plan together."** Include decision-point cards: "Which use cases?", "Who leads?", "When do we start?" Use language like "Three decisions to make today" not "90-day acceleration plan."
15. **Close** — Mutual commitments, next steps, and a tagline that invites continued conversation

##### Engagement hooks (MANDATORY)

Every slide from slide 3 onwards must include a **personalised engagement hook** — a callout box targeting a specific executive attendee by name with a pre-planned open-ended question. Each hook must:

- **Name the person** — "[First name], your [specific reference]..."
- **Reference something specific** — A talk they gave, a paper they wrote, a known initiative, their job posting language
- **Ask an open question** — Not yes/no. Start with "Where...", "What...", "How..."
- **Connect to the slide topic** — Natural bridge from slide content to the executive's world
- **Be unique** — No duplicate hooks across slides. Every hook targets a different person or angle.

Use the planning doc's attendee profiles (from Phase 2 Team C) to match hooks to the right person on the right slide. If attendee research is insufficient for personalised hooks, flag this to the user and ask for more detail rather than writing generic hooks.

##### Anti-patterns to REJECT

Instruct the slide generation skill to avoid these patterns — if they appear, they must be reworked:

- Generic pipeline diagrams (Ideation → Development → Deployment → ...) — these are product dumps
- Multi-layer architecture diagrams with product names — not C-level appropriate
- Slides with more than 4 cards/items — information overload; split or simplify
- More than 3 product capabilities per slide
- Engagement hooks that say "What questions do you have?" — too generic, must be personalised
- Duplicate engagement hooks across slides
- Closing slides that prescribe a timeline — should invite co-creation instead

##### Presentation design principles

- **Customer-branded with Databricks accent** — The deck should feel like the customer's brand. Use their primary colours for backgrounds, headings, and UI chrome. Use their typography (or closest Google Fonts match). Databricks lava/coral appears only as a secondary accent on highlights, CTAs, and data callouts. Customer logo appears first in any logo bar. Research the customer's brand via their website or brandfetch.com to get accurate colours and fonts.
- **Conversation menu, not linear narrative** — Slides should feel like a menu of conversation starters. Each slide should be self-contained enough that the discussion leader can skip, reorder, or deep-dive based on room energy. Include whitespace — slides should not be packed wall-to-wall.
- **80/20 rule** — Target 80% discussion time, 20% presentation. Slides are prompts for discussion, not walls of text. Aim for 5-7 words per bullet, large visuals, and white space.
- **Customer-centric framing** — Lead with their challenges and priorities, not Databricks features. "How [Customer] can..." not "Databricks enables..."
- **Data-driven** — Include specific account metrics (MRR, use case counts, workspace adoption) rather than generic claims
- **Audience-appropriate depth** — Match content density to the seniority of the room. VP+ audiences want strategic themes; technical leaders want architecture and roadmap.
- **The HTML deck works offline** and can be opened in any browser — no PowerPoint needed

After generation, **copy the final HTML file into the current project folder** so it lives alongside the markdown plan:

```bash
cp ~/Documents/presentations/YYYY-MM-DD/<deck-name>/<deck-name>.html ./ebc_deck_<account_slug>.html
```

Then offer to upload to Google Drive using `/google-drive-upload`.

### Phase 6: Refine (best practices sweep)

**Purpose:** Re-read the complete generated document and presentation deck. Apply EBC best practices as a scoring rubric — not a checklist to tick, but a critical review that produces specific revisions.

**Launch a refinement subagent** that:

1. Re-reads `resources/EBC_BEST_PRACTICES.md` in full
2. Re-reads the generated markdown document end-to-end
3. Scores each dimension and flags specific issues:

| Dimension | What to check | Source |
|-----------|--------------|--------|
| **Narrative arc** | Does the agenda follow Opening → Rising Action → Climax → Resolution? Is there a clear story from first session to last? | Best practices: Agenda Design |
| **80/20 balance** | Is there enough discussion time vs. presentation? Does every session have an engagement hook? | Best practices: The 80/20 Rule |
| **Dual objectives** | Are both customer objectives AND account team objectives served by the agenda? Can you trace each objective to at least one session? | Best practices: Define Dual Objectives |
| **Customer-first flow** | Does the agenda open with customer voice, not a Databricks pitch? Is the VOC session before any product content? | Best practices: Customer-First Flow |
| **Customization depth** | Does the planning depth match the lead time (Tier 1/2/3)? | Best practices: Customization tiers |
| **Discussion leaders** | Are speakers framed as facilitators, not presenters? Is there a prep session plan for each? | Best practices: Discussion Leader Preparation |
| **Product dump check** | Are we showing 2-3 pillars mapped to customer objectives, not the entire catalog? | Best practices: Common Pitfalls |
| **Engagement hook quality** | Does every hook reference specific attendee research? No generic "what are your thoughts?" | Step 5c rules |
| **Demo strategy** | Do demos use customer-relevant data? Is there a before/after? Is governance shown? Backup planned? | Best practices: Demo Strategy |
| **Follow-up cadence** | Is same-day through 90-day follow-up defined with owners? | Best practices: Post-Briefing Follow-Up |
| **Sensitive topic coverage** | Are all identified sensitive topics addressed in the handling approach? Are there topics the research missed? | Phase 2 Team C output |
| **Attendee completeness** | Does every attendee have: education, career history, recent activity with links, tailored EBC focus? | Template quality gate |

4. For each dimension scored below "strong", make specific revisions to the markdown document
5. Regenerate the Google Doc if revisions were made (using the clear-and-rewrite pattern from Phase 5)
6. Run the final quality gate checklist from the template and confirm all items pass

**Output:** Present a refinement summary to the user showing what was changed and why.

### Phase 7: Deliver (output)

**Local artifacts** — Ensure both files are saved in the current project folder before delivering output:
- `ebc_plan_<account_slug>.md` — the markdown planning document
- `ebc_deck_<account_slug>.html` — the presentation deck (if generated)

Return to the user:
1. **Google Doc URL**
2. **Summary of the EBC plan** - Quadrant, key themes, speaker lineup
3. **Presentation deck** (if generated) - HTML file path and/or Google Drive link
4. **Speaker prep checklist** - For each discussion leader: customer profile shared, engagement hooks prepared, success criteria defined, backup speaker assigned
5. **Post-EBC follow-up cadence:**
   - Same day: Personalized thank-you from executive sponsor
   - Day 2: Internal debrief (themes, competitive intel, action items)
   - Week 1: Action items summary to all attendees (both sides)
   - Week 2: Follow-up on committed POCs, trials, or deep-dives
   - 30 days: Pipeline checkpoint (deal progression, consumption changes)
   - 90 days: Long-term influence tracking
6. **Pre-EBC preparation items** - Logistics, demo prep, content review deadlines

## Document footer

Always end the document with: `*Document generated by EBC Planner on [DATE]*`

## Tips for best results

### Customer attendee research
- Search LinkedIn profiles via web search for executive backgrounds
- Look for career history, areas of expertise, and "hot buttons"
- Note any previous interactions with Databricks (from Glean/Salesforce)

### Quadrant accuracy
- When in doubt between quadrants, lean toward the one that addresses the most urgent account need
- BRAG Red accounts almost always need Q3 (Value Recovery) or Q1 (Art of Possible)
- New logos or early-stage accounts are typically Q1 or Q2

### Agenda flow
- Open with executive-level vision, not technical detail
- Build toward technical depth gradually
- End with concrete next steps and commitments
- Match presenter seniority to audience seniority

### Speaker matching
- Always include an executive sponsor (MD or Dir level) for exec-facing EBCs
- Technical speakers should match the depth the customer expects
- Industry specialists add credibility for vertical-specific topics
- For Q3/Q4 EBCs, always check for relevant global speakers (industry VPs, product leaders, regional execs)
- Align EBC dates with existing global speaker travel where possible - check calendars early
- Global speakers based in the US need 2-3 weeks lead time for ANZ travel coordination

### Customer and market intelligence
- Always search both Glean (internal) and web (public) for recent customer news
- Regulatory actions and lawsuits often create the highest-urgency use cases - search for these specifically
- Look for technology partnership announcements that reveal competitive positioning (e.g. cloud deals, AI platform selections)
- Check for AI maturity signals - number of models in production, AI team size, publicised AI initiatives
- Search for missed engagements or cancelled briefings in Glean - these are follow-up opportunities
- Cross-reference internal intelligence with public news to build a complete picture
- Always synthesize findings into "what this means for the EBC" - don't just list facts

### Document quality
- Use specific numbers from Salesforce/Logfood, not estimates
- Include hyperlinks to all referenced documents
- Add person chips for all Databricks attendees
- Color-code status indicators in tables

## Example invocations

```
User: /gtm-ebc-planner
-> Starts conversational intake, gathers all inputs, generates full EBC document

User: Create an EBC plan for Acme Corp, half day on March 20th in Melbourne
-> Extracts account name, date, and location, asks for remaining inputs

User: /gtm-ebc-planner for Telstra - full day EBC focused on GenAI and data governance
-> Extracts account, duration, and topics, fills in the rest from research
```

## Resources

- `resources/EBC_BEST_PRACTICES.md` - Industry best practices and Databricks-specific guidance
- `resources/EBC_TEMPLATE.md` - Output document template
- `resources/QUADRANT_GUIDANCE.md` - EBC quadrant selection framework
- `resources/SPEAKER_DATABASE.json` - Speaker expertise and topic mapping
- `resources/PERSONA_GUIDE.md` - Persona-specific anxiety mapping and tailoring guide
- `resources/AI_MATURITY_STAGING.md` - AI/Data maturity assessment framework
- `resources/OBJECTIONS_GUIDE.md` - Common objection handling for discussion leaders
- `resources/AGENDA_TEMPLATES.md` - Half-day and full-day agenda starting templates
- `resources/fix_ebc_doc.py` - Google Docs post-processing script
