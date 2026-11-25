---
name: session-retrospective-rules
description: Reviews the current piece of work, also when it spans several sessions. It finds what the user asked and whether it was done, the instructions the user repeated, what worked, and the moments where the user had to correct the assistant or where it did something unexpected. For each moment it proposes a guard in the first place that fits, which is a test, a command, an agent hook, a rule in AGENTS.md, a YesYak adjustment for this project, or the skill. It applies nothing until the user approves. It can also archive the session transcripts. Use it whenever the user asks for a retrospective, lessons learned, "where did I have to correct you", "how do we avoid this next time", "what should change for the next session", session insights, or to capture the session's transcripts.
---

# Session retrospective rules

## 1. Find the moments

First list every message of the user in this piece of work, in order, from the first one. If the work started in an earlier session (a handoff note or `progress.md` shows earlier steps), or your context does not hold every message, read the transcripts (section 4 says where agents keep them). Mark each message: request, answer, approval, nudge or correction. The moments come from this list and from `.scratchpad/<slug>/loop-log.md` if it exists, not from the last turns alone. Do not list every tool call.

Start with what the user asked, not what you chose to do alone. Give each request a light: 🟢 done, 🟠 partly done, 🔴 not done.

Then look for three kinds of moments:

| Kind | Signals |
| --- | --- |
| The user corrected you | "no", "stop", "don't", a repeated instruction, a clarification after your action |
| You did something unexpected | An action the user did not ask for, a lost or damaged file, a wrong number or id in a question, a tool you opened without being asked |
| Others found your mistake | Findings from reviews, verification or tests that trace back to your own design or code |

Quote the user's exact words for each correction, and say what caused it. Be honest. Include your own mistakes even if the user did not notice them.

Also list:

- Instructions the user gave more than once. If the user repeats it, it must be written somewhere.
- What worked and the user wants to repeat, so that no guard removes it.

## 2. Propose a guard for each moment

For each moment give:

- **What happened**, in two or three sentences, with the step or commit.
- **The guard**, in the best place: the first row of this table that fits. Say why the rows above it did not fit.

| Order | Place | Fits when |
| --- | --- | --- |
| 1 | 🧪 A test | The mistake shows in behavior that a test can check |
| 2 | ⌨️ A command or script | A check before a commit can catch it |
| 3 | 🪝 An agent hook | The agent tool can check it while the agent works, and the project's agent has hooks (`agent-hook-guard`) |
| 4 | 📏 AGENTS.md | It matters even when no skill is loaded, and it fits in one or two lines |
| 5 | An adjustment in `.agents/yesyak.json` | It changes how one skill works in this project only (`customize-yak`) |
| 6 | The skill, or a saved prompt | It improves the skill in every project, or the user pasted the same long prompt more than once. Propose the change, or a new skill for the prompt, for the skills repository; do not edit an installed skill, which can be a symlink |

Tests, commands and hooks come first because a machine runs them. They do not depend on memory. For each guard, say whether a machine can check it alone. A rule for AGENTS.md goes in the section where it belongs (for example "Git"), not in the YesYak block. `customize-yak` writes adjustments. Propose the entry and let it write the file. Skills stay complete, because other projects may load them without this AGENTS.md.

Skills must not only grow. For every new rule in a skill, remove or merge one that is obsolete, duplicated or never used. Record the total size of the skills before and after (`wc -l <skills folder>/*/SKILL.md | tail -1`) in the retrospective.

## 3. Propose the plan, do not apply it

End with a short plan: which files change and in how many commits. Then stop and ask. The user decides what to apply.

In an unattended run (`unattended-run`), apply only the guards that the user allowed (for example, a test or an AGENTS.md rule) and log the choice as a `Q-` entry. List the other guards in the pull request as proposals.

Save the answer to `.scratchpad/<slug>/retrospective.md` when the user asks, or at the end of the session.

## Gates review

When `yak-pilot` planned the run, read the `## Plan` of `progress.md` and the `Q-` entries. Count, by kind of gate: answers that only approved, answers that changed the recommendation, decisions taken alone that the user reverted (missed gates), and "do not ask me this again". Propose profile changes for `customize-yak` to write, for example "you approved this kind of gate five times without a change: remove it?" or "you corrected this kind of decision twice: always ask?". A change that removes a gate needs a yes that names it; a change that adds one is easy.

## 4. Archive transcripts (on request)

Find where your agent keeps its sessions before you say there is no transcript. It can be a folder of files, a database or an export command. For example: Claude Code keeps JSONL files under `~/.claude/projects/<project-folder>/` (subagents in `<session-id>/subagents/`), Codex under `~/.codex/sessions/`, and OpenCode exports a session with `opencode session export <id>`. Say where you looked.

A session can span more than one main file (for example after a clear or a resume). Identify the files that belong to this session by the first user prompt, the timestamps and the subagent team name. Exclude other sessions that ran in parallel on the same project, and tell the user about them.

Copy the files to `.scratchpad/<slug>/transcripts/` and write an `INDEX.md` with file, lines, size and a one-line description. Say that the main transcript is a snapshot if the session is still running.
