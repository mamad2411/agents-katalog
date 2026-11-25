---
name: use-tools
description: >
  The project's ready-made tools — what exists, where it lives, and why looking first is not
  optional. Load this BEFORE building any interface piece that feels generic: a picker, a cropper,
  a dialog for translations, a microphone, a code viewer, a media trimmer. Also load it when the
  owner says "we already made that", "why is there no window", "use the tool we built" — that
  sentence usually means a tool exists and was not found. Tools live in `_tools/<id>/` and are listed in
  `_tools/TOOLS.json`; anything built beside them is a second copy nobody asked for.
---

# use-tools

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

A tool here is a small reusable piece with a home: one folder, one `tool.json` card beside its code,
one place in the showcase that says what it does, how to use it and what it needs. Not a helper
hidden in a feature folder — those are invisible, and invisible is the same as absent.

## Where to look, in this repository

**The list: `_tools/TOOLS.json`** and each tool's own folder `_tools/<id>/`: what it does, how to use it, what it gives you, what
it needs (browser, HTTPS, an OpenAI key, ffmpeg), which package must be installed, and who already calls it.

🔒 **THE CATALOGUE IS GENERATED FROM THE FOLDER, AND A SECOND LIST IS FORBIDDEN.** Each tool carries
`_tools/<id>/tool.json`; `npm run build:tools-map` renders `_tools/TOOLS.json` from those cards and
`check:tools-map` fails the build when a folder has no card, when a card promises an entry file that
is not on disk, or when the map is stale. So the honest answer to "what tools does this project
have?" is the folder — never a list in prose.

✗ **This is not a precaution, it is a repair.** Until 2026-08-31 this project's own `CLAUDE.md` said
"Five ready pieces" while `_tools/` held six: `socials-ai` had arrived, was wired into the socials
field, and was named nowhere. A hand-written list diverges silently, and nothing wakes up, because
there is nothing to wake.

🔒 **THE DESCRIPTION LIVES IN `tool.json`, NEXT TO THE CODE.** Editing what a tool does means editing
its card in the same commit — text torn from its code goes stale on the day the tool changes. The
page's dictionary holds only field labels.

## 🔒 Прочитай соседний инструмент прежде, чем писать свой

Пять готовых лежат рядом (`_tools/`), и первый шаг всегда один: **открой ближайший по смыслу и
прочитай целиком.** Берётся устройство — из каких частей собран, где договор, как объявлены слова,
как он сообщает об отказе; берётся вид — ритм, размеры, состояния. Не берётся его логика: она про
другой предмет.

Причина та же, по которой это записано у виджетов: набор, собранный каждым по-своему, перестаёт быть
набором. Инструмент, чей отказ выглядит иначе, чем у соседа, читается как чужой, даже когда работает
безупречно.

## Look before you build — the failure this prevents is real, not theoretical

The translations dialog existed for months. Its own header said "connects to any entity with
translatable fields". It was written for the footer and menu sections specifically. And when the
translate button in those very sections was built, it was built from scratch: a call to the door
and one line of text — no language cards, no manual editing, no per-language save.

Nobody was lazy. The tool sat in `components/i18n/`, not in `_tools/`, and no catalogue listed it.
**There was nowhere to look.** That is the whole lesson: a tool without a home does not exist, no
matter how good it is.

So: before writing an interface piece that feels generic, open the showcase — or read
`_tools/TOOLS.json`, which is what the showcase reads. It costs one file read. Building the second
copy costs a day, and the copies drift apart quietly afterwards.

✗ **This paragraph used to send you to `bridges/app/lib/tools-registry.ts`, and that file does not
exist in this repository** (corrected 2026-08-31). It is the panel's, and the panel lives outside
your repository. Exactly the failure the removed "two homes" law caused, in the same skill: an agent
reading it either hunts for something absent or decides the rule is not for him.

## Two homes on purpose — and only one of them is yours

🔒 **THE MIRROR IS THE PLATFORM'S BUSINESS, NOT YOURS.** Some tools also exist in the panel, outside
your repository, and the section below explains why that duplication is deliberate. Read it as
background, not as an instruction: **you can neither see nor edit the panel's copy**, and the same
correction was already made once in `CLAUDE.md`, where a federal law about "two homes" stood in the
guest's document until 2026-08-24. Your side of it is one sentence — a tool lives in `_tools/<id>/`,
in your repository, and that is what makes it yours.

The same tool is copied on both sides: `bridges/app/_tools/` (panel) and the app's `_tools/`.
Deleting one of the two breaks something real:

