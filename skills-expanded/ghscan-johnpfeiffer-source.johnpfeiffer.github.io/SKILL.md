Title: Real velocity from a Backlog Deferred and a Skill'd Agent
Date: 2026-08-10 09:11
Tags: ai, agent, productivity

[TOC]

# Why the heck am I reading this?

You have a thing you're putting off because it's boring and manual. You want the outcome, but not the toil.

10x velocity on shiny-new-thing is the wrong framing, nobody would have dared invest in your black hole of a backlog.

Everyone's raving about their Agents - so you're agent-curious.

Your knowledge was the prize the whole time, **you are the main character.**

# It was a Skill issue

I love high-quality content, high signal and human-curated, about software engineering and people management. But I had only published 20% of the things I'd accumulated. *(great articles, blogs, podcasts, etc. - like a dream deferred)*

High quality meant slow because I make things useful and accessible: categorized, meaningful title, published date, canonical source URL, no duplicates, etc.

I broke the ice and I used a coding agent to look at my hand-crafted ugly JSON:

- it immediately **fixed a syntax issue**
- then it **found duplicates** and suggested which one to remove
- and it found numerous ways to look up published date

Ok - so everybody gets lucky once.

## Meta prompt - ask the agent to automate itself

> The human has the skill - the agent creates and updates the skill file

"Now a question for you, can you take an Apple Podcast link and sleuth up the original more canonical podcast link (but we can use the apple podcast one as the alternate?) - and of course the same process as before, in fact create a Skill markdown for this task in the pr too

turing award Liskov https://podcasts.apple.com/us/podcast/the-peterman-pod/id1777363835?i=1000763787598"

The agent took that prompt and turned into a well-documented runbook <https://github.com/johnpfeiffer/favorites/blob/main/.factory/skills/add-favorite/SKILL.md>

> Now I only need to use very short messy prompts

The "Skill'd Agent" reads a markdown file encoding how entries are structured, where they go, what metadata to include, how to handle duplicates, that it needs to surface questions, etc.

*We shifted from imperative to **declarative**...*

# Economically unreasonable

ROI for 1 person's customized favorite links app? <https://feneky.com/links/tags> 

Who would pay a team of engineers to write deterministic code that:

- starts from a URL and searches for a canonical URL, including reading arbitrary podcast and RSS feeds
- identify the exact podcast episode from a single unique identifier
- scrapes that website for the published date
- checks archive.org for the URL and saves that as an "alternate-url"
- determines the media type (Book, Podcast, Video, Blog, Article, Paper)
- uses the context from the URL, the user input, website, and previous favorites to generate a customized title
- select accurate Tags from a pool - and sometimes propose new ones (i.e. people's names)
- saves it, no duplicates, in one of 5 categorical JSON files
- creates a human-readable report on what was accomplished
- identifies and presents options on ambiguous situations

More than just reviewing the stream of ai-generated pull-requests, my job is to look for patterns and improvements in the process. It's non-deterministic so it needs a sharp eye and a deft touch. 🤠

And with a clean and growing data layer, I'm energized to build even more ambitious functionality into the Links app.

## Real Prompts with Receipts

> The commit history shows 15 commits over 5 months manually, then 25+ commits and 12 PRs in 4 days with the agent

Instead of very precise and detailed specifications - which took time and energy, I'm now able to quickly give loose and casual requests.

> In Favorites I added the published date as a later feature, can you look up the following ones (all from Lenny's Podcast) and update their JSON entries?

> great work, now pull latest from main and add these new Links (please lookup date, alternate url, suggest Tags - when possible re-use existing), to the JSON file that best fits thematically, questions?

> yes please fix the typos for Communication, upper casing Anti-Patterns, and Ebay (I think eBay is the real name?) Also, "Paper" is a useful media type, do any exist in Links and if so what are they given as a current media type?

*I still do have to review and approve the requests, it's the price of a high quality bar.*

Recent agent Pull Requests at <https://github.com/johnpfeiffer/favorites/pulls?q=is%3Apr+is%3Aclosed>

## Prompt the Agent to improve itself

> I have noticed you found some of my favorite podcasts like Lenny's or Manager Tools or SE Radio have patterns to their links and publication dates (and you downloaded or created some indexes?) , can those approaches be added to Skills and indexes to the repo?

*...For shows in `podcasts/registry.json`, grep the committed episode index instead of downloading the feed...*

<https://github.com/johnpfeiffer/favorites/pull/10/changes>


# Permissions and Guardrails

> Agents are becoming wickedly good at wrecking virtual stuff

Imagine leaving a car driving forward indefinitely - regardless of pedestrians, lack of visibility in bad weather, etc. 

This is how I kept the agent scoped and managed:

1. The agent has its own separate GitHub account, and is a collaborator on the code repository. All Pull Requests require a (human) review.

*Before when it was just me, I would edit files and write to main directly - why add coordination overhead with myself?*

2. The agent runs in an isolated cloud environment. It cannot bork my laptop or steal my credentials.

*I do give it "high autonomy" and internet access, so I should probably add some sort of deterministic tracker, Agent Observability and Evals are on my very urgent todo-next list*

3. When the agent is done then the UI shows me its final output, usually prefaced with "Done". It does not work when it does not have a job.


At a high level it's still "software does actions that a human asked for". I strongly suspect that if I ran it on a schedule and gave it a more open-ended task ("get me 5 new unique interesting links") that not only would I be burning tokens for diminishing returns (or outright slop), over time the acting unobserved towards a vague reward function may even lead to bad or downright toxic behaviors.


# Gotchas - Thanks I Learned

Confused Agent? Maybe too much in the context. I found after 3 or 4 requests in the same "session/conversation" it loses the plot and I need to create a new session. Agents do best given only the correct context to focus on.

Messy environment? Agent runs would store temporary files and leave code repos with stale branches. After a while this would confuse and trip up the agent.

So about once a week I enforce the adage "cattle not pets" and redeploy the Railway container; cloud-first is an ephemeral environment. The re-deploy automatically installs the latest agent harness, starts with a clean file system, and pressure-tests the Skill.md - that the system and its outcomes are reproducible.

*Infrastructure as code and transparent, clean builds are also security best practices for auditability and traceability. And ephemerality disrupts persistent threats.*

That **Skill.md** is the "memory"; **writing and text files are not obsolete yet.**

# Human as the bottleneck

Doing this for a single workflow is doable. When you start spinning plates, then context switching and keeping up becomes the challenge.

Each agent in a different domain and code repository, doing a different task, waiting for the human.

When you're not unblocking them it can almost feel like a wasted opportunity. *I've heard people start sleeping less. 8|*

> So now I rubber-stamp AI slop?

Nope. Hard pass.

Do: higher level work like designing the system to run longer before needing human intervention, and safely!

Most importantly, your intentionality and judgment is deciding what is high quality, what is truly valuable.

You are the bottleneck because your time is the most valuable. **You are the main character.**


# References

I used Factory and its Droid agent with the Kimi K3 model *(previously used the GLM 5.2 model)*; open-weight models are surprisingly good (and relatively inexpensive).

- <https://blog.john-pfeiffer.com/a-coding-agent-in-the-cloud-with-factory-and-railway/>

The favorites repo: <https://github.com/johnpfeiffer/favorites>

Tip of the hat to the much more famous (and open-sourced earlier, pre-everything-https) project:

<https://github.com/charlax/professional-programming/commit/33b7909aa9e7d99a7e4cc4e5205c9baabdc0899a>
