---
name: us-gaap-asc805-business-combinations
description: "> US GAAP accounting for business combinations under ASC 805 (Business Combinations) and the related goodwill guidance in ASC 350 (Intangibles — Goodwill and Other). Covers the acquisition method — identify the acquirer, determine the acquisition date, recognize and measure the identifiable assets acquired, liabilities assumed and any non-controlling interest at fair value, and recognize goodwill or a bargain purchase gain — plus consideration transferred and contingent consideration, acquisition-related costs, the measurement period, step acquisitions, recognition exceptions, the definition of a business, in-process R&D, and subsequent goodwill impairment under ASC 350-20. Produces recognition conclusions, journal entries, and a reviewer brief. Issued as the US GAAP edition of the business-combinations topic; see ifrs3-business-combinations for the IFRS edition. MUST load alongside financial-reporting-workflow-base."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US
  category: financial-reporting
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/us-gaap-asc805-business-combinations"
  obligation: OTHER
---

# US GAAP Business Combinations — ASC 805 v0.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

**This is a content skill that loads on top of `financial-reporting-workflow-base`.** It supplies the recognition, measurement, presentation, and disclosure rules for business combinations under US GAAP, and the subsequent accounting for goodwill under ASC 350. The base supplies the two-layer output contract, the journal-entry format, and the self-checks.

**Standard currency.** ASC 805 as effective, incorporating ASU 2017-01 (clarifying the definition of a business), ASU 2017-04 (simplifying the goodwill impairment test by eliminating Step 2), ASU 2014-02 / 2014-18 (the private-company and not-for-profit goodwill and intangible alternatives in ASC 350-20-15-4 and 805-20-25-29), and ASU 2021-08 (contract assets and contract liabilities acquired in a business combination measured under ASC 606, not at fair value). Confirm no entity-specific industry guidance overrides.

**Scope.** ASC 805 applies to a transaction or other event in which an acquirer **obtains control of one or more businesses** (`ASC 805-10-15-3`). It does **not** apply to: the formation of a joint venture; the acquisition of an asset or group of assets that does **not** constitute a business (an asset acquisition under `ASC 805-50`); combinations of entities under common control (`ASC 805-50`); and combinations of not-for-profit entities, which follow `ASC 958-805`.

---

## Section 1 — Scope statement

This skill covers:

- The acquisition method of `ASC 805-10`, `805-20`, and `805-30` — the four steps.
- Consideration transferred at fair value, including contingent consideration and its subsequent measurement.
- Acquisition-related (transaction) costs.
- The recognition and measurement **exceptions** to the fair-value principle.
- The measurement period and retrospective measurement-period adjustments.
- Step (business combination achieved in stages) acquisitions and the remeasurement of a previously held equity interest.
- Bargain purchases.
- The definition of a business and the ASU 2017-01 screen test (asset acquisition vs. business combination).
- In-process research and development (IPR&D).
- Subsequent measurement of goodwill: the ASC 350-20 impairment-only model and the ASC 350-20 private-company/NFP amortization alternative.

This skill does NOT cover: asset acquisitions (`ASC 805-50`), common-control transactions (`ASC 805-50`), NFP combinations (`ASC 958-805`), consolidation procedures and the control assessment themselves (`ASC 810`), or pushdown accounting beyond a reference. It defers the IFRS treatment to `ifrs3-business-combinations`.

---

## Section 2 — Reference layer (Layer A): the acquisition method

Every business combination in scope is accounted for by applying the **acquisition method** (`ASC 805-10-05-4`, `805-10-25-1`). The method has four steps.

### Step 1 — Identify the acquirer — `ASC 805-10-25-4` to `25-5`

The acquirer is the combining entity that **obtains control** of the acquiree. Control is assessed under the consolidation guidance in **`ASC 810`** (`ASC 805-10-25-5`) — either the voting interest model (a controlling financial interest, generally > 50% of voting rights) or, for a variable interest entity, the primary-beneficiary model.

