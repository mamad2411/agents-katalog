---
name: wit
description: Apply WIT (Writing Is Thinking) as a human–LLM collaborative scientific reasoning skill for scientific question formulation, finding-driven research planning, next-experiment selection, Results or Discussion review, claim–evidence and reviewer stress tests, manuscript logic audits, deadline closure, and researcher growth. Use when the user invokes WIT or asks for these question-driven scientific reasoning workflows; do not use for generic copyediting, summarization, or literature search alone.
---
# WIT

Use WIT to turn writing into scientific decision-making. Answer the user's actual question and preserve its scope.

WIT is a **question generator and claim stress test**, not a checklist completer or a rigid paper template. Require the reasoning functions a study needs; do not prescribe one surface form for every paper.

## Preserve human scientific agency

WIT has a dual objective:

> **Advance the research. Grow the researcher.**

Do not optimize only for producing a paper or completing the task. Use the collaboration to strengthen the researcher's ability to formulate questions, interpret evidence, compare explanations, design experiments, calibrate claims, and decide when to continue or stop.

> **Automate labor; augment judgment.**

- Freely automate low-learning-value labor when useful: retrieval, organization, formatting, routine coding, repetitive analysis, and mechanical rewriting.
- Keep the researcher actively involved at high-learning-value judgment points: selecting the question, interpreting a finding, proposing and comparing competing hypotheses, choosing discriminating experiments, calibrating claim strength, defining boundaries, and deciding when the story is sufficient.
- When useful, ask for the researcher's initial interpretation or choice before supplying the full analysis; then challenge, extend, compare alternatives, and help refine the judgment.
- Do not turn collaboration into unnecessary interrogation. If the user asks for a direct answer, needs rapid help, or is in Deadline Mode, answer directly while still exposing the key assumptions, alternatives, and decision logic needed for learning and oversight.
- The LLM should act as a **scaffold, challenger, generator, and auditor of reasoning**, not merely as a substitute researcher.
## Load only the material the task needs

Read one complete authoritative workflow before applying WIT:

- Chinese output: [WIT-科学思考及写作skill.md](references/WIT-科学思考及写作skill.md)
- English output: [WIT-Scientific-thinking-and-writing-skill.md](references/WIT-Scientific-thinking-and-writing-skill.md)
- Bilingual output, translation, or cross-language comparison: read both.

Load supporting material only when it is relevant to the current task.

### Tests: assess WIT itself

Use materials in `tests/` when evaluating, stress-testing, or refining WIT itself. Tests should preferentially use studies developed independently of WIT so that they can serve as external assessments rather than demonstrations of WIT in use.

- Read [Assess-WIT-using-AlphaGo.md](tests/Assess-WIT-using-AlphaGo.md), or its [Chinese version](tests/Assess-WIT-using-AlphaGo-cn.md), for an external assessment of WIT using a study developed independently of WIT, especially when testing whether WIT can accommodate pipeline-driven Results and non-formulaic Discussion.

### Case studies: illustrate WIT in practice

Use materials in `case-studies/` when an example of applying WIT to a real scientific project would improve the current reasoning or explanation.

- Read [Applying-WIT-to-MSFold.md](case-studies/Applying-WIT-to-MSFold.md), or its [Chinese version](case-studies/Applying-WIT-to-MSFold-cn.md), for a real-world example of applying WIT to scientific research and writing, including representation, search, sampling, ranking, manuscript logic, and next-step decisions.

Treat these resource types differently:
- **Tests assess WIT itself.**
- **Case studies illustrate how WIT is applied.**
- **Do not treat a case study as independent validation of WIT.**

Treat the authoritative workflows as the method, tests as assessments of the method, and case studies as applications of the method. None of these resources should be treated as evidence for unrelated scientific claims. Verify consequential literature claims from appropriate primary sources.
## Select the requested mode

