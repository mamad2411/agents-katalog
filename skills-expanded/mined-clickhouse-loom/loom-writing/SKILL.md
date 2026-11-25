---
name: loom-writing
description: Plain technical English for commits, PRs, issues, release notes and announcements, review replies, code comments and docs, with a prose checker. Use before writing or posting them, or to make text read less generated. Owns wording; loom-release owns release publication.
metadata:
  internal: true
---

# Writing in Loom

Readers are maintainers who skim dozens of PRs, issues and comments a day. A text earns its place by saying something the diff, the code or the thread does not already say, in the fewest words that are still exact.

## Rules

1. **Lead with the fact.** The first sentence is the claim, the finding or the answer. No preamble ("This PR aims to…", "I wanted to raise…"), no summary at the end that repeats it.
2. **Concrete over general.** Name the op, field, file, setting, query or command. "Search drops pinned rows when `limit` < 3" beats "fixes an edge case in search".
3. **Every adjective has evidence.** "Fast", "robust", "safe", "scalable" need a number with the command that reproduces it, or the mechanism. Otherwise delete the adjective.
4. **Say why, once.** A commit says why; a code comment says why the code is the way it is; neither narrates what changed ("now", "previously", "updated to").
5. **Present tense, the system as it is.** History, dates and the path you took belong in the PR body, not in code, docs or comments.
6. **Plain words.** Write the word a senior engineer says out loud in a design review. The table below lists the words that mark text as generated.
7. **No performance of effort or emotion.** No "Great catch!", "I apologize", "Happy to help", "Let me know if…", "I have carefully reviewed…". A reply states what changed and where.
8. **Formatting serves skimming.** Bullets for parallel items, a table for options, code formatting for identifiers. No headings in a three-line comment, no bold on every other phrase, no emoji.
9. **Public text names no host, internal path, namespace, person, customer or production count** (`tests/unit/test_public_copy.py` enforces the repository side; you enforce the GitHub side).

## Words to drop

| Instead of | Write |
| --- | --- |
| leverage, utilize | use |
| robust, comprehensive, seamless, powerful | the property itself: "retries twice", "covers every read op" |
| ensure (as filler) | the check: "fails closed", "asserts that…" |
| enhance, improve (with no measure) | the change and its number |
| streamline, simplify (as a claim) | what was removed |
| delve, dive into, explore | read, check, measure |
| crucial, critical, essential, vital, key (as emphasis) | delete, or say what breaks without it |
| it's worth noting, note that, importantly | delete; state the point |
| in order to | to |
| a variety of, various, numerous | the count, or the list |
| facilitate, empower, enable (as filler) | the verb for what actually happens |
| going forward, at this point in time | delete |
| addresses, handles (vague) | fixes / rejects / retries / returns |
| holistic, cutting-edge, state-of-the-art, best-in-class | delete |

## Release notes and announcements

- Open with 3–5 user-visible outcomes for a feature release; a small patch can have fewer. Put required upgrade actions and compatibility changes near the top, then the grouped detail and full changelog.
- Explain each highlight through the previous behavior, resulting behavior, affected users and limits where relevant. Name the task a user can do or the failure they avoid; a list of merged pull request titles is supporting detail.
- Give a documented upgrade path and state affected versions, migrations, configuration steps or client requirements when applicable. Do not invent an update command or imply all packages and deployment modes become available together.
- Keep the subscriber announcement short: version and benefit, selected outcomes, required actions and known limits, then links to the full release, relevant docs and roadmap. Link a demo when one exists.
- Separate shipped capabilities from planned roadmap work. Support availability and verification claims with this version's publication and check results; an earlier successful release proves nothing about the next one.

Use [loom-release](../loom-release/SKILL.md#5a-publish-the-reviewed-summary-and-announcement) for carrying approved notes into the release page and publishing to the ongoing announcement discussion. Writing or reviewing text grants no permission to post it.

## Examples

Commit message:

```text
Bad:  Enhance search robustness by implementing comprehensive handling of edge cases
Good: Search keeps pinned rows when limit is below the pin count

      The pin pass ran after the limit, so a limit of 2 with three pins dropped one.
```

Review comment:

```text
Bad:  Great work overall! One small thing worth noting: it might be a good idea to
      consider potentially handling the case where the cursor could be empty.
Good: P2 server/memory/workers/usage_fold.py:88 — an empty cursor re-reads from the start, so a
      worker restart re-emits every event. Treat "" as "no cursor" and test the restart.
```

Reply to a review comment:

```text
Bad:  Thanks so much for the thorough review! I've gone ahead and addressed this.
Good: Fixed in 3f2a9c1: the cursor is now stored before the batch is emitted; the new test
      restarts the worker halfway through a pass.
```

Code comment:

```python
# Bad:  Robustly handle the case where the token might be missing (updated per review)
# Good: Revocation is checked before the cache: a revoked token must not hit a warm entry.
```

## Check before posting

Write the text to a file, then:

```bash
python3 .claude/skills/loom-writing/scripts/check_prose.py <file>...   # prints path:line, the phrase and a replacement; exit 1 on a hit
```

It flags the rows of the table that are filler in every use (the `FILLER` list in the script, which also holds rule 7's phrases), plus home and host paths, private addresses, internal host names and secrets, which it checks inside code blocks too, because pasted logs are where they leak. The other rows are yours to judge. Fix every hit or keep it on purpose (a quoted error message, a term of art such as "critical section"). Then read the text once as the reviewer would and cut any sentence that changes nothing for them.
