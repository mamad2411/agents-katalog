---
name: write-skill
description: >
  Guides the authoring of a new Claude Code skill (SKILL.md) from a domain
  description to a shippable file, applying structural patterns and
  research-grounded quality checks at each step. Use when starting a skill
  from scratch given a domain or problem statement. Do NOT use to evaluate
  an existing skill — see assess-skill for that.
---

# Write Skill

## Prerequisites

- A domain or problem statement: what recurring task should this skill handle?
- At least one real example of the task being done correctly (even informally described)
- Knowledge of any neighbor skills that handle adjacent concerns (name them if known)

## Instructions

### Step 1 — Define Scope Before Writing Anything

1. Ask: what is the single concern this skill owns? Write it in one sentence starting with a verb: "This skill [verb]s [specific thing] when [specific moment]."
2. Name two neighbor skills — adjacent concerns this skill does NOT cover. If you can't name neighbors, the scope is probably too broad or not yet understood.
3. Apply the decomposition tests before proceeding:
   - One trigger: is there one specific moment or context that activates this skill and nothing else?
   - One boundary: can you draw a clear line where this skill stops and a neighbor begins?
   - Independence: could this skill's output be verified without running any other skill?
   - 500-line fit: will the content fit in 500 lines without cutting essential procedures?
   If any test fails, split the scope further before continuing. (Source: *Atomic Skills*, arXiv 2604.05013 — atomic decomposition produces 18.7% better generalization than composite skills; SkillsBench, arXiv 2602.12670 — focused 2–3 module skills outperform comprehensive documentation.)

### Step 2 — Write the Description

4. Draft the description using the trigger contract formula:
   ```
   [What it does, third person, imperative framing].
   Use when [specific trigger condition — name the moment, artifact, or signal].
   Do NOT use when [exclusion condition — name the neighbor skill if one exists].
   ```
5. Check voice: no "I", "you", or "we". The description is injected into a system prompt and read by the system as context about the skill, not by a human.
6. Apply the retrieval test: strip the skill name. Does the description alone uniquely identify what this skill does? Could this description belong to a different skill without changing meaning? If yes, add more specificity to the trigger condition. (Source: *Skills in the Wild*, arXiv 2604.04323 — description quality is the primary retrieval signal; vague descriptions collapse pass rates from 55.4% to 19.8%.)
7. Keep the description to ≤ 3 sentences. Density matters more than length.
8. Write the `name` field: `action-noun`, lowercase, hyphens. The name is the first retrieval key — make it specific enough to be unambiguous.

### Step 3 — Draft the Instructions

9. Before writing directives, list everything the agent must do to complete the task. Do not filter yet — produce the full inventory.
10. Group the inventory into logical phases or concerns if there are more than 8 items. Each group becomes a subheading.
11. Convert each item to a directive by applying the three tests:
    - **Imperative test:** Does it start with a command verb? Rewrite "It's important to..." → the verb that follows it.
    - **Observable test:** Can output be checked against this directive? Rewrite "Handle X appropriately" → "For X: [specific action] + [specific output]."
    - **Domain-specific test:** Would this directive appear unchanged in a skill for a different domain? If yes, cut it — the agent already knows general best practices. Only write what is specific to this domain, workflow, or team convention. (Source: Hamelsmu meta-skill — "Cut general knowledge. Only include domain-specific procedures agents wouldn't know.")
12. Number the directives if order matters. Use bullets if they are independent checks.
13. Do not write motivation sentences — sentences that explain why a directive exists. Delete any sentence starting with "This is important because", "The reason we", or "To ensure". The directive alone is sufficient. (Source: ACE, ICLR 2026 — motivation sentences are the first content lost to brevity bias, and their absence makes no difference to agent behavior.)

### Step 4 — Write Anti-Patterns

14. List the 3–5 most common mistakes in this domain — things the agent might plausibly do that would be wrong.
15. Write each as a one-liner. No explanation. No "because". A scannable ❌ signal is all that's needed:
    ```
    ❌ [The wrong thing, described specifically enough to be unambiguous]
    ```
16. If an anti-pattern requires explanation to be understood, it's either too abstract or a Gotcha — move it to the Gotchas section with its explanation.

### Step 5 — Write Gotchas

17. List the non-obvious failure modes — mistakes that experienced practitioners make, not just beginners. These are the domain-specific heuristics that don't survive compression.
18. Write each as a sentence or two that names the failure mode, the condition that triggers it, and the correct response.
19. Verify specificity: each Gotcha must name something that would only be known from real experience in this domain. Generic Gotchas ("edge cases may arise", "inputs may vary") provide no value and must be replaced. (Source: ACE, ICLR 2026 — "brevity bias" collapses domain-specific heuristics into generic summaries, reducing skill effectiveness to baseline.)
20. Aim for 2–4 Gotchas. More than 5 usually means the skill is too broad.

