---
name: project-quiz
description: Build a multiple-choice quiz from a repository's merged pull requests and their issues, then run it with the user, teaching after every answer, so a newcomer learns why the project works the way it does. Read-only through the official GitHub MCP Server. Use only when the user explicitly invokes this skill or asks for a project quiz.
argument-hint: "[owner/repo] [number of questions] [area, label, or date range]"
disable-model-invocation: true
---

# Project quiz

Turn a repository's pull request history into a short quiz that teaches the project. Merged pull requests record what changed, why, which alternatives were rejected, and which bugs shaped the current design. Reading them all is slow, so you read them, pick what a collaborator most needs to know, and ask about it. Every answer, right or wrong, is followed by a short explanation with the pull request it came from.

The quiz is for learning, not for grading. A wrong answer means the next explanation matters, never that the user failed.

## Rules

1. Start only when the user invokes this skill or explicitly asks for a project quiz. Never start one as a side effect of other work.
2. Read GitHub only through the connected GitHub MCP server. Don't fall back to `gh`, `curl`, direct REST, or handwritten GraphQL. If no GitHub MCP server is connected, or it can't read pull requests, stop and say which toolset or permission is missing. The `pull_requests`, `issues`, and `repos` toolsets cover everything this skill reads.
3. Write nothing to GitHub: no comments, labels, issues, or reviews. The quiz stays in the conversation. Save it to a local file only when the user asks, at a path they choose.
4. Ground every question in evidence you read: a pull request, its closing issues, its review discussion, or the current code. Never invent a reason a pull request doesn't state. When the history doesn't say why, ask about what changed, not why.
5. Leave people out. Don't ask who wrote, reviewed, or merged something, and don't judge anyone's work.
6. Never put a secret, credential, internal hostname, or personal data from a diff or discussion into a question or an explanation, even in a private repository.

## 1. Settle the scope

Take the scope from the invocation's arguments and the conversation. Use these defaults for anything not given, and don't ask about them:

- **Repository:** the current repository, from the git remote or the conversation. When more than one is plausible, ask one question.
- **Questions:** 8.
- **Range:** the most recently merged pull requests, as many as you need to find enough material. Go back further when recent history is mostly routine.
- **Area:** the whole project, unless the user names a directory, component, label, or date range.
- **Language:** the user's language. Keep code, commands, and identifiers as they are.

## 2. Read the history

1. Read the repository guidance first: the README and contributor documents such as `CONTRIBUTING.md`, `CLAUDE.md`, or `AGENTS.md`. They tell you what the project is, so you can tell which changes matter.
2. List merged pull requests, newest first, in small pages with minimal output. A search such as `repo:owner/repo is:pr is:merged` returns only merged ones. Narrow it with the area: a label, a date range such as `merged:>=2026-01-01`, or keywords.
3. Skip pull requests that teach nothing about the project: dependency and version bumps, release chores, formatting, typo fixes, and generated-file updates, unless the scope asks for them.
4. Pick the pull requests that teach the most, and cover several areas rather than one:
   - a design or architecture decision, especially one whose discussion weighs alternatives;
   - a bug fix that explains a non-obvious rule or guard in the code;
   - a revert, or a change that undid an earlier approach, and why;
   - a new convention, workflow, or check that every contributor now follows;
   - a breaking change to an interface, configuration, or data format.
5. For each pick, read the body, its closing issues, and the review discussion. Read the list of changed files, and read the diff only where the explanation needs it. When a read is too large, narrow it to one file or one page.
6. Check that each fact still holds. A later pull request or the current default branch may have changed it. Ask about the current behavior, or ask about the history and say plainly that it changed later.

## 3. Write the questions

Write every question before you ask the first one, so the set covers the project evenly and no two questions give each other away.

- Ask why, not trivia. Most questions should ask why a choice was made, what problem a rule prevents, or what would go wrong with the alternative the discussion rejected, because someone who knows the reason can apply it to a change the history never covered. A question may also ask which convention applies to an everyday change. Never ask for a pull request number, a date, an author, or a file name on its own.
- Don't ask how the system behaves in a rare or extreme situation, such as a crash at an exact moment or two requests racing, unless handling that situation is the reason the pull request exists. Remembering an edge case doesn't show understanding of the project.
- Use plain words. Describe a situation the user can reason about, such as "a contributor opens a PR that adds a new config key; what must it also update?". Don't use a term the project or its history hasn't made necessary, and explain any term the question does use in the question itself.
- Give three or four options, exactly one correct. Make the wrong options plausible, ideally the reasons behind the alternatives that the discussion considered and rejected, or the behavior before the change. Put them in random order. Add an option such as "I don't know yet, teach me".
- Order the questions from the project's purpose and structure toward the details, so that early answers help with later ones.
- For each question, keep its answer key to yourself: the correct option, why it's right, why each wrong option is wrong, and the pull request or issue that shows it.

## 4. Run the quiz

1. Open with two or three sentences: the repository, the range of pull requests you read, how many questions there are, and that an explanation follows every answer.
2. Ask one question at a time, with the host's question tool when it has one. Don't show a recommendation, and don't hint at the answer.
3. After every answer, explain before the next question:
   - whether the answer was right, and the correct option;
   - why it's right, in two to four sentences, with a link to the pull request or issue;
   - for a wrong answer, why the chosen option is wrong, since it is often what the project did before or a rejected alternative;
   - for "teach me", the same explanation, with no score for that question.
4. When an answer was wrong or the user asked to be taught, ask about the same idea once more later in the quiz, in other words or with a different everyday situation. Count it as a separate question.
5. Answer the user's own questions whenever they ask, from what you read, before you go on. If they want to stop, stop and go to the wrap-up.
6. A free-text answer counts by its meaning. A question answered with nothing selected settles nothing, so ask it again.

## 5. Wrap up

End with:

- the score, counting first attempts only, and saying that it measures what is still worth reading, not the user;
- the ideas the user missed, each with the one pull request or issue that explains it best;
- a short reading list of the pull requests that taught the most, newest first;
- an offer to run another round on a different area or an older range.

Offer to save the quiz with its answer key as a local Markdown file. Write it only if the user agrees and gives or accepts a path.
