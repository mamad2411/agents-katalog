# Agent Guidelines

## Planning

### 1. Planning tasks

**Think through and understand the task before writing code. Step back when necessary.**

- State assumptions clearly. Present alternatives. Never guess - ask.
- Convert tasks into verifiable success criteria before writing code.
- For multi-step tasks, outline a brief plan with checkpoints.

---

## Rules for coding

### 2. Simplicity First

**Minimum code for the problem. Nothing speculative.**

- No features beyond what was asked. No unrequested abstractions or "flexibility".
- No error handling for impossible scenarios.
- If you write 200-500 lines and it could be 50, rewrite.
- Если размер исходного файла превышает 40-50кБ, то это кандидат для рефакторинга и раздления файла на по зонам ответственности (класам или логике).
- Если размер исходного стал более 100кБ, то должен быть предолжен пран по его упрощению (раздлениею) на неслколько.

### 3. Surgical Changes

**Touch only what the task requires. Clean up your own orphans.**

- Match existing style. Do not "improve" adjacent code or formatting.
- Remove imports/variables/functions YOUR changes made unused.
- Do not refactor unrelated code. Mention dead code you find -- don't delete it.

### 4. Eliminate Duplication

**Reuse. One source of truth per concern. Prefer compile-time checks.**

- Check for existing implementations before writing new code.
- Avoid duplicating logic or checks.
- Prefer `static_assert` and type system over runtime checks.

### 5. No fallback for invalid data - raise an error (use FAULT and EXPECT with a diagnostic)

**Invalid input → FAULT or EXPECT, never use a silent fallback.**

- Any function that receives invalid data **must** call FAULT() or EXPECT(), not return {}, nulllopt, or any silent default result.

- When changing the API contract, update your tests to reflect the new contract. Fallback code cannot be added to satisfy old test requirements.

- An empty value for std::optional is only allowed when the value is missing. It is invalid when invalid input data is passed (an error/FAULT/EXPECT must be returned).

- Every `EXPECT()` and `FAULT()` call must include a human-readable diagnostic string:
  - `FAULT("description", args...)` - description is the first argument;
  - `EXPECT(expr && "description")` - description is added via `&& "..."`.
  - A bare `EXPECT(expr)` without a description is allowed for obvious checks only.

### 6. No Implicit Backward Compatibility

**Don't preserve history unless asked.**

- Never maintain backward compatibility unless explicitly required.
- Remove old code without deprecation layers or comments explaining removal.
- Breaking changes are default unless compatibility is specified.

### 7. Read and obey comments

**Always read comments and execute explicit requirements stated in them.**

- Comments may contain critical constraints (e.g. "The output directory cannot be deleted!").
- Never ignore, override, or remove a comment that states an explicit requirement.
- If a comment contradicts your intended change, stop and reconsider.


### 8. Use of Git or `.git` is prohibited.

**Use `.git` or any changes from `git`, or modifying or reorganizing Git data in any way, is strictly prohibited.**

- Any use of the `git` (including reading history ) is prohibited.
- Deny reading of the `.git` directory.
- Not allowed reading `git` history or creating stash.
- `grep` MUST **exclude** `.tasklog`, `.git`, `_build`, `.trust`, `node_modules` and other temporary/derived dirs (never scan them for patterns; never `grep -r` over the whole repo so they get included). **Обязательная форма** - явные `--exclude-dir` для всех временных/производных каталогов, а лучше и сужение корня поиска:
  - `grep -rn '<pattern>' src include test examples cmake --exclude-dir={_build,.tasklog,.git,_trust,.trust,node_modules}`
  - Нельзя: `grep -rn '<pattern>' .` (без исключений), `grep -rn '<pattern>' src` (если в `src` попадают производные файлы), поиск в `_build`/`.tasklog`/`.git` целиком.
  - `search_codebase`/поиск по коду - только по исходным каталогам (`src`, `include`, `test`, `examples`), без `_build`, `.tasklog`, `.git`.

---

## Quality Assurance

### 9. Follow CODESTYLE

**All code must follow [CODESTYLE.md](CODESTYLE.md) - naming conventions, formatting, prohibited and required patterns.**

- The naming conventions, formatting, prohibited and required patterns, code rules must follow [CODESTYLE.md](CODESTYLE.md)
- For compiler options and build targent in `CMakeLists.txt`.
- Run `clang-format` before committing.
- Run `clang-tidy` and fix all warnings.

