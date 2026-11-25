---
name: besimple-broccoli-blind
description: "Non-interactive wrapper: plan-sketch -> auto-pick recommended options -> plan-write -> plan-critique-loop -> implement-from-plan -> claude-simplify-wrapper -> dedup -> code-review-loop. No PR creation and no Linear comments."
---

# Sketch -> Auto-select -> Plan -> Critique -> Implement -> Simplify -> Dedup -> Review (blind wrapper)

This is the automation-safe variant of `besimple-broccoli`.

- It uses the same planning + implementation flow.
- It automatically chooses **recommended** clarification options.
- It does **not** open PRs and does **not** post Linear comments.

## Preconditions

- Confirm repo: `git rev-parse --show-toplevel`
- Ensure CLIs: `codex`, `claude`
- Ensure git commits are possible (`user.name` / `user.email` configured)

## Required subskills

- `plan-sketch`
- `plan-write`
- `plan-critique-loop`
- `implement-from-plan`
- `claude-simplify-wrapper`
- `dedup`
- `code-review-loop`

## Workflow

0. **Prepare subagent logs and heartbeat**
   ```bash
   LOG_DIR="/tmp/codex-subagent-logs/$(basename "$PWD")"
   HEARTBEAT_SECONDS=60
   SUBAGENT_TIMEOUT_SECONDS=7200
   mkdir -p "${LOG_DIR}"
   SKETCH_LOG="${LOG_DIR}/plan-sketch.log"
   WRITE_LOG="${LOG_DIR}/plan-write.log"
   CRITIQUE_LOG="${LOG_DIR}/plan-critique.log"
   SIMPLIFY_LOG="${LOG_DIR}/simplify.log"
   DEDUP_LOG="${LOG_DIR}/dedup.log"
   REVIEW_LOG="${LOG_DIR}/code-review.log"
   : > "${SKETCH_LOG}"
   : > "${WRITE_LOG}"
   : > "${CRITIQUE_LOG}"
   : > "${SIMPLIFY_LOG}"
   : > "${DEDUP_LOG}"
   : > "${REVIEW_LOG}"
   ```

   Resolve installed skill directories (so the wrapper works from any repo):
   ```bash
   resolve_skill_dir() {
     local name="$1"
     local repo_root=""
     repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

     local candidates=(
       "$repo_root/.agents/skills/$name"
       "$repo_root/.claude/skills/$name"
       "$HOME/.agents/skills/$name"
       "$HOME/.codex/skills/$name"
       "$HOME/.claude/skills/$name"
     )

     for d in "${candidates[@]}"; do
       if [[ -d "$d" ]]; then
         echo "$d"
         return 0
       fi
     done

     echo "Error: skill '$name' not found in repo-scoped or user-scoped skill dirs." >&2
     return 1
   }

   BESIMPLE_BROCCOLI_BLIND_SKILL_DIR="$(resolve_skill_dir besimple-broccoli-blind)"
   PLAN_SKETCH_SKILL_DIR="$(resolve_skill_dir plan-sketch)"
   PLAN_WRITE_SKILL_DIR="$(resolve_skill_dir plan-write)"
   PLAN_CRITIQUE_LOOP_SKILL_DIR="$(resolve_skill_dir plan-critique-loop)"
   SIMPLIFY_SKILL_DIR="$(resolve_skill_dir claude-simplify-wrapper)"
   DEDUP_SKILL_DIR="$(resolve_skill_dir dedup)"
   CODE_REVIEW_LOOP_SKILL_DIR="$(resolve_skill_dir code-review-loop)"
   ```

1. **Write `IDEA_FILE` from user input**
   - `IDEA_FILE="${LOG_DIR}/idea.md"`
   - Preserve the user message verbatim.

2. **Run `plan-sketch` and auto-select recommended options**
   ```bash
   SKETCH_DOC=$(python3 "$PLAN_SKETCH_SKILL_DIR/scripts/run_plan_sketch.py" --idea-file "${IDEA_FILE}" --output "${LOG_DIR}/sketch.md" --timeout "${SUBAGENT_TIMEOUT_SECONDS}" --progress-log "${SKETCH_LOG}" --heartbeat-seconds "${HEARTBEAT_SECONDS}")
   ```

   Extract the last user-questions block:
   ```bash
   QUESTIONS_BLOCK=$(awk '
     /^BEGIN_USER_QUESTIONS$/ {in_block=1; block=""; next}
     /^END_USER_QUESTIONS$/   {in_block=0; last=block; next}
     in_block                 {block = block $0 ORS}
     END                      {printf "%s", last}
   ' "${SKETCH_LOG}")
   ```

   Auto-pick recommended options by reading `QUESTIONS_BLOCK` directly in the LLM context (no shell/regex parsing):
   - Set `AUTO_SELECTIONS` to a comma-separated list of all labels whose option text ends with `(Recommended)` (for example: `1a, 2c`).
   - Do not compute `AUTO_SELECTIONS` with `awk`, `jq`, or `python`.
   - If no recommended options are present, continue to empty feedback. 

   Save synthetic feedback:
   ```bash
   USER_FEEDBACK_FILE="${LOG_DIR}/user-feedback.md"
   cat > "${USER_FEEDBACK_FILE}" <<'FEEDBACK'
## User feedback (verbatim)
<auto-populated by wrapper>
FEEDBACK
   printf "%s\n" "${AUTO_SELECTIONS}" >> "${USER_FEEDBACK_FILE}"
   ```

   Append to `IDEA_FILE`:
   - Clarification mode: automatic recommended picks
   - Selected labels: `${AUTO_SELECTIONS}`

