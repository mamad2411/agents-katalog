---
name: use-dynamic-pages
description: >
  Pages whose DATA is dynamic — a user's own screen, an admin list, anything read at request time.
  Load it before building a page under `(protectedLayer)`, an `/api/*` door that serves protected
  data, or when the owner says "a page listing users / orders / their own bookings", "show what this
  person has", "an admin table". The thing you cannot guess: in this project such a page is still
  PRERENDERED — a static shell with dynamic holes — and the two lines that would make it honestly
  dynamic (`cookies()`, `headers()`) take the whole layer down with them. The second thing: a door
  that proxies another service can never be more permissive than that service.
---

# use-dynamic-pages

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

🔒 **First, make sure you are in the right skill.** Two different things are called "dynamic" here:

| | Dynamic **data** — this skill | Dynamic **address** — `use-route-parameters` |
|---|---|---|
| What varies | what one page shows | **how many pages exist** |
| Address | one, fixed: `/en/patients` | one per record: `/en/patients/8f21` |
| Shape | static shell + widget calling `/api/*` | a folder named `[something]` |

A request usually needs **both** — a list whose rows link to a page per record — and the owner never
says which he means, because in ordinary language his sentence is already complete. Recognising that
is `use-route-parameters` §1; it is a conversation, not a build decision.

## 1. A static shell with dynamic holes, not a dynamic page

This is the whole model, and it is what makes this the second of the three page models rather than a
different kind of website:

| Part | Where it runs | What it may touch |
|---|---|---|
| route entry `page.tsx` | build | the language from the address, nothing else |
| shell `_components/index.tsx` | build, **server component** | dictionaries, config — never a session, never a request |
| widget `_widgets/dynamic/<name>/` | browser, after a click | `/api/*`, and only what it asked for |
| door `app/api/**/route.ts` | request | the session, the database, another service |

Proof it worked, from the build table: the page is `●` and the doors are `ƒ`.

```
├ ● /[lang]/administration/users
├ ƒ /api/users
├ ƒ /api/users/[id]
```

🔒 **The control panel builds the same screen the opposite way, and copying it here breaks the layer.**
The panel reads the visitor's cookie in a server component and calls the service directly — correct
there, its pages are dynamic by nature. One such line here (`cookies()`, `headers()`, `auth()`) pulls
the **entire protected subtree** out of the prerender. `check:static` refuses it; take the refusal as
the answer, not as an obstacle.

## 2. The door is the real lock; the page is the sign

`proxy.ts` only requires that a session EXISTS — that is enough to stop an anonymous visitor and
nothing more: any logged-in person reaches any role's data through it. `AccessGate` on the page is an
honest sign that explains why someone was not let in, and a sign in a browser is switched off in that
same browser.

So every door serving protected data asks for the role itself: `requireRoles(req, [...])`, first line
of the handler, before it reads the body. Three states must differ, and they were verified live:

```
guest                    → 401 {"error":"Unauthorized"}
signed in, wrong role    → 403 {"error":"Forbidden","requires":["architect"]}
right role               → the data
```

403 rather than 404: the person is authenticated, there is nobody to hide the route's existence from,
and naming the required role gives the interface something to say.

🔒 **A proxying door cannot be more permissive than the service behind it.** Written here as
`['admin','architect']`, while the auth service allowed **architect only** — an `admin` would have
passed our lock and collected a 403 from the service, so the interface would promise access and then
refuse it, with the cause split across two places.

**The fix ran the other way, and that is the lesson:** the owner wanted administrators on this page,
so the SERVICE was widened and the door followed. Narrowing the door would have hidden his decision
in our code. Read the upstream handler, and when its right is wrong, change it there — not here.

## 3. Where the data lives, and where it must not

The users of this project live in the **auth service**, not in its database. There is no `users`
table here and creating one would be the expensive mistake of this area: a second copy of people
diverges from the first the day somebody changes an email.

A door that fronts another service: pass the visitor's `cookie` through (the service answers by THEIR
session, not by the app's authority), derive the service address with `authBaseFromHost` from the
request headers — never from `NEXT_PUBLIC_*`, which is baked at build and goes stale when the project
moves from an IP to a domain without a rebuild — and translate failure honestly: the service refusing
is its status; the service not answering at all is **502**, not 500.

Data that belongs to this project goes in `SCHEMA` (`lib/db/index.ts`) as usual — see `use-code-shape`.

## 3b. What the page is MADE OF, and what goes in the hole

A page here is still a list of blocks in a language cell — the shell, the heading, the explanation and
the chrome are content, exactly as on a static page (`use-static-pages`). The difference is one hole
in that list where something live stands. Deciding WHAT stands there is the first question of this
skill, and it is answered before the first file:

| The thing you need | Kind | Where it lives |
|---|---|---|
| shows and behaves for THIS route only — a table, a picker, a card of one entity | **widget** | `_widgets/dynamic/<name>/` inside the route |
| real logic a SECOND project would want, and it needs the build — a calculator, a converter, an editor | **tool** | `_tools/<id>/`, registry, mirror in the panel |
| the same view a neighbouring route already has | neither — that is the neighbour's widget, and you do NOT reach into it | see below |

