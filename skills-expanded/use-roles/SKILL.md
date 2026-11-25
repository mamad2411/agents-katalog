---
name: use-roles
description: >
  ROLES — who sees what, and where that is actually decided. Load it before building anything behind
  authentication, before adding a role check, when the owner says "only managers should see this" or
  "let administrators do it too", and whenever a screen works for you and refuses somebody else. Two
  things you cannot guess: the visible gate on a page is a sign rather than a lock, and a door that
  fronts another service may never be more permissive than that service — get that backwards and the
  interface promises access, then refuses it, with the cause split across two places.
---

# use-roles

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

## 1. Where roles live and where they are decided

The list of roles is `ALL_ROLES` in `lib/roles.ts`; a person's roles live in the auth service and
arrive as `{ userId, email, roles }` from `getSession()`. Groups map roles to layers —
`PROTECTED_GROUP_ROLES`: `account`, `staff`, `finance`, `admin`.

**`architect` belongs to every group by construction.** That is the role that sees everything, and it
is also why a screen that works for you may refuse everybody else. Name the role you tested as.

🔒 **Never retype a list of roles.** A component, a menu entry, a door — each names its GROUP and
lets `lib/roles.ts` answer which roles that means. A copied list drifts, and then the menu either
teases with a refusal or hides what is permitted.

## 2. 🔒 Three layers of enforcement, and only one is a lock

| Layer | What it is | Worth |
|---|---|---|
| `AccessGate` on the page | a **sign** — explains to a person why they were not let in | zero as protection: a browser check is switched off in that same browser |
| `proxy.ts` | proves a session EXISTS | stops an anonymous visitor and nothing more — any signed-in person passes |
| `requireRoles(req, [...])` in the door | the **lock** | the only thing that actually decides |

So every `/api/*` handler serving protected data asks for the role itself, first line, before it
reads the body. Three answers must differ: guest → **401**, signed in with the wrong role → **403
naming the required roles**, right role → the data. 403 rather than 404: the person is authenticated,
there is nobody to hide the route's existence from, and naming the roles gives the interface
something to say.

## 3. 🔒 A proxying door repeats the right of its source

Written here as `['admin','architect']` while the auth service allowed **architect only**: an `admin`
would have passed our lock and collected a 403 from the service — access promised and then refused,
with the cause in two places at once.

**The fix ran the other way, and that is the lesson.** The owner wanted administrators on that page,
so the SERVICE was widened and the door followed. Narrowing the door would have hidden his decision
inside our code, where nobody would find it. Read the upstream handler; when its right is wrong,
change it there.

## 4. 🔒 Widening a right needs its counterweight in the same change

Letting `admin` manage accounts is safe only because of one extra rule shipped with it: **an
administrator may neither grant nor remove `architect`.** Without it he hands that role to his own
second account and the difference between the two roles disappears the same day.

The general shape: **whenever you widen who may act, ask what that person could now do to their own
rights** — and close that path in the same change, not in the next one. Compare the CURRENT values
with the REQUESTED ones so the rule guards the one thing that matters rather than every edit.

Two more of the same family, already in the service: nobody edits their own account through an admin
screen, and deletion stays with `architect` because it is destructive.

## 5. The bypass, and why your test may mean nothing

On a node authentication is bypassed in `NODE_ENV=development`, and on `localhost` the owner at the
keyboard opens the architect layer without signing in (`lib/auth/owner-at-machine.ts`) — both hand you
`architect`. `FRACTERA_IP_NODOMAIN_MODE` belongs to the old server line; a node never sets it. So a page
tested on this computer is tested for the case that never fails. Say which mode you were in; it is one sentence, and it is the difference between a
proof and a habit.

A changed role reaches a signed-in person on their next session read, not instantly. Say that too
rather than promising immediacy.

## 6. Showing the right things

Menu visibility is courtesy, not protection: an entry names its group, `lib/menu/account-links.ts`
collects them, and the drawer shows what the person's roles allow. A public button leading to a 403
is a promise the site does not keep — so protected pages never appear in a public menu
(`place-page-in-menu`).

When the owner asks for "a page for X", the answer often splits in two: a public page that explains,
and a protected one where X works. Say that out loud — it is a product decision, not a technical one.

## 7. Before you call it done

- All three answers on the deployment, including both refusals. A door proven only with a valid
  session is proven for the case that never goes wrong.
- Fetch the page as a guest and grep the markup for the data it shows: it must not be there.
- If you widened a right, state in the report what the counterweight is.

## 8. 🔒 Роли переносимого проекта решаются ДО первого маршрута

**Решение владельца 2026-08-24, режим `migration`.** Фаза исследования открывается четырьмя вопросами,
и до ответа не строится ничего: **какой тип приложения · будет ли авторизация · будет ли ролевой
доступ · какие роли и что каждая ограничивает.**

**Почему именно здесь, а не при первой защищённой странице.** Ответ решает не одну дверь, а раскладку:
слой маршрута, группу прав, замок и то, что видит гость. Роль, выбранная «пока что», становится
постоянной, и каждая построенная на ней дверь переделывается.

**Как спрашивать:**

| Случай | Что делаешь |
|---|---|
| ответ выводится из исходника (схема, JWT, гейты) | называешь предположение прямо — «вот что я предполагаю» — и просишь подтвердить |
| не выводится | просишь указать прямо, без догадок |

🛑 **Нет ответа — законная остановка, а не провал шага.** Скажи, что именно станет невозможно.

⚠️ **Роли исходника почти никогда не ложатся на группы прав один в один.** Две роли чужого проекта
(`admin`, `operator`) — это не `admin` и не `staff` здесь; раскладка есть решение владельца, а твоё
дело — показать ему обе стороны соответствия.

## 9. 🔒 Слово владельца против ЗАПИСАННОГО решения владельца — это вопрос

✗ **Поймано живьём 2026-08-24.** Владелец сказал «администратор получает доступ по всем функциям», а в
`lib/roles.ts` стоит его же решение от 2026-08-11: `admin` намеренно только в своей группе, потому что
в группе персонала он получал бы права персонала объединением и «ограничение» жило бы лишь в
ненарисованной кнопке.

**Свежая фраза звучит как приказ, а запись выглядит как история** — и агент исполняет фразу, отменяя
решение молча. Формулировка, которую стоит помнить: **молчаливая отмена записанного решения — худший
вид изобретения, потому что выглядит как реализация.**

**Что делать:** показать обе вычитки по строке · назвать цену каждой · **остановиться и ждать слова**.
Отмена записанного решения оформляется надгробием с датой и противовесом, а не правкой массива.

🔒 **Расширение права — всегда с противовесом.** «Пусть видит всё» решается не добавлением роли в
чужую группу (объединение раздаёт разом всё), а явным перечислением роли там, где владелец
действительно этого хочет, — каждое расширение видно и обсуждаемо.
