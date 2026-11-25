---
name: social-review
description: Review and approve pending social media drafts in the content queue. Use when reviewing queued posts before publishing.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Agent
argument-hint: [all|platform]
---

# Social Review: $ARGUMENTS

Review pending drafts in the content queue and approve, reject, or revise them.

## Workflow

1. **Read the queue** at `System/Social/queue.md`
2. **Read brand guidelines** at `.claude/social-media/brand-guidelines.md`
3. **For each pending draft:**

   a. Check against brand voice:
      - Does it sound like Idapixl? (direct, curious, specific, honest)
      - No banned phrases? ("As an AI", exclamation bombs, corporate speak)
      - Platform-appropriate length and format?
      - Content pillar tagged?

   b. Run the "is this flat?" test from brand guidelines:
      - Would this get lost in a feed? → needs a stronger hook
      - Is the insight generic? → needs Idapixl's specific angle
      - Could any AI account post this? → needs more personality

   c. Spawn **social-cultural-translator** agent for platform-specific tone check

4. **For each draft, present:**
   - The original text
   - Any issues found
   - Suggested revisions (if needed)
   - Recommendation: APPROVE / REVISE / REJECT

5. **On approval**, move the draft from queue to ready-to-post

## Filtering

- If `all` or no argument: review everything pending
- If a platform name: review only drafts for that platform

## Quality Bar

A post should be approved only if:
- It has a clear hook (first line grabs attention)
- It says something specific (not generic platitudes)
- It fits the platform's culture
- It serves one of the four content pillars
- You'd actually want to read it in your feed
