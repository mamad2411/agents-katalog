---
name: code-coder
description: (NS) Ad-hoc coding agent for focused implementation without full SDD planning — bug fixes, isolated components, small refactors, scripts, migrations. Use when the user says "just implement this", "quick fix", "add a field to the form", or gives a concrete coding task without execution-handoff — even without naming an agent. When a planned version has execution-handoff.md, follow execution-handoff-generator run-implementation workflow instead of this skill's ad-hoc cycle. Redirect large multi-day features to planning. Do NOT generate requirements.md, task files, or execution-handoff.
depends:
  - nextstage-harness
---

# Code Coder

Implement ad-hoc coding tasks with minimal diff while respecting project rules.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md`. Load rules from `{harness_root}/rules/*.md`. Read `architecture-rules.md` first. Legacy: `.cursor/rules/*.mdc` only if `{harness_root}` is absent.

## When to use

- Bug fixes and hotfixes outside a planned version
- Isolated component, hook, service, or utility
- Small refactors (≤ 1 file or tight group)
- Scripts, migrations, seeds outside version lifecycle
- "Just implement this" without `execution-handoff.md`

For full planned versions with `execution-handoff.md`, follow
`../execution-handoff-generator/references/run-implementation.md` and update the
handoff per `../execution-handoff-generator/SKILL.md` — not this skill's ad-hoc
cycle below.

If the request includes a GitLab **issue URL** (`ISSUE_URL`), use `execute-gitlab-issue` instead — not this skill.

## Session inputs

| Variable             | Required                                                        |
| -------------------- | --------------------------------------------------------------- |
| `{product_root}`     | Yes (or infer if single obvious product)                        |
| `{task_description}` | Yes                                                             |
| `{target_layer}`     | Infer when possible: frontend, backend, infra, tests, fullstack |

## Scope isolation

Operate only under `{product_root}/**` plus harness docs. Do not read other products in a monorepo unless asked.

## Boot (mandatory)

1. Read `AGENTS.md`
2. Load layer rules from harness when present (architecture always; backend/frontend/tests/e2e by layer)
3. Load product context: follow **Implementation boot rule** in `../nextstage-harness/references/artifact-layout.md`
4. `git status` and `git diff`
5. **Read target files before writing**

## Implementation rules

- **Diff-first** — only required lines; no unrelated formatting
- **Prefer editing** existing files over new files
- **Large change gate:** >1 file simultaneously, >20 lines in one file, or public contract change → one-line plan, wait for approval
- **No commits** unless human explicitly asks — when committing, see `../nextstage-harness/references/agent-git-identity.md`
- **No SDD artifacts** — no `task-NNN.md`, `requirements.md`, `execution-handoff.md`
- **No gratuitous comments** unless requested
- Run tests per `AGENTS.md` Docker and testing; project-specific container and commands live in `architecture-rules.md`

## Per-task cycle

1. Understand task
2. Load rules
3. Explore relevant files
4. Identify minimal diff
5. Apply (or present plan if large-change gate)
6. Run tests if in scope
7. **Review loop** — invoke `code-reviewer` and iterate on findings (see below)
8. Report what changed, final review verdict, and follow-ups

## Review loop (mandatory)

After tests pass (step 6), run an internal review loop before reporting done.

- Invoke `code-reviewer` on the working-tree diff (`git diff`) — no `ISSUE_URL`, no version-closure path. Just the ad-hoc diff.
- **Max 3 rounds.** After each review:
  - **No Critical Issues** (satisfactory score) → proceed to report.
  - **Critical Issues** with rounds left → apply the minimal diff that resolves each Critical (`code-reviewer` is read-only, so this skill applies the fixes), re-run tests if in scope, then re-review.
  - **Rounds exhausted** with Criticals still open → **stop and report as blocked**. List the unresolved Criticals. Do not report success.
- Keep fixes within the original task scope. If a Critical finding requires changes outside scope (public contract, cross-product, multi-day work), stop and escalate per **Stop conditions** instead of expanding the diff.
- Warnings and Suggestions do not block: carry them into the final report as follow-ups.

## Stop conditions

| Condition                                       | Action               |
| ----------------------------------------------- | -------------------- |
| `{product_root}` unclear with multiple products | Ask once             |
| Large change gate                               | Plan + wait          |
| Public contract or cross-product boundary       | Stop, explain, ask   |
| Task needs multi-day SDD planning               | Redirect to planning |

## Related skills

- `code-reviewer` — mandatory review loop after implementation (see **Review loop**)
- `code-investigator` — if blocked by unclear bug
- `code-autonomous` — autonomous multi-agent execution (GitLab issue or local plan); for a GitLab issue, use `execute-gitlab-issue` instead

## Forbidden

- SDD artifact generation
- Cross-product access without scope
- Commits without explicit request
- Refactors outside task scope
