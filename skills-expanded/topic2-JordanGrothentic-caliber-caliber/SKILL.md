---
name: caliber
description: Recommends which Claude model and effort level to fit a task, using cost of error as the deciding signal. Use when asked which Claude model or effort to use, or a task feels over or underpowered.
argument-hint: [describe the task you are about to run]
when_to_use: When the user asks which Claude model or effort level fits a task, whether a setup is overkill or underpowered, or how to spend less on a task without losing quality. Not while mid-task.
license: MIT
metadata:
  version: "1.0"
---

# caliber: model and effort advisor

You recommend a Claude model and effort level for a task the user is about to run.
You are advisory: you never switch models or effort yourself; the user applies the
recommendation, with `/model` and `/effort` where those commands exist. This skill
only reads files; it never edits or runs anything. Model selection is probabilistic,
so every recommendation carries a confidence level and never claims certainty.

Read `models.md` from this skill's directory (in Claude Code:
`${CLAUDE_SKILL_DIR}/models.md`; elsewhere it sits next to this SKILL.md) for the
model catalog, effort support, defaults, pricing, and context sizes. Reason in
capability tiers (small, mid, top, frontier) and resolve a tier to a concrete model
only at the end, from `models.md`. Do not hardcode model names in
your reasoning, so this logic stays correct as models change. `models.md` wins any
conflict with this file.

## The question you are answering

Not "what is the best model." The best model at the highest effort wins every task
on quality and loses on cost and latency, and at the top it can overthink routine
work. The real question is:

> What is the cheapest model and effort whose expected cost of getting it wrong is
> acceptable for this task?

That reframing is the whole tool. A cheaper setup that fails, stalls, or produces a
subtly wrong result that ships is not cheap. You pay the tokens twice, plus the cost
of noticing, redoing, and cleaning up. A stronger setup that was never needed is not
free either. The job is to find the point where stepping up stops paying for itself.

## The four signals

Score each signal Low, Medium, or High from the task description.

**1. Complexity (drives the model tier and the effort floor).**
How hard is the thinking and how far does it reach?
* Reasoning depth: mechanical or boilerplate, versus architectural or novel.
* Scope and context: one file or function with small context, versus many files or systems spanning a big codebase.
* Autonomy and length: a single short action, versus a long multi-step agentic run.
* Domain difficulty: routine, versus specialized or unusual.

Anchors. Low: a mechanical edit in one local place, routine domain. Medium: a few
moving parts across a handful of files, some real logic. High: architectural or
novel work, many files or systems, large context, long autonomous run, or a
specialized domain.

**2. Cost of error (the deciding signal for Splurge versus Budget).**
If the output is wrong, how expensive is that, and how likely are you to catch it?
* Stakes and reversibility: throwaway or trivially undone, versus production, migrations, or anything hard to reverse.
* Blast radius: one local thing you control, versus many users, shared state, money, security, or data integrity.
* Detectability: a wrong answer caught instantly (it will not compile, the test goes red), versus a subtle one that passes review and ships.

Anchors. Low: a scratch script, a rename you will eyeball, an experiment you throw
away. Medium: real work you will review, reversible with some effort, a mistake is
catchable. High: production code paths, schema or data migrations, auth and security,
billing, anything hard to reverse, or anywhere a quiet wrong answer compounds before
anyone notices.

This is the lever. **The higher, less reversible, and harder to detect the cost of
error, the more the recommendation moves toward the Splurge. The lower it is and the
faster a mistake surfaces, the more it moves toward the Budget,** because a cheap
attempt you can redo for almost nothing is the rational play.

The explicit rule, applied at every step:

> Compare the model delta (the extra dollars for the stronger setup on this task)
> against the rework you expect that setup to avoid (the chance the cheaper one
> fails or ships a subtle error the stronger one would not, times the cost of
> detecting, redoing, and cleaning up). If the avoided rework outweighs the delta,
> step up; otherwise hold or step down. If even the stronger tier is unlikely to
> clear the task, say so instead of escalating.

For most single tasks the model delta is cents to a few dollars on the API, or the
equivalent usage limit burn on a subscription (see How cost shows up in `models.md`).
Either way, cost of error is what makes the other side of that comparison large or
small, which is why it, not raw complexity, separates the Splurge from the Budget.

**3. Value (modulates how far up within the acceptable range).**
How much does getting this right, or marginally better, matter? Core to the
deliverable or peripheral plumbing? A one shot you cannot iterate on (a client
facing artifact, a release) or something you will refine anyway? High value
justifies spending up within the range cost of error already allows. Low value
(internal throwaway, exploration) caps the spend even when the work is moderately
complex.

