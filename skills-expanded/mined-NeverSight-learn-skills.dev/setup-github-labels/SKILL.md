---
name: setup-github-labels
description: Apply and document the canonical GitHub issue and pull-request label set in a repository.
disable-model-invocation: true
---

# Setup GitHub Labels

Apply one intentional label vocabulary to whatever repo you run this in, then
record its operational meaning for agents. The tables below are the source of
truth, not the GitHub UI. This is a prompt-driven skill, not a deterministic
script: read the set, explore the repo, preview every change, confirm with the
user, then create the labels with `gh` and update the agent docs.

## The canonical set

Four groups, kept small on purpose. This skill owns their GitHub label objects
(name, color, description) and the agent-facing contract in
`docs/agents/triage-labels.md`. Anything a *tool* already owns (Dependabot,
labeler actions) is **not** here.

### Issue `type:` axis

| Label           | Color    | Description (issue-scoped)                          |
| --------------- | -------- | -------------------------------------------------- |
| `type: bug`     | `d73a4a` | issue: Reporting a defect to fix                   |
| `type: feature` | `a2eeef` | issue: Requesting a new capability or improvement  |
| `type: task`    | `cfd3d7` | issue: For other work: maintenance, refactor, docs |

`type: bug` / `type: feature` / `type: task` mirror GitHub's Issue Types
(Bug / Feature / Task). `task` is the catch-all for refactor/docs/chore/test
work. If a repo ever moves under a GitHub org, these map 1:1 onto native Issue
Types and the labels can be retired.

### Issue triage axis

The five whose-turn triage roles the `triage` skill moves an issue through.
This skill creates the GitHub labels and records the role-to-string mapping in
`docs/agents/triage-labels.md`. The scope prefix in each description makes it
clear whether a state applies to issues, PRs, or both.

| Label             | Color    | Description                                        |
| ----------------- | -------- | -------------------------------------------------- |
| `needs-triage`    | `fbca04` | issue: Maintainer needs to evaluate this issue     |
| `needs-info`      | `d876e3` | issue/pr: Waiting on reporter for more information |
| `ready-for-agent` | `0e8a16` | issue: Fully specified, ready for an AFK agent     |
| `ready-for-human` | `1d76db` | issue: Requires human implementation               |
| `wontfix`         | `ffffff` | issue: Will not be actioned                        |

`needs-info` is the one `issue/pr:` label: a PR parked on an outside human reuses
it rather than minting a PR-scoped twin, so "waiting on a human" reads
identically on both. Every other triage role is issue-only.

### Agent PR-verdict axis

Whose-turn routing on a PR needs almost no labels: a non-draft PR with no
verdict is, by definition, the agent's to finalize, and a PR parked on an
outside human reuses the `needs-info` triage label above rather than minting a
PR-scoped twin. What this axis adds is the agent's **terminal verdict** once it
has finished finalizing a PR: the signal that tells the maintainer, at a glance,
what each open PR needs from them.

| Label              | Color    | Description (PR-scoped)                              |
| ------------------ | -------- | --------------------------------------------------- |
| `recommend-merge`  | `0E8A16` | pr: Agent finalized and endorses it: review and merge |
| `recommend-close`  | `D93F0B` | pr: Agent recommends closing: your call to review or close |
| `recommend-triage` | `FBCA04` | pr: Agent finalized it but the merge/close call is yours |

The verdict is **three-way by design**: the agent finalizes a PR (rebase, green
CI, polish) and then emits exactly one of the three. The split exists because
"not mergeable as-is" hides two states with very different maintainer effort:

- `recommend-close` is the agent's **active reject** — broken, abandoned,
  superseded, or clearly out of scope. The maintainer glances and closes.
- `recommend-triage` is for a PR whose **code is sound but whose merge/close call
  is a product or scope judgment the agent can't make** — a clean, working feature
  where the only open question is "does this project want it". The maintainer must
  stop and decide; that decision is theirs, not the agent's.

Folding the second into `recommend-close` would be dishonest — the agent does not
recommend closing a sound feature — and would bury the most expensive pile (the
product calls only the maintainer can make) inside the cheap one (rubber-stamp
closes). So the maintainer's world is three filters: an emerald ship queue
(`is:pr is:open label:recommend-merge`), an amber decision queue
(`label:recommend-triage`), and a red close pile (`label:recommend-close`).

`recommend-triage` is **not a cop-out hatch**. It is only for "code is sound, the
call is product/scope". If the agent has a *technical* reason the PR shouldn't
merge, it still owes a `recommend-close` with that reason in the review comment —
otherwise the decision queue swells with PRs the agent could have resolved and the
label loses its meaning.

