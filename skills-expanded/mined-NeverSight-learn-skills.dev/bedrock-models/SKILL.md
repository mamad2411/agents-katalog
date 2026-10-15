---
name: bedrock-models
description: "AWS Bedrock model IDs and cross-region inference profiles. Use this skill whenever code references AWS Bedrock model IDs (modelId), cross-region inference, or model selection. Triggers on: amazon.nova-*, anthropic.claude-*, cohere.*, deepseek.*, meta.llama*, mistral.*, qwen.*, any Bedrock InvokeModel/Converse call, BedrockRuntimeClient, or questions about which model to use on Bedrock. NEVER guess or invent model IDs — they are inconsistent across providers (some have dates, some don't, some have :0 suffix, some don't). Always check this skill first."
---

# AWS Bedrock Model IDs

NEVER guess or invent Bedrock model IDs. They are inconsistent across providers and even across models from the same provider. Read `references/models.md` for the complete list.

## Staleness fallback

The CLI is the source of truth — AWS doc pages lag behind the live API.

```bash
aws bedrock list-foundation-models --region <region> --query "modelSummaries[].{id:modelId,name:modelName,provider:providerName}" --output table
```

Docs (secondary): https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html

## AccessDeniedException

If a Bedrock call returns `AccessDeniedException`, the model's Marketplace subscription hasn't been set up. Bedrock auto-subscribes on first invoke if the IAM role has `aws-marketplace:Subscribe` and `aws-marketplace:ViewSubscriptions`.

Providers that bypass Marketplace (no subscription needed): Amazon, DeepSeek, Meta, Mistral AI, OpenAI, Qwen. All others go through Marketplace.

Anthropic additionally requires a one-time "First Time Use" form per account via Bedrock console or `aws bedrock put-use-case-for-model-access`.

Diagnose:
```bash
aws bedrock get-foundation-model-availability --model-id <model-id> --region <region>
```

Fix:
```bash
aws bedrock create-foundation-model-agreement \
  --model-id <model-id> --region <region> \
  --offer-token "$(aws bedrock list-foundation-model-agreement-offers \
    --model-id <model-id> --region <region> \
    --query 'offers[0].offerToken' --output text)"
```

Reference: https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html

Last verified: 2026-05-31
