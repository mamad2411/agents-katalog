---
name: git-commit
description: Stages all changes and creates one Conventional Commits 1.0.0 commit. Does not push.
disable-model-invocation: true
---

# Git commit

One commit covering **all** current changes. Message grammar: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/#specification). Full header/body/footer rules → [reference.md](reference.md).

## Steps

1. Inspect with `git status`, `git diff`, and `git diff --staged` if anything is staged. Infer intent and any obvious breaking API/behavior change.
2. Nothing to commit → say so and stop (no empty commit).
3. `git add -A`, then re-check `git diff --staged` and `git status --short` so the message matches **staged** content only.
4. Choose one `type` for the dominant change (`feat` for a new feature, `fix` for a bugfix, else `docs` / `refactor` / `perf` / `test` / `build` / `ci` / `chore` / `style` as fits).
5. Write the message per [reference.md](reference.md). Prefer `git commit -m "header" -m "body and footers"` so the blank line after the header is preserved.
6. Push only if this message explicitly asks.
7. On success, paste the exact recorded message (`git log -1 --format=%B`) into chat — full header/body/footers, not a summary.
8. **Done when:** one commit exists for the staged set, the chat shows that exact message, and you have not pushed unless asked — or you stopped with nothing to commit / awaiting split confirmation.

## Split vs squash

Default is one commit. If the staged set clearly mixes unrelated work, warn and offer to split; split only on user confirm.