The agent **never merges and never closes** — both stay the maintainer's hand;
the verdict is a recommendation, not an action. That is why all three labels lead
with `recommend-` rather than the ecosystem-conventional `ready-to-merge`: the
matched `recommend-merge` / `recommend-close` / `recommend-triage` set names them
honestly as recommendations, and — deliberately — steers clear of the label
strings merge bots watch (Kodiak,
Mergify, bors, GitHub auto-merge). A bot wired to merge on `ready-to-merge` would
turn the agent's recommendation into an actual merge and break this invariant, so
do **not** rename it back to that conventional string.

### Maintainer PR-verdict axis

GitHub prevents pull-request authors from approving their own PRs. A maintainer
who has reviewed a self-authored PR can record that distinct human decision while
CI is still pending:

| Label                 | Color    | Description (PR-scoped)                                      |
| --------------------- | -------- | ------------------------------------------------------------ |
| `maintainer-approved` | `0E8A16` | pr: Maintainer reviewed this head and approves merging after required checks pass |

This label records human acceptance, not merge readiness; required checks remain
authoritative, and the maintainer still performs the merge. An agent applies it
only after explicit maintainer direction and never infers it from an agent verdict,
green CI, or mergeability. It may coexist with a `recommend-*` label because the
two labels record different authorities.

Both verdict axes bind to one specific diff, so they go **stale** the moment the
PR changes. A new commit means the applicable verdict label must be cleared and
renewed by its authority. Pushes after a verdict are rare, so this stays a manual
step rather than something worth a CI workflow.

**A couple of label families are deliberately left out, because a *tool* already
owns them:**

- Tool-managed labels (`dependencies` from Dependabot, and other labels created
  by labeler actions or bots) are owned by that tooling. Leave their color and
  description alone; do not add them here or you will fight the tool that
  recreates them.
- `area:*` labels are per-repo (add them locally, ideally via path-based
  `actions/labeler`), so they do not belong in a shared cross-repo set.

The "still being worked" state is owned by GitHub's native **draft** flag, not a
label. A PR mid-iteration (including agent- or self-authored PRs, where the
author *is* the maintainer so review-request doesn't apply) stays a draft until
the agent has a verdict. So there is deliberately no `ready-for-maintainer` /
`ready-for-review` label: `recommend-merge` already *is* the "your turn to ship"
signal, and the draft flag already owns "not yet". The maintainer's "needs my
attention" filter is `is:pr is:open label:recommend-merge`.
`/sending-pull-request` opens autonomous PRs as draft for exactly this reason.

The same draft flag is why there is no `do-not-merge` label: a "don't merge this
yet" state is almost always temporary (a PR kept open to exercise CI, or one
mid-iteration), and that is precisely what draft expresses. A draft PR already
cannot be merged, so a separate flag would just be a second, redundant mechanism
for "not yet".

PR *type* and *area* stay absent: PR type comes from the conventional-commit
title, and area is per-repo. Only the PR *verdict* is shared here, because "is
this one mine to ship" generalizes across every repo with PRs. Each description
leads with a scope prefix — `issue:`, `pr:`, or `issue/pr:` — to advertise where
it applies, so tools and people don't cross-apply.

### Issue ↔ PR equivalents

Issues and PRs run the same underlying state machine — *whose turn is it, and
what must they do* — but express it with different signals. The PR side also
leans on GitHub's native draft flag. This table lines them up so a state reads
the same whether you're looking at an issue or a PR:

