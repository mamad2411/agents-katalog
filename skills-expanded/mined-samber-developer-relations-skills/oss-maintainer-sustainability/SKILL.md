---
name: oss-maintainer-sustainability
description: "Plans how an open-source maintainer keeps a project going without burning out, or leaves it without stranding users: load against a time budget, published scope and response limits, maintenance-only mode, co-maintainer recruitment, funding as one lever, and stepping down by handover or archive with end-of-life signals. Use whenever an open-source maintainer says they are burned out, want to step back, quit, hand off or archive a library, need a co-maintainer, or feel guilty about an unanswered backlog - even if they only say it became too much. Do NOT use for GOVERNANCE.md (samber/developer-relations-skills@oss-governance), labels or stale bots (samber/developer-relations-skills@oss-issue-triage), or sponsor tiers (samber/developer-relations-skills@oss-sponsors-fundraising)."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# OSS Maintainer Sustainability

You help one maintainer decide how much of a project they will carry, then make that decision true: lighter, shared, or ended, with users told and nothing handed to the wrong person.

The subject is the maintainer, not the project. Three Tidelift surveys found 58-60% of maintainers quit or considered quitting a project, so treat overload as the base rate, not a character flaw. Two causes recur, and both shape the levers below:

- **Overload**: inflow times implicit expectation exceeds the hours the person has, with no published contract between them.
- **Life change**: the top reported reason for quitting is that other things in life and work took priority.

Neither is solved by trying harder. Both are solved by a published contract, a smaller surface, and a planned exit.

Leaving is a legitimate outcome; never argue someone out of it. The worst incidents on record came from bad handovers (event-stream 2018: keys given to a volunteer who asked; xz-utils 2024: a volunteer pushed forward by sock puppets) or from owners leaving destructively (left-pad's unpublish, colors/faker's sabotage). A quiet, announced exit caused neither.

If the user describes a crisis rather than overload (hopelessness, health effects, "I can't do anything anymore"), say plainly that this deserves support from a person. Then keep the plan to its smallest safe step: a published pause.

Every figure and case cited here, and which numbers are this skill's own baselines, is in [references/published-findings.md](./references/published-findings.md).

## Interview

If you can read the repository (forge CLI, API or web), check first: README, open issue and PR counts, last release, contributor graph, who can merge and publish. Infer what you can and confirm it in one line. Without access, ask for inflow as a monthly range inside question 2 and mark those numbers as estimates. A tired reader abandons a long interview, so stop at six questions.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

Ask one question at a time, multiple-choice where possible:

1. **Destination.** Where do you want to be in six months? (a) same project, far fewer hours (b) same project, shared with others (c) not maintaining it (d) not sure yet.
2. **Budget.** How many hours a week do you want to give it, honestly, and how many does it take now? A range is fine.
3. **Drain.** What costs the most energy: issue volume, support questions, reviewing PRs, AI-generated issues or PRs, hostile or entitled comments, security reports, release chores, or the guilt of the backlog?
4. **People.** Who besides you has done real work here in the last year (reviews, answers, merged PRs)? Who can merge, and who owns the registry name and the repository namespace?
5. **Users.** Who depends on it: hobbyists, other open-source projects, companies? Is it a transitive dependency of something large? Do you maintain other packages too?
6. **Clock and money.** Is there a date (new job, leave, a promised release)? Is anyone paying for this work, and do you want more of your hours paid, or fewer hours total?

If the user answers (d), brainstorm before any plan: lay out the three destinations with what each costs them and their users this quarter, recommend one, and let them choose.

The answers re-rank step 2. Say which answer moved which move:

- **Hard date**: promotes moves that land in a day. When question 1's horizon and question 6's date disagree, the earlier one is the deadline.
- **"Fewer hours total"**: deletes funding for the user's own hours; funding a co-maintainer's hours stays.
- **Drain**: the top drain gets the first targeted move. Hostile or entitled comments promote moderation (`samber/developer-relations-skills@developer-community-moderation`) above the backlog reset; release chores promote automation; AI-generated inflow promotes intake cuts.
- **Employer-paid maintainer**: the load is a staffing decision. Bring the ledger to the manager and ask for a second maintainer or a scope cut before cutting your own hours. Check who owns the registry name and repository namespace: employees often publish from personal accounts, so move those to company-owned accounts before any role transfer.
- **Several packages**: triage the portfolio first. Rank packages by dependents and by drain; plan the heaviest one, and freeze or archive the ones nobody depends on.

## Step 1 - Measure the load against the budget

Build a one-screen ledger, never a guess:

- **Inflow**: new issues, PRs, discussions and direct messages per month.
- **Backlog**: open issues split into waiting-on-reporter, waiting-on-maintainer, confirmed bugs, and feature requests.
- **Hours**: what it takes now versus the budget from question 2.
- **Transition hours**: one-time setup the chosen moves cost, with an end date. Moves of a few hours each do not fit a two-hour week; budget a short, dated bridge above the steady-state budget instead.
- **Concentration**: who else can merge, release and publish. A single name on the publish right turns a departure into a stranded package. For the full credential inventory and absence factor, use `samber/developer-relations-skills@oss-governance`.

Read the shape against Nadia Eghbal's taxonomy. Many users and very few contributors (a "stadium") is the usual shape of a popular single-author library, and there contributors do not appear on request. Cut the contract before waiting on a co-maintainer.

## Step 2 - Pick the moves, ranked by efficiency

The moves are ordered by what they return per hour of the maintainer's effort. They are not alternatives: most plans take the top three, then add sharing or an exit.

Default order for "stay, lighter": `publish the contract > declare a maintenance tier > cut intake > automate chores > announced pause > backlog reset > recruit a co-maintainer > funding`

| Move | You do | You get | You owe |
|---|---|---|---|
| **1. Publish the contract** | an hour: README status line, weekly hours, response window, scope, what you will not do | every arriving user calibrated at once; guilt turned into policy | keeping the window, so state one you can keep |
| **2. Declare a maintenance tier** | an hour or two: active, maintenance-only (security and runtime-compatibility fixes), or frozen | feature requests close by pointer, not debate | saying no to features you might like |
| **3. Cut intake** | an hour or two: issue forms, support routed off the tracker, PRs limited to collaborators if inflow is unsolicited | fewer items arrive at all | the PR limit closes the pipeline move 7 recruits from, so skip it when move 7 is planned |
| **4. Automate chores** | a couple of hours, mostly testing one release: grouped dependency updates, release tooling, publishing from CI | release chores stop costing evenings | reviewing the bots' output |
| **5. Announced pause** | ten minutes: dated notice, forge status, who reads security reports meanwhile; skip when an exit is under a quarter away | rest without the silence that reads as abandonment | coming back, or turning the pause into an exit |
| **6. Backlog reset** | a couple of hours: one announced, labelled sweep of stale, unreproduced items | the guilt pile gone | a notification wave and some angry replies |
| **7. Recruit a co-maintainer** | weeks of mentoring before any saving | the only move that compounds, and the precondition for a handover | supervision, and keys withheld for months |
| **8. Funding** | weeks to set up, then reporting | paid hours, yours or a co-maintainer's | sponsor or contract expectations, which are new load |

The order starves move 7: highest long-term value, highest effort, net negative for the first months. Promote it to first when the destination is (b), when a trusted candidate already exists, or when the exit is more than a quarter away and the users would gain from a handover.

Move 8 converts an existing willingness to work into paid time; it does not reduce inflow. Donations rarely reach a salary: core-js's author reported about $400 a month in early 2023, for 250 million monthly downloads and about 250 hours of work a month. Prefer time-based money (an employer's hours, a fellowship, a support contract with a company that demands service levels) over donations, and hand the program design to `samber/developer-relations-skills@oss-sponsors-fundraising`. When the user wants the project to pay a salary through something companies buy, use `samber/developer-relations-skills@oss-monetization`; it adds load, so run it only after the contract and tier moves above.

The order is a default, not a law; re-rank it with the interview answers above. A user who enjoys mentoring makes move 7 cheaper than it looks.

Derive the response window from the budget, never from a norm. Replies a week = weekly hours x 60 x share of time on the tracker / minutes per first reply. Absent better numbers, assume half the time on the tracker and 15 minutes per reply (self-set). If monthly inflow exceeds about four weeks of replies, cut intake before publishing a window.

For ready-to-paste status blocks, window wording, saying-no replies and the backlog-reset announcement, read [references/boundary-kit.md](./references/boundary-kit.md).

## Step 3 - Share the load without handing over the keys

Use this when move 7 is in the plan or the destination is a handover.

- Recruit from people who already showed up: reviewers, frequent answerers, authors of good PRs, and companies whose products depend on the package.
- Ask with the role spelled out: what they would do, how many hours, what they get.
- Grant the ladder fast and the keys slow. Triage and review rights are cheap to give and revoke. Merge comes after a release made together; registry publishing and organization ownership come last, after a supervised release, never in the same act as merge.
- Count track record earned before the invitation: two years of good reviews can compress the triage and review stages, never the publishing stage.
- Treat urgency as a red flag. A newcomer asking for publish rights before merge rights, or third parties loudly naming who should take over, is the xz-utils pattern. Decline in writing and keep reviewing their pull requests normally.

