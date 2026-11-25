---
name: medium-playbook
description: "Runs a devtool vendor's, DevRel team's or open-source maintainer's presence on Medium - brand account vs company publication vs named engineers, submitting to established tech publications, canonical import, distribution tiers and Boost, topics, AI disclosure, the paywall and Partner Program trade-off, follower growth, leaving Medium. Use whenever the user mentions Medium, a Medium publication, syndicating a blog to Medium, Medium Boost or Medium posts nobody reads - even if they only say 'our stories die at 40 views'. Not for an individual writer's income. Do NOT use for drafting the article - use samber/developer-relations-skills@engineering-blog-post; for dev.to, samber/developer-relations-skills@devto-playbook; for a Substack newsletter, samber/developer-relations-skills@substack-playbook."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Medium Playbook

You run a vendor's or maintainer's presence on Medium: a reading platform where human curators and a member paywall decide reach, and where marketing is allowed but not distributed.

Label every distribution claim: **[platform]** when Medium's help center or rules state it, **[practitioner]** for writer reports, publication owners' own pages and reverse-engineering. Say when a point is your own reasoning. Medium rewrites these rules often; when you can browse, re-read the Distribution Guidelines, the Medium Rules, the AI content policy and the Partner Program eligibility page before advising.

## Rules that remove or bury vendor stories

- **Traffic-first is spam.** A story posted "primarily to drive traffic to, or increase the search rankings of" your site or product is spam, removed without notice; so are templated near-duplicate posts [platform]. The Rules remove the worst cases; the Distribution Guidelines cap the rest, below.
- **Allowed is not distributed.** First-party promotion is allowed [platform]. But "sponsored content, content marketing, PR pieces" and stories whose "primary point" is signups or selling get Network distribution only: your followers, nobody else [platform]. Test: strip the product name; if nothing worth reading remains, it is content marketing.
- **No teasers.** A story clipped to send readers to the rest on your site is spam [platform]. Publish the full text with a canonical link home.
- **AI-generated text gets no reach.** Majority-AI text with little editing is low-value content: no General distribution and no Boost, labelled or not, and never paywalled [platform]. Rewrite it as first-hand human writing, or keep it off Medium.
- **AI-assisted text needs a label** in the first two paragraphs; unlabelled, it drops to Network only [platform]. Grammar, outline and fact-check tools need no label.
- **One copy on Medium.** No re-posting after unlisting, no same story in two publications, no duplicates across accounts; suspension until fixed [platform]. Your own blog copy is fine.
- **No engagement on cue.** Bulk or programmatic follows, claps and responses, responses used for promotion, brigades and bought reads are banned; Partner Program misuse is revoked "without notice or the option to appeal" [platform]. Each reader's claps are weighed against that reader's own habit [platform].
- **Paid placements.** A sponsored post promoting your product inside someone else's story or Medium publication is third-party advertising, banned [platform]. Sponsored content also gets Network only [platform]. A paid writer whose piece stands on its own still discloses what they got [platform]. Treat any paid placement on Medium as both a ban risk and a reach loss, and run it off Medium (own reasoning).
- **Disclose offsite signup links** right next to the link [platform].
- **English only for reach.** Curators review English stories only; other languages get no Boost and no General distribution [platform]. Your own translation is not a duplicate [platform], but it reaches followers only: serve that community on your own channels.
- **No new API tokens.** Medium accepts no new integrations; publish through the editor or the import tool [platform].

| Rationalization                                    | Why it fails                                                                                                           |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| "Medium's domain authority will rank us fast."     | Medium withholds new or untrusted accounts from search indexing for days to weeks [platform].                          |
| "Topic followers see it even if curators skip it." | Topic matching belongs to General distribution; Network means followers only [platform].                               |
| "We labelled the AI draft, so it is fine now."     | The label avoids the undisclosed penalty; AI-generated content still gets no General distribution [platform].          |
| "A publication editor can nominate us for Boost."  | Medium no longer lists a nomination program; curators use internal tools and review featured stories first [platform]. |
| "The brand account gives every post one voice."    | Boost rewards a writer's first-hand experience, which a brand account cannot show [platform].                          |

## Interview

One question per message; skip what the request answers.

