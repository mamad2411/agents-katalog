---
name: dev-environment-preflight
description: >-
  Check that a developer machine can run model-backed agent skills, and prove
  it by making one real model call and validating the reply against a contract.
  Use when setting up a new machine or CI runner for agentic work, when a skill
  fails with no output, when choosing between developer AI tools on context
  window and cost, or when "the model is configured" is an assumption nobody
  has tested.
license: Apache-2.0
allowed-tools: Read, Glob, Bash
compatibility: >-
  Requires python3 and network access to an OpenAI-compatible chat completions
  endpoint, configured through OPENAI_BASE_URL, OPENAI_API_KEY and MODEL. Works
  against a local server (Ollama, llama.cpp, vLLM) or a hosted free tier.
metadata:
  commons-lesson: A0.0
  commons-area: programme
---

# Can this machine run a model-backed skill, and did it?

Every skill in this commons is executed **by a model**. The script is the
harness: it assembles the procedure, calls the model, and checks the reply.
That means a working machine needs one thing a normal Python setup does not —
a reachable model endpoint — and the failure when it is missing looks nothing
like "you have not configured a model".

Three things have to be true before any skill's output means anything, and
none of them is visible in that output:

1. the **runtime is importable** — the skill library is on the path,
2. an **endpoint is configured** — `OPENAI_BASE_URL` and `MODEL` are set,
3. the endpoint **answers**, and answers in the shape the contract requires.

When any of those is false a skill does not print a wrong answer. It prints
nothing, or a traceback, and the reader concludes the repository is broken.
This procedure makes each condition explicit and demonstrates the failures
before the success, so the messages are recognised rather than debugged.

## When to use this

- Setting up a laptop, a container or a CI runner to run agentic skills.
- A skill printed nothing, or exited 2, and you do not know which layer failed.
- Deciding which developer AI tool to configure, on context window and real
  cost rather than on marketing.
- Before trusting any model-produced finding: this is the run that establishes
  *which* model produced it.

## Procedure

1. **Import the runtime.** Report the version and the path it resolved from.
   A missing import is a `PYTHONPATH` problem, not a model problem.
2. **Read the configuration.** `OPENAI_BASE_URL`, `MODEL`, and whether
   `OPENAI_API_KEY` is set — report the key's presence, never its value.
3. **Demonstrate the unconfigured failure.** Clear the endpoint in a child
   environment and show the exact refusal a reader will hit first.
4. **Call the model once**, with a task small enough to be cheap and specific
   enough that a wrong answer is obvious.
5. **Validate the reply against this skill's output contract.** Report the
   violations rather than raising: what the model said is the evidence.
6. **Name the model in the output.** A finding that does not say which model
   produced it cannot be reproduced or compared.

## Example

On a machine with Ollama serving `my-local-model`:

```
runtime       : cyber_commons_skill_runtime (skills/_runtime)
endpoint      : http://127.0.0.1:11434/v1
model         : my-local-model
api key set   : yes

[1] unconfigured  -> exit 2, "No model endpoint is configured"
[2] configured    -> 1 model call, 0 contract violations
ready: this machine can run any skill in the commons
```

## Failure modes

- **`ModuleNotFoundError: cyber_commons_skill_runtime`** — the runtime is not
  on the path. Run from the repository root, or set
  `PYTHONPATH=skills/_runtime`.
- **Exit 2, "No model endpoint is configured"** — expected, and the point of
  step 3. Set the three variables.
- **`Connection refused`** — the endpoint is set but nothing is listening.
  Start the server first; `ollama serve` does not start automatically on every
  platform.
- **HTTP 404 on `/chat/completions`** — the base URL is missing its `/v1`
  suffix. This is the single most common setup error.
- **HTTP 401** — a hosted endpoint with no key or a stale one. Local servers
  accept any non-empty value.
- **The model answers, but not with JSON** — small models do this. The runtime
  extracts the first JSON object from fenced or bare text; if there is none, it
  says so and prints what was returned instead of guessing.

## Output contract

```json
{
  "runtime_importable": true,
  "endpoint_configured": true,
  "endpoint": "str|null",
  "model": "str|null",
  "api_key_present": true,
  "unconfigured_exit_code": 2,
  "model_calls": 1,
  "contract_violations": 0,
  "ready": true
}
```

`endpoint` and `model` are strings when the machine reaches a model through an
HTTP endpoint (the example above: `http://127.0.0.1:11434/v1` and
`my-local-model`) and **null** when it does not. A signed-in Claude Code
CLI has no endpoint at all, so `null` is the true answer there and inventing a
URL to fill the field would be worse. Never write a value the input did not
give you.

`ready` is true only when all three conditions held **and** the model answered
in contract. Anything else is false with the failing condition named — a
preflight that reports success on an untested endpoint is worse than no
preflight.
