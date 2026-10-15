---
name: mastra-bedrock
description: "Use Amazon Bedrock as the model provider for a Mastra agent, and deploy Mastra agents to AWS Bedrock AgentCore. Use when someone wants a Mastra agent to run on Bedrock/AWS, mentions Claude on Bedrock, createAmazonBedrock, fromNodeProviderChain, or AgentCore deployment."
license: Apache-2.0
---

# Mastra + Amazon Bedrock

Wire a Mastra agent to Amazon Bedrock, and deploy it to AWS Bedrock AgentCore.

## Verify before writing code

This builds on the `mastra` skill's rule: never trust cached Mastra API knowledge. Confirm the installed `@mastra/core` version and, when a model ID matters, that the model is enabled in the target Bedrock account/region.

## Bedrock is not in Mastra's model router

Mastra's `"provider/model"` string router has **no Bedrock provider** — do not guess a `bedrock/...` string. Bedrock is used the other supported way: pass an **AI SDK provider instance** as the agent's `model`. `MastraModelConfig` accepts `LanguageModelV1`–`V4`, which the AI SDK Bedrock provider satisfies.

```bash
npm install @ai-sdk/amazon-bedrock @aws-sdk/credential-providers
```

## Use the default credential chain

Build the provider with `fromNodeProviderChain()`. This is the load-bearing choice: the **credential chain** resolves credentials the standard AWS way — env vars, shared config (`~/.aws`), SSO, and the container/EC2/AgentCore execution role. The **same code runs unchanged locally and deployed** — locally it uses your AWS CLI session; on AgentCore it uses the runtime's IAM role. No key branching, no code diff between environments.

```ts
import { Agent } from '@mastra/core/agent';
import { createAmazonBedrock } from '@ai-sdk/amazon-bedrock';
import { fromNodeProviderChain } from '@aws-sdk/credential-providers';

const bedrock = createAmazonBedrock({
  credentialProvider: fromNodeProviderChain(),
});

export const agent = new Agent({
  id: 'my-agent',
  name: 'My Agent',
  instructions: '...',
  model: bedrock('us.anthropic.claude-opus-4-5-20251101-v1:0'),
});
```

Do **not** hardcode `accessKeyId`/`secretAccessKey` in the constructor, and do not set `region` there — the chain and the SDK read it from the environment.

## Region must match the model-id prefix

Bedrock Claude models are called through cross-region inference profiles whose ID carries a region prefix — `us.`, `eu.`, `jp.`, or `global.`. `AWS_REGION` must belong to that prefix's group (e.g. `us.anthropic.claude-opus-4-5-20251101-v1:0` needs a `us-*` region). A mismatch is a runtime failure, not a type error.

Set `AWS_REGION` in the environment (`.env` locally, the Dockerfile/AgentCore config when deployed). Confirm the exact current Opus model ID against AWS docs or the `@ai-sdk/amazon-bedrock` model tables before committing to it — IDs change.

## Local credentials

For `npm run dev`, the chain needs an active AWS session. Two common `.env` shapes:

```bash
# Named profile (~/.aws/credentials or SSO) — the chain reads the profile, not keys
AWS_PROFILE=your-profile
AWS_REGION=us-east-1
```

```bash
# Static keys
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
```

With a profile you do **not** set the key vars — the two are alternatives. `AWS_REGION` is required either way. For SSO, `aws sso login` first. Also confirm the model has access enabled in the Bedrock console for that account and region.

## Deploying to AgentCore

For the full deploy to AWS Bedrock AgentCore — project scaffold, `bedrock-agentcore` handler, Dockerfile, storage-removal gotcha, and CLI commands — see [`deploy-agentcore.md`](deploy-agentcore.md).
