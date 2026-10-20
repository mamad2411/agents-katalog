---
name: zoom-mastermind-recap
description: "Automated AIMM recap pipeline: fetches Zoom cloud recordings, then transforms transcripts into newsletter-style recap reports. Can run on a schedule (fetches recordings + recaps all unprocessed sessions) or manually (user provides transcript paths). Full pipeline: Zoom download, topic extraction, newsletter writing with value-add research, prompt template extraction, email-ready styling, and Notion publishing under the AIMM Report Hub with series navigation. Trigger on: scheduled invocation with no file paths, or manual invocation with transcript/chat file paths."
---

# AIMM Mastermind Recap

Transform AIMM session transcripts into newsletter-style reports the community will actually read. Not meeting minutes — these are curated, researched, styled digests that extract the signal from the conversation and add value beyond what was said in the room.

**Community:** AI Mastermind for Leaders (AIMM)
**Audience:** Knowledge entrepreneurs — consultants, coaches, course creators, and thought leaders learning to become AI-augmented to stay competitive, serve clients better, and increase the value of their products and services.
**Notion hub:** Search for "AIMM Report Hub" in Notion. If it doesn't exist, create it.
**Title format:** `AIMM Recap — [Month Day, Year]` with optional subtitle for guest speakers (e.g., `| Special Guest: Michael Simmons`).

## What This Skill Produces

A recap report with these components:

1. **Pull quote** — A memorable line from the session that sets the tone
2. **"This Week in 30 Seconds"** — 4-5 bullet points that let skimmers decide which sections to read
3. **Topic sections** (3-5 per session) — Each one 500-750 words of substantive, newsletter-style content using the conversation as source material
4. **Value-add callouts** per section — Hot takes, "what this means for you" insights, and/or researched "Go Deeper" resource links (use editorial judgment on which type fits each topic)
5. **Community Corner** — Highlights of member wins, ideas, and contributions worth spotlighting
6. **"Try This Before Next Session"** — A single, concrete, low-effort action item anyone can do in 15 minutes
7. **Prompt Templates** (when the session warrants it) — Copy-paste AI prompts that encode the session's most leverageable techniques
8. **Navigation footer** — Prev/Home/Next links when part of a series

## Inputs

This skill runs in one of two modes:

**Manual mode** — the user provides one or more file paths (transcript, optionally chat) directly in their message. Process exactly that session. Skip Step 0 entirely and go straight to Step 1.

**Scheduled / auto mode** — the user invokes the skill with no file paths (e.g., from `claude -p /zoom-mastermind-recap` on a schedule, or "run the recaps" with no further detail). In this mode you must run Step 0 first to fetch any new Zoom recordings and discover which sessions still need recapping.

**Required input (manual mode):** A meeting transcript — VTT format, plain text, or pasted directly into the chat.

**Optional but enriching:** A chat transcript from the same session (Zoom chat export, Slack thread, etc.). Chat transcripts often contain links, resources, reactions, and side conversations that didn't make it into the spoken transcript. When available, mine them for resource URLs, member attributions, and ideas that surfaced in text but not on camera.

**Output destination:** Markdown file saved locally + Notion page under the AIMM Report Hub (both by default). If Notion MCP is unavailable, produce the markdown only.

## How to Write the Recap

### Step 0: Bootstrap (scheduled / auto mode only)

Skip this step entirely if the user gave you explicit transcript/chat file paths. Run it when the skill is invoked with no file paths — that's the signal that you're being called on a schedule and need to find the work for yourself.

The bootstrap is owned by a sandbox at `/Users/loudalo/Downloads/zoom-recap-sandbox/`. It does two things: pull any new Zoom recordings, then queue up every meeting that has been downloaded but not yet recapped.

#### 0a. Fetch new recordings from Zoom

Run the downloader. It is idempotent — meetings already on disk are skipped via per-folder `done.flag`s.

```bash
python3 /Users/loudalo/Downloads/zoom-recap-sandbox/fetch_recording.py
```

Exit codes you must respect:

- `0` — batch finished cleanly. Continue.
- `2` — config / auth / unrecoverable error. **Stop.** Report the stderr to the user and exit. Do not attempt to continue without recordings.
- `75` — at least one meeting still has files processing on Zoom's side; the rest were downloaded normally. **Continue** to step 0b — process whatever IS ready. The unready ones will be picked up next run.

#### 0b. Discover sessions that need recapping

First, read the `OUTPUT_ROOT` from the sandbox's `.env` file to find where recordings were downloaded. The default is `/Users/loudalo/Downloads/zoom-recap-sandbox/zoom` but the user may have changed it.

