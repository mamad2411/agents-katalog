---
name: reflect
description: "Reflect on this conversation: turn each mistake and correction into a rule, route it to where it will be enforced, and apply the ones you pick."
disable-model-invocation: true
---

# Reflect

Turn what went wrong in this conversation into rules that stop it happening again. A **lesson** is one mistake plus the rule that would have prevented it. Every lesson lands in the repo the conversation worked in, in the place that enforces it best.

## Steps

1. **Collect the mistakes.** Go through the conversation for every moment the work was corrected: the user pushed back, asked "why did you", reverted a change, rejected a draft, or relayed a reviewer's requested change; plus any mistake you caught yourself. For each, write what happened and what should have happened, quoting the user's words. Done when every correction in the conversation has an entry.

2. **Write the rule.** One imperative line per mistake, stating the behaviour to follow, with this repo's case as evidence at the end ("PR #868 shipped Ctrl only"). Pitch it at the class of mistake, not the instance: "search `src/components/base/` for a component that already renders it before adding one", not "use StatusTag for badges". Done when each rule would have prevented its mistake and would also catch the next mistake of the same kind.

3. **Route each rule** to the first home that fits:
   - **A fixed pattern** a regex can match on one line (a banned API, a class name, a call shape): the repo's automated check, when its `AGENTS.md` names one (such as `.agents/scripts/check-diff.py`), plus the rule's line in `AGENTS.md`.
   - **A workflow** (a sequence of steps the agent skipped or ran out of order): the skill that owns that workflow. Skill sources live in the skills repo, `~/hq/skills` on the host and `~/skills` in a devvm VM; edit them there.
   - **A browser-testing gotcha** (locators, mocks, test data): the repo's browser-testing doc, when its `AGENTS.md` points to one (such as `docs/agents/browser-testing.md`).
   - **Everything else**: the section of the repo's `AGENTS.md` it belongs to, following that file's "Keeping this file current" section; the Failure log only when no section fits.

   The target is always a file in the repo you are working in, never a user-level file such as `~/.claude/CLAUDE.md`. Done when every rule has one target file and section.

4. **Check against what exists.** Search each target for a rule that already covers the lesson: when one does, the lesson sharpens that rule instead of adding a new one. Also find rules the lesson contradicts, and rules the user overruled in this conversation (a teammate or the CTO allowed it): those become removals. Done when each lesson is marked add, sharpen, or remove.

5. **Present and wait.** Print the lessons numbered, each with the rule text, add, sharpen or remove, the target file and section, and the quoted correction behind it. Then stop until the user picks. Done when the user has said which numbers to apply.

6. **Apply the picks.** Make exactly the chosen edits. In `AGENTS.md`, edit only the lines for the picked lessons and leave every other line as it is, because the file may be shared across worktrees and running sessions. For a check-script rule, show that it fires on the offending line and count its hits on the current code before keeping it. Done when every picked lesson is applied and nothing else changed.

7. **Report.** List each file you edited and what changed. Say plainly when an edited file is untracked (check `.git/info/exclude`: a file listed there never shows in `git status`). For a skill change, follow the `ship-skill` skill's commit, register, and install steps. Done when the user can see every edit without running `git status`.