| State (whose turn / what's needed)     | Issue (triage role)                       | PR (verdict + draft flag)                 |
| -------------------------------------- | ----------------------------------------- | ----------------------------------------- |
| Fresh — agent must route or finalize   | no triage label                           | no verdict label, non-draft               |
| Blocked on an outside human            | `needs-info`                              | `needs-info` (same label, reused)         |
| Still being built / iterated           | *(no issue equivalent)*                   | **draft** flag                            |
| Agent's turn to act                    | `ready-for-agent`                         | no verdict label, non-draft               |
| Maintainer's turn — endorsed           | `ready-for-human` (human implements)      | `recommend-merge` (human reviews/merges)  |
| Maintainer's turn — must decide        | `needs-triage` (maintainer evaluates)     | `recommend-triage` (product/scope call)   |
| Maintainer accepted — checks/merge pending | *(no issue equivalent)*                | `maintainer-approved`                     |
| Won't proceed                          | `wontfix`                                 | `recommend-close`                         |

Three asymmetries are intentional, not gaps:

- **Fresh and `ready-for-agent` collapse into one PR state.** A non-draft PR
  with no verdict already means "agent, finalize this", so the PR side needs no
  separate routing label. On the issue side, no triage label means the agent
  must route the issue; `ready-for-agent` means it has passed that gate and is
  ready for implementation.
- **The maintainer's terminal action differs.** `ready-for-human` on an issue means
  *implement it*; `recommend-merge` on a PR means *review and merge it*. Same "your
  turn, human" role, different verb — which is why `ready-for-human` stays
  issue-only and `recommend-merge` is its PR counterpart rather than a shared label.
  Once that review is complete, `maintainer-approved` records the maintainer's own
  verdict and has no issue equivalent.
- **`needs-triage` spans two PR states.** On issues, "maintainer must evaluate" is
  one state. On PRs it splits by *when*: a fresh PR is the agent's to finalize
  (no verdict, non-draft), and only *after* the agent finalizes does a leftover
  product/scope call earn its own verdict, `recommend-triage`. That is why
  `recommend-triage` is a distinct PR label and the agent never puts `needs-triage`
  on a PR (that would invert it to "agent hasn't looked yet").

`do-not-merge` is absent on purpose: a "don't merge yet" PR is the **draft** row
above, so it needs no label of its own.

## Process

Detect, preview, confirm, apply, then document.

### 1. Detect the current repo

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

If that fails (no GitHub remote), ask the user which repo to target.

### 2. Preview (read-only)

Show the user which canonical labels are new vs already present on the repo, by
comparing the tables' labels against the repo's existing ones:

```bash
gh label list --repo "$REPO" --limit 200 --json name -q '.[].name'
```

Labels in the tables but not in that list will be **created**; labels already
present will have their color/description **updated**.

Also inspect `docs/agents/triage-labels.md` and the root `AGENTS.md`. Preview
whether the contract and its context pointer will be created, updated, or left
unchanged. Preserve unrelated existing instructions.

### 3. Confirm, then apply

Creating labels on a (often public) repo is an outward-facing action, so confirm
the complete label-and-documentation preview with the user first. Then create
each label from the tables with `--force`, which adds it if missing and updates
color/description if it already exists:

```bash
gh label create "type: bug"     --color d73a4a --description "issue: Reporting a defect to fix"                   --force --repo "$REPO"
gh label create "type: feature" --color a2eeef --description "issue: Requesting a new capability or improvement"  --force --repo "$REPO"
gh label create "type: task"    --color cfd3d7 --description "issue: For other work: maintenance, refactor, docs" --force --repo "$REPO"
gh label create "needs-triage"    --color fbca04 --description "issue: Maintainer needs to evaluate this issue"     --force --repo "$REPO"
gh label create "needs-info"      --color d876e3 --description "issue/pr: Waiting on reporter for more information" --force --repo "$REPO"
gh label create "ready-for-agent" --color 0e8a16 --description "issue: Fully specified, ready for an AFK agent"     --force --repo "$REPO"
gh label create "ready-for-human" --color 1d76db --description "issue: Requires human implementation"              --force --repo "$REPO"
gh label create "wontfix"         --color ffffff --description "issue: Will not be actioned"                       --force --repo "$REPO"
gh label create "recommend-merge"  --color 0E8A16 --description "pr: Agent finalized and endorses it: review and merge"   --force --repo "$REPO"
gh label create "recommend-close"  --color D93F0B --description "pr: Agent recommends closing: your call to review or close" --force --repo "$REPO"
gh label create "recommend-triage" --color FBCA04 --description "pr: Agent finalized it but the merge/close call is yours" --force --repo "$REPO"
gh label create "maintainer-approved" --color 0E8A16 --description "pr: Maintainer reviewed this head and approves merging after required checks pass" --force --repo "$REPO"
```

To set up several repos, repeat with each `--repo`.

### 4. Document the contract

Create or update `docs/agents/triage-labels.md` as the durable agent-facing
contract. Preserve unrelated repository-specific content. The document must:

- map the five standard issue triage roles to their exact label strings and
  meanings;
- name the `type:` axis and require each triaged issue to carry exactly one
  triage label and one type label; an issue with no triage label is fresh work
  for the agent to route, while `needs-triage` is reserved for a maintainer
  decision;
- document the three mutually exclusive agent PR verdicts, the explicit-human-only
  `maintainer-approved` verdict, the shared `needs-info` state, and the draft flag
  as the in-progress state;
- state that verdicts record decisions rather than merge or close, and that a new
  commit makes a verdict stale and requires removal and renewal by its authority.

Ensure the root `AGENTS.md` points to that file when issue triage, issue labels,
or PR verdict labels are involved. Add only the smallest contextual pointer;
do not copy the contract into `AGENTS.md`.

### 5. Report

Tell the user which labels were created vs updated and which documentation was
created vs updated. Non-canonical labels already on the repo are **left
untouched**. If they want to retire a stray label, that is a manual, deliberate
step: `gh label delete "<name>" --repo "$REPO" --yes`. Deleting strips it off
every issue/PR currently wearing it, so never do it without explicit
confirmation.

## Changing the set

Edit the tables above: add or remove a row, and keep the `gh label create` lines
in step 3 and the required agent-contract content in step 4 in sync. Keep the
set small: before adding a label, check it carries information the commit title,
diff, or an existing label (or another skill's labels) doesn't.
