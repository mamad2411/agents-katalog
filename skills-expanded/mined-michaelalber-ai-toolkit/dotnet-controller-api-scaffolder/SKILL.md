---
name: dotnet-controller-api-scaffolder
audience: team
description: >
  Scaffolds controller-based ASP.NET Core Web API endpoints ([ApiController]/ControllerBase)
  that CONFORM to an existing codebase — base controller, validation (DataAnnotations or
  FluentValidation), service layer vs. mediator, response envelope, routing, versioning, DI.
  Detect-and-match, never impose. Use when adding controllers/actions to an existing
  controller-based API. Not for greenfield Minimal APIs (minimal-api-scaffolder); use
  dotnet-vertical-slice only when the team has chosen CQRS/vertical-slice.
---

# ASP.NET Core Controller API Scaffolder

> "When in Rome, do as the Romans do."
> — Ambrose of Milan

> "A good API is not just easy to use but also hard to misuse."
> — Joshua Bloch

## Core Philosophy

This skill adds controller-based Web API endpoints to an **existing** ASP.NET Core
codebase. The codebase already has conventions — a base controller, a validation
style, a way to talk to the data/service layer, a response shape, a routing scheme.
This skill's job is to **detect those conventions and conform to them**, producing
controllers a reviewer cannot distinguish from hand-written team code.

**Non-Negotiable Constraints:**

1. **Detect Before Generate** — No controller is written until the existing conventions are inventoried (base controller, validation, service/mediator boundary, response envelope, routing, versioning, auth). Matching the team beats matching a textbook.
2. **Conform, Don't Convert** — Never refactor existing controllers, swap their validation library, or introduce CQRS/mediator into a service-layer project. New code adopts the dominant existing pattern; style changes are a separate, explicit decision.
3. **`[ApiController]` + Attribute Routing** — Every API controller derives from `ControllerBase` (never `Controller`), carries `[ApiController]`, and uses attribute routing (`[Route]`, `[HttpGet]`…). No convention-based MVC routing for APIs.
4. **Thin Controllers** — Controllers orchestrate: bind, validate, delegate to the service/mediator boundary the project already uses, map to a response. No business logic, no EF queries inline, no `try/catch` per action when a global handler exists.
5. **Typed Contracts & ProblemDetails** — Actions accept and return DTOs (never entities), declare `[ProducesResponseType]` for every status code, and surface errors as RFC 7807 `ProblemDetails` — or the project's existing error envelope if one is established.

The full 10-row Domain Principles Table, Knowledge Base lookups, AI Discipline Rules,
Anti-Patterns Table, and Error-Recovery procedures live in
`references/principles-and-pitfalls.md`.

## Workflow

The lifecycle flows: **DETECT → SCAFFOLD → SECURE → DOCUMENT**. DETECT is mandatory and
gates everything else — its output is the convention profile every later phase obeys.

### Phase 1: DETECT (mandatory)

Inventory the existing conventions. See `references/convention-detection.md` for the grep commands.

- [ ] Target framework(s) — `grep <TargetFramework>` across `.csproj`
- [ ] Base controller — does an `ApiControllerBase` / `BaseApiController` exist? What does it provide?
- [ ] Data/service boundary — service layer (`IXxxService`), mediator (`Send()`), or direct `DbContext`?
- [ ] Validation approach — DataAnnotations attributes vs. FluentValidation `IValidator<T>`
- [ ] Response shape — raw DTO, `ActionResult<T>`, or a custom envelope (`ApiResponse<T>`)?
- [ ] Routing & versioning — route template prefix, versioning scheme (URL/header/query)
- [ ] Authorization default — class-level `[Authorize]`? Policies? Anonymous opt-out?
- [ ] DI registration & folder/namespace layout for controllers, DTOs, services
- [ ] **Emit the convention profile** (see State Block) and confirm it before generating

### Phase 2: SCAFFOLD

Generate controller + DTOs + (validators or annotations) matching the profile.

- [ ] Create the controller deriving from the detected base (or `ControllerBase` + `[ApiController]`)
- [ ] Apply the project's route template and versioning scheme
- [ ] Generate CRUD (or requested) actions with correct verbs and status codes
- [ ] Create request/response DTOs (records) — no entity leakage
- [ ] Add validation in the project's style (DataAnnotations OR `IValidator<T>`)
- [ ] Delegate to the project's data boundary (service OR mediator OR matched DbContext)
- [ ] Register any new service/validator in DI following the existing registration site

