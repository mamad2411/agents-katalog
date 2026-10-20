---
name: grove-db
description: >
  Мгновенный поиск по всему GroveMind через SQLite FTS5.
  3012 файлов, 9 категорий. Триггер: «найди», «поищи», «где у нас», «что есть про», «поиск по району», «grove search», «db search».
  Активация: любой поиск по знаниям района.
---
# grove-db — Мгновенный поиск по району

> SQLite FTS5 база всего GroveMind (3012 файлов).
> ВСЕГДА используй первым делом. Чтение файлов — фоллбэк.

---

## Пути

| Что | Где |
|-----|-----|
| База | `~/GroveMind/grove.db` (42.8 MB) |
| Индексатор | `~/GroveMind/grove_index.py` |
| Поиск | `python3 ~/GroveMind/grove_index.py --search "запрос" [--cat категория]` |
| Обновить | `python3 ~/GroveMind/grove_index.py` (инкрементально) |
| Переиндекс | `python3 ~/GroveMind/grove_index.py --full` |

---

## Когда использовать

**ВСЕГДА первым делом.** Любой запрос к знаниям GroveMind → СНАЧАЛА база, ПОТОМ grep/read.

| Ситуация | Команда |
|----------|---------|
| Брат спросил что-то про проект | `grove_index.py --search "запрос"` |
| Нужен скилл | `grove_index.py --search "pentest" --cat wiki` |
| Найти где лежит | `grove_index.py --search "файл или тема"` |
| Кто такая подруга | `grove_index.py --search "denise" --cat skills` |

---

## Категории в базе

| Категория | Файлов | Что внутри |
|-----------|--------|-----------|
| `wiki` | 2382 | Кибер-скиллы, уроки, находки, JB, модели |
| `archive` | 541 | Debi-prototype, старые наработки |
| `skills` | 57 | Скиллы CJ (персоны, тулзы, дизайн) |
| `SETUP` | 12 | Правила, инжекты, настройки |
| `_root` | 8 | BOOT, ORIGIN, AGENTS, CONVENTIONS, etc |
| `templates` | 5 | Шаблоны STATE, DECISIONS, TODO, ARCH |
| `checkpoints` | 4 | Чекпоинты сессий |
| `crew` | 1 | Подруги CJ |
| `sounds` | 2 | Саундтрек |

---

## Принцип

```
Спросили → grove_index.py --search → нашёл (1-2ms) → ответил
                                     → не нашёл → read/grep (фоллбэк)
```

**Экономия:** ~1000x меньше токенов vs чтение файлов.

---

## Как обновлять

```bash
# После правок в районе — инкрементально
python3 ~/GroveMind/grove_index.py

# После больших изменений — полный переиндекс
python3 ~/GroveMind/grove_index.py --full
```

Индексатор проверяет mtime — обновляет только изменённые файлы.

---

*GroveMind DB Skill v1.0 — База первым делом. Всегда.*
