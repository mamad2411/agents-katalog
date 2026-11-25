---
name: update-skill
description: Maintain an existing skill by batching real usage feedback, reflecting on the patterns, and landing one focused edit instead of reactive monkey-patches. Use when the user wants to improve, tune, fix, or update a skill they already wrote, points at feedback for a skill (a notepad, GitHub comments, Slack threads), says a skill is drifting or misbehaving, or wants to set up a weekly self-improvement loop for their skills.
---

# Update Skill

Improve a skill from **batched feedback**, not from a single complaint. Treat skills like code: they drift, and they earn maintenance only when enough signal has accumulated to see the real pattern.

The failure mode this skill exists to prevent is **monkey-patching**: addressing each report independently until the skill is a pile of special cases that miss the broader picture. The fix is to wait, cluster, reflect, then make one coherent change.

## Named heuristics

Use these by name when you reason out loud with the user.

- **Two-data-point rule.** You would not extract an abstraction because you did something twice. Do not reshape a skill on one or two reports. Wait for a third independent signal before treating something as a pattern.
- **Batch window.** Let feedback accumulate for a few days to a week before acting. Reacting per-comment overfits to noise.
- **Monkey-patch test.** Before writing an edit, ask: "Does this fix one report, or the class of reports behind it?" If it only fixes the instance, you are patching, not improving. Go back up a level.
- **EM-coaching reflection.** Interpret feedback the way a good engineering manager coaches a report: identify what went wrong, look for patterns, ask why, self-reflect, zoom out, check against the skill's stated principles. Then, and only then, edit. Full rubric in [REFLECTION.md](REFLECTION.md).
- **Terseness ratchet.** Every edit must leave the skill as tight as it found it. If a change adds lines, look for lines it makes redundant. A skill that only grows is a skill rotting in slow motion.

## Process

### 1. Identify the target and gather feedback

Confirm which skill is being improved and where its feedback lives (a side notepad, GitHub issue/PR comments, Slack threads, the user's own recollection). Pull the **whole batch**, not the one item that prompted the request. See [SCHEDULING.md](SCHEDULING.md) for the feedback-notepad convention and how to collect from each source.

If only one report exists, say so and apply the **two-data-point rule**: either note it for later or ask the user whether this single case is load-bearing enough to act on now. Do not silently edit.

### 2. Cluster into patterns

Group the raw feedback into a short list of **named patterns**, oldest signal first. For each: how many independent reports back it, what the skill currently does, and what good would look like. Drop one-off noise into a "not yet a pattern" bucket and keep it visible rather than acting on it.

### 3. Reflect (do not skip)

Run each candidate pattern through the **EM-coaching reflection** in [REFLECTION.md](REFLECTION.md). The output is a verdict per pattern: change, defer, or reject, each with a one-line reason. A pattern that contradicts the skill's stated purpose is a flag for the user, not an automatic edit.

### 4. Propose before editing

Present the verdicts as a numbered list: pattern, evidence, proposed change, what it removes or simplifies. Ask the user which to apply. Do NOT edit the skill yet.

### 5. Make one coherent edit

Apply the agreed changes as a **single focused revision**, not N independent patches. Honor the **terseness ratchet**. Keep the skill's existing voice and structure. If the change is large or shared across a team, prepare it as a PR rather than an in-place edit (see [SCHEDULING.md](SCHEDULING.md)).

### 6. Close the loop

Mark the acted-on feedback as resolved in its source (clear the notepad lines, note it in the PR). Leave the "not yet a pattern" bucket intact for the next window.

## Invocation

The user invokes `/update-skill` and names a skill or points at feedback. Examples:

- "Update the vault skill, here's a week of notes on it."
- "The triage skill keeps mislabeling. Go through the recent issues and fix it."
- "Set up a weekly loop that drafts improvements to my read-up-on skill." (see [SCHEDULING.md](SCHEDULING.md))

## Guardrails

- Never edit a skill off a single report without flagging the **two-data-point rule** first.
- Never ship N independent patches when one coherent change covers the pattern.
- Never let the skill grow verbose: honor the **terseness ratchet** on every edit.
- If feedback conflicts with the skill's stated purpose, surface the conflict and ask. Do not quietly bend the skill toward whoever complained last.
- Tune reflection instructions to the model in use. Defaults here are written for Claude.
