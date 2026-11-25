---
name: party
description: Compose the review party of this paper: list, add or remove catalogue personas, or create an expert of your own.
argument-hint: "[add|remove <id …> | new <id> \"<Name>\" <role…>]"
disable-model-invocation: true
---

The plugin answers the list, `add` and `remove` itself. What reaches you is `new`: `$ARGUMENTS` is `new <id> "<Name>" <role>` as the author typed it (without a quoted name, the id is the name; the role may be empty), and the plugin has written a skeleton to `party/<id>.md` in the paper folder (frontmatter: `name`, `short`, `role`, `category`, `colour`; then the persona's perspective and voice as the body; the plugin appends the party's shared ground rules itself).

Add this expert to the author's review party. Interview them, one question at a time, 3 to 5 questions: which field or profession, what this expert looks at and asks, what counts as evidence there, the mistakes outsiders make, the guidelines that apply, and how they speak. Then fill `party/<id>.md` in from the answers: a `role` of at most 80 characters, a body of 4 to 8 sentences, one voice line; write no text for the paper itself. Show the author the file. From the next turn on the expert is the `cowrite:<id>` agent, in the pane and summoned like the others; `/cowrite:brief <id>` tells it what to look for in this project.

If `$ARGUMENTS` does not start with `new`, the plugin's module did not answer: tell the author in one line that the CoWriting plugin needs a restart of Claude Code (or an update), and do nothing else.