If `ASC 810` does not clearly identify the acquirer, apply the indicators in `ASC 805-10-55-11` to `55-15`: the entity transferring cash/assets or incurring liabilities is usually the acquirer; the entity issuing equity is usually the acquirer **but watch for a reverse acquisition** (the legal acquiree is the accounting acquirer); relative voting rights, the existence of a large minority interest, governing-body composition, senior management, and relative size. In a combination effected primarily by exchanging equity, also consider terms of the exchange.

> **⚑ AUDIT FLASH POINT — reverse acquisitions.** When the legal subsidiary (the entity issuing no shares, e.g. a private operating company merging into a public shell or SPAC) is the **accounting acquirer**, the accounting is inverted: the legal parent's financial statements are restated as a continuation of the legal subsidiary. Misidentifying the acquirer reverses which net assets are fair-valued and which carry over at book value. Document the `ASC 805-10-55-11`–`55-15` indicators and the SPAC/de-SPAC analysis.

### Step 2 — Determine the acquisition date — `ASC 805-10-25-6` to `25-7`

The acquisition date is the date the acquirer **obtains control** of the acquiree — generally the **closing date** on which the acquirer legally transfers consideration, acquires the assets, and assumes the liabilities (`ASC 805-10-25-6`). Control can be obtained on a date earlier or later than closing if so specified by written agreement (`ASC 805-10-25-7`); document the facts.

The acquisition date fixes the measurement date for fair values, the date the previously held interest is remeasured, and the start of the measurement period. It also determines which results are included in post-combination consolidated earnings.

### Step 3 — Recognize and measure identifiable assets, liabilities, and NCI — `ASC 805-20`

**Recognition principle** (`ASC 805-20-25-1`): as of the acquisition date, the acquirer recognizes, **separately from goodwill**, the identifiable assets acquired, the liabilities assumed, and any **non-controlling interest (NCI)** in the acquiree. To qualify, an item must meet the definition of an asset/liability in the conceptual framework at the acquisition date and be **part of the business combination** (not a separate transaction — `ASC 805-10-25-20` to `25-22`).

**Identifiable intangibles** are recognized apart from goodwill if they are **separable** OR arise from **contractual-legal** rights (`ASC 805-20-25-10`). Examples: customer relationships, trade names, technology, order backlog, non-compete agreements.

**Measurement principle** (`ASC 805-20-30-1`): identifiable assets acquired and liabilities assumed are measured at their **acquisition-date fair values** (per `ASC 820`).

**NCI measurement** (`ASC 805-20-30-1`): under US GAAP, NCI **must** be measured at its **acquisition-date fair value** — there is **no proportionate-share option**. This forces the **full-goodwill** method.

> **⚑ AUDIT FLASH POINT — fair value of identifiable intangibles.** The split between identifiable intangibles (which amortize and depress post-deal earnings) and goodwill (which does not amortize for public entities) is the most litigated number in a purchase-price allocation. Customer-relationship and technology valuations rely on multi-period excess earnings / relief-from-royalty models with sensitive growth, attrition, and discount-rate inputs. Engage a qualified valuation specialist and document the model, inputs, and the reasonableness check (the implied weighted-average return on assets should reconcile to the WACC and the internal rate of return).

#### Recognition and measurement exceptions (`ASC 805-20-25-16` to `25-28` and `-30-10` onward)

Several items are **not** measured at fair value, or are recognized on a different basis:

- **Income taxes** — deferred taxes recognized and measured under `ASC 740`, **not** at fair value (`ASC 805-740`).
- **Employee benefits** — assets/liabilities measured under the relevant benefit standard (`ASC 715`, `ASC 712`).
- **Indemnification assets** — recognized on the **same basis** as the indemnified item, subject to a collectibility assessment (`ASC 805-20-25-27`, `-30-18`).
- **Reacquired rights** (e.g. a franchise/trademark right the acquiree had licensed to the acquirer) — measured on the basis of the **remaining contractual term**, ignoring renewals (`ASC 805-20-30-20`); any settlement gain/loss is separate.
- **Share-based payment awards** (replacement awards) — measured under `ASC 718` (`ASC 805-30-30-9` to `-30-13`); portion attributable to pre-combination service is consideration, the rest is post-combination expense.
- **Assets held for sale** — measured at fair value **less costs to sell** under `ASC 360` (`ASC 805-20-30-22`).
- **Contingencies** — recognized at fair value if fair value is determinable; otherwise apply `ASC 450` recognition criteria (`ASC 805-20-25-18A` to `25-20B`, `-30-23`).
- **Contract assets / contract liabilities (ASU 2021-08)** — revenue contracts acquired are recognized and measured as if the acquirer had originated them under **`ASC 606`** (not at fair value), so deferred revenue is no longer "haircut" to fair value (`ASC 805-20-30-28`).
- **Leases (`ASC 842`)** — the acquirer retains the acquiree's lease classification (unless modified) and measures the lease liability at the present value of remaining payments; a right-of-use asset is adjusted for off-/above-market terms.

