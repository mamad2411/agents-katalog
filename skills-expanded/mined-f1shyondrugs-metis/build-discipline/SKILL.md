---
name: build-discipline
description: "L3 engineering discipline for Metis build tasks: plan-first, skills-first, proven libraries, no-AI-slop checks, verify-before-claim. Use for any /build or implementation task."
priority: high
---

# Build Discipline — L3 Standard

This skill defines the working standard for implementation tasks. It exists
because models skip hard parts, rebuild what already exists, and claim success
without evidence. Every rule below is checkable.

## 1. Plan first — always

Before writing any file in a build task:

1. Read the relevant code first. `repo_search` / `read_file` the exact files
   you will touch — never patch blind from an error message.
2. For 3+ steps: `write_todos` FIRST, then work the list.
3. For bigger features: draft the plan in-chat (files, touch points, tests,
   deploy steps), get the shape right, THEN execute. Plan mode exists for
   exactly this; agent mode executes it.
4. Scope discipline: implement what was asked. No speculative refactors, no
   "while I'm at it" changes. If you notice an adjacent problem, report it,
   don't fix it silently.

## 2. Skills-first, proven libraries over rebuilds

- Before implementing any non-trivial capability, check `list_skills` and the
  MCP registry (`search_tools`) for an existing, proven implementation.
  `ensure_capability` provisions a registry server when it beats hand-rolling.
- NEVER hand-roll what a maintained library does: auth, parsing, crypto,
  charts, UI primitives. Search first, adopt, then customize.
- When adding a dependency, prefer: already in the project > well-known
  library > registry MCP server > hand-rolled code (last resort).
- When you adopt a library, read its actual API (context7_query) instead of
  guessing call signatures from memory.

## 3. The no-slop gate (UI work)

UI changes get a hard quality gate. Banned without explicit user request:

- gradient text, glow/aurora effects, purple-cyan AI aesthetics
- marketing filler copy ("Monitor your X in real-time")
- card-in-card layouts, >2 border-radius values, gray-on-gray text
- missing empty/loading/error states on any data view
- random buttons/icons the user did not ask for

Every view needs: a real empty state, a real loading state, a real error
state. Placeholder text is a defect, not a TODO.

## 4. Verify before you claim — the ledger rule

A claim without evidence is a defect. After implementation:

- Never write "done", "works", "tests pass", "is running" without proof.
- Run the actual verification (`verify_work` tool with expect-markers, or a
  test command) and cite the real output.
- If verification fails, say so plainly and fix it — don't restate the claim
  louder.
- Deploy/restart claims need artifact evidence: BUILD_ID mtime, service
  ActiveEnterTimestamp, HTTP status — not exit codes alone.

## 5. Parallelism (L3 speed trick)

Independent workstreams can run as parallel subagents (`delegate_subagent`),
2–3 concurrent max. But: parent verifies the children's claims by re-running
their key commands — subagent summaries are self-reports, not facts.

## 6. Definition of done

ALL of these, or it is not done:

1. Implemented exactly the requested scope
2. Type check + relevant tests executed and green (cite output)
3. Verification ledger clean (`verify_work` / equivalent real command)
4. If deployed: service restarted AND artifact-verified
5. Report states what was verified — and what was NOT tested
