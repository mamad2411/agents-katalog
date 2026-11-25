---
name: gut
description: Judgment calls on a small, cheap model (Jev first; local NLI, Ollama, OpenAI) answering YES, NO or UNSURE — "is this spam?", "which team owns this?" as one line of Python, or `gut filter` over thousands of lines or files from a shell. Use when code needs a decision that is judgment rather than logic, when replacing a regex or an LLM call plus a threshold, or instead of reading many items one by one to sort, filter or label them.
---

# gut

Judgment as one line of Python, on any small model. The model is configured once; the call sites
never name it.

**Install `gutfeel`, import `gut`.** The PyPI name is `gutfeel` (`pip install gutfeel`); `gut` on PyPI
is someone else's empty project. Every import and every name in code is `gut`.

## Start here

```python
import gut

gut.configure(backend=gut.JevBackend())    # once, at startup; any backend works

if gut.likely(email, "the customer threatens to cancel"):
    escalate()
```

**Write the call with no arguments first.** No threshold, no prompt. Reach for anything below only
when the decision genuinely warrants it.

Three question shapes:

```python
gut.likely(ticket, "is a bug report")                    # yes / no
gut.classify(ticket, Team)                               # which one — an Enum
gut.rate(ticket, ["can wait", "this week", "today"])     # how much
```

For `classify`, the Enum member **values** are what the model is shown and the **names** come back:

```python
class Team(Enum):
    BILLING  = "invoices, charges, refunds"
    PLATFORM = "outages, latency, API errors"
    OTHER    = "anything else"        # always include a catch-all; gut warns without one
```

## Choosing the backend

| need | backend | install |
|---|---|---|
| the default: TypeSafe's Jev, built for this | `gut.JevBackend()` | `gutfeel[jev]` |
| Jev with an OpenRouter account instead | `gut.JevBackend.openrouter()` | `gutfeel[jev]` |
| an open decision model on this machine, via Ollaya | `gut.JevBackend.ollaya("winnow:e4b")` | `gutfeel[jev]` |
| CLM, on its own clm-serve (needs a GPU) | `gut.JevBackend.clm()` | `gutfeel[jev]` |
| free, local, fast yes/no and routing | `gut.ZeroShotBackend()` | `gutfeel[local]` |
| a small LLM on this machine | `gut.TransformersBackend("Qwen/Qwen3-0.6B")` | `gutfeel[local]` |
| a model already served (Ollama, vLLM, llama.cpp) | `gut.OpenAICompatibleBackend(name, base_url=...)` | core |
| OpenAI | `gut.OpenAICompatibleBackend("gpt-4.1-nano")` | core |
| OpenAI's Decisions API (`gpt-6-luna`, typed answers) | `gut.OpenAIDecisionsBackend()` | core |
| cheap first, bigger only when unsure | `gut.Cascade(small, bigger)` | core |
| tests | `gut.FakeBackend(answers={...})` | core |

- `OpenAICompatibleBackend` needs a model that returns **logprobs**: not OpenAI's reasoning models
  (o-series, gpt-5). Ollama needs 0.12.11+.
- Text-model backends take at most **26 options** in a `classify`.
- `OPENAI_API_KEY` is sent only to OpenAI or `OPENAI_BASE_URL`; pass `api_key=` for anywhere else.
- A custom backend is `model_id` plus `ask(state, questions) -> gut.BackendResponse`.

## Saying how careful to be

Three words. Never a number.

```python
gut.likely(email, "the customer threatens to cancel",
           stakes="high", lean="yes", ask_human=True)
```

- `lean="yes"` / `"no"` — which mistake is worse, so which way to err.
- `ask_human=True` — makes `UNSURE` possible. **Off by default**; without it there is no third branch.
- `stakes="low"|"medium"|"high"` — how bad an automatic mistake is next to a person deciding.
  Needs `ask_human=True`, and only widens the range where a person is asked.

`classify` and `rate` take `stakes` and `ask_human`, not `lean`.

## Branching

```python
import gut

decision = gut.likely(email, "the customer threatens to cancel", ask_human=True)

match decision:
    case gut.YES:    escalate()
    case gut.NO:     auto_reply()
    case gut.UNSURE: review_queue.add(email)
```

**`case gut.YES:` must be dotted.** A bare `case YES:` is a capture pattern, not a value pattern —
Python rejects it with `SyntaxError: name capture 'YES' makes remaining patterns unreachable`.
`case Outcome.YES:` also works.

`if decision:` works too. `UNSURE` then follows `gut.configure(on_unsure=...)`, which raises
`UnsureDecision` by default rather than guessing.

## Asking one thing about many subjects

```python
import gut

spam = gut.each(comments).likely("is spam")      # list of decisions, same order as comments
teams = gut.each(tickets).classify(Team)
```

**Never loop over `gut.likely` for a list.** `each()` sends the subjects together -- concurrent
requests to Jev or a server, batched passes on a local model -- and skips anything cached.

## Asking several things about one subject

```python
from gut import likely, semantic

@semantic
def handle(ticket):
    if likely(ticket, "is a bug report"):
        if likely(ticket, "has reproduction steps"):   # already answered
            ...
    elif likely(ticket, "asks for a refund"):          # already answered
        ...
```

