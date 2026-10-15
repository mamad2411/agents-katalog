---
name: refurbish-demos
description: "Upgrade demo agent knowledge — clears old summaries, scrapes real pages via MCP Tavily (advanced mode), falls back to WebFetch, fixes icons, republishes. Pass campaignId or 'all-sent' as parameter."
---

# Refurbish Demos

Upgrade demo agent knowledge from old AI-written summaries to properly scraped page content with real sourceUrls. Each knowledge item becomes a URL-type entry with the actual page URL, so the chatbot can cite specific pages in its answers.

**Parameter:** `campaignId` (CRM campaign ID) or `all-sent` (all demos where outreach was sent)

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> Refurbish Demos — upgrading knowledge
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## Environment

Read from `.env` in the working directory:
- `NUXT_MCP_DEMO_TOKEN` — Bearer token for InboxMate MCP (contains `#` character — use curl, not Python urllib)
- `PSQUARED_CRM_TOKEN` — Bearer token for Twenty CRM
- `EMAIL_DRAFT_ONLY_BEARER` — Bearer token for notification service (used in Option B: all-sent)

**MCP endpoint:** `https://app.psquared.dev/api/mcp`
**CRM endpoint:** `https://crm.psquared.dev/graphql`
**Demo API:** `https://app.psquared.dev/api/demo/{demoId}`
**Supabase project:** `fevtfywriufbqnvbgyrm` (for direct DB queries when needed)
**Demo account ID:** `8942a6e5-91cb-4c5d-8ef5-98cfe7945620`

### MCP Call Template

All MCP calls use this pattern (use curl, NOT Python urllib — the token contains `#`):

```bash
curl -s --max-time 120 -X POST https://app.psquared.dev/api/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NUXT_MCP_DEMO_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"TOOL_NAME","arguments":{...}}}'
```

### Available MCP Tools

| Tool | Purpose |
|---|---|
| `cleanup_agent` | Wipe all knowledge from agent's buckets + delete orphaned buckets in demo account |
| `clear_bucket` | Remove all items from a specific bucket |
| `scrape_and_build_knowledge` | Scrape URLs via Tavily (advanced mode), create URL-type knowledge items. Max 10 URLs per call. Returns `{ created: [], failed: [] }` |
| `add_to_bucket` | Manually add knowledge item. If `sourceUrl` is provided, creates URL-type entry |
| `get_agent` | Get agent config (check knowledgeBucketIds, buttonIcon) |
| `list_bucket_items` | List items in a bucket (verify results) |
| `update_widget_style` | Fix buttonIcon or other widget config |
| `publish_agent` | Republish agent (required after knowledge changes) |

---

## PHASE 1 — Build Work List

> **Announce:** `[1/4] Building work list...`

### Option A: By campaign ID

Query CRM for opportunities in the campaign:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d "{\"query\":\"{ opportunities(filter: { campaignId: { eq: \\\"CAMPAIGN_ID\\\" } }, first: 150) { edges { node { id name demoStatus demoUrl { primaryLinkUrl } company { id name domainName { primaryLinkUrl } } } } } }\"}"
```

### Option B: All sent demos

Get sent email drafts from notification service, extract demo IDs, then look up agents:

```bash
curl -s "https://notifications.psquared.dev/drafts?status=SENT&draftType=outreach&pageSize=200" \
  -H "Authorization: Bearer $EMAIL_DRAFT_ONLY_BEARER"
```

Extract `demoUrl` from each draft's variables, parse the `?id=` param to get demoId.

### For each demo ID, fetch agent info:

```bash
curl -s https://app.psquared.dev/api/demo/DEMO_ID
# Returns: { agentId, companyName, companyDomain, ... }
```

Then get bucket ID:
```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_agent","arguments":{"agentId":"AGENT_ID"}}}
```
Extract `knowledgeBucketIds[0]`.

**Filter out:** `demoStatus` = `SKIP_*`, `DISQUALIFIED`. Skip demos without `companyDomain`.

**Build:** `[ { companyName, companyDomain, agentId, bucketId, demoId } ]`

Announce: `Found N demos to refurbish.`

---

## PHASE 2 — Discover Pages Per Company

> **Announce:** `[2/4] Discovering pages to scrape...`

For each company, determine the best URLs to scrape.

### Quick approach (batch mode, ~5 URLs per company):

Use the domain + common German business site patterns:

```
https://www.{domain}/
https://www.{domain}/kontakt/
https://www.{domain}/ueber-uns/
https://www.{domain}/leistungen/
https://www.{domain}/impressum/
```

**Important:** Split into 2 batches of 2-3 URLs per MCP call. Tavily advanced mode takes ~5-30s per URL. A single call with 5 URLs can hit server timeouts (120s).

### Thorough approach (per-company, ~6-8 URLs):

WebFetch the homepage, extract real nav/footer links, then scrape those. More reliable but slower.

Some "Seite nicht gefunden" / 404 pages will be scraped — that's OK, they're low-content and won't hurt the RAG. The homepage + whatever real pages exist is what matters.

---

## PHASE 3 — Clear & Rebuild Knowledge

> **Announce:** `[3/4] Rebuilding knowledge for N demos...`

Process **one company at a time**:

### Step 3a: Wipe existing knowledge

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cleanup_agent","arguments":{"agentId":"AGENT_ID"}}}
```

This clears the agent's buckets AND deletes all orphaned buckets in the demo account (from old demo creation flow). First call handles the global orphan cleanup.