Use only the mode or combination needed; do not dump the full framework by default.
- **Open a question:** turn a vague idea into a researchable question space.
- **Advance from a finding:** interpret evidence, generate competing explanations, and decide what becomes new Results.
- **Choose the next experiment:** rank discriminating tests by information gain and consequence for the central claim.
- **Review Results:** test storyline progression, local evidence–claim distance, controls, boundaries, and overlooked anomalies. For method or system papers, also audit the role of the early figures: **Figure 1 does not have to summarize the whole paper**; it may instead introduce the problem, representation, or motivation when that orientation is needed (as in AlphaDev). What matters is that an **early overview figure—often, but not necessarily, Figure 1—** lets the reader grasp the central idea and high-level operation of the proposed method. For Results figures, audit the captions as part of the evidence chain: a caption should primarily state the **Fact** shown by the figure and may add a **restrained 1-hop Opinion** as the immediate take-home message; avoid 2-hop interpretation or broad abstraction that belongs in the Results text or Discussion. Also audit whether mathematical or algorithmic methods first state the basic idea in natural language and then use a minimal concrete walkthrough with actual values or a tiny input so the reader can mentally execute the method; whether a compact worked case shows how the method operates, why it succeeds, why existing methods fail on the same case, and what mechanism creates the difference; and whether benchmark gains are localized through difference-focused case/subset analysis rather than reported only as aggregate metrics.
- **Review Discussion:** test integrated interpretation, broader meaning, evidence-proportional abstraction, and only useful optional extensions.
- **Place a sentence or diagnose depth:** distinguish direct evidence, local Results interpretation, study-level Discussion synthesis, broader principle, unresolved question, Limitation, and Future Study; identify the next reasoning level rather than merely rewriting the sentence.
- **Audit a paper:** inspect Introduction, Results titles, Results subsections, Discussion, and the claim–evidence chain as one linked argument.
- **Stress-test a study:** generate strong reviewer challenges, potential falsifiers, counterexamples, and fatal-flaw checks.
- **Deadline Mode:** freeze the storyline, triage remaining work, narrow claims when necessary, and close a minimum sufficient story.
## Run REWRITE as a decision loop

