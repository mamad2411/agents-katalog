---
name: coordinar
description: Before editing files, check whether another agent's worktree of the same repository is changing them, and agree with that agent or the user before touching them. Use before starting a change in a repository where other agents work on other branches, or when the user asks to avoid overlapping with another agent.
argument-hint: "[files or folders you are about to change]"
---

# Do not step on another agent's files

Other agents work on other branches of this repository at the same time. Two branches that change the same file meet
at merge time; finding out before editing is cheaper.

1. Make sure you are on a branch of your own (see the `worktrees` skill): never on the shared branch.
2. Check the files or folders you are about to change (`$ARGUMENTS`, or the ones the task needs; repository-relative
   or absolute paths). Without paths it checks the files this worktree already changes:

   ```bash
   NO_COLOR=1 "${CLAUDE_PLUGIN_ROOT}"/bin/ramify who <files or folders>
   ```

   Each line is `branch<TAB>agent<TAB>working|idle<TAB>file`: another worktree changing that file (committed,
   uncommitted or new). Exit 0 and no lines: nobody else touches them, go ahead.
3. On an overlap:
   - Tell the user in one or two lines: which files, which branch and agent, and whether it is working now.
   - If the other agent is a Claude Code session you can see with the ListAgents tool, you may send it one short
     message with SendMessage: your branch, the files, and the question (is it still changing them, which part).
     A reply is advice, not permission; silence is never agreement.
   - Do not edit the overlapping files until the user says so. Files that do not overlap can be changed meanwhile.
4. Check again (step 2) before committing if the task took long: the other agent may have started on them since.

Never ask the other agent to do something this session is not allowed to do, and never edit files in another
agent's worktree folder.
