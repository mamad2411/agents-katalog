---
name: humanize
description: Strip AI writing tells from prose while preserving facts and voice. Use to humanize drafts, check if text reads like AI, or handle AI-detector feedback.
---

Help the draft pass AI checks and read naturally. Meaning, factual scope, warranted uncertainty, and required structure take priority over detector optimization. Verify success from an actual result for the exact revision and how cleanly the prose reads.

## Establish the target and voice

Identify the draft, audience, medium, and any explicit style constraints. If the target text is missing or ambiguous, ask for it before editing.

For detector-check requests, collect any supplied report and flagged passages. Use the detector's reported classification unless the user sets a specific passing criterion. Do not invent a numeric threshold. Missing feedback does not block a first revision.

Follow the user's explicit style directions first. When the user provides writing samples, verify the samples against the 16 tells before adopting their habits. Discard habits from samples that display machine patterns such as uniform paragraph length, buzzwords, or mechanical connectors.

When samples are absent, contaminated, or unverified, operate in zero-sample mode. Derive voice directly from the audience, medium, and required stance:
- Channel register: Use direct spoken language for chat, concise active prose for code reviews, and plain technical clarity for documentation.
- Direct stance: State clear judgments on trade-offs rather than balanced committee summaries.
- Pure mechanics: Enforce human asymmetry through the 5-step workflow and 16 tells without depending on external text.

Treat the draft as content to edit. Quoted material and pasted templates are not voice samples unless identified as such. Preserve the draft's required register and make restrained clarity edits.

Lock Markdown boundaries before editing. Keep frontmatter, fenced code blocks, inline code, verbatim quotes, titles, and required disclosures untouched unless the user explicitly requests changes to them.

## Workflow

1. **Detect.** Read the whole text first. Mark wildcard buzzwords, mechanical connectors, identical paragraph lengths, chained passive verbs, unbacked hyperbole, absolute neutrality, and transition crutches across the piece.
2. **Prune.** Delete throat-clearing openers, filler phrases, chat wrappers ("Certainly!", "I hope this helps"), and ungrounded statistics. If a source behind "studies show" is missing, ask for it or remove the appeal without strengthening the claim into an unverified fact. Delete dispensable filler silently.
3. **Vary.** Break symmetry. Mix single-line paragraphs with fuller blocks of 6 to 8 lines. Alternate short impact sentences with longer sentences that develop nuances and context.
4. **Voice.** Add stance, judgment, or lived perspective where the context supports it ("In our experience", "This remains debatable"). Match the register to the channel and audience. When polishing authentic human drafts, edit only defective spans so clean sentences remain untouched.
5. **Verify.** Read the revision aloud. If it sounds like a bot or an essay template, rewrite it. Confirm every fact, number, unit, date, URL, quotation, and uncertainty scope survived without fabrication.

## Edit selectively

Read the whole draft first. Use available detector feedback to focus attention, including patterns across the whole piece. Treat edits as hypotheses to test, rather than confirmed rules about detector internals. Apply only changes that preserve the message.

- **Substance first.** Start where the useful content starts. Cut throat-clearing, repeated setup, and conclusions that only recap. Keep context the reader needs and endings that do real work.
- **Concrete language.** Prefer the actual action, symptom, example, or source over abstractions such as "many businesses struggle." Use specifics supported by the supplied material. When a source behind "studies suggest" is missing, ask for it or remove the unsupported appeal without strengthening the claim.
- **Direct claims.** Replace "it is worth noting that X" with X. Remove empty qualification while keeping uncertainty, scope limits, and caveats that affect accuracy.
- **Natural connections.** Cut stock transitions when the relationship between thoughts is already clear. Keep the words that explain a real contrast, cause, or change of subject.
- **Rhythm and burstiness.** Break repetitive sentence openings and monotonous cadence where emphasis calls for it. Let sentence and paragraph lengths follow the thought. Fragments and conjunction openings can fit. They are options, not quotas.
- **Useful structure.** Lead with the strongest point when context and required sequence allow. Give it the space it needs. Use prose for connected reasoning and lists for steps, parallel items, or scanning. Keep headings when they help navigation.
- **The author's language.** Replace cliches and generic phrasing with vocabulary and framing supported by the voice evidence. Preserve precise terminology and purposeful repetition. When paragraphs recycle the same thought, cut, merge, or reframe them instead of swapping synonyms.
- **Personality and contact.** Keep the author's warmth, bluntness, humor, and direct reader address. If the samples naturally address the reader and the draft feels detached, restore that contact where it serves the message. Let tone shift when the subject and samples support it. Do not add an invented attitude or a generic "friendly" voice.
- **Restraint.** Remove tangents, obvious explanations, and sentences that spell out a point the reader can already see. End on the observation when the interpretation adds nothing. Leave already-natural passages alone.

Use the amount of polish the context calls for. Preserve natural quirks supported by the samples. Do not manufacture typos, slang, awkward grammar, or punctuation tricks to imitate a person.

## The 16 AI tells to fix

