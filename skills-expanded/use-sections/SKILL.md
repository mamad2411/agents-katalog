---
name: use-sections
description: >
  The SECTION layer — the closed catalogue of block kinds every page is built from, and what it takes
  to add one. Load it when a page needs a look the catalogue does not have, when you are about to
  write anything under `sections/`, or when the owner says "make a block that…". The decision this
  skill exists for is made before the first file: a new kind is a promise the platform keeps forever,
  and most of what feels like a new kind is a widget belonging to one route. Adding one wrongly does
  not fail loudly — it quietly makes the project's look un-maintainable.
---

# use-sections

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

## 1. What the layer is

A page is a list of blocks; a **kind** is one entry in the catalogue, and its **renderer** is the one
file that draws it.

```
lib/content/blocks/types.ts    the SHAPE of every kind — what fields it has
sections/blocks/<kind>.server.tsx   ONE kind, ONE file — how it looks
sections/index.ts              the SECTIONS map — the authoritative list
sections/contract.ts           what a renderer receives
```

**Перед выбором вида читай `sections/BLOCKS.md`** — порождаемую сводку по всем видам: имя, семейство,
поля, и есть ли у вида карточка с правилами владельца. Она отвечает на вопрос момента выбора и избавляет
от чтения двадцати девяти рендереров.

🔒 **Сводка не заменяет карточку.** Каталог говорит, что вид СУЩЕСТВУЕТ; только карточка говорит, что он
ВЫДЕРЖИТ — сколько элементов, что ломается за пределом, когда его не брать. Есть карточка — открой её.

### 🔒 Карточка — «инструкция блока», и там, где высказался владелец, она ОБЯЗАТЕЛЬНА

Владелец назвал карточку так сам: место, где «можно рекомендовать использование и наложить
ограничения». Туда идут три вещи: **рекомендации** · **ограничения** (сколько элементов выдержит, что
ломается за пределом) · **решения владельца дословно, с датой**.

🔒 **СКАЗАЛ ВЛАДЕЛЕЦ — ЗАПИШИ В КАРТОЧКУ, А НЕ ТОЛЬКО В КОММЕНТАРИЙ.** Комментарий в рендерере читает
тот, кто уже открыл этот файл; карточку читает **каждый**, кто выбирает вид, — навык ведёт сюда. Правило,
осевшее только в коде, для следующей сессии не существует.

**Это проверяется машиной, а не памятью.** `check:sections` отказывает, если рендерер ссылается на
решение владельца, а карточки нет, и предупреждает, если карточка есть, но слов владельца в ней нет.
✗ измерено 2026-08-30: одиннадцать рендереров цитировали владельца, у трёх карточки не было вовсе.

🔒 **КАРТОЧКА НУЖНА НЕ ВСЕМ ВИДАМ, И ЭТО НЕ ПОСЛАБЛЕНИЕ.** «Карточка рождается, когда о виде что-то
узнали»; пустая, написанная ради полноты таблицы, не учит никого. Сторож требует её ровно там, где есть
что записать, и молчит там, где нечего.

Сводка порождается (`npm run build:blocks-map`), свежесть стережёт `check:blocks-map` в `prebuild`.
Правки руками теряются: источник — реестр `SECTIONS` и типы.

## 🔒 Как назван блок: владелец говорит «`quote01`»

У каждого блока есть **код** — первая колонка `sections/BLOCKS.md`: `quote01`, `workspace02`. Этим кодом владелец и называет блок в задаче:
«собери секцию из этого и этого».

**Что делать, получив код.** Открыть `sections/BLOCKS.md`, найти строку по коду — он в **первой
колонке** — и взять из неё вид и поля. Этого хватает, чтобы собрать секцию, не открывая ни одного
рендерера и не переспрашивая.

🔒 **КОД УКАЗЫВАЕТ НА ОБРАЗЕЦ, А НЕ НА ВИД, И ЭТА РАЗНИЦА МЕНЯЕТ ОТВЕТ.** У одного вида образцов
бывает несколько: `workspace01` — рабочий экран **без** верхнего ряда разделов, `workspace02` — он же
**с** рядом. Вид один (`workspace`), различает их одно поле. Услышав `workspace02`, нельзя взять
«просто workspace»: номер называет настройку, а не только вид.

