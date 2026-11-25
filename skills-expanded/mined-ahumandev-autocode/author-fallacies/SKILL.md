---
name: author-fallacies
description: Use this skill when confirm/refute claims (arguments/rebutals) to detect fallacious reasoning in articles, debates, and discussions.
---

# How To Check Claims

For each argument:

1. Identify claim (direct or implied): Scan claim-by-claim, not sentence-by-sentence.
2. Test evidence is valid and complete in context of claim, if not: claim is weak (unproven)
    * Never invent facts, sources, intent, magnitudes, or counterexamples.
    * Use supplied document/context only; never retrieve external facts or sources.
3. Test context (claim implying different meaning of original authored message).
4. Detect Fallacies (compare each Fallacy): Fallacy detected? claim is refuted
5. Label only positive fallacy detections. Never force a label. Allow zero candidates.

## Modes

Infer requested mode: `detect`, `refute`, or `rewrite`; unclear request defaults to all three.

For every candidate, provide exact quote, label, Pattern match, Confirm evidence, confidence `high|medium|low`, concise refutation, and corrected rewrite.

Rewrite preserves defensible intent, removes invalid inference, marks unsupported claims `[support needed]`, and never invents evidence. A fallacy never proves its conclusion false. Zero candidates is valid. Rewrite mode returns one coherent revised passage, not isolated replacements.

## Fallacies

Each entry gives **Label**: Pattern; Confirm; Guard.

* Pattern = premise-to-conclusion move.
* Confirm = supplied-text check before assigning label.
* Guard = common valid lookalike; omit unless needed.

Use most specific confirmed label; use `Non sequitur` only when no specific mechanism fits.

### 1. Formal deduction

For categorical tests: `All A are B` distributes A only; `No A are B` distributes both; `Some A are B` distributes neither; `Some A are not B` distributes B only.

* **Affirming the consequent** — **Pattern:** `If P, then Q; Q; therefore P`. **Confirm:** quote all three moves; test whether Q can be true while P is false, and find no stated `Q -> P`, `P iff Q`, or separate P evidence. **Guard:** a stated biconditional or independent proof establishes P.
* **Denying the antecedent** — **Pattern:** `If P, then Q; not-P; therefore not-Q`. **Confirm:** quote `not-P` and `not-Q`; the argument gives no necessity claim `Q -> P` or `P iff Q`. **Guard:** `P iff Q`; valid modus tollens instead has `not-Q; therefore not-P`.
* **Undistributed middle** — **Pattern:** `All A are B; All C are B; therefore All C are A`. **Confirm:** mark B in both premises: neither premise covers every B, so overlap in B does not place every C inside A. This differs from a valid syllogism with B distributed at least once.
* **Illicit major term / illicit minor term** — **Pattern:** a conclusion distributes major B or minor A after its matching premise leaves that term undistributed. **Confirm:** mark every member claimed in conclusion, then compare matching premise; it covered only part of that term. This is term-scope expansion, not an undistributed middle.
* **Non sequitur** — **Pattern:** premises X; therefore Y, with no stated rule, definition, or evidence bridge from X to Y. **Confirm:** build a countermodel where every supplied premise holds and Y fails; use this fallback only after no named mechanism above fits.

### 2. Ambiguity and language

* **Equivocation** — **Pattern:** premise uses expression T as T1; conclusion uses T as T2. **Confirm:** quote each T occurrence and state two context-fixed meanings, such as legal `right` versus moral `right`; the conclusion needs T2 after premise supplied only T1.
* **Amphiboly** — **Pattern:** grammatical span S permits parse P1; conclusion follows parse P2. **Confirm:** quote S and write both grammatical attachments or referents; show premise support depends on P1 while conclusion takes P2. This differs from equivocation because one sentence's syntax, not word sense, shifts.
* **Accent / context shift** — **Pattern:** qualified statement Q is quoted or stressed as broader Q'. **Confirm:** compare exact quote with supplied adjacent words; identify omitted condition, time, exception, or emphasis that changes Q into Q'. Do not infer missing context.
* **Scope ambiguity** — **Pattern:** operator span S has scope S1 in premise and S2 in conclusion, such as `not all` versus `all not`. **Confirm:** quote quantifier, negation, or modal and write both readings; conclusion requires different scope. This differs from amphiboly when operator scope, not attachment, changes.

### 3. Presumption and burden

