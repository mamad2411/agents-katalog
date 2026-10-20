---
description: Run a multi-AI debate with full context accumulation (Grok + Gemini + Codex)
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Task
argument-hint: "<topic>" --rounds 4 --context <context-file> [--models grok,gemini,codex] [--output docs/debate.md]
---

Run a structured multi-AI debate using `scripts/debate.py`. Every round, every model receives the FULL original context plus ALL prior debate responses — ensuring genuine back-and-forth engagement. Focus: **gap identification** — identify the exact open gap, not proof strategies.

## Step 1: Parse Arguments

Extract from `$ARGUMENTS`:
- **topic** (required): The debate question/topic (in quotes)
- **--rounds N**: Number of rounds (default: 4)
- **--context file**: Path to context file (required — the shared knowledge base for the debate)
- **--models list**: Comma-separated models (default: grok,gemini,codex)
- **--output file**: Output path (default: docs/debate_TOPIC_DATE.md)
- **--timeout N**: Per-model timeout in seconds (default: 300)
- **--round-instructions file.json**: Optional JSON with per-round custom instructions

## Step 2: Verify Context File

If no `--context` file is specified or the file doesn't exist:
1. Ask the user what context to include
2. If appropriate, assemble context from existing files (e.g., progress summaries, code files, prior debate docs)
3. Write the assembled context to a temp file

The context file is CRITICAL — it's included verbatim in every prompt to every model in every round. It should contain all relevant information the models need to make informed arguments.

## Step 3: Verify Prerequisites

Check that the required tools are available:
```bash
# Check Grok API key
echo "GROK_API_KEY: ${GROK_API_KEY:+SET}"

# Check Gemini CLI
which gemini 2>/dev/null && echo "gemini: OK" || echo "gemini: NOT FOUND"

# Check Codex CLI
which codex 2>/dev/null && echo "codex: OK" || echo "codex: NOT FOUND"
```

If a model's CLI/API is not available, warn the user and suggest removing it from `--models`.

## Step 4: Run the Debate

```bash
python3 scripts/debate.py \
  --context "<context_file>" \
  --topic "<topic>" \
  --rounds <N> \
  --output "<output_file>" \
  --models "<model_list>" \
  --timeout <timeout>
```

This runs in the foreground so you can monitor progress. Each round:
1. Builds prompts with full accumulated context
2. Calls all models in parallel
3. Collects responses
4. Appends to transcript (fed to all models next round)
5. Writes output incrementally (safe against crashes)

**IMPORTANT**: This can take several minutes per round (especially with 3 models at 300s timeout each). Run with sufficient timeout.

## Step 5: Present Results

After the debate completes:
1. Read the output file
2. Summarize the key points of agreement and disagreement
3. Highlight any position changes across rounds
4. Present the consensus (if any) and remaining disputes
5. List the recommended next actions from the final round

## Example Usage

```bash
# Full 4-round debate on gap identification
/project:debate "What is the exact open gap in Tuza nu=4?" --rounds 4 --context docs/PROGRESS_SUMMARY_FEB8.md --output docs/debate_tuza_feb8.md

# Quick 2-round debate between Grok and Gemini
/project:debate "What is the precise unsolved conjecture here?" --rounds 2 --context docs/context.md --models grok,gemini

# With custom round instructions
/project:debate "Identify the open gap" --rounds 3 --context docs/design.md --round-instructions round_prompts.json
```

## How Context Accumulation Works

```
Round 1: Each model gets [CONTEXT] + [ROUND 1 INSTRUCTIONS]
Round 2: Each model gets [CONTEXT] + [ALL Round 1 responses] + [ROUND 2 INSTRUCTIONS]
Round 3: Each model gets [CONTEXT] + [ALL Round 1+2 responses] + [ROUND 3 INSTRUCTIONS]
Round N: Each model gets [CONTEXT] + [ALL prior responses] + [ROUND N INSTRUCTIONS]
```

This means by the final round, every model has seen everything everyone said. No information is lost between rounds.
