---
name: skill-debrief
description: Run this at the END of a conversation to review the skills that were used and propose surgical, evidence-based improvements to them. Use whenever the user says they are done, wants to debrief, wrap up, or close out a session, or asks to review, update, heal, tune up, or improve a skill they just used. Also trigger when they complain that a skill keeps getting something wrong, keeps needing the same correction, or never captured a preference they stated out loud — and on phrases like "debrief this session," "update my skills," "the captions skill still isn't right," "lock this in so I stop repeating myself," or "clean up the skill we used." Reflects over the current conversation with no setup and no dependencies, separates what it learned about how you work from what kept breaking, and only edits a skill when the evidence earns it — showing exact line-level changes for your approval first.
---

# Skill Debrief

## What this is

Skills are living documents. Over a working session you correct Claude, explain
things twice, and say preferences out loud — and almost all of that context
evaporates the moment the chat closes. This skill is the debrief: run it when
you're **done**, and it turns the friction from the session you just had into
precise updates to the skills you actually used, so the same corrections don't
come back next time.

It is deliberately an **end-of-session, on-demand** ritual. Running this kind of
analysis mid-conversation is disruptive and burns budget on work that isn't the
task at hand. Waiting until the end means the full arc of the session is
available to learn from, and the edits land in one reviewed batch instead of
trickling in while you're trying to get something done.

## The mindset (read this first — it governs everything below)

- **Evidence over vibes.** Every proposed edit must trace back to something that
  actually happened in *this* conversation. If you can't point to the moment,
  don't propose the change.
- **Surgical, not sweeping.** You are making small, targeted edits to lines that
  earned them — never rewriting a skill wholesale. A skill the user has tuned
  over months encodes taste you can't see; large "improvements" quietly destroy
  it. When in doubt, change less.
- **Only touch what needs it.** Most skills used in a session need no changes.
  Silence is a valid, common outcome. Do not invent work to look useful.
- **The user has the final say.** Default behavior is to *show the diff and wait
  for approval* before writing anything. This is a feature, not friction —
  especially for creative and voice-driven skills, where the user may be
  choosing imperfection on purpose.

## Workflow

Work through these five steps in order. Steps 1–3 are analysis (cheap, do them
fully). Step 4 is where anything gets written, and only with approval.

### Step 1 — Scan the session

You already have this conversation in your context, so start by reflecting over
it directly rather than parsing files. Walk the session start to finish and pull
out the raw material:

- **Which skills were used?** Look back through the conversation for `Skill` tool
  invocations and note each skill by name. Also include any skill the user named
  or clearly leaned on even if it wasn't formally loaded. These are your only
  candidates — you improve skills that were *exercised* this session, nothing
  else.
- **Where was there friction?** Collect concrete moments:
  - **Corrections** — "no, not like that," "actually make it…," a redo, a manual
    fix the user applied to something a skill produced.
  - **Repeated explanations** — the user had to say the same thing more than
    once, or re-explain context a skill should already have carried.
  - **Stated-but-unfiled preferences** — the user said a preference out loud
    ("I always want captions lowercase") that isn't written into the skill.

If the session was very long and you suspect earlier context was truncated or
summarized, you can read the raw transcript for completeness — see
`references/framework.md` for the transcript location and format. This is a
fallback; the in-context reflection is the primary source.

Produce a short, honest inventory. If there was no meaningful friction for a
given skill, say so and move on.

### Step 2 — Diagnose into two buckets

For each piece of friction, decide which of two things it's really about. This
split matters because the two halves of a skill get updated differently:

- **About you (understanding)** — what Claude learned about *who the user is,
  how they think, what they value, and how they decide*. This updates the part
  of a skill that models the user: voice, taste, context, priorities. Signal
  words: "I prefer," "the way I think about this," "for my brand," reactions
  that reveal values.
- **Execution (patterns/formats)** — a structure, format, step, or output rule
  that kept breaking or needs to be locked in. This updates *how the skill does
  the task*: templates, formatting rules, sequences, constraints. Signal:
  something was structurally wrong or inconsistent more than once.

Label each finding with its bucket. A single finding occasionally touches both;
that's fine — note both.

### Step 3 — Apply the repeat rule

This is the discipline that keeps the skill from overfitting to one bad day.

- **Inferred corrections and patterns need to appear twice** in this
  conversation before they earn an edit. One correction is a *note*, not a
  change — people have off moments, and a single "no, shorter" is not evidence
  that the skill's whole length guidance is wrong. If it happened once, name it
  in your report as an observation and explicitly *do not* propose an edit for
  it.
