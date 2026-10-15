---
name: autocraft
description: >
  Use when the user says "autocraft", "build journeys", "test the spec", or "cover my spec".
  Also use when the user has a spec.md and wants automated implementation with real output
  verification. Supports UI projects (screenshot-verified), integration-only projects
  (pipeline-verified), and test refactoring tasks.
  Use "autocraft init" to install the always-on Analyst into a project via CLAUDE.md.
argument-hint: "[spec-file-path | init]"
---

# Autocraft

Five agents. Strict roles. No self-grading. Human in the loop.

```
Human ◄──► Analyst (foreground agent)
               │
               ├──► spec.md (writes/updates)
               ├──► .autocraft/feedback-log.md (routes feedback)
               │
               ▼
           Orchestrator (you) ──► Builder (background agent)
                              ──► Tester (background agent)
                              ──► Inspector (foreground agent)
```

The **Analyst** talks to the human, collects feedback, writes and updates spec.md, and routes actionable feedback to the right agent. → [analyst.md](analyst.md)
The **Builder** implements features but CANNOT write tests, review its own work, grade itself, or commit. → [builder.md](builder.md)
The **Tester** writes journey tests but CANNOT modify production code. They only read it to understand what to test. → [tester.md](tester.md)
The **Inspector** verifies output with automated scans and subjective review. Only the Inspector can set "polished." → [inspector.md](inspector.md)
The **Orchestrator** manages handoffs and commits only when the Inspector approves. → [orchestrator.md](orchestrator.md)

**Why this separation matters:** A builder who writes their own tests optimizes for tests that pass — not for tests that prove features work. A separate tester reads the contract, exercises the pipeline, and checks what came out. If the output is wrong, they write a failing test — and the builder has to make it pass.

---

## When to Use

- Building a new app or feature set from a spec with multiple acceptance criteria
- You want automated, verified proof that every criterion is met (screenshots for UI, test results for integration)
- The project needs real implementations (not stubs) with independent test verification
- Consolidating or refactoring tests into scenario-based integration tests
- Building or testing CLI tools, libraries, or APIs where data pipeline correctness matters
- You have a `spec.md` (or gist) describing requirements and acceptance criteria

## When NOT to Use

- **Single-file bug fixes** — just fix the bug directly
- **Quick prototyping** where stubs are acceptable
- **No spec yet** — start with the Analyst step or write spec.md first

## Project Mode

The Orchestrator detects the project mode at startup and records it in `.autocraft/journey-loop-state.md`:

| Mode | When | UI test contract | Integration test contract | Screenshots |
|------|------|-----------------|--------------------------|-------------|
| `ui` | Project has a UI framework AND spec describes user-visible behavior | Yes | Optional (when silent failure risks detected) | Required |
| `integration` | No UI, or spec describes data pipelines, APIs, test refactoring, or library behavior | No | Yes (primary contract) | Not required |

**Detection rules (in order):**
1. If `spec.md` contains `mode: integration` or `mode: ui` in frontmatter → use that
2. If the task is test refactoring → `integration`
3. If the project has no UI framework and no UI test target → `integration`
4. Otherwise → `ui`

**What changes in `integration` mode:**
- Builder: **skipped** if no production code changes needed
- UI test contract: **skipped**
- Integration test contract: **always generated** — primary contract
- Timing Watcher: **skipped**
- Inspector: **skips screenshot review**, focuses on objective scans + assertion honesty

---

## Inputs

**Special command:** If `$ARGUMENTS` is `init`, run the init flow instead of the build loop:

1. Copy `{skill-base-dir}/claude-md-template.md` to `CLAUDE.md` in the user's project root
2. Create `.autocraft/` directory if it doesn't exist
3. Tell the user: "Analyst is now always-on in this project. Just talk naturally — I'll handle specs, feedback routing, and build triggers automatically."
4. **Do not start the build loop.** Return immediately.

If `CLAUDE.md` already exists, append the Analyst section under a `# Autocraft Analyst` heading instead of overwriting.

---

Spec source: $ARGUMENTS (defaults to `spec.md` in current directory)

