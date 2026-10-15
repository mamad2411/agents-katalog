---
name: efficient-semantic-thinking
description: Use when an agent is processing complex information, planning multi-step tasks, maintaining state, comparing alternatives, repeatedly manipulating information, or drafting text that shows signs of AI-generated writing. Apply whenever natural-language reasoning introduces linguistic overhead, repetition, ambiguity, or verbosity, or when output needs to read as human-written — factual, specific, and free of promotional filler, inflated significance, and formulaic phrasing.
---

# Efficient Semantic Thinking

Think in **meaning before wording**. Convert unnecessary natural-language structure into compact semantic representations, operate on the compressed representation, and expand back into natural language only when communicating with the user.

The goal is to minimize linguistic overhead without dropping any information that affects the result. Cutting words for their own sake does not count.

When active, announce: "I'm using the efficient-semantic-thinking skill."

## When to Use

Use when:

* A task contains multiple constraints, entities, dependencies, or conditions.
* The same information must be referenced repeatedly.
* A task requires planning across multiple steps.
* The agent is comparing, filtering, sorting, ranking, or transforming information.
* A tool workflow contains substantial structured state.
* The agent needs to maintain state across several operations.
* Natural-language phrasing is becoming repetitive.
* A concept can be represented more precisely as a relation, predicate, value, or state.
* The agent is processing large amounts of information where linguistic repetition adds little meaning.

Use when NOT:

* The task is trivial and compression would add more complexity than it removes.
* The user is asking for ordinary conversation.
* The task requires prose as the primary output.
* Compression would remove ambiguity or important nuance.
* The representation would require inventing a vocabulary instead of simply using existing semantic primitives.

## The Iron Law

```text
MEANING FIRST. WORDING SECOND. COMPRESSION ONLY AFTER MEANING IS PRESERVED.
```

Never remove information merely because it makes the representation shorter.

Never replace a specific fact with a generic abstraction.

Never replace uncertainty with false precision.

Never replace a useful statement with decorative language.

## Core Model

Treat natural language as an encoding of information rather than the information itself.

For every piece of input, distinguish:

```text
MEANING
├─ ENTITY
├─ ACTION
├─ STATE
├─ ATTRIBUTE
├─ RELATION
├─ CONSTRAINT
├─ CONDITION
├─ TIME
├─ LOCATION
├─ QUANTITY
├─ PREFERENCE
├─ GOAL
├─ UNCERTAINTY
└─ EVIDENCE
```

Do not preserve linguistic structure that does not contribute meaning.

For example:

```text
"I would like you to find me a laptop that costs no more than
$700 and preferably has good battery life."
```

becomes:

```text
TASK:FIND
OBJ:LAPTOP

REQ:
PRICE<=700USD

PREF:
BATTERY=HIGH
```

The words disappear. The requirements remain.

## When Compression Helps

Compression is valuable when it removes:

* Repetition
* Filler
* Unnecessary qualifiers
* Repeated grammatical structure
* Redundant explanations
* Repeated entity names
* Repeated constraints
* Decorative language
* Generic statements that do not change the conclusion

Compression is NOT valuable when it removes:

* Specific facts
* Numerical precision
* Causal relationships
* Exceptions
* Conditions
* Uncertainty
* Source attribution
* User preferences
* Important distinctions

## Avoid AI Writing Patterns

Many of the signs of AI-generated writing are, at their root, linguistic overhead — statements that puff up significance, pad with formulaic phrasing, or substitute vague generality for specific facts. Removing them is part of semantic compression.

When drafting or editing text, avoid these patterns:

**Inflated significance and legacy.** No "stands as a testament," "pivotal moment," "evolving landscape," "marks a shift," "indelible mark," "contributes to the broader history." Report what happened, not how important it was. Specific facts beat grand statements.

**Superficial -ing analyses.** No trailing "highlighting its importance," "underscoring the need," "ensuring continuity," "reflecting broader trends." If the clause after the comma is commentary, cut it or turn it into a concrete fact.

