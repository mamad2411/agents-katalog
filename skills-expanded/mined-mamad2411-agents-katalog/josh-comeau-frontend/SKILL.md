---
name: josh-comeau-frontend
description: Build, debug, and polish web interfaces using source-linked lessons from Josh W. Comeau on CSS layout, React rendering, animation, SVG, accessibility, and frontend workflow; use for requests like "Fix this CSS layout", "Make this interaction feel polished", "Debug React rendering", or "Apply Josh Comeau's frontend techniques".
---

# Josh Comeau Frontend

Turn frontend surprises into an explicit mental model, then implement the smallest
appropriate solution. This is an independent synthesis, not an official Josh W.
Comeau product, a replica of his website, or a mandate to adopt his technology stack.

## How It Works

1. Establish the actual task, existing stack, rendering environment, browser targets,
   and accessibility requirements. Preserve the project's conventions. For a
   version-sensitive task, read [Current platforms](references/current-platforms.md).
2. Choose the relevant guide below. Read only the sections needed for this task;
   do not load all 88 sources into context.
3. Explain the governing mechanism: layout algorithm, containing block, cascade,
   stacking context, render ownership, hydration, or animation timeline.
4. Implement a minimal change. Distinguish functional requirements from decorative
   enhancements; keep essential content and controls usable without the enhancement.
5. Validate the mechanism and the user experience. Report what was tested, what
   remains uncertain, and the source IDs that materially informed the change.

## Choose a Guide

| Task / symptom | Read |
| --- | --- |
| Overflow, centering, flex/grid sizing, subgrid, z-index, margin collapse | [Layout](references/layout.md) |
| Container queries, `:has()`, anchor positioning, `@starting-style`, resets | [Modern CSS](references/modern-css.md) |
| Color, gradients, shadows, glass, sticky headers, visual fidelity | [Visual design](references/visual-design.md) |
| Transitions, keyframes, springs, scroll timelines, FLIP, performance | [Motion foundations](references/motion-foundations.md) |
| Sprites, particles, tactile buttons, sparkles, boops, sound, 3D effects | [Motion recipes](references/motion-recipes.md) |
| SVG coordinates, paths, arcs, strokes, interactive curves | [SVG](references/svg.md) |
| Forms, state, re-renders, memoization, deferred updates, JS foundations | [React and JavaScript](references/react.md) |
| SSR, RSC, hydration, dark mode, CSS-in-JS, server-data refresh | [Rendering and styling](references/rendering.md) |
| MDX, playgrounds, email, file structure, terminal, real-device testing | [Tooling](references/tooling.md) |
| Font scaling, reduced motion, keyboard and alternative-input access | [Accessibility](references/accessibility.md) |
| Maintainability, learning, AI-assisted work, design collaboration | [Engineering practice](references/engineering-practice.md) |
| Requested career, remote-work, or conference advice | [Career](references/career.md) |

Career and learning material is opt-in context for relevant requests, not extra work
to perform during ordinary implementation. Accessibility applies across all UI work.

## Decision Rules

- Diagnose the algorithm before changing declarations. A larger `z-index`, another
  `height: 100%`, or a memoization hook is not an explanation.
- Choose CSS or JavaScript by capabilities, interruption behavior, and measured
  rendering cost—not by a blanket claim that one language is faster.
- Keep DOM order, semantics, focus, text resizing, and reduced-motion behavior intact
  while improving appearance. Decorative layers must not intercept input.
- Distinguish React re-rendering from DOM mutation, SSR from RSC, and a browser-only
  API guard from hydration correctness.
- A source's library choice, personal preference, historical support percentage, or
  labor-market forecast is not a current universal rule.
- Check installed versions and current primary documentation when implementation
  depends on browser or library support. If offline, describe the uncertainty and
  retain a functional fallback. Do not automatically migrate tools.
- Use current stable APIs, not the implementation era of the linked article.
  The guidance was reconciled with published stable releases and primary documentation
  on September 19, 2026; that is a dated review, not a permanent claim of freshness.
  Remove an obsolete recipe rather than retaining it as a recommended alternative.
  Do not confuse an older but still-supported API with an obsolete one.
