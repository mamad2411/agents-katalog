---
name: use-widgets
description: >
  Widgets — the unique, route-owned pieces a project is recognised by. Load this BEFORE building any
  screen element that is not a plain content block: a table with its own behaviour, an animated
  showcase, a calculator-looking panel, anything a designer handed you as finished code. Also load it
  when the owner says "make it look like this", "here is a block from my other site", "put a widget
  after the hero", or asks why an animation must not sit on the page itself. Two kinds exist —
  `_widgets/static/<name>` and `_widgets/dynamic/<name>` — and the folder names them out loud because
  the two obey different disciplines.
---

# use-widgets

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

A widget is **a unit of ownership inside one route**. Everything that answers *"how does THIS thing
look and behave"* lives in its folder: markup, skeleton, behaviour, words. Delete the route folder and
the widget is gone without a trace — that deletion test is the acceptance, not a metaphor.

What a widget is NOT: a reusable component. Reuse is the opposite of the point. Two widgets that look
alike are two widgets, and they are allowed to drift apart tomorrow — that freedom is the whole value.

## 🔒 Сначала прочитай аналог — до первой строки

**Обойди `_widgets/` по дереву и назови, что уже построено.** Затем открой ближайший по смыслу и
прочитай его ЦЕЛИКОМ, а не по диагонали. Только после этого пиши свой.

```
find app -type d -path "*_widgets/*/*"
```

**Что берётся у аналога:**

| Берётся | Почему |
|---|---|
| **устройство** — какие файлы, что в каком лежит | `use-list` · `toolbar` · `skeleton` · `row` · `pager` · `ui.i18n` — состав проверен работой, свой порядок изобретать не за чем |
| **вид** — ритм отступов, шапка таблицы, чередование строк, размеры кнопок и полей | страницы одного продукта обязаны выглядеть роднёй |
| **состояния** — закрыт, загрузка, пусто, отказ: какие есть и в каком порядке показываются | пропущенное состояние обнаруживает владелец, а не гейт |

**Не берётся:** сам файл импортом, поведение выборки, слова, колонки, действия строки.

🔒 **ИЗОЛЯЦИЯ — ПРО ФАЙЛЫ, СЕМЕЙНОЕ СХОДСТВО — ПРО ВИД, И ЭТО НЕ ПРОТИВОРЕЧИЕ.** Правило «четыре
копии таблицы — не дублирование, а изоляция» говорит: не делите код. Оно НЕ говорит: стройте разный
вид. Разойтись виджеты обязаны в том, ЧТО делают, а не в том, КАК выглядят.

**Оплачено 2026-08-21.** Таблица учётных записей была построена с нуля по правилу изоляции: свой ритм
отступов, заголовки колонок без приглушения, поиск после раскрытия, до нажатия — голая кнопка вместо
скелетона. Каждое решение по отдельности защитимо, вместе — страница из другого сайта. Владелец
сказал дословно: «not similar design, copy widget design from another pages». Ни один гейт этого не
поймал и поймать не мог: разметка формально верна.

**Дешёвая проверка, которая ловит это до владельца:** открой свою страницу и соседнюю рядом, в двух
вкладках. Разница видна за секунду и не требует замеров.

## Two kinds, and the folder says which

```
<route>/_widgets/static/<name>/    отрисован сразу и целиком   — public layer, first impressions
<route>/_widgets/dynamic/<name>/   просыпается по нажатию      — protected layer, data behind a door
```

The path shape is enforced by `check:protected`: a file under `_widgets/` that sits outside
`static/` or `dynamic/` fails the build. Nothing else is enforced — folders are not created in
advance, because a folder that stands everywhere proves nothing when the deletion test comes.

Specimens in this starter: five dynamic (`price-table`, `manage-table`, `catalogue-table`,
`shop-table`, `product-card`) and one static (`security-orbit`, on the homepage).

## The boundary rule — the one sentence to keep