```bash
grep '^OUTPUT_ROOT=' /Users/loudalo/Downloads/zoom-recap-sandbox/.env | cut -d= -f2
```

Each downloaded meeting lives in `<OUTPUT_ROOT>/<YYYY-MM-DD>_<HHMM>_<meetingid>/`. A meeting is **ready to recap** when its folder contains `done.flag` (download complete) but does **not** contain `recap.done.flag` (not yet recapped).

List those folders, sorted by date oldest-first:

```bash
ls -1d <OUTPUT_ROOT>/*/ 2>/dev/null \
  | while read d; do
      [ -f "$d/done.flag" ] && [ ! -f "$d/recap.done.flag" ] && echo "$d"
    done \
  | sort
```

If the list is empty: report "No new AIMM sessions to recap." and exit cleanly. Do not invent work.

#### 0c. Process each pending session

For each folder in the list, in order, execute Steps 1 through 8 of this skill with these inputs:

- **Transcript:** `<folder>/transcript.vtt.txt`
- **Chat:** `<folder>/chat.txt` (if it exists — pass it as the optional chat input. If nobody chatted during the session, Zoom produces no CHAT file and the downloader skips it. Proceed without chat in that case.)
- **Session date:** parse from the folder name's `YYYY-MM-DD` prefix. Use this date for the title (`AIMM Recap — Month Day, Year`), the hub topic line, the AIMM Sessions database row, and the local markdown filename. Do NOT use today's date — sessions may be days old when this runs.

**After each session publishes successfully** (Notion subpage created, hub repositioned, AIMM Sessions database synced, local markdown saved), write the flag:

```bash
date '+%Y-%m-%d %H:%M:%S %Z' > <folder>/recap.done.flag
```

The flag is what prevents re-processing on the next scheduled run. Write it last, after every side-effect has succeeded.

**Fail-fast policy.** If any session in the batch fails partway through (Notion error, missing database, validation failure), STOP the entire batch immediately. Do not write `recap.done.flag` for the failed session. Do not continue to the next session. Report which folder failed, what step it was on, and what the error was, then exit. Already-completed sessions in this batch keep their flags. The next run will resume at the failed session.

The reason for fail-fast: a half-published recap is harder to clean up than a delayed one, and a recurring failure across many sessions in one run produces a cascade of broken Notion pages that's painful to unwind.

#### 0d. Summary

After the loop finishes (whether the list was empty, fully processed, or stopped early), print a one-line summary:

```
Bootstrap complete: <N> session(s) recapped, <M> still pending, <K> failed.
```

Then exit. Do not loop back to Step 0a.

### Step 1: Extract Topics

Read the full transcript. Identify 3-5 distinct topic clusters — not by speaker, but by subject. A topic might span multiple speakers and multiple points in the conversation. Look for:

- Tool discoveries or recommendations
- Workflow demonstrations or techniques
- Architecture/design discussions
- Real-world case studies or client stories
- Strategic debates or philosophical discussions
- Member wins or breakthroughs

Consolidate related threads. If three people discussed the same theme at different points, that's one topic, not three. If one person gave a 30-minute demo covering multiple distinct subjects, break it into the sections the audience would naturally care about separately.

### Step 2: Write Each Topic Section

This is the core of the skill. Each section should read like a standalone newsletter article, not a transcript summary. The guiding principles:

**Write like a newsletter, not meeting minutes.** Never write "Lou said X, then Don said Y." Instead, synthesize the discussion into a cohesive narrative about the topic. The reader should learn something valuable even if they weren't in the room. Use participants' names naturally when attributing ideas, discoveries, or memorable framings — but the structure follows the topic, not the conversation order.

**Use the conversation as source material, not as a script.** The transcript is your raw material. Distill it into 500-750 words of substantive content per topic. You're writing *about* what was discussed, using the specifics and examples from the conversation to make the piece concrete and credible.

**Bold opening sentences for skimmability.** The first paragraph of each new point within a section opens with a bolded sentence that works as a scannable thesis statement. Someone skimming the email should get the arc of the discussion from the bold lines alone. If multiple paragraphs support the same point, only the first paragraph gets the bold treatment — the rest flow naturally underneath.

**Match the audience's sophistication.** These aren't beginners. They're domain experts learning to integrate AI. Don't over-explain concepts they already know. Do explain connections they might not have made.

### Voice and Tone

The recap should feel like a sharp, well-informed colleague telling you what you missed — not a corporate communications department summarizing a meeting. Six principles:

1. **Dense per sentence.** Pack meaning. Trust the reader to keep up. Don't dilute a strong observation with three qualifiers and a softening clause.

2. **Lead with the point, not the setup.** No throat-clearing. Don't write "It's worth noting that in today's session, an interesting discussion emerged around..." Write the point. The reader will decide if it's interesting.

3. **Conversational but substantive.** The tone should feel like a smart friend explaining something over coffee — but a friend who did the homework. Accessible doesn't mean shallow.

4. **Take positions in hot takes.** The value-add callouts are the place to have an opinion. Don't hedge with "it remains to be seen" or "only time will tell." Stake a claim. The reader can disagree — that's part of the value.

5. **Use concrete specifics.** Names, numbers, tool names, exact techniques. "Michael's system generates 43 insights per run" is better than "the system generates many insights." The transcript is full of specifics — use them.

6. **Treat the reader as a peer.** No condescension, no over-explaining, no "you might be wondering." Assume they're competent adults who opted into a mastermind because they're serious about this.

### Step 3: Add Value Beyond the Conversation

This is what separates a recap from meeting minutes. For each topic section, use editorial judgment to add one of these (not all — pick the one that fits):

**🔥 Hot Take** — A provocative, opinionated "here's what this actually means" paragraph. Should make the reader think "huh, I hadn't considered that." Takes a position. Connects the discussion to a bigger trend, a market implication, or an uncomfortable truth the group danced around. Format as a blockquote callout.

**💡 What This Means for You** — A practical translation for the reader. "You don't need to build the thing we discussed — here's the minimum viable version of this idea applied to your practice." Bridges the gap between "interesting discussion" and "thing I can act on Monday morning." Format as a blockquote callout.

**Go Deeper (resources)** — Researched links, books, tools, or references that extend the conversation. Use web search to find real, current resources — don't make up URLs. Include brief descriptions of what each resource offers. Format as a bulleted list under a bold "Go Deeper:" header.

When a chat transcript is available, pull any links, tool recommendations, or resource URLs shared there into the appropriate "Go Deeper" sections. Attribute them (e.g., "shared by Don in the chat").

### Step 4: Write the Structural Elements

**Pull quote:** Find the single most memorable, tone-setting line from the transcript. It should capture the energy or spirit of the session. Format as a blockquote with attribution at the top of the document.

**"This Week in 30 Seconds":** Write 4-5 bullet points — one per topic section — that let someone scanning their inbox decide which sections to read. Each bullet should be one bolded phrase followed by a short dash and a one-line summary.

**Community Corner:** Highlight 2-4 member contributions worth spotlighting — a clever technique someone shared, a client win, an idea that deserved more airtime, a tool recommendation from the chat. Each gets a bolded opening sentence and a short paragraph. This section celebrates the community and gives quieter members visibility.

**"Try This Before Next Session":** One concrete exercise the reader can do in 15 minutes. It should connect directly to something discussed in the session — ideally the most universally applicable technique or insight. Write it as a specific, step-by-step mini-exercise, not a vague encouragement.

### Step 5: Generate Prompt Templates (Golden Nuggets)

After writing the topic sections and structural elements, scan the full recap for moments that can be converted into reusable AI prompt templates — prompts the membership would actually paste into Claude and use repeatedly on their own problems.

**The goal:** Extract the highest-leverage techniques, frameworks, and thinking moves from the discussion and package them as ready-to-use prompt templates. Not every session will produce these. Some sessions are heavy on demos, status updates, or philosophical discussion that don't translate into a repeatable prompt. That's fine — the rubric below exists to prevent forcing it.

#### Where to Look for Candidates

- A technique someone demonstrated live (e.g., "ask Claude to reverse-engineer your thought process")
- A reframe or mental move that shifted the conversation (e.g., "stop asking for better answers, start asking why no answer works")
- A multi-step process someone walked through that can be generalized (e.g., perspective explosion, second-order cascade mapping)
- A system prompt modification or slash-command idea someone shared
- A novel way of structuring AI interaction that produced a noticeably better result than the default approach
- Anything that made the room go "oh, I want to try that"

#### Where NOT to Look

- Generic prompting advice that's already well-known ("be specific," "give examples," "assign a role")
- Tool-specific workflows that only work with one product (unless the prompt itself is the transferable part)
- Insights that are interesting to *read about* but don't translate into something you'd *paste into an AI*
- Workflow automations, API integrations, or code-level techniques — those belong in the topic section, not a prompt template

