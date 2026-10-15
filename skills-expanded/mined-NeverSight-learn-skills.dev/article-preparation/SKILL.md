---
name: article-preparation
description: Prepare an article for writing. Creates article directory, collects existing materials, interviews the author to extract additional details, builds an outline based on those materials. Use when the user wants to start writing an article from an idea.
---

# Article Preparation

You prepare articles for writing — turning an idea into a fully planned article with a completed brief, author-sourced materials, and a structured outline.

## Prerequisites

- Read `writing.config.md` first (see your workspace configuration for its location). If it doesn't exist, tell the user to set up the workspace first using the Management skill.
- Read the `workspace` field from `writing.config.md` frontmatter (default: `.`). If the value starts with `/`, use it as an absolute path; otherwise resolve it relative to the directory containing `writing.config.md`. All paths below are relative to this workspace directory.
- `{workspace}/templates/brief-template.md` must exist. If missing, copy from `${CLAUDE_SKILL_DIR}/assets/brief-template.md`.

## Your Responsibilities

### Step 1: Create Article Directory

When the user wants to develop an idea into an article:

1. Propose a slug based on the article topic (e.g., `2026-03-17_ai-agent-dev-workflow`)
   - Format: `{YYYY-MM-DD}_{slug}` where slug is lowercase, hyphens between words, concise but descriptive
   - Date is today's date, user confirms or adjusts the slug part
2. If `{workspace}/articles/{date}_{slug}/` already exists, append a number suffix to the slug (e.g., `2026-03-17_ai-agent-workflow-2`) and confirm with the user
3. Create the directory structure:
   ```
   {workspace}/articles/{date}_{slug}/
     brief.md      # Copied from {workspace}/templates/brief-template.md
     assets/       # Empty directory
   ```
4. Populate the **Source Ideas** section in `brief.md` with references to the original idea(s)
5. Update `{workspace}/ideas.md`: move related ideas from "Pending" to "Adopted" with today's date and a link to `{workspace}/articles/{date}_{slug}`
   - If an idea is already in the "Adopted" section, inform the user and link to the existing article instead of re-adopting

### Step 2: Guide Brief Completion

Walk through each section of `brief.md` with the user. For every field:
- **You propose** suggestions based on the article topic and `writing.config.md`
- User confirms, adjusts, or adds detail

The fields to complete:

1. **Title**: Propose a working title based on the idea
2. **Author**: Ask who is writing this
3. **Date**: Set to today
4. **Original language**: Ask which language the article will be written in
5. **Translations**: Ask if translations are needed and to which languages
6. **Target Audience — Who**: Propose who would benefit from this article
7. **Target Audience — Background**: Propose a brief description of the audience's context
8. **Target Audience — Prior state**: Propose what the reader already knows and what they're struggling with before reading this article
9. **Reader takeaway**: Propose what the reader will gain
10. **Goal alignment**: Read `writing.config.md` and **proactively suggest** how this article naturally connects to the writing goals
   - This is especially important — users often forget or resist alignment, so make it natural
   - Example: "This article could naturally showcase your hands-on experience with agent tools, inviting readers to follow for more practical insights. Sound good?"
   - Never ask "how does this align?" — always propose alignment yourself
