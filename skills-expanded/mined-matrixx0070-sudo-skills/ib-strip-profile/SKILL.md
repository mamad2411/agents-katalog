---
name: ib-strip-profile
version: 1.0.0
description: Build a named 1-4 slide company profile ("strip profile") — business description, key financials, ownership, and a quadrant/positioning layout — for pitchbooks, buyer screens, and comps.
author: matrixx0070
tags: [investment-banking, profiles, pitchbook, company-analysis, quadrant]
capabilities: []
---

## When to use
Use this when you need a compact, named company overview for internal or pitch use — profiling a potential acquirer, a comparable company, or a target on a shortlist. A strip profile packs the business description, financials, ownership, and a positioning visual (often a 2x2 quadrant) into one to four slides so a reader can size up a company at a glance.

**Not for:** an anonymous pre-NDA teaser (use ib-teaser), the full sell-side book (use ib-cim-builder), or assembling the whole pitch (use ib-pitch-deck). Strip profiles are named and disclosed; do not use one where anonymity is required.

## Method
1. Fix the purpose: is this profiling a buyer (emphasize strategic fit, balance sheet, deal history), a comp (emphasize multiples and financial metrics), or a target (emphasize business and growth)? Purpose drives which fields lead.
2. Write a tight business description: what the company does, where, and its scale — three to four sentences maximum.
3. Populate key financials from a cited source: revenue, EBITDA, margin, growth, and for public names market cap / enterprise value and trading multiples (EV/EBITDA, EV/Revenue, P/E).
4. Add ownership and structure: public/private, major shareholders or sponsor ownership, headquarters, employees, and recent M&A activity.
   **Decision point:** if a positioning visual is requested, choose the two axes that matter for the pitch (e.g., scale vs. growth, or capability breadth vs. geographic reach) and plot the company set on a 2x2 quadrant.
5. Keep one consistent template across all profiles in a set so they are comparable side by side.
6. Cite every figure to its source and date; mark estimates as such.
7. Review for accuracy against filings/data provider before it goes into a client-facing book.

## Example
> Buyer screen for a sell-side pitch: four one-slide profiles of candidate acquirers on a shared template — business description, latest revenue/EBITDA/margin, ownership (two public, one PE-backed, one family-owned), HQ/headcount, and last three acquisitions. A fifth slide plotted all four on a scale (revenue) vs. growth (3-yr CAGR) quadrant, positioning two as high-growth consolidators in the top-right. Every figure cited to latest filings or the data provider with dates.

## Pitfalls
- Inconsistent templates across a profile set, so companies cannot be compared at a glance.
- Uncited or undated figures — especially trading multiples that move daily — that cannot be defended in a client meeting.
- Cramming too much onto the slide; a strip profile is a scan, not a deep dive.
- A quadrant with poorly chosen axes that flatters a preferred name rather than reflecting a real dimension of differentiation.

## Output format
```
COMPANY PROFILE — <Company name>            [1 of N]

BUSINESS DESCRIPTION
<3-4 sentences: what / where / scale>

KEY FINANCIALS (US$M, <source, date>)          OWNERSHIP & STRUCTURE
Revenue        <->   growth <%>                 Type: <public/private/PE>
EBITDA         <->   margin <%>                 Major holders: <->
EV / Mkt cap   <->                              HQ: <->  Employees: <->
EV/EBITDA      <x>   EV/Rev <x>   P/E <x>        Recent M&A: <->

[Optional] POSITIONING QUADRANT
        High <axis Y>
          |   (B)        (A)
  <axis X low> -------------- <axis X high>
          |   (C)        (D)
        Low <axis Y>
Legend: A/B/C/D = <companies plotted>   Axes: X=<>, Y=<>

Sources: <filings / data provider, dates>   Estimates marked (E).
```

## Reference
- Strip profiles are a staple of pitchbooks and buyer/comp screens: named, disclosed, and templated so a set of companies reads consistently side by side.
- For comps, lead with trading multiples (EV/EBITDA, EV/Revenue, P/E) sourced and dated; for buyers, lead with strategic fit, balance-sheet capacity, and acquisition history; for targets, lead with business and growth.
- The 2x2 quadrant (Boston-matrix style) positions a company set on two chosen dimensions — common axes are scale vs. growth, breadth vs. reach, or profitability vs. growth — and must use axes that reflect a genuine differentiator.
- Every number is sourced and dated because trading data and estimates change; consistency of template and citation is what makes the set usable in a client meeting.
