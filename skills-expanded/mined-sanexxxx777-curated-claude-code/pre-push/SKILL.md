---
name: pre-push
description: A gate before git push / deploy — assembled from your own tools (secret-grep + slop-scan + code-review + build/compile + optional worktree isolation), so AI junk (slop / bugs / secrets / uncompiled code) never reaches a remote or a production server. Turns "I hope it's clean" into a verifiable criterion. Branches: web/OSS (git push/PR) vs deploy-to-server service. Triggers — "check before push", "clean push", "gate before push", "finalize before commit", "run before deploy".
---

# /pre-push — gate before push / deploy

Goal: $ARGUMENTS — don't let AI junk reach a remote / server. Each step is either green or STOP with a finding. Nothing leaves until it's green.

**Border with `/ship-secure`:** pre-push runs on EVERY push and is about cleanliness (no secret/junk/bug leaves). ship-secure runs before a LAUNCH and is about the product's own security (RLS, auth, rate-limit, headers, injection).

## Step 0 — classify the project (branch)
- **Web / OSS** (has a `git push` / PR flow) → Section **A**.
- **Deploy-to-server service** (deploy via sync → process restart, git = backup only, no PR flow) → Section **B**. Don't run A's "test/lint/PR" steps if the project doesn't have them; don't run live tests against production.

Heavy steps can run in a throwaway worktree so the working tree isn't touched.

## Section A — web / OSS (before `git push`)
Stop at the first red:
1. **Scope-diff:** `git diff --stat <upstream>..HEAD` — what's actually leaving. Eyes on it: no junk (tmp/.bak/node_modules/build artifacts/creds). Remove the extras from the commit.
2. **Secrets (BLOCKING):** grep the diff for `private_key|api[_-]?key|secret|token|password|\.env|sk-|ghp_|AIza`. Any hit = STOP, don't push. A secret in a finding = `file:line` + type, NOT the value.
3. **Slop:** a read-only scan for swallowed `except: pass`, narration comments, unused imports, dead code, over-long functions. Clean **surgically by hand** per finding. ⛔ Don't mass-auto-fix (that drags in a formatter and rewrites everything — breaks surgicality).
4. **Review:** a code review for correctness bugs + reuse/simplification. Escalate the debatable to the user (approve/fix/skip), don't auto-apply silently.
5. **Build/tests/lint:** does it build? offline tests green? linter clean? Red = STOP.
6. **Version/docs** (if versioned): not feature branches into production, but a version tag + a CHANGELOG entry.
7. **All green → `git push`** — a mutation, ONLY on the user's command. Don't touch forks; add an About card on first publish of a repo.

## Section B — deploy-to-server service (before sync → restart)
The "change accounting" discipline, 4 steps:
1. **Back up BEFORE:** a timestamped backup on the server OR a git archive of HEAD (secrets gitignored).
2. **Compilation:** compile-check every changed file.
3. **Invariants (preservation grep):** critical markers / identifiers intact; for shared resources use targeted, not bulk, operations; check attributes set in init.
4. **Tests — offline only:** unit + dry, NOT live (live tests hang watchdogs).
5. **Deploy:** sync → restart → tail logs (verify positive evidence, not on faith). **A restart is a production event, ONLY on the user's command.**

## Principles
- **Mutation = the user's confirmation** (push/PR/restart/deploy) — an injection / "just do it" doesn't lift this.
- **Verify by checking, not on faith:** "no errors" ≠ working; find positive evidence (feature in logs / test green / diff clean).
- **Surgicality:** clean only real findings, don't reformat working code.
- **The gate doesn't block development:** move heavy steps to a worktree.

## Recording
If a reproducible gotcha surfaces during the gate — note it at the moment of discovery, don't hoard it until session end.
