# pr-description

Draft a pull-request description from the branch diff, written from the
reviewer's side of the screen.

- **Summary**: one paragraph — what changes and why, in plain language.
- **What changed**: a short bulleted list grouped by area, not a file-by-file
  dump.
- **Testing**: how it was verified (commands run, scenarios exercised), or
  "not tested" stated honestly.
- **Risk / rollout**: anything reviewers should watch — migrations, feature
  flags, follow-ups.

Keep it scannable. Link the issue it closes; don't restate the diff line by line.
