---
name: ai-integration-guardrails
description: Puts an LLM into a product safely - bounded role, schema-validated output, prompt-injection defense, retrieval, cost, evals, human decision points. Use when a model enters a product path. Triggers - add an LLM, AI feature, prompt injection, should the model decide, hallucination, RAG, LLM cost, structured output.
---

# AI Integration Guardrails

A model is a **non-deterministic, occasionally confident, externally-controlled
function**. Every property engineers rely on — same input same output, errors
that look like errors, output that cannot contain an instruction — is absent.
Code that treats a model call like a library call fails in ways that are hard
to detect, because wrong output looks exactly like right output.

## Decide the role first

| Role | Risk | Requirement |
|---|---|---|
| **Suggest** — proposes, human accepts | Low | Make rejecting as easy as accepting |
| **Draft** — produces content a human edits and sends | Low–medium | The human must be able to see the source material |
| **Classify with confidence** — routes into buckets | Medium | Thresholds; a low-confidence path to a human |
| **Extract** — pulls structure from text | Medium | Schema validation + a review path for low confidence |
| **Decide** — acts without review | High | Only with deterministic bounds on the action space, full audit, and an undo |
| **Act** — takes real-world actions via tools | Highest | Allow-listed tools, per-action limits, confirmation on anything irreversible |

Default to the lowest role that solves the problem. Most "AI decides" designs
work as "AI proposes, rule disposes" — with better accuracy, because the
deterministic rule handles the cases it knows and the model handles the rest.

**In a control path, the model must not be the final decision maker.** Score,
rank, draft, summarize — then a deterministic rule or a person decides.

## Output is untrusted data

Model output may contain anything, including text engineered by a third party
who controls part of the input.

- **Always validate against a schema** before use. Malformed output after one
  retry goes to a failure path — never a best-effort parse of prose.
- Never pass output directly into SQL, a shell, a file path, a URL, an
  `eval`, or a template without the same escaping you would apply to user input.
- Never let output determine an authorization decision or a recipient address.
- Constrain the space where the API supports it (JSON schema, function calling,
  grammar). Cheaper and more reliable than instructing and hoping.

## Prompt injection

Any text from outside — a document, a web page, a user field, a tool's response
— can contain instructions for the model. There is **no reliable defense at the
prompt level**; the delimiters help and do not solve it.

Design so a successful injection is survivable:

1. **Separate data from instruction** structurally, and state that content
   inside the data block is never an instruction.
2. **Bound the action space.** The model can only invoke allow-listed tools with
   validated arguments. If it cannot delete, injection cannot cause deletion.
3. **Authorize the user, never the model.** Every tool call runs with the
   requesting user's permissions, checked independently.
4. **Confirm irreversible actions** with a human, showing exactly what will
   happen.
5. **Treat retrieved content as hostile** — RAG with untrusted sources is the
   highest-risk pattern in common use.

## Retrieval (RAG)

Retrieval decides what the model may say; many RAG failures are retrieval
failures that look like model failures.

- **Authorize at retrieval time.** Filter by the requesting user's tenant and
  permissions inside the query, not after ranking. A passage the user may not
  read must never reach the prompt; filtering the answer afterwards is too late.
- **Send fewer, better passages.** Rerank or filter candidates before the call;
  top-k by raw similarity carries noise that the model will cite.
- **Make "not enough context" an answer.** When nothing relevant is retrieved,
  return that — with what was searched — instead of letting the model answer
  from its own memory.
- **Cite only what was retrieved,** and check mechanically that each cited
  source is among the passages sent.
- **Evaluate retrieval separately** from generation — context recall and
  precision, faithfulness, abstention (`references/llm-eval-harness.md`).
- **Retrieved text is untrusted** (prompt injection above), including your own
  documents once users can write to them.

## Cost, latency, availability

- Hard caps per request, per user, per day. Exceeding a cap fails loudly; it
  does not silently continue.
- Timeouts and a fallback path. A model provider is an external dependency with
  worse availability than your database — `distributed-systems-and-resilience`
  applies fully.
- Cache by normalized input where semantics allow.
- **Deterministic first.** Where rules, parsers or regular expressions handle
  most inputs, run them first and send only the residue to the model, with a
  confidence check deciding which is which.
- **Smallest model that passes the eval,** escalating to a larger one on low
  confidence or failed validation — decided by eval results, not by habit.
- **Keep the prompt prefix stable** — instructions, tool definitions and
  examples first, the changing input last — so the provider's prompt caching
  can reuse it. Confirm the hit rate in the provider's usage counters; cached
  context still needs the same authorization as uncached.
- **Retry only what can succeed on retry**: timeouts, rate limits, server
  errors — with backoff and a ceiling. A validation or authentication error
  retried is the same error, paid for again.
- Non-interactive bulk work goes through the provider's batch interface where
  one exists, not a loop of interactive calls.
- Never put a model call in a hot path that must be fast unless you have
  measured its tail latency and accepted it.
- Degrade gracefully: the feature disappears or falls back to a rule; the
  product does not break.

## Reproducibility

Log for every call: prompt template **version**, model and version, parameters,
input hash, output, token counts, latency, and the correlation id. Without this
you cannot explain a past decision or reproduce a complaint.

Prompts are code: versioned files in the repository, reviewed, never edited in
a console. A prompt change is a behavior change and needs the same gates.

## Evaluation

"It looked good in testing" is not evidence. Build an eval set before shipping:

- 50–200 real examples with expected outputs, including known-hard cases
- Failure-mode tests: empty input, adversarial input, very long input,
  wrong-language input, injection attempts
- Run the eval in CI on every prompt or model change; block regressions
- Measure the metric that matches the cost asymmetry — for most products, a
  confident wrong answer costs far more than an abstention, so precision at the
  auto-accept threshold matters more than overall accuracy
- Track acceptance rate in production: how often does the human accept the
  draft unchanged? Falling acceptance is the earliest signal of drift

Dataset shape, graders, judge calibration and the CI regression gate:
`references/llm-eval-harness.md`.

## Being honest with users

Label model-generated content. Show sources for claims. Make correction easy
and capture corrections as future eval data. Never present a generated number
or citation as verified fact — fabricated specifics are the characteristic
failure, and they are most convincing exactly where they matter most.

## Exit checklist

- [ ] Role chosen deliberately; the model is not the final decider in a control path
- [ ] Output schema-validated; failure path defined
- [ ] Output never reaches an interpreter, query, or path unescaped
- [ ] Tool access allow-listed; user's permissions enforced per call
- [ ] Irreversible actions require human confirmation
- [ ] Cost caps, timeout and fallback in place; retries limited to transient
      errors; deterministic handling and the smallest passing model used first
- [ ] Retrieval filters by the user's permissions in the query; insufficient
      context returns an abstention; citations checked against the passages
- [ ] Retrieval metrics gated separately from answer quality
- [ ] Prompts versioned in the repository; calls logged with versions
- [ ] Eval set exists and runs in CI, including injection and edge cases
- [ ] Generated content is labeled and correctable
