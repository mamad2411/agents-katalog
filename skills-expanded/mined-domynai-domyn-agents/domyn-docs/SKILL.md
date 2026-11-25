---
name: domyn-docs
description: >-
  The domyn documentation: the CLI (sessions, slash commands, approvals, config,
  install) and building agents (tools, MCP, YAML, teams, providers, hooks, events).
  Use for any question about how to use, configure or build with domyn.
external_files:
  - pages/
---

<!-- The index below lists the pages of docs/docs (`pages` links to it) with the title and
description of their front matter, in the order of docs/sidebars.js.
tests/skills/test_agent_docs.py checks it. -->

# The domyn documentation

These are the documentation pages of the domyn version you are running. To answer a
question about domyn:

1. Pick the page, or the two pages, that cover it from the index below.
2. Read them with `read_file`. Paths are relative to the directory of this file.
3. Answer from what the pages say, and name the page you used.

The pages are the reference: prefer them to what you remember about domyn, and do
not add options, imports or functions a page does not show. If no page covers the
question, say so instead of guessing. Links between pages are relative paths to
other files in this directory.


## Getting started

- `pages/index.md`: **Introduction**. Domyn Agents: a Python library for building agents and teams of agents, and a terminal assistant built with it
- `pages/getting-started/installation.md`: **Installation**. Install Domyn Agents and set up your API keys
- `pages/getting-started/quickstart-cli.md`: **Quickstart: CLI**. Install the domyn command and chat with an agent that works on the files of a directory
- `pages/getting-started/quickstart-library.md`: **Quickstart: library**. Build an agent with a tool in Python, run it, and read the events it produces

## Using the CLI

- `pages/cli/sessions.md`: **Sessions and commands**. Chat with an agent from the terminal with domyn run: starting a session, working in it, its commands, conversations and the context window
- `pages/cli/tools-and-approvals.md`: **Files, commands and approvals**. The file, command and browser tools of the CLI agent, the workspace they are confined to, and how you approve what the agent does
- `pages/cli/configuration.md`: **Configuring the CLI**. The CLI's configuration file, the settings you are most likely to change, and what lives in ~/.domyn

## Building agents

- `pages/guides/tools.md`: **Tools**. Give agents tools: Python functions, streaming tools and remote MCP servers
- `pages/guides/orchestration.md`: **Orchestration**. Compose agents that hand off work to each other, and control what each one sees and can call
- `pages/guides/remote-agents.md`: **Remote agents**. Add an agent that runs in another process to a team, and serve a Domyn agent or a LangGraph graph to other runners
- `pages/guides/llm-providers.md`: **LLM providers**. Connect an agent to the models of a Domyn platform space, OpenAI, Anthropic, vLLM, Cerebras, OpenRouter or any OpenAI-compatible endpoint, or to a model of your own
- `pages/guides/transcription.md`: **Transcription**. Turn speech into text, on your machine or through an OpenAI-compatible endpoint, for voice notes and recordings
- `pages/guides/planner-strategies.md`: **Planner strategies**. Choose how an agent reasons and calls tools, and configure its iteration limit, context and compaction
- `pages/guides/configuration.md`: **YAML configuration**. Describe an application in a YAML file: providers, strategies, tools, hooks and agents, and how to load and run it

## Shared features

- `pages/guides/skills.md`: **Skills**. Give an agent reusable instructions it reads only when a task needs them
- `pages/guides/standing-instructions.md`: **Standing instructions**. Shape every turn with SOUL.md and AGENTS.md: who the agent is for you, and what it is working on
- `pages/guides/approvals.md`: **Tool approvals**. Require a person's decision before a tool runs, remember it, and decide some calls automatically
- `pages/guides/decision-models.md`: **Decision models**. Let a small model answer typed questions with probabilities, where a heuristic or a prompt would otherwise decide
- `pages/guides/context-compaction.md`: **Context compaction**. Keep a long conversation within the model's context window by dropping old tool outputs and summarizing older turns
- `pages/guides/conversations-and-memory.md`: **Conversations and memory**. Keep conversations across turns and restarts, store data per conversation, and remember facts about a user across conversations

## Running agents in an application

- `pages/guides/events-and-streaming.md`: **Events and streaming**. Run an agent, follow its turn event by event, and stream its reply to a user
- `pages/guides/hooks.md`: **Hooks**. Run your own code around agents, tools and events: log, check, rewrite or stop a turn

## Reference

- `pages/reference/cli.md`: **CLI commands**. Every domyn command and its options
- `pages/reference/yaml-schema.md`: **YAML configuration**. Every key of a YAML application file, with its type and default
- `pages/reference/events.md`: **Event types**. Every event type the runner emits or accepts, when it occurs and what it carries
