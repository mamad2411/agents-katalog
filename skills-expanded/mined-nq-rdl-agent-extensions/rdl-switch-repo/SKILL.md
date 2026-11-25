---
name: rdl-switch-repo
license: CC-BY-4.0
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
description: Switch active repository context within a Claude Code multi-repo session, load the target project skills, and verify spec-kit runs in the correct repo.
compatibility: Requires Claude Code 2.1.32+ (skills load from --add-dir directories); /add-dir of a subdirectory of the working directory needs 2.1.257+. Written for Claude Code 2.1.274.
---

Treat the requested repo as the active work target, while retaining the session’s
original root. This does not replace project settings, permissions or MCP servers.
Verify current [skill loading](https://code.claude.com/docs/en/skills)
and [working-directory behaviour](https://code.claude.com/docs/en/tools-reference#what-persists-between-commands)
before claiming a harness change; these contracts evolve.

1. Resolve the user’s path or unique sibling repo name to an absolute path. For
   ambiguous names, ask which repo. Record the previous active repo, then inspect
   target `git rev-parse --show-toplevel`, branch and status without changing them.
2. Load the target skill surface with `/add-dir <absolute-repo>` in the main
   session (ask the user to type this built-in if no directory-registration tool
   is exposed). A shell `cd` or `permissions.additionalDirectories` alone does
   not register skills. On supported hosts a directory-registration tool may
   load them, but check its actual schema and restrictions before calling it.
   Do not edit user config or copy project skills into a global directory.
3. Read target `AGENTS.md`/`CLAUDE.md` and inspect `.claude/skills/` and
   `.claude/commands/`. Change Bash cwd to the target and verify `pwd` and git root
   in a subsequent call. Pin every later shell call to this absolute repo if the
   harness resets cwd. File operations and delegated prompts must use its paths.
4. Check the **loaded** skill list for the intended spec-kit command and its
   target-qualified name/path. Added repos remain loaded, so bare same-named
   commands are unsafe. Use the directory-qualified command exposed by the host;
   do not guess its spelling. If the host cannot disambiguate sibling commands,
   report the limitation and offer a target-rooted session. Do not claim that
   reading a SKILL.md makes its slash command invokable.
5. Verify `.specify/` and the target command’s scripts exist. Before specify,
   inspect the intended base and current HEAD: spec-kit forks from current HEAD.
   Do not switch branches or create a throwaway branch as part of repo switching.
   User-only commands still require the user to invoke the qualified command.
6. Report the active absolute repo, branch, previous repo and verified command
   identity. For “back”, repeat these checks against the previous repo. Before
   each spec mutation, recheck cwd/git root and confirm output paths are inside
   the active repo. Keep the active/previous paths in the session handoff so
   context compression cannot silently restore the launch repo.

Acceptance probe: from a home-rooted session, register two sibling repos with
same-named spec-kit skills, verify both qualified commands appear, switch A → B
→ A, and check each command’s read-only prerequisite output identifies its own
repo. If discovery or targeting fails, stop before creating any spec and report
which host capability failed. An added directory is access plus discovery, not
an exclusive unload/re-root of the entire session.