### Step 6 — Write the Verify Section

21. List 3–5 observable checks the agent can perform after completing the task to confirm success.
22. Each check must be verifiable from output — not a judgment call. Test each item: "could two different agents independently reach the same pass/fail verdict?" If no, rewrite.
23. The verify items collectively must confirm the skill's stated purpose was achieved — not just that steps were followed.
24. Frame as checkboxes:
    ```
    - [ ] [Observable state that confirms success]
    ```
    (Source: Karpathy goal-driven execution pattern; Obra pre-PR checklist; SkillNet executability dimension.)

### Step 7 — Write Examples (strongly recommended)

25. Write at least one Before/After example showing the task in the wrong state and the correct state after following the skill's instructions.
26. Use concrete, specific examples — not placeholders. A real diff fragment, a real function signature, a real prompt/response pair. Abstract examples teach nothing.
27. If examples grow long (> 60 lines), move them to `EXAMPLES.md` in the same folder and reference the file from SKILL.md.

### Step 8 — Quality Gate Before Shipping

28. Check total line count. If over 500 lines, identify the overflow section and move it to `references/` or split the skill. Never compress — compression destroys domain-specific content. (Source: ACE — context collapse: a 18,282-token context compressed to 122 tokens dropped accuracy below the no-context baseline.)
29. Run the SkillNet 5-dimension check (arXiv 2603.04448):
    - **Safety:** Any instruction that could cause destructive or irreversible action must have a guard.
    - **Completeness:** All steps needed to finish the task are present; no gaps requiring domain knowledge not in the skill.
    - **Executability:** Every referenced file, tool, or setup step is either defined in Prerequisites or universally available.
    - **Maintainability:** Section headers are present; one section can be updated without reworking others.
    - **Cost-awareness:** Scope is proportionate to the task; no expensive operations called for simple tasks.
30. Run the human authorship check: look at Gotchas and Anti-Patterns. Did these come from real experience with the domain? If an LLM generated them without domain-expert input, they will be generic and provide no skill benefit. Replace generic entries with specific ones before shipping. (Source: SkillsBench, arXiv 2602.12670 — self-generated skills provide zero benefit on average across 7,308 benchmark trajectories.)
31. Final structure check — verify all required sections are present:
    - [ ] Frontmatter with `name` and `description`
    - [ ] Instructions (required)
    - [ ] Anti-Patterns (minimum 3)
    - [ ] Verify (minimum 3 observable checks)

## Anti-Patterns

❌ Writing the description last — description defines scope and must come before instructions  
❌ Starting instructions before Step 1's scope definition is complete — produces composite skills  
❌ Writing motivation sentences in Instructions ("This matters because...", "The reason we do this is...")  
❌ Asking an LLM to generate the Gotchas section without supplying domain knowledge — produces generic entries with zero benefit  
❌ Compressing the skill when it hits the 500-line ceiling instead of splitting — destroys domain-specific content  
❌ Using "should", "try to", "aim to" in directives — all directives must be imperative, not advisory  
❌ Combining two trigger moments in one skill ("use when writing or reviewing code") — one trigger per skill  
❌ Writing a Verify section with judgment-call items ("output is clear", "code looks correct")

## Gotchas

- The description formula (what + when + not when) can be structurally complete but still fail the retrieval test — specificity and structure are independent checks; run both
- Scope violations most often appear in Step 3 when the instruction inventory grows past 10 items and covers two distinct trigger moments — stop and split before converting to directives
- The domain-specific test (Step 3, step 11) is the hardest to apply to your own skill because you know the domain — test by asking: would an agent working in a different industry follow this directive identically? If yes, cut it
- A Gotchas section written before real usage is speculation, not accumulated knowledge — it's acceptable to ship with 1–2 Gotchas and add more as actual failures are encountered; this is preferable to generic placeholder Gotchas
- Executability failures are invisible to the author — read the Prerequisites section as someone who only has this file and no other context about the environment

## Verify

- [ ] Scope definition (Step 1) was completed before any other section was written
- [ ] Description passes both the formula check and the retrieval test
- [ ] Every directive in Instructions is imperative, observable, and domain-specific
- [ ] Anti-Patterns are one-liners (no multi-sentence entries)
- [ ] Gotchas contain named, specific failure modes — not generic warnings
- [ ] Verify section has ≥ 3 items, each verifiable from output without a judgment call
- [ ] Total line count is under 500
- [ ] SkillNet executability check passed: no broken references in Prerequisites or Instructions
