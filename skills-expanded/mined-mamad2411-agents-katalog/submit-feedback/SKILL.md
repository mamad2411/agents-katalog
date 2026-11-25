---
name: submit-feedback
trigger: /feedback
description: Package learnings and submit to the ADLC master repo
---

# Skill: Submit Feedback

## Trigger
`/feedback`

## Description
Package accumulated learnings from this project and submit them as a PR to the ADLC master repo.

## Master Repo
- URL: git@github.com:MikeMengell/ctolabs-adlc.git
- Feedback branch naming: `feedback/adlc-test-1-<YYYY-MM-DD>`
- Target directory in master: `feedback-inbox/`

## Inputs
None required. Reads `.claude/learnings.md`.

## Process
1. Read `.claude/learnings.md` and identify entries not yet submitted
2. Format the feedback file:
   ```
   # Feedback: adlc-test-1
   Date: YYYY-MM-DD
   Project Type: web-app
   Tech Stack: TypeScript, React, Node.js
   Maturity Level: 4

   ## Learnings
   [entries from learnings.md]

   ## Suggested Changes
   [any specific methodology improvements identified]
   ```
3. Clone the master repo: `git clone --depth 1 git@github.com:MikeMengell/ctolabs-adlc.git /tmp/adlc-feedback-<random>`
4. Create branch: `git checkout -b feedback/adlc-test-1-<YYYY-MM-DD>`
5. Write the feedback file to `feedback-inbox/adlc-test-1-<YYYY-MM-DD>.md`
6. Commit and push the branch
7. Create a PR using `gh pr create`
8. Clean up the temp directory
9. Mark submitted learnings in `.claude/learnings.md`

## Output
A PR against the master repo containing the feedback.

## Autonomy
- Tier 2: submitting feedback to master (requires approval)

## Error Handling
- If git clone fails: report the error and suggest checking SSH key access
- If no new learnings exist: inform the user, do not create an empty PR
