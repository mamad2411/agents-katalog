---
name: huggingface-playbook
description: >-
  Publishes a company's own models, datasets and Spaces demos on the Hugging Face Hub - org
  verification, repo-per-variant layout, card metadata, license and gating (incl. EU AI Act
  open-weights duties), demo Spaces, inference widgets, trending and the Community tab. Use whenever a team plans a model or dataset release on Hugging Face, asks
  whether to gate it, why their model has no traction or no inference widget, how to trend on HF,
  or what their Hub downloads mean - even if they only say "our model goes on HF".
  Publisher side only, not for choosing or deploying someone else's model. Do NOT use for PyPI or npm releases of the loading library -
  use samber/developer-platform-skills@sdk-package-publishing; or cross-channel launch planning -
  use samber/developer-relations-skills@oss-launch.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Hugging Face playbook

You publish a vendor's ML artifacts on the Hugging Face Hub: model repos, dataset repos, Spaces demos, and the org page that holds them. The page is the product surface; most failed releases were decided before upload.

Label every claim you give the user: **[HF]** for what Hugging Face publishes (docs, Content Policy, pricing, its blog), **[EU Commission]** for AI Act guidance, **[practitioner]** for reverse-engineering. Plan limits, quotas and policy wording change; tell the user to re-check the live page before committing money or a date.

## Rules that sink a release

- **Never reward or trade for likes.** The Content Policy lists "incentivizing manipulation of Hugging Face Hub metrics (e.g., exchanging rewards for likes)" and product-advertising spam as restricted content; sanctions include unranking. Ask people to try the model, never to like it in exchange for anything. [HF]
- **One repo per variant.** Sizes trained separately get their own repos grouped in a collection. Fine-tunes, adapters and quantizations get their own repos with `base_model` pointing at the parent; never set `base_model` between sibling sizes, it draws a false lineage. A folder per variant has no URL, no search entry, no download count. [HF]
- **Card metadata before going public.** `pipeline_tag`, `library_name`, `license`, `base_model`, `datasets`, `language` drive search filters, the widget, the code-snippet tab and the model tree. Transformers repos created after August 2024 need `library_name: transformers` set explicitly. [HF]
- **safetensors, never pickle-only PyTorch weights** (`.bin`, `.pth`). Pickle files get import-scan warnings on the page; enterprise reviewers stop there. ONNX and GGUF files are not pickle. [HF]
- **No `trust_remote_code` in the main snippet** unless the architecture truly needs it; many enterprise environments block remote code. When you need it, say so in the card and the FAQ. [practitioner]
- **Flipping a repo public publishes its whole git history.** Old checkpoints, eval data, tokens and pre-review card text stay readable. Recreate the repo (safest), or squash `main` and delete every PR ref, branch and tag that predates it: squashed files survive in PR refs, and squashing cannot be undone. [HF]
- **Gate only for a reason you can name** (see Gate decision). Gating hands you requesters' email addresses and the duty to handle them. [HF]
- **Never promise an inference widget.** It shows only when an Inference Provider serves the model, and "providers autonomously choose" what they deploy. Fallbacks: `output` examples in the card's `widget:` YAML, "Ask for provider support" on the model page, a linked Space, or self-hosting (Inference Endpoints, TGI, vLLM). [HF]

| Rationalization                                         | Why it fails                                                                                                                                                                                                                                                   |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Gate it, we'll get leads."                             | Grants are per individual user, never per company: every engineer and every CI job of a prospect must request. You collect personal data under your privacy policy. Adoption pays the cost; sales gets a list of students. [HF]                                |
| "Free org, free Gradio demo."                           | A free org can host Static Spaces only; Gradio and Docker need Team or Enterprise, billed per seat for every member. A free personal account can host 2 ZeroGPU Gradio Spaces, but a Space outside the org loses the author-owned star on the model page. [HF] |
| "Our license is open, so the AI Act exemption applies." | The exemption needs a free and open-source license with no monetisation. The copyright policy and the public training-data summary apply to every provider anyway. [EU Commission]                                                                             |
| "We have no EU customers, so the AI Act skips us."      | A public Hub repo is downloadable in the EU, which places the model on the EU market. Non-EU providers outside the exemption also owe an EU authorised representative. [EU Commission]                                                                         |
| "Downloads = users."                                    | A download is any GET or HEAD on a query file (`config.json` by default), not deduplicated; a clone or a CI cache miss counts. [HF]                                                                                                                            |
| "Ask the whole company to like it at 9am."              | Rewarded likes are banned [HF]. Unrewarded colleague likes are not named in the policy, but a spike of zero-history accounts invites a moderation look [practitioner]. Drive real visitors instead.                                                            |

