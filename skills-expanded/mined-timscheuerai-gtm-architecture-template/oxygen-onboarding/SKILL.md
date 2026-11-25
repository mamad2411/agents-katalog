---
name: oxygen-onboarding
description: Guide a first OXYGEN session from company context to first leads, a reviewed draft Sequence, a connected sender and a bounded launch. Use for get me started or the first campaign; for a diagnosis or plan, use oxygen-gtm-consultant.
---

# Get to a first campaign

Read [the runtime contract](../../../docs/runtime-contract.md). Work one step at a time in this order: **know the company, show real matches, first leads, first sequence, connect the account, launch**. `oxygen activation checklist --json` shows which steps are done.

## Speed rules

- Resolve context first: `oxygen knowledge resolve --purpose onboarding --json`. Read the company research and the existing persona and filter drafts before asking anything.
- Say in one sentence what you are checking, then check. Ask one question only when it changes the next action, and offer concrete choices.
- In a coding agent, also read the folder you started in (this kit's `company/` and `context/`). Never upload a file into OXYGEN without asking.
- End every answer with the next step and what it costs or needs approved.

## The steps

1. **Know the company.** Say in two or three lines what it sells, to whom and why it wins. Draft the ICP in one line as a hypothesis. A claim without a number or a named customer stays unproven.
2. **Show real matches.** Run the free company preview on that ICP (`oxygen companies search filters --json` lists accepted values) and name the five best matches with the reason each fits.
3. **First leads.** Work the warm ladder first when it exists: customers and open deals, the user's own network and engagers, people showing intent. Otherwise use the free company and people previews, a CSV or the CRM. Tighten once if the first page does not look like the buyer. Save about ten ranked leads with why each fits; drafting first messages needs no approval.
4. **First sequence.** Create a draft for the chosen channel, grounded in the offer and in why these leads fit. A new LinkedIn account starts with a few invites a day; a blast is never the plan.
5. **Connect the account.** A sending account has its own monthly cost, stated before connecting.
6. **Launch.** Preview the exact audience, sender, rendered copy, schedule and send ceiling, then start only under the user's approval. Launch, first confirmed send and daily readiness are separate outcomes.

Save the confirmed offer, ICP, goal and next step in Knowledge so the next session resumes from them. For "why is pipeline flat" or "plan our GTM", hand over to [oxygen-gtm-consultant](../oxygen-gtm-consultant/SKILL.md).
