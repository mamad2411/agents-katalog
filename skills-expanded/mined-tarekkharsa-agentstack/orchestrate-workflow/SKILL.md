---
name: orchestrate-workflow
description: Wire a generate-review-fix multi-agent workflow (one implementer, N adversarial reviewers, a fixer) from agentstack profiles — models per role, skills per role, secrets injected at start — and run it in your executor of choice (sandcastle, Claude Code workflows, or plain Docker). agentstack provisions and governs the agents; it never runs the loop.
---

# Orchestrate a governed multi-agent workflow

Use when you want the Bun-in-Rust shape — an implementer writes, independent
adversarial reviewers attack the diff, a fixer applies feedback — with each
agent's capabilities, model, and secrets managed by agentstack instead of
hand-assembled per run.

The division of labor is fixed: **an executor runs the loop** (sandcastle,
Claude Code workflows, your own script); **agentstack defines and provisions
the agents** the loop spawns. Don't blur it in either direction.

## 1 — Define roles as profiles

A role is a profile: which skills, which servers, and (by convention) which
model. In `.agentstack/agentstack.toml`:

```toml
[profiles.implementer]
skills  = ["porting-guide"]        # the task's context artifacts
servers = ["github"]

[profiles.reviewer]
skills  = ["adversarial-review"]   # ships in this catalog
servers = []                       # reviewers judge the diff; no tools needed
```

Keep reviewer profiles minimal on purpose — a reviewer with no servers can't
be tool-poisoned, and the diff is all it should trust anyway.

## 2 — Bind models to roles

Pick per role, not per run: bulk/mechanical implementation → a cheap strong
coder; review → a different model family than the implementer when possible
(diverse failure modes). Record the binding wherever the executor configures
each agent (sandcastle's `agent:` option, a Workflow `model:` param, a
`--model` flag). If the route-by-cost skill is loaded, apply its ladder.

## 3 — Provision the sandbox (works today, no extra tooling)

The box needs three things: the harness CLIs, the rendered capabilities, and
secrets that never touch disk.

```bash
# on the host — render the role's capabilities into the worktree the
# sandbox will mount (repeat per worktree):
cd <worktree> && agentstack use implementer --write

# start the container with secrets injected from the keychain at run time —
# no .env file, nothing baked into the image or committed:
docker run \
  -e GH_PAT="$(agentstack secret get GH_PAT)" \
  -e ANTHROPIC_API_KEY="$(agentstack secret get ANTHROPIC_API_KEY)" \
  -v <worktree>:/work ...
```

(`agentstack secret list` shows every name the manifest references and
whether it resolves — inject exactly that set, nothing more.)

- The Dockerfile needs each harness the workflow uses (`claude` and/or
  `codex`) plus git — verify **inside** the box with `claude --version` /
  `codex --version` before trusting a long run to it.
- Codex reads `AGENTS.md`, Claude Code reads `CLAUDE.md` — `use --write`
  renders both, so a mixed-vendor workflow gets each harness its native view
  of the same profile.
- Revert with `agentstack use <profile>` semantics or run the loop in a
  disposable worktree and let it die with the container.

## 4 — Run the loop in the executor

The canonical shape, whatever executes it:

```text
while task = todo.pop():
  implementer writes on a branch          (1 agent)
  N reviewers attack the diff in parallel (2+, independent, diff-only)
  fixer applies the feedback              (author role or a third agent)
  re-review the fix; commit when clean
```

- sandcastle: one `run()` per role step; `branchStrategy` keeps commits on a
  task branch; parallel tasks → separate worktrees.
- Claude Code: the Workflow tool's pipeline/parallel primitives map 1:1.
- Reviewers must be *independent* — separate processes with no shared
  context beyond the diff, or the adversarial stance collapses.

## 5 — Govern and account

- Register the gateway (`agentstack more gateway connect`) and let sandboxed agents reach
  MCP through it: the manifest's `[policy]` firewalls every call and
  `~/.agentstack/audit/calls.jsonl` records tool · outcome · latency per run.
- After a run, `agentstack more report calls` shows call activity and dead weight —
  which roles used what, and what you provisioned for nothing.

## Rules

- **Never let a workflow agent edit the manifest or the library.** Provision
  before the run; agents inside the box consume, not administer.
- **Secrets only as env at start**, resolved from the keychain — never in the
  image, the worktree, or a committed file.
- **Match Bun's discipline, not its scale.** Start with one task, one
  implementer, two reviewers. Scale worktrees only when a single box is
  saturated and green.