### Step 4 — Recognize and measure goodwill or a bargain-purchase gain — `ASC 805-30`

**Goodwill** is the residual (`ASC 805-30-30-1`):

```
Goodwill =  consideration transferred (at fair value)
          + acquisition-date fair value of any NCI
          + acquisition-date fair value of the acquirer's previously held equity interest (step acquisition)
          - acquisition-date net of the identifiable assets acquired and liabilities assumed
```

If the residual is **negative**, the acquirer has a **bargain purchase**. Before recognizing a gain, the acquirer must **reassess** whether it has correctly identified all assets/liabilities and remeasure the amounts (`ASC 805-30-25-4`). If a residual gain remains, recognize it in **earnings (P&L)** on the acquisition date, attributed to the acquirer (`ASC 805-30-25-2` to `25-3`).

> **⚑ AUDIT FLASH POINT — bargain purchase gain.** A day-one gain through P&L invites scrutiny: it usually signals an error in fair values (overvalued assets, omitted liabilities, or an undervalued NCI/consideration) rather than a genuine bargain. Genuine bargains exist (forced sellers, distressed sales) but require documented evidence of *why* the seller accepted less than fair value, plus the mandatory reassessment.

---

## Section 3 — Reference layer: consideration, costs, measurement period, step acquisitions

### Consideration transferred — `ASC 805-30-30-7`

Measured at **acquisition-date fair value** — the sum of the fair values of assets transferred, liabilities incurred to former owners, and equity interests issued by the acquirer. Equity issued is measured at its acquisition-date fair value.

### Contingent consideration ("earn-outs") — `ASC 805-30-25-5` to `25-7`, `-30-8`, `-35-1`

Recognized at **acquisition-date fair value** as part of consideration transferred, and **classified** as a **liability** or **equity** under `ASC 480` / `ASC 815` (`ASC 805-30-25-6`). Subsequent measurement:

- **Equity-classified** — **not** remeasured; settlement is accounted for within equity (`ASC 805-30-35-1(a)`).
- **Liability- (or asset-) classified** — remeasured to **fair value each period through earnings (P&L)** until settled (`ASC 805-30-35-1(b)`).

> **⚑ AUDIT FLASH POINT — contingent-consideration classification and remeasurement.** Liability vs. equity classification under `ASC 480`/`815` determines whether earn-out value changes hit P&L. Fair value of the earn-out (typically a Monte Carlo / option model on revenue/EBITDA targets) is a recurring Level 3 estimate with disclosure obligations under `ASC 820`. Distinguish contingent consideration from compensation: if the earn-out is forfeited when a selling shareholder ceases employment, it is **post-combination compensation expense**, not consideration (`ASC 805-10-55-24` to `55-25`).

### Acquisition-related costs — `ASC 805-10-25-23`

**Expensed as incurred** in the periods the services are received — advisory, legal, accounting, valuation, finder's fees, and general administrative costs. They are **not** part of consideration and do **not** go to goodwill. (Costs to **issue debt or equity** are accounted for under the relevant financial-instrument guidance — debt issuance costs against the debt, equity issuance costs against equity — **not** expensed under this rule.)

### Measurement period — `ASC 805-10-25-13` to `25-19`

