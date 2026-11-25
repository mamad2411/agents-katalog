---
name: referral-program-design
description: >-
  Use when the user wants to design, launch, or fix a customer referral or
  advocacy program: who to ask, when to ask, what reward to offer (one-sided or
  two-sided), and whether the economics beat other channels. Also use when the
  user mentions referral program, refer-a-friend, referral rewards, advocacy
  program, customer introductions, double-sided incentive, viral coefficient from
  referrals, or "how do we get customers to refer us". Produces a referral
  program design with referral CAC, break-even reward, payback, k-factor, and
  pointers to the disclosure and healthcare rules to check.
license: MIT
metadata:
  search_description: "Design a customer referral program: who to ask, when, and what reward, with referral CAC, break-even reward, payback, k-factor and the rules to check."
  publisher: AAJ
  slug: referral-program-design
  category: Growth, Retention & RevOps
  phase: Design
  difficulty: Intermediate
  card: >-
    Designs who to ask and what to reward, then prices referral against the CAC
    it replaces.
  version: 1.0.1
  sprint: unit-economics-retention
  topic: retention-expansion
  secondary_topics: [gtm-growth-planning, analytics-budget]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Active customer count, the signals that mark an engaged customer (NPS, usage, renewals), your own or assumed ask and conversion rates, reward cost per side, LTV, and the CAC of the channel referral would replace
  outputs: A referral program design (who, when, reward, mechanics, tracking) with referral CAC, break-even reward, payback, LTV:CAC, k-factor, findings, and compliance pointers to check with counsel
  related_aaj:
    - https://aajconsult.com/tools/referral-program-calculator
    - https://aajconsult.com/blog/referral-programs-for-startups
    - https://aajconsult.com/tools/unit-economics-calculator
    - https://aajconsult.com/playbooks/customer-onboarding-retention-playbook
    - https://aajconsult.com/playbooks/partner-co-marketing-playbook
  related: [aaj-marketing-loops, unit-economics, lifecycle-and-retention, case-study-and-proof, customer-survey-design]
  tags: [referral, advocacy, refer-a-friend, rewards, k-factor, word-of-mouth, cac, retention]
---

# Referral Program Design

Design a referral program that asks the right customers at the right moment, rewards them in a way that does not buy the wrong customers, and costs less per customer than the channel it replaces.

## When to use

The user wants to start a referral or advocacy program, size a reward, decide between one- and two-sided incentives, or check whether an existing program pays for itself. For the general loop math across referral, content and paid loops, use `aaj-marketing-loops`; this skill is the referral program itself.

## Before you start

1. **Read the brand/product context first.** Pull ICP, pricing, buyer, and whether customers are healthcare providers from `.agents/product-marketing.md` (or `.agents/aaj-brand.md`). If none exists, ask.
2. **Gather inputs:** active customers; the signals that mark an engaged customer (NPS promoters, usage depth, renewals, a milestone reached); the share of customers who meet them; LTV on gross margin; the fully loaded CAC of the channel referred customers would otherwise come from; gross margin per customer per month.
3. **Separate data from guesses.** Ask-to-referrer and referral-to-customer rates are usually unknown before launch. Mark them as assumptions and treat the first period as the test that replaces them.
4. **Confirm the objective:** more customers at a lower CAC, references for sales, or both. In B2B, references and introductions often matter more than a cash reward.

## Method

Diagnose whether referral fits: customers can show a result they are proud of, they know people with the same problem, and those people trust them. If any of the three is missing, fix the product or the segment before building a program.

Design around three choices. **Who:** customers already getting value, identified from your own signals (promoters, deep usage, renewals), asked at a success moment rather than all at once. **What:** a modest reward, usually two-sided and in product credit, paid when the friend becomes a customer; in B2B, a reference list and a personal thank-you are often the better design. **How it pays:** referral CAC must sit below the CAC of the channel it replaces, and the reward has a ceiling you can compute.

Execute with tracking from day one (who referred whom, in the CRM), and judge the program on five numbers: share of new customers from referral, referrals per active customer, retention and LTV of referred customers versus others, cost per referred customer, and second-generation referrals.

## Workflow

1. **Check fit** against the three conditions above. Stop and say so if referral does not fit.
2. **Define the referrer pool** from the customer's own signals, and the success moment that triggers the ask (a milestone, a reported result, a renewal, a positive support conversation).
3. **Choose the reward design** (two-sided credit, account usage, status or access, or no reward and a great ask), and when it is paid. Default to paying when the friend becomes a customer.
4. **Run the engine** with the founder's numbers, marking assumptions. Read referral CAC against the CAC it replaces, and the break-even reward.
5. **Resize the reward** if it exceeds the break-even, or if the fixed cost needs a wider ask to spread over.
6. **Switch on the compliance flags** that apply (public posts, reviews, healthcare providers, patient information) and pass the pointers to the founder to check with counsel.
7. **Specify tracking and the review cadence**: the five numbers, every period, with assumptions replaced by measured rates.

