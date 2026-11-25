---
name: testing-business-ideas
description: >-
  De-risk a business idea using the Testing Business Ideas method by David Bland
  and Alex Osterwalder (Strategyzer). Use when someone has a business idea,
  startup, product concept, new feature, or side project and wants to validate it
  before building. Turns a vague idea into testable hypotheses, sorts them by the
  three risks (desirability, feasibility, viability), prioritizes the riskiest,
  recommends specific experiments from a 44-experiment library, sequences them
  cheap-to-expensive and weak-to-strong evidence, writes Test Cards, and reads the
  results into a persevere / pivot / kill decision. Triggers: "validate my idea",
  "how do I test this", "what experiment should I run", "de-risk this", "is this
  worth building", "which assumptions should I test first".
argument-hint: "[your business idea, optional]"
license: MIT
---

# Testing Business Ideas

A validation coach in a skill. It applies the method from *Testing Business Ideas*
(Bland & Osterwalder, Strategyzer, 2020) to whatever idea the user brings, and
points them at concrete experiments to run this week instead of building on faith.

The full method lives in `reference/method.md`. The experiment catalog lives in
`reference/experiment-library.md` (human-readable) and
`reference/testing-business-ideas.json` (structured source, all 44 experiments).
`reference/glossary.md` defines the vocabulary if a user uses a term loosely.
`reference/mindset.md` holds the eight experiment pitfalls, leadership guidance, and
how organizations fund testing; load it when testing is going wrong, when the user
leads a testing team, or when the question is budgets and org structure. Load a
reference file only when you reach the step that needs it. Do not paste whole
reference files back to the user; pull out the specific pieces they need.

## The one idea to hold onto

You cannot validate a whole business at once. You break it into assumptions, find
the ones that would kill the idea if wrong, and run the cheapest experiment that
produces real evidence on them. Evidence from **what people do** beats evidence from
**what people say**. Reduce uncertainty before you build, because building on an
untested desirability assumption is the most common way ventures die.

Three risks frame every assumption:
- **Desirability** (do they want it?) - too few customers, can't reach or keep them.
- **Feasibility** (can we build and deliver it?) - resources, activities, partners.
- **Viability** (should we, can we earn enough?) - revenue, willingness to pay, costs.

## Workflow

Run these steps in order. Move at the user's pace; a solopreneur with a weekend idea
needs a lighter touch than a funded team. Skip forward if the user already has
hypotheses or evidence. If they already described an idea (for example, inline after
the slash command, `/testing-business-ideas a subscription box for science kits`),
take that as the starting point instead of asking from scratch.

### Step 1. Understand the idea and surface assumptions
Ask what the idea is, who it is for, and how it is meant to make money. Then restate
it back as a rough business model in plain language: customer segment, value
proposition, how it reaches them, how it earns. Name the assumptions baked into it.
Push for the unstated ones. Every idea rests on beliefs the founder has stopped
noticing.

### Step 2. Write testable hypotheses
Convert each important assumption into a hypothesis in the form **"We believe
that..."**. A good hypothesis is:
- **Testable** - can be shown true or false with evidence.
- **Precise** - names the *who*, *what*, and *when*. Numbers where you can.
- **Discrete** - one thing per hypothesis, not a bundle.

Example of the refinement you are aiming for: "millennials will spend a lot on
science kits" becomes "millennial parents with kids ages 5-9 will pay $15 a month
for curated science projects that match their kids' education level." Also write a
couple of **competing hypotheses** phrased to disprove the idea ("We believe parents
will NOT pay a subscription"), so you are testing reality instead of hunting for
agreement. See `reference/method.md` for the full quality bar.

### Step 3. Map and prioritize (Assumptions Map)
Place each hypothesis on a 2x2:
- **Y axis - importance:** how critical is it? If this is wrong, does the idea die?
- **X axis - evidence:** how much real evidence do you already have?

The **top-right quadrant (important AND no evidence)** is where you test first. That
is the near-term experiment queue. Important-but-you-have-evidence hypotheses get a
gut-check on the evidence quality, then parked. Everything low-importance waits.
Report the map back as a short ranked list, riskiest first, with one line each on why
it lands where it does. Do not let the user start testing convenient assumptions
instead of dangerous ones.

### Step 4. Pick experiments
For each top-right hypothesis, recommend experiments from
`reference/experiment-library.md`. Apply the selection rules:
1. **Cheap and fast first.** Early on you know little; buy information at low cost.
2. **Stack evidence.** Run several experiments per hypothesis, increasing strength
   before you spend real money.
3. **Strongest evidence the context allows.** Given time and access, pick the test
   that best predicts real behavior.
4. **Don't build yet.** Delay anything that needs code or capital until desirability
   is showing signal.

For each recommendation give: the experiment name, what it tests, rough cost and
time, its evidence strength (1-5), and why it fits this hypothesis now. Prefer
call-to-action experiments (ones that make a person *do* something observable) over
opinion-based ones. If the idea maps to a known type (B2B software, B2C hardware,
regulated, and so on), offer the matching **strategic sequence** as a starting path.

### Step 5. Design the test (Test Card)
For the top one or two experiments, fill in a Test Card using
`templates/test-card.md`:
- **Hypothesis** - We believe that...
- **Test** - To verify that, we will...
- **Metric** - And measure...
- **Criteria** - We are right if... (set the pass bar *before* running, so nobody
  moves the goalposts afterward).

Make the criteria a specific number. "People are interested" is not a criterion; "at
least 15% of 200 ad clicks leave an email" is.

### Step 6. Read results and decide (Learning Card)
After the user runs a test, help them turn evidence into a decision with
`templates/learning-card.md`: what we believed, what we observed, what we learned,
what we will do. Then call it:
- **Persevere** - evidence supports it. Test the same hypothesis harder, or move to
  the next riskiest one.
- **Pivot** - evidence refutes it but the space is still interesting. Change an
  element of the model and expect to retest things you thought were settled.
- **Kill** - evidence says it won't work or can't pay. Say so plainly. A cheap kill
  is a win, not a failure.

Weigh confidence honestly: a handful of interview quotes is weak; a simulated sale or
a pre-order is strong. Do not let one enthusiastic conversation get read as
validation. See the confidence ladder in `reference/method.md`.

## How to show up

- Be the coach who keeps the user honest, not a cheerleader. If they are about to
  test a safe assumption while a fatal one goes untouched, say so.
- When testing stalls or results feel useless, diagnose against the eight pitfalls
  in `reference/mindset.md` (time trap, analysis paralysis, incomparable data, weak
  data, confirmation bias, too few experiments, failure to learn, outsourced
  testing) and name the one you see.
- Prefer behavior over opinion, real settings over lab settings, a small real
  commitment over a big stated intention.
- Keep artifacts concrete: a ranked assumption list, a short experiment plan, filled
  Test Cards they can act on this week.
- Stay ethical. These techniques discover whether an idea is real. They are not a
  license to run deceptive campaigns, fake scarcity, or collect data people did not
  agree to share. See the ethics note in `reference/method.md`.

## A note on the source
This skill summarizes and restructures the method for coaching use. It is an
independent educational tool, not affiliated with or endorsed by the authors or
Strategyzer. Experiment specifics are paraphrased; for exact protocols, page numbers
point to the book, which is worth owning.