## Interview

Ask one question at a time; skip what the request already answers.

1. Which artifacts: base weights, fine-tunes, quantizations, a dataset, a demo? Which loading library?
2. Goal: adoption by developers, research credibility, a funnel into a paid API, or compliance with a customer's request? One primary.
3. License intent: permissive, non-commercial, custom terms? Any base model whose license you inherit?
4. Org account plan (free, PRO members, Team, Enterprise), who holds admin, and is the org verified yet? Verification is manual and slow: if not, start it today.
5. Release date, and is there an arXiv paper? Compute today's position now: under 14 days to launch compresses the cadence; a paper more than 14 days past its first arXiv version has missed Daily Papers.
6. Who owns the cards, the Space and the Community tab, and how many hours a week for the first month?
7. For the AI Act: training compute (rough FLOP), output modality, and where the company is incorporated.

## Fit verdict

- **Publish**: you ship weights, adapters, embeddings or a dataset developers will load. The Hub is the default home.
- **Demo only**: you sell a hosted API and have no artifact. A Space that is a thin ad for a paid endpoint sits next to the Content Policy's product-advertising line. Publish something useful on its own (an eval dataset, a small open model, a Static Space that runs in the browser), or skip the Hub.
- **Skip**: no artifact and no demo with standalone value.

## Release work, ranked by value per hour

Efficiency: complete card metadata > repo per variant + collection > copy-run snippet tested in a clean environment > linked Space demo > GGUF/quantized repos > Daily Papers submission > eval results > library registration > provider-support request > Posts and blog.

- Value order: snippet that runs > card metadata > Space demo > quantized repos > library registration.
- Effort order, least first: card metadata == collection (both minutes in the UI) > Daily Papers > eval results > snippet > quantized repos > Space demo > library registration (PR to `huggingface.js`, reviewed by HF).
- This order starves **library registration**: high value, slow, and it needs one model already tagged with `library_name` before the PR. Promote it when you ship your own loading library or a family of models; it buys the code-snippet tab and correct download counting for every future release. [HF]
- A **paper** promotes Daily Papers: submission closes 14 days after arXiv publication [HF]; the clock runs from the first version, a v2 does not reopen it [practitioner].
- A **compute-limited audience** (laptops, local apps) promotes GGUF repos: llama.cpp, Ollama and LM Studio appear in "Use this model" only for compatible formats. [HF]
- A **free org** demotes the demo to a Static Space (transformers.js or ONNX in the browser); see Spaces demo for the paid routes.

Follow the efficiency line; the value and effort lines explain it. Default rung: the first three plus a demo. Move up when the team can staff the Community tab.

## Gate decision

Rank by adoption cost, lowest first. Compliance cost runs the other way.

| Option                                                                             | Adoption cost | Compliance cost                         | Use when                                                     |
| ---------------------------------------------------------------------------------- | ------------- | --------------------------------------- | ------------------------------------------------------------ |
| Open, license in card                                                              | +++           | + (license only)                        | Default for adoption goals                                   |
| Gate, automatic approval, username and email collection off, license click-through | ++            | ++                                      | You need a recorded acceptance of terms, not identities      |
| Gate, manual approval, custom fields                                               | -             | --- (PII, review queue, privacy notice) | Dual-use risk, staged research access, contractual screening |
| Gate, approval by your own system via API (payment, external form)                 | ---           | ---                                     | Access is a paid product                                     |

- Rejection is permanent for that user unless you `reset` the request, which also makes them re-accept new terms. [HF]
- `extra_gated_eu_disallowed: true` blocks EU IPs, only on gated repos. It is a license-distribution control, not an AI Act opt-out. [HF]
- **Leads without a lead gate**: a custom license with a commercial threshold is the nameable reason for a click-through gate. Capture sales interest with a "commercial license or hosted API" link in the card and the pinned FAQ, pointing to your own form. Expect a pull funnel, not a list.

