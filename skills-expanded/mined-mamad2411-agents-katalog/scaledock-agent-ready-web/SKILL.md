---
name: scaledock-agent-ready-web
description: >-
  Make a ScaleDock website agent-ready with no-JS HTML, robots.txt AI rules, llms.txt, markdown twins,
  JSON-LD, api-catalog, WebMCP and declared content rights. Use when preparing a marketing site, docs
  site or web app for AI agents, AI crawlers and answer engines, or auditing one for agent readiness:
  serving .md twins and Accept: text/markdown negotiation with Vary: Accept, publishing /llms.txt,
  writing per-crawler robots.txt rules, adding a schema.org JSON-LD @graph, publishing
  /.well-known/api-catalog (RFC 9727), mirroring HTTP endpoints as WebMCP tools, publishing an A2A
  Agent Card, declaring AI usage and licensing with aipref Content-Usage, Content-Signal, RSL and
  TDMRep, verifying bots with Web Bot Auth instead of User-Agent strings, sitemaps and security.txt,
  and removing hidden instructions aimed at agents. Triggers: agent-ready website, AI-ready site,
  agent readiness audit, markdown for agents, text/markdown, llms.txt, AI crawler policy, GEO, AEO.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
---

# ScaleDock agent-ready web

A website that an AI agent can read, cite, call and respect without a browser: every page means the same thing as HTML, as markdown and as structured data, its APIs and agent tools are discoverable, and its rules for crawlers and content use are explicit. The spec skills carry the rules of each standard; this skill says which ones apply, in what order, and how they fit the ScaleDock stack.

**Follow the workflow below step by step.** Load the reference a step names when you reach that step. Take framework mechanics (Next.js rewrites, headers, route handlers) from the installed docs and `scaledock-repo-standard`; don't restate or improvise them.

## Inputs (fill in, or ask before starting)

- Site: the hosts (each scheme, host and port), the surfaces (`marketing`, `docs`, `app`) and the framework. Next.js is the default, per `scaledock-repo-standard`.
- Page types: the templates that carry meaning (home, product, pricing, article, docs page, changelog) and one sample URL for each.
- Content-rights policy: for each use (search, AI input such as grounding and retrieval, AI training) whether it is allowed, per crawler where it differs, and whether any use is licensed or paid.
- APIs: the public HTTP APIs and their OpenAPI documents, or none.
- Agent skills: what the site offers agents beyond reading (search, booking, quotes, support), or none.
- Security contact: the vulnerability reporting address and policy URL.

## Skills to install

```bash
npx skills add ScaleDockHQ/scaledock-skills --skill robots-txt --skill llms-txt --skill http-semantics --skill schema-org --skill json-ld --skill well-known-uris --skill sitemaps --skill security-txt --skill web-bot-auth
npx skills add ScaleDockHQ/scaledock-skills --skill aipref --skill content-signals --skill rsl --skill tdmrep
```

Add `webmcp` when the site exposes in-page tools, `a2a` when it offers agent skills, and `owasp-llm` for the prompt-injection review (`npx skills add ScaleDockHQ/scaledock-skills --skill <name>`). `scaledock-http-api` owns the APIs themselves and `scaledock-repo-standard` owns the app layout, the markdown routes and their caching.

## Invariants

