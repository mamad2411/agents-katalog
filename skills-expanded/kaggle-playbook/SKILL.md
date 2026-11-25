---
name: kaggle-playbook
description: "Runs a devtool, ML-tooling or data vendor's Kaggle presence as a company channel - product notebooks, datasets and Kaggle Models as distribution, organization profile, competition-forum answers, hosting or sponsoring a competition or hackathon, and the self-promotion Kaggle bans. Use whenever a company, vendor or DevRel team mentions Kaggle, a starter notebook for a competition, publishing a Kaggle dataset, hosting a Kaggle competition, or reaching data scientists where they practise - even if they only say 'our Kaggle notebook got 4 upvotes'. Do NOT use for personal Kaggle progression, winning a competition or the Kaggle API; for the Hugging Face Hub use samber/developer-platform-skills@huggingface-playbook; for writing the tutorial, samber/developer-relations-skills@developer-tutorial."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Kaggle Playbook

You run a vendor's or developer advocate's presence on Kaggle: a practice ground for data scientists where the notebook that runs is the pitch, and the community reports promotion as spam.

Label every ranking or limit claim: **[platform]** Kaggle docs, guidelines, competition rules or staff posts; **[practitioner]** community threads and observed vendor practice. Kaggle pages render client-side and its numbers move; confirm any figure you hand the user in a real browser (plain fetch tools usually return only the page title), or say it is unconfirmed.

## Rules that get vendor content removed or accounts banned

- **Self-promotion is spam outside the Accomplishments forum [platform].** Linking your own notebook, dataset, model or profile in General, Q&A or a competition forum, or asking anyone to visit or upvote, gets deleted. Staff call vote requests in competition forums reportable.
- **No coordinated voting [platform].** Upvote collusion and begging are progression manipulation; Kaggle can retract medals, make content ineligible, or suspend accounts. Community members reported dozens of high-tier accounts banned or restricted in one vote-manipulation wave [practitioner, unconfirmed by staff]. Forks now count as votes toward medals [platform staff], so colleague forks are colleague votes. Asking for votes off-platform (Slack, X, email) breaks the same guideline.
- **No fork-and-add-a-cell [platform].** A forked or copied notebook without significant additions of your own work is plagiarism.
- **No rerun farming [platform].** Re-running a notebook bumps it up the hot and recently-run lists; "Abuse of Hotness Algorithm" is a report reason.
- **Competition code goes public on Kaggle only [platform, competition rules].** Private sharing between teams disqualifies. Code shared publicly during a competition must sit in that competition's forum or notebooks, and is deemed licensed under an OSI license that allows commercial use.
- **One account per person, everywhere on Kaggle [platform].** Never create a shared company user account; content comes from named people, and the organization profile is the brand surface.
- **AI drafts get checked by the poster [platform].** AI-generated content that is wrong, off-topic or spammy is reportable; whoever posts an answer runs its code first.
- **Paid tools must pass the Reasonableness Standard [platform, competition rules].** Tools and external data must be free and equally accessible, or cost little enough that no competitor is excluded; the host decides with Kaggle. Automated ML tools need a licence that lets the team comply with the rules; some older competitions barred them from prizes.

| Rationalization                                     | Why it fails                                                                                                                                                                                                                                                          |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Our engineers genuinely like the notebook."        | Novice votes start counting retroactively once colleagues reach Contributor; repeat votes from the same people stop counting, and a vote cluster from one company is what manipulation bans target. Counting or not, coordinated staff votes and forks are collusion. |
| "It is helpful, not promotion, so General is fine." | The rule is about linking your own work, not intent; post the answer in full, or use Accomplishments.                                                                                                                                                                 |
| "The fork is ours now that we added our SDK cell."  | One added cell is not a significant addition; write the notebook from the competition data.                                                                                                                                                                           |
| "Our free trial makes the SaaS reasonable."         | The host judges reasonableness, not you; a trial that expires mid-run invites a ruling against it, and an API call cannot run in a code-competition submission.                                                                                                       |

## Interview

One question at a time; skip what the request already answers.

1. Product: does it run inside a Python or R notebook (library, model, embedded mode), or only through a hosted API with a key?
2. Who posts: named staff with a Kaggle history, staff starting as Novice, an organization profile? Anyone already Expert or above?
3. Goal and date: adoption by practitioners, a dataset or model as distribution, or a competition? A launch date?
4. Hours per week, and who can answer competition-forum questions within a day?

