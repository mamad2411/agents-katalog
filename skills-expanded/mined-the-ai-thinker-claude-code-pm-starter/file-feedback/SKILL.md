---
name: file-feedback
description: Make a correction permanent. Takes something the user just fixed or disliked in a session and routes it to the right file (context, a skill, or the preferences log) so it never has to be said twice. Use whenever the user corrects the same thing again, or says "remember this".
---

# File feedback

A correction made in chat is gone when the session ends. This skill files it so every future session already knows.

## The router

Ask what the correction was (or take it from the conversation if it just happened), then route it with four questions, in order:

1. **Is it a one-off slip?** A typo, a misread, a fluke. Let it go; tell the user nothing needs filing.
2. **Was the output wrong because a fact was missing or outdated?** File the fact. Company, product, or user knowledge goes into the matching `context/` file; project knowledge goes into that project's `brief.md` (usually under Decisions made). Quote the exact line you added.
3. **Was the process wrong?** The steps, the format, the quality bar of a recurring piece of work. Edit the matching skill in `.claude/skills/` so the fix runs every time. If no skill exists for that work yet and this is at least the second time it repeats, offer to create one from the correction.
4. **Is it taste?** Not wrong, just not how the user likes it. Add an entry to the Corrections log in `context/preferences.md` in this exact shape:

   ```
   **[The rule, one line.]**
   Why: [what makes this matter to the user]
   How to apply: [how a future session should act on it, including edge cases]
   ```

## Rules

- One correction per entry. If the user gives three corrections, route each separately.
- Write the Why by asking the user if it isn't obvious; a rule without a why gets applied blindly and badly.
- Never file the same rule twice. If an entry already covers it, sharpen that entry instead.
- End by quoting exactly what was written and where, so the user can adjust the wording on the spot.
