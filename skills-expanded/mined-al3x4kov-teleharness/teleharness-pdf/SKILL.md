---
name: teleharness-pdf
description: PDF — создать документ с русским текстом (заголовки, абзацы, таблица, картинка, номера страниц) через reportlab; извлечь текст и таблицы из PDF (pdfplumber, pypdf); объединить, разделить, повернуть страницы. Используй, когда пользователь просит PDF-файл, отчёт или справку в PDF, или прислал PDF и нужно достать из него текст, таблицы, страницы.
---

# PDF: создание, извлечение, слияние

Библиотеки песочницы: **reportlab** (создание), **pdfplumber** (текст и таблицы с координатами), **pypdf** (страницы: слияние, разделение, поворот, метаданные).

## Правила песочницы

- Команды выполняются в `cmd.exe` внутри песочницы (Windows AppContainer). Нет PowerShell и bash. `pip install <пакет>` работает — пакет ставится в папку пользователя; документы смотри через `teleharness-render`. PDF из готового docx/xlsx/pptx/html: `teleharness-render "файл"` кладёт точный PDF в `_preview/<имя>/<имя>.pdf` — скопируй его рядом с результатом; новый PDF с нуля — reportlab.
- Код Python пиши в файл `.py` в рабочей папке пользователя (инструмент `write`) и запускай `python имя.py`. Многострочный `python -c "..."` в cmd ломается.
- Все пути — относительные, внутри рабочей папки. Результат сохраняй туда же и в ответе назови файл.
- Вывод проверяй из Python (печатает UTF-8). `type` в cmd может показать русский «кракозябрами» — это кодировка консоли.
- `dir` недоступен: список файлов — `list`/`glob` или `python -c "import os; print(os.listdir())"`.

## Кириллица: шрифт обязателен

Стандартные шрифты reportlab (Helvetica, Times) **не содержат кириллицы** — вместо русских букв будут чёрные квадраты. Всегда регистрируй TTF-шрифт. В песочнице доступны:
- DejaVu Sans из matplotlib: `<matplotlib.get_data_path()>/fonts/ttf/DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`, `DejaVuSans-Oblique.ttf`, `DejaVuSerif.ttf` (свободная лицензия Bitstream Vera/DejaVu);
- шрифты Windows: `C:\Windows\Fonts\arial.ttf`, `arialbd.ttf`, `times.ttf`, `calibri.ttf` (только чтение).

## Рецепт 1. PDF-отчёт с кириллицей: заголовки, текст, таблица, картинка, номера страниц