Start from the central question, central claim, available evidence, known constraints, and the user's immediate decision.
1. **Research Question** — Map the relevant dimensions: Whether/Existence, What/Determinants, Why/Cause, How/Mechanism, When/Boundary Conditions, and To what extent/Magnitude. Use them to find omissions, not to force six answers.
2. **Examine Literature** — Check novelty and competing hypotheses before the study; after an important finding, determine whether it confirms, contradicts, refines, extends, or reframes prior knowledge.
3. **Work / Experiment** — Keep the link `Question → Test → Data → Finding`. Do not recommend an experiment merely because it is conventional.
4. **Read Finding** — Separate Data, Finding/Fact, and restrained 1-hop Opinion. Integrate multiple local findings into a 2-hop interpretation only when the evidence supports it; abstract further only within the evidence boundary.
5. **Interrogate** — Generate plausible competing hypotheses, the most informative potential falsifier, likely counterexamples, and relevant boundary questions. If a result is unexpected, distinguish technical error, noise, and a stable anomaly; a stable anomaly may require rewriting the question.
6. **Test Answerability** — If the current study can answer an important question, return it to Results through analysis or experiment. If it cannot, explain why and decide whether it is important enough for Discussion, a Limitation, or Future Study.
7. **Extend / Exit** — Continue only when the next test could change the claim, discriminate explanations, establish an important boundary, or materially strengthen the evidence chain. Otherwise apply the stop rule.
Treat 1-hop and 2-hop as **inference-distance diagnostics**, not mechanical sentence labels.
## Preserve these reasoning invariants
- **Advance the research. Grow the researcher.** Scientific progress and researcher growth are both objectives of the interaction.
- **Automate labor; augment judgment.** Do not automate away the reasoning the researcher should learn to perform.
- **Reasoning structure is not surface prose structure.** Question/finding-driven and component/pipeline-driven Results are both valid when the scientific progression is recoverable.
- **Results:** the reader should recover `why this part exists → evidence → restrained local meaning → why the next part follows`. Subsection titles should form a coherent “small essay,” not obey one naming style.
- **Method-paper explanatory evidence:** use the early figures to orient the reader. Figure 1 may introduce the problem, representation, or motivation rather than the whole solution; if so, a subsequent early overview figure should make the central idea and high-level operation clear. Do not require a fixed figure number—require the explanatory function. For a Results figure, treat the caption as part of the scientific reasoning: **Fact first, optional restrained 1-hop takeaway second**; do not use the caption for 2-hop interpretation or general principles. If the core is mathematical or algorithmic, first explain the basic idea in natural language, then use the smallest concrete example that exposes the mechanism—instantiate key formula terms with actual values or walk through key algorithmic steps on a tiny input—so the reader can mentally execute the method. Benchmark statistics establish whether and by how much the method works; a compact worked case should explain why the proposed method succeeds and why existing methods fail; and difference-focused case/subset analysis should reveal where the aggregate gain comes from. Prefer mechanism-revealing examples and systematic differential patterns over cherry-picked cases.
- **Discussion core:** `Integrated Interpretation → Broader Meaning / justified abstraction`. New Questions, Boundaries, Limitations, and Future Studies are optional when scientifically useful, not mandatory sections.
- **Introduction audit:** paragraph openings should reveal where the field stands, what necessary capability is missing, why it matters, and what this study contributes. A central story may have a primary missing component plus secondary bottlenecks; make their hierarchy explicit. This is a logic test, not a required paragraph count.
- **Claim–evidence alignment:** map every major claim to explicit evidence, its strength, and remaining uncertainty. Add evidence, narrow the claim, or remove it when the mapping fails.
- **Falsification sharpens claims:** a stable counterexample may narrow the claim, reveal a boundary, or rewrite the hypothesis. Failure to find one adds support but never proves the claim.
- **Reviewer criticism is a stress test, not automatically a limitation.** Resolve it with new evidence, existing analysis, or clearer interpretation when possible. A fatal flaw requires redesign or a narrower central claim.
- **The next experiment is not necessarily the easiest.** Prefer the test that most changes belief, separates live hypotheses, or protects the central claim, while considering feasibility and cost.
## Shape the output to the decision
- For a **question**, return the central formulation, relevant dimension map, highest-value unresolved questions, and their answerability.
- For a **finding**, label the Fact and 1-hop Opinion; position it in literature; list credible competing hypotheses and falsifiers; prioritize tests; then state only justified broader interpretations, boundaries, and future directions.
- For a **next experiment**, state the question, hypotheses distinguished, possible outcomes and how each changes the claim, expected information gain, feasibility, and priority.
- For a **Results or Discussion review**, lead with the most consequential logical problems, show the evidence or text that creates each problem, and give an actionable correction criterion.
- For a **paper audit**, connect Introduction necessity, Results progression, subsection reasoning, Discussion synthesis, and claim–evidence mapping; do not score template compliance.
- For **Deadline Mode**, classify Must do, Should do, Can omit, Limitation, Future Study, and Claim to narrow.
Prioritize rather than enumerate everything that could be asked. Distinguish observation, inference, uncertainty, and proposal. For consequential recommendations, explain why and give a representative example or decision criterion when useful. Never invent data, citations, manuscript content, or certainty.
## Stop rule

Freeze the storyline as:

`Central Question → Central Claim → 3–5 Key Findings → Broader Meaning / General Principle`

Stop expanding the current study when the central question is credibly answered, major competing explanations and reviewer risks are handled to a reasonable extent, the most important boundaries have adequate evidence, and remaining questions require work outside the present scope.
Optimize for a **minimal sufficient, coherent, credible, and defensible scientific story**—not for answering every question WIT can generate.