**Gist support:** If `$ARGUMENTS` is a GitHub gist URL or gist ID, the spec lives in the gist instead of a local file.

**Detection rules:**
- Starts with `https://gist.github.com/` → gist URL. Extract gist ID from the last path segment.
- Matches `/^[a-f0-9]{20,}$/` → bare gist ID.
- Otherwise → local file path.

```bash
# Read spec from gist
gh gist view <gist-id> -f spec.md

# Update spec in gist (Analyst only) — non-interactive
gh api --method PATCH /gists/<gist-id> \
  -f "files[spec.md][content]=$(cat /tmp/spec-updated.md)"

# If gist has no file named spec.md, list files first:
gh gist view <gist-id> --files
```

**Error handling:** If `gh gist view` fails, print the error, ask the user to verify the gist URL and run `gh auth status`, and do not proceed until the spec is readable.

The Orchestrator detects the source type at startup and stores it in `.autocraft/journey-loop-state.md` as `Spec source: gist:<gist-id>` or `Spec source: file:<path>`. All agents read the spec through a consistent method — the Orchestrator fetches the latest content and includes it in each agent's prompt. The Analyst writes spec updates to a temp file then pushes via `gh api`.

---

## Shared State Files

| File | Written by | Read by |
|------|-----------|---------|
| `.autocraft/journeys/*/` | Builder (code), Tester (tests+screenshots) | Inspector, Orchestrator |
| `.autocraft/journeys/*/test-contract.md` | **Orchestrator** | **Tester** (implements it), Inspector (validates against it) |
| `.autocraft/journeys/*/integration-test-contract.md` | **Orchestrator** | **Tester** (implements unit tests), Inspector (validates) |
| `/tmp/autocraft-screenshots/{journeyName}/*.png` | Tester (snap/waitAndSnap) | Orchestrator (copies to project dir post-test with dedup) |
| `.autocraft/journey-state.md` | Tester (`needs-review`), Inspector (`polished`/`needs-extension`) | All |
| `.autocraft/journey-refinement-log.md` | Inspector | Orchestrator |
| `.autocraft/journey-loop-state.md` | Orchestrator | Orchestrator (resume) |
| `AGENTS.md` (repo root) | Inspector | Builder, Tester (each restart) |
| `.autocraft/feedback-log.md` | Analyst | Orchestrator, Builder, Tester, Inspector |

---

## Playbooks

Playbooks are shared, platform-specific knowledge bases stored as GitHub gists. The Orchestrator fetches them once per invocation and injects the content directly into each agent's prompt (see [orchestrator.md](orchestrator.md) Step 2).

Default registry gist: `bca7073d567ca8b7ba79ff4bad5fb2c5`. Override via `.autocraft` file at repo root. See [playbooks.md](playbooks.md) for full registry management, CRUD commands, entry format, and auto-fork behavior.

---

## Orchestrator Protocol

The full 12-step orchestrator protocol — including agent launch directives, test contract generation, compliance validation, and the build loop — is in **[orchestrator.md](orchestrator.md)**.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Test contract assertions too strict for current implementation stage | Write contracts that match what's testable now, tighten in later iterations |
| Screenshots show permission dialogs (UI mode) | Run `/preflight-permissions` first to grant all TCC permissions |
| Loop stalls with no progress for multiple iterations | Stall detection: if no changes for 2 iterations, re-launch with Inspector's last failure list |
| Playbook gist update fails with 403/404 | Auto-fork triggers automatically — see [playbooks.md](playbooks.md) |

---

## Optional External Skills

These skills enhance autocraft but are not required. If not installed, autocraft works without them.

| Skill | Used by | Purpose |
|-------|---------|---------|
| `/frontend-design` | Inspector (via Orchestrator) | Design principles for screenshot review. If missing, Inspector uses general design judgment. |
| `/attack-blocker` | Builder | Structured approach to resolving permission/hardware blockers. If missing, Builder reports blockers to Orchestrator directly. |
| `/preflight-permissions` | User (before first run) | Grants macOS TCC permissions. Bundled in this repo. |
