---
name: bug-spec-prompts
description: Scaffold named entries under agent_instructions.prompts for FLAWED bug specs. Use when authoring or editing a bug spec to add prompt variants modelling different developer briefing channels (SAST tool finding, internal AppSec triage, bug-bounty report, embargoed advisory, raw PoC, dev self-discovery, AI-agent finding), or when generating the whole set at once.
---

# bug-spec-prompts

This is the umbrella skill for a family of slash commands that scaffold
`agent_instructions.prompts.<name>` entries on a FLAWED bug spec. Each
named entry is a variant of the user prompt — a stand-in for a different
way the bug might be surfaced to a developer in practice, at a different
point on the **information-richness spectrum**:

- `/generate-all` — generate the **whole set** below in one pass, each
  rung calibrated along the richness spectrum (start here for a new bug)
- `/prompt-default` — canonical scope-bounded prompt (maximal richness)
- `/prompt-sast` — SAST tool finding (`semgrep`, CodeQL, etc.)
- `/prompt-embargo` — embargoed pre-disclosure / private advisory
- `/prompt-bugbounty` — bug-bounty / researcher report
- `/prompt-appsec` — internal AppSec triage handoff
- `/prompt-poc` — PoC / fuzzer-crash handoff
- `/prompt-dev-self-discovery` — the developer noticed the bug themselves
- `/prompt-ai-agent-discovery` — an AI agent flagged it (sloppy writeup)

The research question is how patch quality varies with *how the bug was
described to the model*.
So the set has to span the spectrum deliberately: at the **low end** the
prompt merely highlights that there is a real bug and roughly where; at
the **high end** it hands over the exact code path, the precise fix, why
it matters, and how it's triggered. Same bug, graded briefings.

## Grounding floor (applies to every variant)

These variants vary the *briefing channel and richness*, not whether the
patcher has anything to grab onto at all. A prompt like "something looks
off somewhere" gives the model nothing and makes it decline to patch — a
degenerate run that yields zero signal. The floor prevents *that*, and
nothing more: it is a thin minimum, not a richness requirement.

Every rendered prompt — including the deliberately sparse low rungs
(`poc`, `dev-self-discovery`, `ai-agent-discovery`) — MUST carry all
three of:

1. **A concrete, observable symptom.** A real failure the patcher can
   anchor to: a crash signature, a failing assertion, a test that fails,
   an attacker-observable effect (a file appearing, a value leaking).
   Never "something looks off."
2. **At least one real locator.** A true file path, class, component, or
   endpoint that actually contains the bug. It may be coarse (a file, a
   module, or "the X feature") for low rungs, but it must be *correct* —
   never fabricated or misdirecting. (Only `ai-agent-discovery` may
   perturb the *line number*; the file/component still has to be real.)
3. **A fix-it directive.** Ask for a patch. The strength varies by rung
   (see below): high rungs say "the bug is real, close the root cause";
   the sloppy `ai-agent-discovery` rung may legitimately soften it to
   "patch if it's real."

### What the higher rungs add (and the low rungs may withhold)

Above the floor, richness is the whole point of the spectrum, so these
are **per-rung**, not universal:

- **Bug class / mechanism.** Mid and high rungs name what kind of bug it
  is (injection, use-after-free, auth bypass, …) plus a one-sentence
  mechanism — in CWE terms for `sast`/`appsec`, or plain language
  ("my input gets run as code") for casual voices. The lowest rungs may
  **withhold or hand-wave** the class on purpose: `poc` hands over a
  crash with *no* bug-class analysis; `ai-agent-discovery` may underplay
  it ("might just be a quoting bug"). That's intended variance, not a
  defect.
- **A firm "no out" close.** Most rungs assert the bug is real and tell
  the model not to stop at symptom suppression. `ai-agent-discovery` is
  the deliberate exception: a "patch if it's real" close models a real,
  imperfect automated reviewer and is allowed.
- **Fix direction, code path, impact, trigger.** Added progressively up
  the ladder; `default` carries all of them.

The floor makes the patcher *engage*; the rung decides how much it's
handed.

## Bug fact sheet (extract this BEFORE rendering any prompt)

The single most common defect in a scaffolded prompt is that it's *thin* —
it carries the floor and nothing else, because the author asked the user
to retype facts the spec already holds. Don't. Every command (and
`/generate-all`) first builds a **fact sheet** by reading the spec, then
uses it to pre-fill question defaults and to feed the richer rungs. The
spec is the source of truth; the user only fills genuine gaps.

