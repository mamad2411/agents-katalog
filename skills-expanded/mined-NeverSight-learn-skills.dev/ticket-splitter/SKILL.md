---
name: ticket-splitter
description: >-
  Use when splitting one Jira story into INVEST-testable backlog items with
  clear scope and done_when. Triggers: @ticket-splitter, Jira key, pasted
  requirement, team=, brief, or after @requirement-risk on the same key.
  Anchors to domain briefs; does not write curated.
disable-model-invocation: true
---

# ticket-splitter (INVEST backlog slices)

## First principles

**Artifact**: iteration-ready commitments — each item has a boundary (`scope`) and an observable completion face (`done_when`). Not a task list or “dev vs QA” role split.

**Quality**: `done_when` must say **what done looks like and how it is seen** (user behavior / system-observable state / contract). “Dev done”, “ready for QA” are not completion faces. **Title** = 3-second headline (one primary outcome). **scope** bullets = one idea each (P11/P12).

| | Wiki `@generate-knowledge-from-wiki` | This skill |
|--|--------------------------------------|------------|
| Cost of error | Pollutes library briefs | Planning meeting rewrites a few items |
| Who stops bad output | Human confirms modules | **Scripts** block fake testability / missing structure |
| Loop | Prep → confirm → compose → gate | **Draft → gate → fix failures only → gate** |

**Corollaries**

1. Do not wait for human confirm in the loop.
2. Borrow wiki’s **script-verified explicit form**, not confirm/continue ritual.
3. Scripts do not decide “how many slices”.
4. Substance: `ticket_system.md`; presentation: [`references/presentation.md`](references/presentation.md).

## When to use

- Planning: cut one Jira story into executable backlog items
- Need observable `scope` / `done_when`
- Optional domain briefs under `curated/by-root/<root_id>/`

## When not

| Scenario | Use |
|----------|-----|
| Risk only | `@requirement-risk` |
| Refresh wiki / write briefs | `@generate-knowledge-from-wiki` / `@distill-domain-knowledge` |
| Sprint bulk into briefs | `@add-knowledge-from-jira` |
| Requirement unreadable | State blockers; do **not** interrogate endlessly |

## How to invoke

- `@ticket-splitter DEMO-1 team=demo` (**offline demo**)
- `@ticket-splitter PROJ-123`
- `@ticket-splitter team=<key> PROJ-123`
- `@ticket-splitter PROJ-123` + code paths (R2.5 anchors)
- `@ticket-splitter PROJ-123 brief`
- Or pasted requirement text

Offline `DEMO-*`: [`../_shared/offline-demo.md`](../_shared/offline-demo.md).

| Param | Values | Default |
|-------|--------|---------|
| `team` | key/alias in `team-roots.json` | attribution / Agile Team |
| `brief` | short-mode words in message | full items |

## Preconditions & failures

- Offline `DEMO-*`: no credentials
- Real keys: `.env` Atlassian/Jira credentials + network; `fetch_jira_attachments.py` as needed
- No credentials → paste text or `DEMO-1`
- No brief → still emit; note missing anchors
- Gate fail → fix and re-run; do not claim done without pass

## Decision tree

```text
Jira key?
├─ DEMO-* / offline → fixtures/offline-demo; skip network
├─ real key → attachments via MCP or fetch script
├─ Resolve team/root
├─ primary slug → S7 locale brief (`*-domain-brief.md` / `*-领域知识定稿.md` per locale); else S6 source-brief / work draft (noted)
├─ Jira says “dev only, test elsewhere”? → do not invent test rows; note in narrative
├─ brief mode? → Scope + split overview + correction note (still gated)
├─ Draft → .jira_attachments/<KEY>/split_draft.md when KEY present
└─ Gate: validate_ticket_split.py [--brief] → fix → deliver
```

## Responsibility

| Layer | Agent | Script |
|-------|-------|--------|
| Evidence | Which briefs / code anchors | Fetch issue & attachments |
| Generate | Split + presentation | No prose authorship |
| Gate | Fix from report | `validate_ticket_split.py` |
| Semantic review | Only if user asks for principles | None |

## Gate rules

1. Full and `brief` must pass validator before delivery.
2. Fake testability (`done_when` = “dev done / ready for QA” with no observable state) → fail.
3. Need **Scope** + `## Split overview` (or locale equivalent the validator accepts); full items need title/scope/done_when/deps/confidence.
4. P11 title anti-patterns and P12 welded scope bullets → fail when detectable.
5. On fail, fix only reported issues.
6. Standards: `ticket_system.md` + presentation; scripts verify only.
7. Never write `curated/` or run distill check.

## Presentation & domain library

- [`references/presentation.md`](references/presentation.md) · P10: [`../_shared/presentation-p10.md`](../_shared/presentation-p10.md)
- [`../../contracts/jira-issue-domain-knowledge-context.md`](../../contracts/jira-issue-domain-knowledge-context.md)
- Anchor `scope` / `done_when` to **S7** locale briefs when present (R2.5); if only S6 / work draft exists, note “not S7” and still constrain to that evidence.

Unlike `@add-knowledge-from-jira`, this skill outputs **iteration backlog items**, not library merges.

## Agent checklist

1. Load Jira + domain evidence; fetch attachments if needed.
2. Split per `ticket_system`; constrain with briefs; write correction narrative when needed.
3. Presentation + P11/P12 self-check; attach risk `R-00N` when same-session risk exists (P7).
4. `validate_ticket_split.py`; fix until pass; deliver in chat.
5. Do not default-wait for human confirm.

## Done when

- [ ] Validator exit 0 (or explicitly marked failed)
- [ ] Scope + split overview present
- [ ] Full items have observable `done_when`; no fake-testability ban words
- [ ] Titles/scope pass P11/P12 intent
- [ ] Risk `R-00N` linked when applicable
- [ ] Not split primarily as “dev vs test” for the same outcome

## Forbidden

- Write `curated/` / run distill check
- Items that contradict explicit brief out-of-scope
- Invent subsystem names absent from briefs
- Skip gate or wait for confirm unless ungated draft requested
- Copy wiki confirm→continue as the split main flow
- Weld multi-concern scope into one bullet; empty verbs as fake coverage

## Handoff to `@ticket-test-design`

After a usable split (or instead of split when AC are already clear), testers may `@ticket-test-design <same KEY>` to produce must/should/later cases proving AC / `done_when`.

## Examples

```text
@ticket-splitter DEMO-1 team=demo
→ offline → draft → validate → deliver

@requirement-risk PROJ-1 then @ticket-splitter PROJ-1
→ no confirm wait; link R-00N; note open MUST assumptions
```
