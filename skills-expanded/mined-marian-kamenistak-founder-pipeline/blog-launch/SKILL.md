---
name: blog-launch
description: "Use when the user wants a blog post produced end to end for one of their sites: \"write a blog post\", \"new article\", \"blog pipeline\", \"publish a post\", or a named topic for the blog. Covers brief, keyword and SERP research, draft, an 8/10 rating gate, images, localized mirror, internal links, deploy, syndication, backlinks and announcement. NOT for standalone social posts, newsletters or landing pages (`/founder-pipeline:web-site-creator`)."
---

# Blog Post — full production pipeline

> **Model: your top-tier model.** Reader-facing copy is where model tiers separate — cheaper models produce rule-compliant but AI-smooth output. If running in a lower-tier session, flag it; when dispatching this work to an agent, set the model to your top tier explicitly. Mechanical steps (file plumbing, deploys) may run cheaper. Name a tier, never a model codename: codenames age out of this file faster than the pipeline does.

One post, thirteen steps, two human gates plus a blocking privacy gate, one quality bar: if the post doesn't deliver value simply, it doesn't ship. Contrarian, personal, evidence-dense.

**Style north stars.** Pick three writers whose work you want the blog to read like, and name them here — the whole pipeline calibrates against them, so they need to be specific people you can go read, not adjectives. The worked example this skill was written against used one writer known for personal-story essays, one known for dense zero-filler posts, and one known for saying the thing without throat-clearing. `references/writing-style.md` carries the same three and should be edited to match whatever you choose.

## How to run this skill

**One step file at a time.** Read `steps/NN-*.md` for the current step only; never load all steps at once. References (`references/*.md`) are loaded only by the steps that name them.

1. Resolve the target site. Load its profile from `references/sites/<site-slug>.md` once (the "site profile"). Steps only ever refer to "the site profile", so a second site is another profile file and no other change.

   **`references/sites/` holds one config file per site you publish to.** `example-site.md` is the template: copy it, rename it to your site's slug, and fill it in for each of your own properties. Ship no site in this pipeline without a profile. A missing profile is not a small gap — it means no step 05 image contract, no step 09 verification and no gate, and the worked example this skill came from had exactly that failure: a second site with no profile had six posts authored outside the pipeline that reached production with one picture each and no thumbnails on either listing. If asked to write for a site with no profile, say so before starting, and either write the profile first or state plainly that the post is running unpiped. **Never silently substitute another site's profile.** Two sites in the same estate routinely differ in the details this skill cares about most — plain `.md` with an `image:` frontmatter field resolved through a content-collection image pipeline is a different contract from `.mdx` with a `heroImage` gallery slug, and a recipe written for one is wrong for the other.
2. Create/resume the workspace: `<site-repo>/.blog-pipeline/<slug>/` with `STATE.md` (YAML frontmatter + checkbox per step + gate approvals + scores), `brief.md`, `research/`, `skeleton.md`, `gate-report.md`, `exports/`. **Resume reads the frontmatter first** — `current_step`, `status`, `gate_a`/`gate_b`, `privacy_check`, and `pr` are the source of truth; the checklist body is the human log. If `STATE.md` exists for the slug, resume from `current_step` and update the frontmatter at every transition. A `status` of `blocked`/`paused` means stop and report `blocked_on`, never quietly resume.
3. Walk the pipeline map below. Run parallel branches via subagents/Workflow as each step file specifies.

## Pipeline map