If the initial accounting is incomplete at the reporting-period end, the acquirer records **provisional amounts**. During the **measurement period** — the time needed to obtain information about facts that **existed at the acquisition date**, **not to exceed one year** from the acquisition date — the acquirer **retrospectively adjusts** provisional amounts (with a corresponding adjustment to goodwill) for new information about acquisition-date facts (`ASC 805-10-25-13` to `25-17`). Adjustments arising from events **after** the acquisition date are **not** measurement-period adjustments — they go through earnings. Measurement-period adjustments are recognized in the **current period** (in the reporting period in which they are determined), with the effect on prior periods disclosed (`ASC 805-10-25-17A`, per ASU 2015-16) — they are **not** restated retrospectively to prior issued statements.

### Business combination achieved in stages (step acquisition) — `ASC 805-10-25-9` to `25-10`

When the acquirer held an equity interest in the acquiree **before** obtaining control, it **remeasures** that previously held interest to its **acquisition-date fair value** and recognizes the resulting **gain or loss in earnings (P&L)** (`ASC 805-10-25-10`). Any amounts previously recognized in OCI relating to that interest are reclassified as if the interest had been disposed of. The remeasured fair value of the prior interest is then included in the goodwill computation (Step 4).

### Definition of a business and the screen test — `ASC 805-10-55-3A` to `55-9` (ASU 2017-01)

A **business** consists of **inputs** and **substantive processes** applied to those inputs that together contribute to the ability to create outputs. Apply the **screen test** first (`ASC 805-10-55-5A`): if **substantially all** of the fair value of the gross assets acquired is concentrated in a **single identifiable asset or group of similar assets**, the set is **not** a business → account for it as an **asset acquisition** under `ASC 805-50` (cost allocated, **no goodwill**, transaction costs **capitalized**). If the screen is not met, assess whether the set has an input and a substantive process (`ASC 805-10-55-5D` onward).

### In-process research and development (IPR&D)

Acquired IPR&D is recognized as an **indefinite-lived intangible asset** at fair value, **not** expensed at acquisition (`ASC 805-20-55-2` to `55-3`; `ASC 350-30`). It is **not amortized** while indefinite-lived; it is tested for impairment until the project is **completed** (then amortized over its useful life) or **abandoned** (then written off).

---

## Section 4 — Reference layer: subsequent measurement of goodwill — `ASC 350-20`

### Public-entity (and default) model — impairment-only

Goodwill is **not amortized** (`ASC 350-20-35-1`). It is assigned to **reporting units** (`ASC 350-20-35-33` to `-35-44`) and tested for impairment **at least annually**, and more frequently on a triggering event (`ASC 350-20-35-28` to `-35-30`).

An optional **qualitative assessment** ("Step 0") may be performed first; if it is *not* more likely than not that the reporting unit's fair value is below its carrying amount, no further testing is needed (`ASC 350-20-35-3` to `-35-3G`).

**Quantitative test (post-ASU 2017-04 — single step):** compare the reporting unit's **fair value** to its **carrying amount** (including goodwill). If carrying amount exceeds fair value, recognize an impairment loss equal to that excess, **capped at the goodwill** allocated to the reporting unit (`ASC 350-20-35-2`, `-35-8A`). The old "Step 2" (implied-fair-value-of-goodwill) computation is **eliminated**.

Goodwill impairment losses are **never reversed** (`ASC 350-20-35-13`).

### Private-company / not-for-profit alternative — `ASC 350-20-15-4` (ASU 2014-02 / 2014-18)

An eligible private company or NFP may **elect** to:

- **Amortize** goodwill on a straight-line basis over **10 years**, or a shorter useful life if more appropriate (`ASC 350-20-35-63`); and
- Test for impairment only upon a **triggering event** (not annually), at the **entity** or **reporting-unit** level by policy election (`ASC 350-20-35-66` onward), using a single-step measure (carrying over fair value, capped at goodwill).

A related alternative (ASU 2014-18) lets such entities **subsume** customer-related intangibles that are not separable and non-compete agreements **into goodwill** rather than recognizing them separately. **There is no IFRS equivalent** to either alternative.

> **⚑ AUDIT FLASH POINT — goodwill impairment timing and reporting-unit definition.** Auditors challenge (a) whether a triggering event was identified timely (a sustained share-price decline below book value, lost major customer, adverse regulation), and (b) how goodwill was assigned to reporting units and whether units were aggregated to avoid an impairment. Document the reporting-unit determination, the fair-value methodology (income vs. market approach), and the headroom sensitivity.

