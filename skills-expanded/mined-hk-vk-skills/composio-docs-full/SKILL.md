---
name: composio-docs-full
description: Composio powers 1000+ toolkits, tool search, context management, authentication, and a sandboxed workbench to help you build AI agents that turn intent into action.
metadata:
  source: llms.txt
  source_url: https://docs.composio.dev/llms-full.txt
  generated: 2026-07-06T20:24:26.538Z
---

# Search Tools (/toolkits/meta-tools/search_tools)

> Composio powers 1000+ toolkits, tool search, context management, authentication, and a sandboxed workbench to help you build AI agents that turn intent into action.

**Purpose:** Enforce only the **current** and **correct** patterns for integrating [Composio](https://composio.dev/) tools into AI agents.
**Scope:** All AI-generated code using Composio must follow these guardrails.

## Available Resources

### 1. Correct Composio Integration

### 2. CRITICAL INSTRUCTIONS FOR AI MODELS

### Terminology Migration (old → current)

### OpenAI Agents

### Claude Agent SDK

### Vercel AI SDK

- **Configuring Sessions**: Restrict toolkits, set custom auth configs, and select connected accounts
  - URL: /docs/configuring-sessions

- **Anthropic**
  - URL: /docs/providers/anthropic

- **OpenAI**
  - URL: /docs/providers/openai

- **Vercel AI SDK**
  - URL: /docs/providers/vercel

- **Google**
  - URL: /docs/providers/google

- **LangChain**
  - URL: /docs/providers/langchain

- **CrewAI**
  - URL: /docs/providers/crewai

- **LlamaIndex**
  - URL: /docs/providers/llamaindex

- **Mastra**
  - URL: /docs/providers/mastra

- **Pi**
  - URL: /docs/providers/pi

- **AutoGen**
  - URL: /docs/providers/autogen

- **Build your own**
  - URL: /docs/providers/custom-providers

- **Claude Messages API**
  - URL: https://docs.anthropic.com/en/api/messages

- **Claude Agent SDK**
  - URL: https://docs.anthropic.com/en/docs/agents-and-tools/claude-agent-sdk

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

- **Responses API**
  - URL: https://platform.openai.com/docs/api-reference/responses

- **Chat Completions API**
  - URL: https://platform.openai.com/docs/api-reference/chat

- **Agents SDK**
  - URL: https://openai.github.io/openai-agents-python/

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

- **What is a session?**: How sessions scope users, tools, and auth, and how to reuse them across requests.
  - URL: /docs/how-composio-works

### Non-agentic provider

### Agentic provider

- **Configuring Sessions**: Enable toolkits, set auth configs, and select connected accounts
  - URL: /docs/configuring-sessions

### Enable selected meta tools

### Precedence

### tools()

### authorize()

### toolkits()

### delete()

- **Sandbox**: Give sessions a persistent compute environment with COMPOSIO_REMOTE_WORKBENCH and COMPOSIO_REMOTE_BASH_TOOL
  - URL: /docs/sandbox/remote

- **Configuring Sessions**: Restrict toolkits, set custom auth configs, and select connected accounts
  - URL: /docs/configuring-sessions

### Built-in helpers

### Libraries

### Error correction

### Persistent state

### Compute tier

- **Local sandbox**: Run the same tool calls in a sandbox you own, while Composio keeps managed auth and discovery.
  - URL: /docs/sandbox/local

- **What is a session?**: How sessions scope tools, auth, and sandbox state to a user
  - URL: /docs/how-composio-works

- **Custom tools and toolkits**: Define in-process tools and toolkits that run alongside Composio tools
  - URL: /docs/extending-sessions/custom-tools-and-toolkits

### Naming and descriptions

### Accessing authenticated APIs

### Defining inputs in Python

### Tool names get prefixed

- **Configuring sessions**: Filter toolkits and tools, set auth configs, and read tools with session.tools()
  - URL: /docs/configuring-sessions

### Custom callback URL

- **Manual auth management**: Generate Connect Links yourself, check connection status, and disable in-chat prompts
  - URL: /docs/manually-authenticating

- **Managing multiple connected accounts**: Let a user connect work and personal accounts for the same toolkit, then pick which one runs
  - URL: /docs/managing-multiple-connected-accounts

### Configuration options

### Setting an alias during connection

### Updating or clearing an alias

- **Shared connections**: Make one connected account usable by multiple users with a per-user access control list
  - URL: /docs/shared-connections

### Common ACL patterns

- **Configuring sessions**: Pin connected accounts, auth configs, and toolkit restrictions into a session
  - URL: /docs/configuring-sessions

- **auth config**
  - URL: /docs/programmatic-auth-configs

- **Managing multiple accounts**: Pin and select connected accounts for a user
  - URL: /docs/managing-multiple-connected-accounts

- **Composio managed apps**
  - URL: /toolkits/managed-auth

- **white-label the Connect Link page**
  - URL: /docs/white-labeling-authentication#customizing-the-connect-link

### Toolkits without managed auth

- **Programmatic auth configs**: Create auth configs in code and pass them to a session
  - URL: /docs/programmatic-auth-configs

- **Controlling scopes**: Override the default OAuth scopes Composio requests for a toolkit
  - URL: /docs/controlling-scopes

- **White-labeling authentication**: Remove Composio branding from your auth flows
  - URL: /docs/white-labeling-authentication

- ****Auth Screen****
  - URL: https://dashboard.composio.dev/~/project/settings/auth-screen

- **Managed vs custom auth**: Decide when to use custom credentials, create an auth config, and pass it to sessions.
  - URL: /docs/custom-app-vs-managed-app

### Switching from Composio-managed to your own OAuth app

- **Managed vs custom auth**: Set up auth configs for OAuth apps, API keys, and toolkits without managed auth
  - URL: /docs/custom-app-vs-managed-app

- **auth config**
  - URL: /docs/authentication#behind-the-scenes

- **Creating triggers**
  - URL: /docs/setting-up-triggers/creating-triggers

- **Receiving events**
  - URL: /docs/setting-up-triggers/subscribing-to-events

- **Managing triggers**
  - URL: /docs/setting-up-triggers/managing-triggers

- **Creating triggers**: Activate a trigger for a user so events start flowing
  - URL: /docs/setting-up-triggers/creating-triggers

### Targeting a specific connected account

- **Receiving events**: Get trigger events locally with the SDK or in production over your webhook URL
  - URL: /docs/setting-up-triggers/subscribing-to-events

### Quick look with `subscribe()`

### Forward to your local handler with the CLI (recommended)

### Cloudflare Tunnel

### ngrok

### Inspecting trigger payload schemas

### Webhook payload shape

- **Managing triggers**: List, enable, disable, and delete trigger instances
  - URL: /docs/setting-up-triggers/managing-triggers

- **Creating triggers**: Activate a trigger for a user so events start flowing
  - URL: /docs/setting-up-triggers/creating-triggers

### Search, connect, and execute tools

### Run scripts and sub-agents

### Listen to trigger events

### Initialize project context

### Inspect toolkits and versions

### Create and inspect auth configs

### Manage connected accounts

### Execute and inspect logs

### Work with triggers

### Generate type definitions

- **Configuring Sessions**: Toolkits, auth configs, account selection, and session methods
  - URL: /docs/configuring-sessions

### Native tools for your framework

### Execute a tool without an LLM

- **Configuring Sessions**
  - URL: /docs/configuring-sessions

- **Shared connections**
  - URL: /docs/shared-connections

- **White-labeling authentication**
  - URL: /docs/white-labeling-authentication

- **Configuring Sessions**: Toolkits, auth configs, account selection, presets, and session methods
  - URL: /docs/configuring-sessions

- **Configuring Sessions**: Restrict toolkits, set auth configs, and select connected accounts
  - URL: /docs/configuring-sessions

### Before (will fail)

### After (required)

- **Migrate to sessions**: Move from older tool execution patterns to sessions
  - URL: /docs/migration-guide/direct-to-sessions

### UserID scoping

### Replacing ToolSets with Providers

### Fetching and filtering tools

### Fetching raw tool data

### Executing tools

### Tool Modifiers (formerly Tool Processors)

### Custom Tools

### Auth configs (formerly integrations)

### Connected accounts / User IDs

### Triggers

### Local tools

### Toolkits (formerly Apps)

### Tools (formerly Actions)

### Auth Configs (formerly Integrations/Connectors)

### Connected Accounts (formerly Connections)

### Triggers

- **Composio Connect**
  - URL: /docs/composio-connect

### Claude Code

### Codex

### OpenClaw

### Claude Desktop

### ChatGPT

### Cursor

### Notion

### VS Code

### Windsurf

### Cline

### Agent Builder

### n8n

### MCP URL

### Tools aren't appearing in my agent

### The OAuth link expired or didn't open

### An app action is failing with an auth error

- **Composio dashboard**
  - URL: https://dashboard.composio.dev

### I want to remove or reconnect an app

### I still need help

### List servers

### Get server details

### Update a server

### Delete a server

- **Providers**: Use with Anthropic, OpenAI, and other frameworks
  - URL: /docs/providers

### Start with a basic agent

### Put it in a Slack thread

### Share one workspace connection

### Reach the gaps with the proxy

### Redirect auth links

### Serve the webhook

- **Configuring sessions**: Everything a session can scope: toolkits, tools, connections, and limits
  - URL: /docs/configuring-sessions

- **Shared connections**: SHARED vs PRIVATE accounts and the per-user ACL
  - URL: /docs/shared-connections

- **General agent with Pi**: Build a Pi + Composio agent and drop it into Slack: triggers, per-user sessions, a shared connection, redirected auth links, and the proxy.
  - URL: /examples/general-agent-with-pi

- **Daily standup bot**: A Slack bot that drafts each teammate's standup from their own connected tools: your own Slack app, tool-router sessions, manual tool execution, the proxy, and per-member auth links.
  - URL: /examples/standup-slackbot

- **Local sandbox PR reviewer**: Run a PR reviewer in your own sandbox while it calls GitHub tools through a Composio session.
  - URL: /examples/local-sandbox-pr-reviewer

- **Composio session**
  - URL: /docs/how-composio-works

- **`run_composio_tool`, `invoke_llm`, and `web_search`**
  - URL: /docs/sandbox/remote

### Create the Composio client

### Check the GitHub connection

### Create the local sandbox session

### Start your sandbox, inject the helper

### Run the reviewer and stream output

- **manual execution**
  - URL: /docs/tools-direct/executing-tools

- **manual connections**
  - URL: /docs/manually-authenticating

- **white-labelling**
  - URL: /docs/white-labeling-authentication

- **`proxyExecute`**
  - URL: /docs/extending-sessions/proxy-execute

### A session writes the draft

### Use what's connected, nothing more

- **Configuring sessions**: What a session can scope: toolkits, tools, connections, and connection management
  - URL: /docs/configuring-sessions

- **White-labeling authentication**: Ship a bot under your own app's name, icon, and credentials
  - URL: /docs/white-labeling-authentication

- **Custom vs managed auth**: Bring-your-own Slack app versus a Composio-managed connection
  - URL: /docs/custom-app-vs-managed-app

- **Triggers**: Run agents in response to events: schedules, webhooks, and app activity
  - URL: /docs/triggers

### Attributes

### Authentication errors

### Tool errors

### Connection errors

### Trigger errors

- **Discord**: Community support
  - URL: https://discord.com/channels/1170785031560646836/1268871288156323901

- **Email**: Contact support team
  - URL: mailto:support@composio.dev

- **GitHub**: Report a bug
  - URL: https://github.com/ComposioHQ/composio/issues/new?labels=bug

- **Authenticating to Composio**
  - URL: /reference/authenticating-to-composio

- **Rate Limits**
  - URL: /reference/rate-limits

- **TypeScript SDK**: TypeScript SDK reference
  - URL: /reference/sdk-reference/typescript

- **Python SDK**: Python SDK reference
  - URL: /reference/sdk-reference/python

- **Errors**: Understanding API error responses
  - URL: /reference/errors

- **Pricing**: Compare plans and limits
  - URL: https://composio.dev/pricing

- **Scoped project API keys**: Permission areas, access levels, and covered routes
  - URL: /reference/authenticating-to-composio/project-api-key-permissions

- **Errors**: Understanding API error responses
  - URL: /reference/errors

- **Rate Limits**: API rate limits by plan
  - URL: /reference/rate-limits

- **Authenticating to Composio**: Authenticate API requests with project and organization API keys
  - URL: /reference/authenticating-to-composio

- **Projects**: Understand projects, project API keys, and project-scoped resources
  - URL: /reference/api-reference/projects

- **Proxy execute**: Call connected account APIs through the raw proxy path
  - URL: /reference/api-reference/tools

- **Observability**: Inspect tool execution logs and usage summaries
  - URL: /reference/api-reference/logs

- **Errors**: Understanding API error responses
  - URL: /reference/v3/errors

- **Rate Limits**: API rate limits by plan
  - URL: /reference/v3/rate-limits

### Attributes

### Authentication errors

### Tool errors

### Connection errors

### Trigger errors

- **Discord**: Community support
  - URL: https://discord.com/channels/1170785031560646836/1268871288156323901

- **Email**: Contact support team
  - URL: mailto:support@composio.dev

- **GitHub**: Report a bug
  - URL: https://github.com/ComposioHQ/composio/issues/new?labels=bug

- **Authentication**
  - URL: /reference/v3/authentication

- **Rate Limits**
  - URL: /reference/v3/rate-limits

- **Errors**: Understanding API error responses
  - URL: /reference/v3/errors

- **Pricing**: Compare plans and limits
  - URL: https://composio.dev/pricing

- **manually authenticating users**
  - URL: /docs/manually-authenticating

### Filter fields

### Operators

### Parameters

### Find failed Gmail tool calls in the last hour

### Get failures for a specific user

### Fetch a single log's full request/response

### Summary parameters

### Breakdown `group_by` options

### Breakdown parameters

### Top 10 tools my org called last week

### Tool call count per user for my project this month

### Which toolkits is a specific user using?

- **triggers**
  - URL: /docs/triggers

- **connected account**
  - URL: /docs/auth-configuration/connected-accounts

### list()

### create()

### get()

### update()

### delete()

### enable()

### disable()

### update()

### update\_acl()

### initiate()

### link()

### wait\_for\_connection()

### before\_execute

### after\_execute

### before\_file\_upload

### schema\_modifier

### create()

### list()

### get()

### update()

### delete()

### generate()

### tools()

### authorize()

### toolkits()

### search()

### execute()

### custom\_tools()

### custom\_toolkits()

### proxy\_execute()

### update()

### delete()

### list()

### get()

### list\_categories()

### authorize()

### get\_connected\_account\_initiation\_fields()

### get\_auth\_config\_creation\_fields()

### get\_raw\_composio\_tool\_by\_slug()

### get\_raw\_composio\_tools()

### get\_raw\_tool\_router\_meta\_tools()

### get()

### execute()

### proxy()

### set\_webhook\_subscription()

### get\_type()

### list\_active()

### list()

### create()

### subscribe()

### verify\_webhook()

### parse()

### create()

### delete()

### disable()

### enable()

### get()

### list()

### update()

### updateStatus()

### constructor()

### createSession() (deprecated)

### flush()

### getClient()

### getConfig()

### delete()

### disable()

### enable()

### get()

### initiate()

### link()

### list()

### refresh()

### update()

### updateAcl()

### updateStatus()

### waitForConnection()

### updateAcl() (deprecated)

### create()

### delete()

### generate()

### get()

### list()

### update()

### blob()

### buffer()

### save()

### text()

### parse()

### delete()

### download()

### list()

### upload()

### authorize()

### customToolkits()

### customTools()

### delete()

### execute()

### proxyExecute()

### search()

### toolkits()

### tools()

### update()

### create()

### delete()

### use()

### authorize()

### get()

### getAuthConfigCreationFields()

### getConnectedAccountInitiationFields()

### listCategories()

### execute()

### executeSessionTool()

### get()

### getInput()

### getRawComposioToolBySlug()

### getRawComposioTools()

### getRawToolRouterSessionTools()

### getToolsEnum()

### proxyExecute()

### create()

### delete()

### disable()

### enable()

### getType()

### listActive()

### listEnum()

### listTypes()

### parse()

### setWebhookSubscription()

### subscribe()

### unsubscribe()

### update()

### verifyWebhook()

- **manually authenticating users**
  - URL: /docs/manually-authenticating

- **triggers**
  - URL: /docs/triggers

- **connected account**
  - URL: /docs/auth-configuration/connected-accounts

- **Search APIs**: Composio Search, Perplexity, Exa, SerpAPI
  - URL: /toolkits/composio_search

- **Code execution**: Sandboxed runtimes like E2B
  - URL: /toolkits/codeinterpreter

## How to Use This Skill

Reference these resources when working with Search Tools (/toolkits/meta-tools/search_tools).