Candidate sourcing, the invitation, the decline reply and vetting signals are in [references/co-maintainer-recruitment.md](./references/co-maintainer-recruitment.md). The full trust ladder and credential inventory belong to `samber/developer-relations-skills@oss-governance`.

## Step 4 - Step down well

Use this when the destination is (c), or when the plan names an end date. `>` means more of that axis:

- value to users: `handover to a vetted successor > transfer to a custodian > freeze then archive > archive now`
- effort for you: `handover to a vetted successor > transfer to a custodian > freeze then archive > archive now`
- supply-chain risk: `handover to a vetted successor > transfer to a custodian > freeze then archive == archive now`
- unpatched-vulnerability risk: `archive now > freeze then archive > transfer to a custodian == handover to a vetted successor` (the last two tie because both keep someone shipping fixes)
- efficiency for a maintainer with no vetted successor and no custody offer: `freeze then archive > archive now`; a custody offer or a vetted candidate re-opens the full menu

The supply-chain tie holds because an archived package ships nothing new, so nothing malicious. Archiving loses on vulnerabilities instead: known flaws stay unfixed. That is why the default is **freeze then archive**: it keeps security fixes during the notice period, then ends with an explicit statement.

- Move up to a custodian when an organization that depends on the package offers custody with more than one admin.
- Move up to a handover only with a successor who has passed the staged access in step 3.
- When a candidate exists but is not yet vetted, run both tracks: announce freeze then archive, with a dated gate where the handover replaces the archive if the candidate is ready.

Whatever the path, do all of these:

1. Tell the largest dependents' maintainers privately a few days before the public notice; they are the likeliest custodians, and the ones a surprise hurts most.
2. Publish a dated announcement in the README and wherever users read: status, why, what still works, license permission to fork, alternatives, timeline, and what happens to security reports. Explicit end-of-life notices measurably speed downstream migration; silence strands most dependents.
3. Add the registry's deprecation signal as well. Set upload-blocking statuses (PyPI's archived status) only on the archive date, or the promised security fixes become impossible.
4. With a successor or custodian: move publishing to CI-based trusted publishing where the registry supports it, transfer registry ownership yourself while reachable, then the rest of the credentials.
5. Without a successor: keep your forge and registry accounts alive with two-factor authentication and a recovery contact, and never delete them. Revoke CI and personal tokens only. A deleted account or lapsed email domain lets someone else claim the name.
6. Give notice proportional to dependents: same week for a personal tool, about a month for a library other projects use, a quarter or more for a transitive dependency of large projects.

Per-registry mechanics and the announcement templates are in [references/stepping-down.md](./references/stepping-down.md).

## Deliverable

One plan, validated section by section with the user before the next is written:

```markdown
# Sustainability plan - <project> - <date>
## Destination - lighter / shared / ended, and by when
## Ledger - inflow, backlog split, hours now vs budget, transition hours and end date, top drain, who holds publish rights
## Moves - chosen moves in order, each with effort, what it buys, and the date it ships
## Contract - the README status block and response window, ready to commit
## People - candidates, the role offered, access stages and dates (if sharing)
## Exit - path, announcement, registry signals, account and credential plan, notice period (if leaving)
## Review - date to re-read the ledger, and what triggers an earlier look
```

## Health check

Self-set baselines; say so when you present them.

1. **Budget held**: four weeks after the plan, actual hours sit within the stated budget. Over budget means the next move, not more effort.
2. **Contract kept**: the published window was met for most new items. A missed window means the window was wrong, so widen it publicly.
3. **No single key holder**, or an end date: every publish right has two holders, or the plan names the date the project ends.
4. **End state written**: the README says active, maintenance-only, seeking maintainers, paused until a date, or archived, plus one line on any transition under way.
5. **Security path named**: someone reads security reports, or the README states no further security fixes.

Iterate until 3, 4 and 5 pass before calling the plan finished; schedule 1 and 2 for the review date.

## Common failure modes

- **Funding first.** Money fixes neither inflow nor succession.
- **Self-care listicle.** Sleep and weekends matter, but a plan that changes nothing about inflow sends the user back to the same queue.
- **Promising what burned them.** A 48-hour window from someone with three hours a week is a new source of guilt.
- **Silent bulk close.** A bot closing hundreds of issues unannounced reads as contempt and floods every subscriber.
- **Keys to the first volunteer.** Relief comes before a successor.
- **Repo transferred, package not.** The successor owns the code and cannot publish, or the old owner keeps a forgotten token.
- **"Maybe I'll be back."** An ambiguous exit leaves users waiting. The repository can be unarchived later, but users who migrated will not come back, so decide once.

## References

- `samber/developer-relations-skills@oss-contributor-onboarding` - the path that grows future co-maintainers.
- `samber/developer-relations-skills@oss-security-disclosure` - who handles security reports while you step back.
