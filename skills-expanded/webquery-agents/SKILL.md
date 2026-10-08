# WebQuery Agent Working Agreement

This file is the shared source of truth for AI-assisted work in this repository.
It is written to be followed by Codex/GPT, Claude Code, Gemini CLI, and
Antigravity. Tool-specific adapter files must not contradict it.

## Non-Negotiable Session Gate: Open Questions

At the beginning of **every session**, before investigation, planning, editing,
testing, or delegating:

1. Read `docs/open-questions.md`.
2. Find every item whose status is `Open`.
3. Ask the user for the answer to **all** of those questions in one numbered
   message. Do not select an answer, silently convert it into an assumption, or
   continue the task until the user answers or explicitly says to defer it.
4. When the answer affects a feature, record it in that feature's spec. When it
   affects a durable technical decision, record it in an ADR as well.

If there are no open questions, say that there are no active project open
questions and continue. Do not create artificial questions just to satisfy this
gate. If the current request exposes a material unknown, add it to
`docs/open-questions.md` with status `Open`, ask it, and wait rather than making
the choice.

## Project Map

- `web_api/`: FastAPI/Python backend. Domain modules own their router, schemas,
  service layer, and domain exceptions.
- `frontend/`: Vite + React + TypeScript frontend. Arayüz değişikliklerinden
  önce `frontend/DESIGN.md` okunur; tasarım token'ları, bileşen envanteri ve
  erişilebilirlik sözleşmesi oradadır.
- `docs/specs/`: feature specifications and acceptance criteria.
- `docs/adr/`: accepted and superseded architecture decisions.
- `docs/handoffs/`: session or agent handoff records.
- `docs/ai/playbooks/`: reusable, provider-neutral work procedures.
- `.agents/skills/`: Agent Skills open-standard entries. Gemini CLI and
  Antigravity discover these directly; Claude Code has adapters under
  `.claude/skills/`.

## Workflow Routing

Use the smallest workflow that preserves clarity and evidence.

| Situation | Required artifact |
| --- | --- |
| New or changed user-visible behavior, API contract, business rule, or security behavior | A spec based on `docs/specs/SPEC-TEMPLATE.md` before implementation |
| Durable architectural choice, external dependency, security boundary, data model, or non-trivial trade-off | An ADR based on `docs/adr/ADR-TEMPLATE.md` before implementation |
| Bug fix with no contract change | A regression test; use a mini-spec only if behavior is ambiguous |
| Handoff, review, long-running task, or delegated work | A YAML record based on `docs/handoffs/HANDOFF-TEMPLATE.yaml` |

Do not create an ADR for a routine implementation detail. This project has no
BDD runner, so acceptance criteria belong in the feature spec, not in a
`.feature` file.

## Delivery Rules

1. Read the relevant spec, ADR, playbook, and nearby tests before editing.
2. Keep the change scoped; preserve unrelated user changes in a dirty worktree.
3. Add or update automated tests for changed behavior. Map tests back to the
   acceptance criteria where a spec exists.
4. Run the relevant validation and report the actual command and result.
5. For backend changes, use the backend environment and run `pytest` from
   `web_api/` unless a narrower test is demonstrably sufficient.
6. For frontend changes, run `npm run build` from `frontend/`. This project has
   no committed frontend test command yet; do not invent a passing test result.

## Security and Data Safety

- Never commit, print, copy into documentation, or hand off secret values from
  `.env`, `.env.stage`, credentials, tokens, or database backups.
- Preserve authorization, audit logging, query risk analysis, data masking, and
  trace propagation unless the task explicitly changes them.
- Treat SQL execution, authentication, permissions, database connection
  handling, and logging as security-sensitive. Use the change-review playbook
  for changes in those areas.

## Reusable Procedures and Roles

- Feature delivery: `docs/ai/playbooks/feature-delivery.md`
- Bug fixing: `docs/ai/playbooks/bugfix.md`
- Change review: `docs/ai/playbooks/change-review.md`
- Architecture decision: `docs/ai/playbooks/architecture-decision.md`
- Implementation role: `.agents/roles/implementation-agent.md`
- Review role: `.agents/roles/review-agent.md`

Use the matching Agent Skill when the client exposes it. If the client does not
auto-discover repository skills, read the matching file in `.agents/skills/`
explicitly. The underlying standards and templates remain the source of truth.
