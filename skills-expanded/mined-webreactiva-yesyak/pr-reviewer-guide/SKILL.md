---
name: pr-reviewer-guide
description: Explains a pull request so the user and reviewers keep the mental map. It covers the intent, the decisions split into reversible and irreversible, the map of the system, the assumptions nobody verified, and where to look first if it fails in production. It answers first in the chat, then optionally as a PR comment. Use it whenever the user asks to understand a PR or branch, "explain what you built", "what should I know", "what did you assume", onboarding notes for reviewers, or a reviewer guide.
---

# PR reviewer guide

## The five questions

Answer these, in this order:

1. **What was the intent?** The problem, the goal and the principles you followed (for example, "do not break the public API", "secure by default", "small verifiable steps").
2. **Which decisions were taken?**
   - Irreversible: from the decision log, with why each one is irreversible.
   - Also list decisions that are irreversible in practice but have no record (implicit ones, for example no migration path). Say that they have no record.
   - Reversible: from the decision log, one line each.
   - Product decisions from the spec.
3. **What keeps the mental map?** A numbered list: the main parts of the system, where the data lives, the order of checks, sessions, users, configuration, how it starts, how tests are built, where the docs are. Include one small ASCII block for the most important flow.
4. **What was assumed without verification?** Be honest and specific: deployment platform, proxies, HTTPS, instance count, browsers and versions tested, runtime versions, native binaries, real data migrations, client behavior. Say what depends on each assumption.
5. **If it fails in production, where to look first?**
   - The logs: which messages and levels to search for.
   - Startup: warnings and fatal configuration errors.
   - A table with two columns, symptom and first suspect.

## Sources

Read the spec, the plan, the decision log, the reports in `.scratchpad/<slug>/`, the diff and the PR description before you write. Check every claim against them; do not answer from memory.

## Delivery

1. Answer in the chat first, in the user's language.
2. Save the text to `.scratchpad/<slug>/pr-guide.md`.
3. If the user wants it on the PR, translate it to the document language of `simplified-technical-language` and save it to `.scratchpad/<slug>/pr-guide-comment.md`. Post it with `gh pr comment <number> --body-file .scratchpad/<slug>/pr-guide-comment.md`, or on GitLab with `glab mr note <number> --message "$(cat .scratchpad/<slug>/pr-guide-comment.md)"`. Without these tools, use the tools of the environment.

4. Report the comment URL.
