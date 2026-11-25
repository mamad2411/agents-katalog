---
name: teleharness-docx
description: Word (.docx) — создать оформленный документ (стили заголовков, абзацы, маркированный и нумерованный список, таблица, картинка или график, колонтитулы с номером страницы, поля и ориентация), изменить или прочитать существующий документ. Используй, когда пользователь просит Word-файл, отчёт, письмо, справку, договор в docx или разобрать приложенный docx.
---

# Word: создание, оформление, чтение

Библиотека песочницы: **python-docx** (`import docx`). Графики для вставки — **matplotlib** в .png.

## Правила песочницы

- Команды выполняются в `cmd.exe` внутри песочницы (Windows AppContainer). Нет PowerShell и bash. `pip install <пакет>` работает — пакет ставится в папку пользователя; документы смотри через `teleharness-render`. PDF из готового docx: `teleharness-render "файл.docx"` кладёт точный PDF в `_preview/<имя>/<имя>.pdf` — скопируй его рядом с результатом под понятным именем.
- Код Python пиши в файл `.py` в рабочей папке пользователя (инструмент `write`) и запускай `python имя.py`. Многострочный `python -c "..."` в cmd ломается.
- Все пути — относительные, внутри рабочей папки. Результат сохраняй туда же и в ответе назови файл.
- Вывод проверяй из Python (печатает UTF-8). `type` в cmd может показать русский текст «кракозябрами» — это кодировка консоли.
- `dir` недоступен: список файлов — `list`/`glob` или `python -c "import os; print(os.listdir())"`.
- Исходный документ пользователя не перезаписывай: сохраняй правку в новый файл.

## Рецепт 1. Оформленный отчёт: заголовки, список, таблица, график, колонтитулы

```python
# Рецепт: docx-report — отчёт со стилями, списками, таблицей, графиком и колонтитулами
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUT = "отчёт.docx"
data = [("Москва", 1350, 1200), ("Казань", 780, 900), ("Самара", 760, 750), ("Пермь", 450, 600)]

# 1) график для вставки
fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
ax.bar([d[0] for d in data], [d[1] for d in data], color="#2F5597", label="Факт")
ax.plot([d[0] for d in data], [d[2] for d in data], "o--", color="#C00000", label="План")
ax.set_ylabel("тыс. ₽"); ax.legend(); ax.grid(axis="y", alpha=.3)
fig.tight_layout(); fig.savefig("график_продаж.png"); plt.close(fig)

doc = Document()

# 2) базовые стили: шрифт текста и заголовков (w:eastAsia нужен, чтобы Word не подменял шрифт)
def set_font(style, name, size=None, bold=None, color=None):
    style.font.name = name
    style.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), name)
    if size: style.font.size = Pt(size)
    if bold is not None: style.font.bold = bold
    if color: style.font.color.rgb = RGBColor.from_string(color)

set_font(doc.styles["Normal"], "Calibri", 11)
doc.styles["Normal"].paragraph_format.space_after = Pt(6)
set_font(doc.styles["Title"], "Calibri Light", 24, color="1F3864")
set_font(doc.styles["Heading 1"], "Calibri Light", 16, True, "1F3864")
set_font(doc.styles["Heading 2"], "Calibri", 13, True, "2F5597")

# 3) поля и ориентация (для альбомной: section.orientation = WD_ORIENT.LANDSCAPE и поменять width/height)
sec = doc.sections[0]
sec.orientation = WD_ORIENT.PORTRAIT
sec.left_margin = sec.right_margin = Cm(2)
sec.top_margin = sec.bottom_margin = Cm(2)

# 4) колонтитулы: верхний — название, нижний — «Страница N из M»
sec.header.paragraphs[0].text = "ООО «Ромашка» · Отчёт о продажах"
sec.header.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

def field(par, instr):
    run = par.add_run()
    for tag, attr in (("w:fldChar", "begin"), ("w:instrText", instr), ("w:fldChar", "end")):
        el = OxmlElement(tag)
        if tag == "w:fldChar": el.set(qn("w:fldCharType"), attr)
        else: el.set(qn("xml:space"), "preserve"); el.text = attr
        run._r.append(el)

fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fp.add_run("Страница "); field(fp, "PAGE"); fp.add_run(" из "); field(fp, "NUMPAGES")

# 5) содержание
doc.add_paragraph("Отчёт о продажах за IV квартал", style="Title")
doc.add_heading("1. Итоги", level=1)
p = doc.add_paragraph("Выручка компании за квартал составила ")
p.add_run("3 340 тыс. ₽").bold = True
p.add_run(", план выполнен на 97 %.")

doc.add_heading("Главное", level=2)
for t in ("Москва перевыполнила план на 12,5 %.", "Казань и Пермь — ниже плана.", "Самара — в плане."):
    doc.add_paragraph(t, style="List Bullet")

doc.add_heading("Шаги на следующий квартал", level=2)
for t in ("Пересмотреть план Перми.", "Запустить акцию в Казани.", "Повторить опыт Москвы."):
    doc.add_paragraph(t, style="List Number")

doc.add_heading("2. Продажи по регионам", level=1)
table = doc.add_table(rows=1, cols=4)
table.style = "Light Grid Accent 1"
table.alignment = WD_TABLE_ALIGNMENT.CENTER
for cell, text in zip(table.rows[0].cells, ("Регион", "Факт, тыс. ₽", "План, тыс. ₽", "Выполнение")):
    cell.text = text
    cell.paragraphs[0].runs[0].bold = True
for region, fact, plan in data:
    row = table.add_row().cells
    row[0].text = region
    for c, v in zip(row[1:], (f"{fact:,}".replace(",", " "), f"{plan:,}".replace(",", " "), f"{fact / plan:.0%}")):
        c.text = v
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
for row in table.rows:  # ширины колонок
    for c, w in zip(row.cells, (Cm(5), Cm(3.5), Cm(3.5), Cm(3))):
        c.width = w

doc.add_heading("3. Динамика", level=1)
doc.add_picture("график_продаж.png", width=Cm(15))
doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
cap = doc.add_paragraph("Рисунок 1. Продажи по регионам, тыс. ₽")
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.runs[0].italic = True

doc.add_page_break()
doc.add_heading("Приложение", level=1)
doc.add_paragraph("Данные — выгрузка CRM на 31.12.")

doc.save(OUT)
print("Сохранено:", OUT)
```

