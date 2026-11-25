---
name: template-selection
description: Finds clean, licence-clear templates that actually fit a project, shortlists a few with their trade-offs for the user to choose, and hands the chosen one to customisation. It understands the project first, judges each candidate for fit, cleanliness and licence, never picks for the user, never uses a template against its licence, and never ships one unchanged, because a template shipped as-is is the generic default. Use when a project wants to start from a template rather than a blank page.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core]
  outputs: [project-fit-brief, template-shortlist, licence-check, customisation-handoff]
---

# Template Selection

Starting from a good template is faster than a blank page and better than a bad
one. This skill finds templates that genuinely fit the project, judges them for
cleanliness and licence rather than for the demo screenshot, shortlists a few
for the user to choose from, and then hands the chosen one to customisation,
because a template that ships unchanged is the generic default a real product
should not have.

## 1. Understand the project first

"Templates that resemble the project" is meaningless without knowing the
project. Establish it before searching.

```
type        a marketing site, a dashboard, a docs site, a store, an app shell,
            each has a different template shape
stack       the framework and the styling approach; a template in the wrong
            stack is a rewrite, not a head start
features    what the project needs the template to already do, and what it does
            not
identity    the brand, the feeling, the audience the product wants; a template
            is judged against this, not against its own demo
constraints  accessibility, performance, licence terms the project can accept
            (can it use a template that requires attribution, or a paid one)
```

## 2. Search legitimate sources only

```
open source     framework starters, official templates, reputable open UI kits
                and component libraries with a clear licence
marketplaces    template marketplaces, where a template is bought and licensed,
                when a paid template is acceptable and the budget exists
design systems   a public design system as a foundation to build on
never           a template lifted from a site with no licence to use it, a
                paid template used without buying it, or anything whose licence
                does not permit the intended use
```

## 3. Judge each candidate, not by its screenshot

| Axis | The question |
|---|---|
| Fit | does it match the type, the stack and the features the project needs, or is it a rewrite in disguise |
| Cleanliness | does it read as designed or as the generic default, judged with `design-authenticity`; a template with the whole vibe-coded cluster is not clean because it looks modern |
| Licence | does the licence permit this use, including commercial if the project is commercial, and can the project meet its terms (attribution, no redistribution) |
| Quality | is the code maintainable, the dependencies current, the accessibility present, or is it a demo that falls apart on real content |
| Customisation cost | how much work to make it the project's own, which is the real cost, not the download |

A template that looks impressive and is a rewrite in the wrong stack, or is
beautiful and unlicensed for this use, is not a candidate.

## 4. Shortlist, and let the user choose

```
shortlist   a small set, a handful, not fifty; each with why it fits, its
            licence, its trade-offs, and what customising it would take
present     the differences that matter to the choice, so the user decides on
            substance, not on the prettiest thumbnail
choose      the user picks. This skill proposes; it does not decide, because
            the fit to the identity and the acceptable licence are the user's
            call
```

## 5. Confirm the licence before anything is used

Once chosen, the licence is checked and met before a line is used.

```
permits     the licence permits this use, commercial where the project is
            commercial
terms met    attribution rendered where required, no redistribution or resale
            where forbidden, the paid template actually purchased
recorded     the template, its source and its licence are recorded, so the
            project can prove its provenance
```

A template used in violation of its licence is a legal exposure the project
carries, not a shortcut.

## 6. Customisation is not optional

The chosen template is a starting point, not the product. Shipping it unchanged
is exactly the generic-default look `design-authenticity` flags.

```
make it the project's   its typography, colour, spacing and radius become the
                        project's tokens, not the template's defaults
its content             real content replaces the template's placeholder copy
                        and stock imagery
remove the tells         the generic-default markers the template carried are
                        replaced with intentional choices
an original result       what ships is the project's design on a licensed
                        foundation, not a recognisable clone of the template's
                        demo
```

## 7. Prohibitions

- No template used in violation of its licence, and no paid template used
  without buying it.
- No template presented as clean when `design-authenticity` flags it as the
  generic default.
- No choice made for the user; the shortlist is presented and the user picks.
- No template in the wrong stack sold as a head start when it is a rewrite.
- No template shipped unchanged as if it were a custom design.
- No template's provenance and licence left unrecorded.

## 8. Protocol

1. Establish the project: type, stack, features, identity, and the licence
   terms it can accept.
2. Search legitimate sources for templates that fit, whose licence permits the
   use.
3. Judge each candidate on fit, cleanliness with `design-authenticity`, licence,
   quality and customisation cost.
4. Shortlist a handful and present them with their trade-offs, and let the user
   choose.
5. Confirm the chosen template's licence permits the use and its terms are met,
   and record its provenance.
6. Hand off to customisation, where the template becomes the project's own with
   its tokens, its content and its intent, an original result on a licensed
   foundation.

## 9. Auto-critique

Score from 0 to 5: the project was understood before searching, candidates were
judged on fit and cleanliness and licence rather than the screenshot, the
shortlist left the choice to the user, the chosen template's licence was
confirmed and its provenance recorded, and customisation made the result the
project's own rather than shipping the template unchanged.

Threshold: no axis below 3, average at least 4. A template used against its
licence, or shipped unchanged as if it were a custom design, scores 0 overall,
because the first is a legal exposure and the second is the generic default the
project was trying to escape.

## 10. Interfaces

- Upstream: `engineering-core`.
- Lateral: `design-authenticity` for judging a template's cleanliness,
  `design-system` for turning the template into the project's tokens,
  `ui-ux-engineering` and `frontend-engineering` for the customisation,
  `animation` for the motion the customised result carries,
  `dependency-selection` for the libraries the template pulls in.
- Run by: the design-research agent, and the ui-ux-engineer, before building.
