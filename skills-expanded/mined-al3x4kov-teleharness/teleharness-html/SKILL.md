---
name: teleharness-html
description: HTML — самодостаточная страница или отчёт в одном .html-файле (встроенный CSS, картинки и графики внутри файла в base64, без внешних ссылок), отчёт из данных или таблицы через шаблон jinja2, конвертация Markdown в HTML, разбор и извлечение данных из HTML (BeautifulSoup). Используй, когда пользователь просит HTML-страницу, веб-отчёт, письмо-рассылку, лендинг в одном файле или достать данные из html.
---

# HTML: страницы и отчёты в одном файле

Библиотеки песочницы: **jinja2** (шаблоны), **markdown** (Markdown → HTML), **beautifulsoup4** (`bs4`, разбор), **pandas** (`df.to_html`), **matplotlib** (графики).

## Правила песочницы

- Команды выполняются в `cmd.exe` внутри песочницы (Windows AppContainer). Нет PowerShell, bash, браузера, Node.js; `pip install <пакет>` работает (ставится в папку пользователя).
- Код Python пиши в файл `.py` в рабочей папке пользователя (инструмент `write`) и запускай `python имя.py`. Многострочный `python -c "..."` в cmd ломается. Короткую статическую страницу можно сразу записать инструментом `write`.
- Все пути — относительные, внутри рабочей папки. Результат сохраняй туда же (кодировка UTF-8) и в ответе назови файл.
- Вывод проверяй из Python (печатает UTF-8). `type` в cmd может показать русский «кракозябрами» — это кодировка консоли.
- `dir` недоступен: список файлов — `list`/`glob` или `python -c "import os; print(os.listdir())"`.

## Правила самодостаточной страницы

- Один файл: CSS — в `<style>`, картинки и графики — `data:image/png;base64,...`, без CDN, внешних шрифтов и скриптов (файл откроют без интернета или перешлют по почте).
- `<!doctype html>`, `<html lang="ru">`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, осмысленный `<title>`.
- Системные шрифты: `font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`.
- Адаптивность: `max-width` у контейнера, таблицы в обёртке с `overflow-x: auto`, `@media print` для печати.
- Данные пользователя всегда экранируй (jinja2 `autoescape=True`) — в них могут быть `<`, `&`, кавычки.
- Цвета контрастные (текст не светлее `#555` на белом), в таблицах числа выровнены вправо.

## Рецепт 1. Отчёт из данных через jinja2 с графиком внутри файла