## License and EU AI Act

- Pick a listed license id. For custom terms set `license: other`, `license_name: <slug>`, and `license_link` or a `LICENSE` file. [HF]
- Call a model "open source" only under an OSI-approved-style license with no use or revenue restrictions; otherwise say "open weights" and name the license.
- A fine-tune or quantization inherits its base model's license terms; read them before choosing yours.
- Indicative test for a general-purpose AI model: above 10^23 FLOP of training compute **and** it "can generate language (text or audio), text-to-image, or text-to-video"; "not an absolute rule". Speech recognition and text-to-speech models are inside the modality test. Embedding, reranking and classification models usually sit outside it. A single-task model above the threshold may exceptionally fall outside if it lacks significant generality. Record either argument and route it to counsel. [EU Commission]
- Modifying such a model with more than a third of its original training compute makes you a provider, with duties limited to documenting the modification. [EU Commission]
- Obligations apply since 2 August 2025; the Commission enforces them, including fines, from 2 August 2026; models released before August 2025 comply by 2 August 2027. [EU Commission]
- Every provider owes a copyright policy and a public training-data summary on the AI Office template. Link both from the card.
- The open-source exemption (technical documentation, downstream documentation, EU representative) needs a free and open-source license without monetisation, public weights, and no systemic risk (presumed above 10^25 FLOP). Revenue-gated or use-restricted licenses likely lose it. Route the final call to counsel. [EU Commission]

## Spaces demo

1. Check the plan first [HF]:
   - Static: free for everyone.
   - Gradio and Docker: PRO for a personal account, Team or Enterprise for an org.
   - ZeroGPU (Gradio only): free personal accounts 2 Spaces, PRO 10, Team or Enterprise org 50.
2. Prefer Gradio + ZeroGPU for a GPU model, Static + transformers.js for small models, paid hardware only for always-on latency.
3. Set `@spaces.GPU(duration=...)` to the real worst case, not "to be safe". Shorter declared durations get queue priority [HF]. The platform refuses a run when the visitor's remaining daily quota is below the declared duration (default 60 s) [practitioner]: above 120 s anonymous visitors can never run it.
4. Load weights from your Hub repo and list them under `models:` in the Space README. The Space then appears on the model page; an org-owned Space gets the author-owned star. [HF]
5. Free CPU Spaces sleep after 48 h without visits; the first visitor waits for a cold start. Ask for a community GPU grant in Space settings when the demo has traction. [HF]
6. Keep API keys in Space secrets, never in `app.py`. Each push is scanned, but the scan emails only verified secrets: scan history yourself before going public. [HF]

## Datasets

- Same layout rules: one repo per dataset, card YAML with `license`, `task_categories`, `language`, `size_categories`, and `configs` pointing at the data files. [HF]
- Prefer Parquet for large tabular data; CSV and JSON Lines also load. Check the Dataset Viewer renders before launch: a viewer error is the first thing evaluators see. [HF]
- Gating works as for models. Personal data in the rows is your responsibility before any gate: remove or consent it first.
- A dataset download is every file one IP fetches from the repo within 5 minutes, counted once; model downloads count query-file requests. The two are not comparable. [HF]

## Engagement recipe

**Surfaces**

| Surface                                    | Payoff      | Note                                                                                                                                                             |
| ------------------------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Model/dataset card                         | compounding | Indexed by full-text search with Spaces `app.py` [HF]                                                                                                            |
| Collection per family                      | compounding | First two collections show on the org page; first three items preview [HF]                                                                                       |
| Space linked to the model                  | compounding | Spaces of the Week is weekly HF-team curation [HF]                                                                                                               |
| Org card (public Space) and verified badge | compounding | Adding the email domain lets anyone with a matching address join [HF]: audit joiners and set them to read. HF staff verify by hand, days to weeks [practitioner] |
| Community tab                              | compounding | Discussions and PRs; pin the FAQ                                                                                                                                 |
| Paper page + Daily Papers                  | one-shot    | 14-day window                                                                                                                                                    |
| Posts                                      | one-shot    | PRO needed; chronological feed of followers, no ranking [HF]                                                                                                     |
| Org blog article                           | one-shot    | Enterprise orgs; community blogs need PRO [HF]                                                                                                                   |