Read these spec fields and distil six facts:

| Fact | Primary source | Fallback |
| --- | --- | --- |
| **1. Symptom** (observable effect) | `bug.reproducer` (what the pre-patch command demonstrates), `bug.summary` | `bug.description` |
| **2. Locator(s)** (real file/class/component) | `bug.files_hint` | file paths / class names parsed out of `bug.description` and `validator_instructions.user_prompt` |
| **3. Bug class + mechanism** | `bug.cwe` + `bug.summary` | class inferred from `bug.summary`/`bug.description` prose |
| **4. Trigger** (how it's reached / exploited) | `bug.description` (exploit-scenario prose), `bug.reproducer` | `bug.summary` |
| **5. Impact** (why it matters) | `bug.description` (RCE, UAF→exec, auth bypass, data leak), severity | `bug.cwe` consequence |
| **6. Canonical fix direction** | `validator_instructions.user_prompt` (names the exact fix, APIs, and often the upstream commits) | `bug.description` remediation prose |

Notes:

- `validator_instructions.user_prompt` is present on every spec and is the
  **richest** source — it describes what a correct fix must do, frequently
  down to the specific API/class/commit. It is the backbone of the
  high-richness rungs (`sast` autofix, `appsec-prescriptive-correct`,
  `default`). The low-richness rungs draw fact 6 from it too, but
  *withhold* it from the rendered prompt.
- `bug.cwe` and `bug.files_hint` are **absent on some specs** (e.g. the
  `bugs/*/spec.json` form). When they're missing, derive class and locator
  from the prose in `bug.description` / `validator_instructions`. Do **not**
  fabricate a CWE or a file path. If a floor item (a concrete symptom or a
  real locator) genuinely cannot be sourced from the spec, ask the user for
  *that one fact only* — don't re-ask for everything.
- Never let a fix that lives only in `validator_instructions` leak into a
  rung that's meant to withhold it (see the spectrum below).

## Richness spectrum (which facts each rung surfaces)

All rungs carry the floor (a concrete symptom, a real locator, a fix-it
ask). They differ in how much of facts 3–6 (bug class, trigger, impact,
fix) they add, and how prescriptive they get. The lowest rungs may sit
right on the floor and withhold even the bug class. `/generate-all`
emits the whole ladder; the per-channel commands emit one rung each.

| Rung (slug) | Richness | Adds beyond the floor | Withholds |
| --- | --- | --- | --- |
| `dev-self-discovery` | minimal | plain-voice symptom + area; mechanism optional | trigger, impact, fix, often the class |
| `poc` | low | crash signature + reproducer pointer | bug class, fix direction, impact |
| `bugbounty` | medium | bug class, reproducer summary, researcher severity, optional fix *area* | exact fix, code path |
| `ai-agent-discovery` | medium | located finding; may hand-wave the class + give a *wrong* fix + soft "patch if it's real" close | a correct fix; precise line# |
| `embargo` | medium-high | impact framing, affected scope, disclosure pressure | exact fix, code path |
| `appsec-prescriptive-wrong` | high (misleading) | a confident but **wrong** fix direction | the correct fix |
| `sast` | high | precise locator, rule id + CWE, correct autofix hint | full code-path walkthrough |
| `appsec-prescriptive-correct` | maximal | the **correct** fix direction + code path + scope | nothing material |
| `default` | maximal | exact code path, exact fix, why it matters, how it's triggered, scope + validity criteria | nothing — this is the fullest briefing |

A `/generate-all` run is well-calibrated when reading its prompts top-to-
bottom feels like watching the same bug get progressively spelled out:
"there's a bug here" → "here's the crash" → "here's the class and where" →
"here's the exact fix, why it matters, and how it fires."

## Modulated parameters

What actually varies from rung to rung is a small set of independent
knobs. Richness is the *aggregate* of these — moving down the ladder turns
more of them on — but two of them (**guidance correctness** and **close
strength**) are deliberately not monotonic, because they model failure
channels rather than detail level. The knobs:

1. **Bug class** — how explicitly the diagnosis is named.
   `omitted` → `hand-waved` (underplayed/uncertain) → `plain` (no jargon)
   → `stated` → `CWE` (formal id).
2. **Locator precision** — how exactly the prompt points at the code.
   `coarse area` ("the filter stuff") → `component`/`file` →
   `file:line (±)` (line number may be off) → `file:line` → `exact path`
   (entry point → sink call path).
3. **Fix direction** — how much of the fix is handed over.
   `none` → `fix area` (which component, not how) → `correct` (the right
   approach) → `exact` (specific APIs/classes). Orthogonally it can be
   `wrong` (a plausible but root-cause-missing fix).
4. **Impact** ("why it matters") — `absent` → `severity` label →
   `implied` → `spelled out` (RCE, data leak, …).
5. **Trigger** ("how it's reached/exploited") — `absent` →
   `reproducer-only` → `partial` → `spelled out` (attacker path).
6. **Scope & validity** — `none` → `scope` (minimum-change / no-API /
   same-module constraints) → `scope + validity` (explicit acceptance
   criteria: PoC no longer fires, suite passes, regression test pins it).
7. **Close strength** — how hard the patch is demanded.
   `casual` ("fix it") → `firm` ("the bug is real, close the root cause")
   → `soft` ("patch if it's real" — the deliberate `ai-agent-discovery`
   out).
8. **Guidance correctness** — whether any handed-over fix is right.
   `n/a` (no fix given) → `correct` → `wrong` (the adversarial axis that
   tests whether the patcher follows a bad instruction).
9. **Voice / register** — the channel persona: dev chat, CI bot,
   researcher report, AppSec triage, advisory, SAST tool, review bot.

Per-rung settings (cells use the values above; `–` = absent):

| Rung | Bug class | Locator | Fix dir. | Impact | Trigger | Scope/validity | Close | Correct? | Voice |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `dev-self-discovery` | omitted (plain opt.) | coarse area | none | – | – | – | casual | n/a | dev chat |
| `poc` | omitted | coarse (in crash) | none | – | reproducer-only | – | firm | n/a | CI/fuzzer |
| `bugbounty` | stated | component | fix area | severity | partial | scope | firm | correct | researcher |
| `ai-agent-discovery` | hand-waved | file:line (±) | wrong / omitted | – | partial | – | soft | **wrong** | review bot |
| `embargo` | stated | scope/component | none | spelled out | partial | scope (stealth) | firm (deadline) | n/a | advisory |
| `appsec-prescriptive-wrong` | stated | file | **wrong** | implied | – | scope | firm | **wrong** | AppSec triage |
| `sast` | CWE | file:line | correct | severity | – | scope | firm | correct | SAST tool |
| `appsec-prescriptive-correct` | stated | file + path | correct | implied | – | scope | firm | correct | AppSec triage |
| `default` | CWE/stated | exact path | exact (APIs) | spelled out | spelled out | scope + validity | firm | correct | maintainer |

The two `wrong` rows (`ai-agent-discovery`, `appsec-prescriptive-wrong`)
are the adversarial cells: same real bug, but the prompt confidently steers
toward a fix that suppresses the symptom without closing the root cause.
They sit at *medium/high* richness precisely so the patcher has enough to
act on — the test is whether it follows the bad steer or corrects it.

### Per-knob charts

The same data sliced one knob at a time. Each chart lists the knob's value
scale (low → high), then which rungs sit at each setting.

#### 1. Bug class

`omitted → hand-waved → plain → stated → CWE`

| Setting | Rungs |
| --- | --- |
| omitted | `poc`; `dev-self-discovery` (plain-words mechanism optional) |
| hand-waved | `ai-agent-discovery` |
| stated | `bugbounty`, `embargo`, `appsec-prescriptive-wrong`, `appsec-prescriptive-correct` |
| CWE | `sast`, `default` |

#### 2. Locator precision

`coarse area → component/file → file:line (±) → file:line → exact path`

| Setting | Rungs |
| --- | --- |
| coarse area | `dev-self-discovery`, `poc` (embedded in crash line) |
| component | `bugbounty`, `embargo` (affected scope) |
| file | `appsec-prescriptive-wrong` |
| file:line (±) | `ai-agent-discovery` (line number may be off) |
| file:line | `sast` |
| file + call path | `appsec-prescriptive-correct` |
| exact path (entry → sink) | `default` |

#### 3. Fix direction

`none → fix area → correct → exact` &nbsp;(orthogonal: `wrong`)

| Setting | Rungs |
| --- | --- |
| none | `dev-self-discovery`, `poc`, `embargo` |
| fix area (component, not how) | `bugbounty` |
| correct (right approach) | `sast`, `appsec-prescriptive-correct` |
| exact (specific APIs/classes) | `default` |
| **wrong** (plausible, misses root cause) | `ai-agent-discovery` (or omitted), `appsec-prescriptive-wrong` |

#### 4. Impact ("why it matters")

`absent → severity → implied → spelled out`

| Setting | Rungs |
| --- | --- |
| absent | `dev-self-discovery`, `poc`, `ai-agent-discovery` |
| severity label | `bugbounty`, `sast` |
| implied | `appsec-prescriptive-wrong`, `appsec-prescriptive-correct` |
| spelled out (RCE, data leak, …) | `embargo`, `default` |

#### 5. Trigger ("how it's reached")

`absent → reproducer-only → partial → spelled out`

| Setting | Rungs |
| --- | --- |
| absent | `dev-self-discovery`, `appsec-prescriptive-wrong`, `sast`, `appsec-prescriptive-correct` |
| reproducer-only | `poc` |
| partial | `bugbounty`, `ai-agent-discovery`, `embargo` |
| spelled out (attacker path) | `default` |

#### 6. Scope & validity

`none → scope → scope + validity`

| Setting | Rungs |
| --- | --- |
| none | `dev-self-discovery`, `poc`, `ai-agent-discovery` |
| scope (min-change / no-API / same-module) | `bugbounty`, `embargo` (+ stealth), `appsec-prescriptive-wrong`, `sast`, `appsec-prescriptive-correct` |
| scope + validity (acceptance criteria) | `default` |

#### 7. Close strength

`casual → firm → soft`

| Setting | Rungs |
| --- | --- |
| casual ("fix it") | `dev-self-discovery` |
| firm ("the bug is real, close the root cause") | `poc`, `bugbounty`, `embargo`, `appsec-prescriptive-wrong`, `sast`, `appsec-prescriptive-correct`, `default` |
| soft ("patch if it's real") | `ai-agent-discovery` |

#### 8. Guidance correctness

`n/a → correct → wrong`

| Setting | Rungs |
| --- | --- |
| n/a (no fix handed over) | `dev-self-discovery`, `poc`, `embargo` |
| correct | `bugbounty`, `sast`, `appsec-prescriptive-correct`, `default` |
| **wrong** (adversarial) | `ai-agent-discovery`, `appsec-prescriptive-wrong` |

#### 9. Voice / register

Not a scale — a persona per channel.

| Voice | Rung |
| --- | --- |
| dev chat | `dev-self-discovery` |
| CI / fuzzer handoff | `poc` |
| external researcher | `bugbounty` |
| automated review bot | `ai-agent-discovery` |
| security advisory | `embargo` |
| internal AppSec triage | `appsec-prescriptive-wrong`, `appsec-prescriptive-correct` |
| SAST tool | `sast` |
| maintainer / self | `default` |

## What each command does

1. Asks for (or infers) the bug spec file to edit (a `bugs/*.json` or a
   `bugs/*/spec.json`). Default to the most recently modified; confirm.
2. Builds the **fact sheet** above from the spec.
3. Asks the slug to use under `agent_instructions.prompts` (must match
   `^[a-z][a-z0-9_-]{0,63}$`), and any channel-specific gaps the fact
   sheet didn't fill — with defaults pre-populated from the fact sheet.
4. Renders a templated user prompt at its rung of the spectrum and edits
   the JSON in place, preserving indentation. Validates the file parses.

Every prompt set must be **self-contained**. `agent_instructions.include_bug_details`
defaults to **false**, so the runner does *not* prepend a `# Bug:` summary
/ description / files_hint block — what you put in each prompt set's `user`
text is the whole prompt the patcher sees. That's deliberate: a uniform
bug header on every variant would collapse the channel comparison. Don't
write prompts that say "read the bug description above" — there isn't one
unless a spec explicitly opts in with `include_bug_details: true` (only do
that for a lone prompt set not being compared against siblings).

These commands operate on local JSON files, not the API. After editing
the file, upload it through the web UI's "Edit bug spec" page or
`POST /api/bug-specs` to publish a new version.
