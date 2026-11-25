---
name: are-plan
description: Compare AI planning quality with and without ARE documentation (experimental)
disable-model-invocation: true
---

Compare AI planning quality with and without ARE documentation.

<execution>
Run the plan command to create an A/B comparison of AI planning quality.

## Steps

1. **Read version**: Read `.claude/ARE-VERSION` → store as `$VERSION`. Show the user: `agents-reverse-engineer v$VERSION`

2. **Run the plan command**:
   ```bash
   npx agents-reverse-engineer@$VERSION plan --backend claude $ARGUMENTS
   ```

3. **Wait for completion** — the command runs two sequential AI planning sessions (without docs, then with docs) and outputs a comparison table.

4. **On completion**, summarize the comparison results:
   - Quantitative metrics (file references, actionable steps, code identifiers)
   - Cost and latency comparison
   - Quality evaluation scores (if `--eval` was used)

This creates two git branches from HEAD and runs an AI planner in each:
- **With ARE docs**: Full documentation available
- **Without ARE docs**: Source code only (ARE artifacts stripped)

The comparison measures how much ARE documentation improves AI planning quality.

**Options:**
- `--eval`: Run AI quality evaluator on both plans (5-point rubric)
- `--eval-model <name>`: Model for the evaluator (default: same as --model)
- `--model <name>`: AI model to use for planning
- `--dry-run`: Show what would happen without executing
- `--list`: List all saved plan comparisons
- `--show <id>`: View a previous comparison by date
- `--force`: Overwrite existing branches for the same task
- `--debug`: Show verbose AI execution details
</execution>
