---
name: business-registrations-licenses
description: >-
  Setting up a NEW business in India and the registrations/licences it needs: choosing the
  entity type (proprietorship, partnership, LLP, One Person Company, Private Limited) and
  obtaining PAN/TAN, GST registration (GSTIN), Udyam/MSME, Shops & Establishments,
  Professional Tax registration, Importer-Exporter Code (IEC), FSSAI and trade licences;
  bundles a PAN validator. Use for how to start or register a business, which licence or
  registration is needed, entity-type choice, or getting a GSTIN/Udyam/IEC/FSSAI. For
  recurring annual MCA/ROC filings after incorporation, use company-roc-compliance.
---

# Business registrations and licences (India)

Starting and legally operating a business in India means picking a structure and then obtaining the
registrations and licences that structure and activity require. This skill helps map the right set
and the order to get them — it does not submit applications or give legal advice.

> [!IMPORTANT]
> Requirements, fees and thresholds change, and several registrations are **state-specific** (Shops
> & Establishments, Professional Tax, trade licence) or **activity-specific** (FSSAI, IEC, sector
> permits). Never assert a current fee or threshold from memory. Confirm on the official portal for
> each (links in the reference). For incorporation and anything legal, recommend a CA/CS.

## Step 1 — choose the structure

The structure decides tax, compliance load, liability and how you raise money. Establish the user's
situation (solo vs partners, liability concern, funding plans, expected turnover) and lay out the
trade-offs:

| Structure | Good when | Compliance load | Liability |
|---|---|---|---|
| **Proprietorship** | Solo, small, simplest start | Lowest (no MCA) | Unlimited (personal) |
| **Partnership firm** | A few partners, low formality | Low (partnership deed, optional registration) | Unlimited |
| **LLP** | Partners wanting limited liability, services | Medium (MCA: Form 8/11) | Limited |
| **One Person Company (OPC)** | Solo founder wanting a company + limited liability | Medium (lighter company regime) | Limited |
| **Private Limited** | Funding/investors, scale, ESOPs | Highest (full Companies Act, see `company-roc-compliance`) | Limited |

Don't push a Pvt Ltd on someone who needs a proprietorship, or vice versa — match it to the plan.

## Step 2 — the registrations that follow

Read [`references/registrations-checklist.md`](references/registrations-checklist.md) for who issues
each, when it's mandatory, and the portal. The usual set:

- **PAN** (entity) and **TAN** (if deducting TDS) — Income Tax.
- **Incorporation** with MCA for LLP/OPC/Pvt Ltd (SPICe+ for companies, FiLLiP for LLP).
- **GST registration (GSTIN)** — mandatory above the turnover threshold, for inter-state supply, and
  for e-commerce sellers regardless of turnover (verify current triggers).
- **Udyam (MSME) registration** — free, quick, unlocks MSME benefits (priority, delayed-payment
  protection, scheme eligibility). Almost always worth doing.
- **Shops & Establishments registration** — **state** law; most commercial premises need it.
- **Professional Tax registration** — **state**; PTEC/PTRC where PT applies (see
  `payroll-statutory`).
- **Bank current account** — needs the above as KYC.
- **EPF/ESI registration** — once headcount crosses the thresholds (see `payroll-statutory`).

## Step 3 — activity-specific licences

Only if the activity needs them:

- **FSSAI** — any food business (basic / state / central by scale).
- **Importer-Exporter Code (IEC)** — to import or export (DGFT).
- **Trade licence** — from the local municipal body, for many premises-based trades.
- **Sector permits** — e.g. drug licence, pollution-control consent, professional councils, RBI/SEBI
  registrations for regulated finance, etc. Flag these; they're specialised.

## Deterministic helper — validate a PAN with the script

This skill bundles [`scripts/pan.py`](scripts/pan.py). When a user gives you a PAN, validate it
and read its entity type with the script rather than eyeballing the pattern — the 4th character
tells you whether the holder is an individual, company, firm/LLP, trust and so on, which often
decides what they can register for.

```bash
python scripts/pan.py AAPFU0939F   # → {"valid": true, "entity_type": "Firm / LLP"}
```

(PAN has no public checksum, so this validates the published structure and decodes the entity
character; for a GSTIN, the `gst-compliance` skill's `gst_calc.py` checks the full check digit.)

## How to help, concretely

- **"How do I start X in India?"** — recommend a structure with reasoning, then produce an ordered
  checklist: incorporate → PAN/TAN → GST (if triggered) → Udyam → Shops & Est → activity licences →
  bank account → EPF/ESI when hiring. Mark each with its authority and "verify current threshold".
- **"Which licence do I need to sell online / open a café / export?"** — map the activity to the
  specific set (e.g. online marketplace seller → GSTIN usually mandatory; café → FSSAI + trade
  licence + Shops & Est; exporter → IEC + GST LUT).
- **Documents** — list the typical documents each application needs so the user can assemble them.

## Guardrails

- Always ask the **state** (for Shops & Est, PT, trade licence) and the **activity** (for FSSAI/IEC/
  sector permits) before giving a definitive list.
- GST-registration triggers have several limbs (turnover, inter-state, e-commerce, RCM) — check all,
  don't answer on turnover alone.
- Mark fees and thresholds "verify"; recommend a CA/CS for incorporation and regulated sectors.
