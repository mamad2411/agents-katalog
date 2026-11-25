---
name: smoke-verify
description: Stack-agnostic boot-check run as the FINAL step of a behaviour-preserving sweep (/optimize, /audit, /align, /migrate). A green test suite does NOT prove the app still starts — a refactor can break DI wiring, route/handler registration, an import cycle, or config loading that no unit test exercises. This skill actually boots the app (dev server / HTTP server + health probe / CLI invocation / library import) per PROJECT_KIND and FAILS if it doesn't come up. Reuses frontend/skills/dev-server-start/SKILL.md for frontend stacks.
kind: skill
pack: code-quality
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: smoke-verify

## Purpose

Prove the application **still boots** after a behaviour-preserving change. Unit/integration tests pin logic; they do not catch the class of breakage that only surfaces at startup:

- broken dependency-injection wiring (a moved/renamed provider no longer resolves),
- routes/handlers/commands that silently fail to register,
- an import cycle introduced by extracting a module,
- config / env loading that throws before the first request,
- a build/transpile error in a path no test imports.

"Tests are green" + "the app doesn't start" is a real, common post-refactor state. This skill closes that gap. It is the **last** step of a sweep — after the final commit, before reporting success.

## When to use

- Dispatched as the final step by `/optimize`, `/audit`, `/align`, `/migrate` (after the last fix commit).
- On demand: `verify the app still boots after these changes`.
- **Skip** with `--no-boot-check` for pure libraries/SDKs with no runnable entry point. Note that this is rarely the right call: the `library-*` row below (import the package entry) is cheap and catches import cycles, which is the single most common thing an extract-module refactor breaks. `--no-boot-check` is for the case where there is genuinely nothing importable, not for the case where booting is inconvenient.

## Procedure (stack-conditional via PROJECT_KIND)

1. **Resolve the boot command** from `ai/stack.md` § Scripts + `PROJECT_KIND`:

   | PROJECT_KIND | Boot check | Pass criterion |
   |---|---|---|
   | `frontend-*` | dispatch `frontend/skills/dev-server-start/SKILL.md` (dev server up) | server listens + index route 200, no console boot errors |
   | `backend-*` / `api-*` | start the server (`<pm> run dev` / `uvicorn` / `rails s` / etc.) on an ephemeral port | process stays up ≥ N s AND health/`/` probe returns < 500 |
   | `cli-*` | invoke the entry with `--help` / `--version` | exit 0, no stack trace |
   | `mobile-*` | `expo start`/Metro bundler starts OR the build step compiles | bundler ready / build exits 0 |
   | `library-*` | import the package entry in a throwaway script (`node -e "require('<pkg>')"` / `python -c "import <pkg>"`) | import returns 0 |
   | `data-*` (pipeline) | in order of preference: (a) the pipeline tool's own validate/dry-run (`dbt parse` / `airflow dags test` / `dagster job execute --dry-run` / `--check`), else (b) import the DAG/pipeline definition module in a throwaway script — this alone catches the DI, import-cycle and config-load failures the skill exists for, else (c) run the entry against a fixture with a one-row input and an ephemeral output sink | (a)/(c) exit 0 · (b) import returns 0 |

2. **Boot with a timeout** (default 60 s). Capture stdout+stderr. Kill on success criterion met or timeout.
3. **Decide**:
   - Boot succeeded within timeout → PASS; report the URL/exit observed.
   - Process exited non-zero, threw on startup, or never reached the pass criterion → **FAIL**: surface the captured startup error verbatim (the first error is almost always the cause), name the likely category (DI / route-reg / import-cycle / config), and HALT the sweep — do NOT report success.
4. **Clean up**: stop the dev server / kill the process / remove the throwaway import script.

## Verify (the check on the check)

- The boot command actually ran (a skipped boot due to a missing script is a WARN, not a silent PASS — say so).
- For servers: the health probe response was observed, not assumed.
- For CLI/library: the real exit code was captured, not inferred.
- **Every row resolves to one of exactly three outcomes** — `PASS` (criterion observed), `FAIL` (halt the sweep), or `WARN [no-boot-path]` naming what is missing. There is no fourth outcome, and in particular an "if one exists" that found nothing is a **WARN, not an omission**: it must appear in the report so the reader knows the sweep shipped without a boot check.

## Anti-patterns this prevents

- **The Green-Suite Mirage** — tests pass, app won't start; shipped because nobody booted it. (Exactly the asymmetry where `dev-server-start` was only wired into `/scaffold-project`, never the maintenance sweeps.)
- **The Optimistic Boot Claim** — "should still start" reported without starting it.

## See also

- `frontend/skills/dev-server-start/SKILL.md` — the frontend boot implementation this delegates to.
- `frontend/skills/verify-with-playwright/SKILL.md` — deeper post-boot UI verification (optional follow-on).
- `code-quality/skills/test-shield/SKILL.md` — the pre-sweep counterpart (coverage gate before the fix).
- `ai/stack.md` — the canonical boot/dev scripts per project.
