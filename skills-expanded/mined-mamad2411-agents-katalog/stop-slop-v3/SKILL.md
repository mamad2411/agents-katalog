---
name: stop-slop-v3
version: 3.0.0
description: Produce clean, human-register prose by routing into specific voice basins. Use when drafting, editing, or reviewing text for AI patterns, or when matching a writer's voice from a sample. Replaces restriction-based anti-slop methods with retrieval-shaped positive constraints, with an optional editorial pass against an expanded diagnostic taxonomy.
license: MIT
metadata:
  trigger: Writing prose, editing drafts, reviewing content for AI patterns, matching a writer's voice from a sample
  author: Wake & Claude (Axiom). v3 integrates the WikiProject AI Cleanup "Signs of AI writing" catalogue from the humanizer skill (Siqi Chen, MIT) into the editorial layer of Stop Slop v2.
  architecture: Retrieval-Shaped Prompting & Constrained Synthesis v3
---

# Stop Slop v3

Route prose into specific human-register basins. Do not load AI failure patterns into generation context. Use the diagnostic taxonomy only for post-hoc editorial review, never as priming material.

## Architecture Principle

Negative prompting activates the basin it intends to suppress. Listing phrases to avoid primes those phrases. Cataloguing structures to reject makes those structures salient at inference time. The model spends generation energy resisting tokens that would not have been attractive if they had not been injected.

This skill uses the opposite mechanism: **positive routing constraints that make slop structurally impossible.** The model never sees the failure patterns during generation. It sees where to go, not where to avoid.

The diagnostic taxonomy in `references/diagnostic-taxonomy.md` is a separate tool with a separate purpose. It is consulted *after* a draft exists, by a reviewer or by the Final Audit Pass, to spot residue. It is never loaded into the generation context.

## Before Generating Prose

Complete the derivation fields in [references/derivation.md](references/derivation.md) silently before writing. Do not skip this step. Do not treat it as optional. The derivation commits the model to a specific basin before the first sentence is rendered. Without it, the model defaults to its highest-probability prose register, which is the slop basin.

The five required fields are:

1. **readerProfile** — one specific reader, with what they already know and what they need to do after reading.
2. **registerTarget** — a named publication, writer, or communication context whose register this prose should match.
3. **sceneAnchor** — where and when the reader encounters this text, what surrounds them, what they did just before.
4. **textureConstraint** — domain-specific objects and vocabulary that anchor the piece in a material world.
5. **antiPattern** (optional) — a positive redirection addressing a specific failure mode observed in prior drafts.

See `references/derivation.md` for the full specification and a worked example.

### Voice Sample (v3 addition, optional)

If the user provides a sample of their own writing, read it before completing the derivation. Note sentence length patterns, word choice register, opener habits, punctuation patterns, recurring phrases, and transition style. Then add a sixth derivation field — `voiceSample` — populated with the structural observations.

When a sample is provided, the sample replaces "the closest publication" with "this writer's actual voice" as the basin to route into. If the writer uses "stuff" and "things," do not route to "elements" and "components." If the writer writes short sentences, do not produce long ones. The other five fields remain in force.

A user can provide a sample inline ("here is a sample of my writing: ...") or by reference ("use my writing in this file as a style reference"). When no sample is provided, derive the register from the task as normal.

## Core Routing Constraints

These six constraints are simultaneous. Every sentence of output must satisfy all six. They are phrased as positive requirements, not prohibitions.

### 1. Human Subject Rule

Every sentence has a named or specific human subject performing a concrete action. "You" counts. A named role ("the engineer," "her landlord") counts. Inanimate objects, abstractions, and unnamed collectives do not act.

- ✓ "She cancelled the contract on Thursday."
- ✓ "You will lose three clients if the API goes down."
- ✗ "The decision emerged from weeks of discussion."
- ✗ "The market rewards bold moves."

### 2. Material Anchor Rule

Every claim, observation, or argument must contain at least one concrete noun: an object, a cost, a distance, a duration, a name, a sensory detail. Sentences that consist only of abstract nouns evaluating other abstract nouns fail this rule.

- ✓ "The migration will take nine weeks and cost the Austin office $14,000 in overtime."
- ✗ "The implications of this shift are significant."

### 3. Single-Pass Assertion Rule

State the point on arrival. No runway. No negation-then-assertion. No "not X, but Y." No previewing what you are about to say. The first sentence of a paragraph is the claim. Everything after it is evidence or consequence.

- ✓ "Retention dropped 12% after the rebrand."
- ✗ "The problem isn't the product. It's the positioning."

### 4. Rhythm Variation Rule

No three consecutive sentences may fall within five words of each other in length. Inline lists contain two items. Paragraphs do not end with their shortest sentence. No stacked fragments.

### 5. Register Lock Rule

The derivation fields specify a target register. Every sentence must be plausible in that register. If the derivation says "working engineer's Slack message," then no sentence may read like a keynote speech. If the derivation says "literary essay for Granta," then no sentence may read like a blog post. The register is a fence. Stay inside it.

### 6. Earned Emphasis Rule

No sentence may announce its own importance. Importance is earned by the specificity and consequence of the content. "This matters" is empty. The reader decides what matters based on what you showed them.

