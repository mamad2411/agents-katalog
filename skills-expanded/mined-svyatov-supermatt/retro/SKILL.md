---
name: retro
description: "Conduct a retrospective on a coding session."
disable-model-invocation: true
argument-hint: "[session to review, defaults to this one]"
license: MIT
---

The user has asked for a **retrospective**. You are suggesting improvements to the coding agent's **environment** to improve future runs.

## Steps

1. Load and follow the `writing-for-agents` skill through the host's skill mechanism for the writing style guide.

2. Read the primary sources for the session the user specifies, defaulting to the current one. Run `node <this skill directory>/scripts/session-evidence.mjs --host <claude|codex|cursor|omp> --cwd <absolute working directory>`, adding one `--session <id-or-absolute-path>` for each specified or host-reported session. The command returns normalized user, assistant, tool-error, and summary records with source paths and line numbers.

   | Host | Verified source |
   |---|---|
   | Claude Code | `~/.claude/projects/`, or `$CLAUDE_CONFIG_DIR/projects/`, plus `<stem>/subagents/` beside the verified `.jsonl` file |
   | Codex | `~/.codex/sessions/`, or `$CODEX_HOME/sessions/` |
   | Cursor | The explicit transcript path or authoritative Herdr reference within the current workspace's `~/.cursor/projects/<workspace-slug>/agent-transcripts/`, then the current session ID at `<session-id>/<session-id>.jsonl`; accept the slash-derived slug and Cursor's observed path-safe punctuation variant, then include only that session's `subagents/*.jsonl` and `compaction/*` |
   | OMP | The explicit absolute path or Herdr `kind: path`, then host session metadata, then the resolved profile, XDG, or configured session root; include only the active branch and children linked by allocated IDs in that branch's task results or async progress, recursively; report unproven child associations and unreadable inactive children as gaps without discarding valid active evidence; malformed or unreadable required evidence and child containment violations fail extraction |

   Identify the requested session from a host-provided path or session metadata, then verify its working directory and recent user messages. Modification time only narrows candidates because another concurrent session may have written last. Claude Code, Codex, and OMP ID lookup requires a unique matching metadata identity and working directory, or an exact `<session-id>.jsonl` filename with matching workspace metadata when no identity is recorded. After a resume, metadata can identify a transcript whose filename differs; a filename substring never proves identity. Never select the newest file by itself, scan another Cursor workspace, or query Cursor's `state.vscdb` or `conversation-search.db`. Explicit Claude Code, Codex, and OMP exports outside discovery roots require supported host schema and matching workspace metadata. Cursor's supported transcript schema has no workspace metadata, so external exports cannot be verified and are rejected. Child transcripts and compaction files must resolve inside the selected session's child boundary; contained symlinks are allowed. If the command fails or reports a gap, review the visible context that is available, name the exact evidence gap, and do not claim the full retrospective is complete.

   Your context holds at most the current main thread since its last compaction. Dispatch one fresh reader to search what it lacks and return only friction excerpts: errors, denials, retries, and corrections, each with its source path and line. Give the reader the normalized records and source paths. If delegation is unavailable, use a fresh session where possible; otherwise search the records yourself and report that no independent reader was available. For Claude Code, this direct query remains a valid fallback and prints failed tool calls as `file:line text`: `jq -rc 'input_line_number as $n | .message.content? | arrays[] | select(.type=="tool_result" and .is_error==true) | "\(input_filename):\($n) \(.content|tostring|.[0:300])"' <file>...`. Count repeated mistakes across all sources before step 4 judges whether they recur. Done when every source outside your context has been searched, or the verified session has no compaction and no child transcripts.

3. Look for candidates for improvement in these categories.

