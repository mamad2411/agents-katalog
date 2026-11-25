---
name: viral-kit
description: Turn any long-form source into a fact-grounded publicity matrix. Use for product launches, project updates, articles, courses, events, personal ideas, hooks, titles, social copy, and platform-specific promotion.
---

# DSH Promotion Toolkit

This file is the readable source mirror for the runtime Skill exported by
`src/skill.js`. DSH registers that Skill from `apply(ctx)` through
`ctx.skills.register(...)`; it is not loaded as an arbitrary prompt file.

Use the viral_kit tool for the first pass whenever it is available. It returns a structured kit with:

- the core idea and three title angles;
- source evidence and a shareability signal explaining why the idea may travel;
- a hook and a source-grounded quote;
- platform drafts for Xiaohongshu, Zhihu, WeChat, WeChat Moments, Weibo, Bilibili, Douyin, Kuaishou, X, Threads, LinkedIn, Reddit, TikTok, YouTube Shorts, Medium, Facebook, and Instagram, plus the selected publishText;
- an image-generation prompt and hashtags;
- risk flags for numbers, attribution, and absolute claims.

Do not add facts that are absent from the source. Treat the output as a draft: preserve attribution, verify metrics and prices, and soften claims that cannot be proven. Chinese platforms default to Chinese; global platforms (X, Threads, LinkedIn, Reddit, TikTok, YouTube, Medium, Facebook, Instagram) default to English. An explicit `language` always wins. Pass `sourceUrl` whenever a repository, product page, article, signup page, or other canonical source exists; never invent a URL. The link should appear in the platform-native CTA. Zhihu should be Markdown-first and explanatory; Xiaohongshu should be conversational, saveable, and checklist-led with restrained emoji; WeChat should be a substantial article; Moments should be a short personal share; video platforms should include shots, voiceover, captions, and a CTA. When the user asks for a different audience, select the matching platform draft before rewriting it, while keeping the same source boundary. Do not copy one platform draft verbatim to another when a tailored version is available.
