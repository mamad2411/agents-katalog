---
name: github-engagement-playbook
description: "Plans a repository's post-launch engagement on GitHub as a social platform - stars, watchers and release notifications, Discussions, topics, labels, Trending, the home feed and traffic tracking - with ready-to-paste issue, PR and release templates. Use whenever GitHub stars are flat, someone asks how to grow engagement on a repo or SDK, set up Discussions Q&A or a label scheme, get a Release seen by watchers, or whether to buy or trade stars, even if they only say nobody notices the repo. Not a launch - use samber/developer-relations-skills@oss-launch. Not README copy - use samber/developer-relations-skills@readme-optimization. Not cross-channel cadence - use samber/developer-relations-skills@oss-distribution-strategy. Not license choice - use samber/developer-relations-skills@oss-license-strategy."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# GitHub engagement playbook

You are a developer-relations engineer. GitHub is where evaluators judge a repository and users stay subscribed; reach is mostly earned elsewhere.

Listing an app or action on GitHub Marketplace belongs to `samber/developer-platform-skills@github-marketplace-playbook`.

Label every ranking or reach claim: `[documented]` = GitHub docs, changelog or policy; `[folklore]` = practitioner inference, never stated as fact.

## Interview

Ask one question per message, multiple-choice where possible:

1. Whose repository: company SDK or library, community project, or solo maintainer?
2. Which number does leadership read today, and what decision hangs on it?
3. Do usage questions already arrive as issues or in private channels, and how many per week?
4. Date the result must land by.
5. One-off win or compounding asset?
6. Effort ceiling in hours per week, and who answers publicly, with what backup?

Read the sidebar, Releases, Discussions and `.github/` first; without access, ask for pasted copies and a traffic export.

## 1. Diagnose before touching anything

Asked to buy, trade or reward stars: answer with the § 5 risk paragraph and template 7 first, then diagnose.

1. Archive traffic weekly via `/repos/{owner}/{repo}/traffic/views`, `/clones`, `/popular/referrers`, `/popular/paths`: 14 days kept, top 10 only, push access needed [documented]. Run the Google Apps Script files in `scripts/` to append them to a spreadsheet as weekly time series, add Google Alerts for off-GitHub mentions, and read OSS Insight for star and contributor history; setup in [references/tracking-tools.md](./references/tracking-tools.md).
2. Read watchers, dependents ("Used by") and registry downloads beside stars, as trends against the same window a quarter earlier. No absolute threshold exists.
3. Classify the curve. The row sets the headline and first action; § 2-4 still build the standing asset.

| Pattern | Reading | First action |
|---|---|---|
| Unique visitors flat or falling; the registry page or docs missing from referrers | No inflow; GitHub is not the bottleneck | Fix the registry-to-repo link (`samber/developer-platform-skills@sdk-package-publishing`), then off-platform via `samber/developer-relations-skills@oss-distribution-strategy` |
| Visitors rise, stars and dependents do not | Page fails evaluators | `samber/developer-relations-skills@readme-optimization`, then § 2 |
| Downloads or dependents grow, stars flat | Users install from the registry | Change the reported metric (template 8); stop chasing stars |
| Usage questions pile up in issues | Support leaks into the tracker | Name an answerer, then Discussions Q&A (§ 2) |

When two rows fit, run the metric swap first.

## 2. Engagement surfaces, ranked

List order is the efficiency order (value per maintainer hour). Cadence in § 4 is sequence, not rank.

1. **Traffic archive and metric swap** - near-zero effort; buys the knowledge of which problem exists. Compounding.
2. **Small, frequent releases as feed events** - minutes to an hour per release. Ship each merged fix or feature as its own GitHub Release with a written body, ticking "Create a discussion for this release" in an Announcement category. Notifies release watchers; shows on stargazers' and watchers' Feed tab [documented]. Compounding.
3. **Topics** - an hour once: 5-10 accurate topics, each feeding `github.com/topics/<name>` [documented]; search weight unpublished. Compounding.
4. **Discussions Q&A** - a standing job of hours per week; builds an indexed, answered support archive and credits helpers. Compounding.

- value: `Discussions Q&A > releases as feed events > traffic archive > topics`
- effort (highest first): `Discussions Q&A > releases as feed events > topics > traffic archive`

The order starves Discussions Q&A: highest value, standing cost. Promote it to rung 2 when question 3 found weekly usage questions and question 6 named an answerer plus backup. Delete it when nobody answers publicly: an unanswered tab reads as abandonment.

Re-rank against the interview, and say which answer moved what:

- A date inside two months promotes rungs 1-3; Discussions still opens but carries no deadline metric.
- A compounding mandate with an answerer promotes Discussions to rung 2.
- A one-off win cuts the list to rungs 1-2.

## 3. Algorithm preference

**Do more of:**

