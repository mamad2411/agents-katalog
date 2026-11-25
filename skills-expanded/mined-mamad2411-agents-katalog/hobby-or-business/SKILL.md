---
name: hobby-or-business
description: Separate project enthusiasm from business reality when a user wants to monetize an idea they've already decided to build. Use whenever a user asks how to make a product, app, project, or service profitable, OR asks the AI to invent a revenue model or "way to make money" from a thing they've already chosen. Trigger on phrases like "how do I make this profitable", "how can I monetize this", "give me a business model for", "how do I make money from my", "should I add subscriptions/ads", "how do I turn this into a business", and especially when the user wants the AI to do the demand-side thinking after already committing to building. The point is to catch the backwards move of choosing the product first and inventing the buyer later, and to surface whether the user actually wants a business or is building a hobby — both are fine, but the work has to match the goal. Do NOT use when the user already has paying customers and just needs help with pricing mechanics, or for tasks unrelated to monetizing something.
---

# Hobby or Business

Your job is to separate enthusiasm for a *project* from the reality of a *business*, and to stop the user from asking you to do the one thing you cannot do: invent demand by brainstorming. When someone asks "how do I make this profitable?" after already choosing what to build, they are usually trying to get the AI to do the heavy lifting on the demand side — to conjure a buyer for a thing that was chosen for other reasons. Profitability cannot be sprinkled on at the end. It starts with a buyer, and a buyer is a real person, not an output you can generate.

So when a user asks how to monetize an already-chosen idea, do not immediately list monetization tactics. First figure out what they're actually building and what they actually want.

## The real question: does the work match the goal?

The trap is not "having a hobby." A hobby pursued knowingly as a hobby is a complete success — most of the best software in the world started as someone building for themselves. The failure this skill catches is a **mismatch between goal and effort**:

- Someone doing hobby-grade validation (none) while privately hoping it replaces their salary.
- Someone agonizing over pricing tiers and CAC for a thing they're building for fun and would build anyway.

Both are the same error: an unexamined goal. So the first move is not to label the user's idea as "lesser" — it's to make the goal explicit and check whether the work fits it. "Hobby" is not a consolation prize. It's a legitimate, often smarter, answer. The dishonest version is doing one while pretending it's the other.

## When to push back

Push back when the user:

- asks you to invent a revenue model *after* the product was already chosen (the backwards move)
- assumes "add subscriptions" or "add ads" is the same as "make money"
- confuses **users with customers** (someone who uses it free is not someone who pays)
- confuses downloads / signups / waitlist with revenue
- skips the whole operating reality: acquisition, retention, pricing, support, competition
- wants consumers to pay for something they already get free or bundled
- is avoiding the one thing that would actually tell them — talking to a real buyer

## How to respond (keep it tight)

Short by default. Lead with the verdict in the first sentence, give the two or three points that matter most, and stop. Offer to go deeper rather than dumping everything. The user can pull more; don't push a wall of text at them. Scale up only if the stakes are genuinely high (they're about to quit a job, spend savings, or sign something).

Your response should cover, in your own words and in priority order:

1. **The verdict, up front.** Name what this currently is — a hobby, a personal tool, a portfolio piece, or a business — based on the evidence in front of you. Say it plainly in the first line.
2. **The missing buyer.** Identify the customer assumption that hasn't been made. Who, specifically, has this pain badly enough to pay?
3. **Why tactics are premature.** Briefly: monetization mechanics applied to an unvalidated buyer is decorating a house with no foundation.
4. **Users vs. customers, if it's biting them.** If the idea is consumer software competing with free defaults, name that directly — the gap between "people would use this" and "people would pay for this" is where most of these ideas die.
5. **One concrete validation step with real humans.** Not a research project — one narrow, doable step (see below).
6. **The honest close.** If nobody can name the pain and nobody already spends money on it, say so: it's a hobby right now, and that's fine — but don't let them call it a business until a buyer does.

If there's a critical buried point you're holding back for length (a regulatory issue, a fatal competitor, a safety angle), flag in one line that it exists and offer to expand. Don't silently drop it.

**Calibrate length to how loudly you were summoned.** A quiet auto-trigger (the user casually asked "how do I monetize my side project?" and your trigger phrases happened to match) gets three or four crisp sentences — the verdict on what this currently is, the missing buyer, and the next move. An explicit invocation (a `/reality-check` slash command, or "apply hobby-or-business to this") signals the user wants the full pass, so the long form with all six priority items is appropriate. Don't dump the consumer-vs-business essay on someone who just asked a casual question; don't give a one-liner when they asked for the works.

## Consumer vs. business customers

Surface this distinction when it's load-bearing, because it changes everything about whether the idea can pay:

- **Consumers** are expensive to acquire, quick to churn, and reluctant to pay — especially when a free or bundled default already does 80% of the job. Consumer software that charges money has to clear a high bar: frequent, obvious pain the free option doesn't solve.
- **Businesses** pay when something saves them time, makes them money, reduces risk, or removes a compliance/liability headache. The same idea aimed at a professional niche with a budget is often a business when the consumer version is a hobby. "Note app" is a hobby; "note app that keeps therapists' session records compliant" might be a business — because now there's a buyer with a budget and a reason.

## The validation step

Point the user at one narrow group and a behavioral question — not a survey, not "would you use this." Real demand shows up as money already moving or pain already costing something.

Pick one specific group (therapists, recruiters, lawyers, sales reps, nurses, PhD students, contractors — *one*, not "professionals") and find a handful of them. Ask:

- What does your current workflow for this cost you — in time, money, lost clients, risk, or embarrassment?
- What have you already tried, and what do you currently pay for, if anything?
- *Have you ever gone looking for something to pay for to fix this?*

The last question is the one that separates a business from a wish. If the answer across the group is "no, it's mildly annoying but I'd never pay" — that's your answer, and it's better to hear it now than after the build.

## Worked example

**User:** "I've decided to build a note-taking app. How can I make it profitable? Should I add subscriptions or AI features?"

**Weak response (avoid):** "Great question! A few monetization models work well here: freemium subscriptions at $5/mo, a one-time pro unlock, affiliate integrations, and AI features as a premium tier…" — This invents a revenue model for a buyer who doesn't exist yet. It's doing the user's demand-side thinking for them, which is exactly the thing that can't be brainstormed.

**Strong response:** Right now this is a hobby idea, not a business yet — and asking how to monetize it before you know who'd pay is backwards. Profitability doesn't get added with subscriptions; it starts with a buyer, and a consumer note-taking app is fighting free, entrenched defaults (Apple Notes, Keep, Notion, Obsidian) for users who rarely pay. The missing piece isn't a pricing tier, it's a person: who has a note-taking problem painful enough that it costs them money, time, or professional risk? That's usually a *professional* niche, not "everyone" — a therapist who needs compliant session notes is a customer; a casual note-taker is not. Before touching pricing, pick one narrow group and ask a handful of them what their current workflow costs them and whether they've ever paid to fix it. If nobody can name the pain and nobody already spends on it, it's a hobby — which is genuinely fine, just don't build a business plan on it. Want me to help you pick a niche to test, or sketch the questions to ask them?

## What this skill is not

It is not a tool for making people feel bad about hobbies, and it is not reflexively anti-monetization. If the user already has paying customers or clear evidence of demand and just needs help with pricing mechanics, drop the lecture and help them — that's the off-switch. The goal is calibration: match the work to the goal, and refuse only the one specific thing that can't be faked — generating real demand out of a brainstorm.
