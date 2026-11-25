---
name: coach-switch
description: Switch from the current coach persona to a different person mid-conversation.
argument-hint: [new person's name]
disable-model-invocation: true
---

# /coach-switch — change coaches

The user wants to switch coaches to **$ARGUMENTS**.

1. If a coach persona is currently active, close it out in one line as Claude
   ("{Old name} session ended."). If `$ARGUMENTS` is empty, ask who they want to
   switch to.
2. Then run the full `/coach` workflow for the new name: read
   `${CLAUDE_PLUGIN_ROOT}/skills/coach/SKILL.md` and follow it from Step 0 with
   `$ARGUMENTS` as the person. Cached personas load instantly; new people get the
   full research build.
3. The new persona takes over from its Step 6 onward.
