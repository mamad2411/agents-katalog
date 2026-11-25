---
name: tomba-author-finder
description: "Find the email address of the author of a blog post or news article from its URL using Tomba's author_finder tool."
user-invocable: true
argument-hint: "<article URL>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "✍️"
        homepage: https://tomba.io
---

# Tomba Author Finder

This skill uses the `author_finder` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Press and PR outreach, or contacting a journalist or blogger about a specific article.

Do not use it when:

- The URL is a LinkedIn profile: use `tomba-linkedin-finder`.

## Inputs

| Parameter     | Type         | Required | Notes                                                                  |
| ------------- | ------------ | -------- | ---------------------------------------------------------------------- |
| `url`         | string       | yes      | Full public URL of the article (http or https)                         |
| `webhook_url` | string (URL) | no       | Hosted server only: public URL that receives the result asynchronously |

## Workflow

1. Call `author_finder` with the article URL.
2. Optionally verify the result with `tomba-email-verifier`.

## Output Expectations

- Author name, email, position, and confidence; say clearly if no author could be identified.

## Example Usage

```
/tomba:tomba-author-finder https://techcrunch.com/2023/03/14/openai-releases-gpt-4-ai-that-it-claims-is-state-of-the-art/
/tomba:tomba-author-finder https://blog.hubspot.com/marketing/example-post
```

## Example Tool Call

User: "Who wrote this TechCrunch article and how do I reach them?"

```json
{
    "tool": "author_finder",
    "arguments": {
        "url": "https://techcrunch.com/2023/03/14/openai-releases-gpt-4-ai-that-it-claims-is-state-of-the-art/"
    }
}
```
