---
name: llms-txt-authoring
description: >-
  Create, update, validate, or review a site-root `llms.txt` file. Use this skill only when the request includes `llms.txt`. Do not use it for robots.txt, sitemaps, SEO metadata, READMEs, OpenAPI documentation, or AGENTS.md.
---

# llms.txt Authoring

## Workflow

1. Inspect the live site or repository. Identify the canonical documentation, API reference, guides, and examples. Do not invent pages or descriptions.
2. Read [the format guide](references/llms.txt.md) before you write or assess the structure. Treat `llms.txt` as an emerging proposal. Do not treat it as a crawler-control standard or as a guarantee of discovery.
3. For a new file, adapt [the starter template](templates/llms.txt). Keep the required H1 concise. Add optional content only when it helps a reader understand the linked resources.
4. Validate the exact `/llms.txt` location and the Markdown structure. Validate each absolute canonical URL and description. Check for duplicate links. When network access is available, confirm that each target is reachable.
5. Return the complete file or severity-ordered findings. Distinguish proposal violations from optional editorial improvements.

## Verify Current Information

Verify the current proposal at `https://llmstxt.org/` before you state syntax, special section meanings, adoption, or system behavior. Prefer the primary materials that the proposal links to. Record the source URL and access date in the review notes. Do not promise indexing, training, ranking, citation, or crawler behavior after publication.
