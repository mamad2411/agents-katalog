---
name: scrutinize
description: Argument-level scrutiny of one proof, section or statement — the claims with their asserted status, the inference gaps told apart as a missing result or a missing method, the load-bearing steps and the most appealing claim read hardest, the conditions made visible, and a class claim kept apart from an instance claim; a numbered list of findings, the target edited by nothing, after which each sentence found false of the artifact is corrected. Checking, not verification, it certifies nothing. Use as `/research:scrutinize TARGET` (`/research:scrutinize the second lemma`), and before a section is reviewed whole or leans on a result for the first time. The project's instructions file names its conventions; this skill names none of them. When the person says 'scrutinize' or 'does this argument hold', they mean this skill — call it every time, even if it ran earlier in the session, and take every step.
license: Apache-2.0
compatibility: No tooling; reads the target and what it invokes.
metadata:
  version: "0.12.1"
---

# Scrutiny

Scrutiny is checking, not verification: a first-pass reader flags what looks wrong, unsupported or mislabelled and certifies nothing, and the report says so.
A machine-checked proof is what validates an argument in the strong sense, and it is out of this skill's scope.

## The project's part

The setup (`/research:research-init`) forms with the person the conventions an argument is held to and writes them under a `### Reviews` heading of the instructions file, inside its `## Records and method` section: how a regime condition is written, which objects form an abstract class and which are its instances, the status labels the project uses; which documents a review may correct in the session, and which it reports and asks the person about first; scrutiny reads them there.
Where the instructions file has no such part, or it does not say what this review needs, the review says so and advises `/research:research-init`, which forms it with the person in a project set up before as well; where only this review's part is missing and a full setup is not needed, it asks the person for that part in place and, on their word, writes it where the setup would.
The target is what the person names with the command; read it whole, and every section, lemma or assumption it invokes, opened, never recalled.

## The steps

1. **The claims.**
   Every non-trivial claim of the target with its asserted status: proved here, proved elsewhere (where), assumed, conditional on a named hypothesis, open.
   Flag a status that looks wrong: stated as proved while resting on an unproved step, or stated more strongly than the argument supports; a condition is preserved, never dropped.
2. **The inference gaps.**
   Each step whose conclusion does not plainly follow from its stated premises, and which kind it is: a missing result (a step that may be true and is not shown) or a missing method (something the present apparatus cannot express).
3. **The load-bearing steps.**
   The one to three steps the rest depends on most, and the most elegant or appealing claim, are read hardest, since being indispensable and being appealing are both reasons for more doubt; for each, what breaks if it fails.
4. **The conditions.**
   Every assumption named and visible, none buried in a proof or a footnote, and each regime condition written as the project writes it, with its constants.
5. **Class and instance.**
   A claim about an abstract class that uses a fact about one instance, or the reverse, is flagged; each sentence says which it makes.
6. **The report, the target edited by nothing.**
   A numbered list the person can act on, with the caveat that this is checking; an uncertain gap is marked "uncertain: needs the person's judgment", never guessed either way.
7. **Then the corrections.**
   After the report, a sentence found false of the artifact is corrected in this session at its own size, and reaches every summary site that restates it; a document the project's part names as one a review reports and asks about first gets the sentence, its evidence and the correction put to the person instead.
   A gap is not a false sentence: what to do about one is the person's, put as a question with a recommendation or captured on their word (`flow idea` of the gap where the project runs the flow, then a question minted from that idea, `flow question … --ref IDEA`, where the gap is sharp enough to say what would answer it).

**Output.** The caveat, the numbered findings, the corrections made, and what was asked or captured.