#### The Inclusion Rubric

Score each candidate prompt on five dimensions. Each dimension is binary — it either passes (1) or fails (0).

| Criterion | Pass (1) | Fail (0) |
|---|---|---|
| **Actionable** | Member can paste it into Claude and get useful output in under 5 minutes, with no setup beyond filling in bracketed variables | Requires external tools, prerequisite knowledge, or multi-session setup before it produces value |
| **Discussion-native** | The prompt encodes a specific technique, reframe, or process that emerged from *this* session's conversation — not a generic best practice you could find in any prompting guide | Could have been written without attending the session; reads like standard prompting advice with a coat of paint from the discussion topic |
| **Audience-calibrated** | A knowledge entrepreneur (coach, consultant, course creator, thought leader) would recognize this as directly relevant to their work — building IP, serving clients, creating content, developing frameworks | Too technical (requires coding), too niche (only applies to one member's situation), or too abstract (reads like an academic exercise) |
| **Non-obvious** | The prompt teaches the member to interact with AI in a way they probably wouldn't have discovered on their own — a structural move, a counterintuitive sequence, a reframe that changes what the AI produces | The member would likely arrive at this approach independently; the prompt is just a cleaner version of what they'd already do |
| **Reusable** | Works across different topics, client situations, or business problems — the member will use this more than once | Only useful for the specific example discussed in the session; a one-shot exercise disguised as a template |

**Scoring process:** For each candidate, run the rubric explicitly. Write out the score for each dimension in your working notes (not in the output). A prompt must score **4 or 5 out of 5** to be included.

**Volume guidance:**

- **Target: 1–3 prompts per recap.** Most sessions will yield 1–2 strong candidates. A session with a guest speaker or a deep methodology walkthrough might yield 3.
- **Minimum: 0.** If no candidate reaches the 4/5 threshold, omit the section entirely. No filler. No "here's a prompt just to have one." The recap is already valuable without it — the "Try This" exercise fills the actionability role.
- **Maximum: 3.** Even a rich session caps at 3 prompts. More than that dilutes the signal and the member won't try any of them.

#### How to Write the Prompt Template

Each included prompt gets:

1. **A descriptive title** — names the technique, not the topic. "The Belief Resistance Diagnostic" not "Prompt About Dirk's Experience." Use title case.
2. **One-line origin note** — which discussion moment it came from, in italics. Connects the prompt back to the session so members understand the context and can re-read the relevant section. Format: `*From: [brief reference to the discussion moment or speaker]*`
3. **The prompt itself** — formatted as a fenced code block so members can copy-paste cleanly. Use `[BRACKETED ALL-CAPS VARIABLES]` for anything the member fills in. Include brief inline comments where variables aren't self-explanatory (e.g., `[YOUR NICHE — e.g., executive coaching, leadership development, sales training]`).
4. **No explanatory essay.** The prompt should be self-contained. If it needs a paragraph of explanation to make sense, it's not ready for inclusion — either simplify it or cut it.

#### Prompt Design Principles

- **Front-load context, back-load instructions.** The member's filled-in variables (topic, audience, niche) go first, then the AI's instructions. This mirrors how Claude processes — context first, task second.
- **Use numbered steps in the prompt when the technique has a specific sequence.** The sequence *is* the IP — it's the part the member wouldn't have known to do on their own.
- **Include the "why" inside the prompt when it changes the AI's behavior.** If the prompt says "Don't give me your best answer upfront" — that's an instruction that works better when the AI understands the reasoning. A brief inline note like "I want to see the thinking, not just the conclusion" costs almost nothing and improves output quality.
- **Keep prompts between 80–250 words.** Under 80 and there's not enough structure to encode a real technique. Over 250 and the member won't read it carefully enough to customize the variables.
- **Test mentally before including.** Before finalizing, imagine a specific AIMM member (a coach, a consultant) pasting this prompt with their own variables filled in. Does the output they'd get back feel genuinely useful — something they'd act on or share with a client? If you can't picture that clearly, the prompt isn't ready.

### Step 6: Distribute Prompt Templates

When prompts pass the rubric in Step 5, they need to be distributed through two channels beyond the recap itself: as Claude command files (for direct use) and as rows in the AIMM Prompt Library database in Notion (for browsing and discovery). Skip this step entirely if no prompts passed the rubric.

#### 6a. Generate Claude Command Files

For each prompt that passed the rubric, produce a standalone `.md` command file. These files are designed to be placed in a member's `~/.claude/commands/` directory (or the AIMM GitHub repo's `commands/` directory), making each prompt available as a slash command.

