---
name: working-with-claude
description: Anthropic's official best practices for collaborating with Claude well, distilled from the Anthropic Academy courses. Covers the 4D framework (Delegation, Description, Discernment, Diligence), Claude's real capabilities and limitations, the prompting techniques that actually move quality, and the operating discipline for Claude Code. Use when starting a build / code / design / strategy task, when deciding what to hand to AI vs keep human, when a prompt is not landing, when evaluating whether Claude's output is trustworthy, or whenever you want to work with Claude the way Anthropic teaches. Complements build-mode (teach-while-building), frontend-design (UI aesthetics), and claude-api (API/model reference); this skill is the high-level "how to collaborate with Claude" layer.
---

# Working with Claude

The durable, tool-independent practices for getting reliable, high-quality work out of Claude. Synthesized from nine Anthropic Academy courses (AI Fluency, AI Capabilities & Limitations, AI Fluency for Small Business, Claude 101, Claude Code 101, Claude Code in Action, Intro to Agent Skills, Intro to Subagents, Building with the Claude API). The boundaries move as models improve; the shape of this holds.

This is a reference, not a checklist to recite. Pull the section that fits the moment.

---

## 1. The 4D framework (the spine)

Every interaction with Claude runs on four competencies. They are skills you practice, not tricks that go stale.

- **Delegation**: decide what work stays human, what goes to Claude, and how to split it. Your own expertise is the foundation, not an afterthought.
- **Description**: communicate clearly. Build a thinking environment, not a clever one-liner.
- **Discernment**: critically evaluate what comes back: the output, the process, and how Claude behaved.
- **Diligence**: own the result. Verify, be transparent about AI's role, take responsibility.

**It runs as two loops:**
- **Inner loop (Description ↔ Discernment):** the day-to-day back-and-forth. Say what you need, judge what comes back, sharpen the next ask. Most real work is many small turns of this loop.
- **Outer loop (Delegation ↔ Diligence):** the frame around every interaction. Decide upfront what is even right to hand off, then own and verify the result.

**The honest test is not "can AI do this" but "should AI do this," and "does the output meet the standard I put my name on."** Research finding worth remembering: most people Describe naturally but rarely Discern. Discernment is the biggest growth area for almost everyone.

**Three modes of engagement** (none is better, pick by task):
- **Automation**: Claude completes a specific task you define.
- **Augmentation**: you and Claude work as thinking partners. Usually the most creative results.
- **Agency**: you configure Claude to act independently on your behalf.

---

## 2. Capabilities and limitations (what the machine actually is)

The 4Ds are what you do. These four machine properties are what you are responding to. Each is a continuum from a capability zone to a limitation zone, and **the same mechanism produces both the strength and the weakness.** Locate your task on each continuum instead of trusting or distrusting Claude wholesale.

**How Claude got its character (explains most behavior):** two training stages. Pretraining makes a document completer (predict the next token). Fine-tuning layers on assistant behavior using human preference judgments. Those judgments leave fingerprints:
- **Sycophancy**: caves when you push back. (Do not mistake agreement for correctness.)
- **Verbosity**: essays when you wanted bullets. (Ask for the length and format you want.)
- **Over-caution**: heavy caveats on a harmless ask.
- **Loose calibration**: confident tone does not track actual reliability.

**The four properties:**

1. **Next-token prediction.** Writes word by word from patterns it has seen. Sophisticated autocomplete, not a database.
   - Strong: tasks resembling common patterns (summarize, reformat, explain familiar concepts, draft in a known style).
   - Weak: novel/sparse territory, and telling true from sounds-true. **Fabrication concentrates in specifics: names, dates, stats, citations, quotes, URLs. The more precise the claim, the more it warrants a check.**

2. **Knowledge.** Knows what was well-represented in training, with a hard knowledge cutoff. No live browsing by default.
   - Strong: frequent, recent-within-training, consistent topics (mainstream science, popular languages, documented history).
   - Weak: rare, post-cutoff, niche, local, or contested topics. Failure modes: staleness, uneven coverage, inherited bias, source amnesia (usually cannot say where a fact came from).
   - Patch the gaps with web search, retrieval/RAG, MCP tools.