The third row is the one that costs money: two routes needing "the same table" is not a reason to
share one. Four product tables were deliberately split for that reason. Copy the shape, not the file.

## 3c. 🔒 The page is finished even when its widget is not

**A missing widget or tool does not fail the page, and it does not fail the step.** Data that does not
exist yet, a platform field nobody writes, a service that has no such door — these are ordinary
branches with a defined exit, not a verdict about the project:

1. **Finish the page.** Shell, words, chrome, gates, deployment. A page with an honest empty state is a
   finished page — and an empty state that says WHY ("the service does not report this yet") is worth
   more than a page that was never built.
2. **Say it out loud to the owner** — what could not be made, what it depends on, and who owns that
   dependency (the platform, a key, a decision of his).
3. **Open the next step for it**: a plan in `development-docs/development-steps/new-steps/` named for
   the missing thing. The widget becomes its own piece of work, sized honestly.
4. **Close the current step as a success**, naming in its summary what was deferred and where it went.

🔒 **Do not stall the whole page waiting for an answer, and do not invent the data.** Both are worse
than the honest half: the first delivers nothing, the second delivers a lie that looks like a feature.
Refusing to build anything at all is the same mistake wearing caution's clothes.

**What "an error from the widget" means here** — the data source is absent or silent, a field the
service never fills, a right nobody granted. Not: your code does not compile. That one you fix.

## 4. The widget owns the behaviour

🔒 **Read a neighbouring widget before writing yours** — `use-widgets` opens with that rule now, and
it was written after this very page shipped looking like a different site. Take its structure, its
rhythm and its set of states; leave its behaviour and its words alone.

Everything about how this table looks and behaves lives in its folder: the fetch, the skeleton, the
row, the editor, its words. Delete the route folder and it is gone without a trace — that is the
acceptance test (`use-widgets`).

Two habits worth keeping, both bought:

- **Closed by default.** Nothing is fetched until a click. A list of people is the most sensitive and
  most expensive query on its page; asking for it on behalf of everyone who opened the address is
  work done for nobody. It also keeps the page addressable instantly.
- **Refusals are read by status, not by one phrase.** 403 and 502 are different events — "you may
  not" versus "the service did not answer" — and a single "could not load" sends the owner hunting a
  fault that is not there.

After a write, reload from the source rather than patching the array in memory: the service performed
the change, and its answer is the only truth about what happened. Its refusals are more informed than
yours — it is the one that knows an architect may not remove that role from themselves — so pass its
message through instead of replacing it with your own.

Dictionaries: the page's chrome ships with the product (owes all languages the owner can enable), the
widget's own words are the ten-language page set. Both resolve **on the server** and travel as props;
a client file importing a dictionary ships every language to the browser. During construction write
the enabled set and record the rest — `use-multi-lang`.

## 🔒 Страница построена — спроси, где её найдут

Страница, на которую не ведёт ни одна ссылка, существует только для того, кто наберёт адрес руками.
Так уже было: страница менеджера жила с самого начала и не была связана ничем — он свою же таблицу не
находил.

Поэтому **закрывая страницу, спрашиваешь владельца о размещении**, а не решаешь за него:

| Какая страница | О чём спрашиваешь | Куда добавляется |
|---|---|---|
| за авторизацией — динамическая или защищённая | **в выдвижной ящик?** | `lib/menu/account-links.ts`, строка с `group` своего слоя |
| публичная | **в верхнее меню? в подвал?** | манифест `_data/group.ts` (шапка) или список подвала — `place-page-in-menu` |

Спрашиваешь **вопросом, а не утверждением**: «добавить её в ящик администрирования?» — потому что
ответ бывает «нет»: страница может быть шагом мастера, целью ссылки из письма или частью другой
страницы, и пункт меню ей не нужен.

🔒 **Ящик — вежливость, а не защита.** Замок стоит в `layout.tsx` группы и в дверях данных; пункт
лишь показывает дорогу тому, у кого доступ уже есть. Роли пункт НЕ перечисляет — он называет свою
группу (`group: "admin"`), а роли группы знает `lib/roles.ts`. Перечисли их копией — и однажды пункт
начнёт либо дразнить отказом, либо прятать доступное.

## 5. The page must not exist for search — and that is all the SEO here

The protected layout declares `robots: { index: false }` (`check:protected` enforces it), the route
is absent from `app/sitemap.ts` and from `lib/aio/surfaces.ts`, and it has no markdown twin. A crawler that reached it would be handed a login form, and a map listing closed addresses invites an
agent to knock where it was not called.

🔒 **Nothing else from the search surface applies here.** No canonical, no hreflang, no structured
data, no markdown twin, no entry in `robots`. Reaching for `use-seo` on a page behind a role is work
spent to make invisible things findable — and the two skills disagree on purpose.

## 6. Before you call it done

- `check:types`, `check:i18n` (neither runs by itself), plus `check:static`, `check:protected`,
  `check:api`.
- The build table: your page `●`, your doors `ƒ`. The reverse means the shell reads a request.
- On the deployment, all three states above — including the two refusals. A door proven only with a
  valid session is a door proven for the case that never goes wrong.
- Fetch the page as a guest and grep the markup for the data it shows. It must not be there: the shell
  is prerendered, so a name or an email in it means something read a request at build.