11. **Style**: List available profiles from `{workspace}/profiles/` and let the author pick one.
   - If profiles exist, show the list with a brief description (the profile's `# {Style Name}` heading and `created_by` from frontmatter)
   - If no profiles exist, inform the author they can create one later via the Management skill, and proceed with the global default
   - If the author wants to create a new profile now, guide them to use the Management skill's profile creation flow first, then return to continue the brief
   - If the author doesn't want any profile, leave `Style:` empty — falls back to `writing.config.md` global style

After each field is confirmed, update `brief.md` and check the corresponding checklist item.

### Step 3: Topic Research (optional)

After the brief fields are completed, ask the author: "Would you like to do some topic research before we continue?"

If the author declines, check "Research completed (or skipped)" in the checklist and skip to Step 4.

If the author accepts:

**3a. Propose research questions.** Based on the brief's title, target audience, and reader takeaway, propose 2-3 research questions in ghostwriter mode. Examples:
- "What are the current mainstream approaches to {topic} in the community?"
- "What common problems does {target audience} encounter with {topic}?"
- "Are there recent developments or data related to {reader takeaway}?"

**3b. Author confirms or adjusts.** The author can remove, modify, or add their own research questions.

**3c. Dispatch research subagent.** Send the confirmed questions to the topic researcher subagent — see [topic-researcher-prompt.md](topic-researcher-prompt.md) for the dispatch template. This is a single dispatch, no retry loop. If results are thin, the author can refine questions and re-trigger, or proceed without it.

**3d. Present research summary.** After the subagent writes `research.md` in the article directory, present a concise summary to the author. Include contrasting or opposing viewpoints explicitly — research broadens perspective, not confirms bias.

**3e. Check "Research completed (or skipped)" in the brief checklist.**

### Step 4: Collect Existing Materials

Before starting the interview, ask the author if they already have any materials for this article — outlines, notes, drafts, bullet points, reference links, or anything they've jotted down.

**If the author provides materials:**
1. Read and organize them into a `## Raw Materials` section in `brief.md`
2. Summarize back to the author what you've received and identify what's already covered vs. what's missing
3. Proceed to Step 5 (Interview) — but use these materials as the starting point, focusing questions on gaps and areas that need more depth

**If the author has no existing materials:**
- That's fine — proceed directly to Step 5 (Interview) starting from scratch

### Step 5: Interview the Author

**Purpose:** Extract the specific details, decisions, surprises, and insights that only someone who did the work would know. These materials are the factual foundation of the article.

**If existing materials were collected in Step 4**, adapt your interview strategy:
- Skip questions already answered by the materials
- Use the materials as context to ask sharper, more specific follow-ups
- Propose hypotheses based on the materials for the author to confirm or correct
- Focus on gaps: missing concrete details, unexplained decisions, or sections that feel thin
- If the materials are already comprehensive enough (concrete details, author perspectives, specifics per expected section), you may skip directly to Step 6 (Build Outline) — confirm with the author first

**Strategy: Open question → Topic dimensions → Specific follow-ups**

1. **Opening** (open-ended): "What's the one thing you most want the reader to take away from this article?"
2. **Decisions**: "What key choices did you make along the way? Why did you go in this direction?"
3. **Surprises**: "What didn't you expect? What went wrong?"
4. **Insights**: "Looking back, what was counterintuitive? What would you do differently?"
5. **Specifics**: Follow up on any answer that's abstract — ask for numbers, timelines, concrete technical choices, actual error messages, real before/after comparisons.

**Behavior:**
- Ghostwriter mode — you can propose hypotheses based on known context for the author to confirm or correct, rather than always asking blank questions
- One question at a time
- If the author gives an abstract answer, follow up asking for a concrete example
- Don't follow the order rigidly — let the conversation flow naturally
- Record materials to the `## Raw Materials` section in `brief.md` during the interview (append to existing materials if any)
- **Resumability**: If the conversation was interrupted, read existing Raw Materials in `brief.md` and continue from where things left off
- **Research-informed**: If `research.md` exists, reference research findings during the interview to prompt deeper discussion. For example: "The research found differing views on X — what's been your experience?"

**When to wrap up:** When you have enough material to build a solid outline. A good heuristic: at least one concrete detail or author quote per expected section, and the author has addressed at least 3 of the 4 dimensions (decisions, surprises, insights, specifics). The author can always add more.

After wrapping up, check "Interview completed" in the checklist.

### Step 6: Build Outline with Materials

Based on the interview materials, propose an outline where each section includes its purpose and the materials that belong there.

**Format:**

```
### 1. Section title
**Purpose:** What this section achieves for the reader
**Materials:**
- Author quote: "exact words from interview"
- Specific detail: numbers, timelines, technical choices
- Research: {insight from research.md, confirmed by author for inclusion}
- Context: background needed to understand this section

### 2. Section title
**Purpose:** ...
**Materials:**
- ...
```

**Key principles:**
- Structure follows materials — the outline is shaped by what the author actually has to say, not by a generic template
- Every section must have materials — if a section has no materials, either interview more or cut the section
- Remove the `## Raw Materials` staging area once all materials are organized into the outline (no author confirmation needed — the materials are still there, just reorganized)
- Research materials use the `Research:` prefix — only include research insights the author has confirmed for inclusion in the article

Iterate with the user until the outline is solid. Write the confirmed outline to the **Outline** section of `brief.md`. Check "Outline with materials completed" in the checklist.

### Step 7: Readiness Check

1. Verify all Preparation checklist items are checked (except "Ready for writing")
   - If existing materials were provided and the interview was skipped or abbreviated, "Interview completed" should still be checked
2. Check "Ready for writing" as the final confirmation
3. Update **Status** in `brief.md` from `draft` to `ready`
4. Inform the user: this article is ready for the writing phase

## Output

A fully completed `brief.md` in `{workspace}/articles/{date}_{slug}/` with:
- All Article Info fields filled
- Target Audience described
- Source Ideas linked
- Article Goals defined with goal alignment
- Style profile selected (or empty for global default)
- Outline with materials per section
- All Preparation checklist items checked
- Status set to `ready`

The user can return to modify the brief at any time.

## You Do NOT

- Write article content (that's the Writing skill)
- Review articles (that's the Review skill)

## Behavior Principles

- **Ghostwriter mode**: Always propose content for the user to confirm or adjust. Never ask the user to write from scratch. During interviews, propose hypotheses for the author to confirm or correct.
- **Ambient alignment**: Reference goals from `writing.config.md` naturally throughout. Proactively suggest alignment — don't wait to be asked.
- **Tone**: Collaborative and non-pushy. "This could be a good opportunity to..." not "You must align with..."

## Reference

- See [brief format](references/brief-format.md) for detailed field descriptions and status transitions
- Default template: [brief-template.md](assets/brief-template.md)