- Release small and often. Every version published as a GitHub Release is a feed event for the repository's stargazers and watchers [documented], so ten small releases put the project in front of them ten times where one large release does once. One real change and a one-line body is enough.
- Keep the repository visibly active. The home feed shows activity from people and repositories a user follows and stars [documented], and its recommendations lean toward repositories with recent activity [folklore]. Releases, merged PRs, answered discussions and new contributors all count; a quiet month drops the project from that stream.
- Turn on Dependabot version updates. Weekly dependency PRs and merges keep the commit graph and "last updated" date fresh at near-zero effort, so evaluators read the repository as maintained [folklore]; the security patches are real value on their own.
- Post release and roadmap notes in an Announcement category: a feed event type, opened only by maintain or admin roles [documented].
- Mark Q&A answers (the author or triage+ can). GitHub highlights the answer [documented] and lists members with the most marked answers as most helpful [documented in launch notes; check the current UI].
- Earn stars through use, and ask for them in content published elsewhere. "Many of GitHub's repository rankings depend on the number of stars" and Explore lists popular repositories by stars [documented]. End a blog post, talk slide, newsletter or video with one line asking readers who found it useful to star the repository to support its progress (template 14).

**Do less of:**

- Expecting the feed to reach strangers. It reaches followers, stargazers and watchers; the default home page is a work dashboard with the social feed on a separate tab [documented]. Reach beyond them is earned off-platform.
- Chasing Trending day to day. Trending ranks stars gained inside a window, per language; GitHub publishes no formula, and "star velocity against the repo's own baseline" is [folklore]. Getting onto Trending is a launch-sized burst: plan it with `samber/developer-relations-skills@oss-launch`.
- Releases with an empty body. A release is a feed event only worth its slot when the body says what changed.

Treat any feed or ranking claim older than a year as stale until re-checked against GitHub's changelog.

## 4. Cadence

1. **Weeks 1-2, earn first** - archive traffic, answer open usage questions in issues (oldest first, inside the effort ceiling), set topics, back-fill bodies on the last three releases.
2. **Weeks 2-4** - open Discussions with two categories (Announcements, Q&A). Add a `contact_links` entry in `.github/ISSUE_TEMPLATE/config.yml` pointing questions to Q&A. Convert 5-10 answered usage issues to discussions. Pin a start-here post. Set the label scheme from [references/labels.md](./references/labels.md) and enable Dependabot version updates.
3. **Every release** - Release body (`samber/developer-relations-skills@changelog-writing`), the auto-created Announcement, then an off-platform post. Cut a release as soon as one user-visible change is merged; never batch fixes to make a release look bigger.
4. **Weekly** - answer Q&A inside the stated target, mark answers, label new issues, PRs and discussions, merge Dependabot PRs, convert stray usage issues, export traffic.
5. **Quarterly** - read watchers, dependents, downloads and referrers against the baseline; revise topics.

Ask for a watch only where a reader already wants release news: the start-here post, the docs changelog, a solved thread. Ask for a star at the end of content published elsewhere, never with a reward, never in other repositories' issues.

## 5. Limits

| Where | Limit | Enforced or policed |
|---|---|---|
| Whole platform | Acceptable Use Policies ban "rank abuse, such as automated starring or following", fake accounts, bulk promotion, and engagement "incentivized by ... gifts or other give-aways" | Enforced |
| Whole platform | About 80 content-creating requests per minute, 500 per hour, web UI included: hits bulk issue conversion or mass commenting | Enforced |
| Your repository | Topics: 20, lowercase letters, digits, hyphens, 50 characters each. Discussions: 25 categories, 4 global pins plus 4 per category | Enforced |
| Your repository | `FUNDING.yml`: 1 organization plus 4 developers on GitHub Sponsors, 4 custom URLs, 1 account per other platform; button off until enabled in settings | Enforced |
| Other repositories' issues and PRs | No promotion; maintainers hide it as spam. Post only a disclosed answer to that exact issue | Policed |
| `github/explore` | PR template attests "This change is not self-promotion"; self-promotion is "unlikely to be accepted" | Policed at review |
| Awesome lists, other repos' Discussions, Community forum | Each sets its own rules; awesome lists usually accept an author's PR that meets their criteria | Policed per venue |
| Anywhere | Star-for-star or "star to enter" asks | Policed; the AUP give-away clause also applies |

Buying, trading or rewarding stars is never an option, only a risk. StarScout (He et al., ICSE 2026) found 6.0 million suspected fake stars across 18,617 repositories: about five times weaker than real stars, faded within two months, then a liability; about 90% of campaign repositories were deleted.

## 6. Templates

Read [references/templates.md](./references/templates.md): release body, announcement, start-here post, Q&A answer, issue redirect, watch ask, star-for-star decline, leadership metric note, pull request, tracking issue with sub-issue checkboxes, new issue, pointer to an existing issue, pointer to a related but different issue, star ask for off-GitHub content. Leave unknown `<placeholders>` visible; never invent facts. Run each through your preferred humanizer skill.

## 7. Output

Deliver, in this order:

1. Diagnosis row from § 1 with the numbers behind it.
2. Ranked surfaces with the re-rank stated.
3. A cadence up to the landing date, with owner roles.
4. Filled templates 1, 2, 3 and 8.
5. Metrics: unique visitors, top referrers, watchers, dependents, downloads, Q&A answered share, median time to answer (GraphQL `answer.createdAt` minus `createdAt`). Cloners stay diagnostic (CI inflates them); stars are never a target.

Pass bar: every ranking claim carries a label, no rung needs hours the interview ruled out, and no star ask offers a reward or trade.
