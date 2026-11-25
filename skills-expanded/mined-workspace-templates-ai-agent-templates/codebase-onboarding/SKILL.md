---
name: codebase-onboarding
description: "Builds a written map of an unfamiliar repository: entry points, layers, conventions, the commands that work, plus the areas most likely to break."
---

# Codebase onboarding

Read, run and map. Change nothing in the repository.

## Steps

1. Identify the project: languages, frameworks, package manager and build tool from manifests and lockfiles. List top-level directories with one line on each.
2. Find how to run it: the README, `Makefile`, `package.json` scripts, `docker-compose.yml` and CI config. Try the install, build and test commands. Record exactly which worked and which failed, with the error.
3. Find entry points: `main`, server bootstrap, route tables, job and queue consumers, CLI commands, scheduled tasks. Trace one request or command from entry to storage and back, naming each file it passes through.
4. Describe the layers and the data model: the main entities, where they are defined, and where the database schema and migrations live. Note external services and the config or environment variables each needs.
5. Read conventions from the code itself: naming, error handling, logging, how tests are laid out, how dependencies are injected. Quote one example file for each.
6. Find the risky areas. Use `git log --since=1.year --name-only` to count the files that change most. Look for large files, deep nesting, clusters of unfinished-work comments, modules with no tests, and code that is imported everywhere.
7. Write the map in a file the user names, or print it if none is named, using these headings: Overview, Run it, Entry points, Layers, Data, Conventions, Risky areas, Open questions.

## Rules

- Every claim cites a path. Mark anything inferred as a guess.
- Do not install global tools or run anything that writes to databases or external services.
- Keep the map under 120 lines.

## Report

The map, the commands that worked, and the three files to read first.
