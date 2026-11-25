---
name: codex-review
license: Apache-2.0
description: Run a Codex code review against local git state
argument-hint: '[--wait|--background] [--base <ref>] [--scope auto|working-tree|branch] [--model <model|alias>]'
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(node:*), Bash(git:*), AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

<!--
SPDX-License-Identifier: Apache-2.0
Derived from openai/codex-plugin-cc v1.0.6 (db52e28), Apache-2.0. Modified for rdl-agent-extensions.
-->

Run a Codex review through the shared built-in reviewer.

## Preflight — Node.js runtime

Before running the companion, verify Node >=18.18.0:

```bash
node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>18||(a===18&&b>=18)?0:1)'
```

Run this preflight exactly as written, as a single `Bash` command. Read the exit status and output from the Bash tool result (empty stdout on success is expected). Do not append `echo`, `;`, `&&`, pipes, or other shell separators, wrappers, or redirects; the declared grant is `Bash(node:*)`, not a general shell grant.

If that check fails (non-zero exit or `node` not found), stop and tell the user exactly: `Codex plugin requires Node.js >=18.18.0; install or upgrade Node: https://nodejs.org/en/download`. Do not surface a raw `command not found` or version error.

Raw slash-command arguments:
`$ARGUMENTS`

Core constraint:
- This command is review-only.
- Do not fix issues, apply patches, or suggest that you are about to make changes.
- Your only job is to run the review and return Codex's output verbatim to the user.

Execution mode rules:
- If the raw arguments include `--wait`, do not ask. Run the review in the foreground.
- If the raw arguments include `--background`, do not ask. Run the review in a Claude background task.
- Otherwise, estimate the review size before asking:
  - Run each size-check command below as a separate, plain `git` invocation in `Bash`, within `Bash(git:*)`. Read each tool result directly; do not combine commands or add `echo`, `;`, `&&`, pipes, or other shell separators, wrappers, or redirects.
  - For working-tree review, start with `git status --short --untracked-files=all`.
  - For working-tree review, also inspect both `git diff --shortstat --cached` and `git diff --shortstat`.
  - For base-branch review, use `git diff --shortstat <base>...HEAD`.
  - Treat untracked files or directories as reviewable work even when `git diff --shortstat` is empty.
  - Only conclude there is nothing to review when the relevant working-tree status is empty or the explicit branch diff is empty.
  - Recommend waiting only when the review is clearly tiny, roughly 1-2 files total and no sign of a broader directory-sized change.
  - In every other case, including unclear size, recommend background.
  - When in doubt, run the review instead of declaring that there is nothing to review.
- Then use `AskUserQuestion` exactly once with two options, putting the recommended option first and suffixing its label with `(Recommended)`:
  - `Wait for results`
  - `Run in background`

Argument handling:
- Preserve the user's arguments exactly.
- Do not strip `--wait` or `--background` yourself.
- `--model <model|alias>` (or `-m`) picks the Codex model for this run. The companion resolves aliases such as `sol`, `luna-6`, or `astra`; see `codex:model-guide` for the table and GPT-6 caveats.
- For a persistent review model, the user can set `review_model` in `~/.codex/config.toml`. When set, it takes precedence over `--model` for this native review (per the Codex config reference). Live pilot on 2026-09-30 with CLI 0.159.1 (nq-rdl/agent-extensions#430) confirmed precedence in a persisted app-server probe and `codex exec review`; a rejected-model sentinel corroborated Codex's selection of `review_model` on the companion path; the companion's ephemeral native review does not expose the reviewer model in stdout.
- Do not add extra review instructions or rewrite the user's intent.
- The companion script parses `--wait` and `--background`, but Claude Code's `Bash(..., run_in_background: true)` is what actually detaches the run.
- `/codex:review` is native-review only. It does not support staged-only review, unstaged-only review, or extra focus text. `/codex:adversarial-review` shares the same targets (no staged-only or unstaged-only scope either) and adds focus text.
- If the arguments include focus text, still pass them unchanged; the companion rejects them and names `/codex:adversarial-review`. Return that message as-is. Do not drop the focus text and rerun, and do not run `/codex:adversarial-review` unless the user asks for it.

Foreground flow:
- Run:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" review "$ARGUMENTS"
```
- Return the command stdout verbatim, exactly as-is.
- Do not paraphrase, summarize, or add commentary before or after it.
- Do not fix any issues mentioned in the review output.

Background flow:
- Launch the review with `Bash` in the background:
```typescript
Bash({
  command: `node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" review "$ARGUMENTS"`,
  description: "Codex review",
  run_in_background: true
})
```
- Do not call `BashOutput` or wait for completion in this turn.
- After launching the command, tell the user: "Codex review started in the background. Check `/codex:status` for progress."

## Codex packaging

For execution in a native Codex package, use the host-specific entrypoint in
[references/codex.rst](references/codex.rst). The registry selects it during packaging;
the Claude entrypoint above remains the Claude workflow.