**Promotional language.** No "vibrant," "rich heritage," "breathtaking," "revolutionary," "renowned," "seamless." State attributes directly, with specifics.

**Vague attributions.** No "experts believe," "observers note," "it is widely regarded." Name the source or drop the claim.

**Canned notability claims.** No "featured in prominent outlets," "maintains an active social media presence," "has been profiled in." List the coverage or omit it.

**AI vocabulary.** Avoid stacking words like "crucial," "delve," "enhance," "landscape," "leverage," "furthermore," "additionally," "ultimately." Prefer plain equivalents.

**Copula avoidance.** "Serves as," "stands for," "represents" where "is" works. Use the simple copula.

**Negative parallelisms.** "Not just X, but Y," "not X, but Y," "X rather than Y." State the positive directly.

**Rule of three.** Forcing items into triads — "A, B, and C." Use two or four when the content allows.

**Elegant variation.** Swapping synonyms to avoid repeating a word ("the study... the research... the paper"). Repetition is clearer.

**Em dash overuse.** Heavy reliance on "—" for dramatic reveals. Commas and periods read more naturally.

**Curly-quote / formatting tells.** Overuse of boldface, title-case headings, and emoji-as-formatting.

### The test

If a sentence would read fine as a pull-quote — "This represents a major step in the right direction" — rewrite it as plain information. Pull-quote language is the tell.

## Process

### Phase 1 — Semantic Extraction

Strip the input down to its operational meaning.

1. Identify the user's actual goal.
2. Identify every entity relevant to that goal.
3. Extract hard requirements.
4. Extract preferences separately.
5. Extract conditions and exceptions.
6. Extract numerical values and comparison operators.
7. Extract temporal and geographic constraints.
8. Preserve uncertainty.
9. Preserve evidence and source relationships when relevant.
10. Ignore conversational filler that does not affect the task.

Example:

```text
"I'd probably want something pretty cheap, maybe around
$500 or less, but I really need at least 16GB of RAM."
```

becomes:

```text
PRICE<=500USD
RAM>=16GB
RAM=HARD_REQ
PRICE=SOFT_PREF
```

Do not interpret "probably," "pretty," or "really" as information unless the context gives them operational meaning.

**Completion criterion:** Every fact, constraint, preference, dependency, and uncertainty capable of changing the result is represented.

### Phase 2 — Semantic Compression

Replace natural-language structures with compact semantic primitives.

Prefer:

```text
PRICE<=500
RAM>=16GB
OS=WINDOWS
```

over:

```text
The computer needs to cost no more than $500,
should have at least 16GB of RAM, and needs to run Windows.
```

Use compact operators consistently:

```text
=     equals
!=    not equal
>     greater than
<     less than
>=    greater than or equal
<=    less than or equal
&     AND
|     OR
!     NOT
->    causes / transitions to
=>    implies
?     uncertain
@     context / association
```

Prefer direct semantic forms:

```text
PRICE<=500
```

instead of:

```text
The price should ideally be no more than $500.
```

Prefer:

```text
FACT:APPLE_RELEASED_IPHONE_15=2023
```

instead of:

```text
Apple's release of the iPhone 15 occurred in 2023,
which represents an important moment in the company's
ongoing product history.
```

The second representation contains substantially more wording without adding equivalent operational information.

**Completion criterion:** The compressed state contains the same decision-relevant information using fewer semantic units or a clearer structure.

### Phase 3 — Preserve Specificity

Do not allow compression to turn specific information into generic information.

Bad:

```text
PERSON=IMPORTANT_INVENTOR
```

Good:

```text
PERSON=ELIAS_HOWE
FACT=INVENTED_MODERN_LOCKSTITCH_SEWING_MACHINE
YEAR=1845
```

Bad:

```text
COMPANY=SUCCESSFUL
```

Good:

```text
COMPANY=APPLE
REVENUE=...
PERIOD=...
SOURCE=...
```

Specific information is more valuable than generic descriptions.

**Completion criterion:** No specific fact has been replaced by a broader statement that loses information.

### Phase 4 — Eliminate Linguistic Overhead

