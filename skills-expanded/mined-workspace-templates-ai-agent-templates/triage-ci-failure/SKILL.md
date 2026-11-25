---
name: triage-ci-failure
description: Reads a failing CI log, finds the first real error behind the noise and proposes a specific fix you can approve.
disable-model-invocation: true
---

Triage the failing CI run: $ARGUMENTS (a log file, run URL or job name; if empty, use the latest failed run of the current branch).

1. Fetch the log. With the GitHub CLI use `gh run list --branch "$(git branch --show-current)" --limit 5` then `gh run view <id> --log-failed`. For other systems read the file the user pointed to.
2. Find the first error in time order, not the last. Skip warnings, deprecation notices and retry chatter. Note the job, step name and exit code.
3. Classify it: code bug, test failure, flaky test, dependency or cache problem, environment or secret missing, timeout, or runner outage.
4. Reproduce locally with the same command and versions the workflow uses. If it passes, compare Node, Python or tool versions and environment variables.
5. Read the workflow file for the failing step and the commits since the last green run (`git log --oneline <last-green>..HEAD`).

Report: the root cause in one sentence, the evidence (log lines with line numbers), the classification and a proposed fix as a diff. Do not edit files or re-run the pipeline until the user agrees.
