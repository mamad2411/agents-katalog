---
name: wiki-ask
description: Consult a federated llm-wiki agent's wiki via the ask primitive (clone-and-invoke). Use when another project's durable memory would answer the question at hand.
---

You are running the **ask** primitive: synchronous cross-agent consultation via `$SKILL_DIRECTORY/scripts/ask.sh`. It fetches the federation index, clones the target agent's wiki into a local cache, and invokes an LLM there with the wiki Query procedure, so you consult another project's llm-wiki without leaving this session.

**Core rule: you are the picker.** Only ever call `ask.sh` in **direct mode** (`ask.sh <agent-id> "<question>"`), which needs no TTY. Never rely on `ask.sh`'s interactive stdin picker and never pipe a selection into it, orchestrate discovery yourself in the conversation.

The user's input is: `$ARGUMENTS`

## Parse the input

Decide direct vs discovery from the first token:

- **Direct mode** if the first token names an agent: an `@<token>`, an `<owner>/<repo>` slug, or a bareword that resolves to a known agent id (exact id, `owner_repo`, or repo basename, the same resolution `ask.sh` uses). Strip a leading `@`. The remainder (quotes stripped) is the question. A quoted remainder is a strong signal the first token is the agent.
- **Discovery mode** otherwise: the whole input is the question and no agent is named.

If a bareword first token is ambiguous and the rest is not quoted, prefer discovery and let the user confirm.

## Direct mode

```bash
bash "$SKILL_DIRECTORY/scripts/ask.sh" <agent-id> "<question>"
```

Return the agent's answer, attributed to the agent id.

## Discovery mode

1. Render the candidate list for its table only (ignore the harmless `No selection. Nothing asked.` tail, you are not using the picker):
   ```bash
   bash "$SKILL_DIRECTORY/scripts/ask.sh" "<question>"
   ```
   Keep `ask.sh` the single source of truth for the federation index URL and id-resolution, do not fetch the index yourself.
2. Present the numbered candidates and ask which to consult (one, several, or all). Suggest the most relevant if the choice is obvious, but let the user decide.
3. For **each** chosen agent, call **direct mode** once. Return each answer, clearly attributed to its agent.

## Notes

- Requires `git`, `jq`, `curl`, and an LLM CLI (`claude` by default; override with the `LLM_CLI` env var).
- `ask.sh` invokes `claude -p`, billed against `ANTHROPIC_API_KEY`. If that key is over its quota, prefix with `env -u ANTHROPIC_API_KEY` to fall back to the claude.ai login.
- This is `ask`-only; the async `message` / `post` modes are not part of it.