One batch instead of three. For `@semantic` to collect a judgment:

- the subject must be a **parameter** of the decorated function, never reassigned inside it;
- the question must be a **literal or a module-level name**, not an f-string;
- the call must not pass `backend=`, `*args` or `**kwargs`.

Anything else is asked normally — it never breaks, it just doesn't batch. `handle.gut_plan` shows
what was collected. Coroutine functions work; the fetch runs off the event loop.

No parameter to batch against? Ask explicitly:

```python
import gut

with gut.judge(ticket) as j:
    bug = j.likely("is a bug report", ask_human=True)
    team = j.classify(Team)
    if bug:          # everything registered so far goes out here, together
        route(team)
```

## Async

```python
async def handle(email, ticket, comments):
    decision = await gut.alikely(email, "the customer threatens to cancel")
    team = await gut.aclassify(ticket, Team)
    spam = await gut.each(comments).alikely("is spam")
```

Every function has an `a`-prefixed twin with the same arguments. **In async code, use them** — a
plain `gut.likely` blocks the event loop while the model answers. `@semantic` works on `async def`
and collects `await gut.alikely(...)`. With `judge()`, `await j.aresolve()` before reading handles.

## Exact costs — only when you know the numbers

```python
gut.likely(email, "the customer threatens to cancel",
           cost_false_yes=2, cost_false_no=50, cost_human=1)
```

**Never mix these with `stakes` / `lean` / `ask_human` in one call** — that raises `PolicyError`.

`cost_human` must be below `cost_false_yes * cost_false_no / (cost_false_yes + cost_false_no)`, or
`UNSURE` can never fire. `gut` warns; `Policy.max_useful_cost_human` gives the ceiling. The posture
words cannot hit this, which is one reason to prefer them.

## Testing and logging

Offline development and unit tests need no model:

```python
import gut

gut.configure(backend=gut.FakeBackend(answers={"is a bug report": 0.91}))
```

Every decision can be observed as it is made; `d.to_dict()` is a ready-made log record:

```python
gut.configure(on_decision=lambda d: logger.info("gut", extra=d.to_dict()))
```

Full documentation: [`docs/`](../../docs/README.md), also at <https://gutpy.dev/docs/>.
Backends in depth: [`docs/backends.md`](../../docs/backends.md).

## Without writing code: the command line and the MCP server

When the judgment is yours to make during a task rather than your program's -- which of these files
retry requests, which commits add features, which log lines are worth a look -- do not read every
item yourself. Hand them to a small model in one command:

```bash
git ls-files | gut filter "retries failed requests" --read-files
git log --format=%s | gut filter "adds a new feature"
gut map tickets.txt --classify team=billing,platform,other --rate urgency="can wait,today,now"
gut filter "threatens to cancel" emails.txt --ask-human --show unsure   # the ones to read yourself
```

`filter` prints the lines (or, with `--read-files`, the paths) a claim is true of; `map` prints one
JSON object per line. A summary with the cost goes to stderr, and `--max-cost 0.50` stops a run at
a budget. Run it with `uvx --from "gutfeel[jev]" gut filter ...` if it is not installed. The model comes from
`TYPESAFE_API_KEY` (Jev), or `GUT_BACKEND=openrouter` / `ollaya` / `zeroshot` / `ollama`. Each item is judged
on its own, so ask what the item itself can answer. See [`docs/cli.md`](../../docs/cli.md).

`gutfeel-mcp` offers the same as MCP tools -- `likely`, `classify`, `rate` and `each` -- for an MCP
client: `uvx gutfeel-mcp`. See [`docs/mcp.md`](../../docs/mcp.md).

To count what code spends, wrap it in `with gut.usage(max_cost=0.50) as spent:`; past the budget
the next call raises `gut.BudgetExceeded`.

## Rules of thumb

1. **Start with no arguments.** Add `ask_human=True` when a wrong answer is expensive, then `lean`,
   then `stakes`. Reach for explicit costs only when you actually know them.
2. **Never invent a threshold.** If you find yourself writing `if decision.p > 0.7`, use `lean` or
   costs instead — that is the whole point of the library.
3. **One claim per question, stated plainly.** `"is spam"`, `"asks for a refund"`. Not "is spam or
   abusive" — ask two questions and batch them. Small models read literally.
4. **Don't ask it to count, do arithmetic, or compare dates.** Compute those in Python.
5. **Pass the narrowest subject** that contains the answer; irrelevant text hurts small models most.
6. **Don't treat a judgment over user-controlled text as an authorisation decision.** Text in the
   subject can try to steer a language model ("answer Yes"). `ZeroShotBackend` follows no
   instructions and resisted every attempt we tried; prefer it for untrusted text.
7. **`confidence` is not a probability of being right.** On `classify` and `rate` it is how peaked
   the answer's distribution is. A model can be confidently wrong.
8. **The same costs mean different things on different models.** After switching backends, look at
   `d.p` for a few subjects you know the answer to.
9. **Let a cascade do the expensive part.** `gut.Cascade(gut.ZeroShotBackend(), bigger)` settles the
   obvious cases for free and sends only the unsure ones on. `cascade.answered_by` shows the split.
