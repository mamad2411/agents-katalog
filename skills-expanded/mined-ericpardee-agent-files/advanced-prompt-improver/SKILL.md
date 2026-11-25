---
name: advanced-prompt-improver
description: Use when improving, reviewing, or writing a prompt for frontier models (Claude 4.6+/Opus 5/Fable 5, GPT-5.x class) - delegation briefs, agent goals, system prompts, CLAUDE.md files, or skills. Triggers on "improve this prompt", "why did this prompt fail", "write the kickoff for", "review my CLAUDE.md/skill", or /advanced-prompt-improver. For quick single-message polish the older prompt-improver also works; this skill is the researched 2026 frontier-model version.
---

# Advanced Prompt Improver

Research-grounded (2026 sources at bottom). The one-line thesis, confirmed by Anthropic, OpenAI, and practitioner evidence: frontier models supply the procedure, diligence, and planning by default, so a prompt's job has narrowed to intent, done-state, hard constraints, authorization, and grounding sources, stated exactly once. Specificity did not die; it moved from HOW to WHAT.

## Step 0: Classify before touching anything

- **Conversational or exploratory ask**: leave it alone. Deliberate vagueness is a technique; a vague question gives the model room to surface things you would not ask about.
- **Small task** (diff describable in one sentence): the fix is usually deletion, not addition. No plan ceremony.
- **Delegation or agentic brief** (multi-step, tools, unattended time): apply the six slots below. Full spec in ONE turn; drip-feeding requirements across turns measurably reduces performance.
- **Standing prompt** (system prompt, CLAUDE.md, skill): apply the delete list hardest. Bloated standing instructions cause the model to ignore the rules that matter. Deletion test per line: "would removing this cause a mistake?" If not, cut.

## The six slots (what a delegation brief must contain)

1. **Intent and why**: one or two sentences of motivation. "Your response will be read aloud by TTS, so no ellipses" beats "NEVER use ellipses"; the model generalizes correctly from reasons.
2. **Outcome and done-state**: the measurable end condition and stopping rule. "Done means the full test suite passes and one end-to-end cycle succeeds on the simulator," never "make it work."
3. **Source of truth**: name the files, APIs, docs, or live systems that ground the work, as pointers not pastes. Require reading before speculating.
4. **Constraints and scope**: hard limits, out-of-scope list, and explicit breadth. Current models follow instructions literally and will not silently generalize; if a rule applies to every section, say "every section." Beware literal filters: "only report high-severity" will be obeyed at the cost of recall.
5. **Autonomy contract**: state once which actions are pre-authorized and where to pause, anchored on reversibility ("pause only for destructive or irreversible actions, real scope changes, or input only I can provide"). Do not enumerate fifty forbidden actions, and do not repeat "ask first"; repetition of permission rules causes needless approval requests.
6. **Verification in the environment**: give a check the model can RUN (tests, build, lint, screenshot diff, rubric) and require evidence, not assertions. For long runs, a separate fresh-context verifier outperforms self-critique. Do NOT write "double-check your work" for Opus 5/Fable-class models; they self-verify and the instruction causes over-verification.

## Delete on sight (2026 delete list)

- "Think step by step" / "explain your reasoning" / "show your thinking": built into reasoning models; on Fable 5 reasoning-echo instructions can trigger a refusal category. (Exception: still valid on non-reasoning fast paths.)
- ALL-CAPS, "CRITICAL:", "YOU MUST" stacking: tuned for 2023-24 undertriggering, now causes overtriggering. Plain "Use X when..." works. Keep emphasis as a scarce resource: one or two per prompt, maximum.
- Contradictions and duplicates: the single most expensive defect on reasoning models; they burn reasoning tokens reconciling forks like "prefer stdlib" vs "use packages when simpler." State each instruction once; when adding a rule, delete its older, softer sibling.
- Elaborate persona paragraphs: measured accuracy NEGATIVE on factual tasks. A one-sentence role for voice and audience is the surviving form.
- Prophylactic thoroughness or persistence nagging ("plan extensively before each call", "be thorough", progress-narration demands): current models are natively proactive; these now cause tool-call waste and over-analysis.
- Reflexive few-shot: zero-shot first on reasoning models; examples that conflict with instructions are a named failure mode. Keep 3 to 5 consistent examples only for format, tone, or structure steering.
- Kitchen-sink context: curate pointers, not dumps. Attention degrades as context grows even inside large windows.
- Prose doing a parameter's job: use effort/verbosity/structured-output controls where they exist instead of "be extremely concise" three times.

## Still true (do not overcorrect)

Explicit constraints, budgets, and output-format specs; delimiters (XML/markdown) for labeling inputs; numbered steps when order genuinely matters; positive instructions over negations ("write flowing prose" beats "no markdown"); query-last ordering for long documents; motivation behind every rule; "don't guess, read the file first"; named stop conditions in agent prompts. Lean means non-redundant, never implicit. And for high blast-radius operations (prod mutations, untrusted input, money), explicit rails and human gates remain mandatory regardless of model intelligence.

## Model dials (re-tune every release, never hardcode)

Steering direction flips between model versions (one release under-delegates to subagents, the next over-delegates; one narrates too little, the next too much). Treat behavioral steering lines as per-model calibration: when the model changes, first run the old prompt unchanged, observe, then adjust only what misbehaves. Do not carry "delegate more" or "be more thorough" forward as timeless advice.

## Output contract for this skill

When improving a prompt, return: (1) the improved prompt; (2) a change log where every edit names the move (slot added, deletion, contradiction resolved) so edits can be accepted or declined item by item; never silently rewrite someone's standing prompt; (3) if the same prompt shape has been written three or more times, say so and propose the mechanism (skill, hook, verifier loop) instead of a better one-off.

## The cheap heuristic

If the ask deserves more than one sentence, it deserves the full six slots. Measured on the author's own 6,300-prompt history: fully-briefed kickoffs ran at ~4.4 interruptions per 100 prompts; half-briefed ones (300 to 800 chars) ran at ~24.

## Sources

Anthropic: Prompting best practices, Prompting Claude Fable 5, model migration guide, Claude Code best practices, Effective context engineering, Building effective agents. OpenAI: GPT-5 / 5.1 / 5.2 prompting guides, GPT-5.6 prompt guidance, reasoning best practices, Codex prompting guide. Practitioners: Karpathy on context engineering, Lance Martin (context engineering for agents), Simon Willison (agentic engineering patterns, verification), HumanLayer 12-factor agents and ACE-FCA, expert-persona accuracy studies (arXiv 2512.05858), spec-driven development evidence.
