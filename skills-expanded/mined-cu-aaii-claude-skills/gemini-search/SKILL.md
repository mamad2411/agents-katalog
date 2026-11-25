---
name: gemini-search
description: Search the web for current information using Gemini with Enterprise Web Search grounding. Use this instead of the built-in WebSearch tool.
---

# Web Search via Gemini + Enterprise Web Search Grounding

Use this skill when the user invokes `/gemini-search …` **or** whenever you need current web information.

**Goal:** run a grounded web search with Gemini using Google's Enterprise Web Search, then present Gemini's answer with inline citations, Search Suggestions, and a source list — **without adding your own analysis or interspersing other content**.

---

## Step 0: Create the query (do this before calling the API)

Always turn what the user said into a *search query string* first.

### If the user invoked `/gemini-search …`
Treat the text after `/gemini-search` as **user intent**, not necessarily a perfectly-formed query.

- If it already looks like a search query (short, keyword-y, includes operators like `site:` / `filetype:` / quotes), keep it as-is.
- Otherwise, distill it into a Google-style query.

### If you are invoking this skill implicitly
Generate a query from the user's most recent request.

### Query-building rules
- Include **key entities** (names, products, orgs, places) + the **specific ask** (e.g., "pricing", "release date", "policy", "error", "docs", "examples").
- Respect constraints: versions, geography, timeframe, platform, format.
- Prefer 6–14 meaningful words; remove filler.
- Use operators when helpful:
  - Exact phrase: `"…"`.
  - Official sources: `site:…`.
  - PDFs: `filetype:pdf`.
  - Synonyms: `(term1 OR term2)`.

**Do not show your query-building reasoning.**
Optionally, you may show the final query as a single line: `Query: …`

---

## Step 1: Run the search (curl)

Use the Bash tool to execute the request.

**Important implementation notes**
- Construct the JSON payload inline. Escape any double quotes or backslashes in the user's query when building the JSON string.
- Do **not** stream. Some gateways omit grounding metadata in streaming mode; this skill expects the full JSON response.
- Never print or log the auth token.

### Bash command

Replace `<QUERY>` with the final query string from Step 0 (escape `"` as `\"` and `\` as `\\` within the JSON):

```bash
curl -sS --max-time 90 -X POST "https://api.ai.it.cornell.edu/chat/completions" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google-enterprise-web-search",
    "tools": [{"enterpriseWebSearch": {}}],
    "messages": [
      {
        "role": "user",
        "content": "<QUERY>"
      }
    ]
  }'
