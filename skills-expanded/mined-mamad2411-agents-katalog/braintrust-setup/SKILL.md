---
name: braintrust-setup
description: Set up Braintrust, including API keys, projects, SDK install, and the hosted Braintrust MCP server. Use when connecting to Braintrust for the first time or fixing authentication issues.
---

# Braintrust Setup

## Account, project, key

1. Sign up at https://www.braintrust.dev and create an organization.
2. Create a project (one per app or repo is a good default; experiments,
   logs, datasets, and prompts all hang off a project).
3. Create an API key in settings. Keys start with `sk-`.

```bash
export BRAINTRUST_API_KEY="sk-..."
```

Store it in your secret manager or an untracked `.env`; never commit it. The
key is read automatically by the SDKs and CLI.

## Install

```bash
npm install braintrust autoevals     # TypeScript
pip install braintrust autoevals     # Python
```

SDKs also exist for Go, Java, Ruby, and C#. The `bt` CLI (bundled with the
SDK packages) runs eval files: `bt eval my_eval.eval.ts`.

Set the project name in SDK initialization (`Eval("Project", ...)`,
`initLogger({ projectName })`) to your app or repo name so logs and
experiments land together.

## LLM-based scorers

Autoevals judges need a model. Either export a provider key (e.g.
`OPENAI_API_KEY`) or configure provider keys in Braintrust and route through
its AI proxy, which adds caching and lets you switch judge models without
code changes.

## Braintrust MCP server

This plugin connects to the official hosted MCP server at
`https://api.braintrust.dev/mcp` (streamable HTTP). Authentication is OAuth
with your Braintrust account on first use; header-based auth with
`Authorization: Bearer $BRAINTRUST_API_KEY` is also supported by the server.
Never paste the key into chat or config files.

Once connected, agents get: docs search, object resolution (names to IDs for
projects, experiments, datasets), recent objects, `infer_schema`, BTQL
queries, experiment summaries, and permalink generation.

For self-hosted Braintrust deployments the MCP server runs inside your
environment, so data does not leave your infrastructure; point the URL at
your API host instead of `api.braintrust.dev`.

## Verify

1. `bt eval` on a trivial eval file: an experiment link should print.
2. Run one wrapped LLM call (see `braintrust-logging`): the trace should
   appear on the Logs page within seconds.
3. Ask the MCP server to list recent objects in your project.

## Troubleshooting

- 401: key missing or from the wrong organization; re-export and retry.
- Eval runs but no experiment: project name mismatch between code and UI.
- Judge scorers erroring: missing provider key (see above).