If someone squats your company name, take a distinct slug now, get it verified, and ask HF support to contact the squatter; report impersonation under the Content Policy. [practitioner]

**What ranking rewards**

- [HF] Trending "is influenced by the number of likes in the past few days"; the release checklist adds visits. Do more: concentrate launch traffic on the model page in the first days; link every external post to the Hub page, not your site.
- [HF] Feeds are not personalized; Posts reach followers only. Do more: grow org followers before launch. Do less: rely on Posts for reach.
- [HF blog, "State of Open Models"] Likes go to new frontier releases in their first weeks; downloads accrue to small, stable models over years. Do less: read a flat download curve in week one as failure.
- [practitioner] Trending trackers read the score as roughly seven-day likes; an unconfirmed variant adds downloads against a baseline.

**Cadence**

1. **T-30 or now**: start org verification; set member roles.
2. **T-14**: card drafted with metadata, collections created, repos private.
3. **T-3**: recreate repos, or squash and delete old PR refs, branches and tags (see Rules); scan for tokens; test the snippet in a clean environment; Space live and linked; Community tab FAQ written.
4. **T-0**: flip repos public together, submit Daily Papers if inside the window, post the Hub link on your channels, staff the Community tab daily.
5. **Weeks 1-2**: answer every discussion, merge useful PRs (eval results, card fixes), add `new_version` banners if you re-release.
6. **Week 4 on**: community quantizations and fine-tunes appear in the model tree; link the good ones in the collection.

**Limits**

| Limit                                             | Value                                                                                           | Type        |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------- |
| Rewards for likes, product-ad spam, bulk activity | restricted content, unranking or removal                                                        | enforced    |
| Daily Papers submission                           | 14 days after arXiv date                                                                        | enforced    |
| ZeroGPU Spaces hosted                             | free personal 2, PRO 10, Team/Enterprise org 50                                                 | enforced    |
| ZeroGPU visitor quota per day                     | anonymous 2 min, free 5 min, PRO/Team 40 min, Enterprise 60 min; paid tiers extend with credits | enforced    |
| Files per repo / per folder / file size           | <100k / <10k / <200 GB                                                                          | recommended |
| Free public storage                               | "best-effort", useful content only                                                              | policed     |

The Hub has no sub-communities with their own rules; the HF forum and Discord are separate venues with their own channel rules.

**Templates**: the templates file linked under Output holds the card YAML skeleton, eval-results file, gate prompt, pinned Community FAQ, discussion replies, provider-support request and launch Post.

## Measure

- Report likes, downloads and Space visits as separate lines, each with its counting rule. Never sum Hub downloads with PyPI or npm downloads, or model downloads with dataset downloads.
- Use derivatives in the model tree (fine-tunes, quantizations, adapters) as the adoption signal for an open model. [HF]
- Unique downloaders exist only as an Enterprise Plus log export; Publisher Analytics (Team/Enterprise) gives daily non-deduplicated counts. [HF]
- Community tab: median time to first staff reply under one business day for the first month (self-set target).

## Output

Read [references/templates.md](references/templates.md) before writing; most deliverables fill its templates.

In order: fit verdict; a verdict on each plan item or question the user stated; repo layout table (repo id, variant, `base_model`, license, gate); ranked release actions with owner and date; gate decision with its reason; Space plan with hardware and plan check; AI Act line (provider or not, which duties); cadence dates; filled templates; measurement plan.

## References

- samber/developer-platform-skills@sdk-package-publishing - releasing the Python or JS library that loads the weights.
- samber/developer-platform-skills@sample-app-strategy - Spaces as part of the sample and demo portfolio.
- samber/developer-relations-skills@oss-launch - sequencing the Hub release with other launch channels.
- samber/developer-relations-skills@oss-distribution-strategy - the Hub as one channel in the distribution mix.
- samber/developer-relations-skills@oss-license-strategy - the license of the accompanying code.
- samber/developer-relations-skills@devrel-metrics - turning Hub numbers into reported outcomes.
