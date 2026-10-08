# SKILL — Researcher

**Primary:** Topic research  
**Topic:** Repair the Daily Tweet Office — output was generic with no real news. Fix research: require dated headlines with URLs from search_web, no theme threads. Then I'll run the flow again. - "Called Btcprice Fetches Bitcoin" (id: called_btcprice_fetches_bitcoin, status: ready, errors: 0) - "Called Ethprice Fetches Ethereum" (id: called_ethprice_fetches_ethereum, status: ready, errors: 0) [END CONTEXT]

## Triggers
- Topic: Repair the Daily Tweet Office — output was generic with no real news. Fix research: require dated headlines with URLs from search_web, no theme threads. Then I'll run the flow again. - "Called Btcprice Fetches Bitcoin" (id: called_btcprice_fetches_bitcoin, status: ready, errors: 0) - "Called Ethprice Fetches Ethereum" (id: called_ethprice_fetches_ethereum, status: ready, errors: 0) [END CONTEXT]
- search_web

## Execution steps
1. Query plan
2. search_web x3
3. Normalize table
4. DELIVERABLE

## Output template
```markdown
DELIVERABLE
summary: Research pack for curator
content:
| # | Title | Source | Date | URL | Why it matters |
|---|-------|--------|------|-----|----------------|
| 1 | ... | ... | ... | ... | ... |
```