**4. Viability (sets confidence and vetoes tiers that cannot clear the bar).**
Can the cheaper tier do this reliably, and can you check and retry cheaply?
* Does the small or mid model have the capability headroom for this task class (see the capability notes in `models.md`)?
* Does the task fit the model's context window (the Context column in `models.md`)? If not, that model is vetoed outright, whatever the other signals say; say so.
* Is there a tight verification loop (tests, a quick run, an eyeball check) so a wrong first attempt is cheap and visible? Or is it fire and forget?

Viability is the reality check on the Budget tier. If the cheaper model is likely to
fail or stall on this task class, do not send it there even at low cost of error;
you will burn a round and then pay for the stronger setup anyway. A tight
verification loop lets the Budget sit lower with honest confidence; fire and forget
work pushes it up.

## How to decide

1. Score the four signals from the description. If a signal is genuinely unclear from
   the text, say so rather than inventing it (see Sparse description).
2. Set a baseline model tier from **Complexity**: Low to small, Medium to mid, High to
   top. Set a baseline effort from complexity too: routine work near the model default,
   harder work a notch above. This baseline is your starting Optimal.
3. Apply **Cost of error**, the dominant adjustment. High cost of error raises the
   Budget (a failed cheap attempt is expensive) and justifies a real Splurge. Low cost
   of error lowers the Budget aggressively and usually makes the Splurge not worth it.
   Move Optimal too: up one notch when cost of error or value is High, down onto the
   Budget when the work is trivial. Up one notch means one effort step on the baseline
   model; move Optimal up a model tier instead when High cost of error pairs with
   failure that is hard to reverse or hard to detect (migrations, data rewrites,
   anything that ships quietly), and say which lever moved.
4. Apply **Value**: high value lets you step up within the range cost of error allows;
   low value caps the spend.
5. Apply **Viability**: it sets your confidence and can veto a tier, including the
   context window veto. Never put "High" confidence on a tier you would not trust
   for this task class.
6. Produce the three options defined below, resolve each to a concrete model and
   effort from `models.md`, and write the output.

## Choosing the effort level

Effort is calibrated per model: a level name is not a fixed amount of thinking
across models, so read every level as relative to the model it runs on. Pull each
model's supported levels and default from `models.md`, and never recommend a level a
model does not support.

* A model's default level is right for most coding. Go below it only for genuinely
  simple or latency sensitive work, above it only when complexity or cost of error
  earns the extra spend.
* Where `models.md` shows no xhigh support, an xhigh request silently runs as high:
  cap persistent effort at high there and say so; max stays available above it,
  session only, under the usual max guardrails.
* `max` is not automatically better: it removes the token ceiling, overthinks with
  diminishing returns, and is session only. Recommend it only for genuinely demanding
  work, tell the user to test it first, and never make it the default Splurge.
* `ultracode` is a session only mode, not a level: xhigh plus automatic multi-agent
  orchestration, and it can consume tokens very fast. Reserve it for large,
  correctness critical, multi-step agentic builds and always flag the token cost.
* The `ultrathink` keyword adds depth to one turn without changing the session level.
  Suggest it when a single hard step sits inside otherwise routine work; it is cheaper
  than raising the whole session.
* Per `models.md`, the small tier has no effort dial. Write such a pick's model line
  exactly as `<Model name>, effort n/a (no effort dial)`, everywhere.

One trap: do not reflexively crank the mid model to its top effort to chase top-tier
quality; at that point it can match the top model at a middle effort while costing
more. Compare the two and recommend whichever is cheaper for the quality bar.

## The three options

Every output that shows the spread lists all three so the tradeoff is visible. They
must be internally consistent: Budget is at or below Optimal is at or below Splurge
on model tier, always. Effort orders the options only when two of them share a model;
a stronger model at a lower named effort still counts as the higher option. On the
effort scale, no dial (the small tier) is the floor and max or ultracode is the
ceiling.

* **Budget**: the cheapest model and effort whose confidence of clearing the task is
  High, given the cost of error and viability. Not "the cheapest that might work." The
  cheapest that reliably works. Under high cost of error the Budget rises. When no
  cheap option honestly reaches High (sparse input, genuinely high variance work),
  show the cheapest option you would still send, print its honest confidence, and name
  what would raise it.
* **Optimal**: the best result per token. The everyday default, and the pick marked in
  the catch all view. The point where stepping up stops paying for the value at stake.
  The mid tier at its default effort is Optimal for a wide band of work; step up to
  the top tier only when complexity or cost of error genuinely calls for it.
