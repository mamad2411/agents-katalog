---
name: use-routes
description: >
  WHERE a route goes on disk and who may open it — the two layers, the four permission groups, and
  the folder shape a page must have. Load it before creating any folder under `app/`, when the owner
  asks for "a page for managers / for buyers / for me only", when a gate refuses a folder you just
  made, or when you are about to import something from a neighbouring group. The mistakes here are
  not stylistic: a page in the wrong layer has to be moved rather than configured, a folder one level
  too high turns the whole public layer into a tab and fails gates on code you never touched, and a
  borrowed import across permission groups breaks nothing today and everything later.
---

# use-routes

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

## 1. Two layers, and a route in neither is an unasked question

```
app/[lang]/(publicLayer)/      everyone sees the same thing
app/[lang]/(protectedLayer)/   what you see depends on who you are
```

There is no third place. `check:content` refuses a route outside both (`route-unclassified`) — and the
reason is not tidiness: a folder in neither layer means **nobody said whether the page is the same for
everyone**, so no set of rules applies to it and no gate audits it. The gates used to walk `[lang]`
and subtract known names, which is a blocklist: a folder added tomorrow was checked by nobody.

Bracket groups do not appear in the URL — `(publicLayer)/blog` opens at `/blog`. **Transparent for the
address is not transparent for everything else:** the sitemap walk and `check:seo` count only
first-level folders of `app/[lang]`, so a page inside a group is guarded by nobody there and must be
named by hand (`use-seo`).

## 2. 🔒 A page folder sits TWO levels below the layer

`<tab>/<slug>/`, never directly under the group. `(publicLayer)/about/` looks natural and is wrong:
the co-location gate derives the tab as `_data/../..`, so a page one level down turns the WHOLE public
layer into a tab of posts and applies post rules to every neighbour — 27 failures on code you never
touched, and nothing in the message points at your folder. Today's tabs: `blog/`, `products/`,
`(footerPages)/`. A page belonging to none of them needs a tab of its own.

Inside the folder, underscore names are not routes and never become addresses: `_components/` (the
view), `_data/` (words and non-translatable meta), `_lib/` (types and functions), `_widgets/` (the
live parts). A folder with a **dot** in its name is a machine route — `index.md/`, `llms.txt/`,
`manifest.webmanifest/` — and `proxy.ts` deliberately ignores dotted paths.

## 3. Four permission groups, and each carries its own door

| Group | Who gets in (`PROTECTED_GROUP_ROLES`, `lib/roles.ts`) |
|---|---|
| `(account)` | the customer: `user`, `buyer`, `vip_user`, the three `subscriber_*` — plus `architect` |
| `(staff)` | the operators: `manager`, `senior_manager`, `support_manager`, `delivery_manager`, `content_editor` |
| `(finance)` | `finance` |
| `(admin)` | `admin` |

`architect` is in every one of them by construction — that is the role that sees everything, and it is
also why a screen that works for you may refuse everybody else. Say which role you tested as.

Each group **must** have its own `layout.tsx` mounting `AccessGate`; `check:protected` refuses a group
without a layout (`group-without-layout`) or without the gate (`group-without-gate`). The layer's own
layout declares `robots: { index: false }` — a crawler that reached a protected page would be handed
the login form.

🔒 **And the gate on the page is a SIGN, not a lock.** The lock lives in the door: `requireRoles` as
the first line of every `/api/*` handler that serves protected data. `proxy.ts` only proves a session
exists — any logged-in person passes it. See `use-dynamic-pages`.

## 4. 🔒 A group never imports from a sibling

Shared code rises to the lowest common ancestor — `components/`, `lib/` — it does not travel sideways.
`check:protected` refuses it (`cross-group-import`).

This one is worth understanding rather than obeying, because breaking it costs nothing on the day:
`localizeProduct` was born inside `(staff)`, and the public storefront imported it from there. Nothing
failed. What it means is that the storefront now depends on a folder built for a different audience,
so deleting or reshaping the staff area breaks a page nobody connected to it — and the connection is
invisible from either end.

The same reflex applies inside a route: a widget's parts stay in the widget (`use-widgets`); a
neighbouring route's table is not a library.

## 5. Which model of page you are building — decide before the first file

| Model | Route shape | Rendering | Skill |
|---|---|---|---|
| public, authored, finite | **a data folder per item, ONE template per collection** — never a `page.tsx` per item | SSG (a slice) + first visit | **`use-page-tree`** |
| public, from data, unbounded | `[slug]` | prerender a slice, `dynamicParams`, ISR | `use-static-pages` + the catalogue example |
| a person's own screen | inside a permission group | static shell, data through `/api/*` | `use-dynamic-pages` |

