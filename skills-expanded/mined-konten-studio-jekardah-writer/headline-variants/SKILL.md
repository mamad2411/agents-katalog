---
name: headline-variants
description: Use when a blog post, article, YouTube video, email, or long-form draft needs a set of title, headline, or subject-line options — distinct from the body's opening hook — including generation, scoring, and selection without inflating claims.
---

# Headline Variants

Generate and score title/headline/subject-line candidates for a piece of content. This is a separate deliverable surface from `hook-gokil`'s body-opening line: a headline is read before the body, often outside the body's context (search result, video thumbnail, inbox list), and must stay accurate to what the body actually delivers even when the body itself is not shown.

## Load only what you need

- Read [references/headline-patterns.md](references/headline-patterns.md) for the angle types, calibrated Indonesian examples, and when each angle is inappropriate.

## Non-negotiable truth contract

Treat the source draft/body as the claim ceiling for every headline, same discipline as `hook-gokil`.

1. Lock facts before generating: names, numbers, dates, scope, and the body's actual conclusion or outcome.
2. Never invent a number, ranking, timeframe, or outcome the body does not support.
3. Never let a headline promise something the body doesn't deliver — a headline is a contract with the reader, not just an attention device.
4. If the body's actual finding is modest, the headline may sharpen phrasing but must not claim more than the body proves.

## Core workflow

1. **Parse the request.** Deliverable (blog title, YouTube title, email subject, article headline), platform if supplied, desired count (default 5 if unspecified), and whether analysis, candidates, or a final selection is wanted.
2. **Build a fact lock.** Extract the body's actual conclusion, key numbers, and scope — this is the ceiling every headline must stay under.
3. **Choose angles.** Select from [references/headline-patterns.md](references/headline-patterns.md): benefit, curiosity gap, number/list, contrarian, how-to, and urgency-if-true. Skip any angle the body cannot support (e.g. no contrarian angle without an actual contrarian finding).
4. **Generate.** Produce the requested count across at least 3 distinct angle types. Keep the strongest concrete word early; respect the platform's effective display length if one is supplied (defer exact limits to `platform-format` when both skills are in play).
5. **Score.** Rate each candidate on clarity, accuracy-to-body (does the body actually deliver this), and click strength. Accuracy is a gate, not a weighted tradeoff — discard any candidate that overclaims.
6. **Select.** Name the strongest headline, its angle type, and a one-sentence reason it wins and stays accurate.

## Default output

1. Numbered candidates with angle-type labels.
2. `Pilihan terkuat:` followed by one headline.
3. A concise accuracy note confirming the body supports it.

For analysis-only requests, diagnose the current headline's weak points (vague, overclaiming, underselling, mismatched to body) and propose focused repairs without generating a full new set unless asked.

## Composition contract

- **Input owned by orchestrator:** source draft/body, fact lock, platform target, requested count.
- **This skill owns:** headline angle, candidate set, scoring, selected headline, and the accuracy-to-body check.
- **This skill returns:** `headline_candidates`, `selected_headline`, and `headline_accuracy_check` (`pass`/`fail` with reason).
- **Later passes (e.g. `platform-format`) may change:** exact length to fit a display limit, punctuation.
- **Later passes must not change:** the headline's factual claim or angle without re-running this skill's accuracy check.
- **Conflict order:** factual accuracy > user scope > click strength.

## Quality floor

Reject headlines that are generic/interchangeable with any other article on the topic, that promise a number or outcome the body doesn't contain, that bury the concrete word past the platform's visible-length window, or that contradict the body's actual conclusion.
