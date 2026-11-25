---
name: place-page-in-menu
description: >
  Putting a page into the TOP MENU or the FOOTER, and deciding its order. Load it whenever the
  owner names a page together with a place in the navigation — "add a subscriptions page to the
  top menu", "put the todo list in the footer", "this should be in the menu", "reorder the footer
  links". It carries what is easy to get wrong here: whether such a page already exists, whether it
  may appear in a public menu at all, and which of the two menu sources is actually deciding what
  the visitor sees right now. The last one fails silently — the page ships, the menu never changes,
  and nothing reports an error.
---

# place-page-in-menu

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

## The page probably exists

"I want a subscriptions page in the top menu" describes an outcome, not an order for a new file.
Search by meaning rather than by slug — `/pricing`, `/plans` and `/subscribe` are one intent under
three names, and the owner will call all three "подписка". Name what you found back to him and let
him choose; that one question is what prevents a second subscriptions page.

Nothing found is a fork, not a green light. Two things are still unknown: whether he wants the page
at all, and **who may open it**. The second is not a detail for later — it decides which layer the
page lives in, and a page built in the wrong layer has to be moved, not configured. Building comes
after both answers, through `use-static-pages`.

## A protected page can never be a menu candidate

The candidate walk skips every folder whose name contains `protected`, and `navGroupsFromConfig`
marks everything it returns public. That is correct: a public button leading to a 403 is a promise
the site does not keep.

Pages behind roles reach their audience through the account drawer, which resolves by role group —
`PROTECTED_GROUP_ROLES` in `lib/roles.ts` is the source, read it rather than retyping it here.

So "subscriptions in the top menu" usually splits in two: a public page that sells the plans, and a
protected one where a subscriber manages his own. Say that out loud — it is a product decision, not
a technical one.

## 🔒 Two sources decide the menu, and only one of them is speaking

| Who answers | Where | Written by | When it is used |
|---|---|---|---|
| the owner's list | `nav.top` / `nav.footer` in `APP-CONFIG/app-config.json` **on the server** | only the control panel | **whenever the branch exists** — even empty |
| repo default, footer | `lib/menu/nav-config.ts` → `DEFAULT_FOOTER` | this repository | only while `nav.footer` is absent |
| repo default, top | each group's `_data/group.ts` → `menus.top.enabled/order` | this repository | only while `nav.top` is absent |

```ts
if (!nav || !Array.isArray(list)) return null;   // no branch → repo defaults answer
```

**The failure to avoid:** the owner pressed Save in the menu section even once → the branch now
exists → editing `DEFAULT_FOOTER` or a group manifest changes **nothing a visitor sees**. No error,
anywhere. Know which case you are in before touching either, and say it in the report.

A local agent cannot write the owner's list and must not try: `APP-CONFIG` lives on the server,
outside the repository, and the panel owns that file. When the branch exists, finish the page and
tell him plainly: it is ready at such an address, drag it into place in the panel. Five seconds for
him, impossible for you.

## The repo default for the TOP menu is one file, and its shape is exact

The scanner finds a group **only** by `<route>/_data/group.ts`. There is no other way in, and a page
without it is reachable by direct address alone.

```ts
export const group = {
  slug: 'about-us',          // MUST equal the folder name — the address is built from it
  roles: "public",
  childrenAsDropdown: false, // true ⇒ subfolders holding a page.tsx become the dropdown
  menus: {
    top: { enabled: true, order: 30 },
    footer: { enabled: false, order: 10 },
    left: { enabled: false, order: 10 },
    right: { enabled: false, order: 10 },
  },
}
```

🔒 **It is parsed as TEXT, by regular expressions** — the scanner runs at build and must not import
the content engine. So the shape is not free: single quotes around `slug`, double quotes around
`roles`, the four slots present. A prettier rewrite of this file silently produces a group that no
longer exists. Bracket groups on the path are transparent to the walk, so the file works the same at
any depth.

🔒 **The button's label comes from `eyebrow` in the page's language cell** (`_data/<lang>.ts`), read
by the same text scan. No field, and the label falls back to the folder name — Latin text in a
Russian menu, which is the one thing the translation rule forbids. Twelve characters is the cap for a
top-level button.

**Footer labels are a different story, and it is a real limitation to name out loud.** `DEFAULT_FOOTER`
carries English strings, and `labelFor` can only translate them through `APP-CONFIG.i18n`, which is
empty on a fresh project — so a repo-default footer entry shows English in every language until the
owner edits it in the panel. When a page needs a translated label from the repository, the group
manifest is the honest route; say which one you used and why.

**The two defaults live in different shapes, and asking the wrong one returns emptiness that looks
like an answer.** The footer keeps a single list; the top menu is assembled from group manifests
scattered through the layers — `(publicLayer)/products/_data/group.ts` and its neighbours. Fixed-
depth searching has twice produced "nothing found" where everything was in place.

## Order, labels, nesting

Order is the `order` number ascending, ties broken by slug; the panel rewrites the whole column as
`(index + 1) * 10` on every change, so what the owner sees is what the site does. Labels cap at 12
characters in the button — the page title stays full ("Accessibility" ships as "Accessible"), and
translations live in `i18n["nav.<slot>.<id>.label"]`, the same branch as the settings form's
per-language fields. Nesting is exactly one level.

## Proof

Count `<a href>` elements in the rendered header or footer — not words. "privacy" also lives in
structured data and class names, and a stale browser tab has produced more than one false verdict;
fetch fresh.

Check the state you did **not** change. A passing check on a configured project says nothing about
an unconfigured one — that asymmetry has already shipped a defect this month.
