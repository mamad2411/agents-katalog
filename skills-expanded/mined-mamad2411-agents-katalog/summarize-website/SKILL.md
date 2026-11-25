---
name: summarize-website
description: Use this skill when the user asks to summarize or compare website information from either a file or directly provided URLs, for example "このファイルのサイトを要約して", "urls.txt を比較して", or "このURLの内容を要約して".
---

# Summarize Website

This skill helps summarize website information from either a user-specified file or directly provided URLs.

## When to Use This Skill

Use this skill when the user:

- Wants a summary of one or more websites listed in a file
- Wants a summary of one or more URLs written directly in the prompt
- Provides a file that contains URLs, website names, or notes copied from websites
- Wants multiple sites compared based on a file they prepared
- Wants multiple directly provided URLs compared
- Wants a concise digest of website content without reading each page manually

## Inputs This Skill Accepts

The input may be either a file path or one or more directly provided URLs.

If a file is provided, it may contain:

- One URL per line
- Markdown links
- Website names with notes
- Plain text copied from one or more websites
- A mix of URLs and handwritten notes

If URLs are provided directly in the prompt, they may be:

- A single URL
- Multiple URLs separated by spaces or lines
- URLs with a short request such as "compare these" or "summarize this page"

## Workflow

### Step 1: Detect the Input Type

Identify which of these cases applies:

1. The user provided a file path
2. The user provided one or more URLs directly
3. The user provided both a file path and direct URLs

If a file path is provided, read the file and determine whether it contains:

1. One or more URLs
2. Website descriptions or copied text but no URLs
3. Both URLs and local notes

If neither a file path nor a URL is provided, ask for one of them.

### Step 2: Extract Relevant Website Entries

From the file content and direct prompt content, extract:

- URLs
- Website titles or names if present
- Any local notes that clarify what the user cares about

Ignore unrelated boilerplate when possible.

### Step 3: Fetch Live Page Content When URLs Exist

If the file contains URLs or the user supplied URLs directly, use the webpage fetching tool to retrieve the main content of those pages.

Prioritize:

- Official landing pages
- Product or service overview pages
- Documentation index pages when the user is evaluating tools

If a URL cannot be fetched, fall back to summarizing any text already present in the file or prompt and clearly note that limitation.

### Step 4: Merge Notes With Page Content

When the file or prompt includes handwritten notes or copied excerpts, combine them with fetched content instead of discarding them.

Treat the file or prompt as user-provided context that may highlight what matters most.

### Step 5: Summarize for the User's Goal

Choose the summary shape based on the request:

- General summary: 3 to 6 bullet points per site
- Comparison summary: similarities, differences, notable strengths, and likely fit
- Executive digest: short paragraph plus key takeaways
- Research notes: structured bullets grouped by topic

Unless the user asks otherwise, answer in Japanese and keep the summary concise.

## Output Guidelines

When producing the final answer:

- Mention which file was used, if any
- Mention which URLs were provided directly, if any
- Mention which URLs were successfully fetched and which were not
- Separate confirmed page content from assumptions or file-only notes
- Keep claims faithful to the source content
- Do not invent missing facts

## Recommended Response Structure

Use a compact structure like this:

1. Scope: what file and URLs were used
2. Summary: the main points for each site
3. Notes: fetch failures, ambiguity, or missing context

## Example Triggers

- "このファイルにあるサイトを要約して"
- "list.md に書いた候補サービスを比較して"
- "urls.txt の中身を見て各サイトの概要をまとめて"
- "このURLの内容を要約して: https://example.com"
- "この2つのURLを比較して: https://example.com/a https://example.com/b"
- "examples/website-summary-input.md を使ってサイト内容を要約して"

## Example Input File

You can test this skill with:

- `examples/website-summary-input.md`

That sample includes:

- Plain URLs
- Markdown links
- Short notes about what to focus on
- A comparison-oriented prompt style

## Constraints

- If the file content is already a copied article or webpage excerpt, you may summarize that text directly without fetching anything.
- If the user only provides URLs directly, you do not need to ask for a file.
- If the file has many URLs, summarize the most relevant ones first and state any omissions.
- If the request is ambiguous, ask whether the user wants a plain summary, a comparison, or a recommendation.