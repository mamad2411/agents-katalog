Run a full taste audit on the specified files or components.

1. Activate the taste-engineering skill.
2. Spawn @agent-taste-auditor to analyze the target.
3. Run scripts/specificity-test.sh on the target directory.
4. Present the combined audit report with Taste Score.
5. If any element scores GENERIC, ask if I want to run a facelift.

Target: $ARGUMENTS
