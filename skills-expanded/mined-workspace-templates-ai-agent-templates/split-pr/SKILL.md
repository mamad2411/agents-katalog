---
name: split-pr
description: Plans how to break a large branch into small pull requests, in an order where each one builds, passes tests and can merge alone.
disable-model-invocation: true
---

Split the current branch into smaller pull requests. Notes: $ARGUMENTS

1. Find the base with `git merge-base HEAD <default branch>`. Read `git diff --stat <base>..HEAD` and the commit list, then the diff by area.
2. Classify every changed file into a concern: pure refactor or rename, dependency or config change, database migration, new internal API, feature UI, tests, docs. Note which files must stay together because one does not compile without the other.
3. Propose an ordered series where each pull request builds and passes tests on its own, lands the risk early (refactors and migrations first, behavior last), and stays under about 400 changed lines. For each give a title, files, size and what depends on it.
4. Show the plan as a table and mention any file needing a split across two pull requests.
5. Do nothing yet. After approval, create one branch per piece from the previous one (`git checkout <base> -- <files>`), run tests for each, and keep the original branch intact.

Finish with the branch names, the merge order and a suggested description for each pull request. Never push or open pull requests unasked.
