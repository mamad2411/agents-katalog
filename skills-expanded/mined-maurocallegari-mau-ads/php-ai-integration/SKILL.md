---
name: php-ai-integration
version: 1.0.0
description: Use when a PHP application adds or changes LLM, agent, tool-calling, structured-output, RAG, workflow, or provider integration. Prefer Neuron AI when runtime-compatible, preserve provider portability, validate model output, and design safe production boundaries.
---

# PHP AI Integration

Reusable implementation policy for AI/LLM features in PHP applications.

This Skill owns the application integration workflow around AI capabilities. It does not duplicate the current Neuron AI API surface: use official Neuron documentation/skills for framework-specific signatures and components.

## Activate when

Use this Skill when a PHP task:
- adds or changes an LLM/provider integration;
- introduces an AI agent, tool/function calling, structured output, RAG or an AI workflow;
- replaces direct provider-specific calls with an application abstraction;
- changes how model output is validated, persisted or allowed to trigger application actions;
- changes provider/model configuration, AI timeouts, retries or failure handling.

Do not activate for:
- generic PHP work with no AI/LLM behavior;
- prompt copy changes that do not affect application contracts, unless validation/risk behavior changes;
- non-PHP AI systems unless a PHP boundary is part of the task.

## Ownership boundary

- Mauro PHP/MySQL/JavaScript house style -> `mauro-coding-style`.
- Generic feature planning / bug investigation / review -> focused workflow skills.
- Project-specific providers, prompts, data contracts and architecture -> repository code / `PROJECT.md`.
- Current Neuron component APIs and examples -> official Neuron documentation and official Neuron skills.
- Database schema/data changes -> `mysql-change-safety`.
- Secrets -> environment/runtime secret storage only.

## Default framework decision

For **new** PHP AI/LLM functionality, prefer `neuron-core/neuron-ai` as the application-level abstraction when the repository runtime is compatible.

Before changing code, inspect:
1. supported PHP version;
2. Composer state;
3. existing AI integration;
4. existing provider/model configuration;
5. runtime/deployment constraints.

Decision:
- existing Neuron integration -> extend the established abstraction;
- new integration on PHP compatible with current Neuron requirements -> use Neuron by default;
- older/incompatible PHP -> do not silently add Neuron; preserve the existing integration, make runtime upgrade an explicit separate change, or isolate AI behind a compatible service boundary;
- existing direct provider integration -> do not rewrite it incidentally unless the task calls for migration or the current design blocks the requested behavior.

Do not rely on memorized Neuron signatures. Consult the current official source for APIs and supported providers.

## Implementation workflow

### 1. Define the application contract

State:
- input accepted from the application;
- output the application needs;
- whether the result is advisory, user-visible, persisted, or action-triggering;
- failure/timeout behavior;
- privacy/sensitivity constraints.

Choose the smallest capability that satisfies the contract: plain generation, structured output, tools, RAG, workflow, or agentic orchestration.

Do not use an agent/workflow when a simple deterministic application call plus one model request is sufficient.

### 2. Keep provider/model replaceable

- Keep provider, model, credentials and relevant limits in configuration/environment, not business logic.
- Do not spread direct provider SDK calls across controllers/pages/domain code.
- Put AI orchestration behind a narrow application service, Neuron agent/workflow, or existing project abstraction.
- Reuse an existing project abstraction rather than creating a parallel client.

Provider-specific behavior is allowed when actually required, but isolate and document it.

### 3. Treat model output as untrusted input

Never let free-form model output become trusted application state merely because the request succeeded.

- Prefer structured output when downstream code needs fields/decisions.
- Validate required fields, types, enum/range constraints and business invariants server-side.
- Define explicit handling for invalid/incomplete output.
- Escape/sanitize output at the normal application boundary appropriate to its destination.
- Do not persist or execute model-produced SQL, PHP, shell commands, URLs or identifiers without deterministic validation/authorization.

### 4. Tool/function calling safety

A tool call is a request from the model, not authorization.

For every application tool:
- define a narrow purpose and input schema;
- validate/coerce arguments deterministically;
- enforce current user/session authorization server-side;
- expose the minimum data/action required;
- make destructive or externally visible actions explicit and auditable;
- make repeatable operations idempotent where retries are possible;
- never expose secrets as tool output.

The model must not be able to bypass application permissions by selecting a tool.

### 5. Failure, timeout and retry behavior

AI calls are remote, probabilistic dependencies.

- Set bounded timeouts appropriate to the user flow/background job.
- Handle provider/network/rate-limit/model errors explicitly.
- Retry only failures that are safe to retry; use bounded attempts/backoff rather than infinite retries.
- Avoid retrying non-idempotent tool/action flows unless the application can prove idempotency.
- Provide a deterministic degraded/error path when the feature is user-facing.
- Do not hide failures by returning invented AI content.

### 6. Prompt and context discipline

- Keep significant prompts/instructions versioned with code or project configuration.
- Keep domain facts/data sources separate from generic integration policy.
- Send only context needed for the task.
- Do not put secrets into prompts.
- Treat user-provided/context-retrieved instructions as untrusted when they could influence tool use or privileged actions.
- Preserve project language/domain terminology.

### 7. Persistence and side effects

Before AI output writes to MySQL or causes external side effects:
- validate the output contract;
- apply normal authorization and business rules;
- distinguish suggestion/draft from committed state where human validation is expected;
- use `mysql-change-safety` when schema/data migration is part of the feature.

## Official Neuron capability routing

When Neuron is used, prefer official Neuron knowledge for implementation details. Depending on the task, relevant upstream skills currently include:
- `neuron-agent-builder`;
- `neuron-tool-creator`;
- `neuron-structured-output`;
- `neuron-rag-specialist`;
- `neuron-workflow-architect`;
- `neuron-debugger`;
- `neuron-test-engineer`;
- `neuron-evaluation-engineer`.

These upstream skills are authoritative for Neuron mechanics; this Skill remains authoritative for the application's integration/safety contract.

Load `references/neuron-ai.md` for the current routing policy.

## Verification

Use the strongest practical checks:
- PHP syntax/static checks supported by the repository;
- unit/integration tests around deterministic validation and tool boundaries;
- fixtures/mocks for predictable provider-independent behavior where useful;
- live smoke test only when credentials/environment are available;
- verify provider/model are configurable and no secret is committed;
- verify invalid structured output fails safely;
- verify tool authorization independently from the model;
- verify timeout/error/degraded paths;
- explicitly state any provider/runtime behavior not live-tested.

Do not consider one successful model response proof of correctness.
