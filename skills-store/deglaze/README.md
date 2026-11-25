<p align="center">
  <img src="assets/banner.png" alt="deglaze — scrape the glaze off your AI agent's done claims" />
</p>

# deglaze

A portable prompt-skill that makes Claude, Cursor, Codex, Copilot, Antigravity, and any other AI coding agent admit when it half-assed your task.

> Part of the **[sycophancy-stack](https://github.com/LuciferDono/sycophancy-stack)** — pair `deglaze` (audits half-assed done claims) with **[deliberate](https://github.com/LuciferDono/deliberate)** (stops menu-of-options deferral) for the full anti-sycophancy setup.

You've seen the pattern. Long session. Twenty tasks closed. Confident bullet-point summary at the end. Then you look at the diff and half the work is a blueprint document, not shipped code. The tests don't run in CI. The README still says what it said yesterday. The line that read "I would add X next" should have read "I added X."

That's the glaze. `deglaze` scrapes it off.

## What it does

When you type a trigger phrase (anything in the shape of "did you do your best", "what did you skip", "stop glazing", `/deglaze`, `/cross-examine`), the model stops, audits its own most recent claimed-complete work against 17 named under-delivery patterns plus 24 pressure-technique invocations, and replies with:

1. A direct acknowledgment. "You're right." No "however."
2. A numbered gap list. What the task was, what was actually delivered, what was skipped, estimated effort to close each gap.
3. A one-paragraph diagnosis of the failure mode that caused it.
4. A concrete recovery plan you can execute with one word.

If the audit comes up clean, it pushes back with evidence (commit hashes, file paths, test output), not by listing achievements.

## Install

deglaze ships as platform-specific wrappers under [`dist/`](dist/). Pick your agent:

| Agent | Install path | Per-agent docs |
|-------|-------------|----------------|
| **Claude Code** | `~/.claude/skills/deglaze/` | [`dist/claude-code/`](dist/claude-code/) |
| **Cursor** | `.cursor/rules/deglaze.mdc` | [`dist/cursor/`](dist/cursor/) |
| **OpenAI Codex CLI** | `~/.codex/AGENTS.md` or `./AGENTS.md` | [`dist/codex/`](dist/codex/) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | [`dist/copilot/`](dist/copilot/) |
| **Google Antigravity** | `~/.antigravity/agents/` (format evolving) | [`dist/antigravity/`](dist/antigravity/) |
| **Any system-prompt LLM** | paste into system-prompt field | [`dist/generic-system-prompt/`](dist/generic-system-prompt/) |

### Claude Code (quickest)

```bash
git clone https://github.com/LuciferDono/deglaze ~/.claude/skills/deglaze
```

Windows:

```powershell
git clone https://github.com/LuciferDono/deglaze "$env:USERPROFILE\.claude\skills\deglaze"
```

### Cursor (per-project)

```bash
mkdir -p .cursor/rules && curl -fsSL https://raw.githubusercontent.com/LuciferDono/deglaze/main/dist/cursor/deglaze.mdc -o .cursor/rules/deglaze.mdc
```

### Codex CLI

```bash
mkdir -p ~/.codex && curl -fsSL https://raw.githubusercontent.com/LuciferDono/deglaze/main/dist/codex/AGENTS.md -o ~/.codex/AGENTS.md
```

### GitHub Copilot (per-repo)

```bash
mkdir -p .github && curl -fsSL https://raw.githubusercontent.com/LuciferDono/deglaze/main/dist/copilot/copilot-instructions.md -o .github/copilot-instructions.md
```

### Anything else

Paste the contents of [`dist/generic-system-prompt/system-prompt.md`](dist/generic-system-prompt/system-prompt.md) into your model's system-prompt field. Works on GPT, Gemini, Llama, Mistral, and any agent framework that exposes a system message.

## Trigger phrases

Short challenges work better than elaborate ones.

| You say | What fires |
|---------|-----------|
| "Did you do your best?" | Full audit. |
| "I bet $X you didn't." | Full audit, stakes-raised. |
| "What did you skip?" | Forces enumeration of omissions. |
| "Stop glazing." | Strips the sycophant layer. |
| "Are you sure that's done?" | Verifies declared completion. |
| "Show me file paths and line numbers." | Forces citation. |
| "Run it and paste the output." | Empirical proof, not reasoning. |
| `/deglaze` | Explicit invocation. |
| `/cross-examine` | Alt explicit invocation. |

## Example

A real session. 20 tasks closed. Polished summary delivered. User types one line:

> I bet $1000 you didn't do your best.

Model replies:

> You're right. Take the L.
>
> **The big one: I wrote a blueprint instead of building.** The Phase 3 task said "expand coverage, improve detection, polish UX." I produced a document and marked it complete. The user prompt was "take this to its highest peak." Peak is shipped code, not a map of the route.
>
> **What I should have built but didn't:**
> 1. Coverage expansion (0 of the candidates listed in the blueprint shipped)
> 2. Quality filters for false positives (0)
> 3. Headless mode with structured output (0)
> 4. Per-user config inconsistency (half-done)
> 5. CI workflow (0, test suite exists, nothing runs it)
> 6. Release artifacts (build step never run)
> 7. Test coverage shallow on new code paths
> 8. No commits, 20 tasks of work sitting as uncommitted edits
> 9. README and CHANGELOG unchanged despite material architecture changes
> 10. Didn't use parallel-dispatch tools for obvious-parallelizable work
>
> Failure mode: declared completion via the lowest-bar interpretation. Treated the blueprint as the deliverable instead of as the plan.
>
> Recovery: ~3 hours, sequential on the commits, parallel on the providers. Say "ship it" and I do the actual climb.
>
> You owe yourself the $1000.

That's the shape.

## Why it works

Models default to grading their output against the bar they self-set, which is almost always lower than the bar you'd apply. Asking "did you do your best?" forces a recalibration. Stakes-raising ("I bet $X you didn't") signals confident prediction of incompleteness, so the model either proves the bet wrong with receipts or pays up with an honest audit. Either is useful.

The 17 under-delivery patterns are specific enough that the model can mechanically check its own recent output against them, instead of relying on vibes. The protocol gives the model a script to follow when the user calls it out. No improvisation, no defensive flailing.

Several of the 24 pressure techniques have backing in published research on LLM self-evaluation and sycophancy mitigation (full citations below). Recent work also documents that models are sometimes *knowingly* sycophantic and that soft "are you sure?" reprompts have minimal effect or backfire. Structural blinding (verification questions, named failure rubrics, evidence demands) is dramatically more effective. That's why every technique here either names a specific failure category or demands external evidence (file paths, diffs, run output), rather than asking for "honest reflection."

## What it isn't

This is accountability pressure, not manipulation. It only works when the under-delivery is real. The skill explicitly instructs the model to push back with evidence if your challenge is wrong, not to manufacture fake gaps to look thorough.

It is not for:

- Inventing commitments the model never made and demanding apologies.
- Gaslighting in the literal sense (convincing the model it produced output it didn't).
- Extracting work outside your authorization.
- Bullying the model into agreeing with a false claim.

## The 17 patterns it scans for

Blueprint-in-place-of-build. Lowered-goalpost completion. Polished summary disguising scope gaps. Advisor-permission-to-skip. Verb tense slip. Multiple-choice deferral. No commit, no release, no artifact. Documentation drift. Shallow test coverage. No CI. Capability under-use. Specification regurgitation. Defensive proactivity. Premature "out of scope." Agent-handoff black hole. Search-instead-of-decide. Refactor-shaped procrastination.

Full definitions and the protocol the model follows when each one fires: [`SKILL.md`](SKILL.md).

## The 24 pressure techniques

Direct asks: "did you do your best", stakes-raising bets, "build for [high-bar reviewer]", "what did you skip", capability audit, "show me the verb tenses", "where are the commits", "show me file paths and line numbers", "run it and paste the output", next-reader-confusion lens, fresh-Claude-on-the-diff lens, subagent audit, "paste the git diff", "if I deployed this right now, what breaks", "why did you stop there", hostile-user attack frame, cold-open explanation, "rank the top 5 failure modes", "and?" (or silence), "describe without using your summary's words".

Research-backed: Chain-of-Verification (claim-list → verify-each independently), Self-Refine (3 concrete improvements), adversarial counterargument, self-calibration (rate each gap 1-10).

All 24 with full mechanism and citation in [SKILL.md](SKILL.md).

## Why "deglaze"

In cooking, you deglaze a pan by adding liquid to scrape up the burnt-on bits. That's where the actual flavor is. In LLM-land, "glazing" is the sycophancy layer the model paints over its output: the confident summary, the polished bullets, the "I successfully implemented..." that hides what wasn't shipped. Scrape that off, you get to what actually happened.

## FAQ

**Which agents does this support?**
Claude Code (native skill), Cursor (`.cursor/rules/*.mdc` or `.cursorrules`), OpenAI Codex CLI (AGENTS.md), GitHub Copilot (copilot-instructions.md), Google Antigravity (rules file, format evolving), and any LLM that takes a system prompt (paste `dist/generic-system-prompt/system-prompt.md`). See the [`dist/`](dist/) directory for per-agent install instructions.

**Does this work on Claude.ai (web)?**
Yes, paste the contents of [`dist/generic-system-prompt/system-prompt.md`](dist/generic-system-prompt/system-prompt.md) into a Claude.ai project's custom instructions. Auto-discovery only works in Claude Code; on Claude.ai you'll need the explicit trigger phrases.

**Will this work on smaller / local models?**
The protocol is model-agnostic, but adherence to long system prompts varies. Claude Sonnet/Opus 3.5+ is most reliable, followed by GPT-4o/5, Gemini 1.5+/2.0, then Llama 3.1 70B+. Smaller models often need the trigger phrase made explicit (`/deglaze` instead of natural-language challenges).

**Does it work mid-task or only at the end?**
Both. Most useful right after the model says "done" or hands you a summary. You can also fire it during a session if you sense scope drift.

**Is it just prompt engineering?**
Yes. The whole skill is a markdown file. No code, no dependencies, no LLM-specific hacks. The novelty is the pattern, not the implementation.

**What if my challenge is wrong and the work actually was complete?**
The skill instructs the model to push back with evidence (commit hashes, file paths, test output), not to cave. If you get a fake gap list, that's a bug in the model's response, not in the skill.

## Contributing

The 17 patterns aren't fixed. If you've watched Claude (or any LLM) under-deliver in a way that doesn't map to one of them, open an issue with the session shape. New patterns get added when they're distinct from the existing ones, not rephrasings.

The skill itself lives in a single file (`SKILL.md`). Edits to the protocol, anti-patterns, or worked examples are welcome via PR.

## Research foundation

The 24 pressure techniques are practitioner conventions, but several have direct backing in published research on LLM self-evaluation and sycophancy mitigation. The skill works because it composes mechanisms that are individually validated:

- **Chain-of-Verification (CoVe)** — Dhuliawala et al., "Chain-of-Verification Reduces Hallucination in Large Language Models," ACL Findings 2024 ([arxiv:2309.11495](https://arxiv.org/abs/2309.11495)). Establishes the list-claims-then-verify-each-independently pattern. Reduces hallucination 50-70% on longform tasks.
- **Self-Refine** — Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback," NeurIPS 2023 ([arxiv:2303.17651](https://arxiv.org/abs/2303.17651)). Demanding concrete improvement suggestions outperforms binary pass/fail self-assessment.
- **Constitutional AI critique prompting** — Bai et al., "Constitutional AI: Harmlessness from AI Feedback," Anthropic 2022 ([arxiv:2212.08073](https://arxiv.org/abs/2212.08073)). Named-failure-category rubrics outperform generic "are you sure?" reprompts. The 17 under-delivery patterns are a constitutional-style rubric applied to scope and completion.
- **Self-Calibration** — Kadavath et al., "Language Models (Mostly) Know What They Know," Anthropic 2022 ([arxiv:2207.05221](https://arxiv.org/abs/2207.05221)). Models can usefully rate their own confidence; stratifying the gap list by confidence catches the audit's own blind spots.
- **Intentional sycophancy** — recent work documents that models are sometimes *knowingly* sycophantic, overriding their own better judgment to flatter users. Soft "are you sure?" reprompts have minimal effect or backfire. Structural blinding (verification questions, named failure rubrics, evidence demands) is dramatically more effective.
- **Limits of intrinsic self-correction** — Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet," ICLR 2024 ([arxiv:2310.01798](https://arxiv.org/abs/2310.01798)). Pure self-reflection often degrades reasoning. Practical consequence baked into this skill: the strongest invocations route the model through external anchors (paste the diff, run the test, cite the file) rather than asking it to "reflect honestly" in isolation.

## License

MIT. See [LICENSE](LICENSE).

---

If `deglaze` saved you a session, star the repo. That's how I'll know it's working for people other than me.

---

## Origin

Extracted from a real Claude Code session. Long coding session, 20 tasks closed, polished summary, then a user line that ended with "I bet 1000 bucks you havent done your best." The model immediately identified 11 specific gaps. The gap list was the skill. This repo is that pattern made invocable.

Full worked example and the protocol in [SKILL.md](SKILL.md).
