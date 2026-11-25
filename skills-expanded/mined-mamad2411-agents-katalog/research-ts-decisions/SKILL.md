---
name: research-ts-decisions
description: Research why the TypeScript team made a specific typing decision. Use when evaluating whether ts-reset should override a built-in type, or when triaging issues that propose type changes. Searches the microsoft/TypeScript repo for relevant issues, PRs, and team comments.
user-invocable: true
---

# Research TypeScript Team Decisions

When evaluating whether ts-reset should override a TypeScript built-in type, research what the TypeScript team has said about it. Understanding their reasoning lets us make informed decisions — either agreeing with their trade-off or deliberately choosing a different one.

## Who to look for

**Ryan Cavanaugh** (`@RyanCavanaugh`) is the TypeScript project lead and usually the one making final verdicts on typing decisions. His comments carry the most weight. Also look for comments from:

- **Daniel Rosenwasser** (`@DanielRosenwasser`) — TS program manager
- **Anders Hejlsberg** (`@AHejlsberg`) — original designer
- **Nathan Shively-Sanders** (`@sandersn`)

## How to search

### Step 1: Search GitHub issues directly

Use `gh` to search the microsoft/TypeScript repo. Try multiple queries — the issue might be about the specific method, the return type, or a broader pattern:

```bash
# Search issues by title/body
gh search issues --repo microsoft/TypeScript "Object.create return type" --limit 20

# Search with broader terms if the first query is too narrow
gh search issues --repo microsoft/TypeScript "Object.create" --limit 20
```

### Step 2: Find team member comments

Once you have candidate issues, fetch comments and filter for TypeScript team members:

```bash
# Get Ryan's comments on a specific issue
gh api repos/microsoft/TypeScript/issues/{number}/comments \
  --jq '.[] | select(.user.login == "RyanCavanaugh") | {html_url, body}'

# Check for team comments more broadly
gh api repos/microsoft/TypeScript/issues/{number}/comments \
  --jq '.[] | select(.user.login == "RyanCavanaugh" or .user.login == "DanielRosenwasser" or .user.login == "sandersn" or .user.login == "ahejlsberg") | {user: .user.login, html_url, body}'
```

### Step 3: Check for reverted PRs

Many typing decisions were tried, broke things, and got reverted. This history is critical:

```bash
# Search for PRs related to the topic
gh search prs --repo microsoft/TypeScript "Object.create" --limit 20

# Check if a PR was later reverted
gh api repos/microsoft/TypeScript/pulls/{number} --jq '{title, state, merged_at, body}'
```

### Step 4: Search for related issues

TypeScript team members often state general principles on tangentially related issues. If the specific method doesn't have much discussion, search for related patterns:

```bash
# Example: if researching Object.create, also check Object.getPrototypeOf,
# or broader topics like "prototype typing" or "returns any"
gh search issues --repo microsoft/TypeScript "Object.getPrototypeOf any" --limit 10
```

### Step 5: Web search as fallback

If GitHub search doesn't surface enough, use web search:

```
site:github.com/microsoft/TypeScript "Object.create" RyanCavanaugh
```

## What to report

Structure your findings as:

1. **Timeline** — chronological list of relevant issues and PRs, with links
2. **Key quotes** — direct quotes from team members, with permalink URLs to the specific comments (not just the issue)
3. **The reasoning** — summarize why the current typing exists
4. **Was it tried before?** — note any attempts to change it that were reverted or rejected, and why
5. **Relevance to ts-reset** — does this fall in ts-reset's sweet spot, or is the current typing a deliberate trade-off?

Always include direct permalink URLs to specific comments, not just issue URLs. Use the `html_url` field from the GitHub API.

## Common patterns in TS team reasoning

These recurring arguments come up frequently. Knowing them helps you search more effectively and contextualize what you find:

- **"`any` can never be wrong, just less right"** — Ryan's principle that `any` is a safe default that never produces false errors
- **Breaking changes** — the TS team is very cautious about changing return types that would break existing code
- **"Soundness is not a goal"** — TypeScript explicitly prioritizes practical usability over type-theoretic correctness
- **Prototype vs own properties** — methods dealing with prototypes are hard to type because TS's type system doesn't distinguish prototype properties from own properties
- **`PropertyDescriptorMap` is untyped** — any API that takes property descriptors can't carry type information through them