> **Outward goes what answers "how does the project do X at all".
> Inside stays everything that answers "how does THIS widget look and behave".**

Outward: `lib/architecture/project-api` (the way this project talks to its database), `toast`, the
primitives in `components/ui/*`, the entity model in `lib/<entity>/`, tools in `_tools/`.
Inside: layout, columns, empty state, interactions, words — **and the skeleton**.

**The test at the border:** move a piece outward — would that force two widgets to be alike in
anything? If yes, it stays inside.

🚫 **Merging fragments of widgets into a shared library is forbidden** (owner's direct word). Four
copies of a table are not duplication, they are isolation. It would be duplication only if the tables
were the same — and the whole bet is that they are not.

**The skeleton is the sharp case.** A shared skeleton decides in advance that every table has the same
shape: while it is one for four, none of them can look different even while loading. That was caught
live — the shared one drew five columns for a table that has three, and the layout jumped when the
answer arrived.

## Ask first whether an island is needed at all

Tabs, highlighting, reveal-on-select, a lit step — plain CSS does most of this, and then there is no
island: the page works without JavaScript *fully*, not tolerably, and no second copy of the text "for
crawlers" is required. The specimen is the section kind `problemSolution`: the list of cases is a
group of radio inputs, and showing the selected one is a `:checked` rule in `styles/globals.css`.

Reach for an island only when browser state is unavoidable — a database call, an input, a timer. An
island bought for something CSS already does costs the no-JS visitor the whole element.

## One page, no repeated section kinds

A section kind appears once per page. The eye recognises a layout before it reads a word, so a second
section of the same kind reads as a repeat however different the text. Caught by asking "is this shape
already on the page?" before reusing a kind — no gate enforces it.

## Movement: the island rule, and why it is about search, not taste

Classic use of a motion library kills SEO. The page goes dynamic, the markup ships with `opacity: 0`,
and the crawler — like anyone with JavaScript off — sees empty space. So:

1. **The server prints stillness.** A static twin, fully visible, whose letters carry their own
   colour. 🔒 `opacity: 0` is one mechanism out of many — read "Present in the markup and still
   unreadable" below before you call the twin honest.
2. **An island holds the twin** and swaps in the animated version. 🔒 **The event is chosen by the
   price of the motion, not copied from the specimen.** Expensive or decorative — on the **first
   click, or when the pointer enters the area** (`pointerenter`; a finger never fires it, so touch
   keeps the click). Cheap and part of the meaning — the page's own heading, a word that must be
   alive for everyone — **right after mount**, the library still lazy, because asking a person to
   activate a title means showing it to nobody. Name the chosen event and its reason in the file.
3. **The animated version loads lazily** (`lazy` + `Suspense`), and the fallback of the swap is the
   twin itself — so nothing blinks while the chunk flies.
4. **Both versions share one markup file.** Geometry must match 1:1 at any width; measure the
   bounding boxes before and after the swap and demand equality.
5. **`prefers-reduced-motion` is respected**: the swap happens, the movement does not.
6. Movement is declared with `animate` and **no `initial`** — it starts from the current state, which
   is what makes the swap invisible.

Read `security-orbit` before writing your own: `index.tsx` (server, resolves words), `static.tsx`
(the twin), `swap.client.tsx` (the island), `animated.client.tsx` (motion), `parts.tsx` (the one
markup), `ui.i18n.ts` (its words).

## Present in the markup and still unreadable

🔒 **The defect is one class, and `opacity` is only its most famous member: the colour and the
visibility of the letters are decided by something around them instead of by themselves.** `curl`
finds the text, search indexes it, the gate stays green — and the person without JavaScript is handed
a heading in the colour of a caption, or nothing at all.

The ways in, none of them exhaustive:

- `text-transparent` / `color: transparent` with `bg-clip-text` — the background paints the letters;
- `clip-path`, `mask-image` — the letters are cut out of something else;
- `visibility: hidden`, `content-visibility`, a container of zero height;
- text living in `::before` / `::after`, or in an icon font;
- any `initial` style of a motion library, not only the transparent one.

🔒 **Partial degradation is worse than total.** A title that vanishes is noticed in a second. A title
whose real colour was `transparent`, drawn by a second static background layer, simply looks *slightly
grey* — no `curl`, no gate and no person who has not seen the intended colour will catch it. This is
why the no-JS proof measures the **computed colour**, and why a "the text is in the HTML" answer is
not an answer.

🔒 **When the component comes from someone else's registry, read the technique, not the manifest.**
Its dependencies tell you what will be installed; how it paints the content tells you what the reader
gets — and only the second one can hand you transparent letters. `use-tools` carries this as a rule.

## Two ways a widget reaches a page

| Where | How | Example |
|---|---|---|
| Behind authorization | the route entry (`_components/index.tsx`) imports it and passes resolved words | `manage-table` |
| Public homepage | the `afterHero` slot of `createContentPage` — full width, right after the first screen, outside the column | `security-orbit` |

**Why not a new block kind.** The section catalogue is closed and every kind needs a specimen on the
architect's page — a public widget would have to be rendered from the protected layer, i.e. the
platform would import a route. The slot keeps ownership where it belongs.

## Words

Ten languages, the page set (`en ru es fr it de pt pl tr nl`), in the widget's own `ui.i18n.ts`, and
registered in `scripts/check-i18n.mjs` in the same commit. Eighty-two is for reusable parts of the
product — the account drawer, the cart, dialogs — because those appear in any enabled language by
themselves. A widget does not. Enable an eleventh language and the widget answers in English: a
deliberate trade, written in the header of every widget dictionary.

Words are resolved on the SERVER and handed to the island as props. A client file that imports the
dictionary ships every language to every browser.

## Colour: code that arrives from outside must learn the palette

Design handed over as finished code arrives with its own hex values. Translate them to tokens —
`--primary` and its fractions, `bg-card`, `border-border`, `text-foreground`,
`text-muted-foreground` — before anything else. Two reasons, both practical: the owner changes the
palette in the panel and the widget must repaint with the site; and `check:contrast` refuses
fractions on text (`text-muted-foreground/50`), because a fraction reads in one theme out of two.

Keep the donor's geometry, drop the donor's palette. Layout is what was chosen; colour is what the
project owns.

🔒 **A widget that takes the WHOLE screen inherits a page's duties.** The moment it is the page, it
owes what a page owes: the markdown twin for machines, an address in the sitemap, a heading hierarchy,
and honest behaviour without JavaScript — or an explicit statement that it requires it. ✗ "it is only a
widget" is how a full-screen thing ends up invisible to search and to models while looking finished.

## Proof

Green types prove nothing here. Four measurements, all cheap:

1. **The route stays `●`** in the build table. A widget that turns the page `ƒ` has already failed.
2. **No-JS, and the question is READABILITY, not presence.** `curl` the page: every title of the
   widget must be in the HTML — and then, with JavaScript switched off in the browser, the computed
   colour of those letters must equal the theme's text colour and their computed visibility must be
   normal. 🔒 Grepping the markup for `opacity: 0` is NOT this check: `bg-clip-text text-transparent`
   carries no `opacity` at all and still hands the reader a heading painted the colour of a caption.
   No browser at hand — say so out loud and record it as a debt; do not report the widget proven.
3. **The swap does not jump:** bounding boxes of the cards and the centre, before the first click and
   a second after — identical strings.
4. **Deletion:** remove the folder, run the gates, grep the tree. One line in the route entry and one
   in the i18n registry is the whole footprint; anything else means the widget was smeared.

5. **Foreign design knowledge has the widest room here** — a widget owes nobody but its route.
   `use-shadcn` names what still holds: one dialog, one toast, colour as a token.