1. **The spec skills win on protocol details.** File formats, header syntax, matching rules and version postures come from each spec skill. Do not restate them in the app; link the skill in code review.
2. **All meaning is in the first HTML payload.** Text, links, prices, dates and JSON-LD are in the server's first HTML response; JavaScript only enhances. An agent that does not run scripts sees the whole page.
3. **One explicit AI policy in robots.txt.** `/robots.txt` names each AI crawler token the policy treats differently, per the `robots-txt` crawler table, and every crawler-specific group repeats the `*` rules it should keep. Extension lines (`Content-Signal`, RSL `License`) sit inside the group they apply to.
4. **Content rights say the same thing everywhere.** One policy, expressed as the `aipref` `Content-Usage` header, `content-signals` lines, an `rsl` license where use is licensed or paid, and `tdmrep` reservations where text and data mining is reserved. No channel contradicts another. Follow each skill's draft posture before emitting its syntax.
5. **Every page has a markdown twin.** The same content is served at a `.md` URL and to `Accept: text/markdown` on the page URL, as `Content-Type: text/markdown; charset=utf-8` (RFC 7763 § 2 requires `charset`) with `Vary: Accept` on every negotiated response (RFC 9110 § 12.5.5), and is linked with `rel="alternate" type="text/markdown"`. `/llms.txt` maps the site per `llms-txt`.
6. **Structured data is one JSON-LD `@graph` per page.** Schema.org nodes (Organization, WebSite, WebPage and the page's main entity) with stable `@id`s, valid per `schema-org` and `json-ld`, and true to the visible content.
7. **APIs are discoverable.** Sites with public APIs serve `/.well-known/api-catalog` as `application/linkset+json` linking each API's OpenAPI document and docs, and answer `HEAD` with a `Link` header carrying `rel="api-catalog"` (RFC 9727 § 2, § 4.2).
8. **Agent tools mirror plain HTTP.** Every WebMCP tool calls an HTTP endpoint that a non-browser agent can call with the same inputs and permissions; WebMCP adds no capability of its own. Where the site offers agent skills, an A2A Agent Card describes them (`a2a`).
9. **Bots are identified by signatures, not User-Agent strings.** Bot-specific treatment (allow-listing, rate limits, paid access) depends on a verified `web-bot-auth` signature or the operator's published verification method; the User-Agent is only a hint, because any client can send any value.
10. **Discovery basics are present.** A sitemap per `sitemaps`, referenced from robots.txt, and an unexpired `/.well-known/security.txt` per `security-txt`.
11. **Nothing is hidden from humans.** No instructions addressed to agents in hidden text, HTML comments, `aria-hidden` or off-screen elements, and no content served only to bots. Agents and people get the same meaning; hidden instructions are prompt injection (`owasp-llm`, LLM01).

## Workflow

1. **Set the inputs and install the skills.** Fill in the inputs, install the skills above, and read the Invariants of each.
   ✓ Every page type has a sample URL, and the content-rights policy is a written table of use by crawler.
2. **First payload.** Render every page type on the server (static or server rendering in Next.js) and move any content that appears only after hydration into the first response.
   -> [`references/checklist.md`](references/checklist.md) (first payload)
   ✓ `curl` of each sample URL, with no JavaScript, contains its main heading, body text, primary links and JSON-LD.
3. **robots.txt and sitemap.** Write the groups from the policy table using the documented crawler tokens, add the `Sitemap` line, and add `Content-Signal` and RSL `License` lines in the groups they apply to.
   ✓ Each sample URL gets the intended allow or disallow for each named token under longest match, and the file is `text/plain` with a 2xx on every host.
4. **Content rights.** Express the same policy in every channel the policy uses: the `Content-Usage` header, `Content-Signal`, the RSL license document and its associations, and `/.well-known/tdmrep.json` or the TDMRep headers.
   ✓ A table of use by channel shows the same answer in every cell of a row.
5. **Markdown twins and llms.txt.** Serve a `.md` twin of each page, negotiate `Accept: text/markdown` on the page URL, add the alternate link, set caching, and publish `/llms.txt` linking the twins.
   -> [`references/content-negotiation.md`](references/content-negotiation.md)
   ✓ For each sample URL, the HTML response, the negotiated markdown and the `.md` URL carry the same content, and every negotiated response has `Vary: Accept`.
6. **Structured data.** Emit one JSON-LD `@graph` per page with stable `@id`s that link the site-wide nodes to the page's main entity.
   ✓ Each sample page has exactly one JSON-LD graph, it parses, and every value matches the visible page.
7. **APIs and agent tools.** Publish `/.well-known/api-catalog` for the public APIs, register WebMCP tools only over existing HTTP endpoints, and publish the A2A Agent Card when the site offers agent skills.
   ✓ `HEAD /.well-known/api-catalog` returns the `Link` header, each WebMCP tool names the endpoint it calls, and the Agent Card validates per `a2a`.
8. **Bot identity.** Verify Web Bot Auth signatures at the edge before any bot-specific allow or limit, and sign the site's own outbound fetchers.
   ✓ No rule grants bot treatment on the User-Agent alone.
9. **Security and transparency.** Publish `security.txt`, then search templates and content for text aimed at agents that people cannot see.
   ✓ `security.txt` has `Contact` and a future `Expires`, and the hidden-instruction search finds nothing.
10. **Verify.** Run every check in the checklist against production or a preview deployment, and the Verify lists of the spec skills you installed.
    -> [`references/checklist.md`](references/checklist.md)
    ✓ Every check passes or has a written reason it does not apply.

## Verify before done

- [ ] Every item in the Verify lists of the installed spec skills passes.
- [ ] Each sample URL fetched without JavaScript contains its full meaning and one JSON-LD `@graph`.
- [ ] `/robots.txt` names each AI token the policy treats differently, with the `Sitemap` line, on every host.
- [ ] The content-rights table gives the same answer in every channel.
- [ ] Each sample URL has a `.md` twin and answers `Accept: text/markdown` with `text/markdown; charset=utf-8` and `Vary: Accept`.
- [ ] `/llms.txt` resolves and links the twins.
- [ ] `/.well-known/api-catalog` answers `GET` and `HEAD` (when the site has public APIs).
- [ ] Every WebMCP tool has an HTTP equivalent, and the Agent Card exists where agent skills are offered.
- [ ] No bot rule trusts the User-Agent alone.
- [ ] `security.txt` is unexpired, and no hidden instruction to agents exists.
- [ ] `pnpm verify` passes.

## Reference index

- **[`references/checklist.md`](references/checklist.md)**: one `curl`-based check per invariant, with the expected result. Load for steps 2 and 10.
- **[`references/content-negotiation.md`](references/content-negotiation.md)**: markdown twins in detail: URL scheme, `Accept` negotiation, `Vary`, caching, alternate and canonical links, and 406 versus falling back to HTML. Load for step 5.