```python
# Рецепт: pdf-report — PDF с кириллическим шрифтом, таблицей, графиком и номерами страниц
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = "отчёт.pdf"

# 1) шрифт с кириллицей: DejaVu из matplotlib, запасной — Arial Windows
ttf = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
fonts = {"Body": os.path.join(ttf, "DejaVuSans.ttf"), "Body-Bold": os.path.join(ttf, "DejaVuSans-Bold.ttf")}
if not all(map(os.path.exists, fonts.values())):
    fonts = {"Body": r"C:\Windows\Fonts\arial.ttf", "Body-Bold": r"C:\Windows\Fonts\arialbd.ttf"}
for name, path in fonts.items():
    pdfmetrics.registerFont(TTFont(name, path))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body", boldItalic="Body-Bold")

# 2) стили
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName="Body-Bold", fontSize=18, leading=22, textColor=colors.HexColor("#1F3864"), spaceAfter=10)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Body-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#2F5597"), spaceBefore=10)
P = ParagraphStyle("P", parent=ss["BodyText"], fontName="Body", fontSize=10.5, leading=14.5)
CAP = ParagraphStyle("CAP", parent=P, fontSize=9, textColor=colors.grey, alignment=TA_CENTER)

# 3) график
data = [("Москва", 1350, 1200), ("Казань", 780, 900), ("Самара", 760, 750), ("Пермь", 450, 600)]
fig, ax = plt.subplots(figsize=(7, 3), dpi=150)
ax.bar([d[0] for d in data], [d[1] for d in data], color="#2F5597")
ax.set_ylabel("тыс. ₽"); ax.grid(axis="y", alpha=.3)
fig.tight_layout(); fig.savefig("pdf_график.png"); plt.close(fig)

# 4) содержание (Paragraph понимает разметку <b>, <i>, <br/>, <font color=...>; & < > экранируй)
story = [
    Paragraph("Отчёт о продажах за IV квартал", H1),
    Paragraph("Выручка составила <b>3 340 тыс. ₽</b>, план выполнен на 97 %. "
              "Ниже — данные по регионам и динамика.", P),
    Paragraph("Продажи по регионам", H2),
]
rows = [["Регион", "Факт, тыс. ₽", "План, тыс. ₽", "Выполнение"]]
rows += [[r, f"{f:,}".replace(",", " "), f"{p:,}".replace(",", " "), f"{f / p:.0%}"] for r, f, p in data]
t = Table(rows, colWidths=[5 * cm, 3.5 * cm, 3.5 * cm, 3 * cm], repeatRows=1)
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "Body"),
    ("FONTNAME", (0, 0), (-1, 0), "Body-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3864")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F2F2")]),
    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFBFBF")),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story += [t, Spacer(1, 12), Paragraph("Динамика", H2),
          Image("pdf_график.png", width=16 * cm, height=16 * cm * 3 / 7),
          Paragraph("Рисунок 1. Продажи по регионам", CAP),
          PageBreak(), Paragraph("Приложение", H1), Paragraph("Данные — выгрузка CRM на 31.12.", P)]

# 5) колонтитул: номер страницы и название на каждой странице
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Body", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "ООО «Ромашка» · Отчёт о продажах")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Страница {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                        title="Отчёт о продажах", author="Отдел продаж")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("Сохранено:", OUT)
```

Полезное:
- Альбомная страница: `from reportlab.lib.pagesizes import landscape`; `pagesize=landscape(A4)`.
- Длинный текст в ячейке таблицы переносится, только если это `Paragraph(текст, P)`, а не строка.
- Таблица из pandas: `rows = [df.columns.tolist()] + df.astype(str).values.tolist()`.
- Простой текст без вёрстки — `canvas.Canvas(OUT, pagesize=A4)`, `c.setFont("Body", 12)`, `c.drawString(x, y, "...")`, `c.showPage()`, `c.save()`.

### Проверка

```python
# Проверка: pdf-report
import pdfplumber

with pdfplumber.open("отчёт.pdf") as pdf:
    print("Страниц:", len(pdf.pages))
    text = pdf.pages[0].extract_text()
    print(text[:200])
    assert "Отчёт о продажах" in text and "Москва" in text, "кириллица не извлекается — шрифт не тот"
    fonts = {c["fontname"] for c in pdf.pages[0].chars}
    assert all("Helvetica" not in f for f in fonts), fonts
    assert len(pdf.pages) == 2
print("ПРОВЕРКА OK: кириллица извлекается, страниц 2, шрифты", sorted(fonts))
```

## Рецепт 2. Извлечь текст и таблицы из PDF

```python
# Рецепт: pdf-extract — текст по страницам и таблицы в Excel/CSV
import pdfplumber
import pandas as pd

SRC = "отчёт.pdf"   # файл пользователя
with pdfplumber.open(SRC) as pdf:
    print("Страниц:", len(pdf.pages), "метаданные:", pdf.metadata.get("Title"))
    all_text, tables = [], []
    for i, page in enumerate(pdf.pages, 1):
        t = page.extract_text() or ""
        all_text.append(f"=== Страница {i} ===\n{t}")
        for tb in page.extract_tables():
            if tb and len(tb) > 1:
                tables.append(pd.DataFrame(tb[1:], columns=tb[0]))
with open("текст_из_pdf.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(all_text))
print("Таблиц:", len(tables))
if tables:
    with pd.ExcelWriter("таблицы_из_pdf.xlsx") as xw:
        for k, df in enumerate(tables, 1):
            df.to_excel(xw, sheet_name=f"Таблица{k}", index=False)
    print(tables[0].to_string())
```

