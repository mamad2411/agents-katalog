---
description: Review this session and propose concrete improvements to the skill(s) it used
argument-hint: [optional — a specific skill name or area to focus on]
---

Reflect on THIS session and improve the skill(s) it used. The goal is to make the
skill itself better next time, based on how it actually performed here — then edit
its definition on disk (with my approval).

Optional focus (a specific skill or area): $ARGUMENTS

Steps:

1. IDENTIFY which skill(s) ran this session — look for Skill tool calls and
   /<command> invocations in the conversation. If $ARGUMENTS names one, focus there.
   If no skill was used this session, say so plainly and stop — there's nothing to improve.

2. LOCATE each skill's definition on disk and read it. Skills live at
   ~/.claude/skills/<name>/SKILL.md, in a plugin's skills dir, or .claude/skills/<name>/
   in the project. Read SKILL.md and any supporting files it references.

3. REVIEW how the skill performed this session. Hunt specifically for:
   - Places where I deviated from the skill's instructions, or you had to correct or
     redirect me.
   - Steps that were ambiguous, missing, out of order, or wrong.
   - Manual workarounds we did by hand that the skill should have handled.
   - Instructions that turned out to be unnecessary, brittle, or counterproductive.
   - Friction you expressed, or moments the skill slowed things down.

4. PROPOSE concrete edits — exact wording for SKILL.md (and supporting files), not
   vague advice. Tie each proposed change to the specific moment in this session that
   motivates it ("you had to tell me X because the skill never said Y").

5. FILTER HARD. Only durable, generalizable improvements that would help on a future
   run. Drop session-specific noise and one-offs. If nothing genuinely warrants a
   change, say so rather than inventing edits.

6. SHOW me the proposed changes as a clear before/after (or diff) and ask for approval
   BEFORE editing. On approval, apply them to the skill files.

Note: this complements `self-improving-agent` (which captures learnings as notes) by
actually editing the skill definition. If a learning is better stored as a note than
baked into the skill, say so.
