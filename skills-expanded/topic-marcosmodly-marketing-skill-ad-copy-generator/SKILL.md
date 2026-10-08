---
name: ad-copy-generator
description: "Writes paid ad copy for Facebook and Instagram (Meta) Ads, Google Search Ads (RSA headlines and descriptions), and LinkedIn Ads: multiple variants per platform, each testing a different hook angle and sized to that platform's character limits, ready for A/B testing. Use when the user asks for ad copy, ad headlines, ad variants, PPC or paid social copy, Facebook ad text, Google Ads headlines, or A/B test copy for a paid campaign."
allowed-tools: Read, Grep, Glob, Write
---

# Ad Copy Generator

## Purpose

Turn one offer or piece of source content into several genuinely
different paid-ad copy variants — not paraphrases of each other, but
different hook angles (pain point, benefit, social proof, urgency, etc.)
suitable for real A/B testing — sized to fit each target platform's
character constraints.

## Step-by-step process

**Plugin root:** if a path below still shows an unexpanded
`CLAUDE_PLUGIN_ROOT` placeholder (Claude Code fills it in; other agents
such as Codex don't), resolve it before using any of them: take the
output of `printenv CLAUDE_PLUGIN_ROOT` if it prints a path, otherwise
walk up from this file's folder to the first folder that contains
`references/brand-voice.md`, and if neither works, ask the user where
this plugin lives. Use that absolute path in every file path and shell
command below.

1. **Check onboarding status.** Read
   `${CLAUDE_PLUGIN_ROOT}/references/brand-voice.md`. If it doesn't exist,
   or its first line is `<!-- MARKETING-SKILL:UNCONFIGURED -->`, pause and
   ask the user this plugin's 4 setup questions (priority task; content
   types to produce; target audience + tone; default output format — same
   as `/marketing-skill:marketing-setup`) before continuing, then save the
   answers into that file and flip the marker to `CONFIGURED` with today's
   date. Otherwise, read it for tone, audience, and banned words below.

2. **Confirm scope.**
   - The offer/product/source content (paste, file, URL, or "our
     product" — check `README*`/`package.json`/`pyproject.toml` at the
     project root first if so, same as `content-repurposer`).
   - Which platform(s): Meta (Facebook/Instagram), Google Search (RSA),
     LinkedIn Ads — default to asking rather than guessing, since limits
     and tone differ a lot by platform.
   - The landing page URL and CTA, if any — kept identical across
     variants unless the user wants CTA itself tested as a variable.
   - How many variants per platform (default: 3, each a different hook
     angle).

3. **Draft variants**, one distinct hook angle per variant (e.g. pain
   point, concrete benefit/outcome, social proof, urgency/scarcity —
   don't reuse the same angle twice in one batch). Never invent a
   statistic, customer count, or claim not present in the source content.

4. **Fit platform constraints.** Apply the character guidance in
   "Platform constraints" below and show the actual character count next
   to each field — don't just assert it fits.

5. **Self-check before finalizing**: scan every variant against the
   banned-words list, confirm the CTA/link is identical across variants
   (unless CTA is deliberately being tested), and confirm no two variants
   in the same batch use the same hook angle.

## When to use this skill

Trigger on requests like:
- "Write ad copy for [product/offer]"
- "Give me Meta ad variants for..."
- "Google ad headlines for..."
- "A/B test copy for our LinkedIn ad"

## Platform constraints

> These are commonly-cited platform guidelines, not values this skill can
> verify live — character limits and truncation points shift over time,
> so confirm current specs in the platform's own ad-manager UI before
> finalizing a real campaign, especially close to a limit.

| Platform | Field | Guidance |
|---|---|---|
| Google Search (RSA) | Headline | ≤30 characters, up to 15 per ad |
| Google Search (RSA) | Description | ≤90 characters, up to 4 per ad |
| Meta (Facebook/Instagram) | Primary text | Full text allowed, but plan for truncation around ~125 characters on most placements |
| Meta (Facebook/Instagram) | Headline | ~27–40 characters before truncation |
| LinkedIn Ads | Intro text | ~150 characters before truncation on most placements |
| LinkedIn Ads | Headline | ~70 characters before truncation |

## Output structure (required)

Use this exact section order, as Markdown `##` headings, per platform
requested:

### [Platform Name]
A table per variant: `Variant | Hook Angle | Headline (chars) | Body/Primary
Text (chars) | Description (chars, if applicable) | CTA`. Follow the table
with one line per variant naming why that angle was chosen.

## Formatting rules

- Every variant in a batch must use a distinct hook angle — flag it if
  fewer distinct angles are possible than variants requested, rather than
  silently repeating one.
- Show a character count for every length-constrained field.
- Never fabricate a statistic, review count, or claim absent from the
  source.
- Apply `references/brand-voice.md` banned words and tone, adapted to
  each platform's norms (e.g. LinkedIn skews more formal than Meta).
- Keep the CTA/link identical across variants unless the user explicitly
  wants CTA tested as its own variable.

## Example output

> Fictional example: 2 Meta variants for "one-click export."

```markdown
### Meta (Facebook/Instagram)

| Variant | Hook Angle | Headline (chars) | Primary Text (chars) | CTA |
|---|---|---|---|---|
| A | Pain point | "Stop Exporting By Hand" (22) | "Every manual export is ten minutes you don't get back. One-click export replaces the whole process — pick a report, done." (121) | Learn More |
| B | Concrete benefit | "Export Reports In One Click" (27) | "No templates. No copy-pasting. Just pick a report and format — it's live for every customer today." (98) | Learn More |

- Variant A leads with the friction the buyer already feels (manual
  export as wasted time).
- Variant B leads with the mechanism itself as the selling point (how
  fast and simple it now is).
```