### Phase 3: SECURE

- [ ] Apply the authorization default (class-level `[Authorize]`, explicit `[AllowAnonymous]`)
- [ ] Apply specific policies for sensitive actions, matching existing policy names
- [ ] Confirm CORS/rate-limiting are inherited from existing middleware (do not add a second config)
- [ ] Verify no secrets or connection strings are introduced inline

### Phase 4: DOCUMENT

- [ ] Every action declares `[ProducesResponseType]` for all status codes
- [ ] XML doc comments on public actions if the project ships them (`GenerateDocumentationFile`)
- [ ] Swagger/OpenAPI renders the new controller grouped correctly
- [ ] Request/response schemas appear in the OpenAPI document

## State Block

```
<controller-scaffold-state>
mode: DETECT | SCAFFOLD | SECURE | DOCUMENT
target_framework: net8.0
base_controller: ApiControllerBase   # or "ControllerBase (none found)"
data_boundary: service-layer         # service-layer | mediator | direct-dbcontext
validation: dataannotations          # dataannotations | fluentvalidation
response_shape: ActionResult<T>      # ActionResult<T> | ApiResponse<T> envelope | raw DTO
versioning: url-segment              # url-segment | header | query | none
auth_default: class-level [Authorize]
controllers_created: [UsersController]
last_action: Detected conventions; emitted profile for confirmation
next_action: Scaffold UsersController matching service-layer + DataAnnotations
</controller-scaffold-state>
```

## Output Template

```markdown
## Convention Profile: [Solution] | .NET [version]
| Aspect | Detected | New code will |
|--------|----------|--------------|
| Base controller | ApiControllerBase | derive from it |
| Data boundary | IXxxService service layer | inject + delegate |
| Validation | DataAnnotations | annotate DTOs |
| Response shape | ActionResult<T> | match |
| Versioning | /api/v{n} URL segment | match |
| Auth default | class-level [Authorize] | match |

## Controller: [Resource]Controller
Route: /api/v{n}/[resource] | Base: [base] | Auth: [Required/Anonymous]
| Verb | Route | Action | Request DTO | Response DTO | Status Codes |
| GET | / | GetAll | [Query]DTO | PagedResult<T> | 200,401 |
| GET | /{id} | GetById | — | TDto | 200,404,401 |
| POST | / | Create | CreateTRequest | TDto | 201,400,401 |
| PUT | /{id} | Update | UpdateTRequest | — | 204,400,404,401 |
| DELETE | /{id} | Delete | — | — | 204,404,401 |
```

Full controller, DTO, validator, ProblemDetails, and testing templates:
`references/controller-patterns.md`. Convention detection commands:
`references/convention-detection.md`. Auth/CORS/rate-limit/integration-test patterns:
`references/security-and-testing.md`.

## Integration with Other Skills

| Skill | Integration Point | When to Use |
|-------|-------------------|-------------|
| **dotnet-architecture-checklist** | Review the controller/N-tier project before and after scaffolding | Confirms the detected style and grades against it |
| **minimal-api-scaffolder** | Sibling for the Minimal API paradigm | When the project is (or should be) Minimal API, not controllers |
| **dotnet-vertical-slice** | Alternative for teams that have chosen CQRS/vertical slice | Only when the team uses that architecture — not for layered projects |
| **test-scaffold** | Generate controller integration tests | `WebApplicationFactory<Program>` tests exercising the new actions |
| **dotnet-security-review** | Security audit of the new endpoints | Verify auth, validation, CORS, and no entity leakage |
| **ef-migration-manager** | Schema changes behind new endpoints | When new actions require entities or migrations |
| **react-feature-slice** | Front-end consumer of these endpoints | Generate the typed React data layer that calls the new controller |

References: `references/principles-and-pitfalls.md` (principles, KB lookups, discipline,
anti-patterns, error recovery) | `references/convention-detection.md` (detection grep
commands + decision rules) | `references/controller-patterns.md` (controller, DTO,
validator, ProblemDetails templates for service-layer and mediator variants) |
`references/security-and-testing.md` (authorization, CORS, rate limiting, integration tests).
