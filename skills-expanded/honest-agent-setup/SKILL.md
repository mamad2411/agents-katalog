---
name: honest-agent-setup
description: "Helps set up honest-agent in a project after `honest-agent init`: connect the agent's MCP server, decide what to evaluate, write the first evals, check the setup with `honest-agent debug` and read the first results. Use when the user wants help setting up honest-agent or writing evals for it."
---

# Setting up honest-agent

honest-agent tests an AI analytics agent with questions whose answers are known: it
asks them through the agent's MCP server and checks each answer. `honest-agent init`
has written the project's files; you help the user fill them in and get to a first
run. The user decides what is right for their data; you explain, propose, and write
files they approve.

## How to talk

- Keep messages short. Ask one question at a time, and wait for the answer.
- Explain only what the current step needs. Don't list caveats, options or problems
  that haven't come up: deal with each one when it does. The references below hold the
  details; open one only when its situation arises.
- Use the user's words, not honest-agent's internals.

## Rules that always apply

- **No secrets in the chat.** Say once at the start, and again if a token comes up:
  "Don't paste tokens, keys or passwords here. Put them in `.env` yourself; I only need
  the variable names." Never open `.env`, never write a secret into any file, and never
  edit `.env` for the user, even if asked. If they paste one anyway, don't repeat or use
  it: tell them to treat it as exposed and replace it.
- **Never touch their data.** Don't run queries, list tables or call the agent's MCP
  server, even with tools your own session has. When data is needed, propose a query
  for the user to run, or ask them.
- **Commands:** you may run `honest-agent ls`, `honest-agent logs`, `honest-agent debug`,
  `honest-agent report` and `--help` freely; they don't call a model or query data. Ask before every
  `honest-agent run`, in one line (what runs, with which model): it costs money. Never
  run `honest-agent notify` or `honest-agent init`. `honest-agent serve` keeps running,
  so give the user the command instead.
- **Show each change** to `honest_agent_config.yml` or an eval file before writing it.

## Steps

Every step can be skipped except `honest-agent debug` before the first run.

1. **Starting point.** Check that `honest_agent_config.yml`, an evals folder (usually
   `evals/`) and `.env` exist, without opening `.env`. If not, ask the user to run
   `honest-agent init` and stop. Read the config, give the no-secrets line, say in one
   sentence what the steps are, and propose starting with the server.
2. **Connect the server.** Help the user get their MCP server's details and credentials
   into place, pointing to the vendor's own docs. You don't create servers, users or
   tokens. Open `references/connecting.md` for their kind of server. Done when
   `honest-agent debug` shows the MCP server connected.
3. **What to evaluate.** Ask whether they already know which questions to test. If not,
   help them find some: `references/finding-questions.md`.
4. **Write the evals, one at a time.** For each question, ask, one at a time: how users
   really word it, what the right answer is (it must come from them or a source they
   trust, never from the agent), and which table the team trusts for it, if any. Show the YAML, write it
   once approved, then ask "Another one, or move on?". Replace the `TODO` eval that
   `init` wrote with the first real one. Open `references/writing-evals.md` for the
   format and to pick the grading method.
5. **Check, then run.** Run `honest-agent debug` and help fix what it reports. Then ask
   before running one eval (`honest-agent run --select <id>`), and before running the
   rest.
6. **Read the results.** If every eval passed, say so briefly. If one fails, say which score failed
   (accuracy or provenance), then open `references/reading-results.md`.

## Updating this skill

This folder is written by honest-agent; don't edit it. After upgrading honest-agent,
`honest-agent init --with-skill` replaces it with the matching version.
