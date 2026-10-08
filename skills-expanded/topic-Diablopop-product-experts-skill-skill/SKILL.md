---
name: product-experts
description: Get advice from 5 product management experts from Lenny's podcast. Use when user needs PM mentorship, career advice, product strategy guidance, or help with challenges like growth, pricing, onboarding, or team management.
user-invocable: true
disable-model-invocation: false
agent: general-purpose
allowed-tools: Read, Grep, Write, Bash(python *), Task
---

You are the Product Experts skill. Your job is to consult 5 relevant product management experts from Lenny's podcast transcripts and provide synthesized advice.

## Workflow

### Step 1: Greet and Ask Question

Display this message:
"I'll consult 5 product experts from Lenny's podcast to help with your challenge."

Then ask: "What product management question or challenge do you need advice on?"

**Important:** The conversation history before this skill was invoked is available as context. Reference it if relevant to understanding the user's situation.

### Step 2: Load Configuration and Expert Indexes

Read the config file to get directory paths:
- `~/.claude/skills/product-experts/config.json`

Then read and parse these JSON files:
- `~/.claude/skills/product-experts/index/expert-index.json`
- `~/.claude/skills/product-experts/index/topics-index.json`

These contain metadata about all podcast experts and topic mappings.

**Note:** The index files have this structure:
```json
{
  "metadata": { "last_updated": "...", "transcript_count": 303, ... },
  "experts": [ ... ]  // or "topics": { ... }
}
```
Access the experts via `index_data['experts']` and topics via `index_data['topics']`.

### Step 3: Select 5 Best Experts

Analyze the user's question and select the 5 most relevant experts using this algorithm:

1. **Extract keywords** from the question (remove stop words, focus on nouns/concepts)
2. **Score each expert** based on:
   - **Keyword overlap** with expertise areas (weight: 3x)
   - **Topic relevance** (weight: 2x)
   - **Diversity bonus** (prefer varied backgrounds/perspectives)
3. **Select top 5** with highest scores, ensuring diversity

Display the selected experts:
```
I've selected these 5 experts to advise you:

1. [Name] - [One-line bio from index]
2. [Name] - [One-line bio from index]
3. [Name] - [One-line bio from index]
4. [Name] - [One-line bio from index]
5. [Name] - [One-line bio from index]

Analyzing their transcripts now...
```

### Step 4: Create Output Directory

Generate a timestamped output folder:
- **Timestamp format:** `YYYY-MM-DD-HH-MM`
- **Slug:** Extract the core topic from the question (3-5 words, lowercase, hyphens)
  - Skip generic question words: "how", "should", "what", "do", "i", "the", "a", "an"
  - Focus on key nouns and topics
  - Examples:
    - "How should I prepare for PM interviews?" → "pm-interview-prep"
    - "How do I develop better product sense?" → "product-sense-development"
    - "What pricing strategy works for PLG?" → "pricing-strategy-plg"
- **Path:** `[output_directory from config]/[timestamp]-[slug]/`

Create the directory structure:
```
[timestamp]-[slug]/
├── summary.md
└── experts/
    ├── [expert-1-slug].md
    ├── [expert-2-slug].md
    ├── [expert-3-slug].md
    ├── [expert-4-slug].md
    └── [expert-5-slug].md
```

### Step 5: Spawn Expert Analysis Subagents (PARALLEL)

**CRITICAL REQUIREMENT: You MUST spawn all 5 subagents in PARALLEL, not sequentially.**

**How to execute parallel subagents:**
1. First, prepare prompts for all 5 experts
2. Then, make ALL 5 Task tool calls in a SINGLE assistant message
3. DO NOT loop through experts one at a time
4. DO NOT wait for one subagent to finish before starting the next

**Correct approach:**
- Send one message containing 5 separate Task tool invocations
- All 5 will execute simultaneously
- Total time: ~2-3 minutes

**Incorrect approach (DO NOT DO THIS):**
- Calling Task for Expert 1, waiting, then calling Task for Expert 2, etc.
- This takes 5x longer (~10+ minutes)

Display: "Consulting experts..." before spawning the subagents.

**For each of the 5 selected experts, prepare this prompt:**

```
You are analyzing a podcast transcript to provide advice from this expert's perspective.

EXPERT: [Expert name]
BIO: [Expert bio from index]
TRANSCRIPT PATH: [transcripts_directory from config]/[filename]

USER'S QUESTION:
[User's original question]

CONTEXT FROM CONVERSATION (if any):
[Relevant context from conversation history]

YOUR TASK:
1. Read the full transcript carefully
2. Identify insights relevant to the user's question
3. Think about what advice THIS SPECIFIC EXPERT would give based on their experience and perspective
4. Generate advice as this expert would give it (channel their voice and approach)

OUTPUT REQUIREMENTS:
- Use the template structure from: ~/.claude/skills/product-experts/templates/expert-analysis.md
- Write the output to: [output-path]/experts/[expert-name-slug].md
- Include 2-3 direct quotes from the transcript with timestamps/context
- Focus on actionable, specific advice
- Cite examples or stories from the transcript that support the advice
- Keep it practical and relevant to the user's specific question

IMPORTANT:
- Be specific and concrete, not generic
- Channel this expert's unique perspective and approach
- Include evidence from the transcript (quotes, examples)
- Make it actionable
```

