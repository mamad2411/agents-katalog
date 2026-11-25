---
name: inboxmate-demo
description: "Set up a personalized InboxMate demo chatbot for a sales prospect. Use when asked to create a demo, set up an InboxMate playground, or prepare a chatbot demo. Guides the full pipeline: research company, scrape content, call MCP, deliver playground URL."
---

# InboxMate Demo Setup Pipeline

> **Announce to the user at the very start:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> InboxMate Demo Pipeline started.
> Working through 5 phases — I'll narrate each step.
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## PHASE 0 — Learn the Platform

> **Announce:** `[0/5] Learning InboxMate platform capabilities...`

**You are new to InboxMate. Do this before anything else.**

InboxMate is a white-label AI chatbot platform built by psquared. Businesses embed a chat widget on their website — visitors chat with an AI agent that knows the company's products, services, and FAQs.

The MCP server at `https://app.psquared.dev/api/mcp` exposes tools to create and configure these agents programmatically. All operations run against a shared demo account.

**Call `tools/list` on the MCP server first** to get the current tool list and confirm connectivity:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"notifications/initialized","params":{}}
{"jsonrpc":"2.0","id":3,"method":"tools/list","params":{}}
```

**MCP connection:**
- URL: `https://app.psquared.dev/api/mcp`
- Auth: `Authorization: Bearer <token>` — ask Martin for the token if not in env as `NUXT_MCP_DEMO_TOKEN`
- Transport: JSON-RPC 2.0 over HTTP POST

**Key concepts:**
- **Agent** — the AI chatbot entity. Has a system prompt, greeting, widget config (color, domain whitelist, predefined questions)
- **Knowledge bucket** — a vector store. Contains multiple knowledge items that the agent retrieves at query time
- **Knowledge items** — individual focused text chunks added to a bucket. Each item should cover ONE topic (overview, pricing, FAQ, contact, etc.)
- **whitelistedDomains** — controls where the widget appears. Defaults to `demo.inboxmate.psquared.dev`

> **After confirming tools list, announce:** `[0/5] Platform ready. Proceeding to prospect research.`

---

## PHASE 1 — Research the Prospect

> **Announce:** `[1/5] Researching [Company Name]...`

### 1a — Validate Website First

Before scraping, **check if the website is reachable and current**. Use `WebFetch` on the homepage.

**Auto-skip if ANY of these are true:**
- Website returns HTTP error / timeout / unreachable
- Domain is parked, expired, or "coming soon"
- Page has no meaningful content (just a logo or placeholder)
- Copyright year is 2+ years behind current year — site is abandoned
- Only a social media profile exists (no real website)

> If the website is unusable, announce: `SKIP: [Company] — [reason]. Website is not suitable for a demo.`
> **Do NOT ask the user what to do.** Just skip and move on.
> If running as part of the batch pipeline, the batch skill handles CRM marking.
> If running standalone, just stop and report the skip reason — the user can decide later.

### 1b — Scrape Content

Given a company name and/or domain, **fetch all of these pages** (adjust paths as needed):

| Page | What to extract |
|------|-----------------|
| Homepage | Core value prop, headline, tagline, main CTA |
| /about or /ueber-uns | Company story, team, mission, founding year |
| /products or /services or /leistungen | All products/services with descriptions, features, differentiators |
| /pricing or /preise | Pricing tiers, what's included, trial info |
| /faq | Common questions and answers verbatim |
| /contact or /kontakt | Email, phone, address, business hours, contact form |
| /blog or /cases (optional) | Social proof, use cases, customer stories |

**Use WebFetch on each URL.** Do not skip pages — thin knowledge = bad demo.

**Extract and record:**
- Company name (exact spelling, including GmbH/AG/Ltd if present)
- Core product/service in one sentence
- Target customer segment
- Top 3 USPs (what makes them different)
- Pricing structure (free trial? subscription? one-time?)
- Primary CTA (book demo / sign up / contact / request quote)
- Contact details (email, phone, address, hours)
- Tone of the website (formal/informal, corporate/friendly)
- **Primary language** of the website content

> **After fetching, announce:** `[1/5] Research complete. Analyzing language and planning content...`

