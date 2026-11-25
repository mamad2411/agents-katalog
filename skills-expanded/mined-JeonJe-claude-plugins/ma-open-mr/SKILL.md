---
name: ma-open-mr
description: MA 파이프라인의 GitHub PR / GitLab MR을 리뷰어 우선 description·명시적 ownership·멱등 lookup·증적 기반 상태로 생성하거나 재바인딩한다. "ma-open-mr", "MR 올려줘", "PR 올려줘" 요청 또는 MA Phase 6에서 사용.
---

# MA open PR/MR

Create or bind every approved project's PR/MR, then persist evidence that Phase 6 can recheck. Never treat a URL or human-formatted CLI output as proof — use provider JSON (`gh ... --json`, `glab ... -F json` / API) for every metadata claim. Deterministic contract scripts are not included in v1; perform each stated validation yourself before proceeding.

## Invocation

```text
/ma-open-mr ISSUE-KEY [--project PROJECT] [--draft] [--auto]
```

Without `--project`, process all projects in canonical approval. A partial run may save valid project evidence, but Phase 6 stays incomplete until the approved and recorded project sets match exactly.

## References index

| File | When to read |
|---|---|
| [references/diagrams.md](references/diagrams.md) | Step 2 — only when a diagram materially helps the body |
| [references/gitlab-uploads.md](references/gitlab-uploads.md) | Step 2 — GitLab UI uploads, only with real UI evidence |

## Canonical inputs

Read `{stateRoot}/ISSUE-KEY/state.json` and the workspace config.

- Require `gates.implementationApproval.status == "approved"` and use only `gates.implementationApproval.projects[project].{base,target}`.
- Require the exact same project set in `state.worktrees`; each entry supplies `path`, `base`, and `target`.
- Require workspace `platform` to be `github` or `gitlab`, the path to be a real Git worktree root on `target`, and `origin` to match the eventual PR/MR URL.
- Expand only a leading `~/`. Reject shell syntax, control characters, missing paths, branch drift, extra projects, and duplicate paths. Never use `eval`.

## Ownership policy

Resolve policy from `approval.projects[project].mrPolicy`, then the workspace config project `mrPolicy`, then the top-level `mrPolicy`. Approval has precedence.

```json
{"mrPolicy":{"assignee":"alice","reviewers":["bob"],"reviewRequired":true}}
```

- Assignee may default to the authenticated author (`gh api user` / `glab api user`).
- Review is required by default. Resolve reviewers from explicit state/config; when none is configured, the reviewer defaults to the MR author (single-operator self-review model). Each reviewer must be a stable username; self-review by the author is permitted.
- Only an explicitly approved `reviewRequired:false` permits no reviewer.
- In `--auto`, halt when a reviewer is rejected by the provider or absent from the MR after creation. Never fabricate a reviewer other than the author default.
- Re-query the provider right after creation to confirm assignee/reviewers are non-empty — the omission is silent otherwise.

## Workflow

Repeat the following for every selected project.

### 1. Validate and push the feature branch

Confirm the worktree branch equals approved `target`, has commits relative to approved `base`, and is not a protected base branch. Push with hooks enabled:

```bash
git -C "$WORKTREE" push -u origin "$TARGET"
```

Halt on authentication, hook, or push failure. Never force push or use `--no-verify`.

### 2. Allocate and validate the body

Allocate this absolute, project-scoped file before writing:

```text
{stateRoot}/ISSUE-KEY/phase6/PROJECT/body.md
```

Write a reviewer-first body from the PRD/design, Phase 5 review feed, its summarized dispatch/E2E evidence, production-only diff stat, and public tracker/provider links. Treat `review-result.md` as the verdict owner; consult the raw E2E result only to resolve a missing evidence summary, not to create a second acceptance judgment. Use these sections, omitting only inapplicable optional sections:

1. `TL;DR`: problem, core change, observable effect.
2. `Root cause and solution`: plain-language mechanism for non-obvious behavior.
3. `Review points`: risky decisions and exact production files.
4. `Risk and impact`: user/API/data/operations/rollback effects.
5. `Verification`: DoD/scenario, result, command/method, concise evidence.
6. `UI evidence`: optional uploaded or public links only.
7. `Changed files`: production diff only; exclude handoff/tool/meta documents.
8. `Related`: public links only.

Do not make commit lists the change summary. Never publish internal-only paths or secrets in the body: local workspace artifact paths, state directories, `HANDOFF.md`, absolute home-directory paths, `/tmp/...`, scratch filenames, or `file://` links. Summarize local evidence instead.

Diagrams are optional and omitted by default. If one materially helps, read `references/diagrams.md`; included diagrams must render with an already-installed `mmdc`. In unattended mode use deterministic omission; when a diagram is explicitly required, halt if rendering is unavailable or fails.

Before publishing, gate the body yourself: every required section present, no internal path from the denylist above, and any diagram markers resolved per `references/diagrams.md`.

For GitLab UI uploads, and only when real UI evidence exists, read `references/gitlab-uploads.md`. GitHub evidence must already have a reviewer-accessible URL.

### 3. Lookup before create

Query open candidates by canonical repo, source, and target using provider JSON (`gh pr list --json ...` / `glab mr list` via API):

- One exact candidate: bind it; do not create another.
- Zero exact candidates: create, then query again.
- Multiple exact candidates, a same-source target/state mismatch, invalid JSON, missing CLI, or lookup failure: halt.

This lookup is required on every resume. A create race must return to lookup; never blindly retry creation.

### 4. Create only when lookup found no candidate

Build assignee/reviewer flags from the resolved policy as shell arrays, one validated username per element.

GitHub supports a body file directly:

```bash
gh pr create --repo "$REPO" --base "$BASE" --head "$TARGET" \
  --title "[$KEY] $TITLE" --body-file "$BODY" \
  --assignee "$ASSIGNEE" "${REVIEWER_ARGS[@]}" "${DRAFT_ARGS[@]}"
```

`glab` (as installed here) has no description-file flag. Load the validated file without command substitution, pass one quoted argument, then clear it:

```bash
DESCRIPTION=
IFS= read -r -d '' DESCRIPTION < "$BODY" || :
glab mr create --repo "$REPO" --target-branch "$BASE" --source-branch "$TARGET" \
  --title "[$KEY] $TITLE" --description "$DESCRIPTION" --assignee "$ASSIGNEE" \
  "${REVIEWER_ARGS[@]}" "${DRAFT_ARGS[@]}" --yes
unset DESCRIPTION
```

After creation, run exact lookup again. Do not trust create stdout as metadata.

### 5. Bind structured evidence

From the fresh provider JSON, verify: provider/repo/URL, approved source/target, open state, author, assignee, reviewer policy satisfied, and that the published description hash matches the local body file (note that some providers strip a trailing newline from the description — strip before hashing). Then write:

- `worktrees[project].mr`: URL, retained for consumers.
- `worktrees[project].mrEvidence`: absolute evidence JSON path under `{stateRoot}/ISSUE-KEY/phase6/PROJECT/` containing the verified metadata and body hash.

If an existing candidate lacks an explicitly resolved assignee/reviewer, repair it only with those configured identities, re-query, and bind. Do not backfill self-review beyond the configured default.

### 6. Run the phase gate

Revalidate every local body/evidence file and perform a fresh JSON live lookup per project. Missing tools, lookup errors, and metadata drift fail closed. After PASS, report each URL and branch pair (and send the optional notification if a channel is configured). Do not mark Phase 6 complete before the gate passes.

## Safety

- Never push a protected base branch, force push, bypass hooks, print tokens, or parse human CLI output.
- Do not use network installs or `npx -y`; use only installed tooling.
- Treat body and evidence paths as allocated absolute files inside the project's Phase 6 directory.
- PAT/auth failure requires user action; do not mint or replace credentials.
