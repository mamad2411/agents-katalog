---
name: blog-writing-workflow
description: Use when planning, drafting, editing, or packaging a blog post, article, newsletter-style article, technical blog, thought leadership post, or research-backed post from provided ideas, notes, transcripts, outlines, sources, or verified research. Prefer this Skill when the work needs blog-specific angle shaping, outline, draft, voice, evidence, SEO metadata, publishing package, and quality gate. Do not use for official documents, formal reports, HTML reports, software UI, ad copy, social posts, CMS publishing, SEO ranking guarantees, AI-detector evasion, or unsupported factual invention.
meta:
  version: 1
  display_name: 博客写作工作流
---

# Blog Writing Workflow

## Purpose

Create useful, publish-ready blog/article drafts without binding to any MCP server, CMS, SEO SaaS, connector, OAuth flow, publishing pipeline, CLI, script, or external service.

This Skill owns blog workflow, angle shaping, outline, draft structure, editing, SEO metadata fields, publishing package structure, and quality gates. It does not own final factual authority, CMS publishing, live SEO data, search ranking outcomes, or AI-detector evasion.

## Trigger

Use when the user asks for:

- blog post, article, newsletter-style article, technical blog, thought leadership, research-backed post, developer blog, or opinion article;
- turning rough ideas, notes, transcripts, demos, meeting notes, research notes, code snippets, or verified source material into a blog draft;
- blog outline, blog brief, article skeleton, title options, hook, intro, section plan, draft, edit, review, proofread, or publishing package;
- blog-specific SEO metadata, slug, description, tags, categories, internal link suggestions, source list, or author-review checklist.

Prefer:

- `seo-content-strategy` for SEO strategy, keyword clusters, content briefs, search intent maps, and content refresh plans before a specific blog draft exists.
- `writing-and-editing` for general prose polishing when the output is not specifically a blog/article.
- `knowledge-base-article` for task-oriented help center, SOP, troubleshooting, FAQ, or support content.
- `html-report-builder` when the requested deliverable is a visual HTML report or PDF-ready HTML, not a blog/article draft.

## Non-goals

Do not use this Skill for:

- official documents, formal institutional writing, policy documents, contracts, or public statements requiring approval;
- HTML reports, slide decks, dashboards, software UI, landing pages, ad copy, social media posts, or short promotional snippets;
- CMS publishing, scheduling, uploading, deployment, analytics setup, Search Console, keyword tools, link building, or external API work;
- ranking guarantees, traffic guarantees, revenue guarantees, AI citation guarantees, or black-hat SEO;
- AI detector evasion, "humanizer" workflows, detector bypassing, or promises that text will beat AI detectors;
- inventing sources, statistics, examples, case studies, first-hand experience, quotes, benchmarks, dates, owners, or product behavior.

## Inputs

Before writing, identify:

- topic, working thesis, desired reader outcome, target audience, reading context, language, tone, and desired length;
- source material: rough notes, transcript, outline, research, links, files, examples, product docs, code snippets, screenshots, or user-provided experience;
- article type: how-to, tutorial, technical deep dive, opinion, thought leadership, research-backed post, case study, comparison, list, explainer, newsletter-style article, or post in a series;
- evidence state: verified sources, unverified claims, missing numbers, claims needing author input, and experience that must come from the user;
- publishing needs: markdown/frontmatter, title, slug, meta description, tags/categories, canonical URL placeholder, related links, image placeholders, source list, and review checklist.

If the task lacks enough substance to write honestly, ask the smallest necessary question or produce an outline with `needs input` markers.

## Output Contract

Return the artifact the task needs:

- blog brief;
- article outline;
- draft article in Markdown;
- edited article;
- proofread findings;
- SEO metadata block;
- publishing package;
- quality gate report;
- handoff checklist for author/CMS review.

For a complete publishing package, include:

- `title`;
- `slug`;
- `meta_description`;
- `summary` or `excerpt`;
- `tags`;
- `categories`;
- `audience`;
- `search_intent` if relevant;
- `draft_markdown`;
- `source_refs`;
- `claims_to_verify`;
- `image_alt_text` or image placeholders when needed;
- `internal_link_suggestions` if provided or discoverable;
- `author_review_checklist`;
- `publish_blockers`.

Do not publish, schedule, push, deploy, call CMS APIs, or claim ranking outcomes.

## Workflow

