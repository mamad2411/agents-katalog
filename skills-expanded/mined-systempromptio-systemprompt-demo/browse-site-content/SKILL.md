# Browse the Live Site

Answer from the **live systemprompt.io site** — the documentation and blog as
published right now — rather than from documentation compiled into the hub.
The bridge is two governed MCP tools that read the site's own markdown
endpoint and can reach nothing else.

## When to Use

Use this when someone asks about current site content: a specific
documentation page, a blog post, "what does your site say about X", or
anything where being up to date matters more than being fast. For a general
"what is systemprompt.io?" the compiled-in topics (`explain_systemprompt`) are
usually enough.

## How to Use

1. **List the live pages.** One call returns every public page with its
   section and slug:

   ```
   mcp__systemprompt__list_site_pages {}
   ```

2. **Fetch the page(s) that answer the question.** The input is a section
   (`documentation` or `blog`) and a slug from the index — never a URL:

   ```
   mcp__systemprompt__fetch_site_page {"section": "documentation", "slug": "services/ai"}
   ```

   Fetch at most the two or three pages that actually bear on the question;
   each fetch is a governed, human-approved call.

3. **Digest, don't dump.** Summarise what the page says in terms of the
   visitor's question, quote short passages where the wording matters, and end
   with the page's public URL (e.g. `https://systemprompt.io/documentation/services/ai`)
   so they can read it themselves.

4. **Say what you didn't find.** If the index has no page on the topic, say so
   and fall back to `mcp__systemprompt__search_docs` over the compiled-in
   topics rather than guessing.

## Why this egress is allowed

This deployment refuses general egress — `mcp__systemprompt__fetch_remote_docs`
exists precisely to be refused by the `tool_blocklist` policy, and the visitor
can watch that happen. The site bridge is the deliberate contrast: its input is
a `{section, slug}` pair validated against a strict grammar, the base URL is
fixed server-side, and there is no input that composes a URL on any other
host. Browsing is allowed because it cannot be steered — not because the
policy looked away. If a visitor asks why one fetch works and the other is
blocked, that is the answer, and demonstrating both back-to-back is a good
demo.

## Related

- `explain_systemprompt` — the compiled-in overview topics.
- `demonstrate_tool_rejection` — watch `fetch_remote_docs` be refused.
