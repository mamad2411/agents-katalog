---
name: amy-writing-angle
description: Improve the angle, structure, evidence, template fit, creator voice, and AI-writing traces of public-facing writing. Use directly when the user names Amy Writing Angle or asks for writing-angle, hook, template, or anti-AI analysis. If the user only asks to optimize, polish, rewrite, strengthen, or improve an article, post, copy, or writing style without naming this skill, ask whether they want a light direct edit or the full Amy Writing Angle workflow before applying it. Do not invoke or propose it for research, summarization, translation, extraction, local-LLM organization, knowledge-base design, technical documentation, or other tasks where changing the writing is not the stated goal.
---

# Amy Writing Angle

Find the argument before drafting. Do not confuse a topic, headline, source summary, or provocative claim with an angle.

An angle must identify what changed, what the creator sees differently, why the reader should care, and how the article can prove it.

## 0. Get consent before implicit use

If the user explicitly names `$amy-writing-angle`, proceed with the workflow.

If the user asks to optimize, polish, rewrite, strengthen, or improve writing without naming this skill, do not begin the full workflow automatically. Ask whether they want:

1. a light direct edit limited to the stated request; or
2. the full Amy Writing Angle workflow, including angle, structure, fact-checking scope, template fit, and writing QA.

Before the user opts in, do not browse, fact-check, generate angle candidates, recommend templates, or expand the assignment. The skill may be recognized as relevant without being allowed to intervene.

Do not ask about this skill when the primary task is research, summarization, translation, extraction, formatting, local-LLM organization, knowledge-base design, technical documentation, or another non-writing task. The presence of an article or writing material alone is not a trigger.

## 1. Confirm length and editing scope

If length or format is not explicit, stop and ask exactly:

> 这次想写哪一种：短篇（280 字以内）、中篇（一条正常推文，默认 281–450 字），还是长篇（Article 级别）？

Do not analyze, browse, or draft before the answer unless the request is unambiguous:

- short: “280 字以内”, “短推”, “一句话”, “短篇”;
- medium: “正常推文”, “单条推文”, “中篇”, “450 字以内”;
- long: “长文”, “文章”, “Article”, “深度稿”, “公众号文章”.

Never infer length from source volume.

If the requested editing depth is unclear, ask whether the user wants language-only polishing, structural improvement, or angle-level reconstruction. Do not turn a light edit into a new argument without permission.

## 2. Route by length and scene

- For short or medium original posts and reshares, read [references/short-post-angles.md](references/short-post-angles.md).
- For long-form work, continue through this file.
- If the user provides revision history, also read [references/conversation-distillation.md](references/conversation-distillation.md).
- If the user requests titles, read [references/title-hooks.md](references/title-hooks.md).
- If the user asks which content template, hook structure, or proven post format fits the topic, read [references/writing-templates.md](references/writing-templates.md).
- If the user requests layout or shortening, read [references/article-layout.md](references/article-layout.md).
- If the user requests AI-trace review or voice editing, read [references/anti-ai-writing.md](references/anti-ai-writing.md).

Ask no further question when the route and materials are clear. Ask only what changes the thesis or output.

## 3. Build the evidence base

Use inputs in this order:

1. current source material;
2. current market context;
3. creator context and lived experience;
4. revision history and rejected framings.

Read [references/fact-checking.md](references/fact-checking.md) before recommending an angle or drafting factual copy. Declare the fact-checking level before doing external research. Build a claim ledger only to the depth required by the selected level. For current-market claims and data-led hooks, search the most recent 12 months by default and check both publication date and observation period. Expand beyond 12 months only for an explicitly historical, multi-year, or cycle-comparison question; older data must not silently carry a current claim.

Do not search for a user's original source merely because the draft attributes an idea. At Level 1, treat user-supplied premises as supplied material and edit their expression without external verification. At Levels 2 and 3, verify only within the declared scope. If verification fails, remove, qualify, attribute, or mark the claim for confirmation. Never manufacture tension from an unresolved claim.