| # | Step | File | Runs on | Parallel with | Gate |
|---|------|------|---------|---------------|------|
| 1 | Brief | `steps/01-brief.md` | main loop (session model) | — | **GATE A: the owner approves brief + angle — or a task-board row already promoted to `Ready`** |
| 2 | Research | `steps/02-research.md` | W1 workflow: 4× mid-tier | (internal fan-out) | — |
| 3 | Skeleton | `steps/03-skeleton.md` | main loop (session model, high) | — | FYI to the owner, non-blocking |
| 4 | Draft + citations + voice | `steps/04-draft.md` | main loop (session model, high) | step 5 | — |
| 5 | Images | `steps/05-images.md` | cheap-tier subagent | step 4 | — |
| 6 | Rating gate | `steps/06-gate.md` | W2 workflow: 3× session-model judges + `/founder-pipeline:critical` | — | auto-gate: median ≥8/8 |
| 7 | Translate | `steps/07-translate.md` | translation pass (session model) | steps 8, 10-prep | — |
| 8 | Internal links in | `steps/08-internal-links.md` | mid-tier discovery + main loop edits | steps 7, 10-prep | — |
| 8b | Privacy gate → PR + preview → reviewer | `steps/08b-review-pr.md` | main loop | — | **privacy gate: blocks on any hit** |
| 9 | Deploy | `steps/09-deploy.md` | main loop bash | — | **GATE B: the reviewer approves → the owner merges** |
| 10 | Syndicate | `steps/10-syndicate.md` | cheap-tier exports + browser automation | steps 11, 12 | — |
| 11 | Backlinks | `steps/11-backlinks.md` | mid-tier filter → `/founder-pipeline:web-backlinks` | steps 10, 12 | — |
| 12 | Announce | `steps/12-announce.md` | session model + `/founder-pipeline:brand-voice` | steps 10, 11 | — |

DAG: 1 →A→ 2 → 3 → (4 ∥ 5) → 6 → (7 ∥ 8 ∥ 10-prep) → 8b →B→ 9 → (10 ∥ 11 ∥ 12).

## Hard rules (apply to every step)

- **Two human gates, never skipped (hard rule).** **GATE A** = the brief is approved — either the owner's explicit word in-session, or their promotion of a blog-ideas backlog row on your task board to `Ready` by filling `Personal hook` + `Contrarian claim`. **GATE B** = the reviewer (a named delegate, or the owner if there is none) sets `Review` = `Approved` on the post's backlog row, **then the owner merges the PR** opened at step 08b. The reviewer owns the copy judgment, the owner owns the button. Everything else runs without blocking anyone, but nothing goes live, gets posted to an external platform, or leaves `draft: true` before the merge — a merged PR is the only form GATE B takes. The owner can override the review for a post they wrote themselves, but it's recorded as an override with their literal words, never a silent skip.

- **The reviewer works on the task board, not in GitHub (hard rule).** The reviewer reads the rendered deploy preview and comments on the post body pasted into the board card. The PR is plumbing — preview, diff, merge — and they never open it. This is deliberate: it means the reviewer needs **no repo access**, so briefs and raw research (which hold the client detail the privacy gate exists to catch) never leave the owner's account.

