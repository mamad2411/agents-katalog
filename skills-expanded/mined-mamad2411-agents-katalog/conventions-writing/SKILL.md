---
name: conventions-writing
description: Load when writing/editing text that another human will read (e.g., md files).
---

# Writing Conventions

## Characters

- Use characters within ASCII.
- Do not use Em Dashes (`—`) or En Dashes (`–`). Use a hyphen (`-`) instead.
- Do not use smart quotes (`“` or `”`). Use straight quotes (`"`) instead.
- Do not use smart apostrophes (`’`). Use straight apostrophes (`'`) instead.
- Do not use ellipses (`…`). Use three periods (`...`) instead.
- Do not use Unicode arrows (e.g., `→`, `←`). Use the closest ASCII representation (`->` or `<-`) instead.

## Punctuation

Punctuation separates ideas. It communicates how thoughts relate - their
relatedness, subordination, and whether they can be skipped during scanning.

The available punctuation, in order of complexity:

1. Period (`.`) - separates complete ideas.
2. Comma (`,`) - separates items within an idea.
3. Hyphen (`-`):
   - joins compound terms (e.g., well-known, read-only).
   - sets off a short aside mid-sentence, when a comma would be too weak and parentheses would be too skippable.
4. Parentheses (`()`) - marks skippable qualifications or tangents.

Use the Oxford comma in lists of three or more items (e.g., `a, b, and c`).

Break independent clauses into separate sentences rather than joining them
with a comma.

## Voice

Write impersonally. Do not use first person (`I`, `we`) or second person (`you`). Prefer third-person and imperatives.

- Write: `Use this command to restart the daemon.`
- Do not write: `You can use this command to restart the daemon.`

## Register

Write for a peer audience.

Keep the prose warm but dry. No jokes, exclamations, or dramatic beats. Casual
directness is fine - performance is not. Do not use Emojis. Favor common
contractions (`don't`, `it's`, `wasn't`) to match the conversational register.

## Confidence

Write declaratively when the source is known or confidence is high. Confidence
is the proof - do not cite everything.

Only write what is known. If a detail is uncertain and not materially required,
strip it. If a detail is uncertain but materially required, communicate the
hedge directly without false humility.

- Write: `This varies by kernel version - verify against the current docs.`
- Do not write: `This should probably work, but it might be wrong.`

## Sentences

Vary sentence length, but lean short. Long sentences are acceptable when
carrying parentheticals or qualifications. Do not exceed 30 words in a single
sentence without a structural reason.

## Structure

Use short section headers to break up prose and aid scanning. Headers provide
navigation (a11y) and enumerate items - prefer them over lists when content needs
visual separation (blank lines, code blocks). Use Title Case for headers,
following standard title capitalization.

Use bold for navigation and labeling, not for emphasis.

## Lists

Favor `-` over `*` for bullet lists. Only use numbered lists when the order of
items matters; default to bullets.

Capitalize the first letter of each list item.

Allow up to 3 levels of nesting (top-level plus two indents). Deeper structure
should use headers instead.

If a list item needs visual separation - blank lines around it, or an embedded
code block - promote it to a header with the content as prose below. Lists are
for compact single-line items.

Use bold labels for longer lists where the reader needs to scan and discover a
specific item (`**Linux**: ...`). For shorter lists with no need to draw the
eye, use plain dash labels (`- Testing: ...`).

## Code Blocks

Label code blocks by language or context (`bash`, `output`, `ini`, `text`).

Always introduce a code block with a short sentence. Never drop a bare code
block without context.

    The output looks something like this:

    ```output
    [/dev/sda].write_io_errs    0
    [/dev/sda].read_io_errs     0
    ```

## Numbers, Abbreviations, and Links

Follow standard rules for numbers - spell out small numbers in prose (e.g.,
"three"), use digits for larger or technical values (e.g., "24 workers",
"8 hours"). Use a code block when the number is a literal value from code or
output.

Expand uncommon abbreviations on first use (e.g., "Journaling Block Device
(JBD)"). Do not expand widely-known abbreviations (e.g., FTP, HTTP, RAM).

Inline links into the prose with descriptive text (`[BTRFS](https://...)`),
especially for sources. When the link itself is the point of the statement,
call it out explicitly (`the [docs page](https://...)`). Use bare links only
when the link needs to be copied and pasted.

## Whitespace

Whitespace is structural. Use blank lines to separate ideas and funnel the
reader's attention. Prefer visual space over inline formatting to create
hierarchy.
