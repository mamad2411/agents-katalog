---
name: design-authenticity
description: Detects the cluster of generic defaults that make an interface look machine-generated rather than designed: the same gradients, glass panels, bento grids, default fonts, hover-everything motion, and the fabricated testimonials and empty pricing tiers that come with them. Reads each as a signal, not a verdict, and tests the one thing that separates a template from a design, whether a choice was made on purpose. Use when a site looks assembled rather than intended, and before shipping a public page.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core]
  outputs: [authenticity-findings, cluster-assessment, intentionality-gaps]
---

# Design Authenticity

There is a look that a generated interface falls into when nobody decided
anything: a violet to black gradient, a pane of frosted glass, a grid of
rounded cards, one of two fonts, a blurred orb in the corner, and something
that animates on every hover. None of these is wrong on its own. A violet
gradient can be exactly right. What makes the look a problem is the cluster,
and what the cluster reveals: that the defaults were accepted rather than
chosen, and that the product has no visual identity of its own because no one
gave it one.

This skill detects that cluster and, for each signal in it, asks the only
question that separates a template from a design: can the person who built it
say why this choice, for this product, rather than the default. It is not a
list of banned elements. It is a way of finding where intent is missing.

## 1. The principle, stated once

A tell is a signal, not a verdict. A single rounded card proves nothing; a
whole page of the signals below, with no answer to why any of them are there,
is the verdict. The test is intentionality: a good designer using a gradient
can say what it evokes, why those colours, why here. A generated default has
no such answer, because no one was asked.

The skill never says remove all rounded corners. It says: this choice looks
inherited rather than made; if it was made, state why, and if it was not,
make it, or replace it with something that fits this product.

## 2. The visual tells

Each is a signal. The severity is the size of the cluster, not the presence of
any one line.

| Tell | What it usually means |
|---|---|
| Violet, indigo or purple-to-black gradient | the default accent nobody changed |
| Pure white or pure black flat background | no considered ground colour |
| Neon on dark, or a full rainbow spread | colour chosen for effect, not meaning |
| Faded pastel wash | the other default, when not the neon one |
| A single saturated band across a section | a divider standing in for a layout decision |
| Bento grid of feature cards | the default way to arrange things that were not arranged |
| Everything on the same rounded corner radius | one radius applied without a scale |
| Drop shadow on every surface | depth with no hierarchy behind it |
| Frosted glass panels, liquid glass | the season's default material |
| Dot grid or blurred orbs in the background | decoration filling space intent did not |
| A star or sparkle icon on anything AI-adjacent | the default mark for nothing in particular |

## 3. The typography and motion tells

| Tell | What it usually means |
|---|---|
| Geist or Space Grotesk with no reason given | the default font of the default stack |
| A heading with an emoji in it | tone standing in for hierarchy |
| Every interactive element animates on hover | motion applied globally, not designed |
| Arrows that slide on hover, everywhere | the same micro-interaction copied to every link |
| A transition on everything, including what should be instant | motion as a default, not a choice |

Motion has its own rule that this skill enforces alongside the tell: any motion
present must respect `prefers-reduced-motion`, and a page that animates
everything and honours that preference nowhere fails on accessibility grounds
regardless of taste.

## 4. The content tells, which are not only aesthetic

These are the ones that cross from taste into honesty, and they are the more
serious for it.

| Tell | Why it is worse than a visual default |
|---|---|
| Testimonials from people who do not exist | a fabricated endorsement is a lie on the page, not a style |
| Metrics or logos presented as real but invented | the same, and it is the kind of claim a regulator reads |
| The "it is not X, it is Y" construction, repeated | a rhetorical default standing in for a real value proposition |
| A green check list of features that do not all exist | overlaps with fake functionality; a checked item is a claim |
| Three generic pricing tiers for a product with no pricing | a template section shipped because the template had one |
| No actual product, screenshot or demo anywhere | the page sells a thing it never shows |

A fabricated testimonial is handed to `implementation-integrity` and treated
as a truthfulness defect, not a design note. This skill flags it; it does not
soften it.

## 5. Reading the cluster

```
0 to 2 tells, each with a stated reason        authentic, intent is present
several tells, no reason for any               generic, the defaults were accepted
a content tell from section 4                  a separate, more serious finding,
                                               raised regardless of the visual count
```

The count is the visual verdict. A single content tell from section 4 is its
own finding and does not wait for a cluster: one invented testimonial is a
problem on a page that is otherwise well designed.

## 6. What the finding says

For each tell present: where it is, which signal it is, and the intentionality
question put concretely. Not "remove the gradient" but "the hero uses the
default violet-to-black gradient; if it is meant to evoke something for this
product, name it; if not, choose a ground that fits the brand." The finding
proposes the decision, it does not impose a specific replacement, because the
replacement is the designer's to make and depends on an identity this skill
does not own.

## 7. What this skill refuses

- Declaring a single element wrong. Every line in sections 2 and 3 can be the
  right choice; the finding is about the cluster and the missing intent.
- Prescribing a specific replacement palette, font or layout. It names the
  gap; the identity is the project's.
- Softening a section 4 content tell into a matter of taste. A fabricated
  testimonial is a truthfulness defect.
- Passing a page that animates everywhere and honours reduced motion nowhere,
  whatever its aesthetic.

## 8. Protocol

1. Establish the product's own identity if one is stated: brand, audience,
   the feeling it should give. Without it, intentionality can only be asked,
   not judged, and the finding says so.
2. Inspect the rendered page, not only the source: the actual colours, fonts,
   shadows, motion and content a visitor sees.
3. Record each tell from sections 2, 3 and 4 that is present, with its
   location.
4. Assess the cluster per section 5, and raise every section 4 content tell as
   its own finding regardless of the count.
5. For each, put the intentionality question concretely, per section 6.
6. Hand every fabricated-content tell to `implementation-integrity` as a
   truthfulness defect.
7. Check that any motion present respects `prefers-reduced-motion`, and fail
   the page on that ground if it does not, separately from taste.

## 9. Auto-critique

Score from 0 to 5: no single element was condemned in isolation, the cluster
was assessed rather than a tally waved as a verdict, intentionality was tested
against the product's stated identity where one exists, content tells were
raised as truthfulness defects rather than taste, no specific replacement was
imposed, reduced motion was checked.

Threshold: no axis below 3, average at least 4. A finding that condemns one
rounded corner as vibe-coded scores 0 on the first axis and is rewritten,
because it mistakes a signal for a verdict.

## 10. Interfaces

- Upstream: `engineering-core`.
- Lateral: `ui-ux-engineering` for the rendered experience it judges,
  `design-system` for the tokens a real identity would define,
  `frontend-engineering` for the implementation, `accessibility-testing` for
  the reduced-motion and contrast overlap, `implementation-integrity` for the
  fabricated-content defects.
- Run by: the design-verification agent (an agent, named without backticks
  here because it is not a skill).