- **Privacy gate (hard rule — blocking).** If the blog's material comes from live client, mentee or prospect relationships, a post can out a real person's employer, situation, or the mere fact that they are being advised at all. Step 08b runs the gate before the PR is opened, and **again before step 10 syndication** — a Medium or Hackernoon copy can't be quietly edited later the way a site post can. It checks two things: **scanned** (company names, real first/last names, role+company combinations, tenure+size+industry combinations specific enough to identify one person) and **declared** (any `⚠️ Guardrail` block the draft carries about its own sourcing — a short block the writer adds at the top of a draft naming who the story is about, what was changed to protect them, and whether consent was given). Any hit sets `privacy_check: blocked` in `STATE.md`, raises an alert on whatever channel you use for blocking failures, and stops the pipeline. Never flag-and-continue, never resolve a guardrail by guessing at consent.
- **The 8/10 bar (hard rule — no silent exceptions).** The post ships only if the judge panel medians are ≥8/10 on BOTH Simplicity and Value Delivered (see `references/rating-rubric.md`). Below the bar after 2 revise rounds: hard stop, present the owner kill / park / override-publish. Override requires their literal words and is logged in `STATE.md`. Never silently publish, never silently delete.
- **Don't go cheap on copy (hard rule).** Writer, judges, the `/founder-pipeline:brand-voice` pass, and the translation pass always run on the session model at high effort. Only mechanical work (image lookup, export formatting, research fan-out) runs on cheaper models. The draft is written by ONE agent in ONE context; per-section parallel drafting is forbidden — it kills narrative arc and voice coherence.
- **Personal or it's generic (hard rule).** Every post carries at least one personal story ("it happened to me", a client with a changed first name, a scar with a date) or a named real example. A post that could have been written without the owner's life in it fails the gate.
- **Every claim cited or cut (hard rule).** Numbers, names, dates carry an inline link or come from your own verified data-points store (a single file or database holding the stats you are allowed to cite about your business, with the date each was last verified). Counter-voices get cited fairly, then rebutted. No invented stats, testimonials, or stories.
- **No vague quantity words (hard rule).** "Many", "few", "often", "rarely", "most", "some" don't get quoted by AI search — LLMs and Google AI Overviews lift specific numbers, not qualitative hedges. Every quantity claim gets a real, sourced number instead. Dispatch a subagent to find a valid source for it (step 04 mechanic), then cite it inline as `[the number itself](source URL)` — the house convention — or list the source in an "Appendix: Sources" section below the post if the number can't sit naturally in the sentence. No source found → cut the claim; don't fall back to the vague word.
- **`draft: true` until GATE B (hard rule).** The MDX file carries `draft: true` from creation. The flip to `false` happens in the merge commit — so an unmerged or abandoned post is invisible on the live site by construction. This is the pipeline's safety net: if the automation ever misbehaves, nothing publishes.
- **Title tag = `{post title} | {service}`, not the site name (hard rule).** Composed automatically from `tags` via the shared service map (the site profile has the exact mechanism); choose tags in step 04 knowing they decide this suffix too, not just the CTA.
- **Featured-image contract (hard rule).** Every post — the original *and* every localisation — ships with a featured image that is (1) unique against every other live post in that language, (2) present on the mirror in its own right, not inherited from the original, (3) resolving to a real og:image and a real index-card thumbnail, and (4) carried into the post's `BlogPosting` JSON-LD as `image`. One frontmatter field feeds all four surfaces, so they fail together and get checked together. Contract + selection rules in `steps/05-images.md`, mirror rules in `steps/07-translate.md`, live verification in `steps/09-deploy.md`. A post whose og:image resolves to the generic site fallback has failed this rule and does not ship.

