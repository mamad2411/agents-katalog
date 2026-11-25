---
name: standards
description: Give a project standards a machine keeps - measure what the code already does, propose ccm.standards.json (naming, API keys, the Zen design system), and from then on every write and commit is checked, refusing only what a change adds. Use when a project has no conventions, when asked to "set our standards", "enforce naming", "stop secrets in code", or after a review keeps finding the same deviation.
---

# Standards a machine keeps

A standard written in a document is followed until someone forgets it. A standard in `ccm.standards.json` is checked the moment an agent writes a file, again at every commit (whoever commits), and on demand for the whole tree. Only what a change adds is refused, so adopting a standard today never blocks work on the code written before it.

## 1. Measure before proposing

```
ccm standards init
```

It reads the code and says, pack by pack, how much of the project already follows each standard. It writes nothing. Show the person the numbers in plain words: "9 in 10 files already name booleans as questions", "two secrets are in the code today".

## 2. Propose, then let the team decide

The file is the team's, not yours. The proposal follows what most of the project already does:

| Pack | Proposed on when |
|---|---|
| `api-keys` | Always: a secret in code or in a commit is a leak in any project |
| `naming` | 80% or more of the files already follow it |
| `zen` | The project uses `@ciromaciel/components-kit` |

A pack the project mostly does not follow is proposed off: turning it on is a decision for the team, never yours. When they agree, write it:

```
ccm standards init --write
```

Commit `ccm.standards.json`, so every person, agent and editor reads the same standards.

## 3. Prove it refuses

Write one deviation on purpose (a `userID`, a key in a source file) and show the refusal and its fix. A standard that has never refused anything has not been tested.

## 4. Know where the project stands

```
ccm standards report
```

Every pack, active or not, with the files that deviate most. Use it to plan cleanups; never fix the whole tree in an unrelated change.

## The rules of the packs

- **naming**: `Id`, never `ID`; a boolean is an affirmative question (`isOpen`, `hasAccess`, `canEdit`, `shouldRetry`); a new script file is kebab-case. Strings and comments are not checked.
- **api-keys**: no secret in code; the env file is the right place and is never committed. Public keys pass.
- **zen**: radius 0, no shadows, the gray ramp only (`red.6` for errors), Montserrat 500/700/800/900, Tabler icons. Screens and styles only: an e-mail template keeps its hex colors.

## Exceptions

A line that is a real exception says so where the next person reads it: `// ccm: allow <the reason>`. A folder that is out of scope goes in `ignore` in the file. Never turn a pack off to get one change through.

## Secrets already in the history

Untracking a file does not remove what was pushed. Say so, and ask the person to rotate every key the report found: that is theirs to do, in each service.