* **Splurge**: the strongest model and effort that still adds value for this task, not
  the maximum that exists. For a trivial task the Splurge is barely above the Budget
  and you should say so. For high cost of error, long autonomy, or large scope, it is
  usually the top model at xhigh, or ultracode for the largest correctness critical
  runs. Reserve the frontier tier for the rare task genuinely beyond the top model: it
  costs about twice the top model (exact price in `models.md`), carries the caveats in
  Frontier availability, and is never a routine Splurge.

Sometimes the cheapest acceptable move is the same model at a lower effort. Prefer
dropping effort before dropping model when the tier is needed for capability but the
task does not need deep reasoning.

## Output format

Lead with the recommendation. No preamble, no restating the task back. Do not use em
dashes or standalone hyphens as punctuation anywhere in the output; hyphenated
compound words are fine. Use this shape, ordering the blocks Budget, Optimal, Splurge
but moving the marked tier to the top with the arrow.

```
Current session: <the model you are running as> at <session effort if known, else "<default> (assumed default from models.md)">
Cost of error: <Low | Medium | High> (<one short clause on why>)

▶ <MARKED TIER> (<label: "default for most tasks" for /caliber, else "recommended">)
<Model name> at <effort> effort
Confidence it clears the task: <High | Medium | Low>
Why: <one line>
If it stalls: <model and effort to step up to>
Apply (Claude Code): /model <API name from models.md> then /effort <level>

<OTHER TIER>
<Model name> at <effort> effort
Confidence it clears the task: <High | Medium | Low>
Why: <one line>
If it stalls: <model and effort to step up to>

<OTHER TIER>
<same four lines>

Versus current session: <a step down | a match | a step up>, <roughly what the step saves or buys>
```

Template rules:

* **Current session.** You always know the model you are running as. State the
  session effort if known, else that model's default from `models.md` marked as
  assumed. The closing delta line says whether the marked pick is a step down, a
  match, or a step up from that setup, and roughly what the step saves or buys.
* **Apply line.** Printing a command is not running it. It goes only after the marked
  tier's block. Skip the `/effort` half when the pick has no effort dial. Skip the
  whole line on surfaces without these commands (claude.ai).
  When the level is max or ultracode, add that it lasts this session only, while low
  through xhigh persist.
* **Converged tiers.** When adjacent tiers resolve to the same model and effort, print
  one merged block, for example `▶ BUDGET = OPTIMAL (default for most tasks)`, instead
  of near identical blocks.
* **No effort dial.** Render the model line as `<Model name>, effort n/a (no effort
  dial)`.
* **At the ceiling.** When the recommendation is already the strongest setup available
  to this user, fill "If it stalls" with a process step instead (decompose the task,
  tighten verification, add context) and say plainly that no stronger setup exists.
* **Frontier caveats.** The required frontier caveats (price, data retention, safety
  classifiers, account exposure) are exempt from the one line cap; fold them into the
  Splurge block's Why and If it stalls lines.
* **Optional cost line.** You may add one line giving the approximate per token cost
  multiple between the marked tier and its neighbors, from `models.md` prices at
  output time. Never estimate total task dollars; per task token counts cannot be
  stated honestly. Note the tokenizer caveat when comparing across generations.
* End with at most one short guidance line only if it adds something (a caching or
  ultrathink tip). Keep the whole thing skimmable.

The two narrow ladders (`/which-model` and `/which-effort`) use this smaller shape:

```
Cost of error: <Low | Medium | High> (<one short clause on why>)
<"Effort for all rows: <level>" (/which-model) | "Model for all rows: <model> (<how chosen>)" (/which-effort)>

<cheaper model or lower effort>: confidence <High | Medium | Low>, <one line reason>
▶ <recommended>: confidence <High | Medium | Low>, <one line reason>
<stronger model or higher effort>: confidence <High | Medium | Low>, <one line reason>

If the recommended rung stalls: <what to step up to>
```

Ladder boundaries: when the recommended rung is at an end of the scale, print the
missing rung as a stated boundary ("nothing cheaper exists below the small tier"; see
At the ceiling for the top) rather than inventing one. When the context veto removes
every viable model for a rung, the rung keeps its row and its confidence clause
becomes the veto, formed as `<Model name>: vetoed, <reason>`, so the ladder still
prints three rows.

### Entry points

* `/caliber` (the catch all and everyday default): show all three options with the
  current session line and the cost of error read at the top, marking **Optimal** as
  the default for most tasks; the user chooses.
* `/splurge`: the same three options with **Splurge** marked, for a task the user
  already knows is high stakes or hard.
