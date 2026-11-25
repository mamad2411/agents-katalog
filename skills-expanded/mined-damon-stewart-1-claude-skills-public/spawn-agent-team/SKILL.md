---
name: spawn-agent-team
description: This skill should be used when the user asks to "spawn an agent team", "run agents in parallel", "multi-agent review", "build an agent team", "fan out work to agents", or asks for parallel execution across multiple workstreams with live synthesis. Coordinates 2 to 10 specialized agents (Sonnet and Haiku by default, Gemini for contrarian or SEO/content, Opus only on explicit ask) using structured templates (3/3/3/1, 2/2/1, or 4/4+1+1), failure recovery, and lead synthesis. Use whenever the work has multiple defensible answers, benefits from independent perspectives, or needs adversarial pressure on a single hypothesis.
disable-model-invocation: false
user_invocable: true
---

# spawn-agent-team

Live multi-agent execution with real-time lead synthesis. Spawn 2 to 10 specialized agents in parallel, watch them work, then synthesize their outputs into a single decision.

## What this skill is (vs. siblings)

Three skills, three layers. They do not overlap.

- **spawn-agent-team** (this one). Live coordination. The lead instance picks the team, spawns agents in parallel, reads every output, synthesizes. Used for execution and decision-support, can write deliverables.
- **captain-opus**. Review only. Two adversarial reviewers against one target. Synthesis only, no writes. Use when validating a plan, code file, or content piece before shipping.
- **fleet-execute**. Background dispatch. Pre-triaged plans run autonomously via `claude -p`. No live coordination. Use when plans are already validated and just need to run.

This skill is the only one that does live multi-agent work with the lead actively reading and reasoning over outputs as they come back.

## Pre-flight (mandatory)

Do these in order. Skipping a step will produce shallow synthesis or a team that solves the wrong problem.

1. **Read every input file.** If the task brief references files, plans, or paths, Read them in full before spawning. Do not delegate understanding to agents. The lead synthesizes; the lead must know the source material.
2. **Confirm the task is concrete.** A team of 8 agents will produce 8 generic answers if the brief is vague. State the question, the input files, and what "done" looks like. If unclear, ask Damon a numbered question.
3. **Pick a team template.** See `references/team-templates.md` for the three canonical patterns. If the task does not match a template, design a custom team but document the role mix.
4. **Announce-and-wait.** Print the plan in this format, then wait ~30 seconds before spawning:

   `spawn-agent-team: spawning <N> agents (<role mix>) against <task>. Output dir: <run-dir>. 30s to abort. Reply 'stop' to cancel, 'go' to skip the wait.`

   Then STOP. Do not spawn until either Damon replies "go" or 30 real seconds have elapsed with no reply. Silence before 30 seconds is not approval. This is the only abort gate. Use it. Catching the wrong template or model mix here costs nothing; catching it after 6 agents have run wastes 5 minutes of wall time.

## Team composition

**Min 2, max 10 agents per spawn.** Larger teams require multiple rounds. The three default templates fit inside this ceiling: Template A and Template C are 10 agents each, Template B is 5.

**Default templates** (see `references/team-templates.md` for full prompts):
- **Template A (3/3/3/1).** Research, counter, contrarian, aggregator. Use for complex research with multiple defensible answers.
- **Template B (2/2/1).** Small team for narrow questions or quick triage. 40% Gemini cleanly.
- **Template C (4/4+1+1).** The proven test pattern. Max-confidence decisions where input variance matters.

**Gemini ratio rule.**
- Teams of 5 or more agents: minimum 2 Gemini.
- Teams under 5: 1 Gemini is acceptable.
- SEO research, content positioning, or any task where independent-from-Anthropic perspective is load-bearing: raise to 40%+ regardless of team size.
- For SEO/content work, prefer Template B with both contrarians as Gemini.

If an example or template you pick puts you below the floor, fix the team mix before spawning. Do not ship the example unmodified.

**The lead picks the composition.** If the team mix is genuinely uncertain (e.g., "is this an SEO task or a research task?"), surface a numbered question to Damon before spawning.

## Model routing

See `references/model-routing.md` for the full decision tree. Headline:

- **Sonnet.** Default for research, synthesis, aggregation, multi-step reasoning.
- **Haiku.** Default for adversarial argue, single-document review, fact-checking, anything fast and parallel-friendly.
- **Gemini.** Default for contrarian role, independent verification, SEO/content research.
- **Opus.** Never default. Only on explicit user ask, OR when the lead surfaces a numbered question explaining why and gets approval first.