```python
# Рецепт: html-report — самодостаточный HTML-отчёт из данных: jinja2, inline CSS, график в base64
import base64, io
from datetime import date
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from jinja2 import Environment

OUT = "отчёт.html"
rows = [
    {"region": "Москва", "plan": 1200, "fact": 1350},
    {"region": "Казань", "plan": 900, "fact": 780},
    {"region": "Самара", "plan": 750, "fact": 760},
    {"region": "Пермь <ЮГ>", "plan": 600, "fact": 450},   # спецсимволы экранирует autoescape
]
for r in rows:
    r["pct"] = r["fact"] / r["plan"]
total = {"plan": sum(r["plan"] for r in rows), "fact": sum(r["fact"] for r in rows)}
total["pct"] = total["fact"] / total["plan"]

# график → base64
fig, ax = plt.subplots(figsize=(7, 3), dpi=120)
ax.bar([r["region"] for r in rows], [r["fact"] for r in rows], color="#2F5597")
ax.grid(axis="y", alpha=.3); ax.set_ylabel("тыс. ₽")
for s in ("top", "right"): ax.spines[s].set_visible(False)
buf = io.BytesIO(); fig.tight_layout(); fig.savefig(buf, format="png"); plt.close(fig)
chart = base64.b64encode(buf.getvalue()).decode()

TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
  :root { --primary: #1F3864; --accent: #ED7D31; --ok: #2E7D32; --bad: #C62828; --muted: #666; --line: #E3E6EA; }
  * { box-sizing: border-box; }
  body { margin: 0; font: 16px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; color: #1d1d1f; background: #F6F7F9; }
  .wrap { max-width: 960px; margin: 0 auto; padding: 32px 20px; }
  header h1 { margin: 0 0 4px; font-size: 28px; color: var(--primary); }
  header p { margin: 0; color: var(--muted); }
  .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 24px 0; }
  .card { background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: 16px 20px; }
  .card b { display: block; font-size: 28px; color: var(--primary); }
  .card span { color: var(--muted); font-size: 14px; }
  section { background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
  h2 { margin: 0 0 12px; font-size: 20px; }
  .table { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
  th, td { padding: 8px 12px; border-bottom: 1px solid var(--line); text-align: left; }
  th { background: var(--primary); color: #fff; font-weight: 600; }
  td.num, th.num { text-align: right; }
  tbody tr:nth-child(even) { background: #FAFBFC; }
  tfoot td { font-weight: 700; border-top: 2px solid var(--primary); }
  .ok { color: var(--ok); } .bad { color: var(--bad); }
  img { max-width: 100%; height: auto; }
  footer { color: var(--muted); font-size: 13px; text-align: center; }
  @media print { body { background: #fff; } section, .card { border: none; } }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>{{ title }}</h1>
    <p>Сформировано {{ today }}</p>
  </header>
  <div class="cards">
    <div class="card"><b>{{ "{:,}".format(total.fact).replace(",", " ") }}</b><span>факт, тыс. ₽</span></div>
    <div class="card"><b>{{ "{:,}".format(total.plan).replace(",", " ") }}</b><span>план, тыс. ₽</span></div>
    <div class="card"><b class="{{ 'ok' if total.pct >= 1 else 'bad' }}">{{ "%.0f"|format(total.pct * 100) }}&nbsp;%</b><span>выполнение</span></div>
  </div>
  <section>
    <h2>По регионам</h2>
    <div class="table"><table>
      <thead><tr><th>Регион</th><th class="num">План</th><th class="num">Факт</th><th class="num">Выполнение</th></tr></thead>
      <tbody>
      {% for r in rows %}
        <tr><td>{{ r.region }}</td><td class="num">{{ r.plan }}</td><td class="num">{{ r.fact }}</td>
            <td class="num {{ 'ok' if r.pct >= 1 else 'bad' }}">{{ "%.0f"|format(r.pct * 100) }}&nbsp;%</td></tr>
      {% endfor %}
      </tbody>
      <tfoot><tr><td>Итого</td><td class="num">{{ total.plan }}</td><td class="num">{{ total.fact }}</td><td class="num">{{ "%.0f"|format(total.pct * 100) }}&nbsp;%</td></tr></tfoot>
    </table></div>
  </section>
  <section>
    <h2>Факт по регионам</h2>
    <img src="data:image/png;base64,{{ chart }}" alt="Столбчатая диаграмма: факт продаж по регионам">
  </section>
  <footer>ООО «Ромашка» · отдел продаж</footer>
</div>
</body>
</html>"""

env = Environment(autoescape=True, trim_blocks=True, lstrip_blocks=True)
html = env.from_string(TEMPLATE).render(title="Продажи за IV квартал", today=date.today().strftime("%d.%m.%Y"),
                                        rows=rows, total=total, chart=chart)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("Сохранено:", OUT, len(html) // 1024, "КБ")
```

Таблица из pandas без шаблона: `df.to_html(index=False, classes="t", border=0, justify="left", float_format=lambda x: f"{x:,.2f}".replace(",", " "))` — и вставить в страницу через `{{ table | safe }}` (только для своих данных, не для HTML из интернета).

### Проверка

```python
# Проверка: html-report
from bs4 import BeautifulSoup

html = open("отчёт.html", encoding="utf-8").read()
s = BeautifulSoup(html, "html.parser")
assert s.title.string == "Продажи за IV квартал"
assert s.find("meta", charset=True) and s.style and "<script" not in html
external = [t for t in s.find_all(["link", "script", "img"]) if (t.get("src") or t.get("href") or "").startswith(("http:", "https:", "//"))]
assert not external, external
assert len(s.select("tbody tr")) == 4 and "&lt;ЮГ&gt;" in html
assert s.img["src"].startswith("data:image/png;base64,")
print("ПРОВЕРКА OK: один файл, без внешних ссылок, строк", len(s.select("tbody tr")))
```

## Рецепт 2. Markdown → оформленная HTML-страница