While processing information, actively remove structures that carry little semantic value.

Prefer:

```text
IS
HAS
USED
WROTE
MOVED
```

over unnecessary inflated equivalents such as:

```text
SERVES_AS
FEATURES
UTILIZED
AUTHORED
RELOCATED
```

Prefer direct statements over elaborate constructions:

```text
CAUSE=X
```

instead of:

```text
This is significant because it serves to demonstrate that X
ultimately contributes to...
```

Do not add:

```text
IMPORTANCE
LEGACY
BROADER_TREND
FUTURE_IMPACT
```

unless those concepts are actually relevant to the task.

Do not manufacture analysis merely because the subject appears to invite analysis.

**Completion criterion:** Every remaining linguistic component performs a semantic function.

### Phase 5 — Reason Over Structure

Perform operations against the semantic state instead of repeatedly reconstructing the original prose.

Example:

```text
TASK:FIND
OBJ:LAPTOP

REQ:
OS=WINDOWS
RAM>=16GB
STORAGE>=512GB
PRICE<=700

PREF:
PERFORMANCE>BATTERY
```

Candidate data:

```text
A:PRICE=649 RAM=16 STORAGE=512 PERF=MED BAT=HIGH
B:PRICE=679 RAM=32 STORAGE=1024 PERF=HIGH BAT=MED
C:PRICE=599 RAM=8  STORAGE=512 PERF=HIGH BAT=HIGH
```

Filter:

```text
VALID=A,B
REJECT:C RAM<16
```

Rank:

```text
B>A
```

Conclusion:

```text
BEST=B
```

The agent does not need to repeatedly restate the original requirements in prose.

**Completion criterion:** The current state directly supports the next operation without reconstructing unnecessary natural-language context.

### Phase 6 — Compress Repeated Concepts

When the same entity or concept appears repeatedly, assign a stable reference.

Instead of:

```text
Rochester Institute of Technology
Rochester Institute of Technology
Rochester Institute of Technology
```

use:

```text
RIT
```

For multiple entities:

```text
E1=RIT
E2=UB
E3=RPI
```

Then:

```text
COMPARE:E1,E2,E3
```

Do not create abbreviations that are difficult to interpret or remember.

**Completion criterion:** Repeated concepts have stable references and can be reconstructed unambiguously.

### Phase 7 — Expand Only at the Communication Boundary

The compact representation is a working format, not automatically the user-facing format.

Convert:

```text
BEST=B
WHY:
RAM=32
STORAGE=1024
PERF=HIGH
```

into:

> B is the best option because it has 32GB of RAM, 1TB of storage, and the strongest performance among the qualifying options.

Do not expose semantic notation unless:

* The user asks for it.
* The notation is itself useful.
* The task is about the representation.
* The user is building or debugging an agent using this system.

**Completion criterion:** The user receives the requested output format with all relevant information preserved.

## Quick Reference

| Situation       | Representation |
| --------------- | -------------- |
| Simple fact     | `FACT:X=Y`     |
| Entity          | `E1=ENTITY`    |
| Requirement     | `REQ:X=Y`      |
| Preference      | `PREF:X=Y`     |
| Constraint      | `X>=Y`         |
| Condition       | `IF:X THEN:Y`  |
| Uncertainty     | `X?`           |
| Comparison      | `A>B`          |
| Dependency      | `A->B`         |
| Multiple values | `X={A,B,C}`    |
| Filtering       | `FILTER:X>Y`   |
| Ranking         | `SORT:X_DESC`  |
| Goal            | `GOAL:X`       |
| Decision        | `BEST:X`       |
| Evidence        | `SOURCE:X`     |

## Common Mistakes / Anti-patterns

* ❌ **Word-count optimization** — A shorter string is not automatically a better representation.

* ❌ **Semantic deletion** — Removing a detail because it appears minor can change the answer.

* ❌ **Generic replacement** — Replacing specific facts with words like "important," "successful," or "significant" destroys information.

* ❌ **Decorative reasoning** — Adding significance, legacy, impact, or broader trends without a task requirement adds noise.

