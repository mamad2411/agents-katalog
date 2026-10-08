---
name: new-dcode-agent
description: Scaffold a new Deep Agents (LangChain) agent, a dcode CLI agent, or both, from one command. Use ONLY when the user explicitly runs /new-dcode-agent; never auto-trigger. It interviews the user (form, name, purpose, tools, model, safety), shows a spec, and on confirmation writes a self-contained agent into the user's current project (and/or a dcode CLI agent under ~/.deepagents). The agents it writes work with any OpenAI-compatible API via environment variables.
disable-model-invocation: true
---

# /new-dcode-agent

You are running the **/new-dcode-agent** skill. It scaffolds a working agent for the user. Everything it writes is SELF-CONTAINED, so it works from any folder, with no dependency on this skill's own location. Run no `git`; the user commits.

## The three forms (keep them straight)
- **SDK program**: a standalone Python agent (LangChain `create_deep_agent`) the user runs or deploys. Scaffolded into `./<name>/` in the user's current directory.
- **dcode agent**: a named identity for the dcode CLI (an `AGENTS.md`) the user chats with via `/agents`. Scaffolded into `~/.deepagents/<name>/AGENTS.md`.
- **both**: a dcode agent that acts as the cockpit for a deployed SDK program.

(This is NOT Claude Code's own subagents, which are a different feature.)

## Phase 1: Interview (use AskUserQuestion; batch related questions)
1. **Form**: SDK program / dcode agent / both.
2. **name** (kebab-case; reject names starting with `_`, names that match an existing target, or shell-unsafe names).
3. **purpose**: one or two sentences.
4. **(SDK or both)**: closest starting flavour (custom / project / work-jira / vps-ops / personal); the tools it needs (plain Python functions, plus any MCP servers); the **model** (a `provider:model` string for any LangChain provider, or the bundled env-driven connector below); **does it change anything?** (if yes, it gets an approval gate); how it will run (one-shot / long-running / scheduled / server).
5. **(dcode agent or both)**: what it knows and operates; which tools or MCP it leans on; its operating rules.

## Phase 2: Spec
Show the user exactly what you will create: the target paths, the tools, the model, and the safety posture. Wait for explicit confirmation. Do not write anything until they confirm.

## Phase 3: Scaffold

### SDK program (form = SDK or both): write `./<name>/` in the user's current directory
Create the folder `<name>/` with three files. It is self-contained: `agent.py` imports its connector from the sibling `model.py` (a same-directory import, so there is no path manipulation at all).

**`<name>/model.py`** (write this verbatim; the env-driven, provider-agnostic connector):

```python
"""Model connector for this agent. Provider-agnostic, configured from the environment.

Targets any OpenAI-compatible Chat Completions endpoint (OpenAI itself, or a compatible
gateway). Set these in the environment or a .env file next to this agent:
  LLM_API_KEY     (or OPENAI_API_KEY)   required
  LLM_BASE_URL    (or OPENAI_BASE_URL)  optional; omit for OpenAI's default endpoint
  LLM_MODEL                             optional; the model id (default below)
  USE_RESPONSES_API                     optional; set 1 only if your provider supports it
"""
from __future__ import annotations

import os
import pathlib

from langchain_openai import ChatOpenAI

DEFAULT_MODEL = "gpt-4o-mini"  # override via LLM_MODEL or the model= argument


def _load_env() -> None:
    """Minimal .env loader (no extra deps): this agent's folder, then the current
    directory, then ~/.deepagents/.env. Existing environment variables always win."""
    here = pathlib.Path(__file__).resolve().parent
    for path in (here / ".env", pathlib.Path.cwd() / ".env",
                 pathlib.Path.home() / ".deepagents" / ".env"):
        if not path.is_file():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def chat_model(model: str | None = None, *, temperature: float = 0.0, **kwargs) -> ChatOpenAI:
    """Return a ChatOpenAI wired to your OpenAI-compatible provider, from env."""
    _load_env()
    key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("No API key. Set LLM_API_KEY (or OPENAI_API_KEY) in the "
                           "environment or a .env file next to this agent.")
    base_url = os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or None
    use_responses = os.environ.get("USE_RESPONSES_API", "").strip().lower() in ("1", "true", "yes")
    return ChatOpenAI(base_url=base_url, api_key=key,
                      model=model or os.environ.get("LLM_MODEL") or DEFAULT_MODEL,
                      temperature=temperature, use_responses_api=use_responses, **kwargs)
```

**`<name>/agent.py`** (base, non-mutating flavour; fill in `system_prompt` and real tools):

```python
"""<name>: a Deep Agents SDK agent. Run:  python agent.py "your prompt" """
from __future__ import annotations

import sys

from model import chat_model  # sibling model.py, same-directory import
from deepagents import create_deep_agent


def example_tool(query: str) -> str:
    """Describe what this tool does (stub; replace)."""
    return f"[stub] {query}"


SYSTEM_PROMPT = """You are a helpful agent. TODO: describe the role, scope, and rules."""


def build_agent():
    return create_deep_agent(
        model=chat_model(),          # your provider/model from env; pass an id to override
        tools=[example_tool],
        system_prompt=SYSTEM_PROMPT,
    )


if __name__ == "__main__":
    agent = build_agent()
    prompt = " ".join(sys.argv[1:]) or "Hello"
    res = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    print(res["messages"][-1].content)
```

**If the agent can change things (a mutating tool)**, use this gated pattern instead. The approval gate needs BOTH `interrupt_on` AND a `checkpointer`, or it silently does nothing:

```python
"""<name>: an ops agent with an approval gate. Run:  python agent.py "status check" """
from __future__ import annotations

import sys

from model import chat_model
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver


def check_status() -> str:
    """Read-only status check (stub)."""
    return "ok"


def restart_service(service: str) -> str:
    """MUTATING, gated by approval."""
    return f"[would restart {service}]"


def build_agent():
    return create_deep_agent(
        model=chat_model(),
        tools=[check_status, restart_service],
        system_prompt="You are an ops engineer. Investigate read-only first; changes need approval.",
        interrupt_on={"restart_service": True},
        checkpointer=InMemorySaver(),   # required, or the gate no-ops
    )


if __name__ == "__main__":
    agent = build_agent()
    cfg = {"configurable": {"thread_id": "s1"}}
    res = agent.invoke({"messages": [{"role": "user", "content": " ".join(sys.argv[1:]) or "status check"}]}, config=cfg)
    print("[paused for approval]" if res.get("__interrupt__") else res["messages"][-1].content)
```

Verify a mutating agent actually pauses (a single `__interrupt__` check can false-negative):

```python
cfg = {"configurable": {"thread_id": "verify"}}
res = agent.invoke({"messages": [{"role": "user", "content": "<ask it to run the mutating tool>"}]}, config=cfg)
paused = bool(res.get("__interrupt__")) or bool(getattr(agent.get_state(cfg), "next", None))
print("approval gate fired:", paused)   # if False, fix interrupt_on + checkpointer before shipping
```

**Flavour adjustments** (start from the base or gated file above and change these):
- **custom**: the base file as-is. A blank starting point.
- **project**: a code/repo assistant. Add a read-only `run_tests()` tool (shell out to the project's test command) and a senior-engineer system prompt. Point `LLM_MODEL` at a coding-tuned model.
- **work-jira**: a Jira assistant. Either stub `search_issues(jql)`, or load MCP tools with `langchain-mcp-adapters` (`MultiServerMCPClient`) reading `JIRA_*` from the environment at runtime. Never hard-code credentials.
- **vps-ops**: a server-ops agent. Use the GATED pattern above (mutating tools behind `interrupt_on` + `InMemorySaver`).
- **personal**: a personal-assistant agent. Add simple tools (read a tasks file, append a note) and a concise system prompt.

**`<name>/README.md`** (write a short one): what the agent does, then:

```bash
pip install deepagents langchain-openai   # plus langchain-mcp-adapters if it uses MCP
export LLM_API_KEY=your-key                # or put it in a .env next to agent.py
# optional: export LLM_BASE_URL=...  export LLM_MODEL=...
python agent.py "your prompt"
```

### dcode agent (form = dcode agent or both): write `~/.deepagents/<name>/AGENTS.md`
- **Plain Markdown, NO YAML frontmatter**: a dcode agent's AGENTS.md is memory layered on dcode's base prompt, loaded fresh each run (not a program).
- Sections: **Role** (who it is, default posture); **Context / setup** (what it knows; commands it has; link extra files); **How to operate** (workflow; when to delegate to subagents); **Operating rules** (read-only default; approval before destructive actions; no secrets).
- Keep it **lean** (injected every run); push bulky reference into separate files and reference them.
- If the file already exists, preserve any `<!-- ... -->` managed block (dcode self-edits this file).
- Optional subagents at `~/.deepagents/<name>/agents/<sub>/AGENTS.md`. A subagent's frontmatter is only `name`, `description`, `model` (with a provider prefix, e.g. `openai:gpt-4o-mini`); the body is its system prompt; the folder and filename must be `agents/<sub>/AGENTS.md`.
- **If form = both**: the dcode agent's AGENTS.md references the SDK program (its path and how to run it), so it is the interactive cockpit for the deployed agent.

## Phase 4: Smoke-test
- SDK: `cd <name> && python agent.py "hello"` (import plus a minimal run; construct-only if there is no key). If it mutates, run the verification snippet and confirm the gate fires.
- dcode agent: confirm `dcode agents list` shows `<name>` (it auto-discovers the directory).

## Guardrails (never violate)
- No secrets in any file: keys come from the environment or a `.env` at runtime only.
- The scaffolded SDK agent is self-contained: `agent.py` plus a sibling `model.py`, same-directory import, no path manipulation.
- A mutating tool MUST have `interrupt_on` plus a `checkpointer`, or the approval gate silently does nothing.
- Provider-agnostic: never bake a provider, model id, or key into the generated code.
- Run no `git`; the user commits.
