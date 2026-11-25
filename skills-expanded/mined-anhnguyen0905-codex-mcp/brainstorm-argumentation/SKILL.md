---
name: brainstorm-argumentation
description: Use steelman, Toulmin, Walton schemes and critical questions, pragma-dialectical rules, dialectical inquiry, and SAST to structure argumentation.
---

# Brainstorm argumentation (embed into Codex prompts)

Structure each Reason turn as a sourced argumentation audit.
Steelman the current thesis before challenging it, then expose assumptions and the crux.

## Standards block

### Debate block

```
Debate block
- Steelman the other position so its owner would endorse the summary; list agreement and what was learned before criticism. (Dennett, Intuition Pumps and Other Tools for Thinking)
- Lay out each argument as claim, data, warrant, backing, qualifier, and rebuttal; name the one Toulmin element attacked in each challenge. (Toulmin, The Uses of Argument)
- Treat the warrant as the most often unstated and weak element. (Toulmin, The Uses of Argument)
- Identify the Walton scheme and ask its standard critical questions; an unanswered question shifts the burden to the arguer. (Walton, Reed & Macagno, Argumentation Schemes; Walton, Fundamentals of Critical Argumentation)
- cause-effect (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ1 how strong is the causal generalisation? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ2 is the cause sufficient here? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ3 could other causes interfere? (Walton, Reed & Macagno, Argumentation Schemes)
- consequences (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ1 how likely are the consequences? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ2 what evidence supports them? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ3 are there opposite consequences to weigh? (Walton, Reed & Macagno, Argumentation Schemes)
- analogy (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ1 are the cases similar in the respects that matter? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ2 are there relevant differences? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ3 is there a counter-analogy? (Walton, Reed & Macagno, Argumentation Schemes)
- expert-opinion (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ1 is the source a genuine expert in this field? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ2 is the claim consistent with other experts? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ3 is the assertion based on evidence? (Walton, Reed & Macagno, Argumentation Schemes)
- sign (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ1 how strong is the correlation between sign and event? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ2 are there other events the sign would indicate? (Walton, Reed & Macagno, Argumentation Schemes)
- example (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ1 is the example typical? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ2 are there counter-examples? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ3 is the sample large enough? (Walton, Reed & Macagno, Argumentation Schemes)
- sunk-cost (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ1 does past investment change future value? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ2 is continuing still the best use of resources from now? (Walton, Reed & Macagno, Argumentation Schemes)
- slippery-slope (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ1 is each step in the chain likely? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ2 can the sequence be stopped at a point? (Walton, Reed & Macagno, Argumentation Schemes)
  - CQ3 is the final outcome really bad? (Walton, Reed & Macagno, Argumentation Schemes)
- Run confrontation, opening, argumentation, and concluding stages; maintain, retract, or leave the difference unresolved. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD1 freedom: do not block standpoints or doubt. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD2 burden of proof: defend a standpoint when asked. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD3 standpoint: attack the standpoint actually advanced; a straw man violates this rule. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD4 relevance: defend with argumentation about the standpoint. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD5 unexpressed premise: do not deny or exaggerate an implicit premise. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD6 starting point: do not present as accepted what is not, nor deny an agreed start. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD7 argument scheme: use an appropriate, correctly applied scheme. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD8 validity: reasoning must be valid or made valid by explicit premises. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD9 closure: a failed defence means retracting; a successful one means withdrawing doubt. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- PD10 usage: use no unclear or ambiguous formulations. (van Eemeren & Grootendorst, A Systematic Theory of Argumentation)
- Build a counter-plan from opposite assumptions using the same data, then debate plan versus counter-plan to expose assumptions. (Mason & Mitroff, Challenging Strategic Planning Assumptions)
- List each position's assumptions and rate importance and certainty; investigate high-importance, low-certainty assumptions next. (Mason & Mitroff, Challenging Strategic Planning Assumptions)
- Trace a surviving disagreement to one warrant or assumption; record “we still disagree” without that pointer as no conclusion. (derived)
```