**Command file format:**

```markdown
# [Prompt Title]

[One-sentence description of what this command does and the technique it's based on.
Include attribution to the session or speaker.]

---

[The prompt body, identical to the recap version but with one modification:
replace the first [BRACKETED VARIABLE] with $ARGUMENTS so the member can pass
their input directly when invoking the command.]

If no [topic/idea/input] was provided above, ask me to describe it before proceeding.

[Rest of the prompt steps, exactly as in the recap]
```

**Naming convention:** All AIMM prompt commands live in an `aimm/` subdirectory, which creates a colon-separated namespace automatically. Filename is the prompt title in kebab-case with `.md` extension.

**Directory structure:**
```
commands/aimm/
  perspective-explosion.md   →  /aimm:perspective-explosion
  second-order-cascade.md    →  /aimm:second-order-cascade
  voice-activator.md         →  /aimm:voice-activator
```

Members type `/aimm:` to see the full list of available AIMM prompts. For the GitHub repo, the path is `commands/aimm/`. For personal use, the path is `~/.claude/commands/aimm/`.

**Key design rules for command files:**

- **Use `$ARGUMENTS` for the primary input variable.** This lets members type `/aimm:perspective-explosion My idea is that coaching certifications are becoming worthless` and have it flow directly into the prompt. Only the *first* and most important variable gets this treatment — additional variables (audience, niche, etc.) stay as `[BRACKETED]` fill-ins within the prompt body.
- **Include a fallback.** Add a line after the `$ARGUMENTS` injection: "If no [input type] was provided above, ask me to describe it before proceeding." This handles the case where a member invokes the command without arguments.
- **Keep the title and one-line description at the top.** Commands benefit from a brief header that reminds the member what this does — especially when they're scanning a list of available commands.
- **Don't include the origin note.** The `*From: [session reference]*` line belongs in the recap, not the command file. The command should be self-contained.

**Update the index command.** After generating new command files, update `aimm/help.md` — the `/aimm:help` command that lists all available AIMM prompts. Add the new prompt(s) to the appropriate category section with the command name, one-line description, and session date. If a category doesn't exist yet, add it. This is the in-context discovery mechanism — members type `/aimm:help` to see the full menu.

**Deliverable:** Save all command files (including the updated `help.md`) to a clearly labeled output folder (e.g., `aimm-prompt-commands/aimm/`) alongside the recap markdown. Notify the user: "Command files ready for GitHub — [list filenames]. Drop the `aimm/` folder into `commands/` in the AIMM repo or into `~/.claude/commands/` for personal use."

#### 6b. Sync to the AIMM Prompt Library (Notion)

After generating command files, add each prompt as a row in the **AIMM Prompt Library** database in Notion. This database lives under the AIMM Report Hub and serves as the browsable index of all prompts across all sessions.

**How to find the database:** Search Notion for "AIMM Prompt Library". It should exist as a child of the AIMM Report Hub. If it cannot be found, notify the user: "Could not locate the AIMM Prompt Library database — please check that it exists under the Report Hub."

**Fields for each row:**

| Field | Type | Value |
|---|---|---|
| **Prompt Name** | Title | The prompt title (e.g., "The Perspective Explosion") |
| **Session Date** | Date | The session date (e.g., 2026-03-19) |
| **Source Topic** | Text | The recap section title this prompt came from |
| **Category** | Select | One of: Thinking, Analysis, Writing, Reframe, Ideation, Meta |
| **Command** | Text | The namespaced slash command (e.g., `/aimm:perspective-explosion`) |
| **Prompt Text** | Text | The full prompt template with [VARIABLES] |
| **Recap Link** | URL | The Notion URL of the recap page |
| **Rubric Score** | Number | The score (4 or 5) |

**Category assignment guide:**

- **Thinking** — Prompts that change *how* you approach a problem (perspective shifts, paradigm analysis, cognitive fingerprinting)
- **Analysis** — Prompts that map, decompose, or evaluate something (second-order effects, competitive analysis, cascade mapping)
- **Writing** — Prompts that produce or improve written content (voice activation, content drafts, editorial critique)
- **Reframe** — Prompts that diagnose *why* you're stuck and shift the frame (belief resistance, assumption surfacing)
- **Ideation** — Prompts that generate novel options or possibilities (brainstorming, tournament-style idea generation)
- **Meta** — Prompts about prompting itself (prompt reflection, prompt improvement, self-audit)