---

## Section 5 — Executable layer (Layer B): the procedure

Run these steps on the transaction's facts. Each cites the Layer A rule it executes.

1. **Confirm the transaction is a business combination** — apply the screen test / definition of a business (§3, `805-10-55-3A`+). If it is an asset acquisition, stop and apply `ASC 805-50` (no goodwill; costs capitalized).
2. **Identify the acquirer** (Step 1 / §2, `805-10-25-4`, `810` control). Check for a reverse acquisition.
3. **Determine the acquisition date** (Step 2 / §2, `805-10-25-6`).
4. **Build consideration transferred** at fair value (§3, `805-30-30-7`): cash + assets + equity issued + acquisition-date fair value of contingent consideration (classified liability/equity). Strip out amounts that are really post-combination compensation or settlement of pre-existing relationships.
5. **If a step acquisition**, remeasure the previously held interest to fair value; book the gain/loss to P&L (§3, `805-10-25-10`).
6. **Recognize and fair-value the identifiable assets and liabilities** (Step 3 / §2, `805-20-30-1`); apply each recognition/measurement **exception** (income tax, deferred revenue per ASU 2021-08, leases, etc.).
7. **Measure NCI at fair value** (§2, `805-20-30-1`) — full-goodwill method is mandatory under US GAAP.
8. **Compute goodwill** (Step 4 / §2, `805-30-30-1`). If negative, **reassess**, then recognize any remaining **bargain-purchase gain** in P&L.
9. **Expense acquisition-related costs** as incurred (§3, `805-10-25-23`).
10. **Book the consolidation journal entry** (base §3 format); record provisional amounts if the accounting is incomplete and open the **measurement period** (§3).
11. **Subsequently:** remeasure liability-classified contingent consideration through P&L (§3); test goodwill for impairment under `ASC 350-20` (§4), or amortize it if the private-company alternative is elected.
12. **Produce the disclosure checklist** (§7) and **reviewer brief** with every flash point.

### Worked example (illustrative)

**Acquirer** buys **80%** of **Target** for **$800,000 cash** on the acquisition date. The fair value of Target's **identifiable net assets** is **$700,000**. The acquisition-date **fair value of the 20% NCI** is **$190,000**. The acquirer held no prior interest. Acquisition-related advisory and legal costs were **$25,000** (paid in cash).

**Goodwill — US GAAP (full-goodwill, mandatory):**

```
Goodwill = consideration 800,000 + NCI at FV 190,000 - identifiable net assets 700,000 = 290,000
```

```
Acquisition date — consolidate Target via the acquisition method — driving rule: ASC 805-30-30-1
  Dr  Identifiable net assets (at fair value)     700,000
  Dr  Goodwill                                     290,000
      Cr  Cash                                          800,000
      Cr  Non-controlling interest (equity)             190,000
  (memo: goodwill = 800,000 + 190,000 - 700,000 = 290,000; NCI at FV per ASC 805-20-30-1.
   Debits 990,000 = Credits 990,000 ✓)

Acquisition date — acquisition-related costs — driving rule: ASC 805-10-25-23
  Dr  Acquisition expense (P&L, operating)          25,000
      Cr  Cash                                           25,000
  (memo: advisory + legal expensed as incurred, not capitalized to goodwill;
   debits = credits ✓)
```

**Contrast with the IFRS partial-goodwill option** (not available under US GAAP — shown so the divergence is concrete). If NCI were instead measured at the **20% proportionate share of identifiable net assets** = 20% × 700,000 = **140,000**:

```
Goodwill (partial) = 800,000 + 140,000 - 700,000 = 240,000
```

US GAAP **cannot** use this; the $50,000 difference (290,000 − 240,000) is the goodwill attributable to the NCI, which US GAAP requires the acquirer to recognize (full goodwill). See §6.

**Step-acquisition note.** Suppose instead the acquirer had previously held a 10% interest in Target carried at $60,000, whose acquisition-date fair value is $95,000, and now buys a further 70% for cash giving control. The prior interest is **remeasured to $95,000**, booking a **$35,000 gain to P&L** (`ASC 805-10-25-10`):

