Plan the ticket `$ARGUMENTS` (a GitHub issue number in `cov1983/portfolio`). Plan mode until the
Owner approves: no file edits and no commits before step 6 says so.

1. Read `docs/constitution.md`, `CLAUDE.md`, `GLOSSARY.md` and `docs/agents/skill-overrides.md`. Use
   the glossary's vocabulary in everything you write.
2. Read the ticket and its discussion: `gh issue view $ARGUMENTS --comments`. Follow its tasks in
   the order given; a comment from the Owner overrides the body.
3. For every spec section the ticket cites, open the file under `docs/spec/` and confirm its first
   line says `Status: approved` or `Status: amended`. A draft spec stops the planning: report which
   section is not approved and wait.
4. Read the plan the ticket names under `docs/plan/` and the ADRs under `docs/adr/` that touch the
   area; the plan of record wins over the ticket text where they differ, and a conflict between the
   spec and the code is written into the ticket under "Blockers", not resolved silently.
5. Produce the execution plan: for each task, the files to touch, the test that proves it (which of
   the two seams: `tests/e2e` in a browser or `tests/model` under Node), and the order, riskiest
   first. Name the commit for each task (conventional commit, scope = module). Note every new
   dependency with its license and the reason, so the PR body can list it. When a task adds a CI
   job or a third-party action, list the repository settings it needs (dependency graph, code
   scanning, auto-merge, secrets, rulesets) and verify each with `gh api repos/{owner}/{repo}/...`
   now; a missing one is an Owner step in the plan, not a surprise on the first run. Check the
   action's inputs against its source for the mode it runs in, not its README.
6. Stop and wait for the Owner's approval of the plan. Once approved, the plan leaves the chat
   before implementation starts: for a single ticket, post it as a comment on the ticket
   (`gh issue comment $ARGUMENTS --body-file -`); when the work spans more than one PR or changes
   the process, the first commit on the branch writes it to `docs/plan/<name>.md` and the index.
   A plan that exists only in a chat or a local plan file does not exist.
