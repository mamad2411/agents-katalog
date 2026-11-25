---
name: teleharness-xlsx
description: Excel (.xlsx/.xls) — создать оформленный отчёт (заголовки, ширины колонок, форматы чисел, формулы, условное форматирование, диаграмма), изменить существующую книгу, прочитать и проанализировать таблицу через pandas. Используй, когда пользователь просит Excel-файл, таблицу, отчёт в xlsx или разобрать приложенную книгу.
---

# Excel: создание, оформление, анализ

Библиотеки песочницы: **XlsxWriter** (новый файл с диаграммами и условным форматированием), **openpyxl** (правка существующего .xlsx, чтение формул и стилей), **pandas** (анализ данных), **xlrd** (старый .xls).

## Правила песочницы

- Команды выполняются в `cmd.exe` внутри песочницы (Windows AppContainer). Нет PowerShell и bash. `pip install <пакет>` работает — пакет ставится в папку пользователя; документы смотри через `teleharness-render`.
- Код Python пиши в файл `.py` в рабочей папке пользователя (инструмент `write`) и запускай `python имя.py`. Многострочный `python -c "..."` в cmd ломается.
- Все пути — относительные, внутри рабочей папки. Результат сохраняй туда же и в ответе назови файл.
- Вывод проверяй из Python (печатает UTF-8). `type` в cmd может показать русский текст «кракозябрами» — это кодировка консоли, а не порча файла.
- `dir` недоступен: список файлов — `list`/`glob` или `python -c "import os; print(os.listdir())"`.
- Excel в песочнице нет, формулы никто не пересчитает: при чтении файла через pandas/openpyxl формула XlsxWriter вернёт то значение, которое ты передал в `value=` (по умолчанию 0). Итоги, которые нужно прочитать программно, считай в Python и передавай в `value=`.

## Как выбрать библиотеку

| Задача | Библиотека |
|---|---|
| Новый отчёт с нуля, диаграмма, условное форматирование | XlsxWriter |
| Изменить существующую книгу, сохранив её оформление | openpyxl (`load_workbook`) |
| Посчитать, отфильтровать, сгруппировать | pandas |
| Старый формат .xls | `pd.read_excel(..., engine="xlrd")` |

## Рецепт 1. Оформленный отчёт с формулами, условным форматированием и диаграммой (XlsxWriter)

```python
# Рецепт: xlsx-report — оформленный отчёт с формулами, условным форматированием и диаграммой
import xlsxwriter

OUT = "отчёт_продажи.xlsx"
rows = [  # (менеджер, регион, план, факт)
    ("Иванова А.", "Москва", 1200000, 1350000),
    ("Петров Б.", "Казань", 900000, 780000),
    ("Сидорова В.", "Самара", 750000, 760000),
    ("Кузнецов Г.", "Пермь", 600000, 450000),
    ("Смирнова Д.", "Уфа", 800000, 910000),
]

wb = xlsxwriter.Workbook(OUT)
ws = wb.add_worksheet("Продажи")

title = wb.add_format({"bold": True, "font_size": 14, "font_color": "#1F3864"})
head = wb.add_format({"bold": True, "bg_color": "#1F3864", "font_color": "#FFFFFF", "border": 1,
                      "align": "center", "valign": "vcenter", "text_wrap": True})
text = wb.add_format({"border": 1})
money = wb.add_format({"border": 1, "num_format": "# ##0 ₽"})
pct = wb.add_format({"border": 1, "num_format": "0.0%"})
total_lbl = wb.add_format({"bold": True, "top": 2, "border": 1})
total_money = wb.add_format({"bold": True, "top": 2, "border": 1, "num_format": "# ##0 ₽"})
total_pct = wb.add_format({"bold": True, "top": 2, "border": 1, "num_format": "0.0%"})

ws.merge_range("A1:E1", "Выполнение плана продаж, IV квартал", title)
headers = ["Менеджер", "Регион", "План, ₽", "Факт, ₽", "Выполнение"]
ws.write_row(2, 0, headers, head)
ws.set_row(2, 30)

first = 3  # строка Excel 4 (индексы с нуля)
for i, (name, region, plan, fact) in enumerate(rows):
    r = first + i
    ws.write(r, 0, name, text)
    ws.write(r, 1, region, text)
    ws.write_number(r, 2, plan, money)
    ws.write_number(r, 3, fact, money)
    # формула + заранее посчитанное значение (Excel пересчитает сам, а pandas прочитает value)
    ws.write_formula(r, 4, f"=D{r + 1}/C{r + 1}", pct, fact / plan)
last = first + len(rows) - 1
tr = last + 1
plan_sum = sum(x[2] for x in rows)
fact_sum = sum(x[3] for x in rows)
ws.write(tr, 0, "Итого", total_lbl)
ws.write(tr, 1, "", total_lbl)
ws.write_formula(tr, 2, f"=SUM(C{first + 1}:C{last + 1})", total_money, plan_sum)
ws.write_formula(tr, 3, f"=SUM(D{first + 1}:D{last + 1})", total_money, fact_sum)
ws.write_formula(tr, 4, f"=D{tr + 1}/C{tr + 1}", total_pct, fact_sum / plan_sum)

# ширины колонок, закреплённая шапка, автофильтр
ws.set_column("A:A", 18)
ws.set_column("B:B", 12)
ws.set_column("C:D", 15)
ws.set_column("E:E", 13)
ws.freeze_panes(first, 0)
ws.autofilter(2, 0, last, 4)

# условное форматирование: < 100% — красным, >= 100% — зелёным; цветовая шкала по факту
red = wb.add_format({"bg_color": "#F8CBAD", "font_color": "#9C0006"})
green = wb.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})
rng = f"E{first + 1}:E{last + 1}"
ws.conditional_format(rng, {"type": "cell", "criteria": "<", "value": 1, "format": red})
ws.conditional_format(rng, {"type": "cell", "criteria": ">=", "value": 1, "format": green})
ws.conditional_format(f"D{first + 1}:D{last + 1}", {"type": "3_color_scale"})

# диаграмма: план и факт по менеджерам
ch = wb.add_chart({"type": "column"})
for col, name, color in ((2, "План", "#8EA9DB"), (3, "Факт", "#1F3864")):
    ch.add_series({
        "name": ["Продажи", 2, col],
        "categories": ["Продажи", first, 0, last, 0],
        "values": ["Продажи", first, col, last, col],
        "fill": {"color": color},
    })
ch.set_title({"name": "План и факт, ₽"})
ch.set_y_axis({"num_format": "# ##0", "major_gridlines": {"visible": True, "line": {"color": "#D9D9D9"}}})
ch.set_legend({"position": "bottom"})
ch.set_size({"width": 620, "height": 320})
ws.insert_chart("G3", ch)

# параметры печати
ws.set_landscape()
ws.fit_to_pages(1, 0)
ws.repeat_rows(2)

wb.close()
print("Сохранено:", OUT)
```

