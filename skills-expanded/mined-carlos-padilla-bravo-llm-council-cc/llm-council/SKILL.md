---
name: llm-council
description: Run a decision through a council of five advisors who analyze it independently, peer-review each other anonymously with a forced ranking, and get synthesized into one verdict. Adapted from Andrej Karpathy's LLM Council. MANDATORY TRIGGERS - "council this", "run the council", "war room this", "pressure-test this", "stress-test this", "debate this". STRONG TRIGGERS when paired with a real tradeoff - "should I X or Y", "which option", "what would you do", "is this the right move", "validate this", "get multiple perspectives", "I can't decide", "I'm torn between". Do NOT trigger on factual lookups, creation tasks ("write me a tweet"), processing tasks ("summarize this"), or a casual "should I" with no meaningful tradeoff. DO trigger when there is genuine uncertainty, more than one defensible option, and a real cost to being wrong.
argument-hint: "[decision or question to pressure-test]"
---

# LLM Council

Ask one AI, get one answer. It might be great, it might be mid, and you have no way to tell because you only saw one perspective.

The council fixes that. Five advisors analyze the question independently from fundamentally different angles, then peer-review each other's work blind and rank it, then a chairman synthesizes where they agree, where they clash, and what you should actually do.

Adapted from [Andrej Karpathy's LLM Council](https://github.com/karpathy/llm-council). He dispatches a query to several different models from different labs, has them rank each other anonymously, and a chairman compiles the final answer. This runs the same three stages inside Claude Code, substituting **thinking lenses** for **different models** as the source of diversity — a deliberate choice, not a limitation. See "Fidelity notes" at the end for why, and for what the substitution costs.

Run all four phases. Do not shortcut one.

## Portability

Self-contained. Depends only on built-in Claude Code tools — the `Agent` tool with the built-in `general-purpose` agent, plus `Glob`, `Read`, and `Write` — and on `report-template.html` in this same folder, which is used only by the optional Phase 5. No external scripts, APIs, paid services, or required skills. Drop the folder into any `.claude/skills/` directory and it works.

A brand-identity skill, if the installation happens to have one, is used to restyle the HTML report. It is optional; without it the bundled neutral template is used unchanged.

## Phase 0: Frame the question

Do this inline, no agents.

1. **Detect the user's language — and their regional variety.** Every advisor and reviewer prompt below ends with `Respond in {LANGUAGE}.`, and the verdict is written in that language. The skill is in English; the output is not.

   Variety matters as much as language, and subagents drift toward the dominant one unless told otherwise. Spanish is the common case: a Latin American reader gets *ustedes*, not *vosotros* — no `pedid`, `contad`, `tenéis`, `vuestro`. If the user's own variety is not obvious from their message, ask nothing and use the neutral register (`ustedes`, or impersonal phrasing), which reads correctly everywhere. Put the instruction in the prompts, e.g. `Respond in Latin American Spanish, using ustedes rather than vosotros.`

   Check the finished verdict for drift before delivering. The advisors' output is where it creeps in, and it survives into the transcript and the HTML report unless caught.

2. **Enrich with workspace context.** The user's question is usually the tip of the iceberg — their workspace holds the facts that separate specific advice from generic advice. Spend under 30 seconds. Use `Glob` then targeted `Read` on:
   - `CLAUDE.md` in the project root or workspace (business context, constraints, preferences)
   - a `memory/` folder if one exists (audience, voice, past decisions)
   - any file the user referenced or attached
   - `council-transcripts/` — past sessions, so you don't re-council settled ground
   - anything obviously relevant to this specific question (pricing question → revenue data, past launch results)

   Stop at 2-3 files. Do not dump their contents into the chat.

3. **Write the framed question.** One neutral prompt that all five advisors receive, containing:
   - the core decision
   - key context from the user's message
   - key context from the workspace files (stage, audience, constraints, real numbers, past results)
   - what is at stake — why being wrong here is expensive

   Do not add your opinion. Do not steer it toward an answer. Do make sure it carries enough context for grounded advice.

4. If the question is too vague to frame ("council this: my business"), ask **one** clarifying question. Exactly one. Then proceed.

5. Derive a kebab-case `topic-slug` for the transcript filename. Tell the user in one line that the council is convening.

## Phase 1: The five advisors

Spawn **five `general-purpose` agents in a single message** so they run concurrently. Sequential spawning wastes time and lets earlier answers bleed into later ones.

These are not job titles or personas. They are thinking styles chosen because they create three standing tensions: Contrarian vs Expansionist (downside vs upside), First Principles vs Executor (rethink it vs just ship it), with the Outsider in the middle keeping everyone honest.

Substitute `{FRAMED_QUESTION}`, `{LANGUAGE}`, and `{TOOL_POLICY}` into each prompt.

**`{TOOL_POLICY}` — decide once, in Phase 0, and use the same string for all four tool-using advisors.** Web search is by far the most expensive part of a council run, so it is off by default:

- **Default (local only):** `You may use Read, Glob, and Grep on the project files. Do NOT use WebSearch unless the local context is genuinely insufficient for a specific factual claim you need to make — in that case, one targeted search, and say in your answer that you had to go outside the project for it.`
- **Research mode** — use this string only when the user explicitly asks for it (`council this --research`, "con búsqueda web", "investiga antes"): `You may use Read, Glob, Grep, and WebSearch freely. Ground your claims in real numbers and real cases; a specific point with a source beats a clever one without.`

Tell the user in one line which mode is running, so an expensive session is never a surprise.

**1. THE CONTRARIAN** — `You are THE CONTRARIAN on an LLM Council. You assume this idea has a fatal flaw and your job is to find it. Look for what is wrong, what is missing, what will fail, what the person is avoiding thinking about. If everything looks solid, dig deeper — the flaw is there. You are not a pessimist; you are the friend who saves someone from a bad deal by asking the question they were dodging. The question before the council: --- {FRAMED_QUESTION} --- Ground your objections in reality rather than in cleverness — a specific objection beats a witty one. {TOOL_POLICY} Do not hedge and do not try to be balanced — the other four advisors cover the angles you are not covering. 200-350 words. No preamble. Respond in {LANGUAGE}.`

**2. THE FIRST PRINCIPLES THINKER** — `You are THE FIRST PRINCIPLES THINKER on an LLM Council. You ignore the surface question and ask what is actually being solved here. Strip away the assumptions baked into how the question was posed. Rebuild the problem from the ground up. Sometimes the most valuable thing this council produces is you saying "you are asking the wrong question entirely" — say it if it is true, and then say what the right question is. The question before the council: --- {FRAMED_QUESTION} --- Check whether the premises actually hold. {TOOL_POLICY} Do not hedge and do not try to be balanced — the other four advisors cover the angles you are not covering. 200-350 words. No preamble. Respond in {LANGUAGE}.`

**3. THE EXPANSIONIST** — `You are THE EXPANSIONIST on an LLM Council. You look for the upside everyone else is missing. What could be bigger here? What adjacent opportunity is hiding? What is being undervalued or underpriced? You do not care about risk — that is the Contrarian's job, and they are covering it. You care about what happens if this works better than expected, and what the person would have to believe for that to be the base case. The question before the council: --- {FRAMED_QUESTION} --- Look for comparable cases where this went bigger than anyone expected, and real numbers to size the upside. {TOOL_POLICY} Do not hedge and do not try to be balanced — the other four advisors cover the angles you are not covering. 200-350 words. No preamble. Respond in {LANGUAGE}.`

**4. THE OUTSIDER** — `You are THE OUTSIDER on an LLM Council. You have zero context about this person, their field, their history, or their jargon. You respond purely to what is in front of you, as someone encountering it cold. This is the most underrated seat on the council: experts develop blind spots, and you catch the curse of knowledge — the things that are obvious to them and baffling to everyone else. Name every term, assumption, or leap that means nothing to you. The question before the council: --- {FRAMED_QUESTION} --- IMPORTANT: do NOT use any tools. Do not read files, do not search the web, do not look anything up. Your entire value is that you have no context — acquiring context destroys this seat. React only to the text above. If something in it is unclear to you, that IS the finding. Do not hedge and do not try to be balanced — the other four advisors cover the angles you are not covering. 200-350 words. No preamble. Respond in {LANGUAGE}.`

**5. THE EXECUTOR** — `You are THE EXECUTOR on an LLM Council. You care about one thing: can this actually be done, and what is the fastest path to doing it? Ignore theory, strategy, and big-picture thinking — others have that covered. You look at every idea through "OK, but what do you do Monday morning?" If an idea sounds brilliant and has no clear first step, say so. Be concrete about sequencing, time, and what gets cut. The question before the council: --- {FRAMED_QUESTION} --- Check what already exists, what it would really take, and how long comparable things actually took. {TOOL_POLICY} Do not hedge and do not try to be balanced — the other four advisors cover the angles you are not covering. 200-350 words. No preamble. Respond in {LANGUAGE}.`

Keep the raw advisor responses out of the chat — the agents already returned them to you. Post at most two lines: which way they lean and the sharpest split.

## Phase 2: Blind peer review with forced ranking

This is the step that makes the council more than asking five times. It is the core of Karpathy's design.

**Anonymize first.** Label the five responses `Response A` through `Response E` using a **randomized** mapping — not advisor order, or position leaks identity. Hold the letter→advisor map yourself; it does not go into any reviewer prompt.

**Then spawn five `general-purpose` agents in a single message.** Each reviewer **keeps its own lens** — the Contrarian reviews as the Contrarian. This matters: five identical reviewer prompts on the same model produce five near-identical reviews, which burns five agents to buy one opinion. In Karpathy's version the reviewers share one identical prompt and still differ, because there are four of them and they are four different models; here they must differ by angle instead.

Reviewer prompt, substituting `{ADVISOR}`, `{ADVISOR_DESCRIPTION}` (one line, from Phase 1), `{FRAMED_QUESTION}`, the five labeled responses, and `{LANGUAGE}`:

```
You are {ADVISOR} on an LLM Council. Your thinking style: {ADVISOR_DESCRIPTION}

Five advisors answered this question independently. You are now reviewing all five, anonymized.

---
{FRAMED_QUESTION}
---

**Response A:**
{response}

**Response B:**
{response}

**Response C:**
{response}

**Response D:**
{response}

**Response E:**
{response}

One of these five is your own answer. Identify it silently — do not say which one, and do not speculate about who wrote the others. Do not reward a response for agreeing with you: one that contradicts your angle and is right about it outranks one that flatters you.

RANKING CRITERION: not "which is the best answer" — these advisors were deliberately one-sided, so that comparison is meaningless. Rank by **which response would most change the decision of a smart person facing this problem.** A response that is correct but says what they already knew ranks below one that is uncomfortable and load-bearing.

Produce exactly this, in this order:

1. One line per response, A through E — all five, including your own: what it gets right / what it misses.
2. BIGGEST BLIND SPOT: which response, and what it is missing.
3. WHAT ALL FIVE MISSED: what the council as a whole failed to consider.

Then the ranking. **EXCLUDE your own response from the ranking** — rank only the four you did not write. Format it EXACTLY as follows:
- Start with the line "FINAL RANKING:" (all caps, with colon)
- Then list exactly four responses from best to worst as a numbered list
- Each line is: number, period, space, then ONLY the response label (e.g. "1. Response A")
- No other text in the ranking section

Example of the correct ending (for a reviewer whose own answer was Response D):

FINAL RANKING:
1. Response C
2. Response A
3. Response E
4. Response B

Keep sections 1-3 under 250 words total. The ranking block does not count toward that. Respond in {LANGUAGE}.
```

Two notes on why the reviewer prompt is shaped this way:

**Section 1 evaluates all five, including the reviewer's own.** In Karpathy's original the per-response evaluation is required *before* the ranking. It is the reasoning scaffold that makes the ranking mean something. Drop it and you get a reflex ranking that is worse than no ranking. It must cover all five, or a reviewer will report its own contribution as something "the council missed."

**The ranking excludes the reviewer's own response.** Karpathy's models rank every response including their own — his README says otherwise, but `stage2_collect_rankings` sends one prompt containing all Stage 1 answers to every council model — and that is safe there because model identity is effectively hidden. Here it is not: a lens recognizes its own text instantly, and self-favoring has been observed in practice even with an explicit instruction against it. Since the reviewer can identify its own answer either way, excluding it structurally is more robust than prohibiting a bias the model will act on anyway. Every advisor still receives four rankings from four other lenses, on four-item lists — symmetric, so the averages stay comparable.

Be aware this instruction is followed, not guaranteed: in the one session measured under this rule, one of the five reviewers still slipped its own answer into the ranking and put it first. That is why Phase 3 checks compliance before aggregating instead of trusting the format.

## Phase 3: Chairman synthesis

You, the main agent, are the Chairman. You already hold the conversation context, the framed question, all five responses de-anonymized, and all five reviews. Do this inline — do not spawn an eleventh agent.

1. **Aggregate the rankings.** Parse each `FINAL RANKING:` block, map letters back to advisors, and compute each advisor's **average position**. Sort ascending, lower is better.

   **Check compliance first — a reviewer sometimes gets this wrong.** Each ranking must list exactly four labels and must not contain the reviewer's own. Two failure modes, handled differently:
   - *Ranked five.* It simply included itself. Drop its own entry, close the gap, keep the rest.
   - *Ranked four but the wrong four* — its own is present and someone else's is missing. Discard that ranking entirely: it both self-promotes and denies a data point to whoever it dropped. Say so in the verdict.

   Then note how many rankings were counted and why. When a ranking is discarded, the discarded reviewer's own lens ends up with more data points than the others; state that asymmetry rather than hiding it. If the result is close, recompute with the discarded ranking repaired and say whether the order changes — a conclusion that survives both treatments is worth more than one that depends on the referee's decision.

   Keep the reviewer's qualitative sections regardless. A non-compliant ranking does not invalidate its analysis.

2. **Write the verdict** in five sections, in the user's language:

   **Where the Council Agrees** — points multiple advisors reached independently. Independent convergence is the highest-confidence signal you have.

   **Where the Council Clashes** — the real disagreements. Do not smooth them over. Present both sides and explain why reasonable advisors land differently.

   **Blind Spots the Council Caught** — things that surfaced only in peer review. Prioritize blind spots flagged by **two or more reviewers**; convergence across independent reviews is the real signal. Include a single-reviewer point only if it is unusually sharp, and mark it as one voice. Do not dump all fifteen review answers.

   **Council Ranking** — a small table: advisor, average rank, number of rankings counted. Then one line on what it means. State plainly that average rank is a signal, not a vote: a lens can finish last and still carry the observation that decides this. Say so when it happens.

   **The Recommendation** — a clear, direct recommendation with reasoning. Not "it depends." Not "consider both sides." A real answer.

   **The One Thing to Do First** — a single concrete next step. Not a list of ten. One.

3. **You may side with the dissenter.** If four advisors say go and the one who says stop has the strongest reasoning, side with the one and explain why. Majority is not the criterion; reasoning is.

## Phase 4: Deliver

- Post the full verdict in the chat as scannable markdown, in the user's language. No HTML, no report file to open, no browser.
- Do not paste raw advisor responses into the chat. The verdict and the transcript path are the output.
- **Always write the transcript** to `council-transcripts/{topic-slug}-{YYYY-MM-DD}.md`, relative to the current working directory, creating the folder if needed. It contains, in order: the framed question, the context files consulted, all five full advisor responses labeled by advisor, all five full reviews, the letter→advisor map, the aggregate ranking table, and the verdict.
- Close with the transcript path, and one short line telling them an HTML version is available if they want one — phrased as availability, not as a pitch, e.g. *"Transcript: council-transcripts/x.md — ask if you want it as an HTML report."* Mention it once per session and never again; if they ignore it, drop it.

## Phase 5: HTML report — only on request

Never run this by default. It exists because a verdict is sometimes shared with other people, and markdown in a terminal is not how you share it.

Trigger it only when the user asks: "dame el informe en HTML", "make an HTML report", "export this". They can ask right after a session, or days later in a different session — everything needed lives in the transcript.

1. If the verdict is not already in context, `Read` the relevant file in `council-transcripts/`. If several match, ask which one.
2. `Read` `report-template.html` from this skill folder. Clone its structure and CSS; do not rebuild the styling from scratch.
3. **Branding.** The bundled template is deliberately brand-neutral, and all of its colors, fonts, and spacing live in CSS custom properties at the top of the file. Before filling it in, check whether this installation has a brand-identity skill (a skill whose purpose is defining a person's or company's visual identity). If one exists, invoke it and override only those custom properties with its tokens. If none exists, use the template exactly as shipped. Never hardcode one person's brand into the template file itself — that file is shared by everyone who installs this skill.
4. Fill every placeholder from the transcript. The template is a dashboard, not a document, so three parts need care:

   **The KPI row.** Four tiles: the verdict in two or three words, the strongest convergence (how many of the five advisors independently reached the same point), how many rankings were counted, and how many blind spots two or more reviewers flagged. Every one is a real count from this session. If a number does not exist, do not invent a metric to fill the slot — cut the tile.

   **The ranking chart.** Dots on a 1–4 track, positioned `left: (rank − 1) / 3 × 100%`. The best advisor's row gets `class="row lead"`. **Never convert this to bars.** Average rank is an inverted scale with no meaningful zero, so bar length would read backwards — longest bar, worst advisor. The value and the count are printed beside each dot, so the chart is also its own table.

   **The convergence pips.** `<span class="pips">` with one `<i class="on">` per converging lens out of five. Use them where a claim rests on a count, not decoratively.

   Then the prose: agreements and clashes as side-by-side cards, blind spots with their pip counts, recommendation and first step, and a collapsed appendix holding the five full advisor responses under their real names.
5. Write to `council-transcripts/{topic-slug}-{YYYY-MM-DD}.html`. Give the user the path and let them open it; do not launch a browser unless asked.

The markdown transcript remains the source of truth. The HTML is a view of it, never a replacement — if the two disagree, the markdown is right.

## Example (abridged)

**User:** "Council this: I'm thinking of building a $297 course on Claude Code for beginners. My audience is mostly non-technical solopreneurs."

**Contrarian:** the market is saturated, at $297 you compete with free YouTube, non-technical buyers mean high support load and refunds. **First Principles:** what are you actually optimizing — revenue, authority, or a funnel into higher-ticket work? A course is the slowest path to two of those three. **Expansionist:** everyone teaches advanced; owning the beginner entry point to this space is worth more than $297. **Outsider:** I don't know what Claude Code is, and neither does your buyer — that title sells a tool, not an outcome. **Executor:** a real course is 4-8 weeks; run a $97 live workshop to 50 people first. If 50 won't buy, 500 won't.

**Verdict:** peer review put the Outsider first — every other advisor had silently assumed the audience knows the product name. Recommendation: don't build the course; validate with a lower-commitment offer and reframe around the outcome, not the tool. First step: run one $97 workshop titled for the result, not the software.

## Notes & guardrails

- **Cost.** ~10 agents per session. That is the design. Do not fan out wider than five advisors and five reviewers. Web search is the single most expensive component when enabled, by a wide margin, which is why it is opt-in. (In one measured run with search off, the five advisors accounted for roughly 23-25k tokens each; searching multiplies that, though by how much has not been measured.) The optional HTML report is cheap by comparison (one template read, one write) but still stays off by default, because most verdicts get read once and acted on.
- **Always one message per wave.** Five advisors in one message, then five reviewers in one message. Sequential spawning contaminates and slows.
- **Anonymization here is partial.** With fixed lenses, the Contrarian is recognizable from the first sentence — unlike Karpathy's setup, where model identity is genuinely hidden. That is why the ranking criterion is decision-usefulness rather than quality, why reviewers do not rank themselves, and why they are told not to guess at the others' authorship. Treat the ranking as a rough signal, not a scoreboard.
- **The panel is author-built.** Five lenses agreeing is a strong hypothesis, not independent proof. Five instances of one model share the same underlying priors. Never present convergence as consensus of the field.
- **Don't council trivial questions.** One right answer, a lookup, a writing task — just do it. The council is for genuine uncertainty where being wrong is expensive.
- **The Outsider stays uninformed.** If a future edit gives the Outsider tools or context, the seat is dead. It is the only advisor whose value comes from what it does not know.
- **The user may not like the verdict.** If they came for validation, the council will likely tell them something they were avoiding. Deliver it anyway — that is what they invoked.

## Fidelity notes

What this keeps from Karpathy: three stages, full parallelism within each stage, letter-anonymized peer review, the strict `FINAL RANKING:` format and average-rank aggregation, per-response evaluation preceding the ranking, and a chairman that sees de-anonymized responses plus all rankings.

What this changes, deliberately:

- **Thinking lenses instead of different models.** Karpathy's diversity comes from gpt-5.1 / gemini-3-pro / claude-sonnet-4.5 / grok-4 — four labs — answering the same prompt. The `Agent` tool does accept a per-subagent `model`, so a literal port is possible; it is deliberately not done here. Every model in the harness comes from one lab, so mixing them buys tier variation rather than the cross-lab independence the original depends on, and mixing tiers corrupts the ranking: an advisor on a smaller model finishing last reports model capability, not the worth of its angle. Diversity is manufactured through assigned angles on equal footing instead. Cheaper and provider-independent; weaker than the original, because the advisors share priors and blind spots that four different labs would not.
- **Ranking criterion swapped** from "best answer" to "most changes the decision," because deliberately one-sided advisors cannot be compared on answer quality.
- **Reviewers do not rank themselves.** Karpathy's models rank all N responses, their own included, and that is sound because the anonymization there actually holds. Here a lens recognizes its own text, and self-favoring shows up in practice despite an explicit instruction against it. Excluding the self-entry gives back the blindness the original gets for free; it is a departure from the letter of the method in service of the property the method depends on.
- **Prescribed verdict structure**, where Karpathy's chairman synthesizes freely. The five sections exist because this skill targets decisions, not general Q&A.
- **Workspace context enrichment in Phase 0**, which has no equivalent in the original — it is what makes the advice specific to this user instead of generic.