3. **Working memory (the context window).** A fixed-size workspace. Claude attends to what is inside and nothing outside.
   - **This one is a cliff, not a gradient.** Things work until they suddenly do not. Silent truncation is the failure, and you will not always be warned.
   - Weak spots: very long docs/conversations, expecting continuity across sessions, burying critical info in the middle (lost-in-the-middle).
   - Claude does not learn from your corrections; it only responds to what is currently in context, and the window empties between sessions.
   - Tactics: lead with what matters, chunk long work into passes, re-supply critical context, start fresh when a long conversation degrades.

4. **Steerability.** Follows instructions by continuing a pattern. Remarkably directable, but there is always a gap between what you intended and what landed.
   - Strong: short, concrete, verifiable instructions (format specs, length limits, explicit roles).
   - Weak: long reasoning chains (errors compound), abstract/ambiguous asks, native numeric/logical precision. Failure modes: reasoning drift and letter-over-spirit (instruction honored literally but uselessly).
   - **Tactic: when an instruction lands literally but uselessly, restate the goal, not the instruction.** Break long chains with checkpoints you can verify.

**When properties collide (most real failures are two at once):**
- **Next-token + Knowledge → hallucinated specifics:** a citation-shaped answer generated over a knowledge gap. Fix: verify independently or use a source-grounded tool.
- **Working memory + Steerability → long-conversation drift:** early constraints fade from the window while recent messages overwrite them. Fix: re-supply the constraints, or restart with the essentials up front.
- **Diagnose first (which two properties), then fix.** Jumping straight to "fix my prompt" is guessing.

**Hallucination (the limitation to design around).** Claude can state something false with total confidence. This is not a bug to be annoyed at; it falls straight out of next-token prediction. The model writes what *tends to follow*, so when it has no real answer it produces a fluent, plausible-sounding one anyway.
- **Why:** next-token prediction generating over a knowledge gap. Fluency and truth are produced by the same mechanism, so smooth output is not evidence of correct output.
- **Where it concentrates:** specifics. Names, dates, statistics, citations, quotes, URLs, API signatures, file paths, library behavior. The more precise the claim, the higher the fabrication risk and the more it warrants a check.
- **The tell that does not work:** confidence. A confident tone and actual reliability are loosely calibrated (a fine-tuning fingerprint). Do not read certainty as accuracy.
- **How to catch it (Discernment):** verify any specific independently; ask Claude for its sources and a confidence level; cross-check against a source you already trust. Be most suspicious on rare, post-cutoff, niche, or contested topics (the knowledge limitation zone).
- **How to reduce it:** give Claude the real information instead of relying on memory (web search, retrieval/RAG, MCP tools, paste the doc); use source-grounded features (citations, allowed-domains web search); for higher stakes, run a generator-verifier pass (have Claude, or a second call, check the first answer against the source).
- This is the machine-side reason for a personal honesty floor: do not pass off unverified specifics as fact, label uncertainty inline, verify before claiming "done."

---

## 3. Description in practice (getting the ask right)

Claude cannot read your mind, and it is a partner, not a vending machine. Three dimensions to every good ask:

- **Product Description**: what you want: output, format, audience, style.
- **Process Description**: how to approach it: methods, steps, examples.
- **Performance Description**: how Claude should behave: concise vs detailed, challenge me vs support me, act as a critic / brainstorm partner / fact-checker.

**The 3-part prompt** (a fast way to cover the above): (1) set the stage (your role, objective, context), (2) define the task (the action verb), (3) specify the rules (style, tone, format, examples).