Типы диаграмм XlsxWriter: `column`, `bar`, `line`, `pie`, `doughnut`, `scatter`, `area`. Для круговой — одна серия и `ch.set_style(10)`. Другие правила условного форматирования: `{"type": "data_bar"}`, `{"type": "top", "value": 3, "format": f}`, `{"type": "duplicate", "format": f}`, `{"type": "formula", "criteria": "=$E4<0.9", "format": f}`.

### Проверка

```python
# Проверка: xlsx-report
import openpyxl
import pandas as pd

wb = openpyxl.load_workbook("отчёт_продажи.xlsx")
ws = wb["Продажи"]
assert ws["A3"].value == "Менеджер" and ws["A3"].font.b
assert ws["E4"].value.startswith("="), "в E4 должна быть формула"
assert ws.column_dimensions["A"].width >= 18
assert len(ws.conditional_formatting) >= 2, "нет условного форматирования"
assert len(ws._charts) == 1, "нет диаграммы"
df = pd.read_excel("отчёт_продажи.xlsx", header=2)
print(df.head(3).to_string())
assert len(df) == 6 and df.iloc[-1]["Менеджер"] == "Итого"
print("ПРОВЕРКА OK: шапка, формулы, ширины, условное форматирование, диаграмма; строк:", len(df))
```

## Рецепт 2. Из pandas в оформленный Excel (несколько листов)

```python
# Рецепт: xlsx-pandas — DataFrame в оформленный Excel, сводная таблица на втором листе
import pandas as pd

df = pd.DataFrame({
    "Дата": pd.date_range("2026-01-01", periods=8, freq="W"),
    "Категория": ["Чай", "Кофе", "Чай", "Сахар", "Кофе", "Чай", "Сахар", "Кофе"],
    "Сумма": [1200, 3400, 900, 450, 2800, 1500, 600, 3100],
})
pivot = df.pivot_table(index="Категория", values="Сумма", aggfunc=["sum", "count"])
pivot.columns = ["Сумма", "Количество"]

OUT = "сводка.xlsx"
with pd.ExcelWriter(OUT, engine="xlsxwriter", datetime_format="dd.mm.yyyy") as xw:
    df.to_excel(xw, sheet_name="Данные", index=False)
    pivot.to_excel(xw, sheet_name="Сводка")
    wb = xw.book
    head = wb.add_format({"bold": True, "bg_color": "#DDEBF7", "border": 1})
    money = wb.add_format({"num_format": "# ##0"})
    ws = xw.sheets["Данные"]
    for c, name in enumerate(df.columns):
        ws.write(0, c, name, head)
    ws.set_column("A:A", 12)
    ws.set_column("B:B", 14)
    ws.set_column("C:C", 12, money)
    ws.autofilter(0, 0, len(df), len(df.columns) - 1)
    ws.freeze_panes(1, 0)
    xw.sheets["Сводка"].set_column("A:C", 14)
print("Сохранено:", OUT)
```

