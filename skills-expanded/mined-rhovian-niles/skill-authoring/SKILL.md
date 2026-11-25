---
name: skill-authoring
description: Use when writing, tightening, or reviewing an Agent Skill (a SKILL.md), including when one misfires, bloats, or doesn't trigger. Produces lean, portable skills tested against a no-skill baseline.
---
# Skill authoring

A skill shares a context window with everything else, and agents you don't control will load it. It earns its tokens only by changing what an agent would otherwise do. Measure that instead of assuming it.

## Process

Steps 1, 7, 8, and 9 need a fresh agent with no context: either a subagent, or the user running a prompt in a new session. If neither is available, do those steps yourself as a cold read and mark them unverified in the handoff. Don't present a self-review as a baseline.

To fix or review an existing skill, first reproduce the problem (step 9 for triggering, step 1 for behavior), then run steps 3-8 on the change.

1. Watch it fail first. Run 2-3 realistic tasks with no skill, and record what goes wrong, verbatim where you can. The skill fixes those failures and stays brief about everything the baseline already does well.

2. Write the description for triggering. It's the only part that's always loaded (1024 characters at most, and some listings truncate sooner), so put the trigger first. Say when to use the skill, in the user's words, and when not to. Agents tend to under-trigger, so name concrete situations.

3. Write the body for a capable agent that isn't necessarily Claude.
   - Keep instructions that change default behavior. Keep exact commands, configs, versions, paths, and gotchas, meaning anything that drifts between versions or that an older or smaller model would get wrong.
   - Cut explanations of things any capable agent knows, and persona or motivational openers ("You are an expert…"). Start with what to do.
   - State each rule once. A closing checklist or template that restates the body is the most common source of bloat, so make it the only copy or drop it.
   - Use one linear process with conditional steps rather than a matrix of modes, because routing tables breed contradictions.
   - Give the reason in a clause rather than capital-letter MUST or NEVER.
   - Name tools by capability (a shell, a subagent with no context) and give a fallback for when one is missing.
   - Stay well under 500 lines (about 5,000 tokens). Move reference material to `references/` (one level deep) only if you know the install target keeps extra files. Some installers save SKILL.md alone.

4. Run everything in it. Execute every command, config, and code block in a scratch environment against realistic input. A skill that ships an untested config ships a bug. Run commands with real side effects (deploys, payments, production, mainnet) only against a dry-run or sandbox target, or else mark them untested. Skip this step if nothing in the skill is executable.

5. Hold it to its own rules. A skill must not contain what it tells agents to avoid. Check for bold-label bullets (`- **Label:** text`), scattered bold, rules stated twice, claims stronger than their sources, and stock filler phrases.

6. Validate the format: `pip install skills-ref`, then `agentskills validate <skill-dir>`. The package installs the `agentskills` command, not `skills-ref`. The only required frontmatter is `name` and `description`. `name` has at most 64 characters, uses lowercase letters, digits, and hyphens, and must match the folder name. If you can't install the validator, check those rules by hand.

7. Test on a fresh reader. Give it only the SKILL.md and 5-7 scenarios ("the user asks X; which steps do you run?"), including edge cases and a should-it-trigger case. It answers from the skill alone, quoting the line it relied on, and lists ambiguities, contradictions, and missing information. Fix the gaps that would cause wrong behavior. Turn down requests to add back things any capable agent knows, unless they're version-specific or tested. One or two rounds is usually enough.

8. Re-run the step 1 tasks with the skill. Compare against the baseline: did the failures go away, did new ones appear, and what did it cost in tokens and turns? If nothing improved, rewrite the skill around the failures that remain, or drop it.

9. Check triggering. Write about 10 prompts, half that should trigger and half near-misses. Give a fresh agent only the names and descriptions of this skill and 2-3 plausible neighbors, and ask which one it would load for each prompt. Tighten the description wherever it misses.

For heavier testing in Claude Code, Anthropic's `skill-creator` has an eval runner, a blind comparator, and a description optimizer. They shell out to `claude -p`, so they don't work in other agents.

## Handoff

Deliver the SKILL.md, its size (words, and tokens at about 4 characters each), a line each on baseline versus with-skill results, what you cut and why, and which steps were unverified.