**Confirm to the user:** "Added [N] prompts to the AIMM Prompt Library: [list titles with categories]."

### Step 7: Handle Links from Chat Transcript

If a chat transcript is provided, create a **"Links Shared in Chat"** section near the bottom (before the Prompt Templates and CTA) that collects all URLs, tool names, and resource links shared during the session. Format as a bulleted list with bold tool/resource names, brief descriptions, and clickable links. This section serves as a quick-reference bookmark list for attendees.

### Step 8: Publish to Notion (when requested)

If the user wants the recap posted to Notion, follow this sequence carefully. The goal is zero data loss and no duplicate pages.

#### 8a. Locate or create the hub

Search Notion for "AIMM Report Hub". If found, retrieve its page ID and URL — you'll need them for navigation links and database lookup. If not found, create the hub page with an icon (📋), a one-line description of the series, and the tagline "Read the latest, or start from the beginning."

#### 8b. Pre-flight: check for an existing recap page

Before creating anything, search Notion for a page whose title matches the expected title for this session (e.g., "AIMM Recap — March 19, 2026"). Search both by title and by scanning child pages of the hub.

**If a matching page is found — stop and present options to the user:**

> ⚠️ A recap page for this date already exists: "[title]" (last edited [date]).
>
> How would you like to proceed?
> 1. **Overwrite** — replace the existing content (old content will be preserved in a collapsed backup toggle at the top of the page before anything is deleted)
> 2. **Append** — add the new draft as a clearly dated section at the bottom of the existing page
> 3. **Skip Notion** — save the markdown locally only, leave the existing Notion page untouched
> 4. **Abort** — stop here, do nothing

Wait for explicit user choice before proceeding. Do not default to any option.

**Overwrite path:** Before replacing any content, prepend a collapsed toggle block titled "📦 Backup — [current timestamp]" containing the full previous page content. Only after confirming the backup toggle exists should you replace the body with the new recap.

**Append path:** Add a horizontal divider, then a clearly labeled heading: "--- Draft added [date] ---", then the new content below it. Do not modify any existing content above the divider.

#### 8c. Create the recap subpage (new page path only)

Create the page as a child of the hub. Title: `AIMM Recap — [Month Day, Year]` with optional subtitle (e.g., `| Special Guest: Michael Simmons`). Add a 📋 icon. Write the full recap content.

**IMPORTANT — Reverse-chronological ordering:** The hub lists recaps in **reverse-chronological order** (newest at the top of each year section). Notion's `create-pages` API appends new child pages to the *bottom* of the parent's content by default. You **must** reposition the new entry after creation using the technique in step 8d.

#### 8d. Position the page on the hub and add the topic summary

After the subpage exists, update the AIMM Report Hub page to **insert** the new recap's `<page>` block and its italic topic summary at the correct chronological position — **above all existing recaps in the current year section** (i.e., immediately after the `## [Year]` heading and its `<empty-block/>`). The hub is reverse-chronological: newest first.

##### Repositioning the page (required)

Because `create-pages` appends the child page to the bottom of the hub content, you need a **single `update_content` call with two operations** to fix the ordering:

1. **Insert at top:** Match the first existing recap entry in the year section and prepend the new page + CoD summary above it.
2. **Remove from bottom:** Match the auto-appended `<page>` block at the bottom and remove it.

Both operations **must be in the same `content_updates` array** so Notion sees the page reference is being moved, not deleted. If you remove the bottom reference in a separate call, Notion will interpret it as a child page deletion and either error (`allow_deleting_content` required) or trash the actual page.

**Example — single atomic call:**

```json
{
  "command": "update_content",
  "content_updates": [
    {
      "old_str": "## 2026\n<empty-block/>\n<page url=\"https://www.notion.so/[PREV_FIRST_ID]\">[Previous first entry title]</page>",
      "new_str": "## 2026\n<empty-block/>\n<page url=\"https://www.notion.so/[NEW_ID]\">[New recap title]</page>\n*CoD topic summary here*\n<page url=\"https://www.notion.so/[PREV_FIRST_ID]\">[Previous first entry title]</page>"
    },
    {
      "old_str": "[last content block before the appended page]\n<page url=\"https://www.notion.so/[NEW_ID]\">[New recap title]</page>",
      "new_str": "[last content block before the appended page]"
    }
  ]
}
```

