---
name: use-route-parameters
description: >
  One address, or one address per record — the decision hidden inside almost every request about
  "a page for X", and the conversation that must happen before you build either. Load it whenever the
  owner asks for "a client page", "a page for each post", "a card for a user", "show one order", when
  he asks why there are numbers or words in an address, and — most important — whenever anything is
  being REMOVED from an address that already has a parameter in it. He will almost never use the words
  "dynamic route": that is the whole problem, and recognising the request behind his words is your job,
  not his. Not to be confused with `use-dynamic-pages`, which is about dynamic DATA on one fixed
  address; this is about the ADDRESS itself.
---

# use-route-parameters

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

## 0. Two different things are called "dynamic", and the owner cannot tell them apart

Neither can most developers who came to this from another trade. Get this table straight before you
say the word to anybody:

| | Dynamic **data** | Dynamic **address** (this skill) |
|---|---|---|
| What varies | what the page shows | **how many pages exist** |
| The address | one, fixed | one **per record** |
| Example | `/en/patients` — a table that loads rows | `/en/patients/8f21` — one page for one person |
| Built by | a static shell + a widget calling `/api/*` | a folder named `[something]` |
| Skill | `use-dynamic-pages` | **here** |
| Search sees | one page | **one page per record** |

🔒 **A request can need both, and usually does.** A list of clients (dynamic data, one address) whose
rows link to a client's own page (dynamic address, one per client). Saying "yes, dynamic" to a person
who means one of them and building the other is the most common way this goes wrong.

---

## 1. 🛑 The trigger: he will not say "dynamic route"

He will say: *"make a client page"* · *"a page for each post"* · *"a user's card"* · *"show one
order"* · *"the patient should open"*. **Every one of these is ambiguous**, and the ambiguity is not
his fault — the sentence is complete in ordinary language and incomplete in this architecture.

🔒 **Stop before the first file and ask ONE question, in his words:**

> One page for everybody, or a separate page for each?
>
> If it is one: the address is always `/en/clients`, and the page shows whoever we pick — a list, a
> search, a chosen card inside the same page. Nobody can send a link to a particular client.
>
> If it is a separate one for each: the address becomes `/en/clients/anna-petrova` — a real page per
> client, sendable as a link, findable in search, printable, bookmarkable.

**Do not lead with the vocabulary.** "Dynamic segment", "route parameter", "slug" are your words and
they explain nothing to him. **Show the addresses.** He recognises an address instantly and has an
opinion about it in one second.

🔒 **Write his answer into `PASSPORT.md` §5** — it belongs to static-against-dynamic and it will be
asked again in three weeks by somebody who was not in this conversation.

---

## 2. Teach with HIS entity, in three lines

Once he has chosen "one per record", show what he is about to own — before it exists:

```
/en/clients              the list       ← one page
/en/clients/anna-petrova one client     ← one page per client, made from a template
/en/clients/ivan-orlov   another        ← the same file serves all of them
/ru/clients/anna-petrova the same, in Russian
```

**Three things to say out loud, because he cannot guess any of them:**

1. **You write ONE file, and it serves every record.** He often imagines somebody creating pages by
   hand and is quietly worried about the effort — or, worse, expects to edit each one in the panel.
2. **The language prefix is always there** (`/en/…`, `/ru/…`), even with a single language switched
   on — because the day he adds a second one, no address has to change.
3. **What goes in the address is a DECISION, and it is his.** A readable name
   (`/clients/anna-petrova`) or an identifier (`/clients/8f21c3`). Readable is better for people and
   for search; it also changes when she is renamed, and old links break unless something keeps
   redirecting. Identifiers never break and mean nothing to a human. **Say both halves, let him pick.**

---

## 3. How it actually works here — the parts that surprise people

Read the real specimen rather than trusting this summary: `app/[lang]/(publicLayer)/products/[slug]/`.

| What | How it behaves here |
|---|---|
| the pages | **prerendered**, not generated per visit — `generateStaticParams` builds a SLICE at build time, so build time stops depending on how many records exist |
| a record outside the slice | born on the first request, then served as static from then on (`dynamicParams` is `true` by default and deliberately not written out) |
| a record that does not exist | `notFound()` → a real 404. **The page never invents one** |
| freshness | `revalidate` in `app/[lang]/layout.tsx`; the smaller value wins down the tree, and a tag reset (`revalidateTag`) is what actually keeps it fresh |
| the entry file | thin: reads the parameter, hands it to `_components`. `revalidate` must be declared in the route file itself and be **statically computable** — `3600` is fine, `60 * 60` is not, and Next silently makes the page dynamic if it cannot read it |

