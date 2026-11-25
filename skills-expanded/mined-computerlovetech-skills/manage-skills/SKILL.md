---
name: manage-skills
description: Manage agent skills. Use when adding, updating, removing, or installing skills.
---

## Source locations

Keep locally owned skill sources in the repository's root skills/ directory.

Store directory-specific skill sources in that directory's skills/ subdirectory. Run the skills CLI from the containing directory to install them for that scope.

## Installation and editing

Use the skills CLI to install skills. Run it with the package runner this repository specifies, such as bunx or npx.

Install skills owned by another repository from its remote Git URL or hosting shorthand, even when a local checkout is available. The remote Git repository is the source of truth.

Use local paths only for skills owned by the current repository, or when the user explicitly requests a local installation for development or testing.

Never edit or modify installed skills in .agents/skills/, .claude/skills/, .github/skills/, or similar installation directories.

Edit locally owned skills in their skills/ source directory, then reinstall them to update the installed copies. Reinstalling is safe and idempotent; run it without asking.

Treat skills from external repositories as remote dependencies. Update them through the skills CLI rather than editing their source or installed copies.

Install named skills from a remote repository with:

    skills add computerlovetech/skills --skill manage-skills --agent claude-code --agent codex --full-depth -y

Install the root skills/ sources with:

    skills add ./skills --skill '*' --agent claude-code --agent codex --full-depth -y

Name each agent with its own --agent flag; comma-separated lists are rejected. Never use --all or --agent '*': the root skills/ directory is itself an agent target, so those flatten the source taxonomy into symlinks and leave an untracked agent/ directory.

## Version control

Track locally owned skill sources in Git.

Treat installed skills like .venv in Python and node_modules in Node: they are managed dependencies and belong in .gitignore.

Ignore .agents/, .claude/, and .github/ when they contain only installed skills.

When these directories also contain content that should be tracked, such as GitHub Actions or hooks, ignore only their skills/ subdirectories: .agents/skills/, .claude/skills/, and .github/skills/.