Полей из сводки не хватило — тогда, и только тогда, открывается сам образец:
`app/[lang]/(protectedLayer)/(admin)/blocks/_data/specimen.ts`, запись с тем же порядковым номером
среди образцов своего вида.

🔒 **НЕ ПУТАТЬ С ЧИСЛОВЫМ `id`** (`0015`, `0035`) из `SECTIONS.json`: это внутренний ключ панели
управления, и языком общения он не является. Решение владельца 2026-08-30: у них разные читатели и
разные обязанности, сводить их в один он отказался осознанно.

✗ **Чем оплачен этот раздел (2026-08-30).** Коды показывались человеку и не попадали никуда больше —
ни в сводку, ни в карту, ни в один из 48 навыков. Путь при этом был построен: навык честно приводил
агента сюда, в `BLOCKS.md`, а кода здесь не было. Дефект худшего рода — он не выглядит поломкой:
агент читает то, что велено, и не находит.
→ `development-docs/reports/errors-block-identifiers-live-only-on-screen-and-reach-no-skill.md`

## 🔒 Фабрика страницы не изобретает вёрстку

Всё на странице приходит **видом каталога** или **платформенным примитивом** — третьего источника нет
(закон владельца 2026-08-22). Своя разметка в фабрике означает второй слой отрисовки: каталог
перестаёт описывать страницу целиком, правило вида до фабрики не доезжает, и гейты слоя её не видят.

**Признак нарушения:** в файле фабрики или страницы написана разметка с классами вида
`rounded-2xl border bg-muted/40` — то есть переизобретена карточка. Это кандидат в вид каталога.

**Не нарушение:** `PageHeader`, `StaticImage`, примитивы типографики — они общие и платформенные.

**Закон исполнен (шаг 542, 2026-08-22).** В фабрике нет ни одного `className`: оглавление и
вопрос-ответ стали видами `toc` и `faq`, а хром страницы — примитивами `PageCover`, `BackLink` и
`PageHeader` (он же рисует строку сведений по частям `metaItems`).

🔒 **Хром видом каталога НЕ становится.** Строка автора, обложка, ссылка «назад» появляются оттого,
что у страницы есть автор, обложка и уровень выше, — их не выбирают в списке блоков. Вид, который
нельзя поставить, врёт о назначении каталога. Нашёл такую вещь — ей место в `components/`, а не в
`sections/`.

## 🔒 Выбирают по НАЗНАЧЕНИЮ, а не по имени

Виды разложены на **одиннадцать типов** (`sections/taxonomy.json`): десять частей лендинга плюс
материал страницы. Порядок выбора всегда такой:

1. **какой это тип** — «нужен раздел про шаги» → `how-it-works`;
2. **какой вид внутри типа** — там `flow`;
3. **что он выдержит** — карточка `sections/blocks/flow.md`.

| Тип | Виды сегодня |
|---|---|
| 1 герой · 2 преимущества · 3 как это работает | `hero` `heroSplit` · `cards` `badges` · `flow` |
| 6 сравнение · 7 тарифы · 8 отзывы | `problemSolution` · `noBill` · `founder` |
| 10 доверие и логотипы | `metrics` `languageMarquee` `projectTypeMarquee` |
| 11 материал страницы | остальные восемнадцать |

🔒 **Трёх типов не закрывает ни один вид: `product-demo`, `use-cases`, `showcase`.** Просят раздел
такого рода — говоришь прямо, что готовой секции нет, и предлагаешь либо собрать из соседнего типа,
либо завести новый вид (это работа, а не мелочь: рендерер, образец, карточка, гейты). **Не подменяй
молча**: `cards` вместо кейсов выглядит похоже и решает не ту задачу.

**Вид не назван в таксономии — он материал страницы.** Умолчание намеренное: новый вид виден в
каталоге в тот же день, пусть и в последнем типе. Появился вид с назначением — впиши его в
`taxonomy.json` тем же шагом, что и рендерер.

