---
name: deepseek-agent
description: "Call a DeepSeek-backed OpenCode agent as a separate critique, writing, or revision agent from Codex. Use when Codex needs to delegate adversarial research critique, novelty skepticism, method review, manuscript prose, LaTeX section drafting, academic text revision, or paper-writing feedback loops to DeepSeek."
---

# DeepSeek Agent

Use this skill to invoke a DeepSeek-backed agent through OpenCode. Codex remains the controller: it prepares the brief, chooses the output contract, calls the external agent, then reviews the result before integrating it.

## Preconditions

Run these checks once per Codex session before the first DeepSeek delegation:

```powershell
opencode --version
opencode auth list
pwsh -NoProfile -Command '$PSVersionTable.PSVersion'
# If pwsh is unavailable:
powershell -NoProfile -Command '$PSVersionTable.PSVersion'
```

`opencode` should be available on `PATH`, or the caller should pass the wrapper's `-Binary` parameter. The bundled wrapper needs either `pwsh` or Windows PowerShell.

Credentials must come from OpenCode provider configuration or environment loading; never pass API keys as command arguments. If `DEEPSEEK_API_KEY` is missing on Windows Command Prompt, use the prompt-based helper, then open a new terminal:

```bat
%USERPROFILE%\.codex\skills\deepseek-agent\scripts\set_deepseek_env.cmd
```

To verify connectivity, resolve the installed skill path and run:

```powershell
$SkillsRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex/skills' }
$DeepSeekAgentSkill = Join-Path $SkillsRoot 'deepseek-agent'
& (Join-Path $DeepSeekAgentSkill 'scripts\setup_opencode_deepseek.ps1') `
  -Model 'deepseek/deepseek-v4-pro'
```

Do not commit API keys, generated `.env` files, transcripts, or verification outputs. If OpenCode reports missing credentials or provider connectivity failure, stop and report the blocker. Do not substitute Codex-authored manuscript prose for the DeepSeek delegation.

## Invocation

Use the standard invocation path by default. Resolve the bundled wrapper from this skill directory, and invoke it from the repository root so relative workspace paths still resolve correctly:

```powershell
$SkillsRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex/skills' }
$DeepSeekAgentSkill = Join-Path $SkillsRoot 'deepseek-agent'
& (Join-Path $DeepSeekAgentSkill 'scripts\invoke_deepseek.ps1') `
  -PromptFile .\path\to\brief.md `
  -Workspace . `
  -Model 'deepseek/deepseek-v4-pro' `
  -Auto `
  -UsePromptFileReference `
  -ResultFile .\.agents\tmp\deepseek-result.md `
  -Json `
  -OutputFile .\.agents\tmp\deepseek-output.json `
  -TranscriptFile .\.agents\tmp\deepseek-transcript.json `
  -TimeoutSeconds 1800