* **Begging the question** — **Pattern:** premise P' restates conclusion P under renamed or synonymous wording; therefore P. **Confirm:** normalize P' and P into the same proposition, then remove P'; no independent premise remains. This is direct assumption, not a multi-step dependency loop.
* **Circular reasoning** — **Pattern:** A supports B, B supports C, and C supports A. **Confirm:** trace each stated support edge back to its source; every route returns to loop and no premise has support outside it. This differs from begging the question because conclusion is not merely repeated in one premise.
* **Presumption** — **Pattern:** unstated or disputed P is treated as settled premise; therefore conclusion needing P. **Confirm:** quote P and conclusion; conclusion depends on unstated/disputed P and fails without it; text neither establishes nor stipulates P. Lack of proof alone is not this label unless P is used as fact.
* **Loaded question / complex question** — **Pattern:** answer yes/no to question Q entails embedded accusation or premise P. **Confirm:** write both direct answers and show each concedes P; identify P in exact question text. **Guard:** Q explicitly permits denying P, or supplied context already establishes P.
* **False dilemma / forced choice** — **Pattern:** `A or B; not-A; therefore B`, while live option C is omitted. **Confirm:** quote claimed exhaustive A/B choice; name C that fits domain yet is excluded. Option overlap alone is not decisive. **Guard:** domain is expressly exhaustive, including bivalent `P or not-P`; law of excluded middle itself is not a fallacy.
* **Shifting burden of proof** — **Pattern:** claimant asserts P; critic cannot disprove P; therefore P is accepted. **Confirm:** identify P's claimant and critic, then quote failure to disprove as P's sole support. **Guard:** critic advances separate positive Q; critic then owes support for Q, not disproof of P.
* **Appeal to ignorance** — **Pattern:** no evidence for P; therefore not-P, or no evidence against P; therefore P. **Confirm:** quote absence claim and truth conclusion; absence, rather than a stated sensitive search or provisional confidence judgment, performs inferential work. **Guard:** stated adequate search would detect P if P held; absence then supports not-P.
* **Appeal from incredulity** — **Pattern:** speaker cannot imagine, understand, or explain P; therefore not-P. **Confirm:** quote inability and conclusion; test whether text supplies any contradiction, failed prediction, or evidence beyond speaker incapacity. This differs from ignorance because inability, not missing evidence, is proof.

### 4. Relevance and diversion

* **Straw man** — **Pattern:** opponent asserts P; speaker substitutes P'; refutes P'; therefore rejects P. **Confirm:** quote opponent P, substituted P', and rejection; identify dropped qualifier, changed target, or altered strength. This differs from red herring because a distorted version of opponent's claim is attacked.
* **Red herring** — **Pattern:** issue P is under discussion; speaker introduces R; therefore P is accepted, rejected, or left unanswered. **Confirm:** name original P, substituted R, and final conclusion about P; show supplied R neither proves nor defeats P under stated standard. This differs from irrelevant conclusion because R diverts the discussion.
* **Whataboutism** — **Pattern:** criticism P of actor A; allegation R about actor B; therefore criticism P is dismissed. **Confirm:** quote P, R, and dismissal; R does not answer whether A did P or whether P breaches standard. **Guard:** same stated rule governs A and B, so R directly tests inconsistent application.
* **Ignoratio elenchi / irrelevant conclusion** — **Pattern:** premises establish R; therefore stated conclusion P. **Confirm:** state exact R and P, then show R could hold while P remains unsettled. This differs from red herring when argument reaches wrong conclusion without first switching discussion issue.

### 5. Person, source, and social appeals