Полезное:
- Стили таблиц: `"Table Grid"`, `"Light Grid Accent 1"`, `"Light List Accent 1"`, `"Medium Shading 1 Accent 1"`. Объединить ячейки — `table.cell(0, 0).merge(table.cell(0, 1))`.
- Заливка ячейки: `tc = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), "DDEBF7"); tc.append(sh)`.
- Выравнивание по ширине — `WD_ALIGN_PARAGRAPH.JUSTIFY`; отступ первой строки — `p.paragraph_format.first_line_indent = Cm(1.25)`; межстрочный — `line_spacing = 1.5`.
- Разрыв раздела с альбомной страницей: `s = doc.add_section(); s.orientation = WD_ORIENT.LANDSCAPE; s.page_width, s.page_height = s.page_height, s.page_width`.
- Документ по ГОСТ: Times New Roman 14, поля 3/1.5/2/2 см, интервал 1.5, отступ 1.25 см.

### Проверка

```python
# Проверка: docx-report
import docx

d = docx.Document("отчёт.docx")
heads = [p.text for p in d.paragraphs if p.style.name.startswith("Heading")]
print("Заголовки:", heads)
assert len(heads) >= 3
assert len(d.tables) == 1 and len(d.tables[0].rows) == 5
assert len(d.inline_shapes) == 1, "нет картинки"
assert any(p.style.name == "List Bullet" for p in d.paragraphs)
assert any(p.style.name == "List Number" for p in d.paragraphs)
assert "Отчёт" in d.sections[0].header.paragraphs[0].text
assert "PAGE" in d.sections[0].footer._element.xml
print("ПРОВЕРКА OK: заголовков", len(heads), "таблица 5 строк, картинка, списки, колонтитулы")
```

## Рецепт 2. Заполнить шаблон и прочитать документ

```python
# Рецепт: docx-template — заменить {{поля}} в документе с сохранением оформления и прочитать текст
from docx import Document

SRC, OUT = "отчёт.docx", "отчёт_заполненный.docx"
values = {"ООО «Ромашка»": "ООО «Василёк»", "IV квартал": "I квартал"}

doc = Document(SRC)

def replace_in(paragraphs):
    for p in paragraphs:
        for old, new in values.items():
            if old in p.text:
                # замена по run'ам сохраняет форматирование; если поле разбито на несколько run — собираем в первом
                if any(old in r.text for r in p.runs):
                    for r in p.runs:
                        r.text = r.text.replace(old, new)
                else:
                    full = p.text.replace(old, new)
                    for r in p.runs[1:]:
                        r.text = ""
                    p.runs[0].text = full

replace_in(doc.paragraphs)
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:
            replace_in(c.paragraphs)
for s in doc.sections:
    replace_in(s.header.paragraphs)
    replace_in(s.footer.paragraphs)
doc.save(OUT)

# чтение: текст по абзацам и таблицы
d = Document(OUT)
for p in d.paragraphs[:5]:
    print(f"[{p.style.name}] {p.text}")
for t in d.tables:
    print([[c.text for c in r.cells] for r in t.rows][:3])
print("Сохранено:", OUT)
```

### Проверка

```python
# Проверка: docx-template
from docx import Document

d = Document("отчёт_заполненный.docx")
text = "\n".join(p.text for p in d.paragraphs)
assert "I квартал" in text and "IV квартал" not in text
assert "Василёк" in d.sections[0].header.paragraphs[0].text
print("ПРОВЕРКА OK: шаблон заполнен")
```

## Как проверить результат

<!-- FEAT-04.12 -->
- **Посмотри результат глазами.** Отдельной командой (не в цепочке с `&&`): `teleharness-render "имя файла.docx"` (или `--pages 1-3`). Это настоящий рендер LibreOffice/браузера: картинки страниц появятся в `_preview/<имя>/page-01.png …`. Открой их `read`/`look_at` (Claude — Read), сверь с задачей: ничего не обрезано, текст не вылезает за блоки, нет пустых страниц и наложений, таблицы помещаются, шрифт читается. Нашёл проблему — исправь скрипт, пересобери и посмотри снова. Пользователю `_preview` не называй.
- Итоговый файл — в рабочей папке чата под понятным именем; промежуточные (скрипты, вырезанные картинки) — в подпапке `_work`. Не перезаписывай файл, который создал не ты в этом чате: возьми новое имя. В ответе назови итоговый файл полным именем — под ответом появится его карточка для скачивания.
- Перечитай файл `docx.Document(...)`: заголовки (`p.style.name`), число таблиц и строк, `len(d.inline_shapes)` (картинки), текст колонтитулов.
- Напечатай короткую сводку и назови пользователю файл. Номер страницы в колонтитуле — поле, Word покажет его при открытии.
