# agent-research-radar

Скилл для Claude Code и Codex, который следит за техническими блогами AI-лабораторий и
приносит **только фундаментальные посты про автономных агентов** — архитектуру,
память, длинные горизонты, оркестрацию, экономику прогона, эвалы. Продуктовые
анонсы, релизы моделей и кейсы без механики отсекаются.

> **EN:** A Claude Code skill that monitors AI-lab engineering blogs (Anthropic,
> OpenAI, Cursor, LangChain, Amp, Cognition, DeepMind and others) and surfaces
> only *fundamental* posts on autonomous-agent architecture — memory and context,
> long-running loops, self-improvement, orchestration, run economics, agent evals,
> long-horizon risks. Product announcements and model releases are filtered out.
> Docs are in Russian; the collector and sources are language-agnostic.

## Зачем

Читать все блоги целиком невозможно: только у Claude Blog выходит два-три поста
в день, у LangChain — под сотню за два месяца. При этом доля текстов, которые
действительно объясняют, **как устроен агент**, — единицы в неделю. Радар делает
за тебя триаж и отдаёт дайджест, где у каждого поста есть суть, числа и строка
«что забрать» — конкретное следствие для твоей собственной работы с агентами.

## Как работает

Два слоя, и это принципиально:

1. **Сбор — код.** `scripts/radar.py` (stdlib-only, только GET) обходит источники,
   фильтрует по окну дат, режет уже показанное, добирает точные заголовки и даты.
   Логики релевантности здесь нет вообще.
2. **Отсев — рубрика.** Решение «фундаментальный пост или продуктовая новость»
   принимает агент по письменной рубрике `references/relevance.md`. Регулярка по
   ключевым словам отрезала бы ровно то, что интересно: заголовок «Multiplayer»
   может быть и чатом, и архитектурой разделяемого состояния между агентами.

```bash
# всё за неделю, закончившуюся последним наступившим воскресеньем
python3 scripts/radar.py collect --json /tmp/radar.json

# только ядро источников, быстро
python3 scripts/radar.py collect --tier 1

# произвольное окно
python3 scripts/radar.py collect --since 2026-07-01 --until 2026-07-15

# живы ли источники
python3 scripts/radar.py check
```

## Источники

15 штук в трёх тирах — ядро жанра, смешанный поток и периферия с агрегаторами.
Список и обоснование каждого — `references/sources.md`, конфиг —
`scripts/sources.json`.

**Главная техническая находка: RSS почти ни у кого нет.** Ни у Anthropic
(`/engineering` и Claude Blog), ни у Cursor, ни у Cognition, ни у Factory.
У `developers.openai.com` фид формально есть, но покрывает только раздел `/learn`
и отстаёт на месяцы. Поэтому коллектор парсит HTML-индексы и добирает точные
метаданные со страниц постов через JSON-LD (`headline`, `datePublished`),
`og:title` и `article:published_time`.

Ещё три грабли, на которых ложится наивная реализация:

- `claude.com` отдаёт **HTTP 103 Early Hints**, на котором `urllib` падает —
  сделан автоматический откат на `curl --compressed`;
- `openai.com/index/*` закрыт Cloudflare: и обычный фетч, и `curl` получают
  заглушку «Enable JavaScript» — нужен браузер;
- ISO-даты вида `2026-07-25T22:44:05` ломают регулярку с `\b` на хвосте (между
  «25» и «T» нет границы слова) — из-за этого все Atom-фиды молча приходят без дат.

## Установка

```bash
git clone https://github.com/maddness/agent-research-radar.git ~/.claude/skills/agent-research-radar
# или для Codex
git clone https://github.com/maddness/agent-research-radar.git ~/.codex/skills/agent-research-radar
```

Дальше скилл подхватывается агентом автоматически и триггерится на «радар»,
«дайджест», «что нового в блогах про агентов» и подобное.

Состояния между прогонами скилл не хранит: одно и то же окно всегда даёт один и
тот же набор кандидатов. Дедуп работает только внутри прогона — URL канонизируются,
поэтому один пост из двух лент не удваивается.

## Структура

```
SKILL.md                       рабочий цикл: окно → сбор → триаж → чтение → дайджест
scripts/radar.py               коллектор (stdlib, только GET)
scripts/sources.json           каталог источников
references/relevance.md        рубрика отсева: три корзины, 10 осей, матрица скоринга
references/sources.md          зачем каждый источник и где его грабли
references/digest-format.md    шаблон отчёта и требования к нему
references/canon.md            карта опорных публикаций — база для оценки новизны
references/example-digest.md   эталонный прогон за 20–26 июля 2026
evals/evals.json               9 сценариев проверки
```

## Формат отчёта

Один Markdown-файл на прогон. Структура: топ «читать обязательно» (3, максимум 5)
с разбором механики и строкой «что забрать», список «стоит глянуть»,
сводка отбраковки и — обязательно —
**какие источники молчали или отвалились**. Тихо пропущенный источник читается как
«там ничего не было», а это дезинформация, а не краткость.

Живой пример — `references/example-digest.md`.

## Как добавить источник

В `scripts/sources.json` — объект с `id`, `name`, `tier`, `kind` (`rss` | `html`).
Для `html` нужны `link_pattern` (регулярка пути до поста, поддерживает lookahead
для отсечения служебных URL), `base` и обычно `verify: "jsonld"`. После —
`python3 scripts/radar.py check`: в колонке `raw` должно быть разумное число
ссылок, а `in60d` — не ноль, если блог живой.

## Лицензия

MIT — см. [LICENSE](LICENSE).
