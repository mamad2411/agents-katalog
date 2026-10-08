---
name: vehicle-valuation
description: Use when a UK motor claim needs a pre-accident vehicle valuation, market advert evidence pack, guide-value challenge, valuation explanation, dispute response, import/no-guide valuation, Autotrader comparable research, or internal EVA/guide screenshot interpretation.
---

# Vehicle Valuation

Prepare evidence-led UK vehicle valuations for Collision Engineers. Outputs are AI-assisted drafts until a named human signs off.

## Modes

| Mode | Use for | Load |
| --- | --- | --- |
| `market-valuation` | Assess a defensible retail pre-accident value from live market evidence. | `docs/reference/skill-material/vehicle-valuation/valuation-methodology.md`, `docs/reference/skill-material/vehicle-valuation/autotrader-search.md` |
| `evidence-pack` | Render the valuation report and advert evidence pack PDFs. | `docs/reference/skill-material/vehicle-valuation/report-style.md`, `docs/reference/skill-material/vehicle-valuation/example-outputs.md`, `src/skills/ce-house-style/` |
| `valuation-explanation` | Explain an assessed value to a client, solicitor, insurer, or engineer. | `docs/reference/skill-material/vehicle-valuation/external-wording.md`, `docs/reference/skill-material/vehicle-valuation/report-style.md` |
| `dispute-response` | Respond to CAP/Cazana/Glass's/HPI, guide-value, settlement, or no-guide/import challenges. | `docs/reference/skill-material/vehicle-valuation/valuation-methodology.md`, `docs/reference/skill-material/vehicle-valuation/authoritative-sources.md` |

For internal valuation-system screenshots, also load `docs/reference/skill-material/vehicle-valuation/eva-screenshot-intake.md`.
For commercial vehicles or VAT questions, load `docs/reference/skill-material/vehicle-valuation/vat-and-commercial-vehicles.md`.

## Required Inputs

- Registration, make/model/derivative, mileage, year or first registration date, body, fuel, transmission, and engine/power detail.
- Claim or matter reference before rendering PDFs.
- Internal guide value only when the user supplies it or it is visible in a screenshot. Do not ask for a guide value in market-only/no-guide/import work.

## Workflow

1. Extract vehicle facts from typed input or supplied screenshots.
2. Choose `guide_supported` only when a usable guide value is supplied or visible; otherwise use `market_only`.
3. Search Autotrader nationally by default for comparable retail adverts.
4. Select favourable but defensible comparables and record material differences.
5. Build and validate the JSON payload.
6. Render PDFs only when the matter reference is present and comparable evidence is sufficient.

Render commands:

```powershell
python tools/vehicle-valuation/render_report.py payload.json
python tools/vehicle-valuation/render_evidence_pack.py payload.json
```

Validate payloads directly with:

```powershell
python tools/vehicle-valuation/validate_evidence_pack.py payload.json
```

## Governance

Expert class. The valuation, explanation, dispute response, report, and evidence pack remain AI-assisted drafts until a named human signs off. Do not include internal workflow terms, guide strategy, or mode labels in external wording. No autonomous external send.
