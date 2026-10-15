---
name: meta-loss-function-development
description: |
  Turn a high-level goal ("build X in Y using loss-function
  development") into a complete, paste-able /goal prompt plus
  the harness scaffold it drives. The output is a single
  text block ready to paste into a fresh session's /goal
  command.

  Load this skill whenever the user says any of: "loss function
  development", "LFD", "/goal", "use the loop pattern on X",
  "set up a loss-driven loop for Y", "I want to build Z with
  the harness-engineering pattern", or describes a project they
  want to drive with a loss-function loop. Also load it when
  the user pastes a /goal prompt and asks for review, or says
  "this loop isn't converging" and the failure is in the goal
  spec rather than in the harness.

  This skill is the *meta-loop*: it produces the artifacts
  that the loss-function-design skill describes. It does not
  run the loop itself. The output is consumed by a new
  session that runs the loop.
version: 1.0.0
author: open source
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meta, loss-function-development, lfd, goal, harness, agentic]
    related_skills: [loss-function-design, harness-engineering, cline-orchestration]
---

# Meta Loss-Function Development

The loss-function loop has three layers:

1. **Inner loop** — the coding agent (Cline, Codex, Aider, …)
   running the spec-driven development cycle. Spec-driven
   development: "build this, make the tests pass."
2. **Outer loop** — the loss-function driver. The driver
   invents hypotheses, runs the inner loop, scores the result
   against the loss, decides whether to refine or accept.
3. **Meta loop** — *this* skill. Given a high-level goal,
   produce the spec the outer loop drives, plus the harness
   the inner loop runs against.

This skill is the meta loop. It is invoked once per project,
produces a paste-able `/goal` prompt, and the user pastes that
prompt into a fresh session to actually run the outer loop.

## What the output is

When you load this skill and the user says "build a clone of
the slack desktop app from slack.com in golang using loss
function development", the output is a **single text block**
the user can copy-paste into a fresh session's `/goal` command.
The block contains:

- The 4-piece loss spec (target, constraints, instruments,
  forced entropy)
- The design task list (5-10 tasks the loop will use as
  training signal)
- The held-out task list (5-10 tasks the loop will be graded
  on; the user pastes these into a private location the loop
  cannot read)
- The harness scaffold: `verifiers/`, `instruments/`,
  `AGENTS.md`, `GOAL.md`
- The runtime instructions: which agent, which model, which
  flags, which budget
- The stop conditions

The block is the spec. The user pastes it; the next session
runs it.

## How to use this skill (for the user)

