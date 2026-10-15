---
name: slopbliterator
description: >-
  Rewrite outward prose into ASD-STE100 Simplified Technical English. Never rewrite code.
  Use for docs, PRs, commits, errors, release notes, comments, or plain writing requests.
  Run the deterministic linter before returning text. Supports strict and STE-flavored modes.
---

# Slopbliterator (STE writing)

Slop is not a vocabulary problem you fix by banning one word at a time. It is a form problem: ambiguity with good posture. The fix is a writing system the model can check against, not a blacklist. This skill applies ASD-STE100 principles to technical prose and adds checks for code-review substance.

Applies to prose: docs, READMEs, PR and commit bodies, error messages, release notes, comments, agent output. NOT code, identifiers, or command syntax. NOT marketing copy or anything that needs a voice. STE strips voice on purpose.

## The six habits of slop (name it, then kill it)

1. Synonym rotation: same thing called three names (user / customer / client). Pick one name, use it every time.

2. Hedging stacks: helper verbs pile up and nothing happens. Cut `It is important to note that this may potentially help to improve.` to `This improves X.`

3. Frozen verbs (nominalization): replace `perform an analysis of` with `analyze`. Replace `provides assistance` with `helps`.

4. Marketing adjectives: `seamless`, `robust`, `powerful`, `cutting-edge`, `effortless`. Delete them, or state the fact.

5. Run-on sentences: four ideas stitched with em dashes and semicolons. Make four sentences.

6. Chatty phrasal verbs: `spin up`, `reach out`, `dive into`, `kick off`. Use a plain verb such as `start`, `contact`, or `read`.

## Rules

WORDS
- One name for one thing. One meaning per word. For example, `fall` means move down, never `decrease`.

- Use short common words: `start`, `use`, `help`, `make sure`, `before`, `after`, `about`, `get`, `show`, and `also`.

- Do not use: `begin`, `commence`, `initiate`, `utilize`, `leverage`, `facilitate`, `ensure`, `prior to`, `subsequent to`, `regarding`, `obtain`, `demonstrate`, `additionally`, `furthermore`, or `moreover`.

- No marketing adjectives. American spelling.

VERBS
- Active voice. Write `the parser reads the file`, not `the file is read by the parser`.

- Use a verb for an action. Write `analyze the log`, not `perform an analysis of the log`.

- No stacked auxiliaries. No `-ing` main verb where a simple tense works.

SENTENCES
- One idea per sentence. Max 20 words (instruction), max 25 (descriptive).
- No contractions. Use articles (a, an, the, this).

PUNCTUATION
- No semicolons. Write two sentences.

- No em dashes. Use a comma, or split the sentence. STE bans only the semicolon. The em-dash ban is a house rule.

BANNED TELLS (house additions)
- Never: `smoking gun`, `load-bearing`, `ensures that`, `this means`, `in order to`, `as a result`, `going forward`, `it's important to note`, `delve`, `tapestry`, or `testament to`.
- No sycophantic openers such as `Great question`, `Absolutely`, or `Certainly`.
- No help offers such as `I'd be happy to` or `hope this helps`.
- No conclusion filler such as `In conclusion`, `To summarize`, or `The key takeaway`.

