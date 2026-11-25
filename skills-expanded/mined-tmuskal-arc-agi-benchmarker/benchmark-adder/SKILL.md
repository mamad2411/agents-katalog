---
name: benchmark-adder
description: Given a benchmark repository URL (agentic envs like arc-agi, memory/eval benchmarks like longmemeval, QA/code/tool-use benchmarks, etc.), orchestrate the creation of a full Claude Code plugin that benchmarks the current harness setup against it. Wraps the babysitter:babysit skill with the benchmark-plugin-creator process.
---

# benchmark-adder

You are creating a new Claude Code plugin that wraps an arbitrary benchmark repository so a user can benchmark their current harness + plugins + skills + model + MCP servers against it.

This skill is a thin orchestrator. The heavy lifting is a multi-phase, convergent, spec-driven, TDD + adversarial-review babysitter process that lives at:

```
.a5c/processes/benchmark-plugin-creator.js
```

All you do here is:

1. Collect inputs from the user (or parse them from `$ARGUMENTS`).
2. Prepare the inputs file.
3. Invoke the babysitter `babysit` skill, pointing it at the process.
4. Hand control to the babysitter orchestration.

## Inputs

| Field | Required | Default | Example |
|-------|----------|---------|---------|
| `benchmarkRepoUrl` | yes | — | `https://github.com/arcprize/arc-agi` or `https://github.com/xiaowu0162/longmemeval` |
| `pluginName` | no | derived from repo | `arc-agi-benchmarker`, `longmemeval-benchmarker` |
| `outputDir` | no | `./plugins` | `./plugins` |
| `author` | no | empty | `Tal Muskal` |
| `targetHarnesses` | no | `["claude-code", "codex", "gemini", "opencode"]` | |
| `additionalRequirements` | no | empty | free-form extra requirements |
| `autoPush` | no | `false` | if `true`, the integration phase runs `git push` after committing the new plugin |

Parse `$ARGUMENTS` as `benchmarkRepoUrl` plus optional `key=value` tokens. If `benchmarkRepoUrl` is missing, ASK the user for it before proceeding.

## Steps

### Step 1 — Verify prerequisites

Check that the babysitter SDK is available and jq is installed. If not, tell the user to install them (the babysitter skill SKILL.md has the exact commands) and stop.

```bash
command -v jq >/dev/null 2>&1 || { echo "Install jq first."; exit 1; }
command -v babysitter >/dev/null 2>&1 || echo "babysitter CLI not found — the babysit skill will install it."
```

### Step 2 — Verify the process file exists

```bash
ls .a5c/processes/benchmark-plugin-creator.js >/dev/null || {
  echo "Missing .a5c/processes/benchmark-plugin-creator.js"
  exit 1
}
```

If it is missing, stop and report to the user — the skill cannot run without it.

### Step 3 — Write the inputs file

Write the inputs next to the process so babysitter can pick them up:

```bash
mkdir -p .a5c/processes
cat > .a5c/processes/benchmark-adder.inputs.json <<'JSON'
{
  "benchmarkRepoUrl": "<BENCHMARK_REPO_URL>",
  "pluginName": "<PLUGIN_NAME_OR_EMPTY>",
  "outputDir": "./plugins",
  "author": "<AUTHOR_OR_EMPTY>",
  "targetHarnesses": ["claude-code", "codex", "gemini", "opencode"],
  "additionalRequirements": "<FREE_FORM_OR_EMPTY>",
  "autoPush": false
}
JSON
```

Replace the placeholders with actual values parsed from `$ARGUMENTS` or collected from the user. Leave optional fields as empty strings if not provided — the process has defaults.

### Step 4 — Invoke the babysitter:babysit skill

Use the `Skill` tool with `skill: "babysitter:babysit"`. Pass arguments pointing at the process and inputs:

```
skill: babysitter:babysit
args: --process-file .a5c/processes/benchmark-plugin-creator.js \
      --entry .a5c/processes/benchmark-plugin-creator.js#process \
      --inputs .a5c/processes/benchmark-adder.inputs.json \
      --harness claude-code
```

The babysitter skill will:

- install / verify the SDK at the repo-pinned version
- create a run directory under `.a5c/runs/<runId>/`
- iterate through the benchmark-plugin-creator phases
- surface breakpoints for user review (benchmark classification, architecture, etc.)
- produce the plugin in `./plugins/<pluginName>/` plus a spec folder alongside it
- register the new plugin in `.claude-plugin/marketplace.json`
- update the top-level repo `README.md` to list the new plugin
- `git add` + `git commit` the new plugin, marketplace entry, and README update (and `git push` if `autoPush=true`)

### Step 5 — Report back

Once babysitter finishes (or yields a breakpoint), report to the user:

- run id and `.a5c/runs/<runId>/` path
- path to the generated plugin
- final convergence score and ship-ready flag
- any remaining tech debt from the final adversarial review

## Notes

- This skill does NOT run the generated benchmark plugin. It only creates it. After creation, the user installs it as a normal Claude Code plugin and runs its own `/setup` and `/run-benchmark` skills.
- The process is designed to converge to >=99% spec parity per phase, with 3 converging parts per phase (plan, build, refine) and an adversarial review that can include online research.
- Supported benchmark families: agentic-env, memory-eval, dataset-qa, code-eval, tool-use, generic. The process auto-detects and branches accordingly in Phase 4.
- Reference for plugin layout: `specializations/meta/plugin-creation` in the babysitter process library, and the existing `plugins/arc-agi-benchmarker/` in this repo.

## Example invocations

```
/benchmark-adder https://github.com/arcprize/arc-agi
/benchmark-adder https://github.com/xiaowu0162/longmemeval pluginName=longmemeval-benchmarker
/benchmark-adder https://github.com/openai/human-eval author="Tal Muskal"
```