### 10. Tests Are Non-Negotiable

**Every change needs test coverage. Never disable or skip tests.**

- Write tests for additions and modifications: normal paths, edge cases, errors.
- Never remove, skip, or disable tests without explicit permission.
- Fix underlying code on failure -- do not silence the test.
- Tests **MUST** never be silently skipped - missing test infrastructure (GTest, lit, python3, etc.) is a **BUILD FAILURE, not a silent skip or GTEST_SKIP()**.
- Do not delete generated/output files unless asked.
- All tests **MUST** be executed with a timeout (e.g., via `timeout` command) to prevent infinite loops or resource exhaustion.
- **Tests are ALWAYS adapted to code changes, NEVER the reverse.** If a change intentionally alters behavior/structure (incl. AST/term shape, grammar, codegen), update the affected tests to reflect the new contract. Do NOT revert/weaken a correct change to keep outdated tests passing. This also applies to parser tests that pin internal term/AST structure: they must be updated alongside the change.



### 11. Architecture and Persistent Memory From `MEMORY.md` Only

**Do not read header or source files to analyze architecture.**

- The `MEMORY.md` file in each component's directory is the **sole source** of architectural
  information and of persistent memory for that scope (architecture + facts, decisions, relations).
- A root `MEMORY.md` at the project root holds project-level facts, decisions, and
  cross-component relations.
- Read individual source/header files only when the task explicitly requires it or when modifying that specific file.
- Do not scan the project for "understanding" - read `MEMORY.md` or `README.md` first.
- **Exception**: when the task requires modifying/refactoring a specific type, read its complete
  definition (all fields, semantics, relationships) first - see `.clinerules/TASK.md`
  («Read structures before refactoring»). This does not contradict the rule: full type reading
  is done for the type being changed, not for analyzing the architecture.


### 12. Keep file `MEMORY.md` and `README.md` Synchronized

**`MEMORY.md` and `README.md` must always reflect the actual implementation.**

- If a code change reveals a discrepancy between `MEMORY.md`, `README.md` and the code - stop and report it.
- Update `MEMORY.md` in the same change set as the code modification.
- Mismatch between `MEMORY.md` or `README.md` and implementation is treated as a bug.

### 13. Source of documentation `docs/content`

**The Russian-language section `docs/content/ru` is the ONLY original source of documentation.**

- `docs/content/en` is a synchronous translation of `docs/content/ru` and is never an original source:
  it is edited only together with the corresponding `ru` change. English pages must not link to
  Russian-language originals (ru.wikipedia, habr.com/ru, etc.); use English equivalents or drop the link.
- The documentation serves as the basis for creating a site (taking into account the language prefix), so all links and anchors are written in English letters.
- The documentation describes the project's vision for its ultimate goal and may differ from the current implementation. Unrealized capabilities should be clearly identified (highlighted).
- Documentation serves only as a reference. A more important source of information for work is the task description or architecture.
---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation.

---

## Persistent Memory (`MEMORY.md`)

Persistent memory is stored in `MEMORY.md` files together with the architecture documentation:
one per component/directory plus a root project-level `MEMORY.md`. There is **no separate
memory server**.

### Scope

- Root `MEMORY.md` - project-level facts, decisions, and cross-component relations.
- Per-component `MEMORY.md` - the component's architecture and persistent facts relevant to
  that directory (its context/scope).
- **Any directory/component may contain its own `MEMORY.md`**; the file describes the context
  of the directory where it is located. The components currently having a `MEMORY.md` are the
  `include/<component>/` directories and `test/`.

### Rules (summary)

- Authoritative format - mandatory header metadata (`scope`, `role`, `last_reviewed`,

`review_period`, `max_size`) and mandatory sections (`## Architecture`, `## Facts and
invariants`, `## Decisions`, `## Relations`), as well as full rules for size limits and periodic
checks - are defined in `.clinerules/README.md`.

- Detailed criteria for what can/should be stored in `MEMORY.md` - see `.clinerules/TASK.md`

("Component Knowledge Check").

- Key principles: store only brief facts that are **difficult to determine** from code/API/documentation;
no timestamps, no error/task statuses, no plans (these should be in `.tasklog/`); the file must adhere to the `max_size` limit; Before adding, check for duplicates and, if necessary, shorten the information in the file, keeping the most important information in a more compact form; update the `last_reviewed` value after each review;