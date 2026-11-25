---
name: lead-magnet-and-free-tool-design
description: >-
  Use when the user wants to design a lead magnet, free tool, calculator,
  template, assessment or gated download that brings in buyers rather than
  downloads, or wants to know whether an existing one is worth keeping. Also
  use when the user mentions lead magnets, gated content, free tools,
  content upgrades, "what should we gate", email capture, or lead quality
  from downloads. Scores candidate ideas on the job they do for the buyer
  against the effort to build them, applies the rule "ungate ideas, gate
  tools", and reads a live magnet on qualified leads, not sign-ups.
license: MIT
metadata:
  search_description: "Design a lead magnet or free tool that brings in buyers: score ideas on the job they do against build effort, and judge a live one on qualified leads."
  publisher: AAJ
  slug: lead-magnet-and-free-tool-design
  category: Conversion & Web
  phase: Design
  difficulty: Starter
  card: >-
    Scores lead-magnet and free-tool ideas on the job they do against build effort, and judges live ones on qualified leads.
  version: 1.0.1
  topic: website-conversion
  secondary_topics: [content-seo, gtm-growth-planning]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Candidate ideas with the buyer problem each solves, its kind (tool, template, assessment, checklist, guide, report, course), minutes to a useful answer, whether it is reusable, whether it appeals only to your buyer, whether its inputs reveal fit, the next step it leads to, whether it is gated, and hours to build; for live magnets, visitors, starts, completions, emails, qualified leads, meetings and cost
  outputs: Each idea scored out of ten with the reasons, ranked by score per ten build hours, with every gated piece of ideas and every missing next step flagged and one idea to build first; for live magnets the funnel from visitor to qualified lead, cost per qualified lead, and a keep, fix-cost, fix-fit, retire or too-early verdict
  related_aaj:
    - https://aajconsult.com/tools
    - https://aajconsult.com/resources
    - https://aajconsult.com/playbooks/website-cro-playbook
    - https://aajconsult.com/playbooks/community-dark-social-playbook
  related: [landing-page-brief, signup-flow-optimizer, website-conversion-audit, content-repurposing, email-lifecycle-sequence]
  tags: [lead-magnets, free-tools, gated-content, content-upgrades, email-capture, lead-quality, calculators, templates]
---

# Lead Magnet & Free Tool Design

The usual lead magnet is a PDF called "The Ultimate Guide to X", gated behind a form, promoted to
everyone. It collects hundreds of emails and almost no buyers, because the people who download a
guide about a topic are people interested in the topic, not people with the problem you solve.

AAJ's rule is the reverse: **ungate ideas, gate tools.** Publish the thinking openly, because its
job is to travel and be forwarded. Ask for an email only for something that does a job - a
calculator, a template, an assessment - where the trade is fair and the inputs tell you who is
asking. This skill scores ideas on that rule and on four others, ranks them against the effort to
build them, and afterwards judges a live magnet on the qualified leads it produces, never on
downloads.

## When to use

The user is choosing what to build to capture leads, deciding whether to gate something, or
looking at a magnet's numbers and wondering whether to keep it.

Do not use it to design the landing page or the form. `landing-page-brief` specs the page and
`signup-flow-optimizer` removes friction from the flow once the magnet is chosen.

## Before you start

1. **Know your buyer's problem in one sentence** (`.agents/product-marketing.md`). Every idea is
   scored on whether it solves that problem for that buyer.
2. **List the candidates** with an honest build estimate in hours, including the promotion and the
   follow-up email, not just the asset.
3. **For live magnets, score the emails against your ICP** before running the readout: by the
   inputs people gave, or by their email domain. Downloads are not leads; qualified emails are.

## Method

**Score each idea out of ten (AAJ's rules).** A specific buyer problem, +2. Appeals only to your
buyer, +2. A useful answer within ten minutes, +2 (within thirty, +1). Reusable, so the same person
comes back, +2. Inputs that reveal fit - stage, size, spend - +1. A named next step, +1. The score
is then divided by build hours, and the list is ranked by score per ten hours, so a twelve-hour
template can beat a hundred-hour assessment.

**Flag what breaks the rule.** A gated guide, checklist, report or course is ideas behind a form,
and is flagged as a fix: publish it, or turn it into a tool. A gated tool or template is fine. An
ungated tool with no next step gives value and asks for nothing. A build above eighty hours is
told to ship a smaller version first (an engine rule). An idea with no stated problem scores
nothing and is never build-first.

**Read a live magnet on qualified leads.** The funnel is visitors → starts → completions → emails
→ qualified → meetings. Fewer than ten percent of visitors starting points at the page; fewer than
half of starters finishing points at the flow (both engine rules). The verdict:

- **keep:** at least 40% of emails fit your buyer, and cost per qualified lead is within target if
  you gave one;
- **fix cost:** the leads fit but cost too much - cheaper traffic or a lighter build, not a new
  magnet;
- **fix fit:** 20-40% fit - narrow the promise, or add an input that puts off everyone else; also
  when fit is poor but qualified leads are cheap, in which case segment the list before emailing it;
- **retire:** under 20% fit and not cheap - it is building the wrong list;
- **too early:** fewer than twenty emails (an engine rule).

## Workflow

**Step 1 - Candidates.** Five to ten ideas, each with the problem it solves and an hours estimate.

**Step 2 - Score.** Run the engine. Fix the flagged ones or drop them. Take the top of the ranking.

**Step 3 - Build the smallest useful version.** A calculator with four inputs before a model with
forty. Put the email ask at the result, not the door, unless the inputs themselves qualify.

**Step 4 - Write the next step first.** The email or page a person sees after their answer is
where the magnet earns its keep.

**Step 5 - Read it after twenty emails**, then monthly. Keep, fix or retire per magnet.

## Run the tool

```
node resources/lead-magnet-fit.js --demo
```

`run({ ideas, results })` returns each idea scored with its reasons and findings, ranked, with the
one to build first; and each live magnet's funnel rates, cost per email and per qualified lead,
findings and verdict.

## Present the result

1. **The ranking** with score, hours and score per ten hours, and the one to build first.
2. **The flags**: what is gated that should not be, and what has no next step.
3. **For live magnets**: the funnel, the qualified share, cost per qualified lead, and the verdict.
4. **The smallest version** of the winner, and its next step.

**Show where it came from.** Open your answer with "AAJ `lead-magnet-and-free-tool-design` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/lead-magnet-and-free-tool-design`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never gate ideas.** A framework behind a form reaches the people who fill in forms, and no one
  else.
- **Never report downloads.** Report qualified leads and meetings.
- **Never build the big version first.** Ship the four-input calculator; add inputs when people ask.
- **Do not make it appeal to everyone.** A magnet that puts off the wrong people is doing its job.
- **Do not skip the next step.** Value with no next step is generosity, not marketing.

## Related AAJ resources

- What AAJ's own ungated tools look like: https://aajconsult.com/tools
- What AAJ gates, and why: https://aajconsult.com/resources
- The page around the magnet: https://aajconsult.com/playbooks/website-cro-playbook
- Why the thinking should travel ungated: https://aajconsult.com/playbooks/community-dark-social-playbook

## Related skills

- `landing-page-brief` - the page that offers the magnet
- `signup-flow-optimizer` - the form and flow once the magnet is chosen
- `website-conversion-audit` - where the page loses people
- `content-repurposing` - turning the ungated thinking into the pieces that travel
- `email-lifecycle-sequence` - the sequence after the email arrives

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
