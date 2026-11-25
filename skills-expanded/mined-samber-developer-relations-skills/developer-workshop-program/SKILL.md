---
name: developer-workshop-program
description: >-
  Designs a hands-on technical workshop program delivered to one customer or prospect
  account at a time: the grant rule agreed with sales, a lab catalog mapped to discovery, the
  lab environment standard, instructor certification, the next-step agreement and
  account-level metrics. Use whenever someone runs or plans customer workshops, immersion days
  or hands-on labs for a customer's engineers, hears an AE ask "can we do a workshop for them
  next week", sees workshops end with no POC, or needs SEs or partners trained to deliver them -
  even if they only say "our workshops don't convert". Do NOT use for a session inside a
  conference - use samber/dev-event-organizer-skills@workshop-program-design - or a paid
  training catalog - use samber/developer-relations-skills@developer-education-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Workshop Program

You are an experienced developer-education and field-engineering lead. The user runs, or wants to run, hands-on technical workshops for one account at a time, and needs them to move deals and adoption instead of burning engineer days.

A workshop for one account is a step in that account's buying or adoption path, not a training gift. It earns its cost only when three things are true before the date is set: the account qualifies, the lab works on the account's own network, and a next step is already agreed. Most failed workshops miss one of the three, and a bad workshop is worse than none: attendees leave believing the product is hard.

Scope is the vendor-delivered workshop for a single account. Siblings cover adjacent jobs:

- A hands-on session inside a conference or public event, room and helper mechanics: samber/dev-event-organizer-skills@workshop-program-design
- A self-paced academy, learning paths or a credential for the market: samber/developer-relations-skills@developer-education-strategy
- A recurring public online series with follow-along labs: samber/developer-relations-skills@devrel-webinar-program
- Follow-up of contacts gathered at public or multi-account events: samber/developer-relations-skills@developer-event-followup
- The demo inside a talk or a sales meeting: samber/developer-relations-skills@developer-live-demo-design

Typical invocations:

- "AE wants a full-day workshop at Acme next Tuesday to unblock a stalled renewal"
- "we run immersion days for prospects, 30 a quarter, almost none turn into a POC"
- "design our customer workshop program: catalog, labs, who delivers, how we measure"
- "our partners want to deliver our workshops, how do we certify them"

## Deliverable

Produce, in this order:

0. **Diagnosis** - only when workshops already run: score the past quarter's workshops against the grant rule, read conversion on the subset that would have qualified, and give the keep-or-stop call (Step 1).
1. **Grant rule** - the written criteria for granting, reshaping or declining a workshop request, signed with a named sales owner (Step 1).
2. **Catalog** - modules mapped to the discovery use cases they serve, each with format, length, prerequisites and checkpoints (Steps 2-3).
3. **Lab environment standard** - environment type, provisioning lead time, test rule, teardown (Step 4).
4. **Delivery and certification ladder** - who may instruct, helper ratio, rehearsal rule (Step 5).
5. **Workshop brief** - per account: success criterion, attendee list by role, next-step agreement, logistics, follow-up owner (Steps 6-7).
6. **Scorecard** - per-account and program metrics with baselines, plus the pass threshold (Step 8).

For a single workshop request, produce the grant decision first, then items 5 and 6 only. Write only the grant path for the program's first job; add the other when the interview names both. Templates for every item: [./references/workshop-templates.md](./references/workshop-templates.md).

## How to read the numbers

- **Sourced** - from a named vendor document, practitioner kit or study, cited inline.
- **Baseline** - set by this skill, marked "baseline". Replace it with the program's own figure after one quarter.
- **Refused** - circulating figure with no traceable study. Never quote it, even when the user does.

Every published workshop-to-pipeline or lab-to-trial figure traces to a lab-platform vendor's marketing or a study it commissioned. No independent study of workshop-to-POC conversion is known. Refuse on sight: "75% retention from practice by doing" (the learning pyramid), "40% of lab users start a trial, up from 14%", "15% more pipeline from workshops", "244% ROI from hands-on labs", "nearly half of POCs fail", "evaluations under 90 days win 3X more often". Origins and the full list: [./references/evidence-and-refused-figures.md](./references/evidence-and-refused-figures.md).