1. Who writes: named engineers, a maintainer, a brand account? Does the company control a paid Medium membership?
2. Goal and date: adoption from a launch, a standing tutorial channel, or hiring?
3. Where originals live: company blog with a canonical URL, docs, a Medium custom domain, or Medium only? In English?
4. Hours per week, and who answers responses within two days?
5. One-off push or a compounding asset?

Answers 2, 4 and 5 re-rank the surfaces below; say which answer moved which row.

## Fit verdict

- **Invest:** English first-hand engineering stories, named authors, someone answering responses weekly.
- **Syndicate only:** content lives on the company blog; canonical import under named authors, no paywall, no native writing.
- **Skip:** only product announcements, AI-generated drafts, or non-English stories; Medium gives them followers-only reach at best.
- **Leave:** the company blog already sits on a Medium custom domain and you want it home; see Leaving Medium below.

## Account model

1. Named engineers publish under their own accounts; Boost weighs first-hand experience [platform].
2. Solo maintainer: own profile, no publication. Two or more writers: a company publication, owned by a company-controlled account with a paid membership, never a departing engineer's [platform: creating one needs membership; one user owns up to 7].
3. Sign a retention agreement with each engineer before the first import. Put it in their employment or IP terms, not in a publication condition. It covers three points:
   - they may import company posts;
   - canonicals stay on the company domain;
   - on departure, their stories stay up, free and in the publication.

   The agreement is needed because each story stays under its author's control: editors may not delete it or remove it from the paywall without the writer [platform]. Never require outside or partner writers to grant republishing rights to submit [platform].
4. Keep a brand account for release notes only, written to be useful without the product link, expecting followers-only reach.
5. Keep the canonical original on the company domain: it is the copy you control. A publication owner may not move authors' stories off Medium without each author's permission, and a custom domain pointed away gets disconnected [platform]. Medium can also redirect a custom domain's URLs to medium.com, as Towards Data Science reported in 2025 [practitioner].

## Engagement surfaces, ranked by value per hour

Efficiency: canonical import of an existing post under a named author > responses on others' stories in your topics > company publication with a weekly featured story > submission to an established tech publication > native first-hand deep-dive > publication newsletter > brand-account release note. Import leads responses because it puts a finished story before the publication's followers in the same hour a response earns a few profile visits.

Compliance cost: AI-generated or traffic-first story > teaser > paid placement in a Medium publication > paywalled product story > disclosed first-party call to action.

Durability: Medium-only original under a custom domain < publication copy with canonical home.

| Surface                                             | Payoff      | Value | Low effort |
| --------------------------------------------------- | ----------- | ----- | ---------- |
| Canonical import, named author, company publication | compounding | ++    | +++        |
| Substantive responses in your topics (earn-first)   | compounding | +     | +++        |
| Company publication, featured credit used weekly    | compounding | ++    | ++         |
| Submission to an established tech publication       | one-shot    | ++    | +          |
| Native first-hand deep-dive (Boost candidate)       | compounding | +++   | -          |
| Publication newsletter to its subscribers           | compounding | +     | ++         |
| Brand-account release note                          | one-shot    | -     | ++         |

- **Effort, in hours:** an import or a response takes under an hour; a native story takes an engineer a day or more plus review. Submission rates `+` only when the publication accepts published stories; one that demands an original costs as much as a deep-dive.
- **Re-rank:** a launch date promotes the established-publication submission; a compounding mandate promotes the deep-dive; under 2 hours a week, keep canonical import and responses only.
- **The order starves** the native deep-dive: highest value, highest effort. Promote it when the team has a real incident, migration or benchmark story and a named engineer to own it.
- **Default rung:** canonical import, into the company publication when there is one. Move up to native deep-dives once imports draw followers.
- No paid amplification exists: Medium sells no ads, and bought traffic harms a publication's standing [platform].

## What distribution rewards

**Do more:**

- Write from first-hand experience: what you built, broke and measured [platform].
- Titles, subtitles and covers that say what the story is; no cover beats a poor one [platform].
- Up to 5 topics, each one the story is actually about [platform].
- Feature one story a week: credits start at 4, refill one per 7 days, cap at 4; featured stories get reviewed for Boost first [platform].
- Openings that keep readers past 30 seconds: read ratio is reads of 30 s or more over views, and it punishes titles the opening does not honour, not long stories [platform].
- Email your subscribers on publish; import only addresses that opted in to this author [platform].

**Do less:**

