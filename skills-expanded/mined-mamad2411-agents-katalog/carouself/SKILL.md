---
name: carouself
description: Generate posts, carousels, images, and hero banners via carouself_* tools. Use after connecting a Carouself API key under Integrations.
---

# Carouself

Use **`carouself_*`** tools after connecting a Bearer API key under Integrations (Carouself).

## Tools
- **`carouself_get_account`** — credits remaining, scopes, rate limit (free). Call before expensive generation when credits may be low.
- **`carouself_create_post`** — LinkedIn / brand / X / blog text (1 credit, `posts` scope).
- **`carouself_create_carousel`** — multi-slide narrative 3–15 slides (1 credit, `carousels` scope).
- **`carouself_create_image`** — Gemini/Grok image data URL (10 credits, `images` scope).
- **`carouself_create_hero_banner`** — social hero banner (3 credits, `hero` scope).

## Rules
- Generation only — do **not** publish from Carouself. Hand off to LinkedIn / Facebook / Instagram tools to post.
- Surface `402` (credits), `403` (missing scope), and `429` (rate limit) clearly to the user.
- Prefer checking account status once per session when doing a batch of generations.

