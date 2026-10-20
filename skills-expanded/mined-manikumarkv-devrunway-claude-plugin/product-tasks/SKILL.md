---
name: product-tasks
description: Create GitHub milestones and issues from a product-plan doc. One milestone per epic. One issue per story with acceptance criteria and labels. Ask before assuming anything. Outputs docs/product-tasks/<slug>.md. Usage — /product-tasks <slug>
argument-hint: "<feature-slug>"
arguments:
  - name: slug
    description: "Feature slug — matches the product-plan doc filename"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash(find *)
  - Bash(ls *)
  - Bash(gh *)
---

# Product Tasks

Parse `$ARGUMENTS[0]` as the feature slug.

---

## Step 1 — Load the plan doc

```bash
find docs/product-plans/ -name "<slug>*.md" | head -3
```

Read the full plan doc. If not found, tell the user to run `/product-plan <slug>` first. Stop.

---

## Step 2 — Clarify before creating

Do NOT create anything yet. First ask every question that has no clear answer in the plan:

- **Milestone / release name** — what should the GitHub milestone be called? (suggest: `<epic-name>` or `v1.0 — <feature>`)
- **Due date** — is there a target date for any milestone? (or none)
- **Labels** — what labels should stories get? (suggest: `feature`, `epic:<name>`, `size:S`, etc.)
- **Assignees** — should any issues be pre-assigned?
- **Anything unclear in a story's acceptance criteria** — flag each one explicitly

Only ask questions that genuinely cannot be answered from the plan. Do not ask obvious things.

Wait for all answers before proceeding.

---

## Step 3 — Create milestones

For each epic in the plan, create a GitHub milestone:

```bash
# Check if milestone already exists
gh api repos/:owner/:repo/milestones --jq '.[].title'

# Create milestone (if not already present)
gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="<milestone-title>" \
  --field description="<epic-goal>" \
  --field due_on="<ISO-date or omit>"
```

Show the milestone title and URL. Confirm before creating if anything is uncertain.

---

## Step 4 — Create issues

For each story, create one GitHub issue:

```bash
gh issue create \
  --title "<Story Title>" \
  --body "$(cat <<'EOF'
## User Story
As a <persona>, I want <action>, so that <benefit>.

## Acceptance Criteria
- [ ] …
- [ ] …

## Size
<XS|S|M|L|XL>

## Source
docs/product-plans/<slug>.md — Story <epic>.<story>
EOF
)" \
  --label "feature" \
  --milestone "<milestone-title>"
```

After each issue is created, print: `✅ #<number> — <title>`

If creation fails, show the error and ask how to proceed. Do not silently continue.

---

## Step 5 — Write the task summary doc

Write to `docs/product-tasks/<slug>.md`:

```markdown
# Product Tasks: <Feature Name>
_Created: <today>_
_Source: docs/product-plans/<slug>.md_

## Milestones

| Milestone | Epic | GitHub Link |
|---|---|---|
| <name> | <epic> | <url> |

## Issues Created

| # | Story | Epic | Size | Status |
|---|---|---|---|---|
| #<n> | <title> | <epic> | S | Open |

## Next Steps
- Developers: pick up a story and run `/product-refine <issue-number>` for handoff
- To refine a story: `/product-refine <issue-number>`
```

---

## Step 6 — Done

> Tasks created. Summary saved to `docs/product-tasks/<slug>.md`.
>
> When a developer picks up a story, they can run:
> ```
> /product-refine <issue-number>
> ```
> to align on scope and acceptance criteria before development starts.