- Product-first stories, "write for us" pages, posts about Medium itself: Network only [platform].
- Mass mentions: the guideline's example is 20 users, and such stories lose General distribution [platform]. Mention someone only when the story cites their work.
- Off-topic topics chosen for reach [platform].
- Responses that point at your own stories: promotion through responses is spam [platform]. Remove spam responses on your stories; leave critical ones up and answer them.

## Cross-posting and paywall

- Import with Stories > Import a story: canonical link and original date set automatically [platform]. If the importer fails, paste and set the canonical by hand; only the story's author can set it, never a publication editor [platform].
- Publish under the named engineer, then submit to the publication.
- Keep vendor stories free. The paywall hides them from non-members; the Partner Program needs a paid membership and pays on member activity only, so non-members reading through your Friend Link earn nothing [platform]. Writers report single- to low-double-digit dollars a month on small followings [practitioner].
- Paywall only when the goal is writer income, from an individual's account, with no product call to action.
- Skip publications whose submission settings require a paywalled story when reach is the goal [platform]. Editors never post Friend Links inside a writer's story [platform].

For per-publication submission rules, platform limits and templates, read [references/limits-and-publications.md](./references/limits-and-publications.md) and [references/templates.md](./references/templates.md).

## Cadence

1. **Weeks 1-2, earn first.** Complete profiles; each writer follows the target topics and leaves a few substantive responses a week there, no links (a self-set pace, not a platform rule). Sign the retention agreement; create the publication if two or more people write.
2. **Weeks 2-3, syndicate.** Import up to three existing posts that pass the strip-the-product test, one every few days, each under its named author. None pass: start the first native story instead.
3. **Weeks 3-8, publish.** One story every one or two weeks; feature the strongest each week; answer responses within two days.
4. **By week 6.** Submit one story to an established publication whose rules allow your call to action; ask the editor first about any paid-plan or trial link. An open publication takes 3 active submissions per guest writer [platform].
5. **Monthly.** Read story stats; drop topics that drew no presentations.

## Diagnose a story nobody reads

1. Compare presentations with writer plus publication followers; presentations at or below that suggest Network only, a signal rather than proof (own reasoning). Confirm with the traffic-source split; stories from before 2025 show no presentations [platform]. Check product framing, AI-generated text, a missing AI label, off-topic topics, mass mentions or a non-English text.
2. Presentations high, views low: fix title, subtitle and cover.
3. Views high, reads low: the opening fails its promise.
4. Rewrite the next story; leave this one up, never re-post it.

## Leaving Medium

1. For Medium-native stories, collect written permission from each copyright owner (the author, or the company for employer-owned work); the publication's licence does not cover republishing [platform]. Imported posts already live on your domain.
2. Rebuild the Medium-native stories on your own domain.
3. After DNS moves, every old custom-domain path (slug ending in a hex story id) is yours to serve: map each with a 301 to its new URL or it 404s (own reasoning). The Medium copies stay live at medium.com URLs.
4. Ask each author to set the canonical link on the Medium copy to the new home; only they can [platform].

## Measure

Targets are self-set; Medium publishes no vendor benchmark.

- Presentations, feed click-through, reads, read ratio, followers gained per story.
- Referral sessions and signups from UTM-tagged links back to the canonical page, read on your own analytics: Medium allows no tracking scripts [platform].
- Boost badges per quarter.
- Keep each author's third-party AI setting on the default "Prioritize maximum reach": the other option makes some AI products unlikely to credit and link the story [platform].
- Hygiene, pass threshold zero: AI-generated or unlabelled stories, teasers, duplicates, paid placements.

## Output

In order: fit verdict; account model with the retention agreement; ranked surfaces with what moved; publication setup and target external publications with each one's rules; eight-week cadence with owners and hours; filled templates from [references/templates.md](./references/templates.md); metrics. Run drafts through your preferred humanizer skill.

## References

- samber/developer-relations-skills@engineering-blog-post - writing the post this skill publishes.
- samber/developer-relations-skills@devto-playbook - the other cross-posting channel.
- samber/developer-relations-skills@substack-playbook - a newsletter-first alternative.
- samber/developer-relations-skills@hackernews-playbook - launch-day discussion for the same story.
- samber/developer-relations-skills@devrel-content-calendar - fitting Medium slots into the quarter.
- samber/developer-relations-skills@devrel-analytics - attributing referral signups.
