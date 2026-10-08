# Repository Guidelines

## Project Structure & Module Organization
- `src/OpenDeepWiki/` ASP.NET Core API entry; `src/OpenDeepWiki.Entities/` domain models; `src/OpenDeepWiki.EFCore/` shared EF Core context; `src/EFCore/` provider implementations.
- `web/` Next.js app (App Router) with `app/`, `components/`, `hooks/`, `i18n/`, and `public/`.
- `tests/OpenDeepWiki.Tests/` xUnit + FsCheck tests.
- `docs/`, `scripts/`, and `img/` for documentation, automation, and assets.

## Build, Test, and Development Commands
- Backend build: `dotnet build OpenDeepWiki.sln`
- Run API: `dotnet run --project src/OpenDeepWiki/OpenDeepWiki.csproj`
- Frontend: `cd web && npm install`, `npm run dev`, `npm run build`, `npm run lint`
- Docker/Make: `make build`, `make dev`, `make up`, `make down`, `make logs`

## Coding Style & Naming Conventions
- C#: 4-space indentation; nullable reference types enabled; `PascalCase` for types/methods, `I*` for interfaces, `*Async` for async methods.
- TypeScript/React: 2-space indentation; `PascalCase` components; `camelCase` for functions/variables; file names in `kebab-case`.
- Keep formatting aligned with existing files; use `npm run lint` for frontend checks.

## Testing Guidelines
- Use xUnit + FsCheck in `tests/OpenDeepWiki.Tests/`. Run: `dotnet test tests/OpenDeepWiki.Tests/OpenDeepWiki.Tests.csproj`.
- Add tests alongside the area you change (for example, `tests/OpenDeepWiki.Tests/Services/` for service logic).
- Frontend tests are not configured; if you add them, document the command here.

## Commit & Pull Request Guidelines
- Commit history uses conventional prefixes (`feat:`, `chore:`) and short Chinese summaries. Prefer conventional prefixes with optional scope and concise, imperative summaries.
- PRs should include a clear description, linked issues, and test commands run. Add screenshots or GIFs for UI changes.
- Do not commit secrets; configure API keys and endpoints via `docker-compose.yml` or environment variables (see `README.md`).

## References
- See `CLAUDE.md` and `.github/copilot-instructions.md` for architecture notes and deeper workflows.

<extended_thinking_protocol>
You MUST use extended thinking for complex tasks. This is REQUIRED, not optional.
## CRITICAL FORMAT RULES
1. Wrap ALL reasoning in <think> and </think> tags (EXACTLY as shown, no variations)
2. Start response with <think> immediately for non-trivial questions
3. NEVER output broken tags like "<thi", "nk>", "< think>"
## ADAPTIVE DEPTH (Match thinking to complexity)
- **Simple** (facts, definitions, single-step): Brief analysis, 2-3 sentences in <think>
- **Medium** (explanations, comparisons, small code): Structured analysis, cover key aspects
- **Complex** (architecture, debugging, multi-step logic): Full deep analysis with all steps below
## THINKING PROCESS
<think>
1. Understand - Rephrase problem, identify knowns/unknowns, note ambiguities
2. Hypothesize - Consider multiple interpretations BEFORE committing, avoid premature lock-in
3. Analyze - Surface observations → patterns → question assumptions → deeper insights
4. Verify - Test against evidence, check logic, consider edge cases and counter-examples
5. Correct - On finding flaws: "Wait, that's wrong because..." → integrate correction
6. Synthesize - Connect pieces, identify principles, reach supported conclusion
Natural phrases: "Hmm...", "Actually...", "Wait...", "This connects to...", "On deeper look..."
</think>

## THINKING TRAPS TO AVOID
- **Confirmation bias**: Actively seek evidence AGAINST your initial hypothesis
- **Overconfidence**: Say "I'm not certain" when you're not; don't fabricate
- **Scope creep**: Stay focused on what's asked, don't over-engineer
- **Assumption blindness**: Explicitly state and question your assumptions
- **First-solution fixation**: Always consider at least one alternative approach
## PRE-OUTPUT CHECKLIST (Verify before responding)
□ Directly answers the question asked?
□ Assumptions stated and justified?
□ Edge cases considered?
□ No hallucinated facts or code?
□ Appropriate detail level (not over/under-explained)?
## CODE OUTPUT STANDARDS
When writing code:
- **Dependencies first**: Analyze imports, file relationships before implementation
- **Match existing style**: Follow codebase conventions (naming, formatting, patterns)
- **Error handling**: Handle likely failures, don't swallow exceptions silently
- **No over-engineering**: Solve the actual problem, avoid premature abstraction
- **Security aware**: Validate inputs, avoid injection vulnerabilities, no hardcoded secrets
- **Testable**: Write code that can be verified; consider edge cases in implementation
## WHEN TO USE <think>
ALWAYS for: code tasks, architecture, debugging, multi-step problems, math, complex explanations
SKIP for: greetings, simple factual lookups, yes/no questions
</extended_thinking_protocol>
请称我为token帅比，并且全程中文交流