**Key safeguards:**
- Always fetch the hub page **after** creating the subpage to get the exact current content — titles, escaped characters, and surrounding blocks must match exactly.
- The second operation's `old_str` must include at least one block *above* the `<page>` tag to ensure a unique match (the page title alone will appear at both the top and bottom of the content after the first operation runs).
- If a previous failed attempt left a dangling CoD summary orphaned at the bottom, include it in the second operation's `old_str` to clean it up in the same call.
- **Never use `allow_deleting_content: true`** when editing the hub. This flag deletes child pages (sends them to Notion trash), not just reference text from the page body. It is destructive and hard to reverse.

##### Writing the topic summary

**What it looks like on the hub:**

```
<page url="https://www.notion.so/[ID]">AIMM Recap — [Date]</page>
*Named entity: key fact — elaboration · item 2 · item 3 · item 4 · item 5*
```

**How to write the summary — Chain of Density method:**

Use a two-step Chain of Density (CoD) process. The goal is maximum information density in minimum words — every noun earning its seat.

**Step 1: Write a ≤150-word dense paragraph**

Read the published recap and write a single paragraph, hard cap 150 words. Run 3 CoD passes:
- Pass 1 (sparse): write a plain ~80-word summary of what happened
- Pass 2 (named entities): replace generic references with specific names, tools, numbers, and frameworks — "a voice agent" becomes "NHS DORA voice agent: 71% reduction in patient follow-up wait times"
- Pass 3 (mechanism detail): add the *why it matters* and *how it works* where space allows

**Step 2: Compress into dot-separated format**

These are **memory triggers and topic headlines**, not descriptions. Strip the paragraph down to 4–5 dot-separated items. Full sentences not required — drop articles, cut conjunctions, compress clauses to their load-bearing core.

Format: `*Named entity: key fact — elaboration · item 2 · item 3 · item 4*`

- Separate with middle dots (·), not commas or dashes
- Use em dash (—) for payload within an item
- Wrap the full line in italics: `*...*`
- Target: **~75 words** for the final line
- Default to 4 items; use 5 when the session was dense or had a standout thread worth surfacing

**The target feel:** specific enough that someone who was in the room recognizes it immediately; intriguing enough that someone who wasn't wants to click in. Not a description — a signpost.

##### Technical constraints

- The italic paragraph is a *separate Notion block* from the `<page>` block above it — Notion doesn't support inline text appended to a `<page>` block. A small visual gap between the title and the summary is unavoidable with native page links and is acceptable.
- Pipe characters in titles (e.g., `\|`) must be escaped as `\\|` in the `old_str` to match exactly.

#### 8e. Add navigation links

Add a footer navigation block at the very bottom of the subpage:
- First page in series: `[🏠 Report Hub](hub-url) · [Next Recap →](next-url)`
- Middle pages: `[← Previous Recap](prev-url) · [🏠 Report Hub](hub-url) · [Next Recap →](next-url)`
- Latest page (most common): `[← Previous Recap](prev-url) · [🏠 Report Hub](hub-url)`

To identify the previous recap: scan the hub's child pages sorted by creation date, or search for the most recent "AIMM Recap —" page before this session's date.

#### 8f. Update the previous recap's navigation

Fetch the previous recap page and update its footer nav to add the forward link to the newly created page. If the previous page has no footer nav block yet, add one.

**Edge case:** If the previous page cannot be identified with confidence, skip this step and notify the user: "Could not identify the previous recap page — you may need to update its navigation manually."

#### 8g. Sync the AIMM Sessions database

After the Notion subpage is created or updated, sync the record in the **AIMM Sessions** Notion database:

1. Search the database for a row whose **Name** field matches this session's date (search flexibly — "March 19", "Mar 19", "March 19, 2026" should all match).
2. **If a matching row is found:**
   - Set the **Report** field (URL type) to the Notion subpage URL
   - Set the **Topics** field (text type) to the same CoD dot-separated summary from step 8d, in **plain text without italics** (e.g., `GEO 3-layer authority architecture: canon, frameworks, diagnostics — three retrieval signals · LinkedIn's quiet LLM indexing shift: professional authority now readable by AI crawlers · ...`)
3. **If no matching row exists:** Create a new database entry with:
   - **Name**: the session date formatted consistently with existing rows (e.g., "AIMM Session — March 19, 2026")
   - **Report**: the Notion subpage URL
   - **Topics**: same CoD dot-separated plain text summary from step 8d (no asterisks)
   - **Replay**: leave blank — user will add the Zoom link separately
4. Confirm to the user: "✅ AIMM Sessions database updated for [date] — Report linked, Topics filled."

**Important:** The Topics field in the database and the italic summary on the hub are the **same content** — the CoD ~75-word dot-separated summary from step 8d. The only difference is formatting: hub uses `*...*` italics, database is plain text.

