---
name: turn-incident-into-content
description: Use when you've solved a user problem, answered a support question, or helped someone with a technical issue and want to turn it into shareable content. Produces both short-form "TIL" and long-form fully-contextualized pieces, plus recommends the right format (docs, blog, talk).
---

Before doing anything else:
1. Check if `~/.devadvokit.md` exists.
2. If it does, read it silently and use it throughout this skill.
3. If it does not, stop and tell the user: "I need your DevRel context before I can run this skill. Please run /setup-devadvokit first."

---

## What NOT to Do

This skill produces content directions — not finished publication drafts. Specifically:

- **No polished blog posts** — you're creating frameworks for future pieces
- **No commit-ready docs PRs** — this gives you the structure and says where docs should be updated, not the PR text itself
- **No social media threads** — use `/repurpose-talk` for that workflow

The goal is extracting the reusable lesson from a specific incident.

---

## Q&A

Ask these questions one at a time. Wait for each answer before asking the next.

1. What was the problem? Describe what the user was trying to do and what they ran into. Be specific — the actual error message, the unexpected behavior, what was confusing.

2. What did you try? Walk me through your debugging process. What solutions did you attempt? What didn't work? This shows the problem-solving journey.

3. What actually worked? What solved it? Be specific — the command, the config change, the conceptual shift, whatever fixed it.

4. What would you tell someone hitting this cold? If you were writing a guide for someone encountering this for the first time, what's the one-sentence takeaway they need?

5. Who was the user? (Developer, data scientist, DevRel peer, etc. — this affects audience framing)

---

## Output

Produce all of the following once the Q&A is complete.

### 1. TIL Format

A short-form "Today I Learned" version suitable for a quick post, thread, or newsletter item.

**Title:** [Working title with "TIL" framing]

**Body:** 2–3 sentences. Start with what didn't work, then the solution, then the takeaway. Keep it punchy.

**Format fit:** Micro-post, thread starter, or newsletter TIL section.

### 2. Full Context Format

A longer framework for a blog post or deep-dive content.

**Working title:** [Descriptive title, not TIL-style]

**The problem:** [1-2 paragraphs setting up what happened and why it matters]

**The investigation:** [What you tried, what didn't work, the debugging journey — 2-3 paragraphs]

**The solution:** [What actually fixed it — 1-2 paragraphs with code/config examples if applicable]

**The transferable lesson:** [1 paragraph on what this teaches more broadly]

**Audience:** [Who would benefit from this, based on both the user and your audience in `~/.devadvokit.md`]

### 3. Format Recommendation

Recommend the best format based on the nature of the problem:

Choose ONE primary recommendation and explain why:

**If docs update:**
> This should be a docs update. The user hit a gap in documentation — this should be fixed at the source.
> - **Where:** [Which docs page/section]
> - **Why docs:** [User was looking for official reference, not a blog post]
> - **Optional blog:** A blog post could also work, but fix the docs first.

**If blog post:**
> This should be a blog post. This was a reasonable problem that required real problem-solving — others will hit it and want the full context.
> - **Why blog:** [It's a debugging journey others will benefit from]
> - **Angle:** [The narrative frame that makes it compelling]

**If talk seed:**
> This could be a talk. There's a conceptual lesson here that extends beyond this specific incident.
> - **Why talk:** [The principle extends to other situations/technologies]
> - **Talk angle:** [How to frame this as a broader lesson]

**If small/one-off:**
> This is a TIL or small post. It's specific enough that it doesn't warrant a full piece — capture it as-is.
> - **Why small:** [It's a specific gotcha, not a broader lesson]
> - **Fits:** Newsletter item, TIL thread, quick post

---

## Content Library Check

Scan the content library in `~/.devadvokit.md`. If you've already covered this specific problem:

> "You covered this in [title] ([year]) — consider whether this adds new information or updates the existing piece."

If nothing overlaps, omit this section entirely.

---

Before presenting any output, read `../../shared/ai-antipatterns.md` and silently rewrite any flagged patterns. Do not mention this step to the user.