- Prefer original, readable implementations over reproducing whole article examples.
  The guides add explicitly identified engineering safeguards to illustrative demos.

## Usage

The guides work without running a script. For targeted discovery:

```bash
bash /mnt/skills/user/josh-comeau-frontend/scripts/find-guidance.sh 'hydration dark mode'
bash /mnt/skills/user/josh-comeau-frontend/scripts/find-guidance.sh 'subgrid' 3
bash /mnt/skills/user/josh-comeau-frontend/scripts/audit-feed.sh
```

**Arguments:**

- `find-guidance.sh [query] [limit]`: offline search through the source notes; defaults
  to 5 results. With no query, lists topics. Use source IDs such as `S024` for lookup.
- `audit-feed.sh [rss-file]`: compare the live feed with the included snapshot, or use
  a local XML file for an offline audit. It does not modify the skill or fetch articles.
- Scripts need Bash and Python 3; a live audit also needs `curl`. Installation roots
  vary: substitute the actual skill directory if `/mnt/skills/user` is not used.

## Output

Scripts emit JSON on stdout and status messages on stderr. A lookup returns
`query`, `total_matches`, and `results` containing source IDs, URLs, guide paths,
and the matching guidance. An audit returns `status`, counts, and lists of added,
removed, changed, and duplicate feed entries. Audit exit code 2 means feed drift.

## Validation Before Handoff

- Reproduce the original failure, then verify the actual changed interaction.
- Check narrow/wide containers, long content, empty states, and relevant RTL layouts.
- For UI changes, check keyboard focus, increased default font size, and reduced motion.
- For React changes, check applicable SSR/hydration, repeated mount/unmount, stale
  asynchronous work, and multiple instances. Use a production build where relevant.
- For animation changes, check rapid reversal, slow devices, cleanup, and the static
  fallback. Profile before claiming a performance improvement.
- Do not claim every item was tested when tools or devices were unavailable.

## Present Results to User

Use a short task-sized report rather than an obligatory full audit:

```text
Changed: [implementation and location]
Why: [mechanism and trade-off; relevant source ID/title]
Verified: [actual checks and results]
Limitations: [unverified support, devices, or remaining caveats]
```

## Source Coverage and Updating

[Source index](references/sources.json) records every one of the **88 entries** in
the RSS snapshot retrieved on **September 19, 2026**, including an external
Smashing Magazine article and both versions of “How I Built My Blog”. IDs refer
to this snapshot's order; URLs, not titles, identify articles.

Research retrieved full-page HTML for every entry, reviewed section-level excerpts,
and inspected selected longer technical passages and code. **This is not a
word-for-word reading of every article or an exhaustive interactive-demo audit.**
Original article bodies are not bundled. Each entry has an individual application
note, caveat, and verification prompt; these are original synthesis, not quotations.

Current implementation advice can intentionally differ from an article. The primary
sources and release checks in [Current platforms](references/current-platforms.md)
explain those adaptations; the 88 article links remain attribution, not instructions
to copy their original code.

To refresh: audit the feed, recheck stable package releases and primary docs, inspect
revised sources, and update affected guides and provenance while preserving existing
IDs. An unchanged feed does not prove unchanged articles or platforms;
the feed audit checks neither package releases nor documentation. Stored HTML hashes
are provenance, not evidence that the audit rechecked page contents.

## Troubleshooting

- **No lookup results:** try a mechanism (`stacking`, `containment`, `memo`) or ID.
- **Network/TLS/proxy failure:** retry later or pass a previously downloaded RSS file;
  do not disable certificate verification or report a failed fetch as current coverage.
- **Permission denied:** invoke with `bash`; scripts only read packaged references
  and use temporary files. They do not require repository writes or elevated access.
- **An article's code differs from current APIs:** use the adapted guide and current
  primary docs, not the article-era recipe. If the project is older than the verified
  baseline, flag the mismatch; this skill does not authorize a dependency upgrade.
