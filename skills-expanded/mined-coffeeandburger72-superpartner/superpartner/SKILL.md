---
name: superpartner
description: "Build a living profile of your partner from chat history. Analyze personality, interests, important dates, and generate gift ideas and dating plans. Supports WhatsApp, WeChat, and LINE exports."
argument-hint: "[subcommand] [partner-name]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, CronCreate, CronList, CronDelete
---

# Superpartner

Build a living profile of your partner from chat history — personality analysis, interest mapping, occasion tracking, gift ideas, and dating plans.

---

## Language Support

Detect the language of the user's first message and respond in that same language for the entire session.

**Supported languages:**
- **English** — default
- **Chinese (Mandarin)** — if user writes in simplified or traditional Chinese
- **Cantonese** — if user writes in Cantonese dialect (e.g., colloquial expressions, Cantonese-specific characters like 嘅、咗、啲、冇、嗰)

**Rules:**
- Detect from the user's first message in this session. If ambiguous between Mandarin and Cantonese, default to the one that matches the detected patterns.
- All prompts, questions, confirmations, and output summaries must be in the detected language.
- Profile files (persona.md, interests.md, etc.) are always written in the detected language.
- If the user switches language mid-conversation, follow the switch.

---

## Subcommand Router

Parse the argument string passed to this skill. The first token is the subcommand, remaining tokens are arguments.

**Important:** `SKILL_DIR` refers to the directory containing this SKILL.md file. All prompt file reads (parsers/, analyzers/, builders/, merger.md) use paths relative to `SKILL_DIR`. All partner profile reads/writes use `SKILL_DIR/partners/<slug>/`.

### Routing Table

| Argument pattern | Action |
|-----------------|--------|
| *(no args)* | Run **Intake Flow** (create) |
| `create` | Run **Intake Flow** (create) |
| `update <name>` | Run **Update Flow** |
| `gifts <name>` | Run **Gifts Regeneration** |
| `dates <name>` | Run **Dates Regeneration** |
| `guide <name>` | Run **Guide Regeneration** |
| `ask <name> <question...>` | Run **Ask Flow** |
| `list` | Run **List Flow** |
| `delete <name>` | Run **Delete Flow** |
| `sherlock <name>` | Run **Sherlock Flow** |

### Resolving `<name>`

The `<name>` argument is a slug (e.g., `jane-doe`). To resolve:

1. Check if `partners/<name>/meta.json` exists
2. If not found, try fuzzy match: Glob `partners/*/meta.json`, read each, check if `name` field case-insensitively contains the argument
3. If still not found, tell the user the partner was not found and suggest running `list` to see available profiles

---

## Intake Flow (create)

This is the main onboarding flow, triggered by no arguments or the `create` subcommand.

### Question 1: Partner Name

Ask:
> What's your partner's name or nickname?

After receiving the name:
1. Store the display name exactly as given
2. Generate a slug: lowercase, replace spaces with hyphens, strip all characters except `a-z`, `0-9`, and `-`
3. Check if `partners/<slug>/` directory already exists
   - If it exists, ask: "A profile for **<display name>** already exists. Would you like to **update** it with new data, or **overwrite** it completely?"
   - If "update" → switch to Update Flow
   - If "overwrite" → delete existing directory via Bash (`rm -rf partners/<slug>/`), continue with create

### Question 2: Relationship Context

Ask:
> How long have you been together, and what stage? (e.g., dating 3 months / committed 2 years / long-distance)

Store the response. This calibrates:
- Gift budget range (newer relationship = lower budget suggestions)
- Date idea intimacy level
- Expected history depth for analysis

**LDR Detection:**

After storing the response, parse for long-distance indicators:
- Keywords: "long-distance", "異地", "LDR", "遠距離"
- Different city or country names for each person
- Mentions of visits, flights, or travel to see each other

If detected, set `ldr: true` in context. This flag is passed to all analyzers and builders to activate LDR-specific logic.

If not detected from the user's answer but later detected from chat data during analysis (relationship_analyzer will flag this), confirm with the user:

> "Based on the chat patterns, it looks like you might be in a long-distance relationship — is that right?"

Set the flag based on their response.

### Question 3: Chat Import

Ask:
> Drop your chat export file, or paste conversation text. I support:
> - **WhatsApp (.zip)** — export directly from WhatsApp, includes chat + images
> - **WeChat** (.csv or text export)
> - **LINE** (.txt export)
> - **Raw pasted text** from any platform

