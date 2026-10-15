---
name: broker-recognize
description: Product photo recognition for C2C resale. Use when user uploads a product photo and wants AI to identify the item for resale listing. Extracts brand, product name, model, category, condition grade (A-E), material, color, size, notable features, and visible flaws. Also usable standalone via /broker-recognize. Trigger phrases: "what is this", "identify this", "analyze this item", photo upload for resale.
---

# broker-recognize: Photo → Product Info

Extracts structured product information from user-uploaded photos for C2C resale listing purposes.

## Prerequisite: ANTHROPIC_API_KEY

This skill uses the **Anthropic API** (Claude Vision) for image analysis. Your current LLM model may not support multimodal vision, so the skill calls the Vision API directly.

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

If the key is missing, the skill will output an error instructing the user to set it.

## Workflow

1. User provides 1-3 photos of the item
2. Analyze using vision: brand, product name, model, category, condition (A-E), material, color, size, features, flaws, estimated original retail
3. Present structured card to user for confirmation/correction
4. Save product info to conversation context for next skill in pipeline

## Condition Grade Scale

| Grade | Label | Criteria |
|-------|-------|----------|
| A | Like New | No visible wear, original packaging if applicable |
| B | Excellent | Minor signs of use, no significant flaws |
| C | Good | Visible wear, minor flaws, fully functional |
| D | Fair | Noticeable wear/flaws, may need minor repair |
| E | For Parts | Significant damage, sold as-is |

## Key Rule

Be honest about flaws. Transparency is the foundation of C2C trust. A lost honest sale is better than a return from undisclosed flaws.

## Script

`scripts/recognize.py` provides the structured prompt template and output schema.
