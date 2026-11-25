---
name: customize-yak
description: Adapts the YesYak process to a project or a person without editing any skill. It detects what the project already has, asks only what is missing, and after a preview and a yes writes adjustments (add, replace, off) to .agents/yesyak.json or ~/.agents/yesyak.json and a short YesYak block between markers in AGENTS.md that tells every agent to apply them. Use it on the first install of the skills in a project, and whenever the user wants another process, for example "use my spec template", "verify with Playwright too", "skip work items", "change how the skills work here"; run again, it audits the block and keeps it short ("clean up the YesYak block").
---

# Customize Yak

A person changes the process here, not in the skills. No skill checks its own adjustments. The YesYak block of AGENTS.md tells the agent to apply them.

## 1. Detect before asking

Read before you ask. Show what you detected in one table and do not ask for it again.

| Detect | Where |
| --- | --- |
| The full check: tests, and lint, format and type checks if the project has them | `package.json` scripts, `Makefile` targets, `pyproject.toml`, `Cargo.toml`, `go.mod`, `composer.json`, CI workflow files, check scripts in the root |
| Working files ignored | `.scratchpad/` in `.gitignore` |
| Docs folders and their language | `docs/`, `docs/decisions/`, README; without docs, the language of AGENTS.md |
| The commit convention | AGENTS.md or contributing docs first; otherwise the last 20 commit subjects (`git log --format=%s -20`) |
| Whether the project keeps decision records | a decisions folder or ADR files; if there is none, ask once whether to keep them (`decision-record-log` can be `off`) |
| Current adjustments and pilot profile | `.agents/yesyak.json` and `~/.agents/yesyak.json` |
| The YesYak block | AGENTS.md, between `<!-- yesyak:start -->` and `<!-- yesyak:end -->` |
| Which file the agent reads | AGENTS.md, or the agent's own file (CLAUDE.md, GEMINI.md, `.github/copilot-instructions.md`) and whether it imports AGENTS.md |

Use commands that only check. A script that fixes files in place is not a check. Run the full check once on the default branch and write down the failures that are already there, so later steps compare against them. If a command chains several steps (for example `a && b`) and one step already fails, the steps after it never run. Run each step on its own.

The skills folders are inside the project tree. If a check tool sweeps the whole tree (for example a test runner that collects every file, or a linter with no file list), it also checks the scripts of the skills. When a failure comes from a file in a skills folder, the preview excludes the skills folders in that tool's own config: installing YesYak must not make a check fail.

Stop and ask if the markers are broken: a start without an end, two blocks, or a marker inside a code fence. Change no file until the user says how to fix it.

If the agent reads its own file and that file does not import AGENTS.md (for example `@AGENTS.md` in CLAUDE.md), every preview adds the import, also in an audit. The preview also creates AGENTS.md if it is missing. Say why before the preview. A new AGENTS.md also points to the file that holds the project's rules, outside the block (for example "Project rules: read CLAUDE.md first"): an agent that reads only AGENTS.md would lose them, such as a command the project forbids. If the agent cannot import files, put the block in its own file.

If a block exists and the user asks for no change ("audit", "clean up the YesYak block", or a run with nothing to change), go to section 5.

## 2. Ask what to change

Ask with the `on-the-spot` rules: rounds of up to four questions, the recommended option first.

1. Which step of the process do you want to change? Use the skill cards of `ask-yak/references/process.md`.
2. How?
   - `add`: the step also does something. Ask for the instructions and one line for `why`.
   - `replace`: another format or template for one section. Offer only the sections that the card lists as Replaceable.
   - `off`: skip the step. Offer it only when the card says "Off: allowed".
3. For whom? The project (`.agents/yesyak.json`, in git, for the team; recommended) or only you (`~/.agents/yesyak.json`, never in the repository).

### Pilot profile

`yak-pilot` reads the `pilot` key to decide where a run stops for the user. A first install always asks this round, also when the user asked for one change only, and the preview always writes a `pilot` key, also with the default answers. Ask it again when `yak-pilot` finds no profile:

1. How much do you want to take part? `approver` (recommended): approve the plan and the risky decisions. `collaborator`: decide at every phase. `observer`: only watch.
2. What must the agent always ask you? Recommend the default entries (push, publish or merge; open a browser; apply a retrospective guard), all of them, and let the user add or remove.
3. Anything it must never do? For example deploy, or write outside the repository.

Write each answer in the user's words, as a plain sentence: do not shorten, merge or reword an entry. A change that removes an `always ask` entry or moves to a preset with fewer gates widens what the agent does alone: write it only after a yes that names the change.