```

Keep this call shape for non-interactive writing and revision:

- Save the brief to `-PromptFile`; use `-UsePromptFileReference -Auto` so OpenCode can read it from the workspace.
- Require `-ResultFile` for long artifacts. Treat that file as authoritative even when `-Json` is enabled.
- Let the brief's `OUTPUT CONTRACT` decide whether file edits are allowed: `direct-edit` may edit only listed target files; `unified-diff`, `replacement-block`, and `answer-only` must write the artifact to `-ResultFile`.
- Set the surrounding shell/tool timeout at least 60 seconds longer than `-TimeoutSeconds`.
- Add `-RequirePattern "<end-marker>"` when bounded text must be complete. The wrapper checks the marker in `-ResultFile` when a result file is set.

`-StreamIdleTimeoutSeconds` is accepted only for older callers; do not use it for new OpenCode runs.

Use `-Model <provider/model>` when a task needs a specific DeepSeek backend. If omitted, the wrapper uses `$env:DEEPSEEK_AGENT_MODEL` when set and otherwise falls back to its built-in default.

Use `-Agent <name>` only when a project or user OpenCode agent has been configured for this delegation path. If omitted, OpenCode uses its default agent.

## Session Reuse

Use a fresh OpenCode session by default. Reuse a session only for later rounds of the same bounded writing task, especially K-round review/revision loops where the target files, source context, and output contract are materially unchanged.

Session controls are mutually exclusive:

- Round 1: omit session controls and save the transcript/output.
- Later rounds with a known session id: repeat the standard invocation and add `-ResumeSession <id-or-prefix>`.
- Later rounds without a known id: use `-Continue` only when no other OpenCode task has run in this workspace since round 1.

Prefer `-ResumeSession` over `-Continue`; recover ids from OpenCode output or `opencode session list` when needed. Session reuse is only an optimization: every revision brief must still restate the active target files, output contract, non-negotiable constraints, and specific issues to fix.

## Brief Contract

Every prompt sent through this skill must include:

1. `ROLE`: the receiving agent's concrete task role, such as manuscript revision agent, proof-drafting agent, critique agent, or answer-only analysis agent.
2. `TASK`: the exact writing or revision task.
3. `WORKSPACE`: the project root and relevant file paths.
4. `CONTEXT`: selected excerpts or summaries the DeepSeek-backed agent is allowed to rely on.
5. `CONSTRAINTS`: facts, notation, citations, style, and claims that must be preserved.
6. `OUTPUT CONTRACT`: one of:
   - `direct-edit`: edit listed files in the workspace and return changed-file list plus summary.
   - `unified-diff`: write the patch to the agreed `-ResultFile`; stdout should contain only changed-file list plus summary.
   - `replacement-block`: write the replacement text to the agreed `-ResultFile`; stdout should contain only target location plus summary.
   - `answer-only`: write analysis or draft text to the agreed `-ResultFile`; stdout should contain only summary.
7. `PROHIBITIONS`: no invented citations, unsupported results, author metadata, unrelated file edits, or secret exposure.
8. `ACCEPTANCE CRITERIA`: concrete checks Codex will apply.

## Output Handling

After the external agent returns:

1. Inspect the transcript or changed files.
2. Confirm the output contract was followed. For JSON output, inspect the event stream and process diagnostics; do not rely only on the process exit code.
3. If `-ResultFile` was used, inspect that file as the authoritative artifact.
4. Verify only intended files changed when `-Auto` was used.
5. Review content against the protocol acceptance criteria.
6. Apply patches or replacement blocks only after review.
7. Run compile/lint checks when the target artifact supports them.

If the DeepSeek-backed agent produces unusable prose, write a revision brief and call this skill again. Do not directly replace delegated manuscript text with Codex-authored prose while the two-agent protocol is active.

## Public Migration Notes

When copying this skill into a public repository or shared skill collection, keep the operational contract but remove private machine assumptions. Use install-root variables such as `$env:CODEX_HOME` or relative skill paths instead of personal absolute paths, keep examples generic, and do not include local transcripts, account details, unpublished project names, or one-off workspace logs. If a local wrapper path is needed, document how to resolve it from the installed `deepseek-agent` skill directory.

## Failure Handling

- If the CLI command fails, preserve the command, exit code, and relevant stderr in the user-facing report.
- If the wrapper exits with code 124, it hit `-TimeoutSeconds`, not necessarily a DeepSeek API timeout. Inspect `-TranscriptFile` for `TimedOut`, `Stdout`, and `Stderr`; then rerun with a larger `-TimeoutSeconds` and a larger caller timeout.
- If OpenCode reports missing DeepSeek credentials, run `scripts/setup_opencode_deepseek.ps1` with the API key supplied at runtime, or configure the provider through OpenCode's normal auth flow.
- If OpenCode returns JSON events but no result file, treat it as a failed delegation whenever `-ResultFile` was required.
- If the output is truncated or malformed, rerun with `-UsePromptFileReference`, `-ResultFile`, and a required end marker via `-RequirePattern`, or switch to `direct-edit` when bounded file edits are safer than returning long text through stdout.
- If direct edits touched unrelated files, stop and report the changed paths before attempting integration.
- If the prompt would exceed practical command-line size, save it to a brief file and call the wrapper with `-PromptFile -UsePromptFileReference`.
