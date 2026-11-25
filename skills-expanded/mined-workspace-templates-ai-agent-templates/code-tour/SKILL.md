---
name: code-tour
description: "Gives a new developer a guided tour of the repository: layout, entry points, request flow, how to run it and where the risky parts are."
disable-model-invocation: true
---

Give me a guided tour of this repository. Focus: $ARGUMENTS (the whole project if empty).

1. Read the README, the manifest files, CI config and the top two levels of the tree. Identify languages, frameworks, build tool and deployment target.
2. Find the entry points: main files, route tables, job runners, CLI commands.
3. Trace one real request or command from entry to the database or output. Name every file on the path with `file:line`.
4. Find how to run it: install, configure (list required environment variables, never print their values), start, and test. Run the safe ones and note what actually worked.
5. Mark the risk zones: files with high churn (`git log --since=6.months --name-only`), large or untested modules, and anything marked as pending or deprecated.

Output a tour with the headings **What it is**, **Map**, **One request end to end**, **Run it**, **Danger zones**, **First tasks for a newcomer**. Keep it under 600 words. Do not modify files; offer to save it as docs/TOUR.md.