```
Acquisition date — remeasure previously held interest — driving rule: ASC 805-10-25-10
  Dr  Investment in Target (equity interest)         35,000
      Cr  Gain on remeasurement of prior interest (P&L)  35,000
  (memo: 95,000 FV - 60,000 carrying amount = 35,000; debits = credits ✓)
```

The $95,000 remeasured fair value then enters the goodwill formula as the "previously held equity interest" term in Step 4.

**Contingent-consideration note.** Suppose the deal also includes an **earn-out** with an acquisition-date fair value of **$120,000**, classified as a **liability** under `ASC 480`. It is part of consideration transferred (it would increase goodwill), and is remeasured each period through P&L:

```
Acquisition date — recognize contingent consideration — driving rule: ASC 805-30-25-5
  Dr  Goodwill                                      120,000
      Cr  Contingent consideration liability            120,000
  (memo: earn-out at acquisition-date fair value; classified liability per ASC 480;
   debits = credits ✓)

Subsequent period — fair value rises to 150,000 — driving rule: ASC 805-30-35-1(b)
  Dr  Fair value loss on contingent consideration (P&L)  30,000
      Cr  Contingent consideration liability                  30,000
  (memo: 150,000 - 120,000 = 30,000 through earnings, NOT goodwill; debits = credits ✓)
```

> **⚑ AUDIT FLASH POINT — full vs. partial goodwill changes the balance sheet and future impairment.** Under US GAAP the mandatory full-goodwill method records the higher goodwill ($290,000 here) and a higher NCI. A dual-reporter whose IFRS parent elected the partial-goodwill option for the same deal will show **different** goodwill, NCI, and — on impairment — different loss attribution. Reconcile the two in the reviewer brief.

---

## Section 6 — Divergence from IFRS (IFRS 3 / IAS 36)

ASC 805 and IFRS 3 are substantially converged on the acquisition method, but several differences change the numbers. A dual-reporter must check each:

| Area | US GAAP (ASC 805 / ASC 350) | IFRS (IFRS 3 / IAS 36) |
|------|------------------------------|-------------------------|
| **NCI measurement** | NCI **must** be at **fair value** → **full goodwill** only (`ASC 805-20-30-1`) | **Per-transaction choice**: fair value (full goodwill) **or** proportionate share of identifiable net assets (partial goodwill) (`IFRS 3.19`) |
| **Goodwill — subsequent** | Impairment-only for public entities; **private-company/NFP alternative** permits **amortization ≤ 10 years** + triggering-event-only testing (`ASC 350-20-15-4`) | Impairment-only for **all** entities; **no amortization option** |
| **Goodwill impairment unit** | **Reporting unit** (operating segment or one level below) | **Cash-generating unit (CGU)** or group of CGUs (`IAS 36.80`) |
| **Goodwill impairment measure** | Single-step: carrying amount of reporting unit **over** its fair value, **capped at goodwill** (post-ASU 2017-04) | Recoverable amount = **higher of** fair value less costs of disposal **and** value in use; loss first eliminates goodwill, then pro-rata to other CGU assets (`IAS 36.18`, `.104`) |
| **Reversal of impairment** | Goodwill impairment **never reversed**; most other asset impairments not reversed | Goodwill impairment **never reversed** (`IAS 36.124`); but **other** asset impairments **may be reversed** (`IAS 36.114`) |
| **Definition of a business** | Screen test + framework (ASU 2017-01) | **Optional concentration test** + framework (2018 amendments) — converged but cited separately |
| **Contingent consideration — subsequent** | Liability-classified → P&L; equity-classified → not remeasured | Same (`IFRS 3.58`): financial-liability/asset → P&L; equity → not remeasured |
| **Acquisition costs** | Expensed as incurred (`805-10-25-23`) | Expensed as incurred (`IFRS 3.53`) — converged |
| **Acquired deferred revenue** | Measured under ASC 606 as if originated (ASU 2021-08) | Measured at fair value (no equivalent amendment) — a divergence |
| **Measurement period** | Up to 1 year; adjustments in current period with prior-period effect disclosed (ASU 2015-16) | Up to 1 year; adjustments **retrospective** to the acquisition date (`IFRS 3.45`–`.49`) |