---

## PHASE 2 — Language Detection & Content Planning

> **Announce:** `[2/5] Planning agent content and language configuration...`

### 2a — Detect Language

Look at the website content you scraped:

| Signal | Decision |
|--------|----------|
| Website is in German only | `language: 'de'` |
| Website is in English only | `language: 'en'` |
| Website has both DE and EN, or company serves both markets | `language: 'multi'` |
| Austrian/German/Swiss company with DE site but international product | `language: 'multi'` |
| English-only company, no German signals | `language: 'en'` |

> **Announce your decision:** `Language: [EN / DE / MULTI] — [reason in one sentence]`

### 2b — Plan Knowledge Items

**Do NOT put all content into one blob.** Create separate focused knowledge items per topic. Each item is independently retrieved by vector search — short, specific items win over large walls of text.

Plan these items (create all that have content):

| Item | Title | Content |
|------|-------|---------|
| 1 | `[Company] – Überblick` / `[Company] – Overview` | What the company does, who they serve, core value prop, founding story |
| 2 | `Produkte & Leistungen` / `Products & Services` | All services/products with descriptions, key features, use cases |
| 3 | `Preise & Pakete` / `Pricing & Plans` | All pricing tiers, what's included, trial/free tier info, upgrade path |
| 4 | `Häufige Fragen` / `FAQ` | All Q&A pairs from the FAQ page verbatim |
| 5 | `Kontakt & Support` / `Contact & Support` | Email, phone, address, hours, how to reach support, response time |
| 6 | `Anwendungsfälle` / `Use Cases` | Customer stories, case studies, example use cases, industries served |
| 7 (multi-lang only) | `Sprachunterstützung & KI-Features` / `Language Support & AI Features` | Explain that the assistant supports both German and English. List key InboxMate features relevant to THIS company (24/7 availability, instant answers, website integration). Frame as benefits for this company's customers. |

> Write all item content in the **target language(s)**. For `multi`: write each item in the language that's most natural for that content, or bilingual if the company operates in both.

### 2c — Craft the System Prompt

Write a **crisp, specific system prompt** — not a generic template. Include ALL of these:

```
You are [Persona Name], the AI assistant for [Company Name].

**Who you help:** [Target customer segment in 1 sentence]

**Your personality and tone:** [Derived from website tone — e.g. "friendly and approachable, using informal language (du/you)" OR "professional and precise, using formal language (Sie/formal English)"]

**Language:** [e.g. "Always respond in German (du-Form)" OR "Respond in the language the visitor uses — German or English"]

**Your goal:** Help visitors understand [Company]'s [main product/service] and guide them toward [primary CTA — e.g. "booking a free demo", "starting a free trial", "contacting the sales team"].

**What you know:** You have access to [Company]'s complete product information, pricing, FAQ, and contact details. Answer from this knowledge.

**When you can't answer:** If a question falls outside your knowledge, say so honestly and offer to connect them with the team: [contact email or "via the contact form on [domain]"].

**Never:** Invent pricing, make promises not reflected in company materials, or discuss competitors in detail.
```

Adjust heavily based on actual company context. This prompt should sound like it was written for THIS specific company.

### 2d — Greeting Message

Write in target language. **Not generic.** Reference the product, their situation, or a hook.

- **Bad:** "Hi! How can I help you?"
- **Good (EN):** "Hi! I'm [Name], [Company]'s AI assistant. Ask me anything about our [product] — pricing, features, or how to get started."
- **Good (DE):** "Hallo! Ich bin [Name], der KI-Assistent von [Company]. Stell mir gerne Fragen zu unseren [Dienstleistungen] — ich helfe dir weiter!"

For `multi`: write separate EN and DE greetings.

### 2e — Predefined Quick Questions (Card Tiles)

**ALWAYS use card tiles** — never plain text pills. Cards look dramatically better and convert higher. They show an icon, a bold title, and a short description — making suggestions feel like real features instead of generic prompts.

**4–5 suggestion cards** that a real prospect would click. Make them irresistible — they should surface the company's best selling points.