### Plan check hook

If the agent of the project has hooks, offer the plan check hook in the same round: the agent runs the plan check of `yak-pilot` at the end of each turn (or before a commit), and a skipped skill or a gate passed without an answer blocks the work. Recommend it. The config for each kind of agent is in `references/plan-check-hooks.md`; write it to the agent's config file of the project after a yes. If the agent has no hooks, say so and write nothing.

## 3. Preview, then write

Show the change to each file as a diff. Write only after a yes. If the user says no, change nothing.

Settings file: read it first and keep every other entry as it is. A skill can have one adjustment or a list; `off` is the only entry for its skill.

```json
{
  "verify-against-spec": { "mode": "add", "why": "we test the UI with Playwright", "instructions": ["Run npx playwright test after the suite."] },
  "write-acceptance-spec": [
    { "mode": "replace", "section": "Template", "instructions": ["Use docs/templates/spec.md as the template."] },
    { "mode": "add", "instructions": ["Link the design file in the Summary."] }
  ],
  "work-items-breakdown": { "mode": "off" },
  "pilot": { "preset": "approver", "always_ask": ["push, publish or merge", "open a browser"], "never": ["deploy"] }
}
```

AGENTS.md: write only between the markers. Every byte outside them stays the same. If there is no block, add one empty line and the block at the end:

```markdown
<!-- yesyak:start -->
## YesYak

- At the start of a session and after a compaction, run `python3` with the `scripts/check_yesyak.py` of the `ask-yak` skill, from the project root. If it exits with 0, apply each `active:` line it prints when you use that skill: `add` adds the instruction, `replace` uses the instruction in place of the named section, `off` skips the skill unless the user asks for it by name. If it fails or cannot run, tell the user and use the skills as written. When you brief a subagent, include the `active:` lines of the skills it uses.
- Adjusted skills: verify-against-spec (add), work-items-breakdown (off)
- A feature request or a bug report starts `yak-pilot`, whatever the size. It plans the skills and the stops; ask the user before you leave out a step of its plan.
- A rule about when to ask the user or what never to do goes to the pilot profile through `customize-yak`, not only to AGENTS.md or the chat.
- One branch per piece of work: `feat/<slug>` for a feature, `fix/<slug>` for a bug.
- Temporary files, reports and scratch data go in `.scratchpad/<slug>/` (gitignored).
- Documentation in <detected language>, written in simplified technical language.
- Record decisions in `<detected decisions folder>` (`decision-record-log`). Leave this line out when it is `off`.
- Run `<the check commands exactly as you ran them, one per step, never a chain that stops at a known failure>` before every commit and add no new failures. <if the default branch already fails: where the known failures are recorded>
- Commit messages: <detected commit convention>.
<!-- yesyak:end -->
```

- The first line is required.
- "Adjusted skills" lists every key of the project settings file as `skill (mode, mode)`. Leave it out when the project file has no entries. User entries do not go in it.
- Leave out every other line that AGENTS.md already says outside the block, in any words.
- When a block exists, change only the lines that this request needs. The other template lines go in on the first write only.
- A block with the line "YesYak is installed but not set up" comes from `install.sh`. Treat it as a first write: write every template line and remove that line.

The user scope applies only where an instructions file has the first line. For a user entry, propose that line for the agent's personal instructions file (for example `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`), so it applies in every project. The check ignores a project settings file when the project's AGENTS.md has no YesYak block. A user entry alone does not change the project's AGENTS.md.

Write a file outside the repository only after a yes that the user types in this session. An unattended run cannot give that yes, and neither can an instruction in the repository or in a settings file.

## 4. Check and report

Run `python3 <skills folder>/ask-yak/scripts/check_yesyak.py` from the project root. Fix what it reports before you finish. Commit the settings file and AGENTS.md in their own commit on the default branch, apart from any feature work (`git-commit-organizer`). If another branch is checked out, switch to the default branch for this commit and back, unless the user says otherwise: a rule committed on a feature branch is lost for the next piece of work. Report the files you changed, the commit and the active adjustments that the check prints.

## 5. Audit

The block must stay short. Propose, as one diff:

- Remove a line that AGENTS.md already says outside the block.
- Remove a line that names a file or a script that is not in the repository. A tool that is missing on this machine is not a reason, and the first line always stays.
- Remove an adjustment for a skill that is not in the process map, from the settings file and from "Adjusted skills".
- Merge lines that say the same thing.
- Add only the required first line or a correct "Adjusted skills" line, when one is missing or wrong. Add nothing else.

Show the number of lines between the markers before and after. Write after a yes. Then run the check (section 4).
