---
name: taifex-market-rules
description: Taiwan Futures Exchange (TAIFEX, 期交所) rules and technical-system knowledge grounded in official sources. Use for Taiwan futures and options, contracts, trading sessions, order and execution reports, TMP/FIX, market data, positions, margins, risk controls, clearing, settlement, SPAN, member connectivity, testing, file transfer, and TAIFEX technical documents. Keep TAIFEX derivatives rules distinct from TWSE and TPEx securities-market rules.
---

# TAIFEX Market Rules

Use official TAIFEX technical documents, market rules, and clearing sources to answer derivatives trading and system questions. Do not reduce a futures lifecycle to securities-market concepts.

Primary technical source: https://www.taifex.com.tw/cht/8/techDocs

## Source routing

Read `references/source-map.md` first. Select all source bundles needed by the question:

- Trading connectivity: TMP, FIX, file transfer, session, recovery, kill switch, COD, and connection applications.
- Market data: aggregate feeds, tick-by-tick feeds, custom products, and test data.
- Trading rules: contracts, order rules, position limits, error correction, mass cancel, backup, and disruption handling.
- Clearing and risk: margin, positions, settlement, defaults, SPAN, clearing members, MTS/MTS WEB API, and OTC central clearing.
- Change and testing: technical briefings, scheduled tests, mock opening, and version migration.

After choosing a bundle, use `references/manual-index.md`, `references/topic-map.md`, and `references/manual-domain-matrix.md` to route into the 180-file corpus. Use `references/rule-cards.md` for source anchors, then read the full extracted text and original attachment. For architecture questions, also read `references/broker-exchange-integration.md`, `references/market-data-format-cards.md`, and `references/taifex-system-mind-map.md`. The QA and expert-exam files are audited coverage artifacts, not independent authority.

## Workflow

1. Identify product, contract, actor, account, trading session, position lifecycle, clearing lifecycle, and interface.
2. Choose the owning official source pages from `references/source-map.md`. Browse when current versions, dates, rules, schedules, or links matter.
3. Use detail-page `idx` URLs as stable manifest identities; treat versioned PDF links as snapshots.
4. Verify exact tags, binary fields, session transitions, sequence/recovery behavior, limits, margin treatment, and exceptional procedures in the current official document.
5. Answer with applicability, operational meaning, implementation effect, official document title, version/update date, and URL.
6. Explain whether an interface is socket-based TMP/FIX, market-data transport, SFTP/file exchange, MTS, or web API; do not call all of them “API”.

## Guardrails

- Do not use securities concepts such as cash settlement, margin purchase, or securities borrowing as substitutes for futures position and margin rules.
- Separate order/execution state from position, margin, and clearing state.
- Public specifications do not imply anonymous access to production or test systems; member credentials, network settings, sessions, and applications may be required.
- Mark older MTS materials as historical unless the current TAIFEX page confirms them.
- For legal, compliance, production connectivity, and live-trading decisions, verify the latest official publication and recommend confirmation with TAIFEX or the relevant futures/clearing member.

## Maintenance

Run from this skill directory. Refresh the official document inventory without downloading attachments:

```bash
uv run --with requests --with beautifulsoup4 python scripts/download_taifex_documents.py --inventory-only
```

Download the selected corpus and write SHA-256 manifests:

```bash
uv run --with requests --with beautifulsoup4 python scripts/download_taifex_documents.py
```

Regenerate searchable text and the extraction report:

```bash
uv run --with pypdf --with python-pptx --with openpyxl --with xlrd --with odfpy python scripts/extract_taifex_text.py
```

Rebuild all indexes, lifecycle guides, cards, QA, and audits:

```bash
uv run python scripts/rebuild_knowledge.py
```

If Python/OpenSSL rejects the legacy certificate on `activity.taifex.com.tw`, rerun with `--insecure-legacy-hosts`. The flag is restricted in code to the explicit TAIFEX legacy-host allowlist; official-host checks and SHA-256 manifests remain enabled. Do not generalize it to arbitrary hosts.