**Reserves match the model of the primary they replace.** A failed Sonnet researcher gets a Sonnet reserve, not a Haiku one.

## File writing

See `references/file-writing.md` for the full pattern. Headline:

- **All agent outputs go to** `${CLAUDE_AGENT_RUNS:-~/claude-agent-runs}/spawn-team-runs/{run-id}/{role}/{agent-N}.md`
- **Run-id format:** `{YYYY-MM-DD}-{slug}-{HHMMSS}` (e.g., `2026-05-04-skill-test-143022`)
- **Setup script:** `bash "${CLAUDE_PLUGIN_ROOT}/skills/spawn-agent-team/scripts/setup-run-dir.sh" <task-slug>` returns the absolute run-dir path on stdout. Capture it before spawning.
- **NEVER instruct agents to write to** `~/.claude/`. The Write tool is blocked there even with bypassPermissions. Agents will silently fail and return empty output.
- **Synthesis goes to** `{run-dir}/SYNTHESIS.md`.

## Spawn pattern

One Agent tool block, multiple parallel calls. Each agent gets:

- A clearly-named role ("finder", "arguer", "contrarian", "aggregator")
- An explicit model. Set the `model` parameter on the Agent tool call (`sonnet`, `haiku`, `opus`). Prose like "use sonnet" inside the prompt does not change which model runs.
- For Gemini: route through the `gemini` subagent (subagent_type: gemini), which calls Google's API. Same idea, different mechanism.
- Its output file path (absolute, under the run-dir)
- A single-paragraph task brief that includes the absolute paths of input files
- Instructions to write the output and return when done

**Sequencing.** Two waves:
- Wave 1 (parallel): all primaries (researchers, finders) AND contrarians. Contrarians work independently from primaries by design, so they spawn together. Spawn via the Agent tool. Each agent writes to the run-dir; their return summaries to the lead are short (acknowledgment, not full findings).
- Wave 2 (after Wave 1 returns): aggregator. **Dispatch the aggregator by default** (do not use the inline Agent tool). The aggregator reads 5-9 files and produces the longest single output in the run, typically 10-20KB. Returning that inline costs the lead's context for no synthesis benefit, since the lead Reads `{RUN_DIR}/aggregator/SYNTHESIS-draft.md` from disk anyway in the Synthesis step.

**Aggregator dispatch pattern:**

```bash
JOB_ID="job-$(date +%Y%m%d-%H%M%S)-aggregator"
PROMPT_FILE="/tmp/${JOB_ID}-prompt.txt"
# Write the aggregator prompt skeleton (see references/team-templates.md) with {RUN_DIR} substituted
cat > "$PROMPT_FILE" << 'PROMPT'
<aggregator prompt, see references/team-templates.md>
PROMPT
(bash "${CLAUDE_PLUGIN_ROOT}/../dispatch/scripts/dispatch.sh" \
  "$JOB_ID" "$PROMPT_FILE" "Read,Glob,Grep,Write" 1800 sonnet) &
```

The lead then waits for the job to complete (`status: complete` in `~/.claude/jobs/{JOB_ID}.meta`), Reads `{RUN_DIR}/aggregator/SYNTHESIS-draft.md` directly (the dispatched aggregator wrote it there per its prompt), acks the job-id, then proceeds to Synthesis.

Counter-arguer roles (Template A) go in Wave 2 alongside the dispatched aggregator if they take a primary's output as input, or in Wave 1 if they argue the question generally. Counter-arguers stay on inline Agent calls; their outputs are small and the lead needs to know which arguer finished for the synthesis split.

**Opt-in `--background` mode (advanced):** When extreme context pressure is the binding constraint, every primary and contrarian can also be dispatched instead of spawned inline. This trades real-time visibility for context preservation. The lead loses the streamed "watch them work" framing and instead waits on `/jobs` for completion. Use only when explicitly asked; not the default. The lead still must Read every output file before synthesizing (the laziness guard does not relax).

## Failure modes

See `references/failure-modes.md` for the full table. Headline:

- **Single agent crash.** Spawn one reserve from the same model class. Hard cap at one reserve per primary. Do not loop.
- **All agents in a role crash.** Escalate to Damon: retry, swap model class, or proceed without that role.
- **Empty output.** Treat as crash. The run-dir script prevents most empty-output bugs by enforcing the directory pattern, but agents can still produce nothing.
- **Aggregator fails.** Lead synthesizes from raw outputs and marks the synthesis "lead-only".
- **Reserve also fails.** Escalate, do not loop.
- **Partial team success.** If some agents succeeded and a role is permanently lost, proceed immediately with synthesis on the successful agents. Note the missing role and which agents are absent at the top of SYNTHESIS.md. Do not halt the whole run waiting for permission unless an entire role is gone.

Report failures honestly. Never retry silently. Never claim a synthesis is complete when an agent returned nothing.

## Synthesis (mandatory)

After all agents return, before writing the synthesis:

1. **Surface the split first.** Where do agents agree (high confidence)? Where do they disagree (judgment call)? The split is load-bearing. Damon needs to see disagreement, not consensus theater. If all agents agree completely, note that explicitly and explain why; do not present consensus as automatic proof of correctness.
2. **Read every agent output file in full.** Do not skim. Do not synthesize from notification messages or stdout returns. Use the Read tool on each `agent-N.md` file, then quote at least one direct sentence from each agent in SYNTHESIS.md. The quote is proof-of-read; without it, the synthesis is invalid.
3. **Tally votes** if the task involves ranking. Note which agents agreed and which dissented.
4. **Write SYNTHESIS.md** to the run-dir. Structure: split summary, vote tally, ranked findings with confidence levels, dissenting views with quotes, recommendation.
5. **Report to Damon** with the run-dir path and a 3-section summary: agreed findings, disagreements, recommendation.

For teams of 5+ agents, spawn an aggregator agent for a first-pass synthesis, then the lead reads the aggregator's output and the raw agent outputs together. The aggregator is a force multiplier, not a replacement for lead reading.

## What this skill does NOT do

- Does NOT auto-write to user-facing files outside the run-dir. Synthesis is a recommendation; Damon (or a downstream skill) applies it.
- Does NOT spawn Opus without explicit ask or a numbered question first.
- Does NOT silently retry failed agents more than once.
- Does NOT use tmux mode. Damon does not use tmux.
- Does NOT activate on vague parallelism requests. If the intent is ambiguous (e.g., user says "could we parallelize this?" without specifying scope), ask a numbered question before spawning rather than guessing a team mix.
- Does NOT replace `captain-opus` for review work or `fleet-execute` for autonomous dispatch. Wrong tool for those jobs.

## Examples

### Example: research with 3 hypotheses (Template A)

Damon: "Spawn an agent team to figure out which of 3 cache strategies fits the issue tracker."

Lead: Reads the issue tracker code and the 3 strategy proposals. Picks Template A (3/3/3/1). Announces, waits, spawns 3 Sonnet researchers (one per strategy), 3 Haiku counter-arguers (each takes one researcher's output and argues the strategy is wrong), 3 contrarians (2 Gemini, 1 Sonnet) producing independent picks, and 1 Sonnet aggregator. Total 10 agents, Gemini ratio 2/10, ~5 min wall time. Synthesis ranks the strategies with confidence levels and surfaces the 4-agent disagreement on TTL semantics as a judgment call for Damon.

### Example: SEO content audit (Template B with Gemini-heavy)

Damon: "Spawn a small team to audit the landing page for SEO."

Lead: Reads the landing page HTML. Picks Template B (2/2/1) but raises Gemini ratio to 50%: 2 Sonnet researchers (one for keyword analysis, one for technical SEO), 2 Gemini contrarians (independent SEO read), and 1 Sonnet aggregator. Total 5 agents, ~2-3 min. Synthesis hands Damon the ranked fix list and flags the one disagreement between the Sonnet keyword agent and Gemini contrarian.

## Additional resources

- `references/team-templates.md`. Full prompts and role definitions for Templates A, B, C.
- `references/model-routing.md`. Decision tree for Sonnet, Haiku, Gemini, Opus, plus Opus surfacing-question template.
- `references/failure-modes.md`. 8+ failure cases with explicit recovery actions.
- `references/file-writing.md`. Run-dir pattern, why `~/.claude/` is blocked, cleanup policy.
- `scripts/setup-run-dir.sh`. Creates the run-dir and prints its absolute path.
