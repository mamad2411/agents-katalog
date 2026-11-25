---
name: recall
description: >-
  Rebuild where work on something stands from the repo, handoff notes and past agent sessions, check
  it against the live code, and return a short current-state brief. Use for "where did I leave off",
  "recall my work on X", "catch me up", "what was I doing in this repo", "status of X", or at the start
  of a session that continues earlier work.
---

# Recall

After a break, a restart or a new session, the state of a piece of work is scattered: half in git,
half in old conversations, some in a handoff note. This skill gathers it, checks it against what's
actually in the repo now, and hands back one brief.

## Sources, cheapest first

1. **The repo, live.** `git status`, `git stash list`, current branch, `git log --oneline -15`,
   branches touched in the last two weeks (`git for-each-ref --sort=-committerdate refs/heads`), and
   open pull requests (`gh pr list --author @me` when GitHub's CLI is set up).
2. **Notes the work left behind.** Handoff files (ystack's `context-meter` writes them to
   `~/.claude/plans/<project>-handoff.md`), `TODO`, `CHANGELOG` "Unreleased", `docs/HANDOFF*`, plan
   files in the repo.
3. **Past agent sessions.** Claude Code keeps transcripts in `~/.claude/projects/<slug>/*.jsonl`,
   where `<slug>` is the working directory with separators replaced by dashes. Codex keeps
   `~/.codex/sessions/`. Other agents keep their own logs; find them by modification time.

## Reading transcripts without flooding the context

Transcripts are large. Never read one whole. Pick the two or three most recent that mention the
topic, then pull out only:

- the user's prompts (what was asked, in their words);
- the last few long assistant messages (what was reported at the end);
- the last lines mentioning a test, build or push result.

A short script that streams the JSONL and prints those parts, each truncated to a few hundred
characters, is the right tool. If you're delegating, have a cheap subagent extract and quote them;
you do the judging.

## Check before you trust

A transcript records what an agent said, not what's true now. Before the brief states something:

- "done" or "merged": confirm the commit or PR exists and is where it was said to be;
- "tests pass": run them, or mark the claim as from the transcript and unverified;
- a file was changed: confirm the change is in the working tree or a commit;
- a background job or agent was running: assume it's gone unless you can see it.

Mark anything you couldn't confirm. Old state presented as current is worse than no state.

## The brief

```
# <topic>: where it stands (<date>)

Goal: <one line, in the user's words if possible>
Done (verified): <items, each with the commit, PR or command that shows it>
In flight: <uncommitted changes, open PRs, branches, with paths>
Broken or failing: <errors and failing tests, quoted>
Unverified (from past sessions only): <claims you couldn't confirm>
Waiting on the user: <decisions, approvals, logins>
Next step: <the one concrete thing to do first>
Sources: <the transcripts, notes and commands this came from>
```

Keep it under 40 lines. If the user named a topic, leave out unrelated work in the same repo.

## Rules

- Live repo beats notes, and notes beat transcripts, when they disagree. Say which one you trusted.
- Quote errors word for word; don't paraphrase them.
- Don't resume the work on your own after the brief. Show it and let the user pick the next step,
  unless they asked you to carry on.