🔒 **This is why "dynamic" here does not mean "slow" or "bad for search".** In many stacks a
per-record page is rendered on every visit; here it is a static file after the first one. When he
worries that "dynamic pages are bad", that is what he has heard elsewhere, and it does not apply.

---

## 4. What it means for search — in his terms, not in jargon

- **One address per record = one page search can find.** A hundred clients, a hundred pages, each with
  its own title and description.
- **One address that swaps content in the browser = one page for search**, and the records are
  invisible to it no matter how good they look on screen.
- **The 404 matters more than it sounds.** A page that renders something for a record that does not
  exist teaches search engines that infinitely many addresses "work", and they index rubbish.
- **Public or behind the login changes everything.** A page behind authentication is not indexed at
  all and must not be — a public link to a refusal is a promise the site does not keep (`use-roles`).
  Ask which one it is; he usually has not considered the question.

---

## 5. 🛑 The other direction, and it is the dangerous one

**Removing is where the damage happens**, because the request sounds smaller than it is.

He says: *"I don't need this here"* · *"take the id out of the address"* · *"why is this page here at
all"* · *"just make it one page"*. Each can mean four different things:

| What he might mean | What it actually is |
|---|---|
| hide this from the menu | one line, harmless |
| this record should not be public | a rights change, the page stays |
| I don't want ids showing in the address | change WHAT goes in the parameter, keep the parameter |
| there should be no per-record pages at all | **delete the route — the expensive one** |

🔒 **Never act on the fourth reading without asking.** The other three are common and cheap; the
fourth is rare and destroys work. The cost of asking is one sentence.

### Before touching a parameter that already exists, count what stands on it

✗ **Counted in this repository, not recalled.** One dynamic route (`products/[slug]`) is referenced by
**ten files outside its own folder**:

```
app/products/sitemap.ts          its own sitemap
app/sitemap.ts  ·  app/robots.ts the site's
5 widgets in THREE other layers  (account, admin, finance, staff) — rows that link into it
products/_components/index.tsx   the list page above it, and its load-more island
```

Plus, inside the folder, an `index.md` companion route that must go with it. **Delete the folder and
every one of those points at nothing** — and note where they live: three permission layers that have
nothing to do with the public page, which is exactly why nobody expects them.

🔒 **Some of it no gate will catch.** Menus are not checked (`place-page-in-menu`), and a build step
can fail before any gate runs. **Enumerate by hand, name the list to him, then act.** Say it as a
count, not as a warning: *"this address is referenced from ten other places; removing it means editing
all ten — shall I?"* — a number is a fact he can weigh, a warning is noise he will wave through.

🔒 **Removing the parameter is not the same as removing the pages.** Keeping the route and narrowing
what it serves is usually what he wanted, and it is reversible. Deleting the folder is not.

---

## 6. The anatomy is not here

Which files a dynamic route carries — `layout.tsx`, `not-found.tsx`, what its parent owes — lives in
`use-routes` («новый маршрут воспроизводит форму образца того же рода»), and it is measured against a
real specimen, file by file. **Do not restate it here**: two descriptions of the same folder drift,
and the one in `use-routes` is the one the gates agree with.

Which of the three page models you are in — also `use-routes` §5. The catalogue recipe with the
prerendered slice — `use-static-pages`.

---

## 7. Traps

- ✗ **Building it because it sounds more capable.** A per-record page for six authored texts is six
  folders' worth of machinery replacing six folders, with worse search results. Finite and authored →
  a folder per item.
- ✗ **A folder per item for something unbounded.** A thousand clients is not a thousand folders.
- ✗ **Answering "yes, dynamic" without asking which dynamic.** §0.
- ✗ **Using the parameter for something that is not an identity.** Filters, sorting and pages of a
  list belong in the query string; each value in the address becomes a page that search will try to
  index, and a sort order is not a page.
- ✗ **Explaining with vocabulary.** If he has to learn a word before he can answer, the question was
  asked wrong. Show two addresses.

## Proof

Two proofs from different planes. One of them is almost always **two records and a miss**: two
different addresses that render two different records, and a third address that does not exist
answering with a real 404 — the negative control, and the one people skip. A page that renders
something for every address ever typed is the failure this route type is most prone to.
