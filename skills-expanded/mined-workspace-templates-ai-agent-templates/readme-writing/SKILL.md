---
name: readme-writing
description: Writes or rewrites a README so a new developer goes from clone to a running app in minutes, with every command tested against the repo.
---

# README writing

Write for someone who has never seen this repository and wants it running before their coffee cools.

## Steps

1. Gather facts first. Read package.json, pyproject.toml, Makefile, Dockerfile, .env.example, the CI workflow and the existing README. The real install and test commands live there, not in your memory.
2. Note the prerequisites with exact versions (runtime, database, system packages) from lockfiles, `.nvmrc`, `.tool-versions` or CI.
3. Run the quick start yourself in order: install, configure, start, test. Record the command that actually worked and what a healthy start prints.
4. Draft in this order: one sentence on what it is and for whom; a screenshot or sample output if the project has any; Quick start; Configuration (a table of env variables with default and purpose); Common tasks (test, lint, build, migrate); Project layout (five to ten lines, top-level folders only); Contributing and license.
5. Keep every command in a fenced block that can be pasted as is. No prompt characters, no placeholders without a note on where the value comes from.

## Rules

- Never describe a feature you did not find in the code.
- Do not paste the whole API or architecture; link to docs instead.
- Delete badges that point to dead services.
- If a step failed on your machine, write the fix or the known issue under Troubleshooting.

## Report

Return the new README, the commands you verified, and a list of anything you could not run.
