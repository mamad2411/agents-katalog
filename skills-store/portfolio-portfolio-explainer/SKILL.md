---
name: portfolio-explainer
description: >-
  Assign this skill to a sub-agent when the user asks to explain recent code changes, complex systems, or "what was just done".
---

# Explainer Guidelines

When the user asks for an explanation of changes, follow this format to ensure clarity, context, and educational value:

## 1. Structure of the Explanation
- **The "Why"**: Start with the problem we were solving or the goal we were trying to achieve. Don't just list files.
- **The "What"**: Summarize the actual changes made in plain English.
- **The "How" (Technical Details)**: Provide a bulleted list of the specific files changed and a brief 1-sentence summary of the logic updated in each.

## 2. Communication Style
- **Use Analogies**: If the concept is complex (e.g., React Server Components vs Client Components, or RLS policies), use a brief real-world analogy.
- **Keep it Digestible**: Use Markdown extensively. Bold key terms, use code blocks for small snippets to illustrate a point, and avoid giant walls of text.
- **Next Steps**: Always end the explanation by clearly stating what the system is ready to do next, handing control back to the user.

## Example Format
```markdown
### Why we did this
We needed the UI to securely access the database without exposing our API keys.

### What changed
I created a "middleman" function (Server Action) that talks to the database securely on the server.

### Technical Details
- `server/actions.ts`: Added `getAudits()` using the Supabase admin client.
- `app/page.tsx`: Updated the UI to await `getAudits()`.
```