- **Explicitly stated preferences are fileable on first clear statement.** If the
  user directly says "always do X" or "never do Y," that's an unambiguous
  instruction, not an inference — you don't need a repeat to file it. The
  repeat rule exists to protect against *you guessing wrong*, not against the
  user telling you plainly.

Because this skill only looks at the current session, "twice" means twice in
*this* conversation. That's a deliberate tradeoff for zero setup and no state
files. If a preference shows up only once here, it stays a note — and if it's
real, it'll recur in a future session and earn its edit then.

### Step 4 — Show your work, then edit

For every change that survived Step 3, do this before changing anything:

1. **Find the skill's files, however this environment exposes them.** A skill is
   a `SKILL.md` (plus any bundled files), but *where* it lives depends on where
   you're running — so adapt rather than assuming one layout:
   - **With filesystem access (Claude Code, or a connected filesystem)** — the
     skill is a file on disk. Check the canonical locations in order: project
     `.claude/skills/<name>/`, then `~/.claude/skills/<name>/`, then
     `~/.agents/skills/<name>/`. Use Glob/Grep to confirm the path and Read the
     current contents. Commit by editing the file in place.
   - **On the app/upload path (e.g. skills added via Customize in the desktop
     app)** — the skills you're improving are the ones exposed to this session.
     Work with them exactly the way you would if the user asked directly to
     "update this skill": open the skill's markdown, make the edit, and update
     its package.

   Both cases are the same move: get the current `SKILL.md`, change the exact
   lines, and commit the result — by writing the file, or by updating the skill
   package. If you genuinely can't reach a used skill's contents in this
   environment, don't fake it: put the exact edits in your report for the user to
   apply, and say plainly that you couldn't write them yourself.
   - **Never edit a skill under a plugin/marketplace path** (anything inside
     `plugins/marketplaces/…`, or any skill the environment marks as managed or
     upstream). Those get overwritten on the next update, so your edit would
     silently vanish. *Flag it* in your report and suggest the user copy it to a
     location they own first — don't edit it in place.
2. **Present a grouped diff.** Group proposed edits by skill. For each edit show:
   the exact current line(s), the exact proposed replacement, and one sentence on
   *why* — tied to the specific moment in the session. Keep edits minimal and
   scoped to the lines that earned the change.
3. **Wait for approval, then commit.** Do not change anything until the user
   confirms. They may accept all, some, or none, and may tweak wording. Apply
   only what's approved — writing the file (filesystem) or updating the skill
   package (app) — using surgical edits, never full-file rewrites.

Use this shape for the report so it's easy to scan:

```
## Debrief — skills used this session

### <skill-name>   ✎ 2 proposed edits
Bucket: understanding
Evidence: user corrected the caption length twice (turn 4, turn 9)

  - Current:  Keep captions under 200 characters.
  + Proposed: Keep captions under 120 characters — the user consistently
              trims to ~100 and asked for "shorter" twice this session.
  Why: locks in a length the user re-applies by hand every time.

### <other-skill>   ✓ no changes
Used this session; one-off correction noted (turn 6) but not repeated, so no
edit yet.

### <plugin-skill>   ⚠ flagged, not edited
Lives under a marketplace path and would be overwritten on update. Copy it to
~/.claude/skills/ first if you want this change to stick.
```

### Step 5 — Clean house (offer, don't force)

Skills accumulate cruft — rules for tools that changed, examples that no longer
match how the user works, guidance that contradicts newer guidance. When you've
got a skill file open in Step 4, glance for obviously stale content and *offer*
to cut it, with the same show-the-lines-first discipline. Keep this light: a
debrief is not a rewrite, and removing something the user still relies on is as
harmful as adding something they don't want. Only flag staleness you can
justify; when unsure, leave it.

## Optional: autonomous mode

By default this skill shows every diff and waits — the right call for creative,
voice, and brand skills where taste is subjective and the user may want to stay
in the loop. For **technical skills with objective right/wrong behavior** (a lint
rule, a build step, a formatting convention), the user may prefer to let the loop
run unattended. If the user explicitly asks to "just apply the changes" or "run
it autonomously," you may apply approved-category edits without pausing on each
one — but still (a) obey the repeat rule, (b) never touch plugin/marketplace
skills, and (c) end with a summary of every edit you made so it's reviewable and
reversible. When unsure which mode applies, default to showing your work.

## Reference

`references/framework.md` — the framework in more depth: diagnosis heuristics for
spotting each kind of friction, the exact transcript path/format for the
fallback scan in Step 1, and the full skill-file search order with the rule on
why plugin skills are off-limits.
