---
name: env-diff
description: Compare .env against .env.example — flag missing keys (will break at runtime), orphan keys (dead config), and unvalidated keys (absent from the env schema). Run after pulling a branch that may have added env vars, after editing the env schema, and in CI as a pre-deploy gate. Checks key presence and validation wiring only, never whether a value is correct.
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# env-diff

## Premise

Find real config drift, not vibes. Every flagged key cites which file it's in (or absent from) + whether the schema marks it required. "Some env vars look off" is not a finding. NEVER print VALUES — keys only; values are secrets. A clean diff against an empty `.env.example` is suspicious — verify the example actually lists the project's real keys.

A run that returns zero findings without proving the schema was loaded is a failed run.

Config bugs are a top-5 cause of "it works on my machine". Surface missing / orphan / unvalidated env keys before boot.

## When to use

- After pulling a branch that may have added env vars.
- After editing `shared/config/env.schema.ts` (joi/zod) — verify schema, example, and live `.env` agree.
- Before onboarding a new dev.
- In CI as a pre-deploy gate.

## Prerequisites

- `comm` and `awk` (POSIX; preinstalled on macOS/Linux).
- The repo's env schema file path (commonly `shared/config/env.schema.ts`, `apps/*/src/config/env.validation.ts`).

## Procedure

1. Enumerate every env file, and pair them by app:
   ```bash
   ls -1 .env* 2>/dev/null
   ```
   One `.env` + `.env.example` is the single-app case. A repo with several deployable apps carries a
   pair per app (`.env.<app>` + `.env.<app>.example`) — **derive the app names from what is on disk
   and from the workspace/monorepo config, never from a convention this skill assumes.** A hardcoded
   app list is how a scan reports "clean" on the two files it knew about and silently ignores a third.

2. Extract key sets:
   ```bash
   keys() { grep -oE '^[A-Z][A-Z0-9_]+' "$1" | sort -u; }
   ```

3. Diff example vs live for each pair:
   ```bash
   comm -23 <(keys .env.example) <(keys .env)   # MISSING in live
   comm -13 <(keys .env.example) <(keys .env)   # ORPHAN in live
   ```

4. **Diff the precedence chain, not just the pair.** This is the half that actually bites, because a
   key can be present in `.env` and still not be the value the process sees. Most loaders resolve a
   *stack* of files, and the winner is not the file you edited. **Read the loader's own documented
   order before reporting** — it differs by tool and by mode, and asserting an order you did not read
   is the same defect as asserting a value you did not measure.

   ```bash
   for f in .env .env.local .env.development .env.development.local \
            .env.production .env.production.local .env.test; do
     [ -f "$f" ] && printf '%-32s %s\n' "$f" "$(keys "$f" | tr '\n' ' ')"
   done
   ```

   Report a key that appears in **more than one** file in the chain as `SHADOWED`, with the full list
   of files that define it, in resolution order, and which one wins. A `SHADOWED` key is not
   automatically a bug — `.env.local` overriding `.env` is what `.env.local` is *for* — but it is the
   thing that makes "I changed it and nothing happened" unexplainable, and the diff is the only place
   it is visible. Flag it as a bug when the shadowing file is **committed** (`git ls-files --error-unmatch <f>`):
   a machine-local override that ships to every clone is not an override, it is a second default.

