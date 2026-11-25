---
name: security-review
description: >-
  Security review checklist: auth, secrets, API boundaries, data handling, and
  infra. Use with security-reviewer subagent after architect (design) and after
  QA pass (implementation).
---

# Security Review

## Scope

Applies to application source, Docker/compose, env examples, CI config, and database schema/migrations (paths from `project-context`).

## Design review checklist (post-architect)

| Area                    | Check                                                                                                      |
| ----------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Auth**                | Protected routes and mutations require auth; session/token model documented; no privilege escalation paths |
| **API exposure**        | Public vs authenticated endpoints explicit; rate limiting considered for sensitive writes                  |
| **Input validation**    | Validation at API boundary; no trust of client shapes for domain logic or PII                              |
| **Data classification** | PII fields identified; retention and access boundaries in design                                           |
| **Secrets**             | No secrets in repo; env vars documented; third-party keys server-side only                                 |
| **Database**            | Least-privilege queries; no raw SQL without parameterization; migration safety                             |
| **Third parties**       | Minimize PII in prompts/payloads; error messages do not leak internals                                     |
| **Infra**               | Ports, DB credentials, network exposure appropriate for the environment                                    |

## Implementation review checklist (post-QA)

| Area                | Check                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------- |
| **Auth guards**     | Guards/middleware on protected controllers; client cannot call protected routes without token |
| **Validation**      | DTO/schema validation; reject unknown fields where applicable                                 |
| **Injection**       | No string-concatenated SQL; sanitize/log safely                                               |
| **Secrets in code** | Grep for keys, tokens, hardcoded passwords — none in committed files                          |
| **Error handling**  | Stack traces and DB errors not returned to clients                                            |
| **CORS / headers**  | Sensible defaults if configured                                                               |
| **Dependencies**    | No obviously vulnerable patterns introduced in diff                                           |
| **Env files**       | `.env.example` updated; real secrets gitignored                                               |
| **Frontend**        | No secrets in client bundles; token storage approach reviewed                                 |

## Verdict guidance

| Verdict                            | Meaning                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------- |
| **PASS**                           | No blocking or high findings; proceed                                   |
| **REFINEMENT_NEEDED** (design)     | Architect must update `04-architecture-design.md` before implementation |
| **REWORK_NEEDED** (implementation) | Return to developer(s) or architect per finding                         |
| **BLOCKER**                        | Must fix before any release; PM cannot skip                             |

## Return routing (implementation review)

| Finding type                                  | Return to                                       |
| --------------------------------------------- | ----------------------------------------------- |
| Missing guard, bad validation, secret in code | `backend-developer` and/or `frontend-developer` |
| Wrong API contract enabling abuse             | `architect` then developers                     |
| Compose/env exposes DB publicly               | `devops-engineer` + `architect` if design issue |
| Both layers share auth bug                    | `both`                                          |

Document commands run in the security handoff artifact.
