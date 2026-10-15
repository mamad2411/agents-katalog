---
name: slop-mx
description: >-
  Publish a document, a diagram or a small file from the terminal to a publishing
  host (unlisted URL), drawing diagrams with Flux Flow. Use when the user asks to
  publish, post or put something online ("publiceer dit plan op slop.mx", "zet dit
  diagram online"), to update something published earlier, to upload a small image,
  or wants a diagram of a process, flow, pipeline or architecture ("maak een diagram
  van het inlogproces", "teken deze pipeline"), or wants to show a code change as a
  rich diff ("publiceer deze diff", "zet deze wijziging online als diff"). Three
  kinds: a doc (markdown, with components including a GitHub-style diff view), a
  diagram (a Flux Flow template with explicit coordinates) and a file (raw bytes).
license: MIT
---

# Publishing to a host

A page is published with one request and gets an unlisted URL: public to anyone
holding the link, but with a random suffix, no index, and `noindex` on the page.
A URL looks like `/rita/2026/07/login-flow-k3f9dq`, dated by the month it was
first published, and replacing a page later keeps that date so its link never
moves. The first segment is the account publishing it; a host leaves it out for
its own account. The host decides which, so report the URL the script prints
rather than assembling one.

## Installing and updating

The script runs on [Bun](https://bun.sh), so that has to be installed:
`brew install oven-sh/bun/bun`, or `curl -fsSL https://bun.sh/install | bash`.

```shell
npx skills add basmilius/skills --skill slop-mx
npx skills update slop-mx
```

The skill is copied into the agent's skills directory rather than linked, so a
newer version arrives through `npx skills update`, not on its own.

## Setup

One environment variable, and nothing else:

| Variable | Holds |
| --- | --- |
| `SLOP_MX_TOKEN` | The bearer token the host issued |
| `SLOP_MX_ENDPOINT` | Optional. Another host to publish to, when not `https://slop.mx` |

If the token is missing the script says so and stops. Report that rather than
inventing a value or writing a config file: there is no config file to write.

It has to be readable by the shell the agent runs commands in. On macOS that
means `~/.zshenv`, which zsh reads for every shell it starts; `~/.zshrc` is only
read by interactive ones, so a non-interactive command will not see it. For
Claude Code the `env` block in `~/.claude/settings.json` works too. Keep the
token out of a project's `.claude/settings.json`, since that one is committed.

Nothing is kept on disk. The host remembers what was published where, so
publishing the same title from a second machine lands on the same page.

## Choosing the type

- **doc** for prose: a plan, a summary, notes, a proposal. Written as markdown.
- **diagram** for a process or a flow. Written as a Flux Flow template, which is
  Vue markup rather than markdown.
- **file** for raw bytes: a screenshot, a small photo, a PDF. Up to 1 MB.

## Publishing

Write the content to a file first, then hand that file to the script. Never pass
long content as a shell argument.

```shell
bun ~/.claude/skills/slop-mx/publish.ts \
    --type doc \
    --title "Login flow" \
    --description "How a session is issued, end to end." \
    --tags auth,review \
    --file /path/to/content.md
```

The script prints the URL, whether it replaced an existing page, when it expires
and which tags it carries. Report that URL back to the user; it is the whole
point of the operation.

| Argument | Required | Notes |
| --- | --- | --- |
| `--type` | yes | `doc`, `diagram` or `file` |
| `--title` | yes | Shown as the page heading and used to derive the slug |
| `--file` | yes | Path to the markdown, the Flow template or the file to upload |
| `--description` | no | One sentence, used for link previews and under the diagram title |
| `--tags` | no | Comma separated, on top of the project tag |
| `--no-project-tag` | no | Leave the project out of the tags |
| `--path` | no | Publish onto a specific existing page, as `2026/07/some-slug` |
| `--new` | no | Force a fresh URL even when the title was published before |
| `--check` | no | Check a diagram's spacing and stop; publishes nothing |
| `--force` | no | Publish a diagram the spacing check objects to |

### Replacing an earlier page

The host keys a page on its title, so publishing the same title again lands on
the same URL and keeps its original date.

- The user gives a URL to update: pass everything after the domain as `--path`.
- The user wants a separate page despite the same title: pass `--new`.

An upload is the exception: it always takes a fresh URL unless `--path` names one
to replace, and a replacement has to carry the same extension, because the
extension is part of the URL.

## Tags

Tags are what make something findable again in the host's own admin. The script
adds one for the repository it runs in, so everything published while working on
a project groups together without anyone having to remember to say so. Add your
own with `--tags` for the subject or the kind of work: `auth`, `review`,
`incident`.

Before publishing, the script asks the host which tags already exist and reuses
the spelling it finds, so `slop-mx` and `slopmx` do not end up living side by
side. Two or three tags is plenty; past a handful they stop narrowing anything
down, and the host refuses more than ten.

Publishing replaces a page's tags rather than adding to them, so pass `--tags`
again when republishing something that carried tags you want to keep.

## Expiry

A host may remove a page a set number of days after it was last published.
Publishing it again starts that clock over. The script prints the expiry when
there is one; mention it, because a link that disappears in a month is a
different promise than one that does not.

## Uploading a file

```shell
bun ~/.claude/skills/slop-mx/publish.ts \
    --type file \
    --title "Dashboard sketch" \
    --tags design \
    --file /path/to/sketch.png
```

Images, PDFs and small text files up to 1 MB. The URL carries the extension, so
it can be used straight in a doc as a normal markdown image:

```markdown
![Dashboard sketch](https://slop.mx/2026/07/dashboard-sketch-k3f9dq.png)
```

Upload the image first, then write the doc around the URL it printed.

## Writing a doc

Both page types get a fixed house style, so do not write styling of your own: no
HTML in the markdown, no inline styles, no headings used for visual effect.

Start the markdown at `##`. The title comes from `--title` and is rendered as the
page heading already, so a leading `#` would give the page two titles. The h2 and
h3 headings become the page's side navigation, so structure a doc with meaningful
ones.

GitHub-flavoured markdown works throughout: tables, task lists (`- [ ]`),
footnotes (`[^1]`), strikethrough. Code fences are highlighted for bash, css,
diff, html, ini, java, javascript, json, markdown, php, python, scss, sql,
typescript, vue and yaml; any other language renders unhighlighted, never as an
error.

### Components

A doc may also use a small set of components. Rules that make them work: block
components always close with `::`, props are always double-quoted, and internal
targets are paths exactly as the API hands them back (`2026/07/some-slug`, or
`rita/2026/07/some-slug` for another account). On GitHub or in a raw view these
degrade to visible marker lines with the target still readable.

A **card** links to another published item or an external URL. For an internal
target the host fills in the title, description and kind icon at render time,
so write nothing but the path; body text replaces the description. An `icon`
prop (kebab-case Font Awesome Duotone name, same set diagrams use) overrides the
default; an unknown name falls back with a publish warning.

```markdown
::card{to="2026/07/login-flow-k3f9dq"}
::

::card{to="https://flux-ui.dev" icon="paintbrush"}
Optional one-line teaser that replaces the resolved description.
::
```

A **card grid** puts cards side by side where the column allows it. Note the
extra colon on the wrapper:

```markdown
:::cards
::card{to="2026/07/login-flow-k3f9dq"}
::
::card{to="2026/07/checkout-flow-m2xk1p"}
::
:::
```

An **embedded diagram** shows a published diagram inside the doc, in an
interactive frame with a link to the full page. Body text becomes the caption.
Without a `height` the frame takes the reader's own viewport ratio; pass one
(`height="24rem"`) only when a diagram wants less room.

```markdown
::diagram{path="2026/07/checkout-flow-m2xk1p"}
The checkout flow, embedded.
::
```

**Callouts** use GitHub's alert syntax, which GitHub itself also renders:

```markdown
> [!NOTE]
> Docs are cached for five minutes.
```

`NOTE`, `TIP`, `WARNING`, `IMPORTANT` and `CAUTION` are accepted. Note for
context, tip for a shortcut, warning for something that bites.

A **collapsible section** hides detail behind a native disclosure:

```markdown
::details{summary="Full stack trace"}
Any markdown, including code fences.
::
```

A **YouTube video** embeds in a frame; a bare id, a watch URL or a share link
all work, and body text becomes the caption:

```markdown
::youtube{id="5UiM7m9tQ80"}
::
```

A **details group** turns several collapsibles into an accordion: one open at
a time, all closed on arrival. Good for FAQs:

```markdown
:::details-group
::details{summary="First question"}
The answer.
::
::details{summary="Second question"}
Another answer.
::
:::
```

A **progress bar** states how far something is; `status` is the label, `max`
defaults to 100, colors are the badge colors:

```markdown
::progress{value="60" status="Rollout to production" color="success"}
::
```

A **wide image** breaks out of the text column; the title becomes its caption,
and every image in a doc opens in a lightbox when clicked:

```markdown
![Dashboard sketch](https://slop.mx/2026/07/dashboard-sketch-k3f9dq.png "The caption"){.wide}
```

**Steps** dress a plain ordered list as numbered stops on a line, for
instructions and how-tos:

```markdown
::steps
1. Install Bun.
2. Run the script.
::
```

A **facts panel** is a key-value block for metadata at the top of a doc. Every
prop becomes a row and the keys are yours to choose:

```markdown
::facts{status="In review" ticket="IPV3-5924" branch="feature/rich-docs"}
::
```

**Stat tiles** put the numbers of a report in a grid; `hint` is optional:

```markdown
:::stats
::stat{value="12" label="Tests fixed"}
::
::stat{value="2.0 MB" label="Server bundle" hint="gzip"}
::
:::
```

An **inline badge** is a status chip in running text or a table cell. Colors:
`gray`, `primary`, `info`, `success`, `warning`, `danger`:

```markdown
The rollout is :badge[Done]{color="success"}, the docs are :badge[In review]{color="warning"}.
```

A **file tree** renders a plain nested list as a tree. A trailing slash marks a
folder; an entry with children is one already:

```markdown
::tree
- src/
  - worker/
    - index.ts
- package.json
::
```

A **code fence title** names the file above the block, straight after the
language, and gets a copy button either way:

````markdown
```typescript [server/utils/foo.ts]
const x = 1;
```
````

A **code group** turns consecutive fences into tabs, labelled by their titles:

````markdown
:::code-group
```typescript [a.ts]
const a = 1;
```

```bash [terminal]
bun run dev
```
:::
````

A **diff** renders a unified diff the way GitHub does: syntax-highlighted, with
a toggle between unified and split view and a copy button for the raw patch.
`title` names the file above the block. The body is one ```diff fence holding
the patch exactly as `git diff` printed it; the fence is what keeps `---` and
`+++` lines from being read as markdown. One file per block: a multi-file patch
falls back to a plain highlighted fence with a publish warning, so split it
into one `::diff` per file. A bare ```diff fence outside the component stays
what it always was, a simple highlighted snippet, so reach for `::diff` when
the change itself is the story.

````markdown
::diff{title="src/app.ts"}
```diff
--- a/src/app.ts
+++ b/src/app.ts
@@ -1,3 +1,3 @@
 import { createApp } from 'vue';
-const app = createApp({});
+const app = createApp(App);
```
::
````

Publishing a doc never fails over its content, but it may print warnings: a card
target that does not resolve yet, an unknown component (usually a typo like
`::caard`), an unknown icon. Relay them to the user; a target published a moment
later simply starts working.

## Writing a diagram

A diagram is one `<FluxFlow>` element holding positioned nodes and the
connections between them. Publish only the markup: no `<template>` wrapper is
needed, and a `<script>` block is neither needed nor allowed.

```vue
<FluxFlow :padding="24">
    <FluxFlowNode id="start" :x="0" :y="0">
        <FluxFlowTerminal color="info" icon="user" label="Login attempt"/>
    </FluxFlowNode>

    <FluxFlowNode id="check" :x="0" :y="160">
        <FluxFlowConditionCard>Are the credentials valid?</FluxFlowConditionCard>
    </FluxFlowNode>

    <FluxFlowConnection from="start" to="check"/>
</FluxFlow>
```

Everything is static: no state, no data, no event handlers, so a component that
reads a variable will not work.

**Read `references/flow-layout.md` before placing anything.** Flow positions
nothing for you, and the numbers that decide whether a diagram reads well are not
guessable: a card is as tall as its text, a connection carrying a label needs
110px of clear space and one carrying only an icon 100px or its badge lands on
both cards, a connector attaches 31px in from an edge, and a group's frame extends
21px past its nodes plus a 45px title band.

Publishing a diagram checks that spacing and refuses when two connected nodes sit
too close, naming the pairs and the space they need. Fix the coordinates rather
than reaching for `--force`. While drawing, `--check --file <path>` runs the same
check on its own and publishes nothing.

For which component to reach for and the props it takes, see
`references/flow-components.md`.

### What the host adds

The viewer opens every diagram full screen, centred, on a dotted canvas, and
makes it draggable and zoomable. It applies `interactive`, `background` and
`align` itself, so leave them out unless a diagram needs different values.

Publishing rejects a diagram naming a component the viewer cannot resolve. Vue
drops its "failed to resolve component" warning from a production build, so a
rejected publish means a typo or a component that does not exist, not a broken
host. The host itself checks nothing about the layout; the spacing check runs in
`publish.ts`, and everything it does not measure is yours to get right.
