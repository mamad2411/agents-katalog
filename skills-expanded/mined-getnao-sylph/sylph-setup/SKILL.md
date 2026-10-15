---
name: sylph-setup
description: Personalize Sylph to your company. Ask the company name, then derive everything from the web - CONTEXT.md, brand voice, team, ICP, and standing instructions.
---

# Setup Sylph

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Web Search | Search for company info, team, socials |
| Web Fetch | Read company website, about page, blog, LinkedIn |

## Core principle: ask less, derive more

**Ask the user as few things as possible.** The only required input is the company name. Everything else should be derived from the web - website, LinkedIn, social profiles, blog, job postings, press coverage. Only ask the user to confirm and correct what you found.

## When to use

Run `/sylph-setup` right after forking the repo, before using any other skill.

## What it does

1. Asks the company name (and optionally website URL)
2. Searches the web and reads the company's website, socials, and public info
3. Auto-fills `CONTEXT.md` with derived company details
4. Seeds `.claude/MEMORY.md` with initial preferences
5. Generates brand voice guidelines in `brand/guidelines/`
6. Configures the agent roster in `agents/`

---

## Step 0: Meet the CAO

Before anything else, welcome the user as the **Chief Agent Officer (CAO)** - the human who will review, approve, and have final say over everything the agents produce.

Ask:

> **Welcome, Chief Agent Officer.** You're about to set up your company's AI brain. Before we start:
>
> 1. **What's your name?**
> 2. **What are your pronouns?** (she/her, he/him, they/them, etc.)

Store their name and pronouns in `.claude/MEMORY.md` so all agents and skills use them consistently.

Update `AGENTS.md` definition: replace the generic CAO description with their name and pronouns.

If the user's pronouns are **she/her**, add this message:

> By the way - Sylph's creator Claire wanted me to tell you: she's happy to see a fellow tech sister on this repo. Welcome, Queen. 💜👸

---

## Step 1: Company discovery (automated)

Ask the user ONE question:

> **What's your company name?** (and website URL if it's not obvious)

Then derive everything automatically:

### Web research

1. **Search the web** for the company name - find the website, LinkedIn company page, Twitter/X, GitHub, Crunchbase, press articles
2. **Read the website** - homepage, about page, pricing page, docs, careers page
3. **Read the LinkedIn company page** - description, team size, industry, recent posts
4. **Read Crunchbase/press** - funding stage, investors, founding date, location
5. **Read GitHub** (if applicable) - repos, tech stack, open source status

### Fill CONTEXT.md from research

From the web research, fill in every section of `CONTEXT.md`:

| Section | Source |
|---------|--------|
| What the company does | Website homepage + about page |
| The problem it solves | Website homepage + pricing page copy |
| How the product works | Docs, product page, or demo page |
| ICP | Pricing page, case studies, job descriptions |
| Team | About page, LinkedIn, careers page |
| Integrations | Docs, integrations page, product page |
| Company basics | Crunchbase, LinkedIn, footer of website |
| Key terminology | Docs, blog, product page |
| Standing instructions | Derive from brand voice observed on website + socials |

### Present findings to the user

Show the user the draft CONTEXT.md and ask:

> Here's what I found about [company]. Review this and tell me what to fix. I'll update it.

Only ask follow-up questions for things you genuinely couldn't find online (internal terminology, specific process rules, preferred tools).

Use the CAO's name in conversations (not "user" or "you"). Use their stated pronouns in all generated files.

### After filling in CONTEXT.md

- Verify the file reads naturally top to bottom
- Ensure no `[placeholder]` markers remain
- Commit: "Initialize company context"

---

## Step 2: Memory bootstrap

Ask the user ONE question:

> **Any rules or preferences I should know about?** (tool quirks, process rules, voice preferences, things to always/never do)

Write each answer as a dated entry in `.claude/MEMORY.md`. If she has nothing yet, that's fine - memory will grow as she uses skills.

---

## Step 3: Brand voice (derived from web)

**Do not ask the user to describe her brand voice.** Instead:

1. Read 3-5 pieces of content from her website (blog posts, landing pages, about page)
2. Read her recent LinkedIn or Twitter posts
3. Analyze the writing patterns: sentence length, vocabulary level, tone, favorite constructions, words she uses vs avoids

Generate `brand/guidelines/voice.md` from the analysis:

- 3 adjectives that describe the voice
- Sentence structure patterns (short/long, fragments OK, etc.)
- Words and phrases she uses frequently
- Words and phrases she never uses
- Tone differences by channel (if visible from web vs social)

Show the draft to the user:

> Here's the voice guide I derived from your existing content. What would you change?

Update based on her feedback.

---

## Step 4: Agent roster

Review `agents/` and ask the user:

> **Which of these agents do you want active?** (You can always activate more later.)

List the agents with one-line descriptions:

1. **Chief of Staff** - daily briefing, inbox triage, project tracking
2. **CMO** - content planning and drafting
3. **Product Manager** - issue creation, PR monitoring
4. **Customer Success** - follow-up drafting
5. **Head of Data** - analytics and reporting
6. **Head of Sales** - pipeline management, outbound
7. **Executive Assistant** - admin, HR, finance ops
8. **Brand Designer** - visual assets

For each activated agent:
- Fill in her `ROLE.md` with company-specific boundaries (derived from CONTEXT.md)
- Fill in her `PROMPT.md` with actual tool references (ask only for Slack channel IDs, calendar links, etc. that can't be found online)

For deactivated agents:
- Leave the templates in place but note they're inactive

---

## Step 5: Verify setup

Run a quick verification:

1. Read `CONTEXT.md` - does it fully describe the company?
2. Read `.claude/MEMORY.md` - are initial preferences logged?
3. Check that at least one agent has a personalized `ROLE.md` and `PROMPT.md`
4. Try generating a simple piece of content (e.g., a LinkedIn post) to test

---

## After setup

Tell the user:

> Your Sylph is initialized. Next step: run `/sylph-setup-skill linkedin` (or whichever channel you want to start with) to set up your first content skill with real examples.