Отдельной витрины у каталога нет: его читают по `sections/BLOCKS.md` и карточкам `sections/blocks/<kind>.md`; на сайте секция
выглядит так, как её красят токены ядра.

**How many kinds exist: ask `sections/index.ts`, never a document.** `npm run check:sections` prints
the count. A number written into prose is stale the week after — this project's own instruction said
28 while the gate answered 29.

## 2. 🔒 The catalogue is closed by construction, and that is the point

`SectionSet` is a mapped type over every `Block["kind"]`. Add a kind to the catalogue without writing
its renderer and **the project does not compile** — you learn in a second, not in a month by an empty
patch on a page. No gate can offer that: a gate runs when somebody runs it, a type always runs.

The consequence to hold on to: **every kind is the platform's responsibility forever.** It needs its
renderer, its specimen on the catalogue page, its behaviour in every theme and every language, and it
will be maintained by whoever comes next. That is the price of the promise, and it is why the answer
to "we need a new look" is usually not a new kind.

## 3. 🔒 Which is it — a kind or a widget?

One question decides, and it is not about difficulty:

> **Would this look suit ANY page of the project, or only this one?**

**Any page → a kind.** It joins the catalogue, gets a specimen, becomes shared property.

**Only this route → a widget** (`_widgets/{static|dynamic}/<name>/` inside the route, `use-widgets`).
Unique layout, a borrowed library, its own behaviour, a wow element — all of that is a widget, and the
value is precisely that it suits nobody else.

The failure mode is one-directional and slow: a catalogue grown one kind per single page ends up with
kinds nobody reuses, while the thing that was genuinely unique had to be made general to get in.

Two more markers worth naming:

- **A section renderer never takes a build-time dependency of its own.** Something needing a package
  and a build is a **tool** (`_tools/`, `use-tools`), mounted from wherever it is needed.
- **A section owns its LOOK, not the shape of its data.** Fields live in `blocks/types.ts`. A renderer
  decides how `quote` looks and not what `quote` is made of — otherwise material stops being portable
  between the page, the markdown twin and the map, and it is the same material in all three.

## 4. Writing one, when it really is a kind

Four edits, and the type will not let you skip any:

1. the shape in `lib/content/blocks/types.ts`;
2. the renderer `sections/blocks/<kind>.server.tsx`;
3. the entry in `sections/index.ts`;
4. a **specimen** on the catalogue page — `check:sections` refuses a kind that is rendered nowhere
   (`kind-not-rendered`): a kind drawn on no page is checked by nothing.

🔒 **No file under `sections/` carries `"use client"`.** This is a property of the layer, not a habit:
renderers are server components, and anything interactive lives in an island the renderer mounts from
`components/`. The island receives resolved strings as props — a client file importing a dictionary
ships every language to the browser. Pattern to copy: `project-type-marquee.server.tsx`.

## 5. 🔒 Colour comes from the theme, always

`check:sections` refuses:

- **`absolute-colour`** — a literal colour in a class or, worse, in an inline style. An inline style
  outranks a class and does not hear the theme at all; a section painted that way stops changing with
  the rest of the site and nobody notices until the owner switches his palette.
- **`fill-without-pair`** — `bg-primary` without `text-primary-foreground`. Fills and their text come
  in pairs; half a pair is unreadable text in exactly one theme.

**What to write instead of an absolute colour** — the same tokens the rest of the product uses:

| Instead of | Write |
|---|---|
| `bg-black`, `bg-zinc-900` | `bg-background`, `bg-muted` |
| `text-white` | `text-foreground` |
| `text-white/50`, `/40` | `text-muted-foreground` |
| `border-white/10` | `border-border` |
| a named accent (`violet-600`) | `bg-primary` + `text-primary-foreground` |

🔒 **Sweep the SHARED ENGINE too, not only your section folder.** A section can be perfectly clean and
still render dark, because posts are drawn by `components/content-page/` and `lib/content/blocks/`.
The blog was fixed once by sweeping its own folder, and its post pages stayed black for another round.