### Проверка

```python
# Проверка: xlsx-pandas
import pandas as pd

books = pd.read_excel("сводка.xlsx", sheet_name=None)
print(list(books))
assert list(books) == ["Данные", "Сводка"]
assert len(books["Данные"]) == 8
print("ПРОВЕРКА OK: листы", list(books), "строк данных", len(books["Данные"]))
```

## Рецепт 3. Правка существующей книги (openpyxl)

```python
# Рецепт: xlsx-openpyxl — открыть книгу, добавить колонку с формулой, стили, ширины, условное форматирование
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule
from openpyxl.utils import get_column_letter

SRC, OUT = "сводка.xlsx", "сводка_правка.xlsx"   # исходный файл не перезаписываем
wb = load_workbook(SRC)
ws = wb["Данные"]
last = ws.max_row
col = ws.max_column + 1
L = get_column_letter(col)
thin = Side(style="thin", color="BFBFBF")
ws.cell(1, col, "С НДС").font = Font(bold=True)
ws.cell(1, col).fill = PatternFill("solid", fgColor="DDEBF7")
for r in range(2, last + 1):
    c = ws.cell(r, col, f"=C{r}*1.2")
    c.number_format = "#,##0.00"
    c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
ws.column_dimensions[L].width = 14
ws["A1"].alignment = Alignment(horizontal="center")
ws.conditional_formatting.add(f"C2:C{last}", CellIsRule(operator="greaterThan", formula=["2000"],
                              fill=PatternFill("solid", fgColor="C6EFCE")))
ws.conditional_formatting.add(f"C2:C{last}", ColorScaleRule(start_type="min", start_color="FFFFFF",
                              end_type="max", end_color="5B9BD5"))
wb.save(OUT)
print("Сохранено:", OUT)
```

### Проверка

```python
# Проверка: xlsx-openpyxl
from openpyxl import load_workbook

ws = load_workbook("сводка_правка.xlsx")["Данные"]
assert ws["D1"].value == "С НДС" and ws["D2"].value == "=C2*1.2"
print("ПРОВЕРКА OK: колонка с формулой", ws["D2"].value)
```

## Анализ приложенной таблицы (pandas)

1. Сначала посмотри структуру — листы, колонки, первые строки:

```python
import pandas as pd
books = pd.read_excel("файл.xlsx", sheet_name=None)      # все листы
for name, df in books.items():
    print(name, df.shape); print(df.columns.tolist()); print(df.head(5).to_string())
```

2. Если шапка не в первой строке — `header=2` или `skiprows=`; объединённые ячейки дают NaN — `df["Колонка"] = df["Колонка"].ffill()`.
3. Сравнивай строки после очистки: `df["Статус"].astype(str).str.strip().str.lower()`.
4. Частые операции: `value_counts()`, `groupby(...).agg(...)`, `pivot_table`, `merge`, `pd.to_datetime(..., dayfirst=True)`, `pd.to_numeric(..., errors="coerce")`.
5. Значения формул из файла, сохранённого Excel, — `load_workbook(path, data_only=True)`; формулы как текст — без `data_only`.
6. Результат анализа сохраняй в новый .xlsx (рецепт 2), исходный файл пользователя не перезаписывай без просьбы.

## Как проверить результат

<!-- FEAT-04.12 -->
- **Посмотри результат глазами.** Отдельной командой (не в цепочке с `&&`): `teleharness-render "имя файла.xlsx"` (или `--pages 1-3`). Это настоящий рендер LibreOffice/браузера: картинки страниц появятся в `_preview/<имя>/page-01.png …`. Открой их `read`/`look_at` (Claude — Read), сверь с задачей: ничего не обрезано, текст не вылезает за блоки, колонки не обрезаны (####), диаграммы на месте, шрифт читается. Нашёл проблему — исправь скрипт, пересобери и посмотри снова. Пользователю `_preview` не называй.
- Итоговый файл — в рабочей папке чата под понятным именем; промежуточные (скрипты, вырезанные картинки) — в подпапке `_work`. Не перезаписывай файл, который создал не ты в этом чате: возьми новое имя. В ответе назови итоговый файл полным именем — под ответом появится его карточка для скачивания.
- Перечитай файл: `openpyxl.load_workbook(...)` (шапка, формулы, `ws.column_dimensions`, `ws.conditional_formatting`, `ws._charts`) и `pd.read_excel(...)` (число строк, итоги).
- Напечатай короткую сводку и назови пользователю файл, лист и что в нём.