Each question is an object with these fields:
- **`text`**: The actual message sent to the chat when clicked. This is what the AI will answer.
- **`title`**: Short card title displayed prominently (2-5 words). This is what the user reads first.
- **`description`**: Brief hint about what to expect (3-5 words). Shown below the title in smaller text.
- **`icon`**: A Lucide icon name in **kebab-case** (e.g. `"briefcase"`, `"credit-card"`, `"shield-check"`, `"clock"`, `"users"`, `"rocket"`, `"globe"`, `"zap"`, `"heart"`, `"target"`, `"lightbulb"`, `"star"`, `"package"`, `"award"`, `"calendar"`, `"mail"`, `"phone"`, `"building"`, `"trending-up"`, `"search"`). If invalid, falls back to a checkmark.

Rules:
- Use the target language (both EN + DE arrays for `multi`)
- Mix types: feature question, pricing question, differentiator question, use-case question
- Keep titles short (2-5 words), descriptions short (3-5 words)
- The `text` field can be longer — it's the actual question the AI answers
- Always set `style: 'cards'` in the `update_quick_questions` call

**Examples for a SaaS company:**
```json
// EN
[
  { "text": "What does [Product] do and who is it for?", "title": "What is [Product]?", "description": "Features & use cases", "icon": "rocket" },
  { "text": "How much does [Product] cost? Are there different plans?", "title": "Pricing & Plans", "description": "Tiers & free trial", "icon": "credit-card" },
  { "text": "How long does setup take and do I need technical knowledge?", "title": "Getting Started", "description": "Setup in minutes", "icon": "zap" },
  { "text": "What makes [Product] different from competitors?", "title": "Why [Company]?", "description": "Key differentiators", "icon": "award" }
]
// DE
[
  { "text": "Was macht [Produkt] und für wen ist es gedacht?", "title": "Was ist [Produkt]?", "description": "Funktionen & Einsatz", "icon": "rocket" },
  { "text": "Was kostet [Produkt]? Gibt es verschiedene Pakete?", "title": "Preise & Pakete", "description": "Tarife & Testphase", "icon": "credit-card" },
  { "text": "Wie lange dauert die Einrichtung und brauche ich technisches Wissen?", "title": "Erste Schritte", "description": "Setup in Minuten", "icon": "zap" },
  { "text": "Was unterscheidet [Produkt] von der Konkurrenz?", "title": "Warum [Company]?", "description": "Die Vorteile", "icon": "award" }
]
```

### 2f — Brand Color

Extract the **primary color** from the website:
1. Check the primary button color or main CTA color in the HTML/CSS
2. Look at the logo colors and dominant accent color
3. If the website uses multiple shades of the same hue (e.g. light blue headers, medium blue buttons, dark blue footer), **always pick the darkest shade** — it looks best as the widget accent color
4. Use the final color as a hex value (e.g. `#1a365d` not `#63b3ed`)

If you can't detect it reliably, ask before proceeding.

### 2g — Demo Page Content

- **offerText**: The main headline of the offer banner. This is NOT a "free consultation" — it's the value proposition with a deadline. The countdown timer shows when THIS offer expires. Examples:
  - DE: "Jetzt starten und 50% Rabatt im ersten Jahr sichern" / "14 Tage kostenlos testen — danach upgraden mit Rabatt" / "Ihren KI-Assistenten jetzt aktivieren — Sonderkonditionen sichern"
  - EN: "Start now and save 50% in your first year" / "14-day free trial — then upgrade with a discount" / "Activate your AI assistant now — special terms available"
  - **Do NOT use "Kostenlose Erstberatung" (free consultation)** — the countdown is for the offer deadline, not a consultation
- **offerExpiresAt**: 7 days from today (ISO 8601). The countdown timer counts down to this date.
- **customMessage**: 1–2 sentences speaking directly to the prospect: "Wir haben diesen Demo-Bot speziell für [Company] konfiguriert. Probier ihn aus!"

> **After planning, show a summary to the user:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> PLAN READY — confirm before building:
>   Company: [name]
>   Language: [en/de/multi]
>   Knowledge items: [N items listed by title]
>   Quick questions: [list]
>   Color: [hex]
>   Offer: [offerText]
> Proceeding to build in 5 seconds unless you say stop.
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## PHASE 3 — Build the Agent via MCP

