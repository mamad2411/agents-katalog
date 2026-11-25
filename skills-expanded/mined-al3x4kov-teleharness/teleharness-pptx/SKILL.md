---
name: teleharness-pptx
description: "PowerPoint (.pptx) — создать презентацию 16:9 в едином фирменном стиле (цвета, шрифты): титульный слайд, слайды с текстом и списками, с картинкой, с нативной диаграммой, с таблицей, заметки докладчика; прочитать или изменить существующую презентацию. Используй, когда пользователь просит презентацию, слайды, pptx или разобрать приложенный pptx."
---

# PowerPoint: презентации

Библиотека песочницы: **python-pptx** (`import pptx`). Картинки и графики — **Pillow** / **matplotlib** в .png; диаграммы лучше делать нативными (`add_chart`) — их можно править в PowerPoint.

## Правила песочницы

- Команды выполняются в `cmd.exe` внутри песочницы (Windows AppContainer). Нет PowerShell и bash. Office/LibreOffice в песочнице не запускаются, но есть `teleharness-render` (см. «Как проверить результат»). `pip install <пакет>` работает — пакет ставится в папку пользователя.
- Код Python пиши в файл `.py` в рабочей папке пользователя (инструмент `write`) и запускай `python имя.py`. Многострочный `python -c "..."` в cmd ломается.
- Все пути — относительные, внутри рабочей папки. Результат сохраняй туда же и в ответе назови файл.
- Вывод проверяй из Python (печатает UTF-8). `type` в cmd может показать русский «кракозябрами» — это кодировка консоли.
- `dir` недоступен: список файлов — `list`/`glob` или `python -c "import os; print(os.listdir())"`.

## Принципы хорошей презентации

- Один слайд — одна мысль; заголовок — вывод («Москва перевыполнила план»), а не тема («Продажи»).
- Не больше 5–6 пунктов по 1 строке; шрифт текста не меньше 18 pt.
- Единая палитра: 1 основной цвет, 1 акцент, серый для второстепенного. Шрифт один (Calibri/Segoe UI).
- Формат 16:9. Слайды собираем на пустом макете (layout 6) своими блоками: стандартные плейсхолдеры шаблона рассчитаны на 4:3 и «съезжают».
- Число слайдов — ровно столько, сколько просили (титульный считается слайдом, если пользователь не сказал иначе).

## Рецепт 1. Презентация: титульный, текст, картинка, диаграмма, таблица