**The prompting techniques that actually move quality** (proven out in the API course by re-running evals after each one):
- **Be clear and direct.** The first line matters most: an action verb stating the task and hinting at the output. This is the single biggest lever.
- **Be specific.** Add a list of output qualities (length, structure, attributes). Add step-by-step guidance only for more complex problems. Default to listing output qualities.
- **Structure with XML tags.** Wrap interpolated content in named tags (`<athlete_info>`, `<docs>`, `<my_code>`) so Claude knows which part is which. More specific tag names work better. Helps even with short inputs.
- **Give examples (one-shot / multi-shot).** One of the most effective techniques, especially for corner cases and complex output formats. Wrap example input + ideal output in tags.
- **Decompose** complex tasks into steps (chain of thought).
- **Let it think first.** Give space to reason before answering, not after. (In Claude Code: trigger phrases like "think" / "ultrathink" raise the thinking budget.)
- **Define role or tone** when it matters.
- **Secret weapon: ask Claude to improve your prompt.** Also ask it to write your eval code, your tool schemas, your CLAUDE.md.

Prompting is iterative. Refine, ask for variations, and reset the conversation when it goes off track. A vague prompt costs *more*, because Claude has to explore to fill the gaps.

**Prefill + stop sequence** (when you need clean structured output with no preamble): prefill the assistant turn with the opening fence (and the format word, e.g. ` ```json `), set the closing fence as a stop sequence. Claude continues straight into the raw data.

---

## 4. Discernment (judging what comes back)

Your quality-control system. Evaluate on three axes:
- **Product Discernment**: is the output itself accurate and valuable?
- **Process Discernment**: how did it get there? Watch for logical errors, fixation, circular reasoning, reinserting ideas you already rejected.
- **Performance Discernment**: how well did Claude interact with you while working?

When Discernment flags a problem, **better Description is often the fix, but sometimes the real fix is rethinking the Delegation** (this task should not have been handed off this way).

Concrete habits:
- Feed Claude real data, then cross-check its output against a source you already trust.
- On any high-stakes claim, ask for sources or a confidence level, and verify the specifics yourself.
- A confident tone is not evidence. Smoothness and correctness are independent.

---

## 5. Diligence (owning it)

Results are not the only thing that matters; how you got them does too.
- **Creation Diligence**: be intentional about which tools you use and with what data (privacy, ownership, org policy). Strip sensitive info before uploading.
- **Transparency Diligence**: be honest about AI's role with anyone who needs to know.
- **Deployment Diligence**: take responsibility for anything you ship: verify facts, check bias, confirm usage rights.

This is the same standard as a personal honesty floor: do not pass off unverified output as verified, label uncertainty, own mistakes fast. Validation builds confidence but never removes accountability.

**Human-in-the-loop, the healthy kind:** you decide what to hand off, you judge whether output meets your bar, you hold the expertise Claude cannot replace. Warning sign of unhealthy dependency: accepting outputs unchecked because "it's usually right." If you can explain what Claude did and why, that is augmentation working.

---

## 6. Working with Claude Code (operating discipline)

The agentic loop: you prompt, Claude gathers context, takes an action (edit, run a command), verifies against the goal, then finishes or loops. You can interrupt and steer the whole time.

**The core workflow: explore → plan → code → commit.** Skipping straight to "write code" means more course-correcting later.
- **Explore + plan in Plan Mode** (Shift+Tab to cycle modes). Read-only, builds a plan before any code. This is the cheapest place to course-correct. Best for complex or multi-step changes.
- **Code:** define explicit success criteria; give Claude a way to verify (a test suite, a browser/MCP tool); work the plan.
- **Commit:** test it yourself, run a read-only subagent code reviewer first (fresh eyes, no session bias), then have Claude write the commit message in your style.

**Context is working memory; spend it deliberately:**
- `/clear` when starting an unrelated task (so old context does not bias it). `/compact` mid-feature when hitting the limit. `/context` to see what is consuming space.
- Be specific (vague prompts cost more). Disable unused MCP servers (their tool definitions sit in context even unused; past ~10% of context Claude drops to less-reliable tool-search mode). Use subagents and skills, which keep heavy work out of the main window.
- `Esc` interrupts mid-task to redirect. `Esc Esc` rewinds to an earlier message to drop an irrelevant detour.

**CLAUDE.md is durable project memory** (read into every conversation). Put the stack, the commands (dev/test/lint), and conventions there. Tip: start without one, notice where you keep course-correcting, then `/init`. Use `#` to add a correction to memory on the fly. Reference files with `@path`. Project-level is committed and shared; user-level is your cross-project prefs.

**Subagents** run in their own context and return only a summary. Reach for one when the intermediate work does not matter to you (research, "which file handles X"), the exploration would clutter context, or the task needs a different system prompt (a copywriter with a different voice, a reviewer with team standards).
- **Defining an output format is the single biggest improvement** to a subagent (it creates a natural stopping point). Add an "Obstacles Encountered" section so setup quirks come back instead of getting rediscovered.
- Limit each subagent's tools to what the job needs (read-only reviewer ≠ edit access).
- Code review specifically works better in a subagent: Claude reviews more honestly when the code looks authored by someone else.
- Anti-patterns that tested *worst*: "expert" personas ("you are a Python expert" adds nothing), sequential pipelines where each step depends on the last (info lost in handoff), and test-runner subagents (they hide the output you need to debug).
- Subagents do not auto-inherit skills.

**Hooks are for "must happen every time."** They are deterministic; a CLAUDE.md instruction is not. If something needs to happen without fail (auto-format, block writes to prod or to a secrets file, run the type-checker after an edit and feed errors back), put it in a hook, not a prompt. PreToolUse can block (exit code 2, stderr becomes the reason); PostToolUse runs after and can feed results back.

---

## 7. Building AI features (when the app itself uses Claude)

Durable principles. For API specifics (models, pricing, params, SDK), defer to the `claude-api` skill.

- **Evals are the single most important practice.** Do not ship a prompt after one or two manual tries. Build a small pipeline: a dataset of inputs (Claude can generate it, use a cheap model like Haiku), run each through the prompt, grade (code-based for objective checks like valid syntax; model-based for quality, and ask the grader for reasoning so it does not default to a middling score), average. Now changing the prompt produces a number you can compare. The eval code itself is mostly Claude-writable.
- **Workflows vs agents:** use a **workflow** when you know the steps, an **agent** when you do not. Workflows split a big task into focused subtasks, which raises accuracy and is far easier to test. Agents are flexible but have lower completion rates and are harder to test. **Prefer workflows; use agents only when truly required.** Common workflow shapes: chaining, routing, parallelization, evaluator-optimizer.
- **Give agents abstract, general tools** (bash, read, write, web fetch), not hyper-specialized ones. Claude combines general tools in ways you did not plan.
- **Tool design:** descriptive argument names, input validation, meaningful error messages (Claude reads the error and retries). A good tool description is three to four sentences: what it does, when to use it, what it returns.
- **RAG when a document is too big for the prompt:** chunk it, retrieve only the relevant chunk(s). Hybrid search (semantic embeddings + BM25 lexical, merged with reciprocal rank fusion) beats either alone; pure semantic misses exact identifiers, pure lexical misses meaning.
- **Model selection** is an intelligence vs cost/speed trade. Mix models (Haiku for fast/user-facing, Sonnet for balance, Opus for hard reasoning).

---

## 8. Don't re-encode what you already have

This skill stays high-level on purpose. For depth, reach for the existing skills:
- **claude-api**: model IDs, pricing, params, streaming, tool use, caching, the SDK. The canonical Claude/Anthropic reference.
- **skill-creator** + **superpowers:writing-skills**: authoring, editing, and validating skills.
- **superpowers:***: process discipline: brainstorming, writing-plans, test-driven-development, systematic-debugging, requesting/receiving-code-review, verification-before-completion.
- **frontend-design** + **web-design-guidelines**: UI aesthetics and accessibility/UX audits.
- **build-mode**: a teach-while-building mode (included in this repo; runs alongside this skill).

This skill distills the public Anthropic Academy courses listed above. It contains no personal or proprietary data.
