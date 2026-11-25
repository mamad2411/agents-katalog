---
name: wiki
description: Answer codebase-documentation questions using DeepWiki as the primary source, falling back to local docs. Use when asked to map out an extension's architecture, document skill connections, or explain how parts of a repo fit together.
---
# Wiki Generation

DeepWiki is the primary source. Do not crawl and rewrite a whole repo by hand when DeepWiki already indexed it.

## Step 0 — run the sidecar

```bash
./scripts/wiki-context.sh                # current repo (from git remote)
./scripts/wiki-context.sh <owner/repo>   # explicit repo
```

It returns `deepwiki_url`, `local_docs[]`, and `skill_count` as JSON. No network calls — you fetch DeepWiki yourself in the next step.

## Step 1 — ask DeepWiki first

Fetch the relevant DeepWiki page(s) for the question:

```
https://deepwiki.com/<owner>/<repo>
```

Use the agent's URL-fetch tool and drill into the sections that answer the question (architecture, routing, skills, capture formats, guardrails). Quote or link the DeepWiki sections you used so the answer stays traceable.

DeepWiki indexes only what is pushed — it cannot see unpushed work. Check any
answer that depends on recent code against the local checkout and revision
before quoting it; when `repo` differs from `checkout_repo` in the sidecar
output, treat `local_docs[]` as belonging to the checkout.

If the repo is private or DeepWiki has no page for it, fall through to step 2.

## Step 2 — local fallback (only when DeepWiki has nothing)

Read the local docs from the sidecar's `local_docs[]` list plus `packages/skills/*/SKILL.md` for the skills in question. Synthesize a focused answer — not a full `docs/wiki/` tree. A full generated wiki is only worth it when explicitly asked; a directly answering page with links beats five speculative index pages.

When you do write local pages, follow these rules:

- One page per question, Mermaid only where a diagram carries information text cannot.
- Every skill listed links to its actual `SKILL.md` file.
- Keep it agent-friendly and concise. No human-centric tutorials.

## Step 3 — chain

If the answer exposes gaps in tests or implementation, chain into `review` (audit) — not into writing more wiki pages.
