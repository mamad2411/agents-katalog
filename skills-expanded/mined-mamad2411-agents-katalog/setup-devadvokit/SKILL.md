---
name: setup-devadvokit
description: One-time setup skill that builds your DevRel context file (~/.devadvokit.md) through a guided Q&A. All other DevAdvokit skills read this file — run this first.
---

Run an interactive setup to capture your DevRel context and content library. The output is written to `~/.devadvokit.md` and read automatically by every other DevAdvokit skill.

If `~/.devadvokit.md` already exists, do not overwrite it without asking first. Offer to update individual sections or append to the content library instead.

---

## Part 1: Identity and context

Ask the following questions one at a time. Wait for the user's answer before asking the next question. Do not batch questions.

1. What's your name?
2. What's your current job title and company?
3. In one sentence, what does your company do — in plain language, not marketing copy?
4. What are your specialist areas in this role? (e.g. the technical domains you focus on, the audiences you work with, the type of work you spend most time on)
5. How many years have you been working in Developer Relations?
6. List your previous roles briefly, most recent first. For each: job title, company, and the specialist areas you focused on in that role.
7. What are your broader specialist areas across your whole career? (Themes that run across roles, not just your current one)
8. Who do you primarily write and speak for? Describe them: job title, seniority, what context they're in when they encounter your content.
9. What platforms do you publish to? (e.g. company blog, personal blog, LinkedIn, X, YouTube, newsletter)
10. What are your main content pillars or recurring talk topics?
11. What's your writing voice like? (e.g. direct and technical, conversational, educational, opinionated)
12. Are there any words, phrases, or styles you want to avoid in your content?
13. Where are you based? (City, country, or region — whatever level of detail you're comfortable with)
14. What do you do outside of work? (Hobbies, interests, side projects — anything you'd be happy to see appear in a bio)

If any answer is vague or very short, consult `reference/devadvokit-md-schema.md` for guidance on what a strong answer looks like and ask a follow-up question before moving on.

---

## Part 2: Content library

Once Part 1 is complete, tell the user:

> "Now let's build a library of your existing content. This helps the CFP skill avoid repeating angles you've already covered, and lets it reference your past work when relevant. Add as many or as few items as you like — press enter on a blank line when you're done."

For each item, ask:
1. Title or topic
2. Type (talk, blog post, video, podcast, newsletter, other)
3. Where it was published or delivered (event name, publication, URL if known)
4. Year
5. One-sentence summary of the main argument or takeaway

Repeat until the user enters a blank title. Confirm the total count of items added before writing.

---

## Output

Write the following to `~/.devadvokit.md`:

```markdown
# DevAdvokit Context

## Identity
- **Name**: 
- **Current role**: 
- **Current company**: 
- **Company one-liner**: 
- **Years in DevRel**: 
- **Location**: 

## Background
- **Current role specialisms**: 
- **Previous roles**: (title, company, specialisms — most recent first)
- **Career-wide specialisms**: 

## Audience
- **Primary audience**: 

## Content
- **Platforms**: 
- **Content pillars**: 
- **Writing voice**: 
- **Avoid**: 

## Personal
- **Hobbies and interests**: 

## Content Library

| Title | Type | Where | Year | Summary |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

Fill in all fields with the user's answers. If the content library is empty, include the table header with a note: "No content added yet."

Confirm to the user once the file has been written and where it lives (`~/.devadvokit.md`).

---

Before presenting any output to the user, read `../../shared/ai-antipatterns.md` and silently rewrite any flagged patterns. Do not mention this step to the user.
