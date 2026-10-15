---
name: tpex-market-rules
description: Taiwan Stock Exchange (TPEx, 櫃買中心) market and broker-system knowledge grounded in official TPEx documents. Use for 上櫃, 興櫃, TPEx stock trading, bonds and negotiated trading, TPEx ETFs and derivatives, margin trading, securities lending, odd lots, FIX, host connectivity, market data, file formats, backup systems, and TPEx broker computer-operation manuals. Keep TPEx scope distinct from TWSE centralized-market and TAIFEX derivatives rules.
---

# TPEx Market Rules

Use official TPEx documents to answer market-rule, broker-operation, protocol, and system-design questions. Preserve the owning market and system in every answer.

Primary source: https://dsp.tpex.org.tw/web/system/mainboard.php

## Source routing

Read `references/source-map.md` before researching or answering. Route by system instead of treating all TPEx products as one market:

- 上櫃股票: 等價交易、零股、信用、借券、當沖、ETF, FIX, host connectivity, reports, and files.
- 興櫃股票: dealer quotation/trading and its separate back-office operations.
- 債券: dealer-negotiated and bond-system rules; do not infer them from stock rules.
- 衍生性商品: TPEx OTC or TPEx-operated systems; do not confuse them with TAIFEX contracts.
- 行情與基礎設施: market-data transmission, information integration, backup, and co-location.

Use `references/source-inventory.json` to audit every discovered storage link. After the corpus is downloaded, use `references/source-manifest.json` for file hashes, `references/manual-index.md` and `references/topic-map.md` for source routing, `references/manual-domain-matrix.md` for whole-corpus ownership, and `references/rule-cards.md` for source-grounded retrieval anchors.

For cross-layer system work, read `references/broker-exchange-integration.md`, `references/market-data-format-cards.md`, and `references/system-design-checklists.md`. Use `references/tpex-broker-mind-map.md` when a question spans several TPEx systems. `references/knowledge-qa-100.md` and `references/expert-self-exam.md` are audited coverage artifacts, not substitutes for current official text.

## Workflow

1. Identify system, product, actor, account, lifecycle stage, and protocol.
2. Open the official TPEx entry and locate the current document for that system. Browse when current rules, versions, dates, or URLs matter.
3. Prefer the document page or stable category URL over an attachment URL as the canonical source. Treat attachments as version snapshots.
4. Verify exact codes, field lengths, session times, order restrictions, eligibility, and exceptional procedures against the current document.
5. Answer with scope, operational meaning, implementation impact, official document title, version/update date, and URL.
6. If a rule resembles TWSE, do not assume equivalence. Check both official sources and label differences explicitly.

## Guardrails

- Treat a 403 response sometimes returned by the portal as access behavior, not proof that a document does not exist. Use official TPEx announcements or official-domain search results to recover the document location.
- Distinguish business rules from protocol encodings. A field value does not by itself establish customer eligibility or settlement treatment.
- State uncertainty when only an older announcement or attachment is available.
- For legal, compliance, production connectivity, and live-trading decisions, verify the latest official publication and recommend confirmation with the relevant exchange or broker operations contact.

## Maintenance

Run from this skill directory. Refresh the official link inventory without downloading attachments:

```bash
uv run --with requests --with beautifulsoup4 python scripts/download_tpex_documents.py --inventory-only --insecure
```

Refresh the selected document corpus and manifest:

```bash
uv run --with requests --with beautifulsoup4 python scripts/download_tpex_documents.py --insecure
```

Regenerate searchable plain text and the extraction report:

```bash
uv run --with pypdf --with python-pptx --with openpyxl --with xlrd --with odfpy python scripts/extract_tpex_text.py
```

Rebuild all indexes, guides, cards, QA, and audits:

```bash
uv run python scripts/rebuild_knowledge.py
```

Use `--insecure` only for the official TPEx domains recorded by this skill. Python/OpenSSL currently rejects the site's legacy certificate because it lacks Subject Key Identifier, while the system TLS client accepts it. Keep SHA-256 hashes and official-domain checks enabled; never reuse this flag for arbitrary hosts.
