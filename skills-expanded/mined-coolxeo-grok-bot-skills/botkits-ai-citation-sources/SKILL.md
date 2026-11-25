---
name: botkits-ai-citation-sources
description: >-
  use this when AI answers (ChatGPT, Copilot, Gemini, Perplexity, AI Overviews)
  cite third-party pages instead of your site for prompts you care about, and
  you need to list those sources and pick a draft-only action for each one
---
# AI citation sources

Use this skill for prompts where your site loses because AI answers trust other sources: lists, reviews, forums, directories, articles, video platforms. You list those sources. You tag each one OWN, CLAIM, EARN, or CONTEST. You write a draft action for each one. A human approves every action.

Input: the lost rows with cause `third-party` from [botkits-ai-search-gap-loop](../botkits-ai-search-gap-loop/SKILL.md). Each row has the prompt, the date, the tool, and the cited domains.

Helper file: [source-table-template.md](source-table-template.md).

## Step 1. List the sources

1. For each lost prompt, copy the cited URLs in the order the answer gave them.
2. Merge the URLs into one table. For each source, record:
   - URL and domain
   - Source type: list article, review site, forum or community, directory, video platform, news, reference, competitor
   - Lost prompts that cite it (row IDs) and the count
   - What it says about your category, and whether it names you
3. Open each page. Read it. Do not tag a source from its title only.
4. Sort by the number of lost prompts that cite it. Work from the top.

## Step 2. Tag each source

Give each source exactly one tag.

| Tag | When | Draft action |
| --- | --- | --- |
| **OWN** | You control the page (your site, your channel, your profile, your store page), but it is weak or not cited. | Draft an edit to that page so it answers the prompt plainly and matches the facts on your site. Use [botkits-aeo-geo-site](../botkits-aeo-geo-site/SKILL.md). |
| **CLAIM** | The source has a listing or profile slot for you that you can claim or fill as the owner: a directory, a platform profile, a knowledge panel, an app or catalog listing. | Draft the claim or profile text with true, consistent facts (name, what it is, who it is for, official links). Note the account and verification steps a human must do. |
| **EARN** | An independent editor, reviewer, or list author decides who is included. | Draft a short, factual note to the author or editor that says what the product is and why it fits their list. No payment for placement unless the page discloses it. No pressure. |
| **CONTEST** | The source has a factual error about you, or a fair comparison leaves you out of a set you clearly belong to. | Draft a correction request with evidence (a link to a public page that shows the fact). Ask for a correction, not removal of others. |

If a source does not fit any tag (for example a large reference site where a product mention would be self-promotion), write `skip` and the reason.

## Step 3. Forums and communities

Forums such as Reddit, Quora, and topic boards are often cited. Treat them with care.

- Pick communities only when they are close to the product and to the buyer's decision. Use the tracked prompts to choose them, not community size.
- Read each community's rules first. Many ban self-promotion or links. Follow them exactly.
- Draft only. Never post, reply, vote, or message from this skill.
- Disclose the connection in every draft ("I make X"). Never pose as a neutral user, customer, or parent.
- Answer the question first. Mention your product only if it truly answers the question and the rules allow it.
- Respect any posting limits the account owner sets. Keep drafts few and specific.
- A human reads, edits, and decides whether to post each draft.

## Step 4. Pick the work for this cycle

1. Pick at most one or two source actions per cycle, so the loop can tell what helped.
2. Prefer OWN and CLAIM first. You control them, and they are fast to check.
3. EARN and CONTEST depend on other people. Log the date you sent them and do not count them as wins until the source changes.
4. Add the chosen action to the cycle entry in the [botkits-ai-search-gap-loop](../botkits-ai-search-gap-loop/SKILL.md) log.

## Step 5. Recheck

On the next cycle, reopen each acted-on source. Record what changed on the page, with the date. Then rerun the lost prompts. Do not claim that a source change caused an AI change unless the rerun shows the source cited with your name in it.

## Guardrails

- Same content for bots and people. No cloaking.
- No fake reviews, ratings, testimonials, or sock-puppet accounts.
- No astroturfing. Always disclose the connection to the product.
- No paid placement without clear disclosure on the page.
- No invented numbers. Use `missing` when a value was not read.
- On sites for children or families: no personal data about children in drafts, outreach, or tracking.
- All outbound text is a draft. A human approves before anything is sent or posted.
- Respect each site's terms and each community's rules.