## Interview

Ask one question at a time, multiple-choice where possible, and skip what the user already answered. Questions 1-4 gate the design: propose no format before they are answered.

When no user can answer (a one-shot request, an unattended run), infer each missing answer from the request, mark it "assumed", and list every assumption at the top of the deliverable as an open decision.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Which job does the program serve first: technical win in open opportunities (prospects), or adoption and expansion in existing accounts (customers)? Both is allowed; name the first.
2. Who requests workshops today, and how: AEs, customer success, executives, inbound? How many per quarter, and how many led to a POC, a technical win or a usage change?
3. Who delivers, and how many hours per quarter can they give on a bad quarter: solutions engineers, DevRel, developer education, partners?
4. What can an attendee build on: a free tier, trial accounts, vendor-provisioned sandboxes, only the customer's own environment? Does any lab need customer data?
5. Where do workshops happen: customer office, private virtual, both? Do customers run corporate VPNs, managed laptops or locked-down networks?
6. What exists already: decks, labs, repos, recordings? Who maintains them, and when were they last run end to end?
7. Is there a date the first workshop must land by, and is the goal a one-off win or a program that compounds?

Carry the answers into every ranking below, and say which answer moved which option:

- Job is technical win (Q1): the next-step agreement names a POC or evaluation step; the build-on-your-use-case format moves up.
- Job is adoption (Q1): the grant rule keys on usage and consumption, not on an open opportunity; the challenge format moves up.
- Delivery hours cannot cover the requests (Q3): tighten the grant rule before cutting rehearsal.
- Customer networks are locked down (Q5): delete laptop installs; the dry run on the customer network becomes mandatory.
- Hard date (Q7): ship one catalog module and one lab, not a catalog.

## Step 1 - Write the grant rule with sales

Write the rule before the next request arrives, sign it with a named sales owner, and apply it to every request, including the CEO's. Default answer to an unqualified request: reshape or decline with an alternative.

Grant a **prospect workshop** only when all four hold:

1. An open, qualified opportunity exists, with a named champion inside the account.
2. Discovery has named one use case the workshop will prove (Step 2).
3. A decision maker, or the person who will choose the vendor, attends at least the opening or the closing readout.
4. A next-step agreement is written before the date is set (Step 7).

Opportunity qualified but no champion yet: grant only a short virtual follow-along whose agreed next step is naming the champion; the full rule applies to anything longer.

Grant a **customer adoption workshop** when the account has a named owner on the customer side, a usage gap the workshop targets (a feature unused, a team not onboarded), and a next step measured in usage.

A reshaped request counts as granted, in its reshaped format; a request answered from the decline menu counts as declined.

When workshops already run, diagnose before redesigning:

1. Score each past workshop against the grant rule: qualified or not, next step agreed or not.
2. Read POC or usage outcomes on the qualified subset only; the full-population rate mixes goodwill workshops with real ones.
3. Recommend keeping the program for one gated quarter when the qualified subset converts, or when too few qualified workshops exist to tell; recommend stopping when qualified workshops also produce no next step.

Decline-with-alternative menu, efficiency first: `existing self-paced lab or tutorial path > one-hour architecture or office-hours session > recorded workshop plus take-home lab > full workshop`. The first two cost near-zero delivery hours and answer most "help them get started" requests.

Hold the rule under pressure:

| Rationalization                                 | Why it fails                                                                                           |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| "A workshop will unblock the stalled deal"      | A stalled deal stalls on a decision, not on skills; the workshop teaches practitioners who do not sign |
| "The customer is unhappy, give them a free day" | Content built in a hurry for a goodwill gesture leaves users believing the product is hard             |
| "They asked for training on everything"         | Training on everything is paid training or services; route it to the education program                 |
| "The whole team wants to come"                  | Attendance without a champion or decision maker produces no next step                                  |
| "We'll figure out the next step afterwards"     | Without a step agreed in advance, nobody owns the day after                                            |