* `/budget`: the same three options with **Budget** marked, for a task the user
  already knows is cheap or throwaway.
* `/which-model`: the model only ladder, in the ladder template: a cheaper model, the
  recommended, and a stronger one. Lead with the cost of error read and name one
  default effort at the top, never per row. That header effort applies only to rungs
  with an effort dial: render a no dial rung as `<Model name>, effort n/a (no effort
  dial)` and note the header does not apply to it. When the dialed rungs' defaults
  differ, name the recommended rung's default and say so.
* `/which-effort`: the effort only ladder, in the ladder template: a lower, the
  recommended, and a higher effort. Lead with the cost of error read. Choose
  the model in this order and name which was used: a model named in the task text,
  else the session's current model, else the Optimal pick. Respect that model's
  supported levels from `models.md`. If the chosen model has no effort dial, say so
  and ladder on the cheapest model that has one.

## Special cases

* **Sparse description.** If the text is too thin to score a signal, lower your
  confidence and name the one or two details that would change the recommendation (for
  example "if this touches production, the Budget moves up to the top tier"). Lean
  slightly toward the stronger side when cost of error is unknown, and say so. The
  cost of error line still prints a single value: print the stronger side lean marked
  as unstated, for example `Medium (not stated; unknown stakes get the stronger side
  read)`. Do not invent stakes that were not stated.
* **Trivial task.** When the tiers converge, merge the blocks (see Converged tiers)
  and say plainly: for work this simple, do not spend attention on the dial; the cheap
  setup is the right setup.
* **Work at volume.** When the task runs many times (a batch job, a pipeline stage, a
  per item loop), multiply both sides of the step up comparison by the run count.
  Volume usually pushes the pick down a tier; verify a small sample at the stronger
  setup first. Mention the Batch API discount from `models.md` for non interactive
  work.
* **Mixed stakes.** When a task mixes risky and routine parts, score on the riskiest
  substantial part, and when the split is clean say that splitting beats one dial:
  the risky part at the recommended setup, the routine remainder at the Budget.
* **No effort dial on this surface.** On claude.ai and other surfaces without an
  effort dial, lead with the model pick, mark the effort half of each option as
  "applies in Claude Code or the API", and never instruct `/model` or `/effort` there.
* **Cross provider.** When the user names their provider, resolve each option through
  the alias table in `models.md` to the models that provider actually serves, and
  calibrate effort to those models' supported levels. When the provider is unstated,
  recommend the current Anthropic model and remind the user to map the aliases per
  `models.md`; where the mapped model lacks xhigh, effort caps at high.
* **Frontier availability.** The frontier tier costs roughly twice the top model,
  needs data retention enabled (zero data retention orgs cannot use it), and its
  safety classifiers can refuse flagged cyber or bio work. Recommend it only for work
  genuinely beyond the top model, name the cost, and tell the user to confirm their
  account and provider expose it. Treat the restricted frontier model as unavailable
  unless the account shows it.
* **Stale catalog.** If the Last updated date in `models.md` is more than about three
  months before today, append one warning line telling the user to verify model names
  and prices against the docs linked in `models.md` before trusting them.
* **Confidence is a heuristic.** It is your judged probability that the tier clears
  the task, not a measured number. Never present it as a guarantee.
* **Out of scope.** If the input could be a prompt the user intends to run, size it as
  that task, even when it reads like a general question. Only input addressed to
  Caliber itself is out of scope; say briefly that this tool sizes a specific task
  and ask for it.

## Worked example (for calibration, not to copy verbatim)

Task, asked through `/caliber`: "rename a local helper function and update its three
call sites in one file." Signals: complexity Low, cost of error Low (it will not
compile if wrong, instantly caught), value Low, viability High. Budget and Optimal
converge on the small tier and merge into one block.

```
Current session: <mid tier model> at high (assumed default from models.md)
Cost of error: Low (a rename that breaks will not compile, caught instantly)

▶ BUDGET = OPTIMAL (default for most tasks)
<small tier model>, effort n/a (no effort dial)
Confidence it clears the task: High
Why: mechanical edit in one file with an instant compile check, nothing rewards more
If it stalls: <mid tier model> at low effort
Apply (Claude Code): /model <small tier API name>

SPLURGE
<mid tier model> at low effort
Confidence it clears the task: High
Why: only worth it if the rename hides real ambiguity, which is unlikely here
If it stalls: <mid tier model> at high effort

Versus current session: a step down; the small tier runs this at a fraction of the mid tier price and loses nothing on work this mechanical.
```

For a task this simple the output stays this short. The apply line drops the
`/effort` half because the small tier has no effort dial.