Answers 1 and 3 re-rank the surfaces below; say which answer moved which row.

## Fit verdict

Decide before any plan. The test is whether a stranger can fork a notebook and run your product in it with internet off.

- **Invest:** the product installs in a notebook and runs offline (library, model weights, local mode), and someone can answer forum questions weekly.
- **Notebooks and datasets only:** hosted API with a free tier; standalone tutorial notebooks with internet on and Kaggle Secrets, no competition starter notebooks for code competitions.
- **Skip:** no data or ML workflow touches the product (CI, auth, frontend tooling), or the product has no free path. Kaggle's account total is not your audience; point the user at a channel where their developers already are.

## Kaggle surfaces, ranked by value per hour

Efficiency: substantive answers in active competition forums > standalone notebook on a public dataset == dataset with a starter notebook > competition-attached starter notebook > organization profile > Kaggle Models listing > Accomplishments post > Community Hackathon > Community Competition > Featured Competition. The tie holds because both take a day and keep earning votes and forks for months; a starter notebook ranks lower only because its audience ends with the competition.

Compliance cost: Featured Competition > Community Competition == Community Hackathon (prize payout, tax, winner licence) > competition-attached notebook (OSI licence by rule) > everything else.

| Surface                                                    | Payoff      | Value | Low effort |
| ---------------------------------------------------------- | ----------- | ----- | ---------- |
| Full answers in competition forums, no links (earn-first)  | compounding | ++    | +++        |
| Standalone notebook solving a real task with the product   | compounding | +++   | ++         |
| Dataset you own (benchmark, schema sample) + notebook      | compounding | +++   | ++         |
| Starter notebook attached to an active competition         | one-shot    | +++   | +          |
| Organization profile owning datasets, models, competitions | compounding | +     | +++        |
| Kaggle Models: weights with variations and licence         | compounding | ++    | +          |
| Accomplishments post with what changed and why (no medals) | one-shot    | +     | +++        |
| Community Hackathon or Community Competition you host      | one-shot    | ++    | --         |
| Featured Competition with Kaggle                           | one-shot    | +++   | ---        |

- **Re-rank:** an offline-capable library promotes the competition starter notebook to second, behind forum answers, which build the standing it needs; an API-only product drops it; a dataset vendor promotes the dataset row; an LLM-eval or model vendor checks Kaggle Benchmarks, where community benchmarks may be the strongest surface (confirm current terms live).
- **Sponsoring inside someone else's competition** (prizes, credits, tooling) is the host's call and must clear the same external-tools and Reasonableness rules.
- **The order starves** staff competing under the company name, as H2O.ai and NVIDIA do with employed Grandmasters [practitioner]. A gold finish whose write-up credits the product beats any notebook, because leaderboards award medals, not votes. Promote it when the product helps win, the team can spend months per competition, and staff use only the public, free or reasonably priced release any competitor can install; unreleased builds risk disqualification in public.
- **Default rung:** forum answers from week 1 and one standalone notebook from week 3, run in parallel. Move up to a dataset or starter notebook once that notebook survives the fork test below.

## What Kaggle's ranking rewards

**Do more:**

- Earn votes in the first week; Hotness favours recent votes and views [platform docs], and an old staff post describes weighting the past week [platform staff, formula unpublished].
- Reach readers past Novice tier: votes from Novices (until they reach Contributor), self-votes and votes on old posts (about 90 days [practitioner]) do not count toward medals [platform]. Get each poster to Contributor in week 1 (complete profile, verified phone, one notebook run, one competition submission, one comment, one vote) [platform].
- Name the product in tags and the subtitle; titles that name the task ("Hybrid search over 2M arXiv abstracts") get forked, so put the product in the title only when the task is the product.
- Fill every dataset usability field (subtitle, tags, description, cover image, source, licence, file and column descriptions, a public notebook); the 0-10 score feeds dataset search [platform UI, weights unofficial].
- Publish new versions when the content changes, with a changelog cell.

**Do less:**

- Reruns for position, copied notebooks, vote requests in any form [platform].
- Placeholder API-key cells: every fork breaks, and a broken fork costs the comments section.
- Marketing cells: one "About {product}" cell at the end, not a banner on top [practitioner].

## The fork test

A demo notebook passes only if a stranger forks it and runs all cells. Before publishing:

1. Have one colleague fork it once from their own account and run all cells; Kaggle allows one account per person, so never create a second one. Their fork counts as a vote, so never spread the test across the team.
2. In a code competition (its Overview says so and lists the runtime and internet limits), install offline: Kaggle's Dependency Manager where the editor still offers it, otherwise an attached dataset or model holding the wheels or weights. Elsewhere a pinned `pip install` with internet on is fine.
3. If an API key is unavoidable, read it from Kaggle Secrets under a named label, and say in the first cell which label to add. Secrets never follow a fork [platform] and cannot be used with internet off [practitioner].
4. Fit runtime under the session cap and the weekly GPU quota; state the accelerator in the first cell.
5. Pin package versions, or pin the notebook to its original environment in settings; image updates break old notebooks [practitioner].

To get a package preinstalled in Kaggle's image, open an issue or PR on the Kaggle/docker-python repository; staff set "a decently high bar" [platform staff].

## Hosting a competition

1. Pick the track:
   - **Community Competition:** free, self-serve, prediction prizes up to about $25,000; the host pays and ships prizes.
   - **Community Hackathon:** self-serve, prize pools up to about $10,000, judged write-ups; confirm who funds the prizes.
   - **Featured Competition:** partnership with Kaggle; budget class well above the Community prize cap, negotiated.
   - **Research Competition:** scientific problems, usually academic or non-profit hosts. Kaggle's research grants go only to those, so a vendor usually joins as data partner or co-sponsor.
2. Tell the user that Community Competitions, like Getting Started and Playground ones, typically award no points or medals [platform], so expect students and newcomers, not Grandmasters; Featured and Research competitions usually do.
3. Choose the winner licence before launch (OSI such as Apache 2.0 or MIT, CC-BY 4.0, or write-up only). Never plan to keep winning code proprietary without saying so in the rules.
4. Exclude your own staff and judges from prizes in the rules.
5. Staff the forum daily for the whole run; an unanswered data question in week one sets the tone.

Read [references/limits.md](./references/limits.md) for per-surface caps, prize and licence obligations, with enforced versus policed labels, before quoting any number.

## Cadence

1. **Weeks 1-4, earn first.** Each poster answers 2-3 forum questions a week in competitions the product helps with, in full, no links [practitioner]. Request the organization profile.
2. **Week 3, first notebook.** Standalone notebook on a public dataset; fork test passed; posted by a named staff member, its data under the organization.
3. **Weeks 4-8.** One notebook or dataset every two weeks. Answer every comment within two days.
4. **When a competition fits, week 5 at the earliest.** Starter notebook in week 1 of that competition, in its own Code tab, with the full method and no vote request.
5. **Monthly.** Read forks, copies and comments per notebook; drop topics that drew none.

## Removed, warned or reported

1. Delete the offending post or notebook yourself; never repost it reworded.
2. Replace a copied notebook with one built from the data, crediting the original author by link.
3. Ask staff in the Product Feedback forum only about the rule, never for votes or restored medals.

## Measure

Targets are self-set; Kaggle publishes no vendor benchmark.

- Forks and copy-and-edit counts per notebook from accounts outside the company (forks also count as votes), dataset downloads, model downloads; votes only as a secondary signal.
- Signups from a tagged link in the closing cell; competition notebooks that import the package; `kagglehub` downloads when your own docs pull the dataset or model from Kaggle.
- Hygiene, pass threshold zero: removed posts, staff warnings, plagiarism reports, medal retractions.

## Output

In order: fit verdict; interview answers that re-ranked the surfaces; ranked surfaces; fork-test result for each notebook; eight-week cadence with owners and hours; competition plan when relevant, with track, prize, licence and staff exclusion; filled templates from [references/templates.md](./references/templates.md); metrics. Run drafts through your preferred humanizer skill.

## References

- samber/developer-relations-skills@developer-tutorial - writing the notebook's teaching content.
- samber/developer-platform-skills@huggingface-playbook - publishing the same weights on the Hugging Face Hub.
- samber/developer-platform-skills@sdk-package-publishing - making the package installable from PyPI before Kaggle.
- samber/developer-relations-skills@developer-event-sponsorship - sponsoring hackathons Kaggle does not host.
- samber/dev-event-organizer-skills@hackathon-cash-prize - paying and taxing hackathon prizes.
- samber/developer-relations-skills@devrel-analytics - attributing signups from notebook links.