After receiving input, detect the type:

**File path detection:** If the input looks like a file path (starts with `/` or `~`, or contains common path patterns):

1. **`.zip` file** — Read `parsers/whatsapp.md` from skill directory, follow its instructions to unzip and parse
2. **`.txt` file** — Read the first 5 lines to detect format:
   - WhatsApp pattern: lines matching `[DD/MM/YYYY, HH:MM:SS]` or `[M/D/YY, H:MM:SS AM/PM]` → Read `parsers/whatsapp.md`
   - LINE pattern: date headers like `YYYY/MM/DD` followed by tab-separated `HH:MM\tName\tMessage` → Read `parsers/line.md`
   - If unclear, ask the user which platform
3. **`.csv` file** — Read `parsers/wechat.md` from skill directory, follow its instructions
4. **Raw text paste** (no file path detected) — Treat as generic chat data. Extract what you can: look for timestamp patterns, sender names, message content. Do best-effort parsing without a dedicated parser.

**After parsing, confirm:**
> Found **X messages** from **[start date]** to **[end date]** between **[sender1]** and **[sender2]** on **[platform]**. Proceeding with analysis.

Wait for user acknowledgment or correction before proceeding to the create orchestration.

---

## Create Orchestration

After parsing is complete and confirmed, run the following pipeline **sequentially**. Each step reads a prompt file from the skill directory, executes its instructions against the parsed chat data, and holds or writes results.

### Phase 1: Analysis (hold results in memory)

1. **Persona analysis** — Read `analyzers/persona_analyzer.md`, analyze the parsed chat data. Hold the structured analysis results. This now includes Layer 5: Attachment Orientation.
2. **Interests analysis** — Read `analyzers/interests_analyzer.md`, analyze the parsed chat data + any photo paths from the import. Hold results.
3. **Occasions analysis** — Read `analyzers/occasions_analyzer.md`, analyze the parsed chat data. Hold results.
4. **Relationship analysis** — Read `analyzers/relationship_analyzer.md`, analyze the parsed chat data. Pass the `ldr` flag from context. Hold results. This now includes Dimension 7: Relationship Health Indicators and LDR-specific signals if applicable.

### Phase 2: Build (write profile files)

Create the partner directory first:
```
Bash: mkdir -p partners/<slug>
```

5. **Persona profile** — Read `builders/persona_builder.md`, generate `partners/<slug>/persona.md` using persona analysis results.
6. **Interests profile** — Read `builders/interests_builder.md`, generate `partners/<slug>/interests.md` using interests analysis results.
7. **Occasions profile** — Read `builders/occasions_builder.md`, generate `partners/<slug>/occasions.md` using occasions analysis results.
8. **Gifts guide** — Read `builders/gifts_builder.md`, generate `partners/<slug>/gifts.md` using persona + interests + occasions results. The builder now reads love language ranking and attachment orientation from persona results to prioritize and calibrate recommendations.
9. **Dating ideas** — Read `builders/dating_ideas_builder.md`, generate `partners/<slug>/dating_ideas.md` using persona + interests + relationship results. Pass the `ldr` flag and relationship stage. The builder now reads love language, attachment, and LDR status to adapt its output structure.
10. **Relationship guide** — Read `builders/relationship_guide_builder.md`, generate `partners/<slug>/relationship_guide.md` using persona profile + relationship analysis results. Pass the `ldr` flag.

### Phase 3: Finalize

11. **Write meta.json** — Write `partners/<slug>/meta.json` with the following structure:

```json
{
  "name": "<display name>",
  "slug": "<slug>",
  "created_at": "<ISO 8601 timestamp>",
  "updated_at": "<ISO 8601 timestamp>",
  "version": "v1",
  "relationship": {
    "stage": "<stage from Question 2>",
    "duration": "<duration from Question 2>",
    "started": "<approximate start date if calculable>"
  },
  "ldr": false,
  "sources": [
    {
      "platform": "<whatsapp|wechat|line|generic>",
      "file": "<original filename or 'pasted text'>",
      "date_range": "<start date> to <end date>",
      "message_count": <number>,
      "imported_at": "<ISO 8601 timestamp>"
    }
  ],
  "stats": {
    "photos_analyzed": <number>,
    "stickers_sampled": <number>
  }
}
```

