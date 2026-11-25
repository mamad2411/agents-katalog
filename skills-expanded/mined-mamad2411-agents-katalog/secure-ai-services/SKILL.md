---
name: secure-ai-services
description: Secure AI services and the AI tooling in your stack — scan OpenAI, Anthropic, vLLM, Databricks AI, and vector stores with cnspec, and govern which AI agents, IDE extensions, and MCP servers are approved (mondoo-ai-security, mondoo-mcp-security), mapped to the OWASP Top 10 for LLM & GenAI. Use to check an AI service's configuration or audit AI tooling on a host.
allowed-tools: Bash Read
---

# Secure AI Services

Check whether the AI services you run — and the AI tooling your developers use — are configured
and governed securely, by running [cnspec](https://github.com/mondoohq/cnspec). This is the
posture side of AI security; it complements `secure-pipeline`, which flags insecure LLM *code*
(prompt handling, untrusted model output) as an agent writes it.

## When to use

- Auditing a hosted or self-hosted AI service (OpenAI, Anthropic, vLLM, Databricks AI) and its
  vector store (Weaviate) for insecure configuration.
- **Governing AI tooling**: enforcing which AI coding agents, IDE extensions, local LLM runtimes,
  and MCP servers are approved on a host — the agentic supply chain.
- Checking MCP server/client security (tool-schema validation, prompt-injection / PII / malicious-URL
  content checks).

## What cnspec checks

- **AI services** — `mondoo-openai-security`, `mondoo-anthropic-security`, `mondoo-vllm-security`,
  `mondoo-databricks-security`, `mondoo-weaviate-security`
- **AI-tooling governance** — `mondoo-ai-security` (approved agents / IDE extensions / local
  runtimes), `mondoo-mcp-security` (MCP server & client security)

These carry `compliance/owasp-llm-top-10-2025` mappings, so a scan doubles as an OWASP LLM Top
10 check (strongest on LLM02, LLM03, LLM06).

## Run a scan

```bash
# Govern AI tooling on the local host (approved agents / MCP servers / runtimes)
cnspec scan local --incognito -f mondoo-ai-security.mql.yaml   -o sarif
cnspec scan local --incognito -f mondoo-mcp-security.mql.yaml  -o sarif

# AI services / vector stores connect via their own provider + credentials —
# load the relevant bundle and follow the cnspec provider docs for the connection.
```

- Logged in to Mondoo Platform, assigned policies run automatically; otherwise `--incognito -f <bundle>`.
- Per-service connection and auth are in the [cnspec docs](https://mondoo.com/docs/cnspec/) —
  this skill names the right bundle for the outcome; cnspec owns how to reach each service.
- `-o sarif` for a CI gate; cnspec exits non-zero on failures.

## Reference, don't duplicate

cnspec owns the policies and authoring (see the
[cnspec repo](https://github.com/mondoohq/cnspec/tree/main/skills)). This skill invokes cnspec
and interprets results.

## Part of the secure-your-stack toolkit

`secure-ai-services` is the **AI** pillar of posture, alongside `secure-os` (hosts),
`secure-cloud` (cloud accounts), and `secure-saas` (SaaS & identity). For the code side of LLM
security (insecure output handling, secrets in prompts), use `secure-pipeline` / `secure-coding`
and the [LLM Top 10 matrix](../../docs/owasp.md#owasp-top-10-for-llm-and-genai-2025). Needs `cnspec`
([install](https://mondoo.com/docs/cnspec/install)) plus access to the target service or host.
