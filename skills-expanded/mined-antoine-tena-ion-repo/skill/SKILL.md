---
name: skill
description: Write or sharpen a skill of an Ion tool's plugin - intent, SKILL.md in the right craft's plugin, one trigger case, docs; tested with `claude plugin eval` only on request. Use when the user wants a new skill, to fix one, or to check one fires and does its job.
argument-hint: "[skill, or what it must do]"
metadata:
  author: Anthropic (skill-creator), adapted for Ion
  source: https://github.com/anthropics/skills/tree/main/skills/skill-creator
  license: Apache-2.0 (LICENSE.txt), changed from the original
---

The skill: `$ARGUMENTS`; without it, what the user just asked for. Talk to the user in their
language; write the skill in English (Claude reads it).

Writing a skill is light: no session is started, nothing is measured. Testing it is a separate
loop of Claude sessions on the user's quota, run only when the user asks ("check it fires",
"test it") or when a skill misfires or does its job badly: then follow `references/eval.md`.

1. **Intent.** If the conversation already holds the workflow ("turn this into a skill"), draw
   it from there: the tools used, the order, the corrections the user made. Ask only what
   nothing gives: what Claude should do, which sentences start it, what it hands back.
2. **Place.** A skill holds a craft's know-how: it goes in the plugin of that craft's tool
   (`plugins/<tool>/skills/<name>/SKILL.md` in `ion-<tool>`), never in a client project. Read
   the plugin's other skills first: one that already covers the need is sharpened, not doubled.
   Name: a plain English word, the folder's name (`/<tool>:<name>`). Work on a branch
   (`/repo:worktree`).
3. **Write it**, following `references/writing.md`: a description of at most 300 characters
   (what it does, then `Use when …` in the user's own words; `tests/test_plugins.py`), then
   steps in the order of the work, each with its why, the long parts in `references/`, what a
   command can do without tokens in the tool's command. The end-of-work answer follows the
   debrief output style inside the [SKILL-FRAME].
4. **One trigger case**, not run: `plugins/<tool>/evals/<name>/prompt.md` with a sentence the
   user would type, and `graders/fires.md`, copied from a neighbour case (`references/cases.md`).
5. **Finish**: the skill in both references and the READMEs of the plugin's repo, in the same
   branch, then `/repo:merge`. Code or idea taken from another repo: a line in
   `~/code/Ion/sources.md`.