Getting this wrong is not cosmetic: a folder per item for a catalogue is a million folders, and a
dynamic page for an authored text is a page search never sees.

🔒 **2026-09-25 — the first row changed.** It used to read "a folder per item" and was built as one `page.tsx`
per folder. Measured on one element: 300 page files built in 1252 s, the same 300 pages through one
template in 98 s; the core reached 126 near-identical `page.tsx` and 5–7 minutes of compile. The folder stays
(it holds the data); the route file per page is forbidden. Details and the guard — `use-page-tree`.

🔒 **The row is chosen by an answer only the OWNER has, and he was probably never asked.** "One page,
or one per record" is invisible inside a sentence like "make a client page", which is complete in
ordinary language and ambiguous here. → **`use-route-parameters`**: how to ask it in his words, what to
tell him before he answers, and — the dangerous half — what to check before REMOVING a parameter that
already exists, because "I don't need this here" has four readings and only one of them deletes a
route.

## 6. Before you call it done

- `check:content` (`route-unclassified`), `check:protected`, `check:static`, `check:seo` — each covers
  a different way a route can be misplaced.
- `page.tsx` stays thin: declare the segment, re-export `./_components`. `check:protected` measures it.
- Open the page as somebody who should NOT see it. A protected page that opens in `dev` or on
  `localhost` is the bypass or the owner-at-the-keyboard rule, not a fault — check it on the own domain
  and say which address you tested on.

## 🔒 Форма страницы задаётся СЛОЕМ, и слои устроены по-разному

✗ **Оплачено 2026-08-24.** Публичный маршрут собрали по образцу соседей из защищённого слоя — три
сторожа отказали хором: собственный `<main>` вместо `PageShell`, нет `generateMetadata`, нет
markdown-двойника.

| Слой | Что обязана нести страница |
|---|---|
| `(publicLayer)` | оболочку слоя, метаданные, markdown-двойника для машинных читателей; собирается фабрикой → `use-static-pages` |
| `(protectedLayer)` | ничего из перечисленного: индексации нет, машинный двойник не нужен |

🔒 **Образец берётся из СВОЕГО слоя.** Сосед по дереву — не образец, если он живёт в другом слое:
внешне страницы похожи, а обязанности у них разные. Проверка одна: чем собран ближайший маршрут ТОГО
ЖЕ слоя.

## 🔒 Новый маршрут воспроизводит форму образца ТОГО ЖЕ РОДА

Слой — первое деление, но не последнее. Внутри слоя **род маршрута задаёт наличие динамического
сегмента**, и формы у родов разные.

**Сверься с образцом поимённо, файл за файлом:**

| Род | Что несёт образец в этом репозитории |
|---|---|
| статический маршрут | `page.tsx` (тонкий вход) · `_components/` · `_data/ui.i18n.ts` · `_widgets/` при наличии виджета |
| **маршрут с динамическим потомком** | то же **плюс** `error.tsx` и `not-found.tsx` у родителя |
| **сам динамический сегмент** | `page.tsx` · `_components/` · **`layout.tsx`** · **`not-found.tsx`** |

✗ **Оплачено 2026-08-24:** новый динамический маршрут собрали по форме статического соседа — `layout`
и `not-found` не появились, и отказ на несуществующем идентификаторе остался без ответа.

🔒 **Расхождение с образцом либо устраняется, либо объясняется строкой.** «У образца есть, у меня нет»
без причины — не упрощение, а потерянный паттерн: образец однажды удалят, и восстанавливать будет не
из чего.

### Где эталон после того, как образцы удалены

🔒 **Анатомия маршрута НЕ переписывается в этот навык.** Документ, повторяющий устройство кода,
расходится с ним молча — а по-настоящему нужен он ровно один раз, когда кода уже нет.

**Постоянный эталон — публичный стартер: https://github.com/Fractera/fractera-next-starter.**
Оттуда берётся АРХИТЕКТУРА (состав папки, границы слоёв, устройство контракта) и никогда — текст и
картинки. Открывать ближайший маршрут того же слоя и того же рода; сравнивать поимённо.

**Порядок, когда образец в проекте ещё жив:** сравниваешь с ним, он под рукой и точно той же версии.
**Когда удалён:** сравниваешь с публичным стартером и **говоришь об этом вслух** — версии могли
разойтись, и это часть ответа, а не мелочь.