3. **Create working branch**
   - Ensure clean tree:
     ```bash
     if [ -n "$(git status --porcelain)" ]; then
       echo "Working tree is not clean. Aborting before branch creation." >&2
       exit 1
     fi
     ```
   - Choose `BASE_REF` explicitly:
     - If the user explicitly asked for a base branch/commit in the request, use that.
     - Otherwise, derive the default remote branch:
       ```bash
       DEFAULT_BRANCH="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')"
       if [ -z "${DEFAULT_BRANCH}" ]; then
         if git show-ref --verify --quiet refs/remotes/origin/main; then DEFAULT_BRANCH=main;
         elif git show-ref --verify --quiet refs/remotes/origin/master; then DEFAULT_BRANCH=master;
         else
           echo "Could not determine origin default branch (origin/HEAD, main, master). Aborting." >&2
           exit 1
         fi
       fi
       BASE_REF="origin/${DEFAULT_BRANCH}"
       ```
   - Choose branch name explicitly from clarified scope:
     - Use `task/` prefix.
     - Build a short slug from the clarified goal in `IDEA_FILE` (letters/numbers/dashes only, concise and specific).
     - Example: `task/auto-select-recommended-options`.
   - Sanitize, avoid collisions, and create the branch:
     ```bash
     BRANCH_NAME_SEED="task/<clarified-scope-slug>"
     BRANCH_NAME="${BRANCH_NAME_SEED}"
     BRANCH_NAME="$(echo "${BRANCH_NAME}" | tr '[:upper:]' '[:lower:]' | sed -E 's@[^a-z0-9._/-]+@-@g; s@/+@/@g; s@^-+@@; s@-+$@@; s@^/+@@; s@/+$@@')"
     if [ -z "${BRANCH_NAME}" ]; then
       echo "Branch name is empty after sanitization. Aborting." >&2
       exit 1
     fi
     BRANCH="${BRANCH_NAME}"
     if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
       i=2
       while git show-ref --verify --quiet "refs/heads/${BRANCH}-${i}"; do i=$((i+1)); done
       BRANCH="${BRANCH}-${i}"
     fi
     if ! git rev-parse --verify --quiet "${BASE_REF}^{commit}" >/dev/null; then
       echo "Base ref does not resolve to a commit: ${BASE_REF}. Aborting." >&2
       exit 1
     fi
     git checkout -b "${BRANCH}" "${BASE_REF}"
     ```

4. **Build plan-write input**
   ```bash
   PLAN_WRITE_INPUT="${LOG_DIR}/plan-write-input.md"
   python3 "$BESIMPLE_BROCCOLI_BLIND_SKILL_DIR/scripts/prepare_plan_write_input.py" \
     --sketch-doc "${SKETCH_DOC}" \
     --sketch-log "${SKETCH_LOG}" \
     --user-feedback "${USER_FEEDBACK_FILE}" \
     --output "${PLAN_WRITE_INPUT}"
   ```

5. **Run `plan-write` and commit plan**
   ```bash
   PLAN_DOC=$(python3 "$PLAN_WRITE_SKILL_DIR/scripts/run_plan_write.py" "${PLAN_WRITE_INPUT}" --timeout "${SUBAGENT_TIMEOUT_SECONDS}" --progress-log "${WRITE_LOG}" --heartbeat-seconds "${HEARTBEAT_SECONDS}")
   git add "${PLAN_DOC}"
   git commit -m "Plan: initial draft"
   ```

6. **Run `plan-critique-loop`**
   ```bash
   python3 "$PLAN_CRITIQUE_LOOP_SKILL_DIR/scripts/run_critique_loop.py" "${PLAN_DOC}" --max-iterations 2 --timeout "${SUBAGENT_TIMEOUT_SECONDS}" --progress-log "${CRITIQUE_LOG}" --heartbeat-seconds "${HEARTBEAT_SECONDS}"
   ```

7. **Commit plan updates (if changed)**
   ```bash
   git add "${PLAN_DOC}"
   git diff --cached --quiet || git commit -m "Plan critique: updates"
   ```

8. **Git hygiene**
   - Ensure `codex-progress.log` is ignored and untracked
   - Ensure clean tree
   - Record `REVIEW_BASE_SHA=$(git rev-parse HEAD)`

9. **Implement from plan (inline)**
   - Run `implement-from-plan` subskill with `PLAN_DOC`

10. **Run simplify loop**
    ```bash
    python3 "$SIMPLIFY_SKILL_DIR/scripts/run_simplify_loop.py" "${REVIEW_BASE_SHA}" --timeout "${SUBAGENT_TIMEOUT_SECONDS}" --progress-log "${SIMPLIFY_LOG}" --heartbeat-seconds "${HEARTBEAT_SECONDS}"
    ```

11. **Run dedup loop**
    ```bash
    python3 "$DEDUP_SKILL_DIR/scripts/run_dedup_loop.py" "${REVIEW_BASE_SHA}" --timeout "${SUBAGENT_TIMEOUT_SECONDS}" --progress-log "${DEDUP_LOG}" --heartbeat-seconds "${HEARTBEAT_SECONDS}"
    ```

12. **Run review loop**
    ```bash
    python3 "$CODE_REVIEW_LOOP_SKILL_DIR/scripts/run_review_loop.py" "${REVIEW_BASE_SHA}" --max-iterations 2 --timeout "${SUBAGENT_TIMEOUT_SECONDS}" --progress-log "${REVIEW_LOG}" --heartbeat-seconds "${HEARTBEAT_SECONDS}"
    ```

13. **Stop**
    - Do not open a PR.
    - Do not post Linear comments.
    - Leave branch/PR/comments to external automation worker.