**Edge case — multiple matching rows:** List them and ask the user which to update before touching anything.

**Edge case — database not found:** Skip this step and notify: "Could not locate the AIMM Sessions database in Notion — please update the Report field manually."

#### 8h. Save local markdown copy

Always save a local markdown copy regardless of whether Notion publishing succeeds or is requested. Save to `~/Documents/AIMM Recaps/` (or ask the user for a preferred folder on first use). Filename: `AIMM-Recap-YYYY-MM-DD.md`. If that filename already exists, save as `AIMM-Recap-YYYY-MM-DD-v2.md` — never silently overwrite.

## Output Format

The final markdown structure:

```
# [Community Name] Recap — [Date]
### [Optional subtitle, e.g., "Special Guest: Name"]

> *"Pull quote here."*
> — Attribution

---

### This Week in 30 Seconds

- **Topic 1** — one-line summary
- **Topic 2** — one-line summary
- ...

---

## [Topic 1 Title]

**Bolded opening sentence.** Rest of paragraph...

[Content sections with bold lead-ins for each new point]

> 🔥 **Hot Take: [Title]**
> [or 💡 **What This Means for You**]
>
> Callout content...

**Go Deeper:**
- **Resource** — description: [link](url)

---

## [Topic 2 Title]
...

---

## Community Corner

**Member highlight.** Description...

---

## Links Shared in Chat (if chat transcript provided)

- **Tool Name** — description: [link](url)

---

## ⚡ Try This Before Next Session

**Specific exercise.** Step-by-step instructions...

---

## 🧰 Prompt Templates from This Session (if prompts pass the rubric)

Prompts you can paste directly into Claude. Fill in the [BRACKETED] variables for your context.

### [Prompt Title]
*From: [brief reference to the discussion moment]*

```
[The actual prompt template with [VARIABLES]]
```

### [Prompt Title 2]
*From: [brief reference]*

```
[Second prompt template]
```

---

*Next session: [date/info]*

---
[← Previous](url) · [🏠 Report Hub](url) · [Next →](url)
```

## Common Pitfalls

- **Don't write meeting minutes.** If your output reads like "First, Lou discussed X. Then Don shared Y. Next, Elizabeth asked about Z" — stop and rewrite. The reader shouldn't be able to reconstruct the conversation timeline from your recap.
- **Don't add value-add callouts to every section.** Pick the 2-3 where a hot take or resource list genuinely adds something. Forced insight is worse than no insight.
- **Don't over-research.** The value-adds should enhance, not overwhelm. One or two researched resources per section is plenty. The goal is "here's where to go deeper," not "here's a literature review."
- **Don't forget the chat transcript.** If the user provides one, mine it thoroughly — links, reactions, ideas, attributions. Chat transcripts often contain the most concrete, linkable resources from the session.
- **Don't use generic bolded openers.** "This was an interesting discussion" is not a bolded lead-in. Each bold sentence should be a specific, scannable claim: "Michael's system generates 40+ insights per run, then pits them against each other in a tournament."
- **Don't publish to Notion without the pre-flight check.** Always search for an existing page before creating one. A duplicate is harder to clean up than a two-second search.
- **Don't overwrite silently.** If a page exists, stop and ask. The backup toggle must exist before any content is replaced.
- **Don't skip the hub topic summary.** Every new recap published to Notion gets an italic dot-separated topic line below its hub entry (step 8d). It takes one targeted `update_content` call and it's the first thing readers see when scanning the archive.
- **Don't skip the database sync.** The AIMM Sessions database is the index that links the hub, the HTML page, and the Notion subpages. Every published recap should update it.
- **Don't skip prompt distribution.** If prompts pass the rubric and appear in the recap, they also need command files and Notion library rows (Step 6). The recap is the discovery moment; the command files and library are where prompts earn their longevity. All three layers should stay in sync.
- **Don't force prompt templates.** If no discussion moment passes the 4/5 rubric threshold, omit the section entirely. A mediocre prompt that nobody uses is worse than no prompt at all. The "Try This" exercise already provides actionability — prompt templates are a bonus when the material warrants it, not a mandatory fill.
- **Don't confuse "Try This" with "Prompt Templates."** They serve different purposes. "Try This" is a conceptual exercise that teaches a thinking approach — it might involve multiple tools, a specific scenario, or steps that aren't all AI prompts. "Prompt Templates" are copy-paste-ready AI interactions. Both can exist in the same recap. Neither replaces the other.
