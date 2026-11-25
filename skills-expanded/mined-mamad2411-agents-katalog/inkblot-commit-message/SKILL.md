---
name: inkblot-commit-message
description: Inkblot git commit message convention. Use when writing a commit message, creating a git commit, amending a commit message, or when the user asks how to format a commit subject.
---

# Inkblot commit messages

This convention is **only required when the work has a Jira ticket**. If there is no ticket, do not invent an ID, do not ask for a ticket, and do not restrict the subject.

## Ticket work (required)

```text
<TICKET-ID>: <Concise imperative summary>
```

1. Full Jira key, **uppercase**, **one** ticket per commit (e.g. `POD2-2291`, not `pod2-2291` and not `2-2291`)
2. Colon and space after the key, then an imperative summary (“Fix …”, “Add …”, “Rename …”)
3. Sentence case. One line. Aim for ~72 characters. Say the outcome, not a file list.
4. Put the ticket **this commit** belongs to in the subject — not every ticket on the PR, and not always the branch name.

Do **not** use Conventional Commits prefixes (`feat:`, `fix:`, `chore:`). The ticket is the classifier.

### Multiple tickets on one piece of work

A branch/PR may list several tickets. Each commit still has **one** key: the ticket that commit implements or fixes.

- Default to the branch ticket (`pod2-2291-…` → `POD2-2291: …`) when the commit is for that work.
- If this commit is for a different linked ticket, switch the subject to that key.
- If it is unclear which ticket this commit belongs to, ask. Do not invent an ID and do not stack keys (`POD2-2276-2277: …`).

Example — branch `pod2-2276-restrict-provider-access`, also linked to `POD2-2277`:

- `POD2-2276: Restrict availability reserved-for-client`
- `POD2-2277: Hide estimates from unauthorized clients`

### Examples

- `POD2-2291: Fix no-show video call outcome`
- `POD2-2291: Baseline the false-positive Brakeman role warning`
- `POD1-3452: Rename renewal date service to resolver`
- `POD1-3452: Guard missing specialized renewal periods`

### Body

No rule. Do not require a body and do not add one unless the user asks. Context lives in Jira.

### Do not (ticket work only)

- `feat: add renewal dates` / `fix: …` — no Conventional Commits
- `pod2-2291: Fix no-show …` — uppercase the key in commits
- `2-2291: Fix no-show …` — not a Jira key
- `POD2-2291 - fix stuff` — use `: `, not ` - `
- `POD2-2291: Fixed bug` — prefer imperative (`Fix …`)
- `POD2-2276-2277: …` — one primary ticket in the subject
- Inventing a ticket ID

### Validation (for hooks / lint)

```text
^[A-Z][A-Z0-9]+-[0-9]+: .+
```

## No ticket

No subject rule. Merge commits, syncs, and other untracked work can use any subject.

## Why

- **Ticket in the subject:** Jira Smart Commits and GitHub–Jira linking read the commit subject. The branch name is not enough.
- **Uppercase here, lowercase on branches:** Trackers expect the canonical `POD2-2291:` form. Branches stay lowercase to avoid git case-sensitivity.
- **No `feat:` / `fix:`:** The ticket already classifies the work. Two prefixes only make the subject longer.
- **Rule only when a ticket exists:** Same as branches. Do not block chores, merges, or hotfixes that have no ticket.
- **One ticket per commit, not per branch:** Jira attaches the commit to the key in the subject. If one PR covers several tickets, each commit should land on the ticket it actually changes. Stacking IDs in the subject breaks grep, hooks, and that attachment.
- **No body convention:** The ticket already has context. A second paragraph in git does not help Jira linking and is easy for agents to invent.