- **Panel-only** would make the app depend on the panel at runtime — and the owner's right to
  detach and run alone dies with it.
- **App-only** would put the panel's own forms inside the user's repository, where he can delete
  them and break the panel he is using.

Copies drift. That is the price, and it is paid deliberately. What keeps it survivable: each copy
carries a header naming its mirror and listing what differs and why. Typically the dialog primitive
(the panel's shadcn vs the app's shared dialog), where languages come from (a prop vs the app's own
config), and which door does the work. Behaviour stays common.

**Distribution is by copy, never by network call.** The app does not read tools from the panel at
runtime — it installs a copy into its own `tools/<id>/` and edits it as its own code. A tool is
almost always adjusted to the task; reading it over the network would mean either forbidding edits
or drifting silently between what is installed and what runs.

## What a tool must carry to count as one

**`_tools/<id>/` with `client` / `server` / `types`** — one folder, so that "take the tool" means
"copy the folder" and not "hunt seven files across the tree".

**`_tools/<id>/tool.json` beside it**, and this is the part that is easy to skip and fatal to skip:

| Field | What goes in it |
|---|---|
| `entry` | the file a caller imports; the gate checks it exists on disk |
| `needs` | honest requirements — `browser`, `https`, `openai-key`, `ffmpeg` |
| `npmDeps` | packages this repository lacks; a missing package is a decision for the owner **before** installing, not a surprise at build time |
| `usedBy` | who already calls it. Empty is legal and is said in words ("not used by anything yet"), never left blank |
| `en` / `ru` | `title` · `what` it does · `how` to use it · `value` it gives. Written for a person, not a changelog |

Then `npm run build:tools-map`, and the tool appears in the showcase by itself — there is no list to
add yourself to. `check:tools-map` refuses the build if the card is missing or stale.

Half of that is not a tool. It is a component someone will fail to find.

## A component from a foreign registry: read the technique, not the manifest

🔒 **`npmDeps` answers what will be INSTALLED. It never answers what the reader GETS.** A visual
component brought in from someone else's registry (AI Elements, shadcn-style catalogues, a snippet
from a docs site) can add no package at all and still hand every visitor without JavaScript a broken
surface — the known case paints its text with `bg-clip-text text-transparent`, so the letters are
transparent and only the background makes them visible.

**Before installing, grep its source for how it draws content:** `transparent`, `bg-clip-text`,
`clip-path`, `mask-image`, `visibility`, `initial`. Anything found there is a decision for the
static twin (`use-widgets`), not a detail — and it is invisible in the dependency list, in the demo
and in the screenshot, because all three run JavaScript.

**Pairs with the CLI law** — `ANTI-PATTERNS.md`, "An unknown flag on a foreign CLI means *do
everything*": same suspicion of outside code, a different axis. That one is about what it may
execute, this one about what it may hide.

## When you build a new one

Ask first whether the thing is genuinely reusable or belongs to one screen. A tool that serves one
caller is a component in that caller's folder, and pretending otherwise puts a card in the showcase
that nobody reads.

🔒 **THE REQUEST FORM ASKS THAT QUESTION FOR YOU, AND ITS ANSWER TRAVELS TO YOU.** The card at the
bottom of the showcase has a second field — *where will you use it* — precisely because that is what
separates a tool from a widget: will a SECOND caller want exactly this thing. When a request reaches
`pre-steps/` with that field empty, it is not a formality you may skip; it is the question to ask
before the first line.

If it is a tool: put the words on the server and hand them to the island as props — the panel's
dictionary is 82 languages and never travels to the browser. Take the owner's existing pieces
rather than adding your own: the microphone, the cropper and the code viewer are already there.
Name refusals plainly and link to where they are cured; "could not" tells a person nothing about
what to do next. And write the `tool.json` card **in the same commit as the code** — a card added
later is a card written from memory.

## If a tool was deleted, do not rebuild it from memory

The starter's own tools live in its latest version:
**https://github.com/Fractera/fractera-next-starter**. Take the ARCHITECTURE from there — folder
shape, contract, layer boundaries — not the text or the images of that project. Copying a whole page
into someone else's product carries their identity along with it; copying the structure is exactly
what the specimens exist for.

A tool rebuilt from memory differs from the original in the details nobody notices until the first
refusal: no focus trap, the card's language lost, the reason hidden behind "could not".

## Proof

A tool is done when it works in a browser on both sides — not when types are green. Green types
proved nothing about the translate button: it compiled perfectly and showed a line of text where a
window belonged.