```

### Token handling

- `$ANTHROPIC_AUTH_TOKEN` must be set in the environment.
- Keep the header exactly as shown (double quotes are fine); do not single-quote the header (that would prevent shell expansion), and do not hardcode a token.

### Timeouts

- Keep `--max-time 90`.
- The default Bash tool timeout is sufficient; do not override it.

---

## Step 2: Parse the response

This endpoint returns standard OpenAI Chat Completions JSON.

### 2.1 Extract the answer text

Primary answer is in `choices[0].message.content`. This is the **Grounded Result**.

### 2.2 Extract Search Suggestions (when present)

Search Suggestions are the search queries Google provides alongside Grounded Results. **You must always display them whenever they are present.**

Look for:
- **`vertex_ai_grounding_metadata[0].webSearchQueries[]`** — Array of search query strings (e.g., `["What is a monstera?"]`). Display these in CLI output.
- `vertex_ai_grounding_metadata[0].searchEntryPoint.renderedContent` also exists but is HTML/CSS meant for web UIs — not usable in a CLI context.

### 2.3 Extract source citations and build inline citations

**Inline citations are required.** Displaying grounding support helps validate responses and provides avenues for further learning. Use `groundingSupports` and `groundingChunks` to attach citation markers to specific claims in the Grounded Result text.

**Source data** comes from two places (they encode the same information in different formats):

#### Vertex grounding metadata (preferred — richer structure)

`vertex_ai_grounding_metadata[0]` contains:

- **`groundingChunks[]`** — Array of web sources. Each has:
  - `web.uri` — An opaque Google redirect URL (the **Link** per the Service Specific Terms). This is the actual clickable URL for the source.
  - `web.title` — Title or label for the source (often a domain name like `"ivywise.com"`).
  - `web.domain` — Domain of the source.
- **`groundingSupports[]`** — Maps text spans of the Grounded Result to their supporting sources. Each entry has:
  - `segment.startIndex` / `segment.endIndex` / `segment.text` — Identifies the span of text in the Grounded Result that is supported.
  - `groundingChunkIndices[]` — Array of indices into `groundingChunks[]` identifying which sources support this segment.

#### OpenAI-style annotations (alternative)

`choices[0].message.annotations[]` where `type == "url_citation"`. Each entry includes `title`, `url`, and `start_index`/`end_index`. These carry the same citation information as the Vertex metadata but in a flatter format.

#### Building inline citations

Use the `groundingSupports` array to insert citation markers into the Grounded Result text. The approach (matching the pattern shown in the Gemini API documentation):

1. Build a numbered source list from `groundingChunks`.
2. Sort `groundingSupports` by `endIndex` in **descending** order (to avoid shifting issues when inserting markers).
3. For each support entry, insert citation markers (e.g., `[1]`, `[2]`) at the `endIndex` position in the text, referencing the corresponding `groundingChunkIndices`.

In CLI output, format the inline markers as bracketed references like `[1]` or `[1][3]`, then list the full sources (title, domain, and full URI) at the bottom.

### 2.4 Error handling

If the curl command fails, returns non-JSON, or `choices[0].message.content` is missing/empty:

- Tell the user the search failed.
- Suggest verifying `$ANTHROPIC_AUTH_TOKEN` is set.
- Include relevant error output or the raw response for debugging.

---

## Step 3: Present the results

### Output rules

- Present the Grounded Result (from `choices[0].message.content`) **as-is**. Preserve its formatting.
- **Do not modify the Grounded Result text or intersperse your own content with it** — no added analysis, interpretation, commentary, or follow-up searching inline with the result.
- **Insert inline citation markers** (e.g., `[1]`, `[2]`) at the end of each supported text segment, as described in Step 2.3. This is the only permitted modification to the Grounded Result text.

### Inline citations in the Grounded Result

Insert citation markers directly into the Grounded Result text at the positions indicated by `groundingSupports`. Example output:

```
Cornell University is widely recognized as a distinguished Ivy League
institution with a unique public-private character, serving as New York's
federal land-grant university.[1][2] This distinct status contributes to
its broad academic scope and commitment to public engagement across
various fields of knowledge.[2]
```

### Search Suggestions (when present)

If `webSearchQueries` is present, display them **immediately after** the Grounded Result under a `## Search Suggestions` heading, exactly as returned:

```
## Search Suggestions
- query one
- query two
```

Omit this section if no Search Suggestions are present.

### Sources (when available)

After the Search Suggestions (or after the Grounded Result if no suggestions), add a `## Sources` heading.

For each entry in `groundingChunks`, display all three fields: `title`, `domain`, and the full `uri`. The numbers must correspond to the inline citation markers used in the text. Format each source as:

```
[index] title (domain)
    uri
```

Example:

```
## Sources
[1] wikipedia.org (wikipedia.org)
    https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG01p6km6QF2eDrt9ZPqyYgD0n3cMKnuCB4YygpoqdGZncsbwvdMwuptEecOwbpWfeejovsMZqHgUGmoT_ZOZ1mvajDpAmsbbjoFOpw9YsQsGP6topznyoF2qvGHcpl66rD417b8D97z16e-5Gpxes=
[2] anthropic.com (anthropic.com)
    https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGreAd7WMBS-olPa2utmulVfxXjwuxdDL1FYUl13FI2t4pxUxp6vbXJN_Cl8WGUwIhM0jxIOTE3ttIanLBx7_YATUKbYlEjHBuCAHL5KHaHCaLPLkW9Xbkeb0AK4jloHIAT
[3] claude.com (claude.com)
    https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHHPspB_TC3Akc8e4yGkwL3dveCgltUUwVN3qh9u3eZJGAQM8ZdFsdoCjDQn_MHVLzKybeSzykPv9BwqpsEIZaHMoSlzVOxJOyy7dTHICFwJQxGBCltXT4VA6dytsqqfJpYUVtFWqFcBWAQvKl4_GZEAXJRTTrdU1MUVg==
```