```python
# Рецепт: pptx-deck — презентация 16:9 в фирменных цветах: титульный, текст, картинка, диаграмма, таблица
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

OUT = "презентация.pptx"
# тема: цвета и шрифт
PRIMARY, ACCENT, DARK, GREY, LIGHT = (RGBColor(0x1F, 0x38, 0x64), RGBColor(0xED, 0x7D, 0x31),
                                      RGBColor(0x26, 0x26, 0x26), RGBColor(0x7F, 0x7F, 0x7F), RGBColor(0xF2, 0xF2, 0xF2))
FONT = "Calibri"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)   # 16:9
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

def text(slide, x, y, w, h, s, size=20, bold=False, color=DARK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = s
    r.font.size, r.font.bold, r.font.name, r.font.color.rgb = Pt(size), bold, FONT, color
    return tb

def rect(slide, x, y, w, h, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = color; sh.line.fill.background()
    return sh

def content_slide(title, n):
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, W, Inches(1.1), PRIMARY)
    t = text(s, Inches(0.6), Inches(0.15), Inches(12), Inches(0.8), title, 30, True, RGBColor(255, 255, 255), anchor=MSO_ANCHOR.MIDDLE)
    t.name = "Title"
    text(s, W - Inches(1.2), H - Inches(0.5), Inches(0.8), Inches(0.3), str(n), 12, color=GREY, align=PP_ALIGN.RIGHT)
    return s

def bullets(slide, x, y, w, h, items, size=22):
    tf = slide.shapes.add_textbox(x, y, w, h).text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = "•  " + it
        r.font.size, r.font.name, r.font.color.rgb = Pt(size), FONT, DARK
        p.space_after = Pt(12)

# 1. титульный
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, PRIMARY)
rect(s, Inches(0.8), Inches(3.55), Inches(1.5), Inches(0.08), ACCENT)
t = text(s, Inches(0.8), Inches(1.6), Inches(11.5), Inches(1.9), "Итоги продаж за IV квартал", 44, True, RGBColor(255, 255, 255), anchor=MSO_ANCHOR.BOTTOM)
t.name = "Title"
text(s, Inches(0.8), Inches(3.8), Inches(11), Inches(0.6), "Отдел продаж · январь 2027", 22, color=RGBColor(0xD9, 0xE1, 0xF2))
s.notes_slide.notes_text_frame.text = "Приветствие, цель встречи — решения на I квартал."

# 2. текст
s = content_slide("План выполнен на 97 %: рост в Москве, провал в Перми", 2)
bullets(s, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5), [
    "Выручка 3,34 млн ₽ (+8 % к III кварталу)",
    "Москва: 112 % плана — новые B2B-клиенты",
    "Пермь: 75 % плана — ушёл ключевой клиент",
    "Средний чек вырос до 18,4 тыс. ₽",
])
box = rect(s, Inches(8.6), Inches(1.8), Inches(4), Inches(2.4), LIGHT)
text(s, Inches(8.8), Inches(2.0), Inches(3.6), Inches(1.0), "97 %", 54, True, ACCENT, PP_ALIGN.CENTER)
text(s, Inches(8.8), Inches(3.2), Inches(3.6), Inches(0.6), "выполнение плана", 18, color=GREY, align=PP_ALIGN.CENTER)

# 3. картинка (график matplotlib или фото пользователя)
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
months = ["Окт", "Ноя", "Дек"]
ax.plot(months, [1.02, 1.08, 1.24], marker="o", lw=3, color="#1F3864")
ax.set_title("Выручка по месяцам, млн ₽"); ax.grid(alpha=.3)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig("слайд_график.png"); plt.close(fig)
s = content_slide("Декабрь — лучший месяц квартала", 3)
s.shapes.add_picture("слайд_график.png", Inches(0.8), Inches(1.5), height=Inches(5.4))
text(s, Inches(10.6), Inches(2.2), Inches(2.4), Inches(3), "Пик продаж — новогодние заказы корпоративных клиентов", 18, color=GREY)

# 4. нативная диаграмма
s = content_slide("Москва и Уфа выше плана, Пермь — ниже", 4)
cd = CategoryChartData()
cd.categories = ["Москва", "Казань", "Самара", "Пермь", "Уфа"]
cd.add_series("План", (1200, 900, 750, 600, 800))
cd.add_series("Факт", (1350, 780, 760, 450, 910))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.6), cd)
ch = gf.chart
ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
ch.font.size, ch.font.name = Pt(14), FONT
for ser, color in zip(ch.series, (RGBColor(0xB4, 0xC7, 0xE7), PRIMARY)):
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = color
ch.plots[0].has_data_labels = True
ch.plots[0].data_labels.font.size = Pt(11)
ch.value_axis.has_major_gridlines = False

# 5. таблица и выводы
s = content_slide("Решения на I квартал", 5)
rows = [("Регион", "Действие", "Срок"), ("Пермь", "Пересмотреть план, новый менеджер", "до 15.01"),
        ("Казань", "Акция для розницы", "февраль"), ("Москва", "Масштабировать B2B-воронку", "март")]
tbl = s.shapes.add_table(len(rows), 3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(3)).table
for c, w in enumerate((Inches(2.5), Inches(7), Inches(2.2))):
    tbl.columns[c].width = w
for r, row in enumerate(rows):
    for c, v in enumerate(row):
        cell = tbl.cell(r, c); cell.text = v
        para = cell.text_frame.paragraphs[0]
        para.runs[0].font.size, para.runs[0].font.name = Pt(18), FONT
        if r == 0:
            cell.fill.solid(); cell.fill.fore_color.rgb = PRIMARY
            para.runs[0].font.bold = True; para.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            cell.fill.solid(); cell.fill.fore_color.rgb = LIGHT if r % 2 else RGBColor(255, 255, 255)

prs.save(OUT)
print("Сохранено:", OUT, "слайдов:", len(prs.slides))
```

