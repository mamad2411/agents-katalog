---
name: terminal-fallback-via-vscode-tasks
description: Industrial fallback protocol for executing shell commands when the run_in_terminal tool is unavailable, by routing every command through the create_and_run_task tool (VS Code tasks.json) with a file-mediated output-capture pattern.
category: Environment-Management
---

# Terminal Fallback via VS Code Tasks Skill (v1)

This skill defines the operational fallback when the **`run_in_terminal`** tool (or any equivalent direct-shell
execution tool) is not available in the current agent toolset, but the **`create_and_run_task`** tool is.

VS Code tasks were designed for build / run / watch workflows, not for ad-hoc shell scripting. Using them as a
general-purpose terminal substitute introduces several quirks that the agent MUST handle explicitly. This skill
captures the field-proven pattern: a task created and run, output redirected to a file, then the file read back
through workspace tools.

***

## 1. Environment & Dependencies

The agent MUST verify the fallback path is necessary before invoking it.

1. **Primary path probe**: Attempt to call `run_in_terminal` (or the project's documented terminal tool) first.
   The fallback is engaged ONLY when that tool is absent from the toolset, disabled, or returns "tool not
   available".
2. **Required tool**: `create_and_run_task` MUST be available. If it is also absent, halt and surface the
   situation to the user — the agent CANNOT execute shell commands silently.
3. **Workspace folder**: A workspace folder path is mandatory for every task invocation. The agent MUST already
   know an absolute workspace folder path (typically a project root opened in VS Code) before engaging this skill.

***

## 2. The Five Operational Quirks (MUST READ)

When `create_and_run_task` is used as a shell-execution substitute, the agent MUST account for the following
behaviors:

| # | Quirk | Mitigation |
| :--- | :--- | :--- |
| 1 | **Truncated terminal display** — the `Output:` block returned to the agent is line-wrapped and frequently truncated mid-line, hiding errors and the actual command result. | Redirect stdout/stderr into a workspace-relative file (`Out-File .X.txt -Encoding utf8`), then read it back via `read_file`. |
| 2 | **Exit code 1 with no visible reason** — when the command's stderr or its complex quoting fails, the task terminates with exit code 1 and the cause is hidden in the truncated display. | Always pipe `2>&1` (POSIX shells) or use `Tee-Object` / `Out-File` redirection (PowerShell) so stderr is captured into the same file. |
| 3 | **PowerShell quoting hostility** — on Windows, tasks run through `powershell.exe -Command ...`. Double-quoted strings, embedded `"`, and backtick escapes (`` `n ``) frequently break or get reinterpreted, especially in `-m` flags to `git commit`. | Prefer **single-quoted** argument strings; use repeated `-m '...'` flags for multi-paragraph commit messages instead of `-m "...`n..."`. |
| 4 | **Task reuse** — VS Code reuses the same shell process across tasks. The cumulative scrollback shown to the agent may include output from previous tasks, easily misread as current output. | Use unique task `label`s per call (e.g., suffix `-v2`, `-retry2`) so the agent can correlate the request with the latest output, and always verify by reading the redirected output file. |
| 5 | **No interactive prompts** — tasks have no TTY, so commands requiring interactive input (e.g., `git credential-manager`, `ssh-add`, `gh auth login`) hang or fail silently. | Surface interactive operations back to the user with copy-pasteable manual commands instead of attempting them through a task. |
| 6 | **UTF-8 corruption on read-modify-write** — Windows PowerShell 5.1's `Get-Content` / `Set-Content` default to the system ANSI code page, silently turning `§`, `—`, `–`, emoji into mojibake (`Â§`, `â€"`) that persists on disk. `Set-Content -Encoding utf8` additionally writes a BOM. | Bulk text edits MUST follow [`shell-execution-rules.md` §2.4 (UTF-8-Safe Bulk Text Edits)](../../../ai-agent-rules/shell-execution-rules.md#24-utf-8-safe-bulk-text-edits-in-powershell-forbidden-patterns) — use `[System.IO.File]::ReadAllText` / `WriteAllText` with explicit UTF-8 (BOM-less), or prefer the editor's `replace_string_in_file` tool. |

***

## 3. The Canonical Pattern: File-Mediated Output Capture

The agent MUST follow this five-step pattern for every non-trivial shell command:

### 3.1 Step 1 — Compose the command with file redirection

PowerShell-on-Windows form (default for tasks running through `powershell.exe`):

```powershell
<command> 2>&1 | Out-File .<label>.txt -Encoding utf8
```

POSIX form (Git Bash / Linux / macOS):

```bash
<command> > .<label>.txt 2>&1
```

Where `.<label>.txt` is a **workspace-relative, dot-prefixed** filename that:

- Lives at the workspace folder root (so `read_file` can resolve it).
- Begins with `.` so it is unobtrusive and easy to clean up.
- Is uniquely named per command so retries don't overwrite a previous capture out of order.

### 3.2 Step 2 — Submit via `create_and_run_task`

```jsonc
{
  "task": {
    "label": "<unique-label>",
    "type": "shell",
    "command": "<command-with-redirection-from-step-1>"
  },
  "workspaceFolder": "<absolute-path-to-workspace-folder>"
}
```

**Flag-by-flag breakdown:**

- **`label`** — Display name and unique identifier for the task. MUST be unique per invocation; reusing a label
  can confuse the agent's correlation of output to request.
- **`type: "shell"`** — Tells VS Code to spawn a shell (PowerShell on Windows, `$SHELL` on POSIX) rather than a
  process invocation.
- **`command`** — The full one-liner including the redirection from Step 1. Avoid using the `args` array; inline
  everything into `command` so quoting rules are predictable.
- **`workspaceFolder`** — Absolute path; the task's `cwd` is set to this folder, so the output file lands here.

### 3.3 Step 3 — Skim the truncated terminal display

Read the truncated `Output:` block returned by the task. Use it ONLY to confirm:

- The task actually ran (exit code visible).
- No obvious authentication or syntax error halted execution before redirection took effect.

DO NOT trust this view for the command's actual results.

### 3.4 Step 4 — Read the captured file

Use the workspace's file-reading tool (e.g., `read_file`) on the dot-prefixed file:

```text
read_file(<workspace-folder>/.<label>.txt)
```

This is the authoritative output. Parse it as if it were direct terminal output.

### 3.5 Step 5 — Clean up

Once the captured output has been consumed, remove the file in a follow-up task so the workspace stays clean:

```powershell
Remove-Item -Force .<label>.txt -ErrorAction SilentlyContinue
```

Multiple capture files can be cleaned up in a single task by comma-separating paths.

***

## 4. Pattern Variants

### 4.1 Multi-command pipelines

For multiple commands that share state (e.g., a `cd` followed by a `git` command), chain them with `;` (PowerShell)
or `&&` (POSIX) in a single task — DO NOT split across tasks, because VS Code may spawn separate processes and lose
the implicit working directory state.

```powershell
git -C <subdir> remote -v; git -C <subdir> log -1 --oneline 2>&1 | Out-File .audit.txt -Encoding utf8
```

Prefer the **`-C <subdir>`** flag for `git` over `cd` to make each command self-contained and to keep the task's
`cwd` predictable.

### 4.2 PowerShell-friendly quoting for git commit

Multi-paragraph commit messages MUST use repeated single-quoted `-m` flags. Double-quoted forms with `` `n `` or
embedded `"` frequently fail with exit code 1 inside a task shell.

```powershell
git commit --only <path> `
  -m 'feat(scope): short subject' `
  -m '- Bullet 1.' `
  -m '- Bullet 2.'
```

### 4.3 Listing forks / repos / branches (read-only HTTP queries)

For GitHub queries when `gh` is unavailable, defer to the
[GitHub REST API Fallback](../github-rest-api-fallback/SKILL.md) skill. The output-capture pattern is identical;
only the command body changes.

### 4.4 Interactive commands — FORBIDDEN inside tasks

Tasks have no TTY. The agent MUST NOT attempt the following inside a task:

- `git credential-manager <subcommand>`
- `gh auth login`
- `ssh-add`
- Any `apt`, `dnf`, `brew`, `winget` install command (these may prompt for sudo / UAC).

Surface these to the user as a manual code block instead. See the
[Git/GitHub Auth Fallback](../git-github-auth-fallback/SKILL.md) skill for the auth-specific protocol.

***

## 5. Failure Modes

| Symptom | Likely Cause | Resolution |
| :--- | :--- | :--- |
| Task exits with code 1, no visible error | Quoting failure or stderr lost | Re-run with `2>&1` redirection; verify single-quote vs double-quote arguments. |
| Output shows previous task's content | Shell scrollback reuse | Use a unique label per invocation; read the capture file, not the display. |
| Empty capture file | Redirection happened before command crashed | Combine `2>&1` so stderr lands in the file; check the truncated display for the early-exit reason. |
| `read_file` reports file not found | Workspace folder mismatch or POSIX path on Windows | Verify the `workspaceFolder` parameter and re-emit the path with the correct separator. |
| Output truncated in display, but file is correct | Expected — display is line-wrapped/clipped | Always trust the capture file over the display. |

***

## 6. Composition by Higher-Level Skills

| Composer | Role | Reuses From This Skill |
| :--- | :--- | :--- |
| [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md) | Run REST queries via PowerShell `Invoke-RestMethod` / `curl` when `gh` is absent. | §3 file-mediated output capture, §4.3 GitHub query examples. |
| [`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) | Diagnose and recover from `git push` 403 / 401 / auth-cache failures. | §3 capture pattern for `git remote -v`, `git push`, and §4.4 forbidden-interactive guidance. |
| [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) | Reroute submodule remotes to a personal fork after a 403. | §3 capture pattern for the `git remote` / `git push` / `git commit` sequence. |
| [`git-submodule-fork-sync`](../git-submodule-fork-sync/SKILL.md) | Automated submodule-fork realignment. | §3 capture pattern for `gh repo view` / `git submodule sync` etc. |
| [`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md) | Recover orphan gitlinks via SHA-based discovery. | §3 capture pattern for `gh` / `curl` / `git` operations. |
| [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md) | Diagnose unreachable submodule upstreams via REST queries. | §3 capture pattern for every `curl` REST call. |
| [`git-branch-promotion`](../git-branch-promotion/SKILL.md) | Promote a refined branch onto canonical via force-push. | §3 capture pattern for `git fetch` / `git push --force-with-lease`. |
| [`github-secrets-bulk-set`](../github-secrets-bulk-set/SKILL.md) | Bulk-set GitHub Actions secrets. | §3 capture pattern for `gh secret set --env-file` (or REST equivalent). |
| [`jira-acli-operations`](../jira-acli-operations/SKILL.md) | Jira workflows that include `gh pr create`. | §3 capture pattern; §4.4 interactive `acli` flows surfaced to user. |

***

## 7. Related Skills

- [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) — Use to install `gh`, `git`, or other
  tools instead of repeatedly working around their absence. This skill is the short-term workaround when
  installation is not desired or possible.
- [Script Management Rules](../../../ai-agent-rules/script-management-rules.md) — When a task body grows beyond
  a one-liner, promote it to a `.ps1` script in the skill's `scripts/` folder per the PowerShell-First mandate.
- [Redaction & Portability](../redaction-portability/SKILL.md) — Capture files frequently contain absolute paths
  and identity strings; redact before committing or quoting in artifacts.

***

## 8. Traceability

- Originating session: May 2026 — submodule push (`ai-agent-rules`) blocked because the agent had only
  `create_and_run_task` available, and direct terminal tooling was disabled. The file-mediated capture pattern
  was discovered empirically when raw task `Output:` display turned out to be truncated mid-error-message.