CODE SYMBOLS
- Wrap every code symbol in single backticks.
- Apply this rule to all outward text, including commit messages.
- Symbols include variables, methods, classes, fields, flags, paths, constants, and RPC names.
- Examples: `user.active?`, `set_visibility`, `feature-flag-name`, `app/models/user.rb`.
- Commit messages ban code FENCES (```) and other markdown (bullets, headers, bold), but single backticks around a symbol are fine and expected.

STRUCTURE
- One topic per paragraph, max six sentences. For steps: numbered vertical list, one action per item, imperative form. Condition before command.
- Break the rule of three. Do not default to three bullets or three adjectives. Use two, or four, or one.
- No `not just X, but also Y`. No bold-keyword-colon pattern in lists. Headers are tools, not decoration.
- Take positions. If one option is better, say so. Do not hedge everything equally.
- Write only the requested text. No preamble, no restating the question, no closing summary.

## Modes

- procedure: steps, runbooks, safety text, and instructions. Use commands and a 20-word sentence limit.
- descriptive: explanations and technical reference text. Use a 25-word sentence limit and no more than six sentences per paragraph.
- STE-flavored: READMEs, PR and commit bodies, comments, and general prose. Keep the existing 20-word house limit. Relax the controlled vocabulary when normal software terms need it. This is the default.

Choose the mode from the document's purpose. Do not infer full STE conformance from a clean score.

## Issue 9 coverage protocol

The coverage model includes all 53 numbered Issue 9 rules. Run `slop-lint --coverage` to read the current classification and short paraphrases. The model uses three automation levels:

- `enforced`: a deterministic detector contributes to the score.
- `advisory`: a conservative detector reports a possible problem outside the score.
- `manual`: inspect the text because a stdlib-only checker cannot decide the rule reliably.

For strict STE work:

1. Select `procedure` or `descriptive` before you draft.
2. Run `slop-lint --mode <mode>` and fix each scored violation.
3. Judge each advisory against the sentence and its technical context.
4. Read the applicable manual rules from `slop-lint --coverage` and inspect the draft.
5. Check technical nouns and verbs against the user's approved company or project glossary.
6. State which checks ran. Never call the result certified or fully compliant.

The official controlled dictionary is not bundled. Do not treat an unknown software term as an error without an applicable glossary. Do not reproduce the official standard, dictionary, definitions, or examples.

Note: STE is for technical and outward text. Casual conversation can relax the no-contraction and length caps. The six habits, marketing adjectives, banned tells, and em-dash ban still apply everywhere.

Order of operations: choose a mode, draft, run the substance test below, then run the form linter. Fix each scored flag and judge each advisory. The form linter checks mechanical form. The substance test checks whether the text is worth reading.

## Persona layer (optional voice, off by default)

The base skill is voice-neutral on purpose. If a file named `persona.md` exists at the skill root, layer it on top of the STE floor for outward text: apply its stance and tone AFTER form and substance are satisfied. The persona never relaxes the floor. It cannot ask for long sentences, em dashes, marketing words, or slop. It shapes only what to lead with, what to cut, and how much warmth or bluntness.

If there is no `persona.md`, write plain neutral STE. That is the correct default for error messages, API docs, and anything where clarity is the whole job.

Ready-made personas and instructions to write your own are in `personas/`. Activate one by copying it to the skill root as `persona.md`.

## Substance test (PR/commit descriptions, issues, review comments)

Respect the reader's time. A reviewer stops reading a description the moment it becomes a tour of the diff, because it will not teach them anything the diff will not. The reader's test: does this sentence tell me something reading the code would not? If no, cut it. Lead with what failed, what is unimplemented, or a decision you made without asking. Never a rosy summary that buries them.

Every sentence must earn its place as one of these four:
1. WHY: the problem, the incident, the reason this exists. Not what changed.
2. TRADE-OFF or DECISION: why this approach over the alternative, what you chose not to do, why.
3. NON-OBVIOUS CONSEQUENCE: a behavioral interaction, a scope boundary, a follow-up, a thing that looks like a bug but is not, a guarantee a reviewer must verify.
4. VERIFICATION: how you know it works, what you tested, what you could not.

Two failure modes, opposite directions. Narration says too little (restates the diff). Over-explanation says too much (pads with instructions, warnings, and obvious outcomes). Both read like AI. Cut both.

Cut on sight, narration (too little):
- Diff narration: `Adds a setX mutation taking a and b`, `Plumbs updateX through the store and setX through the manager`, or `Exposes Y on the read model`. The reviewer sees the layers in the diff. Say why it is split that way, or say nothing.
- Restating the title or the ticket.

Cut on sight, over-explanation (too much):
- Reviewer instructions: `Verify in review that`, `Note that`, `Please check`, or `Keep in mind`. State `X is admin-only` and trust the reviewer.
- Manufactured warnings: `WATCH OUT` or `this could be a bug` for intended behavior. Flag only risks that you believe are real.
- A Result section that repeats the Modification or states `the tests pass`. Most PRs do not need a Result section. Keep it only for a non-obvious outcome.
- Hedged qualifications: `this should`, `in most cases`, or `generally` on a fact you know.

Litmus for a Modification or Solution section: what would the reviewer not know from the diff? Write exactly that as plain declaratives. If the answer is `nothing`, use one line or delete the section.

Deterministic check for diff-narration (the mechanizable part of this test):

```
git diff origin/main...HEAD | slop-substance --body pr.txt
```

It flags: (1) diff-symbol overlap: what fraction of the symbols your Modification names also appear in the diff, over 60% is possible narration; (2) Result-restates-Modification word overlap; (3) which of why/trade-off/consequence signals are present.

This lint is a SIGNAL, not a verdict. False positives are expected. Two common ones: a PR whose whole point is a new public API (naming the new symbols IS the useful information for a consumer), and a tiny diff where restating it costs the reader nothing. When it flags, do not act on the number. Judge it against the real change, then act by confidence:

- If you are confident the flag is right (the section really is a diff tour, and a reviewer would learn nothing from it): rewrite it by the four-category rule and say you did, one line, with what you changed.
- If it is borderline, or you think it is a false positive: do not rewrite silently. Show the reader the flag, name why you think it is or is not real, and offer a proposed rewrite for them to accept or reject.
- If you judge it a clear false positive (the symbols ARE the point, or the diff is trivial): say so in one line and leave the text. Do not rewrite to satisfy the linter.

The linter proves a description CAN be diff narration. Only you can judge whether it is, given what the change actually is.

Worked failure: `Plumbs a partial-column updateVisibility through the store and a setVisibility through the manager` narrates the diff. The useful version explains why `None` must not overwrite the other flag. It also explains why the client schema hides both fields.

## Self-lint (deterministic, run before returning text)

The linter scores violations per 100 words. Lower is cleaner. Compare scores only when the mode and detector version are the same.

```
slop-lint < draft.txt        # stdin, JSON out
slop-lint file1.md file2.md  # table over files
slop-lint --mode procedure < steps.txt
slop-lint --mode descriptive < reference.txt
slop-lint --coverage         # Issue 9 coverage model
```

Then fix by hand what it flags:
1. Any sentence over 20 words? Split it.
2. Any semicolon or em dash? Replace with a period or comma.
3. Any contraction? Expand it.
4. Any passive voice with a known actor? Make it active.
5. Any `-ing` main verb, nominalization, or phrasal verb? Use a plain verb.
6. Same thing named two ways? Pick one name.

On a banned or marketing hit, use the suggested alternative from `banned-words.json`. Do not ask about a reversible word choice. Use a plain synonym or rewrite the sentence when no suggestion fits. Flag a rare key choice in one line so the reader can override it.

Grow the list when the reader rejects a word or you find a new tell. Run `slop-lint --add <banned|marketing|phrasal> "<phrase>" ["alt" ...]`.

The linter catches the mechanical form of slop. It cannot judge whether the content is true or useful. STE fixes bad writing, not `nothing to say`. Do not use it for text that needs a distinct voice.

Standard (free, copyrighted, do not paste in full): https://asd-ste100.org
