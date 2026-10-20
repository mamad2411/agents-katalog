---
name: genai-workflow
description: Produce the Generative AI deliverable V6 grades — the prompt used to scaffold the task API, a representative output sample, and a written account of how AI output was validated, corrected, and hardened for edge cases/auth/validation. Load this skill when writing the GenAI section of the README/presentation, capturing prompts, or documenting critical evaluation of AI-generated code.
---

# Generative AI Workflow & Documentation

V6 has a dedicated **Generative AI tools** section and grades **GenAI fluency + critical thinking** at the panel. This is a **written deliverable**, not just something you did — capture it as you build.

## What V6 Requires You to Produce

1. **The prompt** you would use to generate the task-management API scaffold or full implementation.
2. **The output code** (or a representative sample).
3. **A description of how you:**
   - Validated the AI's suggestions
   - Corrected or improved the output, if necessary
   - Handled edge cases, authentication, or validations

## Capture As You Go (don't reconstruct at the end)

- Keep a running `docs/genai.md` (or a README section). Every time a prompt produces something you accept, tweak, or reject, jot the before/after and *why*. Reconstructed-from-memory prompt logs read as inauthentic to a panel that does this daily.
- This project is itself the evidence: it was scaffolded with Claude Code under `.claude/` rules + skills. That curated-context approach **is** a prompt-engineering story — tell it (see "Angle" below).

## Writing the Prompt (show a strong one)

A good scaffolding prompt is specific about contract, architecture, and constraints:

> Generate an ASP.NET Web API for a task-management system using Clean Architecture (Domain/Application/Infrastructure/WebAPI), CQRS via MediatR, EF Core (SQL Server). Entities: `Task` (Id, Title, Description, Status, DueDate, UserId) and `User` (Id, hashed credentials). Include CRUD use cases for Task and register/login for auth, cookie-based JWT, FluentValidation on inputs, and NUnit tests written test-first. Tasks are scoped to the authenticated user. Follow TDD: for each use case, produce the failing test first.

Point out *why* it's good: names the architecture, pins the entity contract, states the auth model, and demands tests-first — leaving little for the model to guess wrong.

## Validating AI Output — the Critical-Thinking Part (graded)

Document concrete checks you applied, e.g.:

- **Architecture leaks** — did the handler reference `DbContext` or `HttpContext` directly? (It shouldn't; see the `clean-architecture` skill.) Caught and corrected → strong evidence of critical evaluation.
- **Stale/invented APIs** — did it pin an outdated MediatR/EF Core version or call a method that doesn't exist? Cross-checked against latest stable (see the `packages-backend` skill).
- **Security shortcuts** — plaintext passwords, `ValidateLifetime = false`, `AllowAnyOrigin()` with credentials, a client-supplied `UserId`. Each is a real failure mode of naive AI output — flag which you found (see the `security-backend` skill).
- **Test theater** — tests that assert nothing meaningful or mock the thing under test. Replaced with behavior assertions (see the `testing-tdd` skill).
- **Edge cases the model skipped** — empty task list returning 404 instead of `[]`, past due dates, duplicate registration, accessing another user's task.

For each: *what the AI produced → what was wrong → how you corrected it.* That before→after is exactly the fluency the panel scores.

## Angle That Lands Well

Frame it as **curated context, not one-shot prompting**: the `.claude/rules`→`skills` refactor, situational loading, and confirmed-against-real-source conventions show you drive the tool deliberately and verify its output — rather than pasting whatever it emits. That narrative directly answers "fluency with GenAI tools and prompt engineering, and critical thinking when evaluating AI-generated code."
