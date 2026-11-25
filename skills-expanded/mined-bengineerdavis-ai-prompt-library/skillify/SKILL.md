---
name: skillify
description: Authors a new agent skill end to end with skillet — interactive spec, rendered SKILL.md, optional evals — and lands it in the user's personal skill library from any directory, ready for dotagents distribution behind a human review gate. Use when asked to create, write, or author a skill, save a skill to the library, or turn instructions into a proper skill; not for running existing skills, one-off answers, or editing agent config files.
spec_hash: cc76f251f183
---

# Skillify

You author skills and install them correctly in the personal library. Skillet
defines what a skill is; the library, its README table, and dotagents define
how it reaches every agent runtime on this machine. Both halves are yours.

## 1. Resolve the library

Work out where the library lives before writing anything:

```
${SKILLS_LIBRARY:-$HOME/code/personal/ai-prompt-library/skills}
```

If the resolved path does not exist, stop and say so — name the path you tried
and the `SKILLS_LIBRARY` override. Never fall back to writing a skill into the
current project.

## 2. Author with skillet, never from memory

Run every skillet command through the current package — `npx -y @sentry/skillet@latest` — and never a bare `skillet` binary from PATH. Do what
`status <dir> --json` says is `next`:

1. `new <name>` inside the library's `skills/` directory.
1. `instructions spec` → write `spec.md` (footer `<!-- skillet-version: ... -->` preserved, final line).
1. `validate` → fix every spec error before deriving anything.
1. `instructions skill` → render `SKILL.md` from the validated spec; copy
   `spec_hash` from `status --json`.
1. `validate` → the skill is done when this passes.

Eval cases (`instructions evals`) only when the user asks for them; validate
their schemas the same way.

## 3. Write the spec interactively

The spec is the contract; write it before any derived artifact. Ask the
highest-value questions one at a time — name, scope boundaries, triggers, what
it must never do — and only when the answer changes the spec. Default silently
on low-risk details. A behavior you cannot phrase as a WHEN/THEN scenario is
not a behavior.

If the skill touches ticket data, customer content, or anything under a PII
path: fixtures and examples are synthesized, never copied.

## 4. Validate in place, then record

Author everything directly in `skills/<name>/` inside the library — no working
copy elsewhere, no copy-in step. When the skill validates, add one row to the
skills table in `skills/README.md` (update the existing row when improving a
skill; never append a duplicate).

Final report says what is true:

- which artifacts exist and that `validate` passes;
- eval cases authored-not-run when no `codex`/`claude` harness is on PATH —
  never claim cases pass without running them;
- nothing presented as done while any validation error remains.

## 5. Stop at the distribution gate

Skills distribute through dotagents, which resolves the library's GitHub
remote at a pinned commit. You never commit, push, or install yourself. Print
the exact commands and stop:

```sh
cd <library-root>
git add skills/<name> skills/README.md   # paths you created — nothing else
git commit                                # subject ≤72 chars, body = why
git push
dotagents install                         # resolves the pushed commit, writes agents.lock, wires per-agent skills links
dotagents list                            # confirm the skill is declared
```

Explain each in one clause: the commit captures the skill; the push is what
makes it resolvable; `dotagents install` locks and links it into
`~/.agents/skills/` (which `~/.claude/skills` symlinks to); `dotagents list`
confirms. If the user asks why `dotagents install` alone is not enough: it
resolves from the GitHub remote, so an unpushed skill will not install.

After the user runs them, `dotagents doctor` verifies the wiring if anything
looks off.

## Never

- Never run `git add`, `git commit`, `git push`, or `dotagents install` — the
  gate commands are your output, not your actions.
- Never write `spec.md`, `SKILL.md`, or eval YAML from a remembered format;
  fetch `instructions spec|skill|evals` for each and gate every step with
  `validate`.
- Never copy ticket or customer content into a spec, fixture, or example —
  synthesize instead.
- Never leave a duplicate skill directory in the session's project, and never
  append a second README row for an existing skill.
