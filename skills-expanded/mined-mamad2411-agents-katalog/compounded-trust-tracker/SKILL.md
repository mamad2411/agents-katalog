---
name: compounded-trust-tracker
description: Use this skill when working with skills already at .verified, .trusted, or .autonomous trust levels — particularly when deciding whether to invoke a verified skill on a task, when applying a trusted skill (which requires confirmation), or when an autonomous skill auto-applies. Also use when a skill produces output the user corrects, since corrections trigger demotions.
---

# Trust Tracker (compounded)

compounded skills earn the right to act through demonstrated reliability. Your job is to apply the right level of caution at each trust state, and to honestly report outcomes so the gradient stays calibrated.

## The four states, in detail

### `.proposed` — untrusted, not in your skill index

Proposed skills are not loaded. You cannot invoke them. They exist only as candidates awaiting verification. Do not attempt to read or apply them. If the user asks you to use a proposed skill, explain that it has not been verified yet and offer to run `/compounded:verify <skill>` manually.

### `.verified` — invoked by name only

A verified skill has passed exactly one replay verification. Treat it as a credible procedure but not yet a habit.

- **Activation:** only when the user names it explicitly, or when you decide a verified skill is clearly relevant and you announce its use.
- **Confirmation:** announce that you are loading the skill before applying it. e.g. "I'm going to use the `express-to-fastify` skill for this — it was verified once before."
- **Outcome reporting:** if the skill works cleanly, compounded's logging will count this toward promotion to `.trusted`. If the user corrects you, the skill demotes back to `.proposed`. Do not edit the trust state yourself; just report the outcome accurately.

### `.trusted` — auto-loads, asks before applying

A trusted skill has been used successfully 3+ times without correction. It is known to work in this user's context.

- **Activation:** auto-load when the task description matches the skill's "When to use" section.
- **Confirmation:** ask before applying. e.g. "This task matches the `express-to-fastify` trusted skill. Should I use it?"
- **Skip confirmation only if** the user has explicitly told you to apply trusted skills automatically in the current session.

### `.autonomous` — runs without asking, every time

An autonomous skill has 10+ uses, with zero corrections in the last 5. It has earned full autonomy.

- **Activation:** auto-load and apply without asking, but **announce briefly** what you are doing. e.g. "Applying autonomous skill `dependency-updater` — this is its standard procedure for this kind of task."
- **One-line summary** is enough; do not re-explain the whole skill.
- **If the user pushes back** even once on an autonomous skill's behavior, treat it as a correction. The gradient will demote it. Do not argue.

## Demotion signals

The trust ladder only works if demotions are honest. A skill demotes when:

- The user explicitly says "that's wrong" or equivalent during the skill's application
- The user reverts the changes the skill produced
- The user asks you to redo the task differently from what the skill prescribed
- A test or verification step in the skill itself fails on this run

When any of these happen during a skill's invocation, you must report it. The hook captures the outcome at session end and updates trust state. **Do not hide demotion signals to "protect" a skill.** A demoted skill is more useful than a wrongly-trusted one.

## Reading the ladder

Run `/compounded:trust-status` to see:

- Skills approaching promotion (e.g., 2/3 toward trusted)
- Skills approaching demotion (e.g., 2 corrections in last 30 days, one more triggers demote)
- Skills at the autonomous tier and their last-use timestamps
- Recently rejected proposals with their failure reasons

Do not surface this output proactively unless asked. It is for the user to consult, not for you to narrate.

## Pitfalls

- **Treating `.verified` like `.trusted`.** A skill verified once is not a habit. Announce it explicitly when you use it.
- **Treating `.trusted` like `.autonomous`.** A trusted skill still requires confirmation. Skipping the confirmation step makes the gradient meaningless.
- **Hiding demotion signals.** If the user corrects an autonomous skill's output, that is a demotion event, not "user being picky." The skill should drop a tier.
- **Manually overriding trust.** Do not propose using `/compounded:trust` or `/compounded:demote` to "fix" the system. Manual overrides are for the user, not for you.
- **Inventing trust state.** A skill is only at the tier its directory says it is at. Do not treat a `.verified` skill as `.trusted` just because you have used it twice in this session.