Полезное:
- Другие диаграммы: `XL_CHART_TYPE.PIE` (одна серия, `ch.plots[0].data_labels.number_format = '0%'`), `LINE_MARKERS`, `BAR_CLUSTERED`, `DOUGHNUT`.
- Картинку по центру с сохранением пропорций: задай только `height=` или только `width=`.
- Фото пользователя большое? Сначала уменьши его Pillow до ~1920 px (скилл `teleharness-images`), иначе pptx будет весить десятки МБ.
- Заметки докладчика — `slide.notes_slide.notes_text_frame.text = "..."`.
- Если пользователь дал свой шаблон .pptx — `Presentation("шаблон.pptx")` и его макеты `prs.slide_layouts[i]` (имена: `[l.name for l in prs.slide_layouts]`), текст — в `slide.placeholders[idx]`.

### Проверка

```python
# Проверка: pptx-deck
from pptx import Presentation

p = Presentation("презентация.pptx")
print("Слайдов:", len(p.slides), "размер:", p.slide_width.inches, "x", p.slide_height.inches)
for i, s in enumerate(p.slides, 1):
    title = next((sh.text_frame.text for sh in s.shapes if sh.name == "Title"), "")
    kinds = sorted({("chart" if sh.has_chart else "table" if sh.has_table else "picture" if sh.shape_type == 13 else "text") for sh in s.shapes})
    print(i, title, kinds)
assert len(p.slides) == 5
assert sum(sh.has_chart for s in p.slides for sh in s.shapes) == 1
assert any(sh.shape_type == 13 for s in p.slides for sh in s.shapes)
assert round(p.slide_width.inches, 2) == 13.33
print("ПРОВЕРКА OK: 5 слайдов 16:9, диаграмма, картинка")
```

## Рецепт 2. Прочитать презентацию пользователя

```python
# Рецепт: pptx-read — текст, таблицы и заметки всех слайдов
from pptx import Presentation

p = Presentation("презентация.pptx")
for i, s in enumerate(p.slides, 1):
    print(f"--- слайд {i} ({s.slide_layout.name})")
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            print(" ", sh.text_frame.text.replace("\n", " / "))
        if sh.has_table:
            for r in sh.table.rows:
                print("  |", " | ".join(c.text for c in r.cells))
        if sh.has_chart:
            print("  [диаграмма]", [s.name for s in sh.chart.series])
    if s.has_notes_slide and s.notes_slide.notes_text_frame.text:
        print("  заметки:", s.notes_slide.notes_text_frame.text)
```

### Проверка

```python
# Проверка: pptx-read
from pptx import Presentation

texts = [sh.text_frame.text for s in Presentation("презентация.pptx").slides for sh in s.shapes if sh.has_text_frame]
assert any("IV квартал" in t for t in texts)
print("ПРОВЕРКА OK: текст читается, блоков", len(texts))
```

## Как проверить результат

<!-- FEAT-04.12 -->
- **Посмотри результат глазами.** Отдельной командой (не в цепочке с `&&`): `teleharness-render "имя файла.pptx"` (или `--pages 1-3`). Это настоящий рендер LibreOffice/браузера: картинки страниц появятся в `_preview/<имя>/page-01.png …`. Открой их `read`/`look_at` (Claude — Read), сверь с задачей: ничего не обрезано, текст не вылезает за блоки, нет пустых слайдов и наложений, шрифт читается. Нашёл проблему — исправь скрипт, пересобери и посмотри снова. Пользователю `_preview` не называй.
- Итоговый файл — в рабочей папке чата под понятным именем; промежуточные (скрипты, вырезанные картинки) — в подпапке `_work`. Не перезаписывай файл, который создал не ты в этом чате: возьми новое имя. В ответе назови итоговый файл полным именем — под ответом появится его карточка для скачивания.
- Перечитай файл `Presentation(...)`: `len(p.slides)` равно запрошенному числу, на нужных слайдах есть диаграмма (`sh.has_chart`), картинка (`sh.shape_type == 13`), таблица (`sh.has_table`).
- Напечатай план слайдов (номер, заголовок, что на слайде) и назови пользователю файл.