Run `ifrs3-business-combinations` in parallel for dual-reporters and present both answers (base §2).

---

## Section 7 — Disclosure checklist — `ASC 805-10-50`, `805-30-50`, `350-20-50`

Trigger and produce as relevant:

- [ ] Name and description of the acquiree; acquisition date; percentage of voting interests acquired; primary reasons for the combination (`ASC 805-10-50-2`)
- [ ] Acquisition-date fair value of **total consideration** transferred, by major class (cash, equity, contingent consideration) (`805-30-50-1`)
- [ ] **Contingent consideration** arrangements: amount recognized, range of outcomes, basis for the estimate; subsequent fair-value changes (`805-30-50-1(c)`, `-50-4`)
- [ ] Amounts recognized for each major class of **assets acquired and liabilities assumed** (`805-20-50-1`)
- [ ] **Goodwill** recognized and the factors that make up the goodwill; expected tax-deductible portion (`805-30-50-1(d)`)
- [ ] For a **bargain purchase**: the gain, the line item, and why it arose (`805-30-50-1(f)`)
- [ ] **NCI** in the acquiree recognized and the measurement basis/valuation technique (`805-20-50-1(e)`)
- [ ] **Step acquisition:** acquisition-date fair value of the previously held interest and the **remeasurement gain/loss** (`805-10-50-2(g)`)
- [ ] Acquisition-related **costs expensed** and the line item (`805-10-50-2(f)`)
- [ ] **Measurement-period** adjustments and the nature/amount (`805-10-50-4A` / ASU 2015-16)
- [ ] Acquiree **revenue and earnings** since acquisition and **supplemental pro forma** revenue/earnings as if combined from the start of the period (`805-10-50-2(h)`)
- [ ] **Goodwill rollforward**: gross, accumulated impairment, by reportable segment; impairment losses recognized (`350-20-50-1`, `-50-2`)
- [ ] If the **private-company alternative** is elected: amortization method/period and impairment policy (`350-20-50-3A`)

---

## Section 8 — Topic self-checks (in addition to base §7)

- [ ] Confirmed a **business** (screen test applied) vs. an asset acquisition; if asset acquisition, no goodwill and costs capitalized
- [ ] **Acquirer** identified via `ASC 810` control; reverse-acquisition possibility checked
- [ ] **Acquisition date** = date control obtained, tied to `805-10-25-6`
- [ ] Identifiable assets/liabilities at **fair value**; each recognition/measurement **exception** applied (tax, deferred revenue per ASU 2021-08, leases, etc.)
- [ ] **NCI at fair value** (full goodwill) — confirmed no proportionate-share shortcut used
- [ ] **Consideration** at fair value; contingent consideration classified (liability/equity) and fair-valued; compensation stripped out
- [ ] **Goodwill** = consideration + NCI + prior-interest FV − identifiable net assets; arithmetic shown and balanced
- [ ] Negative residual → **reassessed**, then bargain-purchase **gain to P&L**
- [ ] Acquisition-related costs **expensed**, not capitalized to goodwill
- [ ] Step acquisition → prior interest **remeasured to FV**, gain/loss to P&L
- [ ] **Measurement period** opened for provisional amounts; ≤ 1 year; adjustments treated per ASU 2015-16
- [ ] Subsequent: liability contingent consideration remeasured to P&L; goodwill impairment per `ASC 350-20` (or amortization if alternative elected)
- [ ] Divergence from IFRS 3 / IAS 36 checked for dual-reporters (NCI method, goodwill amortization, impairment model)

---

## Section 9 — Disclaimer

Provides computational and interpretive guidance on ASC 805 / ASC 350 only. Not an audit and not assurance. Business-combination accounting turns heavily on entity-specific facts and significant judgment — fair-value measurement of intangibles and contingent consideration, identification of the acquirer, the business-vs-asset determination, and goodwill impairment all require specialist input. Have outputs reviewed and signed by a qualified accountant before they are reflected in financial statements relied upon by third parties.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/us-gaap-asc805-business-combinations) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
