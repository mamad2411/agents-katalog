---
name: retro
description: Review a finished coding session for what slowed the agent down or let a mistake through, and turn one lesson into a test, check or doc in the project so the next session does not repeat it. Use when the user asks for a retro or retrospective, a post-mortem of a session, or "what should we change so this doesn't happen again". To carry unfinished work into a new session, use `handoff`; to prove a fix before claiming it, use `regression-proof`.
argument-hint: 'Which session to review (default: this one)'
disable-model-invocation: true
---

# Retro

A retro improves the agent's **environment**: the checks, docs and pointers that the next session in this project will run into. It ends with one change made in the project, which the user reviews and commits. Credit and license: `LICENSE.md` in this folder.

## Steps

1. **Load the style guide.** Call the Skill tool with `writing-for-agents`. Every doc or rule this retro writes is read by an agent, and that skill says how to write one so it is followed the same way every run.
2. **Read the session.** Use the session the user names; with none named, use the current one. For an earlier session, read its transcript rather than working from memory: Claude Code keeps them as `.jsonl` files under `~/.claude/projects/<project slug>/`. Note each place the agent searched for a long time, made a mistake, retried, or lacked a fact it needed.
3. **Find candidates** in the categories below. Each candidate names the moment in the session (the tool call, the error, the retry) and the change that would have prevented it.
4. **Present them to the user, most severe first.** Severity is what the problem cost or would cost again: a mistake that shipped outranks a slow search, a slow search outranks a wasted tool call.
5. **Build the one the user picks.** Make the change in the project: the test, the lint rule, the CI step, the doc or the pointer. Run it and report its exit code. A new check must fail on the mistake it is meant to catch before it counts, so show it red on that mistake, then green on the fixed code.

## Categories

- **Navigation.** How easily did the agent find the right files? Are there hidden dependencies between files? Would a **navigation pointer** (one line in a file the agent already reads, naming where something lives) have saved the search? _Use when_ the session took a long time to find a piece of information.
- **Automated checks.** Could a lint rule, a type check, a test or a file-layout check have caught a mistake the agent made? Read the project's own check commands first (its package scripts or build tool targets, its CI workflow), so a check that exists but is unwired or silently broken is the finding, not a reinvention. A project with no **guardrail** at all (no pre-commit hook and no CI job running its lint, type check or tests) is itself a finding. _Use when_ the agent made a mistake a check could have caught, or the project has no guardrail.
- **Coding standards.** Should the reviewer be given a new rule, or should an existing rule be removed or clarified? Classify the violation first. A **mechanical** one (a fixed syntax pattern, a banned API, an import shape, a file-location rule) gets a deterministic check: a custom rule in the project's linter, a pre-commit hook or a CI job, whichever the project's existing guardrail makes cheapest. Build the check rather than writing the rule. Keep written standards for **judgment calls** that no check can make, such as consistency across files or matching the surrounding style. _Use when_ a review missed a mistake.
- **Always-loaded instructions.** Should a steering instruction in `CLAUDE.md` or `AGENTS.md` move to the coding standards or to a check? _Use when_ that file is large, in the project or in the user's global scope.
- **Tool economy.** Did the agent make expensive tool calls that could be cheaper? Is a custom CLI or MCP server spending many tokens for little information? _Use when_ the agent made an expensive tool call.
- **No-ops.** Is there an instruction in a steering file that does not change what the agent does? Remove it. _Use when_ the steering files are large.
- **Information access.** Was a fact the agent needed out of its reach? Writing dev server logs to a file it can read, or read-only access to a third-party service, can fix that. _Use when_ a crucial piece of information was not available to the agent.

## Where a lesson goes

Work goes through two stages: implementation and review. The implementing agent is under the most **context pressure**: it explores, writes code and debugs failures. The reviewing agent receives a diff and usually neither explores nor debugs, so it has room. Coding standards belong to review, not to implementation.

- **`CLAUDE.md` / `AGENTS.md`**: loaded into the context of every agent in the project. Use them sparingly, mostly for navigation pointers to other files.
- **Coding standards file**: read during review, not implementation. If it grows past about 1,000 lines, move sections into docs and leave pointers.
- **Docs**: reference files reached through a pointer from another file. Look for an existing doc before writing a new one.
- **Skills**: for reference whose description should sit in the agent's context, or for a command the user types.
- **Checks**: the first choice for anything mechanical, because a check is enforced on every run and costs no context.
