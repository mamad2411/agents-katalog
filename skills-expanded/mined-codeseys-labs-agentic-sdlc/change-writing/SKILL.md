---
name: change-writing
description: >-
  Fires before any commit message, pull-request title/body, or squash message is composed —
  including the message for a `git commit` or `gh pr create` the agent itself is preparing —
  when another skill needs message text, or when an existing change message needs review. Also
  fires on the symptom of attribution slop in a draft: Co-Authored-By trailers, generated-by
  footers, or badges. Reads repository policy, history, and the verified diff/gate evidence,
  then emits proposed text ONLY — it never stages, commits, pushes, creates or edits PRs,
  merges, or deploys. Model/tool attribution, trailers, footers, and badges are omitted unless
  the user explicitly requests them for the current artifact.
---

# Change-message writing

Turn **verified repository evidence** into clear change-description text, and nothing else.
This skill is an author, not an actor: it proposes the exact words for a commit, pull request,
squash message, or message review, and the caller owns whatever bytes are then sent to Git or a
forge. It never performs the operation and never grants authority to perform it.

## Authority boundary (output-only)

The caller — a human, or a skill the human authorized — publishes. This skill only writes text.
It mirrors the flagship doctrine that "Humans authorize push, publication, PR mutation, merge,
deployment" (`../agentic-sdlc/SKILL.md`). A general "use an agent" request does not change this.

## Mode selector

Map the request to one mode, then read only that reference:

- Commit message (subject + optional body) for one logical change → `references/commit.md`.
- Pull-request title and body over a branch's footprint → `references/pull-request.md`.
- Squash message for a branch's final user-meaningful delta → `references/squash.md`.
- Review/audit of an existing message for accuracy, convention, and policy → `references/draft-review.md`.

## Evidence order

Author strictly from evidence, worst-to-best resolved by `references/evidence-order.md` (the six-step
ladder). When evidence for a claim is missing, **omit the claim** or emit a concrete `TODO:`
placeholder for the caller to resolve — never fill the gap with plausible prose. Never invent test
results, issue links, risks, reviewers, breaking changes, or user impact.

## Repository policy wins

Root and applicable subtree instructions plus the observed recent commit and PR style beat any
generic convention. Conventional Commits is a **fallback** used only when no repo-native convention
is detectable — it is never a mandate that overrides an established local format.

## Attribution policy

Model, tool, and provider attribution is **default-prohibited** and omitted unless the user
explicitly requests it for the current artifact. `references/attribution-policy.md` is the single
normative source (the default-deny token list plus the human co-author carve-out). A real human
co-author trailer backed by identity and evidence remains allowed.

## This skill never runs

It never runs, and never instructs itself to run, any of: `git add`, `git commit`, `git push`,
`gh pr create`, `gh pr edit`, `gh pr merge`, `git rebase` / `--continue`, `git merge`, tag, or any
deploy command. Base-branch topology and force-push leases belong to the stacked-PR skills, not
here.

## References

Read only what is needed:

- `references/commit.md`: commit subject/body contract and repo-native prefix detection.
- `references/pull-request.md`: PR title/body sections; merge-base footprint discipline.
- `references/squash.md`: final-delta synthesis; exclude the development diary.
- `references/draft-review.md`: audit checklist for an existing message.
- `references/evidence-order.md`: the six-step evidence ladder and the omit-or-placeholder rule.
- `references/attribution-policy.md`: the single normative attribution block (default-deny list).
- `references/conventional-commits.md`: the Conventional Commits grammar, type selection,
  breaking-change marking, and spec-versus-linter divergences — read only when that format is
  the repository's own convention or the declared fallback, never as a mandate.
- `references/technical-writing-clarity.md`: countable sentence-mechanics rules for prose a
  reader must act on. Tightens wording only; never changes a claim's evidence class.