- ✓ "If the patch ships late, the 2.0 launch slips to Q3 and the Series B deck needs new numbers."
- ✗ "This matters because timing is everything."

## Voice Within the Register (v3 addition)

The six constraints make slop structurally impossible. They do not, on their own, guarantee that the prose has a pulse. A piece can satisfy all six constraints and still read as well-scrubbed corporate-neutral. The Register Lock prevents that drift, but only if the `registerTarget` specifies a register with a human posture inside it.

When the target register includes a first-person perspective or commentary, the following are positive moves available within the basin:

- **Hold a position.** Report consequences, then take the stance the consequences imply. "The deal is bad for the seller" is a stance. "The deal has pros and cons" is the absence of one.
- **Name mixed feelings when they are real.** Two true reactions to the same thing, held at once, are a feature of human cognition. "The launch is impressive and it makes me uneasy" is sayable in most registers above pure technical reportage.
- **Use first person when the register allows it.** "I keep coming back to the third quarter numbers" signals a person thinking. Drop it in registers that forbid it (technical reference, legal filing).
- **Permit small structural mess.** A short aside, a one-clause tangent, a sentence that refines a previous one. Perfect paragraphic structure is itself a slop tell. The Rhythm Variation Rule already forces variance in length; this is variance in *function*.
- **Specify the feeling, not the label.** "There is something unsettling about agents working at three in the morning while nobody is watching" routes harder than "this is concerning."

These are moves available *inside* the register basin. They are not license to break it. If the `registerTarget` is "FDA submission," none of the above applies.

## Quick Routing Checks

Before delivering prose, run these checks. Each one is a presence test, not an absence test.

- Does every sentence have a human subject? Find the actor in each one.
- Does every paragraph contain at least one concrete noun (object, number, name, place, texture)?
- Does the first sentence of each paragraph state the point?
- Do sentence lengths vary across every three-sentence window?
- Does the prose stay inside the register specified in the derivation?
- Is every claim of importance backed by a specific consequence in the same paragraph?
- Could a reader identify the author's target register without being told? (If the prose is register-neutral, the derivation failed.)
- If a `voiceSample` was provided, do the sentence rhythms and word choices in the output match it?

## Final Audit Pass (v3 addition, optional)

For high-stakes drafts, run one editorial pass after the routing checks. **This is the only place in the skill where AI failure patterns may be loaded into context, and it happens after generation, on a finished draft, not during writing.**

The pass has two steps.

**Step 1.** Ask: "What makes the below so obviously AI generated?" Answer in two or three short bullets, naming the specific residue. If nothing stands out, the audit ends here.

**Step 2.** Ask: "Now make it not obviously AI generated." Revise the draft to remove what step 1 named.

If step 1 returns repeated hits on specific patterns, consult `references/diagnostic-taxonomy.md`:

- Use **Part I (mechanism categories)** to diagnose the *cause* — usually a weak derivation field, not a vocabulary problem.
- Use **Part II (specific pattern catalog)** to see exactly how the offending construction is rewritten.

Run this pass on the finished draft, in editor mode, never while writing the next paragraph.

## Scoring

Rate 1-10 on each dimension. Each dimension measures a positive quality.

| Dimension | Measures |
|-----------|----------|
| Specificity | Concrete nouns per paragraph. Objects, costs, names, textures, durations. |
| Agency | Percentage of sentences with a human subject performing a concrete verb. |
| Rhythm | Sentence-length variance across the piece. Standard deviation of word counts. |
| Register fidelity | Would this paragraph be publishable in the target outlet without editing for voice? |
| Density | Ratio of load-bearing sentences to total sentences. Every sentence advances the argument or provides evidence. |

**Below 35/50: the derivation was too thin. Re-derive and rewrite.**

## Reference Files

- [references/derivation.md](references/derivation.md) — Derivation fields (readerProfile, registerTarget, sceneAnchor, textureConstraint, antiPattern, voiceSample). Complete before every prose task.
- [references/routing-patterns.md](references/routing-patterns.md) — Positive structural patterns organized by register: technical, conversational essay, literary, business, narrative fiction, instructional.
- [references/examples.md](references/examples.md) — Four worked examples showing the same input transformed by restriction vs. routing.
- [references/diagnostic-taxonomy.md](references/diagnostic-taxonomy.md) — Human-facing reference catalogue. Part I: eight mechanism categories from Hardik Pandya's Stop Slop. Part II: twenty-nine specific pattern types from WikiProject AI Cleanup. **For editorial review only. NEVER load into generation context.**

## Source Basis

The diagnostic taxonomy in this skill draws from two sources, integrated in v3:

- **Part I**, the mechanism categories, comes from [Hardik Pandya's original Stop Slop](https://github.com/hardikpandya/stop-slop) (MIT). Stop Slop v2 (Wake & Claude, Axiom) reorganized these into eight causal failure modes and added per-mode explanations of why the model produces each pattern.
- **Part II**, the specific pattern catalog, comes from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup, via the [humanizer skill](https://github.com/blader/humanizer) (Siqi Chen, MIT). v3 integrates this catalog into the editorial layer, not the generation layer, in keeping with this skill's architectural principle.

Key insight from WikiProject AI Cleanup: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases." The routing constraints in this skill exist to push generation away from that default basin and toward a chosen one.

## License

MIT. See `LICENSE`.