Always show the full, untruncated URI. Do not shorten or omit any part of it.

De-duplicate entries that share the same `title`, `domain`, **and** `uri`. Entries from the same domain but with different redirect URIs are distinct sources (they point to different pages) and should be listed separately.

Omit this section if no citations are present.

---

## Compliance notes

This skill uses **Web Grounding for Enterprise** (`enterpriseWebSearch`), governed by the Service Specific Terms:

- **§20(k) "Grounding with Google Search"** defines the core terms for Grounded Results, Search Suggestions, and Links.
- **§20(l) "Web Grounding for Enterprise"** modifies §20(k) for enterprise use: all references to "Grounding with Google Search" become "Web Grounding for Enterprise", "Google's search engine" becomes "GCP's web index", and the 30-day data storage provision (§20k(ii)) is deleted — **no customer data is logged**.

### Definitions (from the Service Specific Terms)

- **Grounded Result**: The generated response in `choices[0].message.content`. It is generated using the prompt, any contextual information, and results from GCP's web index.
- **Search Suggestions**: The search queries in `webSearchQueries[]` that Google provides alongside Grounded Results. Must be displayed whenever present.
- **Links**: Any means to fetch web pages contained in a Grounded Result or Search Suggestion, including the opaque redirect URIs in `groundingChunks[].web.uri` and `annotations[].url_citation.url`, as well as the titles/labels provided with them.

### Display requirements

1. **Show the Grounded Result as-is** with inline citation markers. Do not modify it or mix in other content.
2. **Always show Search Suggestions when present.** Display the `webSearchQueries` strings exactly as returned, alongside the Grounded Result.
3. **Always show inline citations when grounding support data is present.** Use `groundingSupports` and `groundingChunks` to connect specific claims back to their sources.
4. **Show sources with their numbers, titles, domains, and full URIs.** The URIs in the response are opaque Google redirect URLs — they function as the Links defined in the terms. Display all three fields from each `groundingChunks` entry: `title`, `domain`, and the full untruncated `uri`.
5. **Grounded Results, Search Suggestions, and Links are intended to be used in combination.** Per the terms, it is a violation to extract or collect one or more of these components for another purpose (e.g., collecting Links to build an index, or using Links to identify pages for crawling/scraping).

### Use restrictions (from §20(k), as modified by §20(l))

- **No caching, copying, or training.** Do not cache, copy, frame, syndicate, resell, analyze, train on, or otherwise learn from Grounded Results or Search Suggestions.
- **No click/link tracking.** Do not implement click tracking, Link-tracking, or other monitoring of Grounded Results or Search Suggestions.
- **Limited storage of Grounded Result text.** The text of Grounded Results (excluding Links) may be stored: (1) for up to 90 days for evaluating and optimizing display, or (2) in an end user's chat history for up to 6 months for displaying past conversations.
- **No IP claims.** Do not assert ownership rights in any intellectual property in Search Suggestions or Links in Grounded Results (excluding your own domain).

### Enterprise-specific context

- **No customer data logging.** The standard 30-day storage provision for debugging is deleted for Enterprise. Google does not log customer data.
- **Curated web index.** Enterprise uses a subset of Google Search, selected for regulated industries. Fast-changing content updates every ~6 hours; the full index refreshes every ~24 hours. Coverage may be narrower than standard Google Search grounding.

---

## Credits

Original skill author: **Jai Chandnani** ([@jaichandnani](https://github.com/jaichandnani)), Cornell AI Hub.