12. **Display summary** — Show the user a summary of key findings:
    - Top personality traits (3-5 bullet points)
    - Attachment orientation (1 line — behavioral summary, no psychological labels)
    - Top interests (5-8 items across categories)
    - Next upcoming occasion (date + what it is)
    - Top 3 gift ideas with brief reasoning
    - Top relationship insight from the guide (1 sentence)
    - A note that they can use `gifts`, `dates`, `guide`, or `ask` subcommands for more detail

13. **Offer occasion reminders** — Check `occasions.md` for dates within the next 90 days. If found, offer:

    > "I found **N upcoming occasions** in the next 90 days. Want me to set up reminders so you don't miss them?"

    If the user accepts:
    - For each occasion, create two cron reminders using the CronCreate tool:
      - **2 weeks before:** "**[Partner Name]'s [Occasion]** is in 2 weeks ([date]). Want me to refresh gift ideas or search for something specific?"
      - **3 days before:** "**[Partner Name]'s [Occasion]** is in 3 days ([date]). Here's your top gift pick: [#1 from gifts.md]. Need last-minute ideas?"
    - Each cron job message should include the partner slug for context
    - If the user declines, skip this step entirely

14. **Offer web search** — After the summary, offer:

    > "I can also search for specific products, restaurants, and venues near [detected location] based on these recommendations. Want me to look up concrete options for gifts or date ideas?"

    If accepted, follow the web search instructions in `gifts_builder.md` and/or `dating_ideas_builder.md`.

15. **Memory entry** — Check if the directory `~/.claude/projects/` exists. If it does, attempt to find the current project's memory directory. If a memory directory is found, write a concise entry file with:
    - Partner name and common nicknames
    - Attachment orientation (1-line behavioral summary — no labels)
    - Top 2 love languages
    - Next upcoming occasion and date
    - LDR status (if applicable)
    - Format: one short paragraph summarizing who she is and what to remember, suitable for ambient context in future conversations

---

## Update Flow

Triggered by: `update <name>`

1. Resolve `<name>` to an existing partner directory (see "Resolving `<name>`" above)
2. Read `merger.md` from the skill directory for merge instructions
3. Ask the user to provide new chat data (same import prompt as Question 3 in Intake Flow)
4. Parse the new data using the appropriate parser
5. Follow the merge instructions from `merger.md` to integrate new data into existing profile files
6. After merge, auto-regenerate `gifts.md`, `dating_ideas.md`, and `relationship_guide.md`
7. Update `meta.json`: bump `updated_at`, append to `sources` array, update `stats`
8. **Post-update nudge:** Compare old and new analysis for significant changes. If detected, inform the user:
   - New conflict patterns → "I noticed some new tension patterns in the recent messages."
   - Love language signals shifted → "Her love language ranking may have shifted based on the new data."
   - New wishlist items found → "Found [N] new wishlist items."
   - LDR status changed → "It looks like your situation may have changed — [started/ended long-distance]."
   - These are informational — the regeneration already happened in step 6.
9. **Check for new occasion reminders:** Compare occasions.md before and after merge. If new occasions were found in the next 90 days, offer to set up reminders (same flow as create step 13).

---

## Gifts Regeneration

Triggered by: `gifts <name>`

1. Resolve `<name>` to an existing partner directory
2. Read the following files from `partners/<name>/`:
   - `persona.md` (for love language ranking and attachment orientation)
   - `interests.md`
   - `occasions.md`
3. Read `builders/gifts_builder.md` from the skill directory
4. Follow the builder instructions to regenerate `partners/<name>/gifts.md`
5. Display the updated gift ideas to the user
6. Offer web search for concrete product and experience picks near the user's location

---

## Dates Regeneration

Triggered by: `dates <name>`

1. Resolve `<name>` to an existing partner directory
2. Read the following files from `partners/<name>/`:
   - `persona.md` (for love language ranking and attachment orientation)
   - `interests.md`
   - `occasions.md` (for occasion-tied date ideas)
3. Read `partners/<name>/meta.json` to check the `ldr` flag and relationship stage
4. Read `builders/dating_ideas_builder.md` from the skill directory
5. Follow the builder instructions to regenerate `partners/<name>/dating_ideas.md`
6. Display the updated dating ideas to the user
7. Offer web search for concrete venue and activity picks near the user's location

---

## Guide Regeneration

Triggered by: `guide <name>`

