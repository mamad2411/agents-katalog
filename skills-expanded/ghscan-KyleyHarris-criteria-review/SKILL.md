---
name: criteria-develop
description: Implement the code for criteria the build does not yet satisfy, test first: write the journey, watch it fail for the criterion's own reason, then build until it passes, walking the implementation against the scenario as you go. Refuses to change a criterion or a journey's clauses to make a test pass, and stops to ask when the criterion turns out to be wrong. Use when the architect says "implement these", "build this feature", "make these pass", or a plan holds scenarios carrying a write-the-code-to-match work order.
---

# Implement against the criteria

The other half of the work orders the review produces. `criteria-test` writes the journey that
proves a criterion; this takes criteria the build cannot satisfy and makes it satisfy them.

---

## The cardinal rule

**Never edit a criterion, or a journey's clause keys, to make a test pass.**

It is the one failure that is both easy and invisible. A reworded `Then` turns red green, the
suite reports success, the requirement quietly became whatever the code already did, and nobody
can see it happened afterwards. Everything else in this system exists to prevent exactly that.

If the criterion turns out to be wrong - and it sometimes will, because it may have been
inferred by someone reading code - **stop and raise it**:

```bash
npx criteria-review ask <ID> --message "Implementing this, I found <what>. The criterion says <clause>, which cannot be satisfied because <reason>. Should the criterion change?" --as claude
```

Then move to another item. Changing the requirement is the architect's decision, not a step in
getting to green.

The corollary: the generated scenario module is not editable either. It is emitted from the
documents, and a change there is a change to the requirement made in the wrong place.

## 1. Take the work, and confirm what it is

```bash
npx criteria-review plan            # what this task covers
npx criteria-review plan next       # the next outstanding one
npx criteria-review show <ID>       # the criterion in full, with its notes
```

**Read the notes.** A work order usually arrived as one: it names what the software does today
and, often, the blocker. Implementing without reading it is how a session rediscovers something
the architect already wrote down.

Confirm the criterion is confirmed. A scenario still marked `INFERRED` and unreviewed is a
guess, and building code to satisfy a guess is expensive. Say so and offer `criteria-lookup`.

## 2. Write the failing journey first

**Test first, always, and this skill owns writing it.** Not because TDD is a preference, but
because of what the alternative produces: a journey written after the feature is written to match
what was built, which is a description of your own code with an assertion wrapped round it. It
passes on the first run, it will pass on every run, and it can never tell you that you built the
wrong thing.

So before any implementation:

1. Bind the journey to the criterion's clauses - generated, never retyped, one body per clause.
2. **Run it, and watch it fail for the reason the criterion names.** Not a missing route, not a
   compile error, not a selector typo: the specific outcome the scenario says should happen and
   does not. A red that comes from scaffolding proves nothing and will go green for the wrong
   reason.
3. Only then write code.

Do not hand this to `criteria-test`. That skill learns behaviour by driving a **running**
application, which is exactly what does not exist yet - here there is nothing to observe, and the
criterion is the only description of what should happen. Use its rules for binding, selectors and
seeding; do not use its method.

**Already green before you have written anything?** Then either the work is done, or the journey
is not proving what it claims. Find out by breaking the behaviour deliberately. A journey that
stays green through that is the finding, and it matters more than the feature.

## 3. Implement, walking the code against the scenario

Take the clauses in order. They are a description of what has to become true, and they are a
better guide than a ticket because each one is checkable.

While you work:

- **Follow the project's own conventions.** Read a sibling implementation before adding a new
  one; match its naming, its error handling, its layering. A correct feature in a foreign style
  is a maintenance cost the reviewer has to pay.
- **The negative clauses are requirements too.** "And the drawer does not open" is work, not
  commentary, and it is usually the part that gets forgotten.
- **Cover the engineering obligations the change instantiates** - the tier the criteria
  deliberately do not mention. Partial writes, idempotency under retry, races, malformed input,
  boundaries. `criteria-review guide` and the standard's obligations catalogue name them; a
  scenario never will, because no operator would describe one.
- **State intent in comments** as you go: why, not what. The scenario is the why for the
  feature; the comments carry the why for each decision inside it.

## 4. Green, then prove it means something

A passing journey is not the end - though having watched it fail first, you already know it can.
Confirm the same for each clause you added along the way: break the thing you just built,
confirm the journey goes red **on the right assertion**, restore. A feature whose test cannot
fail has shipped untested with a green badge on it, which is worse than shipping it untested.

Then run the wider suite, not just this journey. The most common damage from a feature is to
something nobody was looking at.

## 5. Regenerate if any document moved

If a criterion changed while you worked - the architect answered a question, or clarified a
clause - regenerate before running anything:

```bash
npx criteria-review generate . --out <the project's emit path>
```

Otherwise the suite is proving the previous requirement, and the gate will catch it later in a
place with less context than here.

## 6. Report, and leave the status alone

```
LOCK-OPEN-002  implemented; journey green, proved red by <mutation>; obligations covered: O3, O10
CASH-CLOSE-003 NOT implemented - the criterion cannot be satisfied as written; raised @looknow
```

**Place it in the walkthroughs before reporting done.** A scenario nobody placed is absent
from what a customer is shown, and nothing announces it. `criteria-review present place <ID>`
recommends where; the person who wrote it decides, and QA confirms. This is stage 6a of the
definition of done, not a courtesy.

**Do not accept or verify anything.** `verified` claims a person watched the software do it, and
`accepted` is a claim about intent - neither is an implementer's to make about their own work,
least of all in the same session that wrote it. Hand the finished items to `criteria-lookup`,
and the recordings to `criteria-bundle`.

Leave the work uncommitted for review unless asked otherwise. What you present is the diff and
a note of what proved it.
