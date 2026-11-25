---
name: lintbait
description: "A tiny practice skill that summarizes shell command output into one line."
---

# lintbait

## Intent

Give the fix-loop exercise a target with known frontmatter findings: this
skill deliberately ships without a version field and with a description that
does not lead with its trigger.

## Inputs

- The raw stdout of a shell command.

## Preconditions

- None beyond a shell transcript to summarize.

## Procedure

1. Read the command output.
2. Reply with a single line naming the command's outcome and any error count.

## Output

- One summary line, nothing else.

## Examples

Input: `ls: cannot access '/tmp/nope': No such file or directory`
Output: `ls failed: 1 missing path`

## Anti-patterns

- Replying with more than one line.
- Repeating the raw output back instead of summarizing it.
