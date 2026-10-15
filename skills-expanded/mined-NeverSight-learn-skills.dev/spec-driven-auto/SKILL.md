---
name: spec-driven-auto
description: Run the full spec-driven workflow automatically. Proposes, implements, verifies, reviews, and archives a change with one confirmation checkpoint.
version: 0.1.0
---

You are running the full spec-driven workflow end-to-end for a single change.

## Steps

1. **Assess complexity** — before doing anything, evaluate whether this change is suitable for the auto workflow:
   - Read `.spec-driven/config.yaml` for project context
   - Read `.spec-driven/specs/INDEX.md` and relevant spec files to understand the current system
   - Read the codebase files that the change will likely touch — estimate the number of files, modules, and cross-cutting concerns involved
   - **Reject if any of these are true:**
     - The change touches more than 3 modules or packages
     - The change requires modifying more than ~10 files
     - The change involves database schema migrations
     - The change affects authentication, authorization, or payment flows
     - The change requires coordinating across multiple services or repositories
     - The scope is vague or open-ended (e.g. "refactor the codebase", "improve performance")
   - If rejected, explain why and suggest using the step-by-step workflow (`/spec-driven-propose` → `/spec-driven-apply` → ...) instead
   - If suitable, proceed

2. **Propose** — run `/spec-driven-propose`:
   - Run `node {{SKILL_DIR}}/scripts/spec-driven.js propose <name>`
   - Fill all artifacts: proposal.md (with Unchanged Behavior), specs/ delta files, design.md, tasks.md (with ## Testing), questions.md (open questions)
   - Show the user a summary: scope, key decisions, task count, unchanged behaviors, and any open questions
   - **Wait for explicit confirmation** before proceeding — this is the only mandatory checkpoint
   - If questions.md has open questions, list them and ask the user to resolve them before confirming
   - If the user requests changes, apply them and re-confirm

3. **Apply** — implement all tasks:
   - Run `node {{SKILL_DIR}}/scripts/spec-driven.js apply <name>` to show task summary
   - Check questions.md for open `- [ ] Q:` entries — if any, ask the user and resolve before continuing
   - Work through each `- [ ]` task in order: read code, implement, verify Unchanged Behavior, mark `- [x]`
   - For `## Testing` tasks: actually run the tests and confirm they pass
   - Run `node {{SKILL_DIR}}/scripts/spec-driven.js apply <name>` to confirm `remaining === 0`

4. **Verify** — check completeness:
   - Run `node {{SKILL_DIR}}/scripts/spec-driven.js verify <name>`
   - If errors or CRITICALs: fix them automatically, then re-verify
   - If CRITICALs cannot be auto-fixed: stop and ask the user
   - Re-read delta spec files and update them to match what was actually implemented

5. **Review** — check code quality:
   - Read every file changed by this change
   - Check: readability, security, error handling, performance, best practices, test quality
   - MUST FIX issues: fix them automatically, then re-review
   - If MUST FIX issues cannot be auto-fixed: stop and ask the user
   - SHOULD FIX and NITS: fix if straightforward, otherwise note in the final report

6. **Archive** — close out the change:
   - List all delta files in `specs/` and merge each into the corresponding main spec file
   - Update `.spec-driven/specs/INDEX.md` if new spec files were created
   - Run `node {{SKILL_DIR}}/scripts/spec-driven.js archive <name>`
   - Report the final result: what was built, files changed, tests passing

## Rules
- The complexity check in Step 1 is mandatory — never skip it
- The user confirmation in Step 2 is mandatory — never skip it
- All other steps run automatically unless blocked by an unresolvable issue
- Follow all config.yaml rules (specs, change, code, test) throughout
- If anything goes wrong mid-flow, stop and explain — do not silently continue
- Mark tasks complete one at a time, not in bulk