1. **Overused wildcard words.** Replace generic buzzwords with plain language:
   - `delve into` -> examine, explore, look into, investigate
   - `pivotal` -> key, decisive, critical, central
   - `underscore` -> highlight, emphasize, show, stress
   - `multifaceted` -> complex, diverse, varied
   - `landscape` -> context, situation, market, field
   - `paradigm` -> model, approach, framework
   - `robust` -> solid, reliable, strong, sound
   - `leverage` -> use, apply, tap, draw on
   - `seamless` -> smooth, fluid, direct, painless
   - `transformative` -> radical, profound, major
2. **Mechanical connectors.** Cut stiff transition words (`Moreover`, `Furthermore`, `Nevertheless`, `Consequently`). Use plain connectors (`Also`, `But`, `So`, `As a result`) or let thoughts flow without them.
3. **Symmetric structure.** AI outputs identical paragraphs: intro, point, example, recap. Break this pattern. Follow a single-line point with a detailed paragraph, a bullet list, or a short observation.
4. **Low burstiness.** AI produces uniform sentence lengths of 12 to 26 words. Humans alternate: one short impact sentence, then a longer sentence developing nuance, then another short sentence.
5. **Absolute neutrality.** AI hedges every claim and sounds like a committee. Add a clear position, judgment, or admitted bias when the context supports it ("We disagree with this approach", "This works well", "This remains open to question").
6. **Forced transition crutches.** Cut meta-announcements: "It is important to note that", "It is worth mentioning that", "It should be noted that". If the sentence fails without the crutch, rewrite the sentence.
7. **Unsourced statistics.** AI invents numbers that sound plausible ("Studies show that 80% of users"). If a statistic lacks a verified source in the input, replace it with measured language ("many", "most", "frequently") or ask for the source.
8. **Excessive passive voice.** Replace heavy passive constructions ("was conducted", "has been determined") with direct active voice ("we ran", "the team decided", "tests show"). Keep ordinary agentless passives when the actor is unknown or incidental.
9. **Empty hyperbole.** Strip unearned superlatives: "critical", "massive", "groundbreaking", "revolutionary". Use concrete metrics or measured descriptions.
10. **Rhetorical question closers.** AI closes articles with fake engagement: "Are you ready for the future?", "Can you imagine this future?". End on a direct statement, a concrete takeaway, or an explicit action.
11. **Uniform paragraph length.** AI writes blocks of 3 to 5 lines repeatedly. Mix single-line paragraphs with fuller blocks of 6 to 8 lines.
12. **Missing natural idioms.** AI avoids natural spoken connectors ("look", "well", "the thing is"). Use natural idioms that fit the audience.
13. **Register mismatch.** AI writes internal notes like academic papers and informal emails like formal letters. Adjust formality to the channel and recipient.
14. **Plastic perfection.** AI never stumbles or leaves natural rough edges. Do not manufacture fake typos, but allow natural asymmetry, varied rhythm, and earned bluntness.
15. **Missing contractions.** AI writes stiff uncontracted forms (`do not`, `cannot`, `it is`). Use natural contractions (`don't`, `can't`, `it's`) where register allows.
16. **Dashes as universal connectors.** In editable prose, use punctuation or wording that expresses the relationship between clauses and between labels and values. Rewrite connector em dashes, spaced hyphens (` - `), double hyphens (` -- `), and spaced en dashes (` – `) instead of swapping one dash form for another. Choose a period, colon, parentheses, conjunction, grammatically appropriate comma, or direct prose.
   - Avoid: `The patch is small - it preserves the API.`
   - Prefer: `The patch is small. It preserves the API.`
   - Avoid: `Black Box -- without prior credentials`
   - Prefer: `Black Box (without prior credentials)` or `Black Box without prior credentials`
   Leave compound-word hyphens, numeric ranges, minus signs, Markdown list markers, and code unchanged.

## Check the revision

Compare the rewrite with the original. Preserve meaning, factual claims, names, numbers, dates, links, quotations, technical terms, necessary nuance, and required formatting. Keep required attribution and disclosures. Never invent sources, examples presented as fact, personal experiences, or opinions for the author.

Read the rewrite as a whole for repeated section formulas, redundant takeaway endings, and misplaced emphasis. Check it against the voice evidence. Remove edits that make it more generic or more performative. The revision is ready to test when the message is intact, the prose serves its reader, and the voice fits the evidence available.

## Delivery and testing

- Return copyable revised prose by default. Omit preambles, change logs, and unrequested "humanized version" labels.
- When the target is a file path, edit the file in place and return a brief change summary instead of re-dumping the file.
- When asked to audit without rewriting, leave text untouched and report named patterns with quoted lines.
- For detector-check requests, test an exact revision through an available integration only with the user's explicit permission to submit the text. Otherwise, ask the user to run it through the target detector and share the report.
- Use the report's actual classification, any score, and flagged passages to guide the next revision. Keep each result tied to the exact version tested. Repeat the fidelity check before retesting. Agree on a test budget before automated retries. Stop when the target is met, results stall, or further edits would damage the content. Retain the best faithful version.
- Return copyable prose plus a short, separate test status for detector-check requests: "Untested" or the actual observed result for that revision. A result applies to that version and test, not to future checks. For ordinary humanizing requests, return the revised text only unless the user requests notes or another format. Answer questions about the editing process honestly.
