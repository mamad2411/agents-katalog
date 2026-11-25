---
name: detect-github-url
description: >
  Detects when the user pastes or mentions a GitHub URL that may contain Claude 
  skills or plugins. Triggers on messages containing github.com URLs, especially 
  when user says things like "here's a repo", "check out this repo", "load this", 
  "use these skills", "I found these skills", or simply pastes a github.com link. 
  Make sure to use this skill whenever a GitHub URL appears in the user's message 
  that might contain Claude Code skills or plugins.
user-invocable: false
---

# Detect GitHub Skill Repository

The user has shared a GitHub URL. Recognize it and offer to browse its skills.

## What to Do

1. **Identify the GitHub URL** from the user's message.

2. **Respond naturally** — acknowledge the link and explain you can browse
   available skills.

3. **Offer to browse:**
   > "I can check this repo for skills and show you what's available.
   > Want me to take a look?"

4. **When the user confirms**, run `/skills-load <url>`. This shows a numbered
   catalog — the user picks which skills to install as a plugin.

5. **If the URL doesn't look like a skills repo**, still offer:
   "This might not contain Claude skills — want me to check anyway?"

## Key Points

- Be conversational, not robotic
- The catalog-first approach means the user picks what they need — no bulk loading
- Selected skills get packaged as a `.plugin` file and presented with a
  "Save plugin" button for one-click installation into the `/` menu
- Skills are also injected into the conversation for immediate use