* **Ad hominem** — **Pattern:** speaker/source trait S; therefore source claim P is false or dismissible. **Confirm:** quote S attack and P conclusion; no evidence about P's content connects them. **Guard:** concrete bias, access, competence, incentive, or deception fact changes reliability of this witness's testimony.
* **Genetic fallacy** — **Pattern:** P came from origin O; therefore P is true or false. **Confirm:** quote O and truth verdict; argument tests neither P nor its evidence. **Guard:** provenance identifies a concrete evidence-chain defect, such as forged record, contaminated sample, or broken custody.
* **Poisoning the well** — **Pattern:** preemptive source trait S; therefore audience should reject forthcoming P. **Confirm:** quote prejudicial framing before or instead of P-specific reasons; conclusion asks rejection based on source framing. **Guard:** stated source fact directly affects reliability of forthcoming testimony.
* **Unqualified authority** — **Pattern:** X says P; therefore P. **Confirm:** supplied facts show X lacks applicable expertise/access or uses basis unrelated to P; missing credentials alone is `Missing support/context`, not this label. **Guard:** qualified expert testimony with access and stated basis is defeasible evidence, not conclusive proof.
* **Bandwagon / popularity** — **Pattern:** many people believe or do P; therefore P is true or right. **Confirm:** quote count, majority, or prevalence and truth/right conclusion; popularity is warrant rather than topic being measured. This differs from a report that concludes only what people believe or buy.
* **Appeal to tradition** — **Pattern:** P is old or customary; therefore P is true or right. **Confirm:** quote age/custom and verdict; no tested outcome or independent reason links practice to verdict. This differs from evidence that a practice repeatedly achieved specified result.
* **Appeal to emotion** — **Pattern:** evoke fear, pity, anger, pride, or disgust E; therefore P is true/right or action A required. **Confirm:** quote E-trigger and conclusion; emotional response is stated warrant instead of factual support. **Guard:** concrete harm, risk, or benefit evidence supports policy A independently of emotional wording.
* **Appeal to consequences** — **Pattern:** believing P would have desirable/undesirable outcome O; therefore P is true/false. **Confirm:** distinguish factual P from O and quote truth verdict drawn from O. **Guard:** O is used to choose an action or policy after P is separately assessed, not to decide P's truth.

### 6. Evidence and generalization

* **Hasty generalization** — **Pattern:** observed cases S; therefore population T has property P. **Confirm:** name sample S, target population T, and claimed scope; supplied cases leave unobserved T members untested and give no coverage basis. This differs from a representative sample claim with stated selection.
* **Sweeping generalization** — **Pattern:** rule `All A are B`; case x is A; therefore x is B, despite exception condition E. **Confirm:** quote rule and case facts; x meets supplied E, but rule is applied without showing E does not exempt x. This differs from hasty generalization because rule, not sample, drives conclusion.
* **Biased / unrepresentative sample** — **Pattern:** selected sample S; therefore target T has P. **Confirm:** name T and sample selection rule; it systematically excludes, overweights, or self-selects a T subgroup that affects P. This is a selection defect, not merely a small sample.
* **Cherry-picking / evidence suppression** — **Pattern:** favorable evidence F; therefore P, while supplied context contains omitted counterevidence C. **Confirm:** quote F and C; C bears on same P in opposite direction and was available in supplied argument/context. Do not invent unmentioned counterevidence.
* **Anecdotal evidence** — **Pattern:** one or few cases A; therefore broad or causal P. **Confirm:** identify case count and target scope; cases are sole support for population or causal conclusion. This differs from an anecdote offered only to illustrate already supplied evidence.

### 7. Causation

* **Post hoc ergo propter hoc** — **Pattern:** A occurred before B; therefore A caused B. **Confirm:** quote timing and causal conclusion; supplied support is sequence alone, with no mechanism, comparison group, or alternative cause check. This is temporal order error, not correlation error.
* **Cum hoc ergo propter hoc** — **Pattern:** A and B co-occur or correlate; therefore A caused B. **Confirm:** quote association and direction claim; text gives no test of temporal direction, intervention, or confounder. This differs from post hoc because association, not order alone, is warrant.
* **Reverse causation** — **Pattern:** A-B association; therefore A causes B, though B could cause A. **Confirm:** evidence fails to establish A -> B direction or rule out B -> A; A-before-B alone is not reverse-causation evidence. This is direction error, not merely unmeasured confounding.
* **Ignoring common cause** — **Pattern:** A-B association; therefore direct A -> B, omitting C -> A and C -> B. **Confirm:** supplied context identifies plausible C causing both; argument has no control, stratification, or comparison for C. This differs from reverse causation because C explains both.
* **Oversimplified cause** — **Pattern:** A is asserted sole cause of B, or sufficient-by-itself for B. **Confirm:** quote sole or sufficient scope; check supplied alternatives, enabling conditions, and interactions. Sole means no other cause; sufficient means A alone guarantees B. Do not label a claim limited to A as one contributor.
* **Slippery slope** — **Pattern:** first step A -> B -> ... -> remote Z; therefore accept or reject A. **Confirm:** list each stated link and identify first unsupported causal/probability jump; conclusion treats chain as inevitable or likely without link evidence. This is a multi-step causal claim, not a single post hoc inference.

### 8. Comparison and part-whole