1. Describe the goal in one sentence. Include: the artifact
   ("build X"), the constraints ("in Y", "for Z"), and any
   quality bar ("looks like reference", "passes acceptance
   tests"). **Also tell the skill the absolute path of the
   project root** (the directory where the harness should
   live). If you don't, the skill will ask, because the
   generated prompt must embed the path so the fresh session
   can find the project without guessing.
2. The skill will emit a paste-able block whose first line
   after the title is `PROJECT_DIR: <absolute-path>`.
3. Open a fresh session. Paste the block as the first message.
   The session will scaffold the project, build the harness,
   install the per-task graders, and run the outer loop.

The fresh session does *not* have the meta-skill loaded. It
has only the three inner skills (loss-function-design,
harness-engineering, cline-orchestration) and the goal prompt
itself. The goal prompt is the spec; the inner skills are the
vocabulary; the fresh session does the work.

## How orchestrators drive this skill (non-interactive)

The interactive flow above assumes the user cd'd to the project
root before opening the fresh session. Non-interactive
orchestrators (CI scripts, the LFD system verifier, etc.)
often run from a different working directory. The
`/goal` prompt has a project-root pinning protocol that
handles both cases:

- **Pinned (recommended — interactive or orchestrator).** The
  generated prompt embeds `PROJECT_DIR: <absolute-path>` as a
  header line. The fresh session's first action reads that
  line and uses it as the authoritative project root. This
  works regardless of the fresh session's cwd, regardless of
  env vars, and is copy-pasteable across machines. **Always
  prefer this.** Interactive meta-skill invocations should
  pin the path the user gave. Orchestrators that know the
  project path should pin it instead of (or in addition to)
  setting `LFD_PROJECT_DIR`.
- **Env-var (orchestrator fallback).** The orchestrator sets
  `LFD_PROJECT_DIR=/path/to/project` in the env when launching
  the fresh session; the discovery step's second preference
  picks it up. Use this when the orchestrator does not want
  the path baked into the prompt (e.g. the same prompt is
  shipped to multiple environments).
- **cwd / walk-up (last-resort fallback).** The discovery
  step's third / fourth preference: if cwd contains
  `GOAL.md` or `verifiers/`, use it; otherwise walk up
  ancestor directories. This handles the case where the
  user is running the fresh session from inside the
  project by accident.

If none of the checks find the root, the agent stops and
reports the failure. This is the right failure mode — silently
guessing the project root is the bug this design prevents.

Concrete patterns:

```bash
# Pinned (preferred) — orchestrator bakes the path into the
# generated /goal prompt; no env needed at run time.

# Env-var (fallback) — same prompt, runner sets the env:
LFD_PROJECT_DIR=/path/to/verifier-project \
  npx skills add antifragileer/loss-function-development-skills -y -g
# launch the fresh session with the env var set
```

When using the env-var pattern, the fresh session inherits
`LFD_PROJECT_DIR` and the goal prompt's discovery step picks
it up automatically. When using the pinned pattern, the path
travels with the prompt itself.

## How to write the goal prompt (for the skill itself)

A goal prompt has six parts:

1. **The 4-piece loss spec.** What the agent is descending
   toward (target), what it is forbidden from doing
   (constraints), how it observes its own progress
   (instruments), and how it forces entropy to escape local
   maxima (forced entropy).
2. **The candidate / verifier contract.** Where the agent
   writes its work, where the verifier reads, and what the
   JSON contract between them looks like.
3. **The design task list.** 5-10 tasks the agent will see
   during the loop, with deterministic graders. These are the
   *training signal* — they tell the loop whether the skill is
   improving, but they are not the final grade.
4. **The held-out task list.** 5-10 tasks the agent will NOT
   see during the loop. These are the *test set* — the
   final grade. The agent must not read them; the harness
   puts them behind a private directory the agent cannot
   access.
5. **The harness layout.** File tree of `verifiers/`,
   `instruments/`, `AGENTS.md`, `GOAL.md`, `skills/`, `logs/`.
6. **The runtime instructions.** Which agent (Cline, Codex,
   Aider), which model (**whatever the user has currently
   authenticated — never ask, never pin**), which budget
   (wall-clock, tokens), and which stop conditions.

Each part is filled in from the user's goal statement plus a
short round of clarifying questions (see "Discovering
information" below).

## Discovering information (the question phase)

The user often doesn't say everything needed to fill the six
parts. The skill should ask 1-3 clarifying questions, *in
priority order*, before emitting the block. Examples:

- "What absolute path should the harness live at? (The
  generated prompt bakes the path in so the fresh session
  finds the project without guessing.)" — the **project
  root**. If the user does not specify, ask. Do NOT
  default this — wrong-path prompts are unrecoverable.
- "What does 'done' look like for X? A reference output, a
  behavior spec, an acceptance test?" — the **target**.
- "What's the wall-clock budget? 1h? 6h? 24h?" — the
  **constraints**.
- "What agent and (implicitly) what model? Cline with its
  default provider? Codex with whatever OpenAI model the
  user has? Aider with whatever Anthropic key the user
  has? A Hermes session? — Note: do NOT ask the user to
  name a specific model. The model is whatever they have
  currently authenticated for whichever agent they pick.
  The /goal prompt should pin the agent but NOT the model
  and NOT the provider. The agent's own config (e.g. `cline
  auth`) is the source of truth." — the **runtime**.
- "What reference artifacts exist publicly that I should
  generate the held-out set from?" — the **held-out set
  source**.
- "What are the obvious reward hacks for X? Tests that can be
  deleted? Lints that can be suppressed? Token budgets that
  can be gamed?" — the **defense list**.

Aim for **at most 3 questions**. Beyond that, the user is
better served by a default than a Q&A. Use the user's "use
defaults" affordance from `loss-function-design`: pick
sensible defaults, state them in the prompt, the user can
change them.

When the user already specified everything, do not ask
redundant questions. Skip the discovery phase.

## Researching the goal (the synthesis phase)

For goals that involve an external reference ("clone of X",
"implement Y from the paper", "match the public API of Z"),
the skill should do **bounded research**:

- Pull the reference's public artifacts (homepage, API docs,
  sample inputs/outputs, public test cases).
- Identify what "looks like the reference" means in 5-10
  concrete test cases.
- For each test case, identify the deterministic grader
  (does the output match, does the function return the right
  shape, does the binary build, does the unit test pass).
- Identify the *cheap reference* the loop can score against.
  If the reference has a public API, that's the target. If
  it has a public test suite, that's the target. If it has
  public benchmarks, those.

Bounded = **at most 10 minutes of web/tool calls**. The skill
must not turn into a research project. The user is paying for
a /goal prompt, not a domain analysis.

For goals that are *internal* ("build our internal tool", "add
feature Y to our codebase"), the research phase is just
reading the project's existing files. Same time budget.

## Composing the prompt (the writing phase)

The skill emits the prompt as a single code-fenced text block.
The format is the one from the @elvissun article, adapted to
the user's specific goal. A canonical template is at
`templates/goal-prompt.md` in this skill. Examples of completed
prompts are at `examples/` (e.g., `examples/slack-clone-golang.md`).

The writing phase is mechanical once the discovery and
research are done. Fill the template. Do not improvise the
format.

**Mandatory template fill: the project-root header.** When
filling `templates/goal-prompt.md`, replace
`<ABSOLUTE-PATH-TO-PROJECT-ROOT>` with the absolute path the
user specified (or the `LFD_PROJECT_DIR` value, if the
orchestrator supplied one). The fresh session will read this
line and use it as the authoritative project root — see the
"Project-root pinning" subsection above. Replace
`<SHORT-SLUG>` with a filesystem-safe short name for the
project (e.g., `cline-go`, `slack-clone`, `pyforge-rust`).
This becomes the artifact's default name and skills-dir slug.

## What this skill is NOT

- **Not a loop driver.** It does not run the outer loop. It
  produces the spec; the user runs the loop in a fresh
  session.
- **Not a research project.** 10 minutes of bounded research
  is the cap.
- **Not a domain expert.** If the user says "build a slack
  clone", the skill does not become a slack engineer. It
  reads the public artifacts, identifies the testable
  behaviors, and produces a /goal prompt that drives an agent
  toward those behaviors.
- **Not a verifier implementer.** The /goal prompt includes
  placeholders for the harness; the fresh session fills them
  in based on the spec.

## Pitfalls when using this skill

- **Don't ask 5+ questions.** The user wants the /goal prompt
  now, not a Q&A. Ask the top 1-3, then emit with defaults
  for the rest.
- **Don't write the prompt before the research is done.** If
  the goal involves a public reference, the held-out tasks
  come from the reference's public outputs. Skip research,
  the held-out set is invented and the loop overfits to it.
- **Don't write a 10,000-word prompt.** The loop driver
  reads the prompt; long prompts dilute the signal. Aim for
  the same density as the canonical example:
  `examples/slack-clone-golang.md`.
- **Don't put machine-specific paths in the prompt body.** The
  prompt must work on any machine. Use `$PROJECT_DIR` and
  add a "Locate your project root" first-action step so the
  agent knows how to resolve `$PROJECT_DIR` to an actual
  path regardless of whether the orchestrator (or the user
  in an interactive session) has cd'd to the project
  directory. The canonical template at
  `templates/goal-prompt.md` and all three example prompts
  show the standard pattern.
  **EXCEPTION — the `PROJECT_DIR:` header line.** The
  absolute path in the header is the whole point: it is the
  one piece of machine-specific information the prompt MUST
  carry, because the fresh session's cwd is unknown and the
  env var is not guaranteed. Without the header, the
  discovery step has nothing to find and the prompt is
  unrecoverable. Never leave the placeholder
  `<ABSOLUTE-PATH-TO-PROJECT-ROOT>` unfilled. If the user
  refuses to supply a path, refuse to emit the prompt —
  ask again.
- **Don't hard-code the model.** The model is the user's
  choice. Pick a *capability tier* (e.g., "any current
  Cline-compatible model") and let `cline auth` decide.
  **Do not even name a specific model in the prompt.**
  The /goal prompt should reference "whatever provider
  the user has authenticated" — not "kimi-for-coding"
  or "GPT-5" or "Sonnet 4". The same prompt must work
  if the user switches from Cline+openrouter to
  Cline+anthropic without the meta-skill being re-run.
  Hard-coding the model also voids the orchestrator's
  ability to ship one prompt to multiple users with
  different auth states. The verification rule: if the
  string in the prompt's `INNER_MODEL:` line, the
  wrapper script, or the constraints section names a
  specific model or provider, the verifier should fail
  the prompt.
- **Don't make the held-out set larger than the design set.**
  5/5 or 5/10 is fine. 50/50 dilutes the loop's attention
  budget.

## The 4-piece loss spec — quick reference

This is the same anatomy from `loss-function-design`. The
meta-skill fills each piece from the user's goal.

- **Target.** What the agent is descending toward. Must be
  large enough that enumeration doesn't pay, and must be
  **blind** to the agent during the run.
- **Constraints.** What the agent is allowed to do. Time,
  money, surface, methodology. For every constraint, ship a
  CLI command the agent can inspect.
- **Instruments.** The harness the agent runs against. A
  constraint without an instrument is a vibe.
- **Forced entropy.** Each loop continues from the *entire*
  previous run's context. The model is reading its own last
  hundred decisions. Force entropy to escape local maxima.

## The candidate / verifier contract — quick reference

```
verifier: <path to script or MCP tool>
inputs:
  candidate: <how the agent emits the candidate — file, dir, deploy url>
  evidence: <what the verifier reads — logs, screenshots, pprof, …>
outputs:
  score: float in [0.0, 1.0]
  details: { sub_loss: <name>, signal: <key>, … }
  artifacts: [ <paths to evidence files the agent can read> ]
exit_code:
  0: success (verifier ran, score is real)
  non-zero: verifier itself failed (DO NOT score 0; surface the failure)
determinism: deterministic | stochastic(seed) | llm_judge(model, prompt, temperature)
budget: <max wall-clock + max tokens>
```

## The skill's deliverables

When invoked, this skill produces:

1. **A single paste-able text block** — the /goal prompt.
2. **A short summary** above the block — what the goal
   prompt assumes, what it doesn't, what the user should
   change.
3. **A list of clarifying questions** if the goal is
   under-specified and the skill can't emit a good default.

The block is the artifact. The summary and questions are
context.

## Related skills (install separately if not present)

- `loss-function-design` — the 4-piece loss anatomy. This
  meta-skill is its upstream.
- `harness-engineering` — what the agent sees. The
  meta-skill's prompt is informed by this.
- `cline-orchestration` — the Cline runtime. Substitute
  your own if not using Cline.

## References in this skill

- `references/four-piece-anatomy.md` — the canonical 4-piece
  loss spec, with the @elvissun article's worked example.
- `references/research-budget.md` — the 10-minute research
  cap, with examples of what counts and what doesn't.
- `templates/goal-prompt.md` — the canonical /goal prompt
  template, the meta-skill fills this in.
- `examples/slack-clone-golang.md` — a worked example.
- `examples/cli-tool-rust.md` — another worked example.
- `examples/algorithm-from-paper.md` — another worked example.
