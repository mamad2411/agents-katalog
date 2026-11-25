---
name: figure-audit
description: Decide whether a given article should get a figure at all — additive, performative, or none — against a five-type taxonomy where each type has a hard entry requirement. Use when Shane says "should this post have a diagram", "audit these articles for figures", "does this need a chart", or before commissioning any illustration for written work. Do NOT use to build the figure once approved (use the design artifact skills), to audit an existing figure's styling, or for social artifacts, which are decorative by design.
---

# Skill: /figure-audit [article path]

Answer whether a figure earns its place, applying the standard that most articles should get none — the value is in the rejections, not the approvals.

**Don't:** invent the data a figure would need; if the article does not contain the numbers, the verdict is not additive, full stop. **Don't** approve a figure that restates the thesis in boxes — that is the exact failure this guards against. **Don't** audit several articles in one agent; it starts pattern-matching the second against the first and stops reading.

## The standard

> If the page is no worse without the figure, cut the figure.

Prefer `none`. Reaching for a figure to fill space is the failure mode.

## The taxonomy

A figure may ONLY be one of these five types, and ONLY if it meets its entry requirement.

| Figure | Use it for | REQUIRES |
|---|---|---|
| Dimensioned diagram | A claim about proportion, or where a line sits | Two regions and a measured split you can defend |
| Cycle | A process with a genuine return edge | Three or more stages AND a real loop back |
| Record chart | A claim about the author's own history or data | A file it reconciles to, named in the caption |
| Detail | Clarifying one step of an assembly | A step that is actually unclear without it |
| Footed table | Anything with numbers, including pricing | Figures that add up, shown adding up |

Hard limits: **max one figure per article**, max three callouts per figure. Zero figures is a perfectly good answer.

## Rules

1. **No invented data.** `groundedIn` must quote or cite something actually in the article.
2. **Record chart** needs a real file it reconciles to. Do not claim reconciliation you cannot verify.
3. **Cycle** needs a genuine return edge. A linear process with steps is not a cycle.
4. **Dimensioned diagram** needs a defensible measured split — an explicit percentage or ratio stated in the article. A vibes-based split is not defensible.
5. **Prefer `none`.**

## Steps

1. Read the project's `DESIGN.md` figure section — if it defines a different taxonomy, that file wins over the table above.
2. Read the article **in full**. Not the intro, not a grep.
3. Test each of the five types against its entry requirement, in order. Stop at the first that genuinely passes.
4. Return the verdict.

## Output

```
slug:            <slug>
verdict:         additive | performative | none
figureType:      <one of the five, or null>
depicts:         <name the actual regions / stages / values — not "the process">
entryRequirement: <how it is met, or which requirement each type failed>
groundedIn:      <quote or cite from the article>
```

`none` still fills `entryRequirement` — say which requirement each type failed. A bare "none" is not reviewable.

## Fan-out

One agent per article, in parallel, each blind to the others. When auditing a set, follow with a single skeptic pass over the collected verdicts to catch a reviewer who drifted lenient.