## The math

```
asked          = customers x shareAsked
referrers      = asked x askedToReferrer
referrals      = referrers x referralsPerReferrer
newCustomers   = referrals x referralToCustomer

rewardCost     = referrer rewards (per customer, or per referral) + friend rewards (per customer)
referralCAC    = (rewardCost + fixedCost) / newCustomers
breakEven      = otherCAC - fixedCost / newCustomers      (combined reward per referred customer)
payback        = referralCAC / monthly gross margin per customer
k (program)    = newCustomers / customers                 (per period)
amplification  = 1 / (1 - k)  if referred customers refer at the same rate and k < 1
```

A reward per referral (not per customer) costs `reward / referralToCustomer` per referred customer. That is the most common way a program ends up paying more than the channel it replaces.

## Run the tool

```bash
node resources/referral-economics.js --demo
node resources/referral-economics.js '<json-config>'
node resources/referral-economics.js --help
```

The engine returns the funnel, referral CAC split into rewards and fixed cost, break-even reward, the most the referrer reward can be at the current friend reward, payback, LTV:CAC, savings against the other channel, and k. It flags: rewards above the CAC they replace, referral CAC above the other channel or above LTV, rewards paid per referral, one-sided rewards, rewards larger than a month of customer spend, asking every customer, a missing fixed cost, and assumed inputs. Flags in `flags` switch on compliance pointers. Every rate is the founder's; the engine holds no benchmarks.

## Reference

- AAJ's post *Referral Programs for Startups* (aajconsult.com/blog/referral-programs-for-startups) carries the research and the rules this skill points to, with primary links:
  - Referred customers worth at least 16% more at a German bank: Schmitt, Skiera and Van den Bulte (2011), doi:10.1509/jm.75.1.46.
  - Larger rewards brought more referred customers but less profitable ones: Wolters, Schulze and Gedenk (2020), doi:10.1287/mksc.2020.1242.
  - For innovative products, rewarding both sides softened the drop in referrals a visible referrer reward caused: Dose and others (2019), doi:10.1007/s11747-019-00635-z.
  - Who to recruit as referrers: Van den Bulte and others (2018), doi:10.1509/jmr.14.0653. Business reference value: Kumar, Petersen and Leone (2013), doi:10.1509/jm.11.0424.
- Rules to check (pointers, not verdicts): FTC Endorsement Guides, 16 CFR Part 255; FTC consumer reviews rule, 16 CFR Part 465; Google Maps content policy on incentivized reviews; HHS-OIG on the Anti-Kickback Statute; HIPAA marketing authorization, 45 CFR 164.501 and 164.508(a)(3). Links are in the engine's `POINTERS` and in the post.
- The research is mostly consumer banking, telecom and apps. AAJ's post found no peer-reviewed study of cash-incentive referral programs specifically in B2B: say so when advising a B2B company.

## Present the result

- **Fit:** the three conditions, each met or not.
- **Program design:** referrer pool and the signal that defines it, the success-moment trigger, the reward (sides, form, size, when paid), the ask message, and how a referral counts.
- **Economics:** the engine's funnel, referral CAC against the CAC it replaces, break-even reward, payback, k; with assumptions labelled.
- **Rules to check:** the pointers that apply, stated as things to check with counsel.
- **Tracking:** the five numbers and when they are reviewed.

**Show where it came from.** Open your answer with "AAJ `referral-program-design` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/referral-program-design`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **No invented rates.** If the founder has no ask or conversion rates, run the engine with labelled assumptions and say the output is a scenario.
- **Do not assume referred customers are worth more.** The 16% finding is one bank. Use a separate `referredLtv` only when the founder has measured it.
- **Pay on the outcome.** Rewards per referral buy names, not customers.
- **Bigger is not better.** Larger rewards can attract people who come for the reward; start modest and test up.
- **Never tie a reward to a review.** Keep referral rewards and review requests separate.
- **Healthcare providers are different.** Anything of value to a provider for steering business can be a kickback risk; the default design is no reward, and any incentive goes to a healthcare lawyer first. Never give a legal verdict; point to the rule and to counsel.
- **Track who referred whom from the first referral,** or none of the five numbers can be computed later.

## Related AAJ resources

- Referral Programs for Startups (AAJ post): https://aajconsult.com/blog/referral-programs-for-startups
- Unit Economics Calculator: https://aajconsult.com/tools/unit-economics-calculator
- Customer Onboarding and Retention Playbook: https://aajconsult.com/playbooks/customer-onboarding-retention-playbook
- Partner Co-Marketing Playbook (partner referrals): https://aajconsult.com/playbooks/partner-co-marketing-playbook

## Related skills

`aaj-marketing-loops` · `unit-economics` · `lifecycle-and-retention` · `case-study-and-proof` · `customer-survey-design` · `partnerships-and-co-marketing`

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