* **False analogy** — **Pattern:** A and B share S; A has P; therefore B has P. **Confirm:** name shared S, transferred P, and difference D; show D changes whether P transfers under conclusion's standard. This differs from false equivalence because property transfer, not equal evaluation, is conclusion.
* **False equivalence** — **Pattern:** A and B share S; therefore A and B are equally good, bad, serious, or deserving under E. **Confirm:** name evaluation E and ignored difference D; D changes E under stated standard. This differs from analogy because conclusion asserts equal judgment, not a transferred trait.
* **Composition** — **Pattern:** each part has P; therefore whole has P. **Confirm:** supplied definition or aggregation rule shows P need not transfer parts -> whole; never invent a counterexample. This differs from valid addition when P is explicitly additive or defined collectively.
* **Division** — **Pattern:** whole has P; therefore each part has P. **Confirm:** supplied definition or distribution rule shows whole P need not apply to every member; never invent a counterexample. This differs from valid distribution when P is defined of every member.

### 9. Consistency and rule application

* **Inconsistency / self-contradiction** — **Pattern:** P and not-P are both asserted. **Confirm:** quote both and match subject, predicate meaning, time, and respect; only then show direct conflict. Do not flag statements about different times, meanings, groups, or conditions.
* **Special pleading** — **Pattern:** Rule R applies to cases meeting K; case or group F meets K; R exempts F while comparable K cases remain governed. **Confirm:** quote R, K, F, and exemption; comparable K cases remain governed, and no prior criterion separates F. This differs from a rule with a stated exception criterion.
* **No true Scotsman** — **Pattern:** `All T are P`; counterexample x is T and not-P; therefore redefine T to exclude x. **Confirm:** quote original rule, counterexample, and exclusion; exclusion criterion first appears after challenge. This is ad hoc redefinition, not application of a prior criterion.

### 10. Probability and statistics

For conditional probabilities, preserve order: `P(E|H)` and `P(H|E)` answer different questions.

* **Base-rate neglect** — **Pattern:** evidence signal E; therefore case is class H, using E while ignoring prior `P(H)`. **Confirm:** quote supplied applicable prior/reference-class rate that conclusion ignores. Competing likelihoods are required only when calculating posterior probability.
* **Conjunction fallacy** — **Pattern:** same case is judged `P and Q` more probable than P alone. **Confirm:** quote both probability judgments, reference class, and scale; conjunction event is subset of P, so its probability cannot exceed P. This is not a mere claim that both facts are vivid.
* **Prosecutor's fallacy** — **Pattern:** low `P(E | innocent)`; therefore low `P(innocent | E)` or high `P(guilty | E)`. **Confirm:** posterior innocence/guilt is derived from `P(E|innocent)`; supplied evidence lacks at least one required prior or competing likelihood and gives no independent posterior support.
* **Gambler's fallacy** — **Pattern:** independent past outcomes occurred; therefore opposite next outcome is due. **Confirm:** quote fixed odds/independence and claim that history changes next-trial odds. **Guard:** trials are dependent or probability changes with state, depletion, or intervention.

### 11. Definition and normative inference

* **Loaded definition** — **Pattern:** define T using disputed evaluation E; x is T; therefore x is E. **Confirm:** quote definition and conclusion; loaded membership T is used as independent evidence for disputed E, not mere stipulated terminology. This differs from a stipulative definition used only to set terminology.
* **Is-ought fallacy** — **Pattern:** descriptive P; therefore one ought to do Q. **Confirm:** list supplied premises; none states or entails value, goal, duty, normative rule, or conditional with ought-consequent linking P to Q; a merely descriptive condition is not a normative bridge. **Guard:** explicit normative bridge states why P supports Q.

## False-positive guards

Do **not** label these fallacies without a specific defect:

* Relevant credibility criticism bearing directly on reliability, bias, or expertise.
* Qualified authority used within relevant expertise as defeasible, not conclusive, support.
* A genuinely exhaustive choice set.
* A supported causal chain with evidence, mechanism, and alternatives addressed.
* Emotional wording that does not replace evidence or inference.
* Legitimate uncertainty, qualification, or a request for more evidence.

A credibility, authority, causal, or choice claim can lack support without being a fallacy. Mark `Missing support/context` instead of forcing a label.

## Output

For each candidate, quote smallest exact reasoning span; name label; show Pattern match and Confirm evidence; assign `high|medium|low`; give concise refutation and corrected rewrite.

In `rewrite` mode, return coherent revised passage preserving defensible intent, remove invalid inference, and mark unsupported claims `[support needed]`; never invent evidence.