> **Announce:** `[3/5] Building agent in InboxMate...`

Use **individual MCP tools** — do NOT use `quick_setup_demo` for the full pipeline. It only supports one knowledge item. We need multiple.

### Step 3.1 — Create Agent

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_agent",
    "arguments": {
      "name": "[Company] Assistant",
      "prompt": "[full system prompt from 2c]",
      "primaryColor": "[hex from 2f]",
      "greetingMessage": "[EN greeting from 2d — omit if DE-only]",
      "greetingMessageDe": "[DE greeting from 2d — omit if EN-only]"
    }
  }
}
```

> Save `agentId` from the response. **Announce:** `Agent created: [agentId]`

### Step 3.2 — Create Knowledge Bucket

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_knowledge_bucket",
    "arguments": {
      "name": "[Company] Knowledge",
      "description": "Website knowledge base for [Company] — [N] items"
    }
  }
}
```

> Save `bucketId`. **Announce:** `Knowledge bucket created: [bucketId]`

### Step 3.3 — Add Knowledge Items

For **each item planned in 2b**, call `add_to_bucket` separately:

```json
{
  "method": "tools/call",
  "params": {
    "name": "add_to_bucket",
    "arguments": {
      "bucketId": "[bucketId]",
      "title": "[item title]",
      "content": "[item content — focused, complete, in target language]",
      "sourceUrl": "https://[domain]/[page]"
    }
  }
}
```

> **Announce after each:** `Knowledge item added: "[title]"`
>
> Wait for each call to complete before the next — do NOT batch these.

### Step 3.3b — (If multi-lang) Add Language Support item

If language is `multi`: add one extra knowledge item to the bucket:

- **Title:** `"Sprachunterstützung / Language Support"`
- **Content:**
  ```
  This AI assistant supports both German and English. It responds in whatever language the visitor uses.

  Key features relevant for [Company]:
  - Available 24/7, responds instantly in German or English
  - Trained on [Company]'s complete product and service information
  - Handles common customer questions so your team doesn't have to
  - Guides visitors toward [primary CTA]
  - Escalates to your team for complex inquiries

  Use cases for [Company]:
  [Write 2-3 specific use cases based on what you know about the company]
  ```

**Content quality rules:**
- Each item: 200–800 words. Long enough to be useful, short enough for precise retrieval.
- Write in complete sentences, not bullet-point dumps
- Include actual numbers, prices, and specifics from the website
- For FAQ items: include both the question AND the answer, verbatim if possible

### Step 3.4 — Link Bucket to Agent

```json
{
  "method": "tools/call",
  "params": {
    "name": "set_knowledge",
    "arguments": {
      "agentId": "[agentId]",
      "knowledgeBucketIds": ["[bucketId]"]
    }
  }
}
```

### Step 3.5 — Set Quick Questions (Card Format)

```json
{
  "method": "tools/call",
  "params": {
    "name": "update_quick_questions",
    "arguments": {
      "agentId": "[agentId]",
      "style": "cards",
      "questionsEn": [
        { "text": "[message sent to chat]", "title": "[Card Title]", "description": "[3-5 word hint]", "icon": "[lucide-icon-name]" },
        { "text": "[message sent to chat]", "title": "[Card Title]", "description": "[3-5 word hint]", "icon": "[lucide-icon-name]" }
      ],
      "questionsDe": [
        { "text": "[Nachricht an den Chat]", "title": "[Karten-Titel]", "description": "[3-5 Wort Hinweis]", "icon": "[lucide-icon-name]" },
        { "text": "[Nachricht an den Chat]", "title": "[Karten-Titel]", "description": "[3-5 Wort Hinweis]", "icon": "[lucide-icon-name]" }
      ]
    }
  }
}
```

> For EN-only: use `questionsEn` only, leave `questionsDe` as `[]`.
> For DE-only: use `questionsDe` only, leave `questionsEn` as `[]`.
> Always set `style: "cards"` — this enables the rich card display in the widget.