- **Three pictures minimum, and the body carries at least two (hard rule).** Every post, the original *and* every localisation, ships with **≥3 images: the featured one plus ≥2 in the body.** The featured image is not one of the body two — it renders as the hero, the card thumbnail and the og:image, and a reader scrolling the article never meets it again. This is a **count, verified in the built output** at `steps/09-deploy.md`, not a judgment call at draft time. It exists because the old wording ("on top of the hero, add 1-2 inline images") was prose inside a selection step, nothing downstream counted, and an entire site's worth of posts shipped with exactly one picture each while passing every other gate. Site-agnostic: the frontmatter field and the body syntax differ per site profile, the count does not. If a post genuinely has nowhere for a second body image, that is a skeleton problem to fix in step 03, never a clause to waive here.
- **Dates state content change, nothing else (hard rule).** A post's last-modified date moves only when a human revises the content. Never on a rebuild, deploy, git commit, or cosmetic sweep. Old dates are safe — there is no penalty for an honest 2020 date — but a noisy `lastmod` makes Google discount the signal across the whole site. Full policy, per-page-type date sources, and the checks: `references/dates-and-freshness.md`. Read it before any bulk edit to `src/content/blog/` and before agreeing to anything phrased as "refresh the dates".
- **Technical SEO contract (hard rule).** Every post ships with: `robots` = `max-image-preview:large, max-snippet:-1`; `article:modified_time` always present; `BlogPosting` carrying `dateModified`, `wordCount`, `timeRequired`, `isAccessibleForFree`, an `ImageObject` image, a `publisher.logo`, and `author` as an `@id` reference to the site Person node (never an inlined duplicate); `srcset` on every listing thumbnail; an honest `<lastmod>` in the sitemap or none at all. Verification commands in `steps/09-deploy.md`. Structured data may only assert facts that are true — never hardcode image dimensions you have not measured.
- **Reading layout contract (hard rule).** Presentation is CSS and template level, never per-post. The post body is one `<div class="post-body">` styled in `src/styles/global.css` (44rem measure, 17/19px, 1.75 line-height, headings pulled toward the text they introduce); every markdown table is wrapped by `rehypeWrapTables` in `astro.config.mjs` and styled with an accent header band, zebra rows and horizontal scroll; blog index cards are one full-width row per post with a **24px title**, featured image, abstract and tag pills. **Never paste typography classes or raw table markup into an `.mdx` file** — if a post needs custom styling to read properly, the contract has a gap, so fix the contract and every post benefits. Full spec and the build-output verification commands: `references/reading-layout.md`. This rule exists because the template previously carried its styling as an inline `[&_h2]:…` string that had no table rules at all, so every post with a table rendered at browser defaults.
- **Voice delegation.** Sentence-level humanization (banned AI words/phrases, no em dashes, no smooth transitions, grep self-check) is `/founder-pipeline:brand-voice`'s job and is mandatory in step 4. Essay-level structure lives in `references/writing-style.md`. Don't duplicate either.
- **Context budget.** Steps loaded one at a time; research raw JSON stays on disk in `research/`, only synthesized conclusions enter the main window.

## Skill routing

| Need | Skill |
|---|---|
| Sentence-level humanization, your brand voice | `/founder-pipeline:brand-voice` (mandatory in step 4) |
| Adversarial strategy check | `/founder-pipeline:critical` (runs in step 6) |
| AI-citability + on-page checks post-change | `/founder-pipeline:ai-seo` + `/founder-pipeline:seo-audit` (step 9) |
| Getting the published URLs discovered | `/founder-pipeline:web-indexation` (step 9) |
| Backlink outreach execution | `/founder-pipeline:web-backlinks` (step 11) |
| Persuasion/psychology pass on the CTA framing | `/founder-pipeline:marketing-psychology` (optional, step 4) |

Four things this pipeline calls for that ship as **inline instructions rather than skills**, because the plugin does not carry a skill for them. If you have your own skill for one, route to it instead:

- **Imagery — sourcing, counts, optimisation, alt text (step 05).** The count is a hard rule above (featured + ≥2 body). Beyond it: prefer real photographs you own over stock; never use an image you cannot say why it sits in that particular section; write alt text that states what the image shows, not what the section argues; export at the widths the template's `srcset` actually requests and no larger.
- **Domain terminology (step 04).** If your business uses terms of art whose distinctions matter commercially — two product tiers that are routinely confused, a word your industry uses differently than the public does — keep a one-page glossary in your brand context and make reading it mandatory for posts on those topics. Getting these wrong in public is a credibility cost, not a style one.
- **Localized mirror (step 07).** Translate for the target market rather than the target language: localized slug, localized examples, and terminology from the site's `TRANSLATION-GLOSSARY.md`. A machine-translated mirror ranks worse than no mirror.
- **Social announcement drafts (step 12).** Draft in your brand voice via `/founder-pipeline:brand-voice`, one post per platform, each carrying a distinct hook rather than the same paragraph reposted.

Charts in a post are worth having only if the post carries data that earns a figure. If you have a data-visualization skill installed, use it; otherwise a clean markdown table beats a bad chart, and the table is what AI search engines lift anyway.

## Modes

- **Default:** step-by-step with the two gates; steps 3 and 6 post their outputs to the owner as FYI without waiting.
- **"Run it through":** same gates, zero FYI pauses; the owner sees the brief and then the complete pre-deploy package (draft + gate report + localized mirror + syndication plan) at GATE B.