1. Classify the task: idea planning, brief, outline, draft, edit, proofread, metadata, or publishing package.
2. Capture audience, thesis, angle, voice, evidence, desired format, and constraints.
3. Check topic overlap if the user provides existing posts or a site corpus; otherwise do not assume access.
4. Interview lightly when needed: ask focused questions about the author's real experience, claim, scope, examples, and reader takeaway.
5. Select article type and structure.
6. Build an outline with section goals, evidence needs, examples, visuals, code/screenshot placeholders, and source gaps.
7. Draft section by section or full draft depending on user request.
8. Preserve facts and source boundaries. Mark missing material with `needs source`, `needs author input`, or `not verified`.
9. Edit for flow, structure, voice, evidence, clarity, and reader value.
10. Generate SEO metadata and publishing package fields when requested.
11. Run the quality gate before delivery.

## Voice And Audience Rules

- Match the user's requested language and voice.
- Preserve the author's actual perspective; do not simulate personal experience that was not provided.
- For technical blogs, prefer concrete examples, code, commands, architecture notes, screenshots, and before/after outcomes over abstract claims.
- Use one main idea per section and one topic per paragraph.
- Keep intros direct: hook, problem, stake, or story. Avoid generic openings like "In today's fast-paced digital landscape".
- Keep conclusions short and useful. Do not pad with a restated summary unless the format requires it.
- If the article is exploratory or "learning in public", preserve uncertainty and questions while still correcting errors that could mislead readers.

## Research And Evidence Rules

- Do not invent facts, sources, statistics, quotes, examples, experience, or case studies.
- Every statistic, legal/regulatory claim, market claim, performance number, benchmark, quote, or named-source claim needs a source or a `needs source` marker.
- Prefer primary sources, official docs, first-party data, original research, and directly inspected materials.
- Treat blogs, newsletters, forum posts, social posts, and secondary summaries as leads unless they are the object of analysis.
- Avoid source laundering: multiple articles repeating one upstream report count as one source cluster.
- For time-sensitive topics, mark freshness limits and dates. Do not present stale material as current.
- If web research is not available or not requested, produce a draft from provided material and label research gaps.

## Outline Rules

An outline should include:

- title options with angle notes;
- one-sentence thesis;
- target reader and promise;
- section headings with one-sentence purpose per section;
- evidence or examples needed per section;
- code, screenshot, diagram, or chart placeholders when useful;
- internal link opportunities if known;
- source gaps and questions for the author;
- CTA or closing direction if relevant.

Avoid outlines that are just generic H2 lists. Every section must carry a job.

## Drafting Rules

- Use Markdown by default unless the user asks for another format.
- Start with a hook and value promise, not a table of contents.
- Use H2/H3 hierarchy without skipped levels.
- Use short paragraphs and scannable sections.
- Use bullets for lists, not for carrying the whole argument.
- Use code blocks only when they clarify the article; keep long code as placeholders or excerpts.
- For transcript-derived posts, add placeholders for screenshots, code, links, facts, and diagrams that must be verified by the author.
- For opinion pieces, separate experience, interpretation, and recommendation.
- For research-backed posts, keep citations and caveats close to claims.
- Do not write "as an AI" disclosures unless the user explicitly wants an AI-assistance note.

## Editing Rules

When editing or reviewing:

- read the full draft before changing conclusions;
- identify the article's core purpose and flag scope creep;
- flag unsupported claims, weak logic, hand-waving, contradictions, repetition, and overbroad promises;
- preserve the author's voice while removing filler, generic phrasing, and unsupported certainty;
- check title, intro, section order, transitions, paragraph density, closing, and source visibility;
- for technical posts, check code snippets, commands, product names, version claims, image alt text placeholders, and verification markers;
- provide fixes, not only criticism.

## SEO Metadata Rules

SEO metadata is packaging, not a ranking promise.

When requested, provide:

- `meta_title`: concise, accurate, keyword-aware if a keyword is provided;
- `meta_description`: one sentence that states value without clickbait;
- `slug`: lowercase, hyphenated, short, and stable;
- `tags`: 3-6 focused tags;
- `categories`: broad buckets only;
- `excerpt`: short reader-facing summary;
- `canonical_url`: placeholder only unless supplied;
- `internal_links`: suggestions only, with anchor text and target rationale;
- `external_sources`: authoritative sources used or needed.

Do not stuff keywords. Do not promise ranking, traffic, or conversions.

## Runtime Boundary

It must not run shell, Python, Node, npm, curl, MCP, CMS, SEO SaaS, analytics, browser automation, package install, publish, deploy, or external API commands by itself; those actions belong to XAgent tools visible in the current session.

## Publishing Package Rules

A publishing package may include:

```yaml
title: ""
slug: ""
meta_description: ""
excerpt: ""
language: ""
audience: ""
search_intent: ""
tags: []
categories: []
canonical_url: ""
related_links: []
source_refs: []
claims_to_verify: []
image_placeholders: []
publish_blockers: []
```