### Step 3.5b — Restrict widget to demo page only

After the demo page is created (Phase 4), the MCP automatically calls `update_widget_style`
to set `showOnPages: ['/?id=<demoId>']`. This is handled by the `create_demo_page` tool.
You do NOT need to call `update_widget_style` manually for this.

### Step 3.6 — Publish Agent

```json
{
  "method": "tools/call",
  "params": {
    "name": "publish_agent",
    "arguments": { "agentId": "[agentId]" }
  }
}
```

> **Announce:** `Agent published and live.`

---

## PHASE 4 — Create Demo Page

> **Announce:** `[4/5] Creating demo page...`

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_demo_page",
    "arguments": {
      "agentId": "[agentId]",
      "companyName": "[Company Name]",
      "companyDomain": "[domain.com]",
      "logoUrl": "[logo URL if found — otherwise omit]",
      "offerText": "[from 2g]",
      "offerExpiresAt": "[ISO date 7 days from today]",
      "customMessage": "[from 2g]",
      "language": "[en or de — must match the language you chose in Phase 2]",
      "useCases": [
        { "text": "[Use case 1 — specific to this company, 1 sentence]", "icon": "[lucide-icon-name]" },
        { "text": "[Use case 2 — specific to this company, 1 sentence]", "icon": "[lucide-icon-name]" },
        { "text": "[Use case 3 — specific to this company, 1 sentence]", "icon": "[lucide-icon-name]" },
        { "text": "[Use case 4 — optional, if relevant]", "icon": "[lucide-icon-name]" }
      ]
    }
  }
}
```

> The MCP will automatically restrict the widget to only show on `/?id=<demoId>` — no extra step needed.

> Save `demoId` and `playgroundUrl`.

---

## PHASE 5 — Deliver

> **Announce:** `[5/5] Done!`

Output this summary to the user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEMO READY — [Company Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Playground URL (share this with the prospect):
→ [playgroundUrl]

What was configured:
  Language:        [en / de / multi]
  Brand color:     [hex]
  System prompt:   [first 2 sentences of the prompt]
  Greeting (EN):   [greeting]
  Greeting (DE):   [greeting or "—"]
  Quick questions: [list, language-appropriate]
  Knowledge items: [N items — list titles]
  Offer:           [offerText] (expires [date])

Agent ID: [agentId] (for follow-up adjustments)
Demo ID:  [demoId]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Follow-Up Adjustments

If the demo needs changes after delivery, use these individual tools:

| What to change | Tool |
|----------------|------|
| System prompt | `update_prompt` |
| Quick questions | `update_quick_questions` (card objects with text/title/description/icon, set `style: "cards"`) |
| Color, greeting, domain whitelist | `update_widget_style` |
| Add more knowledge | `add_to_bucket` with the existing `bucketId` |
| Republish after changes | `publish_agent` |

---

## Quality Gate — Before Delivering

Run through this checklist mentally before Phase 5:

- [ ] System prompt is specific to this company — no generic filler
- [ ] Greeting message references the product or company name
- [ ] Quick questions use card format (objects with text, title, description, icon) — NOT plain strings
- [ ] Quick questions would make a real prospect click them
- [ ] Primary color matches the company brand
- [ ] At least 4 knowledge items covering: overview, services, pricing/FAQ, contact
- [ ] If multi-lang: DE and EN questions both filled, greeting in both languages
- [ ] If multi-lang: knowledge item 7 (language support + use cases) added
- [ ] Knowledge items are focused topics, not one big dump
- [ ] Offer text is specific and time-limited
- [ ] Widget domain is restricted to `demo.inboxmate.psquared.dev` (auto-set by the platform)
- [ ] `language` matches the company's website language
- [ ] 3-4 specific `useCases` as objects with `{ text, icon }` — not plain strings
- [ ] Use case icons are valid Lucide kebab-case names (e.g. "clock", "users", "shield-check")
- [ ] Offer text is NOT "Kostenlose Erstberatung" — it describes the offer, countdown shows when it expires
- [ ] Widget domain + page restriction set (auto-handled by `create_demo_page`)
