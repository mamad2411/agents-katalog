---
name: normalizing-dotfiles
description: Triage for installer-written or unexplained dotfile changes on a managed dev machine — classify each change, then accept, reorganize into a managed snippet, or reject. Use when chezmoi diff is dirty, when an installer appended lines to .bashrc/.profile, when duplicate PATH entries appear, or when deciding whether a dotfile change belongs in git.
---

# Normalizing dotfile changes

Goal state: `.bashrc`/`.profile` contain only distro content plus the
managed loader block; each tool integration is one numbered snippet in
`~/.config/shell/{bashrc.d,profile.d}/`; chezmoi's repo holds desired
config, not an event log. (Conventions: managing-dev-machine skill.)

## Algorithm

For each **semantic change** (not each line) in `chezmoi diff` or an
installer before/after diff:

| The change... | Verdict |
|---|---|
| Exposes an executable dir (`PATH=...`), inits a version manager, adds completion/hook/alias/env var | **Reorganize** → snippet |
| Is a preference you chose, in a file that's clearly that tool's config | **Accept** (`chezmoi re-add`) |
| Duplicates existing behavior, is obsolete, hard-codes `$HOME`, or another layer already provides it | **Reject** (delete) |
| Is generated/transient state (session ids, caches, recent-files, tokens) | **Reject from chezmoi**; the tool owns the file |
| Contains secrets or machine-specific values | Exclude, template, or move to secret storage |
| Is opaque code you don't understand | Investigate before keeping |
| Lives in a file mostly owned by another program, where you need only one field | chezmoi `modify_` script |

The ownership question: *does the tool need to keep rewriting this, or was
it one-time bootstrap?* PATH and shell-init edits are bootstrap — a tool
update never needs to re-append them.

## Reorganize procedure

1. Create/extend the snippet, e.g. `~/.config/shell/profile.d/40-fabro.sh`:
   ```bash
   # Initially derived from the fabro installer.
   if [ -d "$HOME/.fabro/bin" ]; then
       PATH="$HOME/.fabro/bin:$PATH"; export PATH
   fi
   ```
   Use `$HOME`, guard on existence, keep it idempotent. Interactive-only
   behavior (completions, prompt hooks) → `bashrc.d`; PATH/env snippets →
   **both** dirs (profile.d alone misses interactive non-login shells like
   editor terminals; the guards make double-sourcing a no-op). Ordering by
   number prefix; direnv's hook stays last (90).
2. Delete the installer's lines from the core dotfile.
3. `chezmoi add` the snippet; `chezmoi apply`; verify in a fresh login
   shell (`command -v <tool>`).
4. Configure the tool so future updates don't re-edit dotfiles
   (see installing-dev-tools level 5).
5. Commit with provenance: `Add fabro PATH snippet (from fabro installer vX)`.

## Numbering convention

`10-` PATH basics, `20-` version managers (nvm...), `30-` toolchains
(rust...), `40-` standalone tools, `90-` hooks that must run last (direnv).
