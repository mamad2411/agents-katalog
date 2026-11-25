---
name: t3-feature-check
description: Checks whether T3 Code (pingdotgg/t3code) supports a feature, keybinding or setting by reading its docs, keybindings contract and source, then finds existing issues, discussions and PRs and votes or comments on them. Use when asked "does T3 Code support X", "is there a keybind for X in T3", "har T3 støtte for", or to request a T3 Code feature.
---

# T3 Feature Check

Answer from the source on `main`, not from memory. T3 Code ships often.

Repo: `pingdotgg/t3code`. Work in the scratchpad.

## 1. Read the docs

```bash
gh api repos/pingdotgg/t3code/contents/docs/user --jq '.[].name'
gh api repos/pingdotgg/t3code/contents/docs/user/<file>.md --jq .content | base64 -d
```

Pick files by name (`composer.md`, `keybindings.md`, `terminal.md` ...) and grep them for the feature's UI label and synonyms.

## 2. Read the code

```bash
git clone -q --depth 1 --filter=blob:none --sparse https://github.com/pingdotgg/t3code t3
cd t3 && git sparse-checkout set packages/contracts packages/shared apps/web/src
```

- **Keybindings:** `packages/contracts/src/keybindings.ts` lists every command that can be rebound. A missing command means it cannot be bound in Settings → Keybindings.
- **Settings:** grep `packages/contracts/src` for the setting name.
- **UI:** grep `apps/web/src` for the button label or `aria-label`, then read the component's `onKeyDown` and `addEventListener("keydown"` handlers. Hidden keyboard paths (such as `Tab` to focus, then `Enter`) live there and are often undocumented.

Done when you can say: supported / not supported, which setting or command is involved, and any workaround, each with a `file:line` reference.

## 3. Find existing demand

Run all three. `gh search issues` does not cover discussions.

```bash
gh search issues --repo pingdotgg/t3code "<terms>" --limit 10   # issues
gh search prs --repo pingdotgg/t3code "<terms>" --limit 10      # PRs
gh api graphql -f query='{search(query:"repo:pingdotgg/t3code <terms>",type:DISCUSSION,first:10){nodes{...on Discussion{number title url closed upvoteCount}}}}'
```

Try two or three phrasings. Read the strongest hits' bodies: they link related PRs and discussions. Note each one's state (open, merged, upvotes, last update).

## 4. Report

Lead with the answer. Then the workaround, then a table of existing threads with links and state. Offer the actions in step 5. Do not act yet.

## 5. Vote, comment or request (only after the user says yes)

Prefer adding to an existing thread over creating a duplicate.

```bash
# Upvote a discussion
ID=$(gh api graphql -f query='{repository(owner:"pingdotgg",name:"t3code"){discussion(number:N){id}}}' --jq .data.repository.discussion.id)
gh api graphql -f query="mutation{addUpvote(input:{subjectId:\"$ID\"}){subject{upvoteCount}}}"
# 👍 on an issue or PR (same endpoint for both)
gh api -X POST repos/pingdotgg/t3code/issues/N/reactions -f content=+1
# Comment
gh issue comment N --repo pingdotgg/t3code --body '...'
```

A comment must add something the thread lacks, such as a use case or a requirement (for example, "make it rebindable, not only a fixed key"). Write it in English. A bare "+1" belongs in a reaction.

With no existing thread: feature requests go to Discussions → **Ideas** (blank issues are disabled, and `config.yml` routes features there). Bugs use `.github/ISSUE_TEMPLATE/bug_report.yml`. Show the draft to the user before posting.

Finish with links to everything you voted on, commented on or created.
