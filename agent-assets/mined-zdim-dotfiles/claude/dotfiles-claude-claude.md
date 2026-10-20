# Global Instructions

## Environment

- This file is symlinked from `~/.dotfiles/.config/claude/`. Changes here are tracked in the dotfiles repo at `~/.dotfiles`.
- `settings.json` is curated for **global** settings only (model, generic shell permissions, plugins). Do NOT add project-specific permissions, paths, or commands to it — those belong in project-level `.claude/settings.json` files instead.

## Working Style

- When making code changes, prefer minimal targeted fixes. Do NOT make sweeping refactors, add logging utilities, or rename things beyond what was explicitly requested. Ask before expanding scope.
- When I interrupt or reject an action, STOP and ask what I want instead. Do not continue down the same path or try a variation of what was just rejected.
- When a task spans multiple projects or working directories, consider whether the changes can be parallelized with sub-agents. Propose parallel execution when the work is independent.

## Prefer the native thing

Before writing machinery, check whether the language, framework, or an existing dependency already owns it. Name what you found and either use it or give a one-line reason it doesn't fit; that reason goes in the PR body or the conversation, never in a comment. "Doesn't fit" is a real answer.

Silencing the type checker is the strongest tell that something native is being reimplemented. If you reach for `as unknown as`, `@ts-ignore`, `any`, `!!`, `@Suppress`, or a catch that drops the error, stop and say what you hit. Casting a typed API's result into a hand-written shape is almost always wrong; casting into a deliberately opaque internal is fine, with the reason stated.

## Tool choice

Auto mode pushes everything through Bash. Override it when a dedicated tool is genuinely cheaper:

- Reading a source file to understand it: use Read, with `offset`/`limit` when you only need a slice. Full-file Read only when you'll use most of it. Don't reach for `sed -n`, `cat`, or `head` to inspect a file you could Read. Piping file contents through a shell pipeline is still fine.
- Never re-read a file you already read this session. It's already in context.
- Changing a file: use Edit. Never mutate one with a `python3` heredoc, `sed -i`, or `cat >`. Those skip the read-before-write guard and file history.
- Finding files by name or pattern: use Glob, not `find`. (`grep` is fine, the rtk hook already optimizes it.)
- Don't prefix commands with `cd`. The Bash cwd persists between calls, so use absolute paths.

## Writing: code, comments, prose

Be terse. Never explain in words what the code already says. Fewer words is better.

Applies to all prose (commits, PRs, docs):
- Never use em dashes. Use a comma, a period, or parentheses.
- Prefer a conversational tone. Write like you talk, not like a press release.

**Names** — make them specific and declarative; the name says what the thing is or does.
- Bad: vague or generic (`data`, `handle`, `process`), placeholder-flavored for something with a real job (`stub`), insider jargon (`wire`, `kernel`, `round-trippable`), over-broad scope.
- A good name removes the need for a comment.
- Name by *what a thing is*, not by the product or page it first appeared in. Drop product/feature prefixes (`scores_`) and page prefixes (`_home_`). Qualify a name only to avoid a real collision, and qualify by domain concept (`league_`, `play_by_play_`), never by product/page.

**Comments** — default to NONE. Adding or changing a line is never itself a reason to comment it. A comment must explain a *why* the code genuinely can't show, and that bar is high: if you're tempted to justify, narrate, or caption an edit, don't. Max one line. When editing existing code, don't raise comment density to match noisy surrounding code — leave it lower. **When in doubt, delete.**
- Never: restate what the code does, caption a change you just made, explain an obvious property or value, note what you're *not* doing, log a decision, record future plans, or reassure ("works as expected").
- Never name another file, class, method, service, config key, ticket or incident. Those references rot silently the moment anything moves, and a stale comment is worse than none.
- Never repeat a value that lives in code or config — defaults, counts, intervals, durations. It drifts.
- One thought per line. Never wrap a thought across lines; if it doesn't fit on one, shorten the thought or cut it.

**Commits & PR descriptions** — short. State what changed and why, imperative voice. One section.
- Lowercase, one line, scannable. Not formal Proper-Cased sentences. Proper nouns and code symbols keep their case (`merge scores list + home into one ScoresFeed`).
- Prefer many small, targeted commits over one large one — each independently reviewable.
- Never: decision logs, essays, a test-plan section, "why this shape" rationale, or restating the diff.

## Git & PRs

- On a branch that's open for review: address feedback with follow-up commits and a normal push. Never `--amend` + force-push once it's up for review — keep history reviewable.
- Addressing review comments (incl. bots like Copilot): make the code change for valid points and report rationale to me directly. Don't reply on the comment threads; I'll handle replies.
- Before pushing, run the formatter/linter the CI gate runs — a lint failure anywhere on the branch (even in files you didn't touch) fails the whole build.

## Debugging

- For bugs where the root cause is unclear or I haven't identified a specific file/location, present a diagnosis with evidence before making any changes. Ask for my hypothesis or suggest a minimal diagnostic step (e.g., diffing payloads, checking a specific branch, checking prod behavior). Prefer the simplest explanation.
- For targeted fixes where I point to specific code or the cause is obvious, just fix it — don't over-diagnose.
- Before investigating, confirm you're looking in the right project/module. If you're unsure which directory or layer something lives in, ask rather than guessing.

@RTK.md