```python
# Рецепт: html-markdown — текст в Markdown в самодостаточную страницу с оглавлением
import markdown

md_text = """# Регламент работы с заявками

[TOC]

## Приём заявки
1. Проверить контакты клиента.
2. Завести карточку в CRM.

## Сроки
| Тип | Срок |
|---|---|
| Срочная | 4 часа |
| Обычная | 2 дня |

> Важно: **все** заявки фиксируются в течение часа.
"""
body = markdown.markdown(md_text, extensions=["tables", "toc", "fenced_code", "sane_lists"], output_format="html5")
page = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Регламент работы с заявками</title>
<style>
body {{ max-width: 760px; margin: 40px auto; padding: 0 20px; font: 17px/1.6 system-ui, "Segoe UI", Arial, sans-serif; color: #222; }}
h1, h2 {{ color: #1F3864; line-height: 1.25; }}
table {{ border-collapse: collapse; }} th, td {{ border: 1px solid #ccc; padding: 6px 12px; }} th {{ background: #F2F4F7; }}
blockquote {{ margin: 16px 0; padding: 8px 16px; border-left: 4px solid #ED7D31; background: #FFF6EF; }}
.toc {{ background: #F6F7F9; padding: 8px 16px; border-radius: 8px; }}
code, pre {{ background: #F2F4F7; border-radius: 4px; }} pre {{ padding: 12px; overflow-x: auto; }}
</style></head><body>
{body}
</body></html>"""
with open("регламент.html", "w", encoding="utf-8") as f:
    f.write(page)
print("Сохранено: регламент.html")
```

Markdown из файла пользователя: `md_text = open("файл.md", encoding="utf-8").read()`. HTML из Markdown пользователя может содержать сырой HTML — для чужого текста очищай его: убери `<script>`, `on*`-атрибуты через BeautifulSoup.

### Проверка

```python
# Проверка: html-markdown
from bs4 import BeautifulSoup

s = BeautifulSoup(open("регламент.html", encoding="utf-8").read(), "html.parser")
assert s.find("h1").get_text() == "Регламент работы с заявками"
assert s.find("table") and s.find("div", class_="toc") and s.find("blockquote")
print("ПРОВЕРКА OK: заголовки, таблица, оглавление, цитата")
```

## Рецепт 3. Достать данные из HTML

```python
# Рецепт: html-parse — таблицы и ссылки из HTML-файла (сохранённой страницы) в Excel
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

SRC = "отчёт.html"   # файл пользователя (страницу из интернета сначала скачай requests.get(...).text)
html = open(SRC, encoding="utf-8").read()
s = BeautifulSoup(html, "html.parser")
print("Заголовок:", s.title.string if s.title else "—")
print("Ссылки:", [(a.get_text(strip=True), a["href"]) for a in s.find_all("a", href=True)][:20])
tables = pd.read_html(StringIO(html))   # парсер lxml; html5lib в песочнице нет
print("Таблиц:", len(tables))
tables[0].to_excel("таблица_из_html.xlsx", index=False)
print(tables[0].to_string())
```

### Проверка

```python
# Проверка: html-parse
import pandas as pd

df = pd.read_excel("таблица_из_html.xlsx")
assert len(df) == 5 and "Регион" in df.columns
print("ПРОВЕРКА OK: таблица из HTML, строк", len(df))
```

## Как проверить результат

<!-- FEAT-04.12 -->
- **Посмотри результат глазами.** Отдельной командой (не в цепочке с `&&`): `teleharness-render "страница.html"` (или `--pages 1-3`). Страницу печатает настоящий браузер (Edge) без доступа к сети — внешние шрифты и картинки по http не загрузятся, поэтому всё встраивай: картинки страниц появятся в `_preview/<имя>/page-01.png …`. Открой их `read`/`look_at` (Claude — Read), сверь с задачей: ничего не обрезано, текст не вылезает за блоки, нет пустых слайдов и наложений, шрифт читается. Нашёл проблему — исправь скрипт, пересобери и посмотри снова. Пользователю `_preview` не называй.
- Итоговый файл — в рабочей папке чата под понятным именем; промежуточные (скрипты, вырезанные картинки) — в подпапке `_work`. Не перезаписывай файл, который создал не ты в этом чате: возьми новое имя. В ответе назови итоговый файл полным именем — под ответом появится его карточка для скачивания.
- Разбери файл BeautifulSoup'ом: есть `<title>`, `<meta charset>`, `<style>`; нет внешних `src`/`href` на `http(s)://` у `link`/`script`/`img`; число строк таблицы совпадает с данными.