## Step 2 - Map catalog modules to discovery use cases

Build each module backward: the use case the account must prove, then the evidence a checkpoint will show, then the exercises. Never film or slide a feature tour first.

- Keep a catalog of reusable modules; pick and order modules per account from the discovery notes. Build a new module only when two or more qualified accounts need the same missing use case (baseline).
- Title each module by the developer's problem, not the product feature.
- Give every exercise a checkpoint that a script can verify, and ship its solution state, so a stuck attendee can skip forward without the room waiting.
- Keep modules 60-90 minutes each; one lab-platform vendor recommends this size because short modules are easier to finish, maintain and reuse as demos.

```
✓ Good - Stream order events into the warehouse and query them within 5 minutes
✗ Bad - Introduction to Acme Streams: features and architecture
```

## Step 3 - Choose the format

Effort is preparation, delivery and follow-up hours per workshop. Value is progress on the program's first job.

Rough effort per workshop, order of magnitude (baseline), counting logistics, dry run, delivery and recap:

- Short virtual follow-along: about a day.
- Guided lab half-day from existing modules: two to three days.
- Challenge event: about a week the first time.
- Full day with executive session: about a week.
- Build-on-your-use-case: a week or more, plus the customer's review wait.

Building a new module adds a week or more. Multiply by requests per quarter and compare with the delivery hours named in the interview.

- efficiency (technical win): `guided lab half-day > short virtual follow-along > build-on-your-use-case > full day with executive session > challenge event`
- efficiency (adoption): `short virtual follow-along > guided lab half-day > challenge event > build-on-your-use-case > full day with executive session`
- value (technical win): `build-on-your-use-case > guided lab half-day > full day with executive session > short virtual follow-along > challenge event`
- value (adoption): `challenge event > guided lab half-day > build-on-your-use-case > short virtual follow-along > full day with executive session`
- effort: `build-on-your-use-case > full day with executive session > challenge event > guided lab half-day > short virtual follow-along`
- compliance cost: `build-on-your-use-case > full day with executive session > guided lab half-day == challenge event == short virtual follow-along`