### Step 3b: Scrape via MCP (batch 1)

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"scrape_and_build_knowledge","arguments":{"bucketId":"BUCKET_ID","urls":["https://www.domain.de/","https://www.domain.de/kontakt/"]}}}
```

### Step 3c: Scrape via MCP (batch 2)

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"scrape_and_build_knowledge","arguments":{"bucketId":"BUCKET_ID","urls":["https://www.domain.de/ueber-uns/","https://www.domain.de/leistungen/","https://www.domain.de/impressum/"]}}}
```

### Step 3d: Handle failures with WebFetch fallback

For each URL in the `failed` arrays:

1. WebFetch the URL
2. If content returned, call `add_to_bucket` with `sourceUrl` set:

```json
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"add_to_bucket","arguments":{"bucketId":"BUCKET_ID","title":"Page Title","content":"[full page text]","sourceUrl":"https://domain.de/kontakt/"}}}
```

**Content rules:**
- Full page text, not a summary
- Keep headings, lists, structure
- Remove nav, footer, cookie banners
- Max 20,000 characters
- `sourceUrl` MUST be the actual page URL (creates URL-type knowledge entry)

### Step 3e: Fix button icon if broken

Valid icons: `messageCircle`, `messageSquare`, `sparkles`, `support`, `help`, `inboxmate`, `heart`, `zap`, `globe`, `wave`, `brain`, `lightbulb`, `compass`, `star`, `shield`, `robot`, `mascot`

Any other value (e.g. `shoppingBag`, `truck`, `home`, `car`, `music`) renders as a broken circle in the widget. Fix to `messageCircle`:

```json
{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"update_widget_style","arguments":{"agentId":"AGENT_ID","buttonIcon":"messageCircle"}}}
```

### Step 3f: Republish agent

```json
{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"publish_agent","arguments":{"agentId":"AGENT_ID"}}}
```

> **Log per company:** `✓ {companyName}: {N} items created, {M} failed → republished`

---

## PHASE 4 — Report

> **Announce:** `[4/4] Refurbish complete.`

Print summary table:

```
| Company | Domain | Items | Failed | Icon Fixed | Status |
|---------|--------|-------|--------|------------|--------|
| Schuh Marke GmbH | schuh-marke.de | 5 | 0 | yes | ✓ |
| Mainfilm | mainfilm.tv | 5 | 0 | no | ✓ |
```

Totals:
- Companies processed: N
- Knowledge items created: N
- Failed URLs: N (fell back to WebFetch: N, completely failed: N)
- Icons fixed: N
- Tavily credits used: ~N (2 credits per 5 URLs at advanced mode)

---

## Batch Script

For large batches (100+ demos), use the Python batch script instead of processing one-by-one from Claude:

```bash
python3 -u scripts/refurbish-all.py < /tmp/worklist.json > /tmp/refurbish.log 2>&1
```

The script at `claude-overlord-folder/scripts/refurbish-all.py`:
- Uses curl (not urllib) for MCP calls — handles `#` in auth token
- Splits URLs into 2 batches of 2-3 to avoid server timeouts
- Processes sequentially with 1s pause every 5 agents
- Logs progress to stdout (use `-u` flag for unbuffered output)
- Input: JSON array of `[{company_name, company_domain, agent_id, bucket_id}]`

---

## Known Issues & Workarounds

### Tavily advanced mode timeouts
Tavily `extract_depth: 'advanced'` takes up to 30s per URL. Batch 5 URLs in one MCP call = 150s, which exceeds server timeout. **Always split into batches of 2-3 URLs.**

### Fallback API key
If primary Tavily key runs out, set `NUXT_TAVILY_FALLBACK_API_KEY` in agenthub `.env`. Auto-switches on 429/402 errors.

### "Seite nicht gefunden" pages
Some scraped pages will be 404s (the generic URL patterns don't exist on every site). These are low-content and won't affect RAG quality. The homepage + real pages provide the value.

### Bucket name mismatches
Old demo creation flow sometimes linked wrong-named buckets to agents (e.g. "Autohaus Freier Wissensbasis" on a Hinzmann Elektrotechnik agent). The content is correct after refurbish — the bucket name is cosmetic. Can be fixed via SQL if needed.

### Orphaned buckets
Old demo creation left ~160 orphaned "Wissensdatenbank" buckets not linked to any agent. `cleanup_agent` deletes these. For large batches, clean up via SQL first (faster):

```sql
DELETE FROM knowledge_bucket_chunks WHERE bucket_item_id IN (
  SELECT kbi.id FROM knowledge_bucket_items kbi
  JOIN knowledge_buckets kb ON kb.id = kbi.bucket_id
  WHERE kb.account_id = '8942a6e5-91cb-4c5d-8ef5-98cfe7945620'
  AND kb.id NOT IN (SELECT unnest(knowledge_bucket_ids) FROM agents WHERE account_id = '8942a6e5-91cb-4c5d-8ef5-98cfe7945620')
);
-- Then delete items, then buckets (same pattern)
```

### Content length limit
Knowledge entries allow up to 20,000 characters (was 10,000, fixed 2026-03-26). Tavily advanced mode returns more content — large pages may get truncated at 20K.

### Cross-contamination
Audit showed only 1 true case out of 152 sent demos (Dachdeckermeister Hoffmann had DBM Metallbau content). Refurbish fixes this by clearing and re-scraping based on the correct domain from the demo page.
