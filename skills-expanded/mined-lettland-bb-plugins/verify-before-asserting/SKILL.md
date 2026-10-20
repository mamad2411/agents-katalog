---
name: verify-before-asserting
description: "Use when writing a concrete reference (env, path, command, version) into a plan or code: confirm it exists or mark it ASSUMPTION; never infer it."
metadata:
  added: 2026-06-24
  last_reviewed: 2026-06-24
  type: core
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-06-24"
  keywords:
    [
      guess,
      infer,
      assumption,
      hallucinate,
      verify,
      reference,
      env,
      config,
      port,
      schema,
      version,
      command,
      symbol,
      ground,
    ]
  related: [honest-completion, planning, brainstorming, requirements-gathering, debugging, code-review]
  owns: verify-before-asserting
---

# Verify before asserting

You're about to write `DATABASE_URL`, `npm run build`, or `localhost:5432` into a plan because the name _fits_ — it's what a setup like this usually calls things. Stop. A name that fits the convention is a guess wearing the costume of a fact. The reference is cheap to check; check it before you write it.

This is the mid-turn sibling of `honest-completion`: that skill stops you rounding a failed step up to "done" at the _end_ of the turn; this one stops you writing an unverified reference into the artifact _during_ the turn.

## The iron law

```
IF A REFERENCE IS CHECKABLE IN SECONDS, CHECK IT BEFORE YOU WRITE IT
```

A concrete reference is anything a reader could copy and run or look up: an env var, a config key, a path, a command, a port, a table or column name, a function or symbol, a dependency version, an API field. If it's wrong it fails for them — and "it followed the usual convention" is no defense.

## Confirm it — read-only — before you write it

| Reference                  | Confirm by (read-only)                                                      |
| -------------------------- | --------------------------------------------------------------------------- |
| env var / config key       | grep the repo + `.env.example` / settings; never assume the name            |
| env var **default value**  | read the default in code / compose; don't invent `localhost` / `5432`       |
| file path                  | read it / `ls`; don't infer it from layout conventions                      |
| CLI / make / just target   | read `package.json` scripts, `Makefile`, `justfile` — the target must exist |
| port number                | read the binding in config / compose; don't assume `3000` / `8080` / `5432` |
| DB table / column / schema | read the migration / model / schema file                                    |
| function / symbol          | ripwire or grep — confirm it's defined                                      |
| version / dependency       | read the lockfile / manifest, not memory                                    |
| API field / response shape | read the type / schema / fixture                                            |

"Read-only" is the rule: confirm by _reading_ the manifest or source. "A command you ran" means one you ran to **observe its output** where a run is genuinely needed — never license to speculatively execute a side-effecting command just to prove a name exists.

## Cite what you confirmed

Every concrete reference traces to evidence — a `path:line` you read or the command you ran:

- ✅ `DATABASE_URL` — confirmed `docker-compose.yml:14`
- ❌ silently writing `DATABASE_URL=postgres://localhost:5432/app`

The citation is the difference between a fact and a guess that happened to be right.

## Can't verify? Label it — don't smuggle it in

Sometimes you can't confirm a reference. That's allowed; a _silent_ guess is not. Mark it, and say which kind:

- `ASSUMPTION[new]: <ref> — introduced by this plan at <step / file>` — a thing you are _creating_. A legitimate forward reference; it doesn't exist yet because that's the point.
- `ASSUMPTION[unverified]: <ref> — existence unknown; confirm before relying on it` — you inferred it and could not check. The reader now knows to verify.

A labelled assumption is honest — it is `honest-completion`'s _needs-input_, mid-turn. An unlabelled one is the failure.

## Red-flag rationalizations

Each is a guess in disguise. Stop, then verify or label:

- "the convention is usually…"
- "it's probably called…"
- "standard setups have…"
- "I'll use the typical port / name / path"
- "the framework defaults to…" — does _this_ project override it? read and see

## Limits

This is a _soft_ rule. Nothing forces it: no hook can know whether `FOO_BAR` in a plan is a real env var unless the hook itself greps for it. It changes behavior only because it is surfaced — keyword routing in `skill-discovery` and the standing pointer in `using-devkit`. So it lives or dies on you actually applying it. `honest-completion` guards the end of the turn (don't report done after a failure); this guards during the turn (don't write unverified references). Reach for both.