1. Resolve `<name>` to an existing partner directory
2. Read the following files from `partners/<name>/`:
   - `persona.md`
   - `interests.md`
   - `occasions.md`
3. Read `builders/relationship_guide_builder.md` from the skill directory
4. Follow the builder instructions to regenerate `partners/<name>/relationship_guide.md`
5. Display the key insight from each section (1 sentence per section) to the user

---

## Ask Flow

Triggered by: `ask <name> <question...>`

1. Resolve `<name>` to an existing partner directory
2. Read all 6 profile files from `partners/<name>/`:
   - `persona.md`
   - `interests.md`
   - `occasions.md`
   - `gifts.md`
   - `dating_ideas.md`
   - `relationship_guide.md`
3. Use the full profile as context to answer the user's question
4. For relationship or communication questions (e.g., "how should I handle X", "what's the best way to tell her Y", "why does she do Z"), prioritize context from `relationship_guide.md` — it contains the most synthesised and actionable relationship insights.
5. Answer naturally and helpfully, citing specific details from the profile where relevant
6. If the question is about something not covered in the profile, say so and suggest what additional chat data might help

---

## List Flow

Triggered by: `list`

1. Glob `partners/*/meta.json`
2. If no results, tell the user no partner profiles exist yet and suggest running the skill with no arguments to create one
3. If results found, read each `meta.json` and also read the corresponding `occasions.md` to find the next upcoming occasion
4. Display a summary table:

| Name | Stage | Duration | Last Updated | Next Occasion |
|------|-------|----------|-------------|---------------|
| ... | ... | ... | ... | ... |

---

## Delete Flow

Triggered by: `delete <name>`

1. Resolve `<name>` to an existing partner directory (see "Resolving `<name>`" above)
2. Read `partners/<name>/meta.json` to get the display name
3. Confirm with the user:
   > Are you sure you want to delete the profile for **<display name>**? This will remove all analysis, gift ideas, dating plans, relationship guide, scheduled reminders, and memory entries. This cannot be undone.
4. Only proceed if the user explicitly confirms
5. Delete all profile files:
   - Run via Bash: `rm -rf partners/<name>/`
6. Clean up scheduled reminders:
   - Use CronList to find all cron jobs
   - Delete any cron job whose message or metadata references this partner's slug, using CronDelete
7. Clean up memory entries:
   - Check the project memory directory for any file referencing this partner
   - If found, delete the memory file and remove its entry from MEMORY.md
8. Confirm deletion to the user:
   > Deleted profile for **<display name>**: profile files removed, scheduled reminders cancelled, memory entries cleared.

---

## Sherlock Flow

Triggered by: `sherlock <name>`

An interactive behavioral analysis session that helps the user examine suspicious or confusing relationship patterns.

1. Read `sherlock.md` from the skill directory for full session instructions
2. Resolve `<name>` to an existing partner directory (see "Resolving `<name>`" above)
3. Read `partners/<name>/persona.md` and `partners/<name>/relationship_guide.md` into context for baseline calibration
4. Follow the session flow in `sherlock.md`: intake → analysis → session loop → session end

---

## Tool Usage Matrix

| Tool | When to use |
|------|------------|
| **Bash** | Unzip `.zip` files, create directories (`mkdir -p`), delete profiles (`rm -rf`), count messages (`wc -l`), list directory contents |
| **Read** | Read prompt files from skill directory (parsers, analyzers, builders, merger), read chat export files (`.txt`, `.csv`), read images/stickers (`.jpg`, `.png`, `.webp`) for visual analysis, read existing profile files |
| **Write** | Write new profile output files (`persona.md`, `interests.md`, `occasions.md`, `gifts.md`, `dating_ideas.md`, `relationship_guide.md`), write `meta.json`, write memory entries |
| **Edit** | Update existing profile files during merge/update flow, update `meta.json` fields |
| **Glob** | Find partner directories (`partners/*/meta.json`), find media files in unzipped exports (`**/*.jpg`, `**/*.webp`), find chat files in zip extracts |
| **Grep** | Search chat text for date patterns, keyword extraction, find mentions of birthdays/anniversaries, search across profile files |
| **WebSearch** | Search for concrete products, venues, and experiences during opt-in web search step |
| **CronCreate** | Set up occasion reminders (2 weeks and 3 days before upcoming dates) — only with user consent |
| **CronList** | List existing reminders during delete flow cleanup |
| **CronDelete** | Remove reminders for deleted partner profiles |
