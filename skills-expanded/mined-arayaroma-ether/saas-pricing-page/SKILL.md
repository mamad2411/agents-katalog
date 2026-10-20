---
name: saas-pricing-page
description: Use when building or redesigning a B2B SaaS pricing/plans page with N real priced tiers (e.g. Free/Pro/Max) plus a "talk to sales" catch-all for custom needs — real tiers as cards, the catch-all split out as a distinct dark contact bar (NOT a real plan, no specs/no comparison-table row), plus a full feature-comparison table below the cards (not just card bullets). Pair with the current tenant's real plan/usage data if the app has it — never fabricate numbers, and never invent a 4th tier's specs just to fill out the layout.
metadata:
  origin: seiko-pos /pricing redesign, 2026-08-27
allowed-tools: Read, Edit, Grep, Glob
---

# SaaS pricing page pattern

All the real priced tiers (however many the product actually has — 2, 3, whatever
`docs`/backend plan config defines) go in a card row together. A separate, visually distinct
contact bar goes below for "need something custom" — this is NOT a 4th tier: it gets no price,
no feature list, no row in the comparison table. It exists because even a top tier with generous
limits will have some prospects asking for something outside it (custom integration, unusual
volume, a one-off contract), and conflating that ask with "upgrade to our biggest plan" undersells
both. Three-part layout:

1. All real tiers as cards in one row (highlight the most-recommended one with an accent border + "Most popular" badge; highlight the user's current tier with a "Current plan" badge and a disabled button).
2. A full-width dark "talk to sales" bar below the cards — generic copy, no specs, no plan name pretending to be a tier.
3. A full feature-comparison table underneath the bar, grouped by category, covering only the real tiers (not the contact bar) — card bullets alone under-sell a plan with many differentiators; a real product usually has more features than fit in 4-5 bullet points.

## Card row (all real, priced tiers)

```tsx
<div className="grid gap-4 lg:grid-cols-3">
  {tiers.map(({ tier, label, priceLabel, tagline, cta }) => {
    const isCurrent = tier === currentTier;
    const isPopular = tier === "PRO";
    return (
      <div key={tier} className={cn(
        "flex flex-col gap-5 rounded-lg border bg-white p-6",
        isPopular ? "border-emerald-600" : "border-slate-200",
      )}>
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-semibold text-slate-900">{label}</h2>
            {isCurrent && <Badge className="bg-slate-900 text-white hover:bg-slate-900">Current plan</Badge>}
            {!isCurrent && isPopular && (
              <Badge variant="outline" className="border-emerald-300 text-emerald-700">Most popular</Badge>
            )}
          </div>
          <p className="text-sm text-slate-500">{tagline}</p>
        </div>
        <p className="text-3xl font-semibold text-slate-900">{priceLabel}</p>
        <Button asChild className="mt-auto" variant={isCurrent ? "outline" : isPopular ? "default" : "outline"} disabled={isCurrent}>
          {isCurrent ? <span>Active plan</span> : <a href={ctaHref(label)}>{cta}</a>}
        </Button>
      </div>
    );
  })}
</div>
```

## Contact bar (not a tier — no specs, no table row)

Dark, full-width, horizontal — reads as categorically different from the cards above it, which
is the point: it signals "this isn't one of our plans, it's a conversation." Keep the copy
generic ("need something different from our biggest plan?"), never give it a fake price or a
name that reads like a tier ("Enterprise" is fine as a label as long as it has no specs attached
anywhere — no comparison-table column, no bullet list).

```tsx
<div className="flex flex-col items-start gap-6 rounded-lg bg-slate-900 p-8 text-white sm:flex-row sm:items-center sm:justify-between">
  <div className="space-y-2">
    <div className="flex items-center gap-2">
      <h2 className="text-lg font-semibold">Enterprise</h2>
      <Badge variant="outline" className="border-white/30 text-white/80">Custom</Badge>
    </div>
    <p className="max-w-md text-sm text-white/70">
      Need something beyond our top plan — a custom integration, unusual volume, a specific
      agreement? Let's talk and put together a proposal for your operation.
    </p>
  </div>
  <Button asChild variant="secondary" className="shrink-0 bg-white text-slate-900 hover:bg-white/90">
    <a href={ctaHref("custom")}>Talk to sales</a>
  </Button>
</div>
```

## Full feature comparison table

Group rows by category (usage limits, core features, advanced modules, support), not one flat
list — a flat list of 15+ rows is harder to scan than 4 labeled groups of 3-5. Highlight the
current-plan column so a logged-in user immediately sees where they stand.

```tsx
<table className="w-full min-w-[560px] border-collapse text-left">
  <thead>
    <tr className="border-b border-slate-200 bg-slate-50">
      <th className="px-4 py-3 text-sm font-medium text-slate-500">Feature</th>
      {tiers.map(({ tier, label }) => (
        <th key={tier} className={cn("px-4 py-3 text-center text-sm font-semibold text-slate-900",
          tier === currentTier && "bg-emerald-50/60")}>
          {label}
        </th>
      ))}
    </tr>
  </thead>
  <tbody>
    {sections.map((section) => (
      <Fragment key={section.title}>
        <tr className="border-b border-t border-slate-200 bg-slate-50/60">
          <td colSpan={tiers.length + 1} className="px-4 py-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
            {section.title}
          </td>
        </tr>
        {section.rows.map((row) => (
          <tr key={row.label} className="border-b border-slate-100 last:border-b-0">
            <td className="px-4 py-3 text-sm text-slate-700">{row.label}</td>
            {row.values.map((value, i) => <Cell key={i} value={value} emphasized={tiers[i]?.tier === currentTier} />)}
          </tr>
        ))}
      </Fragment>
    ))}
  </tbody>
</table>
```

`Cell` renders a `Check`/`Minus` icon for booleans, plain text for numeric limits ("10", "Unlimited").

## Current-plan awareness (if the app has auth + plan state)

If the logged-in user's tenant/account already carries plan + usage data (quotas and current
counts), surface it in the hero instead of leaving that space generic — real usage bars
("7/10 users", "980/1000 invoices this month") do more selling work than marketing copy, because
they show the user their own ceiling. Use the app's existing `Progress` component, one row per
quota that has a real max (skip unlimited ones):

```tsx
{usage.map((entry) => {
  const pct = entry.max ? Math.min(100, Math.round((entry.current / entry.max) * 100)) : 0;
  return (
    <div key={entry.label} className="space-y-1">
      <div className="flex items-center justify-between text-xs text-slate-600">
        <span>{entry.label}</span>
        <span className={cn(pct >= 90 && "font-semibold text-amber-600")}>{entry.current} / {entry.max}</span>
      </div>
      <Progress value={pct} className="h-1.5" />
    </div>
  );
})}
```

Never invent tier prices, limits, or feature lists — pull them from the same source of truth the
backend enforcement uses (a plan-limits config, a pricing doc). A pricing page that disagrees with
what the backend actually gates is worse than no pricing page.

## FAQ instead of fine-print disclaimer

A single gray sentence at the bottom ("contact us for details") under-explains real operational
questions (how upgrades activate, what happens at the limit, can you downgrade). Replace it with
3-4 short Q&A pairs, `dl`/`dt`/`dd` with a hairline divider — keeps the minimal look without
losing the information.