The contract file carries no colour and no class deliberately: the first look-detail that leaks in
becomes mandatory for every renderer at once.

## 6. 🔒 One page, no repeated kinds

The owner's rule: a kind does not appear twice on the same page. The eye recognises the drawing before
it reads the words, so a second block of the same shape reads as a repetition even when the text is
entirely different. Counted for standalone sections (`flow`, `cards`, `metrics`, `panel`, …), not for
what lives inside them — a paragraph, a card, a list item is material, not a second section.

No gate catches this. It is a question you ask yourself before reaching for a ready kind: *is this
drawing already on the page?* If it is, the honest answer is a different kind — that is normal work,
not extra work. `problemSolution` exists because of exactly this.

## 7. 🔒 Число колонок сохраняется у ЛЮБОГО вида, если не описано обратное

Владелец, дословно (2026-08-31): «смысл того, что мы заложили дизайн, — нужно переиспользовать без
добавления количества колонок; это относится вообще ко всем. Если три колонки, то их должно быть три,
если две — то должно быть две, за исключением тех, где в описании будет описано, что и как можно
масштабировать. Если не описано — количество колонок сохраняем как есть».

🔒 **ЭТО ПРАВИЛО ПО УМОЛЧАНИЮ ДЛЯ ВСЕГО КАТАЛОГА, А НЕ ЗАМЕЧАНИЕ ПРО ОТДЕЛЬНЫЕ ВИДЫ.** Сколько
колонок у вида — столько и рисуется. Три значит три, две значит две, одна значит одна. Не «обычно»,
не «по умолчанию», не «если поместится»: **столько**. Спрашивать себя, подходит ли тут другое число,
не нужно — ответ уже дан устройством вида.

🔒 **МОЛЧАНИЕ ОПИСАНИЯ = ЗАПРЕТ, А НЕ РАЗРЕШЕНИЕ.** Исключение существует ровно одно: карточка вида
(`sections/blocks/<kind>.md`) прямо описывает, **что и как в нём можно масштабировать**. Нет такой
записи — сетка неприкосновенна. Обратное прочтение («раз не запрещено, значит можно») здесь неверно:
у молчания одно значение, и оно «как есть».

🔒 **ЗАЧЕМ ЭТО ВООБЩЕ ЕСТЬ: ДИЗАЙН УЖЕ ЗАЛОЖЕН, ЕГО ПЕРЕИСПОЛЬЗУЮТ, А НЕ СОЧИНЯЮТ ЗАНОВО.** Каталог
существует, чтобы страницы проекта выглядели одним продуктом. Вид, у которого на одной странице три
колонки, а на другой четыре, — это уже два разных вида, и единство, ради которого каталог заведён,
кончилось. Меняя сетку, ты не подгоняешь блок под страницу: ты **тратишь чужой дизайн**.

🔒 **СОДЕРЖИМОЕ ПОДГОНЯЕТСЯ ПОД СЕТКУ, А НЕ СЕТКА ПОД СОДЕРЖИМОЕ.** Пришло четыре элемента в
трёхколоночный вид — это не повод сменить сетку. Это одно из двух: либо четвёртый лишний, либо взят
не тот вид. Оба ответа честные; правка `grid-cols` — нет.

| Столкнулся с | Верный ход |
|---|---|
| элементов больше, чем колонок | убрать лишние или взять другой вид |
| элементов меньше, чем колонок | тоже не тот вид: полупустая сетка читается как недоделанная страница |
| «а давай тут в две колонки» | это заявка на ДРУГОЙ вид или на новый, а не правка существующего |
| карточка описывает масштабирование | делай, как описано в ней, и только в описанных пределах |

🔒 **ЗАПРЕТ КАСАЕТСЯ ШИРОКОГО ЭКРАНА.** Как вид складывается на узком — часть его собственного
устройства: одна колонка на телефоне, две на планшете. Трогать это не нужно и не запрещено — речь о
том виде, ради которого вид и выбран, на обычном рабочем мониторе.