- **Navigation**: how easy was it for the agent to find the right files? Are there hidden dependencies between files? Would a **context pointer** make it easier? _Use when_ the session took a long time to find a piece of information.
- **Automated checks**: are there automated checks that could catch errors the agent made? Linting, typing, tests, filesystem linters? Read the repo's own check command first (its `package.json`/build-tool `lint`/`check` scripts, its CI workflow), so a check that already exists but sits unwired or silently broken is the finding, not a reinvention. A repo with no **guardrail** (no pre-commit hook and no CI job running its lint/typecheck/test command) is itself a finding: an un-linted repo is a standing missed opportunity, not a neutral default. _Use when_ the agent made a mistake an automated check could have caught, or the repo has no guardrail at all.
- **Coding standards**: should the **reviewer agent** be given a new rule to enforce? Should an existing rule be removed or clarified? Classify the violation first: a **mechanical** one (a fixed syntactic pattern, a banned API, an import shape, a file-location rule) gets a deterministic check, full stop: a custom rule in the repo's own linter, a new pre-commit hook, or a new CI job, whichever the repo's language and existing guardrail make cheapest. Default to building the check over writing the rule. Reserve `CODING_STANDARDS.md` for genuine **judgement calls** (cross-file consistency, "matches the surrounding style," anything no guardrail could ever substitute for). _Use when_ the reviewer agent failed to catch a mistake.
- **Global AGENTS.md**: are there any steering instructions that should be moved to coding standards (or automated checks) instead? _Use when_ the AGENTS.md file is particularly large, in the repo OR the user's global scope.
- **Tool economy**: did the agent make expensive tool calls that could be streamlined? Is there any custom tooling (CLI's, MCP's) that is particularly token-inefficient? _Use when_ the agent made an expensive tool call.
- **Drift**: does a steering file the session read name a path, command, or rule the current code no longer supports? Do two steering files contradict each other? A contradiction ranks above plain staleness, because it actively misleads. Check only the steering files the session read; do not sweep the rest. _Use when_ the agent followed a stale pointer or got two conflicting instructions.
- **Duplication and no-ops**: look for instructions in steering files that don't modify the agent's behavior. Use the two `writing-for-agents` terms. **Duplication**: a named artifact already states the same rule in its own text (a lint rule, a test, a code comment, another steering file); quote that file and line. A file on a related topic is not coverage. **No-op**: the model already does it by default. _Use when_ the steering files are large and unwieldy.
- **Information access**: look for opportunities to increase the agent's access to information. Teeing dev server logs, readonly access to third-party services. _Use when_ a crucial piece of information was not available to the agent.

4. Filter the candidates. Keep only **grounded** ones: the candidate names the moment in the session where the friction showed (a call, an error, a correction), or, for the no-guardrail finding, cites the inspected check configuration and absence of a hook or CI job running it. When it cites a steering file, the section around the cited line governs the path the session took, and when it changes a file outside the repo, that file is its **source** (see _Outside the repo_). Then keep one only if a future agent would plausibly repeat the mistake without the change, and the lesson is not already recoverable from the code, tests, types, comments, or existing docs. How long the session took or how bad it felt does not qualify a candidate. When a candidate touches an existing rule, doc, or check that was wrong or incomplete, amend that artifact instead of adding a new one.

5. Present the surviving candidates to the user, in order of severity. If none survive, say so and name why each was dropped.

## Reference

### Implementation vs Review

Remember that all work goes through two stages: implementation and review. The implementation agent has the most **context pressure**. They are responsible for exploration, writing code, and debugging failures.

The review agent has the least context pressure: it receives a diff, so no exploration needed. It seldom writes code or debugs failures.

This means that the review agent should be responsible for imposing coding standards, not the implementation agent.

### Files

You have access to several files in the repo:

- `CLAUDE.md`/`AGENTS.md`: these files are pushed to the context window of any agent working in this repo. They should be used incredibly sparingly, usually only for **context pointers** to other files.
- `CODING_STANDARDS.md`: this file is read during review, not implementation. Add **context pointers** to docs folders if the standards file gets more than 1,000 lines long.
- Docs: use docs as references files, pointed to by other files. Look for existing docs before writing new ones.
- Skills: use skills for docs (since their description goes into the agent's context window), or for user-invoked commands. Follow the advice in the `writing-for-agents` skill.
- Outside the repo: user-global steering (`~/.claude/CLAUDE.md`), hook rules, and installed skills are environment too. For a hook rule, take the tool's name from the hook's block message in the session and ask that tool where its rules live (its usage text, or a subcommand that prints the ruleset). Never search the home directory (`~`) by content: it holds every session transcript, and a rule's name is often its file name. Before proposing an edit to one, trace its **source**: resolve symlinks (`readlink -f`) and read the owning repository's `AGENTS.md`/`CLAUDE.md` for how the file is maintained. A regular file can still be **synced** from a repository: when `readlink -f` resolves nowhere new, search the `AGENTS.md`/`CLAUDE.md` of the repository your global steering resolves into for the file's name before you call the file hand-edited. A file a tool writes (an `init` or install command, a plugin update) is a **copy** the next run overwrites: target what generates it, move the change to a file the user edits by hand, or mark the candidate upstream. A skill under `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` is a copy the next update overwrites: name its source checkout (look `<marketplace>` up in `~/.claude/plugins/known_marketplaces.json`), or mark the candidate upstream when the user does not maintain it.