Если `extract_text()` пустой — это скан (картинка). OCR в песочнице нет: скажи пользователю, что нужен текстовый PDF или распознавание вне портала. Таблицы без линий: `page.extract_tables({"vertical_strategy": "text", "horizontal_strategy": "text"})`. Быстро весь текст без вёрстки — `pypdf.PdfReader(SRC).pages[i].extract_text()`.

### Проверка

```python
# Проверка: pdf-extract
import pandas as pd

text = open("текст_из_pdf.txt", encoding="utf-8").read()
df = pd.read_excel("таблицы_из_pdf.xlsx")
print(df.columns.tolist())
assert "Отчёт о продажах" in text and "Регион" in df.columns and len(df) == 4
print("ПРОВЕРКА OK: текст и таблица извлечены, строк", len(df))
```

## Рецепт 3. Объединить, разделить, повернуть страницы

```python
# Рецепт: pdf-pages — слияние, разделение, извлечение и поворот страниц
from pypdf import PdfReader, PdfWriter

# объединить несколько файлов
w = PdfWriter()
for src in ["отчёт.pdf", "отчёт.pdf"]:          # список файлов пользователя
    w.append(src)
w.add_metadata({"/Title": "Сборник отчётов"})
with open("объединённый.pdf", "wb") as f:
    w.write(f)

# разделить: каждая страница — отдельный файл
r = PdfReader("объединённый.pdf")
for i, page in enumerate(r.pages, 1):
    one = PdfWriter(); one.add_page(page)
    with open(f"страница_{i}.pdf", "wb") as f:
        one.write(f)

# выбрать страницы (1 и 3, нумерация с нуля) и повернуть вторую на 90°
w = PdfWriter()
for idx in (0, 2):
    w.add_page(r.pages[idx])
w.pages[1].rotate(90)
with open("выборка.pdf", "wb") as f:
    w.write(f)
print("страниц в объединённом:", len(r.pages))
```

Защищённый паролем файл: `r = PdfReader(src); r.decrypt("пароль")`. Сжать: `for p in w.pages: p.compress_content_streams()`.

### Проверка

```python
# Проверка: pdf-pages
from pypdf import PdfReader

assert len(PdfReader("объединённый.pdf").pages) == 4
assert len(PdfReader("страница_3.pdf").pages) == 1
sel = PdfReader("выборка.pdf")
assert len(sel.pages) == 2 and sel.pages[1].rotation == 90
print("ПРОВЕРКА OK: объединение 4 стр., разделение, выборка с поворотом")
```

## Как проверить результат

<!-- FEAT-04.12 -->
- **Посмотри результат глазами.** Отдельной командой (не в цепочке с `&&`): `teleharness-render "файл.pdf"` (или `--pages 1-3`). Это настоящий рендер LibreOffice/браузера: картинки страниц появятся в `_preview/<имя>/page-01.png …`. Открой их `read`/`look_at` (Claude — Read), сверь с задачей: ничего не обрезано, текст не вылезает за блоки, русский текст не превратился в квадраты, шрифт читается. Нашёл проблему — исправь скрипт, пересобери и посмотри снова. Пользователю `_preview` не называй.
- Итоговый файл — в рабочей папке чата под понятным именем; промежуточные (скрипты, вырезанные картинки) — в подпапке `_work`. Не перезаписывай файл, который создал не ты в этом чате: возьми новое имя. В ответе назови итоговый файл полным именем — под ответом появится его карточка для скачивания.
- Созданный PDF: `pdfplumber.open(...)` → число страниц, `extract_text()` содержит русский текст (если вместо букв пусто или квадраты — не зарегистрирован TTF-шрифт).
- Слияние/разделение: `len(PdfReader(...).pages)`.
- Назови пользователю файл и число страниц.