🔒 **И НИКОГДА НЕ ПРАВЬ СЕТКУ РЕНДЕРЕРА РАДИ ОДНОЙ СТРАНИЦЫ.** Вид стоит на десятках страниц, включая
те, которых ты не видел. Правка `grid-cols` меняет их все разом — молча.

✗ **ЧЕМ ЭТО УЖЕ ОПЛАЧЕНО — ОДИН ИЗМЕРЕННЫЙ СЛУЧАЙ ИЗ МНОГИХ ВОЗМОЖНЫХ.** У `metrics` рендерер
`grid-cols-3`, а тип принимает массив без границы: четвёртое число **собирается, доезжает и встаёт
одиноко у левого края**. Сборка молчит, типы молчат, ломается только вид — и находит это человек, а
не проверка. Здесь он приведён не как исключение из правила, а как показ того, что **ни сборка, ни
типы это правило не сторожат: сторожишь его ты.**

## 8. 🔒 Every kind has a card, and the card is where the owner's taste is remembered

`sections/blocks/<kind>.md`, beside the renderer. Free form, written for a model to read: the family
it belongs to (`proof`, `breakdown`, `action`, `story`, …), how many elements it holds and **what
exactly breaks** past that, when to reach for it, when not to.

🔒 **КАРТОЧКА — ЕДИНСТВЕННОЕ МЕСТО, ГДЕ ОБЪЯВЛЯЕТСЯ МАСШТАБИРОВАНИЕ СЕТКИ** (закон 7). Если у вида
колонки можно менять, здесь написано **что именно и в каких пределах**. Молчание карточки об этом —
не пробел, который можно восполнить рассуждением: это и есть ответ «как есть». Заполняя карточку, не
пиши «можно масштабировать» вообще — либо назови предел, либо не пиши ничего.

Read the card before using a kind. The catalogue tells you a kind EXISTS; only the card tells you what
it can carry — and that difference has already cost real work: `metrics` is `grid-cols-3` in the
renderer while its type accepts an unbounded array, so a fourth number compiles, ships, and lands
alone against the left edge.

**Cards are not written in advance for all 29.** A card is born the moment somebody learns something
about that kind — usually the owner, usually because something looked wrong. An empty card written to
fill a checklist teaches nobody.

### The rule is caught in the dialogue, not applied silently

**Trigger:** the owner corrects the LOOK rather than the text — "drop the fourth one", "this is ugly",
"it doesn't sit right", "put it back the way it was".

**What you do — and this is the whole mechanism:** fix it, and then ask.

> What exactly is wrong with it? If this section is built wrong, we can change its instruction so it
> works better next time — want to tell me more?

**Then write his answer into the card**, in his words, with the date. Not "the agent decided three" —
his rule, his reason.

🔒 **Silently fixing and moving on is forbidden.** The same correction reaches the next agent, who has
no way to know it was ever made, and the owner pays for the same work twice. A rule spoken once must
survive the session that heard it — that is the same discipline as skill evolution in `CLAUDE.md`,
one level down.

**What counts, goes in the TYPE instead.** "Exactly three" is countable: a tuple in
`lib/content/blocks/types.ts` makes the fourth element fail to compile, and prose only teaches while a
type refuses. "Looks wrong right after `flow`" is not countable — that stays in the card. Change the
type only when the owner has confirmed the number is hard, never on your own reading of the CSS.

## 9. Before you call it done

- `check:sections` — every kind has a specimen, colours are tokens, fills carry their pairs.
- `check:typography`, `check:layout`, `check:contrast` — text through the primitives, no size that
  shrinks as the screen grows, contrast that survives both themes.
- Open the catalogue page and look at the specimen in **both** themes and in a narrow window.
- Read the page you built with JavaScript off: a server renderer plus an island degrades visibly; a
  renderer that drew nothing without scripts is the mistake this layer is shaped to prevent.

- **Building the inside of a new kind?** The vendored `shadcn` skill composes it best; `use-shadcn`
  says when that is legal and what the section layer forbids it regardless.
