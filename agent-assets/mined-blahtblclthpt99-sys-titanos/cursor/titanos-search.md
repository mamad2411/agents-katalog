---
description: Global search — instant local index across core TitanOS domains
alwaysApply: true
---

# SEARCH

Global search (Cmd/Ctrl+K desktop, Search on mobile) must feel instant and cover the operating system — not just nav labels.

## Index (required)

| Domain | Source |
|---|---|
| Jobs | Entity cache / warm index |
| Trips | Driver Hub deliveries + shifts (`searchDeliveries`) |
| Messages | Local DM threads + bodies |
| Invoices | Entity cache / warm index |
| Customers | Entity cache / warm index |
| Voice transcripts | `voiceTranscriptStore` (dock / AI mic) |
| Files | Customer files + expense receipts |
| Analytics | Static catalog + `/analytics` deep links |
| Settings | Settings section catalog |
| AI conversations | `aiConversationStore` rolling log |

## Latency

- Keystrokes query **sync** local memory (+ persisted snapshot) — never await network on each character  
- Warm / prefetch / `fetchEntity` ingest runs in the background  
- Cap result list; score + fuzzy; prefer recent entity docs  

## Honesty

- Hits reflect indexed / cached data — not a guarantee of full remote warehouse search  
- Empty index (first launch offline) still returns Pages / Actions / Settings / Analytics catalogs  

## Definition of done

Incomplete if Jobs/Customers/Invoices only appear as page nav, if search awaits Supabase per keystroke, or if AI/voice leave nothing searchable after use.
