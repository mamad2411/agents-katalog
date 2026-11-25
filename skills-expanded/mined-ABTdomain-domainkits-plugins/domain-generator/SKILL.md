---
name: domain-generator
description: Generate modern brandable domains from a user-supplied keyword, concept, or specific taken domain. Treat the input as either a hard literal constraint or a creative seed, then explore abstract, evocative, artistic, sound-led, coined, blended, compound, and modifier-based directions before presenting a small shortlist verified as available at check time. Use when the user already knows the seed or direction and wants creative registrable names, including requests such as "use the word flow" or "getflow.com is taken; create variations". Do not use when requirements are still vague or no seed exists (use domain-name-advisor), when the user wants expired, deleted, aged, or other lifecycle alternatives (use domain-name-advisor in taken-target mode), or when they want trend-based ideas (use keyword-trend-hunter).
---

# Modern Creative Domain Generator

**What this does:** transforms a known keyword, concept, or taken target into a deliberately varied portfolio of modern brand names. It moves beyond mechanical keyword attachment by exploring semantic distance, metaphor, abstraction, sound, letterform, invented language, blends, compounds, and purposeful modifiers, then presents a small shortlist verified as available at check time.

Modern naming does not require every name to describe the product literally. A strong name may communicate a function, benefit, attitude, movement, image, emotional promise, or memorable sound. Abstractness is valid when it creates intentional openness and a coherent brand story; random obscurity is not. Concatenation remains a useful construction method, but it is one instrument rather than the default method.

**Data interfaces it needs.** DomainKits MCP supplies the availability lead and TLD pricing below; host-provided web access supplies the public collision check and the registrar's own pricing page. Equivalent providers are acceptable. Never infer availability from a missing field, request failure, or undocumented response shape; mark the capability `Unavailable` and continue.

- Availability check, DomainKits: `bulk_available`
- A TLD's standard registration and renewal price, DomainKits: `price`
- Premium status and a name's actual registration price: host web access to the registrar's own page
- Web access for a lightweight public-web check on obvious brand collisions

## Evidence discipline

- **Availability is a point-in-time signal.** Only a successful per-domain result that explicitly reports the domain as available qualifies as verified. Any other status, a missing domain row, a failed request, or an unrecognized response does not qualify. Every verified domain must carry the observation timestamp. Describe it as "available at check time", never as guaranteed registrable until registration completes.
- **Respect the creative constraint.** Treat the full input as the source string. Identify possible roots and modifiers as interpretations, not facts (for example, `getflow` may be root `flow` with modifier `get`, or the whole brand `getflow`). Never silently discard a user-required word. When the input is only a conceptual seed, candidates may move beyond the literal string while preserving an explainable connection.
- **Creative meaning is interpretation.** Present metaphors, emotional readings, sound symbolism, and visual impressions as intended creative rationale, not universal fact. Deliberate ambiguity is allowed; accidental incoherence is not.
- **Price is data, not a guarantee.** The price fields are listed under Output format. Premium status comes only from the registrar's own page; when it was not checked, mark it Not Provided and label the price as the TLD's standard price.
- **Availability and a lightweight public-web check do not constitute trademark clearance. Do not claim that a candidate is legally safe to use.**

## Input modes

Determine which input mode applies before generating:

- **Literal constraint:** the exact word, fragment, or spelling must appear. Preserve it and create around it.
- **Conceptual seed:** the keyword supplies meaning or direction but need not appear literally. Permit semantic and phonetic transformation.
- **Taken-target seed:** preserve what the user values in the unavailable target (keyword, pattern, sound, rhythm, image, or brevity), not necessarily every character. If the user wants lifecycle inventory rather than creative variants, use domain-name-advisor.

If the user's wording makes the mode clear, proceed. Ask one concise question only when literal preservation versus creative transformation would materially change the result.

## Creative system

### Semantic distance

Generate across several distances from the source rather than staying at one literal level:

1. **Refined literal:** clean compounds, purposeful modifiers, phrase compression, or TLD integration.
2. **Suggestive:** names expressing the benefit, behavior, outcome, or attitude associated with the seed.
3. **Evocative:** sensory images, movement, materials, nature, spatial ideas, contrast, or metaphor.
4. **Symbolic / abstract:** a compact symbol, invented form, or open-ended idea with a coherent connection to the intended brand character.

When the user imposes a literal constraint, keep the required string while varying the surrounding concept. Otherwise include meaningful non-literal directions; do not make the shortlist a collection of the same keyword with interchangeable prefixes.

### Construction methods

Use construction methods selectively and explain the choice:

- Compounds, including unexpected but coherent pairings.
- Prefix / suffix or word + modifier constructions.
- Portmanteaus and blends with clean morpheme boundaries.
- Clipping, phrase compression, and controlled respelling.
- Coined words built from recognizable semantic or phonetic fragments.
- Sound-first names designed around rhythm, energy, softness, speed, precision, or warmth.
- A semantically integrated TLD or domain hack only when it strengthens the idea and the user accepts the extension and renewal economics.

Do not manufacture availability through random vowel deletion, arbitrary `x` / `z` insertion, doubled letters, or hard-to-defend misspellings. Avoid default startup formulas such as `get-`, `try-`, `use-`, `my-`, `go-`, `-ly`, or `-ify` unless that construction genuinely strengthens this specific name. Do not imitate a famous brand's distinctive naming pattern.

### Sound and visual form

Judge a candidate as both spoken language and a visual mark:

- Syllable count, stress, rhythm, consonant energy, vowel color, and ease of repetition.
- Radio test: whether a listener can repeat and plausibly spell it after hearing it.
- Lowercase readability, letter balance, repeated shapes, and confusing character sequences.
- Memorability without requiring a long explanation.

## Workflow

Use the keyword, TLD, audience, industry, and style the user has already supplied. If a preference is missing, default to `.com` and a balanced modern portfolio of short, pronounceable names, and disclose those defaults. Do not force a long naming interview when the seed is clear.

1. **Set the creative frame.** Determine the input mode. Record the source string, plausible roots or valued features, intended audience or use, TLD constraint, and two or three desired brand qualities. Infer and disclose reasonable qualities when the context supports them; ask only when the literal-versus-conceptual distinction is materially ambiguous. If the user is still choosing the underlying direction, use domain-name-advisor.

2. **Build a creative palette.** Expand the seed into its literal meanings, functions, benefits, emotional promises, verbs, sensory images, metaphors, symbols, phonetic fragments, and useful contrasts. Record what must be preserved and what may transform. This palette is internal working material, not the final answer.

3. **Generate internally (do not show yet).** Generate 40 to 60 candidates across at least four distinct naming territories from the Creative system. Unless the user explicitly requests literal names, ensure that a meaningful share of the pool is evocative, abstract, coined, or sound-led. Include compounds and blends where they are strong, but do not let one construction template dominate. Do not treat `.ai`, `.io`, or `.app` as automatic substitutes; weigh audience, industry, regional meaning, semantic fit, and renewal cost.

4. **Filter intrinsic quality before availability.** Reduce the pool to the strongest 15 to 20:
   - A coherent one-sentence creative rationale; reject accidental nonsense, not intentional abstraction.
   - Distinctiveness from generic category language and tired startup formulas.
   - Easy enough to say, repeat, and spell for the intended audience.
   - Sound and visual form that support the intended brand qualities.
   - A defensible connection to the literal constraint, conceptual seed, or valued feature of the taken target.
   - Avoid unnecessary hyphens and digits.
   - Avoid unintended negative or misleading associations in the target languages and regions.
   - Scan concatenations for sensitive, adult, discriminatory, or offensive words formed accidentally.
   - Avoid names that clearly match an existing company or brand (lightweight public-web check).
   - Fit the intended audience and brand character; do not require an abstract name to describe the industry literally. For regulated industries such as medical or finance, flag suggestive or misleading wording rather than blanket-excluding every imaginative term.
   - Availability alone does not make a name worth recommending.

5. **Verify and curate.** Run `bulk_available` on the filtered candidates. Retain in the verified shortlist only candidates that meet the availability rule in Evidence discipline. From the explicitly available candidates, present only the 5 to 10 strongest. Preserve creative diversity in the shortlist rather than returning several versions of the same formula. If availability removes all strong non-literal directions, generate fresh candidates instead of filling the list with weak literal leftovers, within the verification budget below.

   **Verification budget.** Verify each round's candidates in one `bulk_available` call where the tool allows. Allow at most two more generation-and-verification rounds after the first, and stop earlier on a quota or rate-limit message. If fewer than five candidates qualify when the budget or quota runs out, present those that do, say why generation stopped (budget, quota, or no strong candidates left), and offer to continue later or in a different direction.

6. **Iterate by territory.** On feedback, generate fresh names within the preferred semantic distance, image, sound, or construction method. Do not merely swap prefixes. Use domain-name-advisor in taken-target mode if the user wants deleted, expired, aged, or other acquisition-path options.

## Output format

Present each shortlisted candidate with:

- **Domain**: the candidate.
- **Naming territory and semantic distance**: refined literal, suggestive, evocative, or symbolic / abstract.
- **Formation**: compound, modifier, blend, clipping, controlled respelling, coined, sound-led, or integrated TLD.
- **Creative concept**: the intended image, feeling, metaphor, attitude, or brand story, explicitly labeled as creative rationale.
- **Connection to the seed**: what literal constraint, meaning, sound, pattern, or valued feature it preserves.
- **Why it works**: memorability, pronunciation, spelling, rhythm, visual form, audience fit, and distinctiveness.
- **Availability at check time**: the per-domain `bulk_available` result that meets the availability rule, with observation timestamp.
- **Standard / premium status**: as the price rule in Evidence discipline defines it.
- **Registration and renewal price**: first-year and renewal price where available, with currency.
- **Provider and observation date**: the source of the price and when it was checked.
- **Language / brand caveat**: any cross-language meaning issue or possible brand collision noted.

If the availability tool fails or returns inconclusive, missing, or unrecognized results, you may offer the affected creative candidates only in a separate group labeled "Availability not verified", with the returned status or error. Never mix them into the verified shortlist.

## Key principles

- Treat the input as a hard literal constraint only when the user requires it; otherwise it is a creative seed. Roots, modifiers, metaphors, and sound readings are interpretations, not facts.
- Naming may be literal, suggestive, evocative, symbolic, or abstract; intentional openness is valid, accidental incoherence is not. Avoid template-driven cliches and availability-driven distortion.
- Generate many internally, filter hard, and present a small, creatively diverse verified shortlist within the verification budget.
- Label availability only as Evidence discipline defines it; inconclusive results stay in the separate unverified group.
- Weigh the TLD by audience, region, meaning, and renewal cost rather than defaulting to `.ai`, `.io`, or `.app`.
- Availability plus a public-web check is not trademark clearance.