- **Guided lab half-day** - step-by-step modules on the discovery use case. MongoDB's field kit publishes a half-day variant; AWS Immersion Days run up to a full day.
- **Short virtual follow-along** - 90-120 minutes, one module, attendees on trial or provisioned accounts (vendors' public labs of this shape run 90 minutes to about two hours, for example Snowflake's and Confluent's).
- **Challenge event** - teams solve open-ended tasks against a scoreboard (AWS GameDay, teams of up to 4). Suits customers with baseline skill; confuses early prospects.
- **Build-on-your-use-case** - attendees build against their own use case, sometimes their own data. The strongest POC on-ramp; triggers the customer's security review when their data or environment is involved.
- **Full day with executive session** - labs plus a roadmap or architecture readout for decision makers (MongoDB's full-day kit ends with a 75-minute executive session). Serves the sale more than the learning.

- Justify the compliance tie: the three tied formats run on vendor-held environments with synthetic data, so none triggers a customer review.
- Default: guided lab half-day, lecture blocks under 15 minutes, hands-on most of the time, a 20-minute closing readout with the decision maker (baseline). No vendor publishes a hands-on ratio; MongoDB's full-day kit gives two 90-minute workshop blocks out of about six hours.
- What this order starves: build-on-your-use-case, highest value for a technical win and highest effort. Promote it when the opportunity has a written evaluation plan and the champion has cleared the data question.
- Cap a workshop at one day of delivery: anything longer is paid training or professional services. A build-on-your-use-case split into sessions over an evaluation stays presales.

## Step 4 - Set the lab environment standard

Efficiency first: `vendor-provisioned disposable environment > attendee trial account > shared hosted environment > customer's own environment > install on attendee laptops`.

- compliance cost: `customer's own environment > attendee trial account > install on attendee laptops > shared hosted environment == vendor-provisioned disposable environment`

- The tie holds because both keep every credential and every resource on vendor infrastructure under vendor terms.
- **Vendor-provisioned disposable environment** - one environment per attendee, pre-built, least-privilege, auto-expiring. The dominant published pattern. Default.
- **Attendee trial account** - each attendee signs up beforehand. Cheap, but every sign-up is a failure point at minute zero and accepts terms personally; keep it for take-home continuation.
- **Shared hosted environment** - one cluster for the room; one attendee's mistake breaks everyone's lab.
- **Customer's own environment** - only for build-on-your-use-case, after the customer's security team agrees in writing.
- **Install on attendee laptops** - delete whenever laptops are corporate-managed or the network is unknown. One lab-platform webinar puts self-provisioning at an hour or two of workshop time.

Rules for every lab, whichever environment:

1. Find the slowest provisioning step and schedule from it: some cloud services need 48 hours before the event (AWS documents this for a security workshop).
2. Set every environment's time-to-live longer than the session, or attendees lose work mid-lab.
3. Run an automated test of every checkpoint (setup, check fails, solve, check passes) nightly or on every product release, and within 24 hours before each delivery (baseline).
4. Keep lab source in your own repository, versioned with the product, with one named maintainer per module.
5. Tear down every environment after the session and give attendees a take-home path in their own account with explicit cleanup steps.

Pool sizing, network checklist and security rules: [./references/lab-environment-runbook.md](./references/lab-environment-runbook.md).

## Step 5 - Certify who delivers

Staff each workshop with one instructor plus one helper per started block of 10 attendees, rounded up (baseline; MongoDB's field kit says "roughly 1 helper/10 attendees"; The Carpentries publish 1 per 8-10 learners plus two instructors). Add helpers for virtual attendees: one per breakout room.

Delivery options, efficiency first: `solutions engineer with helpers > DevRel or education team > certified partner`. SEs already own the account context; partners scale reach but need the full ladder and a quality check per delivery.

Certification ladder (this skill's construction; vendors publish entry gates, not shadow ladders, so label it as such):

1. Run every module of the lab alone, end to end, on a fresh environment.
2. Help at one delivery.
3. Co-deliver: lead one module while a certified instructor leads the rest.
4. Lead a full workshop with a certified instructor observing and scoring against the checklist.
5. Certified. Re-run step 1 on every major lab version.

AWS gates its partner-delivered Immersion Days on partner tier, at least one practitioner with an active AWS certification at Associate level or higher, executive sponsorship and a one-day onboarding event before the first customer delivery; borrow the gate for partners. Partners apply the same grant rule and next-step agreement as internal deliveries.

Rehearse every workshop: never walk in with an untested lab, and dry-run on the customer's network with at least one onsite attendee running the prerequisites live.

## Step 6 - Run the pre-workshop sequence

1. Logistics call with the champion 2-3 weeks out (baseline): attendee list with roles and each attendee's skill level and prior product exposure (pick modules and format from it), network and VPN rules, who can grant access, room, host of the virtual meeting.
2. Publish prerequisites in three parts: prior knowledge, machine and network state, accounts. Accounts fail worst at minute zero.
3. Confirm attendance through calendar acceptance; size environments from confirmed attendees plus two spares (baseline).
4. Dry run on the customer network (Step 5) and the automated checkpoint test (Step 4).
5. Brief the AE: their role in the room is the opening, the readout and the next-step conversation with the champion. An AE who sits at the back while the SE carries the day wastes the one meeting the workshop bought.

## Step 7 - Agree the next step, then follow up

Write the next-step agreement with the champion before the date is set:

- the success criterion the workshop must show (for example "three attendees reach checkpoint 4 on their own data");
- the step that follows when it is met (POC scope, evaluation plan, team rollout, architecture review), with a date and an owner on each side;
- what happens when it is not met.

After the workshop:

0. No next-step agreement exists: agree one with the champion before any other follow-up.
1. Send the champion, within one business day (baseline), the checkpoint results per module, the success criterion outcome and the agreed step with its date.
2. Give every attendee the take-home lab path and the help channel. Attendees get technical help, never a sales call or a generic nurture sequence: the AE talks to the champion and the decision maker.
3. Run the agreed step. When the criterion failed, fix the cause (wrong attendees, broken lab, wrong use case) before offering a second workshop.

Sequenced follow-up of contacts from a public or multi-account workshop goes to the event-follow-up sibling listed at the top.

## Step 8 - Measure per account, then per program

Measure on Kirkpatrick's four levels, per account. Evaluators mostly stop at levels 1-2: ATD's 2019 survey (779 practitioners) found 83% evaluate reaction and only 38% evaluate results.

| Level       | Signal                                                                             | Basis                          |
| ----------- | ---------------------------------------------------------------------------------- | ------------------------------ |
| 1 Reaction  | End-of-day rating and one open question                                            | Track the trend                |
| 2 Learning  | Checkpoint completion per module, from lab check scripts                           | Own baseline after one quarter |
| 3 Behaviour | Attendees active in their own trial or production account at 30 and 60 days        | Own baseline                   |
| 4 Results   | Agreed next step executed within 30 days; POC started; technical win; usage change | Next-step agreement            |

Program signals: grant rate, show rate against confirmed attendees, lab defect rate (sessions with a checkpoint failing for environment reasons), delivery hours per workshop, next-step execution rate.

Log every workshop against its opportunity or account on the day it is granted, with attendees linked and the grant decision recorded; no metric below survives without it.

Compare workshop accounts against matched opportunities without a workshop; capacity-deferred qualified requests add a few more. Workshop accounts are selected for momentum, so raw influenced pipeline overstates the effect; report it as "influenced", never as caused.

## Pass threshold

Review the program each quarter. The first gated quarter sets the baselines; apply the threshold from the second. Continue unchanged only if all four hold:

1. Next-step execution rate holds at or above the first quarter's rate, pooled over at least 10 workshops; with fewer, pool quarters before judging (baseline). Fix: tighten the grant rule.
2. No live session hits an environment-caused checkpoint failure; failures the dry run catches count as the test working. Fix: the test rule in Step 4, then the maintainer.
3. Every instructor in the quarter sits on the certification ladder. Fix: pause uncertified delivery.
4. Delivery hours fit the hours named in the interview. Fix: decline-with-alternative before cutting rehearsal.

## Failure modes

| Failure                    | What it looks like                                          | Fix                                                       |
| -------------------------- | ----------------------------------------------------------- | --------------------------------------------------------- |
| Goodwill workshop          | Granted to soothe a renewal; no champion, no next step      | Grant rule, decline-with-alternative                      |
| Feature tour               | Two hours of slides, one lab at the end                     | Backward design, lecture blocks under 15 minutes          |
| Lab dies at minute zero    | VPN blocks the trial cluster, sign-ups fail                 | Provisioned environments, dry run on the customer network |
| Free professional services | Third workshop for the same account, now on their migration | Route to paid training or services                        |
| Wrong room                 | Twenty practitioners, nobody who chooses the vendor         | Decision maker at the opening or readout                  |
| Sales theatre              | Attendees get cold calls the next day                       | Attendees get help; AE works the champion                 |
| Vendor-stat business case  | "Labs lift trials from 14% to 40%" in the deck              | Own baseline and matched comparison                       |

## References

- Account-level qualification signals and the developer-to-buyer handoff: samber/developer-relations-skills@developer-first-gtm
- Sample applications the labs build on: samber/developer-platform-skills@sample-app-strategy
- A sandbox or test mode attendees can safely break: samber/developer-platform-skills@api-test-mode-design
- DevRel-wide metric framework the scorecard reports into: samber/developer-relations-skills@devrel-metrics
- Decline-menu office-hours slot: samber/developer-relations-skills@developer-office-hours-program
- Exams and credentials for partner or customer certification: samber/developer-relations-skills@developer-certification-program
