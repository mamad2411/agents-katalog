---
name: codex-grok
description: "Codex-only workflow for non-trivial implementation: the current Codex session freezes the plan, delegates execution to Grok CLI, then reviews and verifies the result. Use when Grok should implement a resolved plan without inventing the architecture. Skip in every non-Codex harness; never launch a nested Codex planner."
---

# Codex Grok

## Session Gate

Apply this gate before running any CLI command:

- Codex session: continue. The current session owns planning, scope decisions, review, and verification.
- Any non-Codex harness: stop applying this skill.

Explicitly naming `$codex-grok` does not override the gate. Never run `command codex`, `codex exec`, or any equivalent nested Codex invocation from this skill.

## Route

Use this workflow when:

- implementation is non-trivial and needs an explicit plan before edits
- the desired outcome is known, but the exact file-level execution path is not frozen
- Grok should implement a refactor, bug fix, test fill, CI fix, or migration without redesigning it
- a separate Grok execution pass is worth the delegation overhead

Do not use it for tiny edits, design-only work, or ordinary one-pass investigation. For a read-only investigation or review, use this workflow only when the user explicitly asks for a Codex-plus-Grok cross-check; keep every external pass read-only.

If the spec is already frozen, hand it directly to Grok.

Keep in the coordinator:

- architecture, API, naming, UX, and final scope decisions
- session-only tools, secrets, and authenticated state
- destructive operations, releases, pushes, and GitHub mutations
- plan acceptance, diff review, verification, and final reporting

## Freeze The Plan

The accepted plan must resolve assumptions and contain:

1. problem framing and non-goals
2. exact files or modules to inspect and change
3. ordered implementation steps
4. exact tests and verification commands
5. risks and out-of-scope items

Do not hand Grok unresolved alternatives unless choosing among them is explicitly part of the task.

Produce and review the frozen plan in the current Codex session. Do not run `command codex`, `codex exec`, or any equivalent nested Codex invocation.

## Invoke Grok Executor

Pass the accepted plan to Grok without asking Grok to redesign it:

```bash
GP=$(mktemp); cat >"$GP" <<'EOF'
Execute the frozen implementation spec below. Do not redesign it or broaden scope.

Repo:
<absolute repo path>

Coordinator constraints:
<paths to avoid, non-goals, exact verification expected>

Frozen Codex plan:
<paste the accepted plan>

Output shape:
- files changed
- commands run and their results
- deviations from the plan, with reason
EOF
command grok --prompt-file "$GP" \
  --cwd <repo> \
  --model grok-4.5 \
  --output-format plain \
  --always-approve \
  --no-alt-screen \
  > /tmp/grok-last.md
```

- Keep the prompt scoped to the target repo.
- Use `--always-approve` only for scoped, non-destructive repo work.
- Read `/tmp/grok-last.md`; Grok's claims are advisory until verified.
- Do not kill a quiet run under 30 minutes.
- Use separate prompt and output files for independent parallel tasks.

## Follow-Up Fixes

- Bad or incomplete plan: correct it in the current Codex session before asking Grok to continue.
- Sound plan but faulty execution: continue Grok with the exact failing proof and narrow correction.
- After two failed Grok execution rounds, stop delegating and take over in the coordinator.

```bash
P2=$(mktemp); cat >"$P2" <<'EOF'
Fix only:
<specific correction>

Failure proof:
<test output, diff concern, or reviewer finding>

Expected verification:
<commands>
EOF
command grok --prompt-file "$P2" \
  --cwd <repo> \
  --continue \
  --output-format plain \
  --always-approve \
  --no-alt-screen \
  > /tmp/grok-last.md
```

## Prompt Contract

Every external CLI process starts with zero coordinator context.

- Grok is the only external agent in this workflow.
- Include the goal, repo, relevant paths, constraints, non-goals, expected proof, and output shape in every external prompt.
- Do not assume external agents can see chat history, screenshots, secrets, MCP state, or coordinator-only reasoning.

## Verify In The Coordinator

- run `git status -sb` and read the full diff
- compare Grok's changes with the accepted plan
- run focused tests or inspect their real output
- verify documentation when behavior, commands, configuration, or runtime architecture changed
- keep pushes, releases, and other irreversible operations in the coordinator

## Economics

The only valid path is current Codex planning -> Grok execution -> current Codex verification. Never pay for a nested Codex planning pass.