Keep platform-specific fields generic unless the user provides a CMS or static-site convention. Do not call the CMS or write to a publishing system.

## Quality Gate

Before delivery, check:

- The article has one clear reader promise and one primary thesis.
- The first 150 words make the topic, stake, and reader value clear.
- Headings are meaningful and ordered.
- Sections do not duplicate or contradict each other.
- Claims that need evidence are sourced or marked.
- No invented first-hand experience, examples, data, sources, or quotes.
- No ranking, traffic, revenue, or AI-detection guarantees.
- No AI detector evasion or "humanizer" framing.
- Metadata is accurate, not clickbait, and not keyword-stuffed.
- Any publish blockers are listed.

## Integration With html-report-builder

Use `html-report-builder` only when the user explicitly asks to convert the article, content plan, editorial calendar, source audit, or quality report into a single-file visual HTML report or PDF-ready HTML artifact.

This Skill owns the blog/article content and publishing package. `html-report-builder` owns HTML visual packaging, print styling, chart/table presentation, and PDF compatibility.

## Failure / Escalation

- Missing angle: ask for the author's claim, reader, and example.
- Missing evidence: mark claims as `needs source` or produce a source-gap list.
- Weak or sprawling topic: propose narrower article options.
- Conflicting sources: show conflict and avoid forced conclusion.
- Sensitive claims, regulated topics, or legal/medical/financial advice: keep conservative, mark review needed, and avoid authoritative recommendations.
- User asks to publish or connect CMS/SEO tools: provide a publishing package and state that publishing belongs to visible XAgent tools or external workflow, not this Skill.
- User asks for detector bypass or guaranteed rankings: refuse that part and offer ethical quality, clarity, originality, and evidence improvements.

## References Reviewed

| source | candidate | fit_score | useful_patterns | dependencies_to_remove | risks | recommendation |
| --- | --- | ---: | --- | --- | --- | --- |
| `mdelapenya/blog-skills` | `blog-writer`, `blog-editor`, `blog-planner`, `blog-keeper`, `blog-marketer` | 5 | interview-driven angle shaping; topic overlap checks; front matter; related links; concise technical voice; review checklist | Hugo-specific paths, allowed-tools, AskUserQuestion, file writes, social promotion, published/scheduled link audits | personal blog conventions too specific; social distribution outside scope | adopt workflow patterns, adapt generic publishing package |
| `ComposioHQ/awesome-claude-skills/content-research-writer` | `content-research-writer` | 4 | collaborative outline; research to-do; hook improvement; section feedback; voice preservation; citation management | local writing folder setup, shell examples, implied live research | broad content scope; needs stronger fact boundary | adapt outline, hook, section-feedback patterns |
| `AgriciDaniel/claude-blog` | full blog engine and many sub-skills | 3 | template selection; quality gates; fact-check extraction; SEO checklists; evidence discipline; content templates | MCP, Python scripts, Google APIs, NotebookLM, image generation, CMS taxonomy, Vercel/deploy, command routing, agents, scoring automation | overfit to rankings/AI citations; strong external-system coupling; some claims too SEO/GEO-specific | reference-only for quality gates and article structures |
| `rmoff/rmoff-blog` | `proofread-blog` | 4 | direct critical proofreading; logic/scope review; learning-in-public exception; alt text; taxonomy consistency | Bash, ImageMagick conversion, AsciiDoc-specific fixes, site-specific links/categories | highly personal/site-specific; executable edits and image conversion out of scope | adapt proofreading stance and scope-creep checks |
| `aaron-he-zhu/seo-geo-claude-skills` | `seo-content-writer` | 4 | intent match; natural keywords; meta description; snippet-ready block; content templates; cite-or-flag rule | SEO connectors, Search Console, memory writes, handoff to other repo skills, external links in references | SEO/GEO scope broader than blog writing; connector assumptions | adapt SEO metadata and evidence boundary |
| `chouzz/chouzz-blog-writer` | `chouzz-blog-writer` | 4 | progressive section writing; language choice; style options; code organization; screenshot reminders | personalized Medium/Zhihu identity, platform-specific style guide | too personalized; not general XAgent skill as-is | adapt incremental writing and technical-blog placeholders |
| `jbaruch/blog-writer` | `blog-writer` | 3 | persona voice, transcript-to-blog workflow, placeholder numbering, anti-pattern review, source-material discipline | persona directory, symlinks, curl Wikipedia fetch, shell, global memory, series tracker, evals | AI-detector framing risk; heavy personal workflow; external fetch and file conventions | reference-only for voice preservation and placeholders |

Decision: create one XAgent `blog-writing-workflow` Skill with no bundled scripts, no external service dependencies, no CMS publishing, no ranking guarantees, and no AI detector evasion.
