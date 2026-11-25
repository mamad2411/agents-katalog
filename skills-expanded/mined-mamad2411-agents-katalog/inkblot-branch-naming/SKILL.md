---
name: inkblot-branch-naming
description: Inkblot git branch naming convention. Use when creating a branch, checking out a feature/bugfix branch, naming a PR branch, or when the user asks to start work on a Jira ticket.
---

# Inkblot branch naming

This convention is **only required when the work has a Jira ticket**. If there is no ticket, do not invent a prefix, do not ask for a ticket, and do not restrict the name.

## Ticket work (required)

The branch **starts with the full Jira key, lowercase**. Do not add `feat/` / `fix/` / `feature/` type prefixes.

```text
<ticket-id>-<short-kebab>
```

1. Full key, lowercase, **one** primary ticket (e.g. `pod2-2291`, not `2-2291`)
2. kebab is lowercase, **3–5 words** — the change, not the ticket title
3. Keep the whole name short enough to read in GitHub’s branch list (~50 characters)

### Examples

- `pod2-2291-video-call-no-show`
- `pod1-3452-company-renewal-dates`
- `pod1-3459-coaching-duration-options`

### Do not (ticket work only)

- Do not prefix the ticket ID (`fix/pod2-2291-…`, `feat/…`, `feature/…`, `bf-…`)
- Do not shorten the project key (`2-2291-…`, `1-3452-…`)
- Do not use uppercase in the branch name (`POD2-2291-…`)
- Do not put initials in the name (`ji-pod1-2178-…`)
- Do not append the target env (`-qa`, `-master`)
- Do not stack ticket IDs (`pod2-2276-2277-2282-…`) — use the primary ticket
- Do not dump the full Jira title into the kebab

## No ticket

No naming rule. `hotfix/7.54.2`, `sync/…`, `qa-kuma`, or any other name are all fine.

## Why

- **Ticket-first, no type prefix:** Jira and `git grep` need the key at the start. `feat/` / `fix/` only adds length.
- **Full key, lowercase:** `pod2-2291` is still the Jira key (linking works). Lowercase avoids macOS vs Linux case-sensitivity. `2-2291` is not a Jira key, so GitHub/Jira will not attach the branch.
- **Rule only when a ticket exists:** Chores, syncs, and hotfixes without a ticket should not be blocked or renamed by the agent.
- **Short kebab:** GitHub truncates long branch names; the ticket title already lives in Jira.
