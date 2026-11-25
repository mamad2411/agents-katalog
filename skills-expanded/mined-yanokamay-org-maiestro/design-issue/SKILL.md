---
name: design-issue
description: Turn a thinly-described GitHub issue into a concrete implementation plan written back to the issue, with sub-issues if the work spans multiple tracks. Stops before implementation.
allowed-tools: Bash(gh *) Bash(git *) Bash(grep *) Bash(find *) Bash(ls *) Read Write
---

You are designing the issue, not implementing it. Stop after the issue body is updated. The user will trigger implementation in a separate session.

The repo is the current working directory's GitHub remote.

## Procedure

1. **Resolve the issue ID.** If the user provided an issue number, use it. Otherwise, parse the current branch name (`git branch --show-current`) to extract the issue number — branch names follow the pattern `<anything>/<number>-<slug>` (e.g. `feature/13-add-pr-link-pill` → `13`). If no number can be found in the branch name, ask the user for the issue ID before continuing.

   **Fetch the issue.** `gh issue view <id>`. Treat the body as raw intent — it's typically one or two sentences and missing structure.

2. **Investigate before designing.** A plan written without reading the code becomes generic and wrong. Spend tool calls on:
   - `CLAUDE.md` for architecture, conventions, and the recorded design decisions, and `docs/` for the per-feature reference (settings, health check, session status, theming, tool resolution).
   - The files most likely to change. mAIestro Code is split into `backend/` (Rust/Tauri) and `frontend/` (web) — read enough of both to know exact paths and the surrounding patterns.
   - Similar features that already exist in the repo — copy their shape rather than inventing.
   Do not skip this step even when the issue feels obvious. The investigation is what makes the plan useful.

3. **Reconsider the title.** A vague title ("Add a dialog to suggest upgrade") often hides what the issue is actually about. After investigating, judge whether the existing title accurately describes the change you've planned. If a sharper title would help (more specific, better scoped, fewer filler words), propose a new one and include it in the draft you show the user. If the existing title is already good, leave it alone — don't rewrite for its own sake.

4. **Draft the plan.** Use this structure (skip sections that don't apply):

   - **Goals** — clarified scope in 2–4 bullets. Distinguish soft vs. hard behaviors, backend vs. frontend responsibilities, etc.
   - **Design** — concrete shapes: Tauri command signatures, frontend component/module names, file paths under `backend/`/`frontend/`, data flow. If the work crosses the backend/frontend boundary, give each side its own subsection.
   - **Configuration** — new settings, per-repo or per-profile config (`~/.maiestro/`), defaults. Note where they're read and where they're documented (`docs/settings.md`).
   - **Out of scope** — explicitly list things a reader might assume are included but aren't. This is the most undervalued section: it prevents scope creep and aligns expectations.
   - **Implementation steps** — numbered. If split into sub-issues, group steps under each sub-issue heading.
   - **Manual prerequisites** — if the issue involves steps that must be completed outside the repo (e.g. creating accounts, configuring third-party dashboards, generating tokens, code-signing certs), list them as a GitHub task checklist (`- [ ]`). This gives the implementer trackable progress and makes it obvious what must happen before the code work begins.
   - **Acceptance criteria** — verifiable. Mention `cargo build` / `cargo clippy` / `cargo test` for the backend and the frontend's build/lint as appropriate.

5. **Decide whether to split.** Create sub-issues when:
   - Work spans the backend/frontend boundary in a way that can be implemented and reviewed independently (e.g. a new Tauri command + the UI that calls it).
   - The tracks have a clean dependency boundary (one ships independently of the other, even if not in parallel).
   Do **not** split if the work is one cohesive change on a single side — sub-issues add overhead, not value. One issue with a numbered checklist is fine.

6. **Show the draft to the user before writing.** Output the proposed title (if changed) and body in the chat and ask for approval. Call out 1–3 design choices that are non-obvious or reversible (e.g. "per-repo setting vs. global", "soft-fail on network error"), so the user can redirect cheaply before the issue is edited.

7. **Write the issues with `gh`.** Once approved:

   **Designing an existing issue, no split** — update the body (and optionally the title) in place:
   ```bash
   gh issue edit <number> --title "…" --body-file tmp/issue-body.md
   ```
   Author the body with the `Write` tool to a temp file and pass it via `--body-file` so multi-line markdown survives intact.

   **Existing issue + new sub-issues** — create each sub-issue, then update the parent body to reference them by number:
   ```bash
   gh issue create --title "…" --body-file tmp/sub-1.md   # note the returned number
   gh issue edit <parent> --body-file tmp/parent-body.md   # body cites the new sub-issue numbers
   ```
   GitHub's native sub-issue linking is not exposed by `gh` directly — link them in the parent body with a task checklist (`- [ ] #<sub-number>`).

   Read each command's output for the issue number + URL — that's your confirmation.

8. **Stop.** Do not start implementation. End the turn with a one-line summary of what was created and ask the user whether to proceed with the first sub-issue.

## Pitfalls

- **Don't paste the original issue text verbatim** at the top of the rewritten body and then append your plan — replace the body. Keep one source of truth.
- **Don't add an "Implementation notes" section that prescribes specific code.** The plan describes the shape of the change; the implementer chooses the lines. Concrete file paths and command signatures are good; literal code blocks of the proposed implementation are usually too much.
- **Don't skip "Out of scope".** It is the cheapest insurance against the implementer doing more than asked.
- **Use `--body-file`, not `--body`,** for anything multi-line — inline `--body` mangles markdown and newlines.