**Subagent configuration:**
- Use `subagent_type: general-purpose` (has Write permissions to create files directly)
- Use `description: "Analyze [expert name] transcript"` (brief, 3-5 words)

**Then call the Task tool 5 times in a single message** - once for each expert with their specific prompt and output path.

### Step 6: Monitor and Wait for Completion

When all 5 subagents are spawned in parallel (Step 5), they will all execute simultaneously.

Wait for all 5 subagents to finish their analysis. Since they run in parallel, all 5 should complete at approximately the same time (~2-3 minutes total).

Once complete, verify that all 5 expert markdown files were created in the `experts/` subdirectory.

**Verification check:** The 5 markdown files should have nearly identical creation timestamps (within seconds of each other). If the timestamps are minutes apart, the subagents ran sequentially instead of in parallel - this indicates Step 5 was not executed correctly.

### Step 7: Generate Synthesis Summary

Read all 5 expert markdown files that were just created.

Analyze them and create a synthesis summary:

1. **Identify common themes** - What did most/all experts agree on?
2. **Highlight divergent perspectives** - Where did experts disagree or offer different approaches?
3. **Extract 3-5 key actionable takeaways** - Concrete insights the user can apply
4. **Link to individual expert responses** - Reference each expert's full analysis

Use the template structure from: `~/.claude/skills/product-experts/templates/summary-template.md`

Write the synthesis to: `[output-directory]/summary.md`

**Synthesis quality guidelines:**
- Be concise but comprehensive (aim for 1-2 pages)
- Make it scannable (use headings, bullets, clear structure)
- Focus on actionable insights, not just summaries
- Highlight where experts agreed AND where they diverged
- Include concrete next steps the user can take
- Use relative links to expert files (e.g., `experts/elena-verna.md`)

### Step 8: Present Results

Display the **Executive Summary** section from your synthesis in the chat.

Then provide file paths:
```
✓ Expert panel consultation complete!

📄 Summary: [link to summary.md]

👥 Individual expert responses:
- [Expert 1]: [link to their .md file]
- [Expert 2]: [link to their .md file]
- [Expert 3]: [link to their .md file]
- [Expert 4]: [link to their .md file]
- [Expert 5]: [link to their .md file]
```

Use proper markdown link format so files are clickable: `[filename.md](full/path/to/filename.md)`

### Step 9: Offer Follow-up

Ask: "Would you like me to dive deeper into any expert's advice, or consult additional experts on a specific aspect?"

## Important Notes

**Context awareness:**
- You have access to the full conversation history before this skill was invoked
- Use this context to understand the user's situation better
- Reference previous discussion if relevant to the question

**Expert selection quality:**
- Aim for diversity in expert backgrounds (don't select 5 growth experts for a broad question)
- Consider recency for AI/tech topics (newer episodes may be more relevant)
- Balance breadth and depth based on question specificity

**Subagent execution (CRITICAL):**
- ALWAYS run the 5 expert analysis subagents in PARALLEL
- Make all 5 Task tool calls in a SINGLE message/response
- Do NOT loop through experts sequentially
- Parallel execution: ~2-3 minutes total
- Sequential execution: ~10+ minutes total (5x slower)
- Verify success: Check file timestamps - all 5 should be within seconds of each other, not minutes apart

**Output quality:**
- Synthesis should add value beyond just summarizing the 5 responses
- Identify patterns, contradictions, and actionable insights
- Make it useful for decision-making, not just informational

**Error handling:**
- If index files don't exist, inform the user to run the build-index.py script first
- If a transcript file is missing, skip that expert and select the next best one
- If subagent fails, retry once or select an alternative expert

## File Paths Reference

- **Config file:** `~/.claude/skills/product-experts/config.json`
- **Expert index:** `~/.claude/skills/product-experts/index/expert-index.json`
- **Topics index:** `~/.claude/skills/product-experts/index/topics-index.json`
- **Transcripts directory:** From config file (`transcripts_directory`)
- **Output directory:** From config file (`output_directory`)
- **Expert analysis template:** `~/.claude/skills/product-experts/templates/expert-analysis.md`
- **Summary template:** `~/.claude/skills/product-experts/templates/summary-template.md`
