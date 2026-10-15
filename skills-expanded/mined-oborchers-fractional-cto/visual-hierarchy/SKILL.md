---
name: visual-hierarchy
description: This skill should be used when the user is establishing visual importance, designing headings, creating focal points, designing CTAs or buttons, arranging label-data relationships, implementing scanning patterns (F-pattern, Z-pattern), or ensuring one dominant element per screen. Covers the three levers of hierarchy (size, weight, color), three-tier information architecture, the 'emphasize by de-emphasizing' principle, CTA design, and label-data relationships.
version: 1.0.0
---

# If Everything Is Important, Nothing Is -- One Star per Screen

Users form a first impression within 50ms (Lindgaard et al., 2006). Hierarchy must work at the gestalt level -- before anyone reads a single word, the eye must know where to land. If two elements compete for dominance, neither wins and the user stalls.

## Three Levers of Hierarchy

Control visual importance with exactly three levers. Use them independently, not simultaneously.

| Lever | How It Works | Example |
|-------|-------------|---------|
| **Size** | Larger elements attract first | 2x body size for primary headings |
| **Weight/Boldness** | Heavier strokes draw focus | Bold for labels, regular for body |
| **Color/Contrast** | Higher contrast = more important | Dark text on light bg for primary, gray for tertiary |

**Rule:** Adjust one lever at a time. If a heading is already 2x body size, do not also make it bold and high-contrast -- that overshoots. Reserve additional levers for when a single lever is insufficient.

## Three-Tier Information Architecture

Every screen must have exactly three tiers of visual importance. No more, no fewer.

| Tier | Size | Weight | Contrast Ratio | Role |
|------|------|--------|----------------|------|
| **Primary** | 2x body | Bold (600--700) | >= 7:1 | The star -- one per screen/section |
| **Secondary** | 1x body | Regular (400) | 4.5--7:1 | Supporting content |
| **Tertiary** | 0.75x body | Light (300--400) | 3--4.5:1 | Metadata, timestamps, captions |

If you cannot assign every text element to one of these three tiers, the hierarchy is broken.

## One Dominant Element per Screen

Every screen and every section needs exactly one "star" -- the element the eye hits first. This is the F-pattern entry point, the dashboard KPI, the landing page headline.

**The squint test:** Squint at the screen until you can barely see it. The element that remains most visible is the star. If nothing stands out, or if two elements compete, the hierarchy has failed.

**The 5-second test:** Show the screen for 5 seconds, then ask: "What was this page about?" If users cannot answer, the star is not dominant enough.

## Emphasize by De-Emphasizing

Do not make the primary element louder. Make everything else quieter. When secondary and tertiary elements recede, the primary element naturally dominates without needing to be oversized or garish.

| Approach | Result |
|----------|--------|
| Make heading bigger, bolder, brighter | Feels aggressive, reduces reading comfort |
| Make body text lighter, smaller, lower contrast | Heading dominates naturally, entire page feels calm |

This is Steve Schoger's (Refactoring UI) core hierarchy insight: "If everything on the page is fighting for attention, nothing feels important."

## Scanning Patterns

| Pattern | When to Use | Key Constraint |
|---------|------------|----------------|
| **F-pattern** | Content-heavy pages, dashboards, lists | Place primary info on the left, secondary info indented right |
| **Z-pattern** | Landing pages, hero sections, CTAs | Top-left (logo) -> top-right (nav) -> bottom-left (headline) -> bottom-right (CTA) |

Place the most important content where the pattern predicts the eye will land. Do not fight the pattern -- work with it.

## CTA Design

| Rule | Rationale |
|------|-----------|
| One primary CTA per section | Multiple primaries create decision paralysis |
| Button hierarchy: filled > outlined > ghost | Visual weight signals importance |
| Primary CTA uses a distinctive color | Must be the highest-contrast interactive element |
| Secondary actions use outlined or ghost buttons | Visually subordinate to primary |
| Destructive actions use red, but not filled-red at primary weight | Prevent accidental clicks |

## Label-Data Relationships

Labels exist to describe data. Data is what the user came for. Labels must always be subordinate.

| Property | Label | Data |
|----------|-------|------|
| Size | 0.75--0.875x body | 1x body or larger |
| Weight | Regular or light | Medium or bold |
| Contrast | Lower (tertiary tier) | Higher (primary/secondary tier) |
| Color | Muted gray | Full-strength text color |

**Anti-pattern:** Labels in bold, data in regular weight. This inverts the hierarchy and forces users to scan past the noise to find the value.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Everything same size and weight | No entry point, no scannable structure | Apply three-tier architecture |
| Multiple competing CTAs | Decision paralysis, lower conversion | One primary CTA per section |
| Labels dominating data | User scans past noise to find values | Labels subordinate: smaller, lighter, lower contrast |
| Heading + bold + color simultaneously | Overshooting, feels aggressive | Adjust one lever at a time |
| No squint-test star | Page has no focal point | Designate one dominant element and de-emphasize the rest |

## Cross-Media Notes

- **Presentations**: One idea per slide, heading ratio 2x body minimum, audience reads the star in under 2 seconds
- **CVs/Resumes**: Name is the star (largest, boldest), section headings are secondary, body text is tertiary
- **Dashboards**: Key KPI is the star, passes the 5-second test, supporting metrics are secondary

## Examples

Working implementations in `examples/`:
- **`examples/three-tier-hierarchy.md`** -- Implementing 3-tier hierarchy with CSS custom properties, Tailwind utilities, and React components, with good/bad comparison

## Review Checklist

When reviewing or building visual hierarchy:

- [ ] Every screen has exactly one dominant element (the star)
- [ ] The squint test passes -- the star is the most visible element when squinting
- [ ] Three-tier architecture applied: primary, secondary, tertiary
- [ ] Every text element can be assigned to exactly one of the three tiers
- [ ] Size, weight, and color levers used independently, not stacked
- [ ] Primary headings are approximately 2x body size
- [ ] Tertiary text (metadata, captions) is approximately 0.75x body with reduced contrast
- [ ] Labels are always subordinate to data (smaller, lighter, lower contrast)
- [ ] One primary CTA per section with clear visual dominance
- [ ] Button hierarchy follows filled > outlined > ghost
- [ ] F-pattern used for content pages, Z-pattern for landing pages
- [ ] De-emphasizing secondary content rather than over-emphasizing primary
- [ ] The 5-second test passes -- users can identify the page purpose
- [ ] No competing elements of equal visual weight at the same level
- [ ] Contrast ratios meet the three-tier model and WCAG minimums (see `accessibility-inclusive-design` skill)
