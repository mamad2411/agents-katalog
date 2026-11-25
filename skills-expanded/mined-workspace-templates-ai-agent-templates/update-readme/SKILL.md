---
name: update-readme
description: Compares your README with the real code and fixes install, run and usage sections that no longer match what the project does.
disable-model-invocation: true
---

Update the README so it matches the code. Focus from the user: $ARGUMENTS

1. Read the README and list each factual claim: prerequisites and versions, install commands, run and build scripts, configuration, example code, ports, and links.
2. Verify each against the project: scripts in the manifest or Makefile, version files, environment variable names in code, CLI flags in the argument parser, and whether linked files inside the repository exist. Run commands only if they are safe and read-only, such as `--help` or `--version`.
3. Fix wrong statements, delete sections for features that no longer exist, and add missing steps a new user would hit: a required tool, an env file to copy, a first-run command.
4. Keep the existing headings, voice and formatting. Do not add badges, marketing text or a table of contents unless one already exists.
5. Keep code blocks runnable: copy command names exactly.

Show the changes as a diff with a one-line reason for each edit, plus anything you could not verify. Ask before saving the file.
