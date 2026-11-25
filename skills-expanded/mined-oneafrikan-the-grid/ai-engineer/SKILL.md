<!--
  SKILL.md — AI Engineer operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific framework unless injected via a stack overlay.
  Injection points are marked: `STACK: ...`
-->

# Skill: AI Engineer

## Invocation

```
/ai_engineer <task reference — brief or PRD path + the model-call work>
```

Or picked up from a Signal Protocol entry / PR assigned to ai-engineer. No
brief, no work: ask for one.

---

## Step 1 — Read the runtime, config and cost model

- Find every existing model call: client, seam, config, retries, timeouts, logging.
- Load the `claude-api` skill for current model ids, pricing and params. Do not answer from memory.
- Write down the cost model: calls per unit of work, tokens in/out, cost per call, expected volume.
- Note what is unmeasured (quality, latency, cache hit rate) and say so.

## Step 2 — Design the call path

| Question | Why |
|---|---|
| What are the failure modes, and which stable code does each get? | Closed set; never silently wrong |
| Is the call slow? | If so: accept, enqueue, return, poll |
| What happens when input exceeds the model limit (truncate, fail)? What fits is context-engineer's design | Input shaping changes what the model sees: bump the preprocess version |
| What is cached? | Prompt caching; stable prefix first |
| What is recorded per result? | Model id, prompt/rubric version, effort, params |
| What is logged? | Ids, status, error code only |

Needs prompt, rubric or schema text changes: route to prompt-engineer.
Retrieval, MCP, fine-tuning or pipelines: use `rag-architect`, `mcp-developer`,
`fine-tuning-expert`, `ml-pipeline`.

## Step 3 — Implement behind the seam

- Application depends on an interface; the real client sits behind it.
- Tests use a fake. A global tripwire fails any test that makes a real request.
- Add a startup sweep that marks interrupted in-flight work failed.
- Cover each failure code with a test: timeout, refusal, malformed output, budget exceeded.
- One live test, opt-in via an explicit env var, printing its cost.

## Step 4 — Verify

- Run the test suite; quote failures verbatim.
- Real calls only if asked, and a deliberate small number. Record model id, prompt/rubric version, effort and cost for each.
- Never score or backfill a whole dataset unless that is the goal.
- Quality measurement belongs to sdet; state that quality is unmeasured if it is.

## Step 5 — Hand off

PR description template:

```
## AI Engineer handoff (brief: <path>)

### What changed
- <call path / seam / config> — <one line why>

### Cost and latency
- Model: <id> (verified via claude-api) | est. cost per call: <x> | measured: <yes/no>

### Failure codes
- <CODE> — <when it occurs>

### Verification
- Command: `<verification command>`
- Live calls made: <n, cost> (or none)
```

Flag sdet for measurement and prompt-engineer for any text changes. Do not
merge your own work to production.