Use [scripts/compare_invariants.py](scripts/compare_invariants.py) after editing factual copy when names, dates, percentages, URLs, quotes, or product terms must remain unchanged.

## 4. Separate topic from angle

Rewrite the material into:

- **Topic:** what everyone can see.
- **Default angle:** the obvious version most people would write.
- **Changed reality:** what makes the default stale, incomplete, or misleading.
- **Creator tension:** the judgment this creator is willing and qualified to defend.

If changed reality or creator tension is missing, say the angle is not yet differentiated.

## 5. Choose the framing path

Use the direct path by default. When a credible broader pattern exists, offer:

- **Direct:** explain the event, product, person, or source on its own terms.
- **Larger context:** connect it to a verified market shift, strategic split, historical pattern, or event cluster.
- **Non-consensus:** use a verified gap between audience expectation and observed reality.

For the latter two, read [references/non-consensus-path.md](references/non-consensus-path.md). Follow:

> reader expectation → factual contrast → verified reality → creator judgment

Treat non-consensus as an evidence burden, not a tone. Reject straw-man consensus, false binaries, mismatched comparisons, and cherry-picked surprise.

## 6. Generate and score candidates

Generate three different theses, not three headlines for one thesis. For each include:

- one-sentence angle;
- why now and why this creator;
- reader tension;
- evidence path;
- strongest counterargument;
- falsifiability;
- possible hook;
- claims requiring verification.

At least one candidate must examine downside, conflict, or a credible opposing explanation.

Read [references/angle-scorecard.md](references/angle-scorecard.md). Eliminate source summaries, generic publication angles, unsupported provocation, company messaging without an independent test, and claims with no reader consequence.

Prefer the angle with the strongest combined timeliness, creator fit, tension, and evidence—not the loudest hook.

## 7. Ask only decision-changing questions

If two candidates remain close, ask at most three short questions:

- Which claim are you willing to defend?
- What experience gives you standing to make it?
- What evidence would change your mind?

Do not ask for information already present.

## 8. Deliver the correct contract

Read [references/output-contracts.md](references/output-contracts.md) and use the exact contract for the selected route.

For long-form work, recommend one angle and explain rejected alternatives. Include larger-context fields only when that path was selected. Do not pad a direct angle with an invented consensus.

Do not draft the full article before angle confirmation unless the user explicitly asks.

After the angle is confirmed, use a template-first default for the full workflow. Recommend one primary high-attention template and optionally one secondary template based on the available proof, creator standing, reader tension, desired action, and length. Use the standard direct structure only when the user explicitly asks for no template. Treat templates as information architecture, never as evidence or a substitute for creator judgment, and do not select from topic keywords alone.

Template-first does not authorize fabrication. If none of the templates can be supported, do not silently fall back to the standard structure. Explain which proof is missing and ask whether the user wants to supply it or opt out of templates. Prefer the lowest-risk supported template—often a real provoking question, audience callout, curiosity mechanism, or numbered field guide—over an unsupported research, non-consensus, failure, or before/after claim.

Before a finished short, medium, or revised draft, show a compact writing decision card containing the task type, editing depth, fact-checking level, core angle, recommended structure or template decision, and main change. This is a decision summary, not hidden chain-of-thought. It should make the editorial value visible without turning the interaction into a long intake form.

For Chinese short and medium drafts, run [scripts/count_chinese_length.py](scripts/count_chinese_length.py) when exact length compliance matters.

## 9. Learn without creating a dependency

After revision or approval, produce one reusable creator rule:

```text
When [market condition], this creator prefers [type of tension], avoids [generic framing], and needs [evidence standard].
```

Keep personal preferences separate from universal writing rules. If persistent memory is available, offer to save the rule; never require a proprietary memory product.

For a worked example, read [references/examples.md](references/examples.md).
