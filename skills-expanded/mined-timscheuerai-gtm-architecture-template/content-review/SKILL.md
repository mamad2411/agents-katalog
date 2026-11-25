---
name: content-review
description: Review published content, platform performance and the production workflow, then turn the evidence into the next experiment. Use for a YouTube review, a content retrospective, why a piece underperformed, or a review across platforms.
---

Workspace: all context paths below (identity, audience, strategy, voice, brand, raw, output, index, log, workspace preferences and context scripts) resolve from `context/` in the kit root. Read both the root `AGENTS.md` and `context/AGENTS.md`. Skill-local `references/` and flowchart `scripts/` resolve from this skill directory.

# Content review

Review the whole path: audience need, idea, packaging, opening, delivery, distribution, response, product outcome and production effort. The output is a decision, not a list of metrics or an automatic rewrite of the content strategy.

## Choose the review

Use the platform, account, piece and dates supplied. Without dates, review the last 28 days plus the previous comparable period; with few uploads, widen the window and label it. A single-piece request stays a single-piece review, with channel context.

| Platform | Keep its native context |
| --- | --- |
| YouTube | Long-form, Shorts and live separately; impression source, package, retention, next action |
| LinkedIn | Personal and company, organic and paid, and format separately; reach, substantive response, resource requests, product outcomes |
| X | Originals, replies, threads, Articles and paid separately; distribution, profile and link actions, useful conversations |
| Newsletter | Delivered audience, clicks, replies, unsubscribes and product outcomes; opens may be distorted by privacy protection |

Never add different platforms' view definitions into one audience total.

## Ground and collect

Read the positioning, ideal follower, funnel and content-waterfall pages and the previous review. Prefer live native account reads, then dated native exports, then snapshots. Public counters cannot replace owner analytics. Verify the account, timezone, window and access before concluding anything.

For each piece keep its ID or URL, format, publication and observation dates, goal (Reach, Belief or Signup), source and metric window. Record a coverage table: available, stale, denied, unavailable or not applicable. Missing is not zero. If a field is blocked, continue and name the smallest missing input. Collect first, then diagnose; save new captures under a dated `raw/sources/` folder with a manifest, without secrets or customer data.

## Make it useful

Use [the report shape](references/report.md). For each material finding give the evidence, confidence, an alternative explanation, the practical change and the next observation. Review together: audience and idea, promise and delivery, distribution and response, product outcome (keep first-touch, assisted and self-reported separate) and production effort (actual time, runtime, waits, revisions). Separate measured facts, interpretations and hypotheses; compare like with like; keep inconclusive tests inconclusive.

End with the most consequential constraint, what to keep and a few experiments the next cycle can run. Each experiment needs a hypothesis, a changed variable, a goal metric, a comparison, a review point and a keep, change or inconclusive rule.

## Close the loop

Save the report under `research/reviews/YYYY-MM-DD-<platform-or-waterfall>.md` with frontmatter and Source Notes. Check every public result against the cleared table in `identity/proof.md` and label anything else as internal. Update the performance page and test log only when new evidence resolves a result. Propose skill or prompt edits with their evidence; apply them only when asked.