* ❌ **Vocabulary inflation** — Using complicated synonyms when simple words represent the same concept increases linguistic overhead.

* ❌ **Repeated restatement** — Repeating unchanged constraints instead of maintaining them as state wastes representation.

* ❌ **Fake certainty** — Compressing uncertainty into a definite value changes meaning.

* ❌ **Premature abbreviation** — Creating an opaque shorthand can cost more cognitive effort than it saves.

* ❌ **Output leakage** — Returning raw semantic notation when the user requested normal language reduces usability.

* ✅ **Semantic compression** — Remove wording while retaining meaning.

* ✅ **Specificity preservation** — Keep exact facts rather than generic summaries.

* ✅ **State reuse** — Store information once and reference it.

* ✅ **Direct language** — Prefer the simplest expression that preserves meaning.

* ✅ **Selective compression** — Compress complex state, not everything indiscriminately.

* ✅ **Natural output** — Expand the final result into the format the user expects.

## Red Flags — STOP and Reconsider

If you catch yourself thinking:

* "This sounds more sophisticated."
* "This makes the answer sound more important."
* "I should mention the broader significance."
* "I can probably replace this specific fact with a general statement."
* "This qualifier makes the sentence sound better."
* "I should explain this again for completeness."
* "A more advanced word would sound more professional."
* "I can probably infer the missing detail."
* "Shorter automatically means better."
* "The user probably won't notice this information was removed."

Stop and return to semantic extraction.

## Common Rationalizations

| Excuse                                        | Reality                                                                                               |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| "More words means more reasoning."            | Additional wording can represent additional information, but it can also be pure linguistic overhead. |
| "Complex vocabulary is more precise."         | Often the simpler word carries the same semantic value with less overhead.                            |
| "The broader context is useful."              | Only include broader context when it changes understanding or satisfies the task.                     |
| "I'll just summarize the details."            | Summarization can destroy information. Preserve details that affect the outcome.                      |
| "The user asked for a detailed answer."       | Detail means information, not necessarily verbosity.                                                  |
| "This sounds professional."                   | Professionalism does not require inflated language.                                                   |
| "The model can infer the omitted constraint." | Important constraints should remain explicit.                                                         |
| "I can make the representation even shorter." | Stop compressing when further compression risks ambiguity or information loss.                        |

## Example

User:

> "I need to pick between three laptops for college. I don't want to spend more than $700. Windows is required. I need at least 16GB of RAM and 512GB of storage. I'd prefer better performance, but battery life matters too."

Semantic state:

```text
TASK:SELECT
OBJ:LAPTOP

REQ:
PRICE<=700USD
OS=WINDOWS
RAM>=16GB
STORAGE>=512GB

PREF:
PERFORMANCE>BATTERY
BATTERY=HIGH

CANDIDATES:
A:PRICE=649 RAM=16 STORAGE=512 PERF=MED BAT=HIGH
B:PRICE=679 RAM=32 STORAGE=1024 PERF=HIGH BAT=MED
C:PRICE=599 RAM=8  STORAGE=512 PERF=HIGH BAT=HIGH
```

Filter:

```text
VALID={A,B}
REJECT:
C:R[RAM<16]
```

Rank:

```text
B>A
```

Decision:

```text
BEST=B
```

Final response:

> I'd pick B. It meets every requirement and has 32GB of RAM, 1TB of storage, and the strongest performance. A has better battery life, but you said performance matters more.

## Final Principle

The target is not:

```text
FEWER WORDS
```

The target is:

```text
MORE MEANING / LESS LINGUISTIC OVERHEAD
```

A good representation should be:

```text
COMPACT
+ PRECISE
+ REVERSIBLE
+ SPECIFIC
+ UNAMBIGUOUS
```

When compression and precision conflict:

```text
PRECISION > COMPRESSION
```

When natural language and semantic structure conflict during internal processing:

```text
SEMANTIC STRUCTURE > NATURAL-LANGUAGE FORM
```

When communicating with the user:

```text
USER_REQUESTED_FORMAT > INTERNAL_REPRESENTATION
```
