---
name: use-aio
description: >
  The MACHINE surface of the site — the markdown twin of every public page, `llms.txt` and
  `llms-full.txt`. Load it whenever you add a public section or page, move an address, wonder what a
  model sees when it visits, or the owner says "make it readable for AI", "add llms.txt", "ChatGPT
  quotes the wrong price", "the agent gets a 404". Same reader problem as search, opposite shape: a
  crawler sends a human to a page, a model comes itself and needs TEXT — page markup is half chrome
  to it. The trap this area produces is silent: a new section ships with no twin, `llms.txt` never
  learns it, and the only symptom is a model that answers about your site from something older.
---

# use-aio

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

**AIO is SEO with a different reader.** The engine sends a person; the model arrives itself, reads and
retells. So the page must exist twice: as a page, and as its text.

🔒 **A model is not promised to run JavaScript.** OpenAI's own bot documentation says nothing about
executing it — so the finished CONTENT has to be in the server markup, not assembled after hydration.
Motion, tabs and reveals belong on top of a printed twin, never instead of it (`use-widgets`). A
section that only exists after hydration exists for nobody here.

## 1. One registry feeds all three surfaces

`lib/aio/surfaces.ts` is the single list of public surfaces. From it come `llms.txt` (the map),
`llms-full.txt` (all texts in one document) and every page's markdown twin. One list means a new page
appears in all three at once or in none — a map that disagrees with the site is physically impossible.

| File | What it is |
|---|---|
| `lib/aio/surfaces.ts` | the registry: `subPath`, title, description, map section, and a **lazy** `body()` |
| `lib/aio/md-route.ts` | the shared `markdownRoute(subPath)` behind every `index.md` |
| `lib/aio/blocks-to-markdown.ts` | page blocks → text, plus `faqToMarkdown` |
| `lib/aio/llms.ts` | both maps |

Posts and products need no entry: posts come from `_list.generated.ts` inside the registry, and product
cards carry their own twin at their own address. **A new SECTION or standalone page is the case that
needs your hands** — a registry line and an `index.md/route.ts` next to the page.

## 2. The address of a twin always carries the language

`mdUrlFor(lang, subPath)` → `<origin>/<lang><subPath>/index.md`, **even in single-language mode**,
where the page itself has no language segment. Not a matter of taste: `proxy.ts` deliberately ignores
any path containing a dot (the same exclusion that lets `/llms.txt` through), so nobody is left to
rewrite `/index.md` into `/en/index.md` — and the route physically lives under `app/[lang]/`. It
shipped wrong once and the first link of the map answered 404.

The twin is also announced from the page: `buildAlternates` puts it in `alternates.types` as
`text/markdown`. A model that follows it skips the menu, the footer, the consent banner and the
scripts — which is the entire saving.

## 3. The route is three declarations and a shared brain

```ts
const md = markdownRoute("/blog")
export const dynamic = "force-static"
export const dynamicParams = false
export const generateStaticParams = md.generateStaticParams
export const GET = md.GET
```

Segment values are declared literally: Next parses them statically and refuses a re-export from an
object ("needs to be a static boolean").

## 4. 🔒 One source of text, never a hand-written file "for the AI"

The twin is built from the SAME blocks as the page. A separate hand-written copy diverges at the first
edit and nobody notices, because nobody opens a markdown twin in a browser — today that divergence is a
model quoting a price you changed last month.

## 5. What goes in the map, and what never does

**What the format is FOR, in the words of its own specification: inference, not training.** A model
reading the site to answer a question now — not a corpus somebody trains on. Say that when asked, and
do not stretch it: the specification makes no promise either way about training.

`llms.txt` follows llmstxt.org literally: `# Title`, a `> quote` carrying everything needed to
understand the rest, optional prose **without headings**, then `## Section` lists of
`- [name](url): note`. The section named `## Optional` is from the specification — it marks links an
agent may skip when trimming context, so its name is **not translated**; legal pages go there.

- **Sections are named, rows are not.** The map names the catalogue; individual products are reached
  through the sitemap and their own twins. A file that grows to its limit stops working whole — the
  same lesson as `sitemap.xml` and its 50 000 URLs.
- **Nothing behind a role, ever.** A page under `(protectedLayer)` has no twin and no map entry. The
  map is an invitation to read; a closed address in it invites an agent to knock where it was not
  called. `check:aio` enforces both halves.
- **`llms-full.txt` is community practice, not a standard.** It does not exist in the specification,
  the file says so in its own first line, and `check:aio` fails if the word "standard" appears next to
  it. Calling practice a standard is how a wrong fact enters documentation, marketing and support
  answers at once.

## 6. What the gate refuses

`npm run check:aio`, and it runs inside `prebuild` — a build with a public page missing its twin does
not complete, so it never deploys:

- a public page with no neighbouring `index.md`;
- a markdown twin under a role-gated route;
- a map that is still a stub instead of being built from the registry;
- `llms-full.txt` described as a standard.

## 7. Before you call it done

Two proofs from different planes, and the gate is only one of them:

- fetch `/<lang>/<page>/index.md` and read the text — headings, body, FAQ, all of it present;
- fetch `/llms.txt` and `/<lang>/llms.txt`, find your page, and **request every link you added** —
  200, not 404, on the real deployment;
- view the page source and confirm the content is in the server markup rather than arriving with the
  scripts.

Green gate plus 200 on the page is one plane. The text of the twin is the other.