5. **Check client-exposure prefixes before reporting a MISSING key as harmless.** Bundlers inline
   only prefixed variables into the client bundle (`VITE_`, `NEXT_PUBLIC_`, `PUBLIC_`, `REACT_APP_`,
   `EXPO_PUBLIC_` — confirm the prefix from the project's own bundler config, do not assume). Two
   findings live here and nowhere else in this skill:
   - A **secret-looking key carrying an exposure prefix** (`*_SECRET`, `*_KEY`, `*_TOKEN`, `*_PASSWORD`)
     is a leak, not a config nit — it is compiled into a file the public downloads. Report it and halt.
   - A **non-prefixed key read from client code** is `undefined` at runtime, not missing at boot. It
     presents as a feature silently doing nothing, which is why nobody files it as a config bug.

6. Cross-check example keys against the env schema validator (joi/zod/pydantic-settings) — keys present
   in the example but absent from the schema are UNVALIDATED.

7. **Triage MISSING by what the schema says about each key, rather than counting them.** Read the
   required/optional/default declaration out of the schema (`.required()` / `.optional()` /
   `.default(…)` in joi and zod; `Field(...)` vs `Field(default=…)` in pydantic-settings) and split:

   | Class | Schema says | Consequence | Verdict |
   |---|---|---|---|
   | **BOOT-BLOCKING** | required, no default | the process exits on start | HIGH — fix before anything else |
   | **SILENTLY-DEGRADED** | optional with a default | boots fine; one feature is quietly off or pointing at a fallback | **the dangerous class** — name the feature the default disables, because nothing else will |
   | **INERT** | optional, no default, guarded at the read site | genuinely fine | note, do not escalate |

   A count of "4 MISSING" is not a finding. `1 boot-blocking + 3 silently-degraded` is, because the
   three are the ones that make it to production wearing a green health check.

## Output

```
Env diff — .env vs .env.example        (schema: shared/config/env.schema.ts, zod)

MISSING — BOOT-BLOCKING (1):     required, no default → process exits on start
  DATABASE_URL

MISSING — SILENTLY-DEGRADED (2): optional with a default → boots green, feature off
  REDIS_URL                 default: in-memory cache. Cache is per-pod; invalidation
                            crosses no process boundary. Looks fine on one replica.
  ANTHROPIC_API_KEY         default: none; guarded read disables the summariser.

MISSING — INERT (1):
  WHATSAPP_APP_SECRET       optional, read site guarded at notify.service.ts:41

SHADOWED (1):
  API_BASE_URL              .env → .env.local (wins).  .env.local is UNTRACKED — ok.

ORPHAN (2):
  OLD_API_KEY               (remove from .env — no longer used)
  DEBUG_MIGRATION_TRACE     (remove from .env.example — only for one-off debug)

UNVALIDATED (1):
  CUSTOM_FEATURE_FLAG       (add to shared/config/env.schema.ts)

Boot risk: HIGH — 1 boot-blocking key missing.
Silent risk: 2 keys degrade a feature without failing the health check.
```

## False positives / gotchas

- Comments and blank lines — strip with the `^[A-Z]` anchor in `keys()`.
- `KEY=` (set but empty) is valid syntax but often a misconfiguration — flag empty values separately if the schema requires non-empty.
- Multi-line values (e.g., `PRIVATE_KEY="-----BEGIN..."`) require careful parsing — `dotenv-cli`'s parser is more accurate than naive grep.
- NEVER print VALUES — only keys. Values may be secrets.
- `.env` MUST stay gitignored. If it shows up in `git status`, stop and check `.gitignore`.
- **An ORPHAN key is not always dead.** It may be read by a sibling app in the same repo, by a
  deployment manifest, or by a script outside the app's source tree. Grep the whole repo — including
  `infra/`, CI config and Dockerfiles — before recommending a removal; a "dead config" removal that
  breaks a deploy pipeline is a worse outcome than the drift.
- **A key with a default is still MISSING.** The schema not failing is what makes it dangerous, not
  what makes it fine.

## Related

- `.claude/skills/module-scaffold/SKILL.md` — a scaffolded module that adds config keys is a common source of the drift env-diff catches; run env-diff after scaffolding.
- `.claude/skills/endpoint-test-method/SKILL.md` — a route that 500s on boot is often a MISSING required key; env-diff isolates config drift before blaming the handler.
- **Dispatched by `/fix-bug` and `@bug-investigator`** — both route the "works on my machine / works in one
  environment but not another" signal here *before* the handler is read, because config drift presents as a code
  bug and is not one (`/fix-bug` Phase 3; the agent's Evidence gathering § Config drift). Those two are the only
  callers this skill has; rename it and you must edit both.
- `security` pack — secret storage / rotation; env-diff reports keys only and never values, deferring value handling there.
- `.claude/rules/backend-principles.md` — the env-schema-validation MUST/SHOULD behind the UNVALIDATED classification.

## Halt conditions

- Halt on hand-waves: every MISSING / ORPHAN / UNVALIDATED entry must cite the file it's in (or absent from) + the schema's required flag.
- Halt if any value (not key) appears anywhere in the output — values are secrets and never printed.
- Halt if `.env` shows up in `git status` — that's a security incident, not a diff finding.
- Halt if the schema validator file (joi/zod/pydantic) couldn't be located — without the schema the "UNVALIDATED" classification is a guess, and so is the required/optional/default split that the whole triage rests on. Report `triage: NOT RUN (schema not located)` rather than emitting a raw MISSING count that reads like a verdict.
- Halt on a secret-shaped key carrying a client-exposure prefix — that is a disclosure finding, not a config diff, and it does not wait for the rest of the report.
- Report the precedence chain as observed from the loader's documented order, or state that the order was not confirmed. An asserted resolution order is the same class of guess this skill refuses everywhere else.
