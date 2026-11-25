---
name: teleharness-images
description: Картинки — изменить размер и сжать, конвертировать форматы (JPG, PNG, WebP, ICO, PDF), повернуть по EXIF, обрезать, добавить водяной знак (текст с кириллицей или логотип), собрать коллаж, построить график или диаграмму matplotlib с русскими подписями. Используй, когда пользователь просит обработать фото или картинки, сделать превью, баннер, коллаж, водяной знак или график в png.
---

# Картинки и графики

Библиотеки песочницы: **Pillow** (`from PIL import Image`), **matplotlib** (графики).

## Правила песочницы

- Команды выполняются в `cmd.exe` внутри песочницы (Windows AppContainer). Нет PowerShell и bash. `pip install <пакет>` работает — пакет ставится в папку пользователя; документы смотри через `teleharness-render`.
- Код Python пиши в файл `.py` в рабочей папке пользователя (инструмент `write`) и запускай `python имя.py`. Многострочный `python -c "..."` в cmd ломается.
- Все пути — относительные, внутри рабочей папки. Результат сохраняй в новый файл (исходник не перезаписывай) и в ответе назови файл.
- Вывод проверяй из Python (печатает UTF-8). `type` в cmd может показать русский «кракозябрами» — это кодировка консоли.
- `dir` недоступен: список файлов — `list`/`glob` или `python -c "import os; print(os.listdir())"`.
- Посмотреть картинку самому можно инструментом `look_at` (если он есть) или `read` для .png/.jpg.

## Шрифт с кириллицей

`ImageFont.load_default()` кириллицу не рисует. Бери TTF: `os.path.join(matplotlib.get_data_path(), "fonts", "ttf", "DejaVuSans.ttf")` (есть всегда) или `C:\Windows\Fonts\arial.ttf`.

## Рецепт 1. Размер, сжатие, конвертация

```python
# Рецепт: img-resize — поворот по EXIF, уменьшение с сохранением пропорций, обрезка, конвертация
from PIL import Image, ImageOps

SRC = "фото.jpg"   # файл пользователя
im = ImageOps.exif_transpose(Image.open(SRC))   # фото с телефона «лёжа» — повернуть по EXIF
print("Исходник:", im.format, im.size, im.mode)

# уменьшить по длинной стороне до 1200 px (thumbnail не увеличивает и сохраняет пропорции)
small = im.copy()
small.thumbnail((1200, 1200), Image.LANCZOS)
small.convert("RGB").save("фото_1200.jpg", "JPEG", quality=85, optimize=True, progressive=True)

# точный размер с обрезкой по центру (обложка 1080x1080)
ImageOps.fit(im, (1080, 1080), Image.LANCZOS).convert("RGB").save("фото_квадрат.jpg", quality=88)

# конвертация: WebP, PNG, иконка
im.convert("RGB").save("фото.webp", "WEBP", quality=80)
im.save("фото.png", optimize=True)
im.convert("RGBA").resize((256, 256)).save("иконка.ico", sizes=[(16, 16), (32, 32), (64, 64), (256, 256)])
print("Готово:", small.size)
```

- PNG с прозрачностью → JPEG: прозрачность залей белым: `bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.convert("RGBA").split()[3])`.
- Несколько картинок в один PDF: `ims[0].save("альбом.pdf", save_all=True, append_images=ims[1:])` (все — `convert("RGB")`).
- Пакетная обработка: `import glob; for f in glob.glob("*.jpg"): ...` — результат в подпапку `out` (`os.makedirs("out", exist_ok=True)`).

### Проверка

```python
# Проверка: img-resize
from PIL import Image

for f in ("фото_1200.jpg", "фото_квадрат.jpg", "фото.webp", "фото.png", "иконка.ico"):
    im = Image.open(f); im.verify()
    print(f, Image.open(f).format, Image.open(f).size)
assert max(Image.open("фото_1200.jpg").size) == 1200
assert Image.open("фото_квадрат.jpg").size == (1080, 1080)
print("ПРОВЕРКА OK: размеры и форматы")
```

## Рецепт 2. Водяной знак: текст и логотип

```python
# Рецепт: img-watermark — полупрозрачный текстовый водяной знак (кириллица) по диагонали и логотип в углу
import os
import matplotlib
from PIL import Image, ImageDraw, ImageFont, ImageOps

SRC, OUT = "фото.jpg", "фото_водяной_знак.jpg"
TEXT = "© Ромашка 2026"
font_path = os.path.join(matplotlib.get_data_path(), "fonts", "ttf", "DejaVuSans-Bold.ttf")

base = ImageOps.exif_transpose(Image.open(SRC)).convert("RGBA")
W, H = base.size

# 1) повторяющийся диагональный текст
size = max(24, W // 18)
font = ImageFont.truetype(font_path, size)
tile = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
d = ImageDraw.Draw(tile)
tw, th = d.textbbox((0, 0), TEXT, font=font)[2:]
for y in range(0, tile.height, th * 4):
    for x in range(-(y % (tw * 2)), tile.width, int(tw * 1.6)):
        d.text((x, y), TEXT, font=font, fill=(255, 255, 255, 70))
tile = tile.rotate(30, resample=Image.BICUBIC)
tile = tile.crop((W // 2, H // 2, W // 2 + W, H // 2 + H))
out = Image.alpha_composite(base, tile)

# 2) логотип (здесь — нарисованный; у пользователя — Image.open("logo.png").convert("RGBA"))
logo = Image.new("RGBA", (W // 6, W // 6 // 3), (31, 56, 100, 200))
ImageDraw.Draw(logo).text((10, 5), "РОМАШКА", font=ImageFont.truetype(font_path, logo.height // 2), fill="white")
logo.thumbnail((W // 5, H // 5))
margin = W // 40
out.alpha_composite(logo, (W - logo.width - margin, H - logo.height - margin))

out.convert("RGB").save(OUT, quality=90)
print("Сохранено:", OUT, out.size)
```

Непрозрачность — четвёртое число `fill` (0…255); для логотипа с прозрачностью уменьши альфу: `logo.putalpha(logo.getchannel("A").point(lambda a: a * 0.5))`.

### Проверка

```python
# Проверка: img-watermark
from PIL import Image, ImageChops

a, b = Image.open("фото.jpg").convert("RGB"), Image.open("фото_водяной_знак.jpg")
assert a.size == b.size
diff = ImageChops.difference(a, b.convert("RGB")).getbbox()
assert diff is not None, "картинка не изменилась"
print("ПРОВЕРКА OK: водяной знак нанесён, размер", b.size)
```

## Рецепт 3. Коллаж

```python
# Рецепт: img-collage — сетка из нескольких фото с отступами и подписями
import math, os
import matplotlib
from PIL import Image, ImageDraw, ImageFont, ImageOps

files = ["фото.jpg", "фото2.jpg", "фото3.png", "фото.jpg"]   # файлы пользователя
COLS, CELL, GAP, CAPTION = 2, 600, 16, 40
font = ImageFont.truetype(os.path.join(matplotlib.get_data_path(), "fonts", "ttf", "DejaVuSans.ttf"), 24)
rows = math.ceil(len(files) / COLS)
sheet = Image.new("RGB", (COLS * CELL + (COLS + 1) * GAP, rows * (CELL + CAPTION) + (rows + 1) * GAP), "white")
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = ImageOps.fit(ImageOps.exif_transpose(Image.open(f)).convert("RGB"), (CELL, CELL), Image.LANCZOS)
    x = GAP + (i % COLS) * (CELL + GAP)
    y = GAP + (i // COLS) * (CELL + CAPTION + GAP)
    sheet.paste(im, (x, y))
    d.text((x, y + CELL + 6), f"{i + 1}. {os.path.splitext(f)[0]}", font=font, fill=(60, 60, 60))
sheet.save("коллаж.jpg", quality=88)
print("Сохранено: коллаж.jpg", sheet.size)
```

### Проверка

```python
# Проверка: img-collage
from PIL import Image

im = Image.open("коллаж.jpg")
assert im.size == (2 * 600 + 3 * 16, 2 * (600 + 40) + 3 * 16), im.size
print("ПРОВЕРКА OK: коллаж", im.size)
```

## Рецепт 4. График matplotlib с русскими подписями

```python
# Рецепт: img-chart — столбчатая и круговая диаграммы в одном PNG, подписи значений
import matplotlib
matplotlib.use("Agg")                      # без окна: в песочнице нет экрана
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
regions = ["Москва", "Казань", "Самара", "Пермь", "Уфа"]
fact = [1350, 780, 760, 450, 910]
plan = [1200, 900, 750, 600, 800]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=150, gridspec_kw={"width_ratios": [3, 2]})
x = range(len(regions))
b1 = ax1.bar([i - 0.2 for i in x], plan, 0.4, label="План", color="#B4C7E7")
b2 = ax1.bar([i + 0.2 for i in x], fact, 0.4, label="Факт", color="#1F3864")
ax1.bar_label(b2, fmt="%d", fontsize=9, padding=2)
ax1.set_xticks(list(x), regions)
ax1.set_ylabel("тыс. ₽"); ax1.set_title("План и факт по регионам"); ax1.legend(frameon=False)
ax1.grid(axis="y", alpha=.3)
ax2.pie(fact, labels=regions, autopct="%1.0f%%", startangle=90, counterclock=False,
        colors=["#1F3864", "#2F5597", "#8EA9DB", "#B4C7E7", "#ED7D31"], wedgeprops={"width": 0.45})
ax2.set_title("Доля в выручке")
fig.suptitle("Продажи за IV квартал", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig("график.png", bbox_inches="tight")
plt.close(fig)
print("Сохранено: график.png")
```

Другие виды: `ax.plot` (линия, динамика), `ax.barh` (длинные подписи), `ax.scatter`, `ax.hist`, `df.plot(kind=...)` из pandas. Даты на оси — `fig.autofmt_xdate()`. Для печати — `dpi=300`, для веба — `dpi=100…150`, формат SVG — `savefig("график.svg")`.

### Проверка

```python
# Проверка: img-chart
from PIL import Image

im = Image.open("график.png")
assert im.format == "PNG" and im.width > 1000
print("ПРОВЕРКА OK: график", im.size)
```

## Как проверить результат

<!-- FEAT-04.12 -->
- Картинку открой `read`/`look_at` (Claude — Read) и сверь с задачей. Диаграмму в документе смотри через `teleharness-render` документа.
- Итоговый файл — в рабочей папке чата под понятным именем; промежуточные (скрипты, вырезанные картинки) — в подпапке `_work`. Не перезаписывай файл, который создал не ты в этом чате: возьми новое имя. В ответе назови итоговый файл полным именем — под ответом появится его карточка для скачивания.
- `Image.open(f).verify()` — файл не битый; `Image.open(f).size`, `.format` — размер и формат как просили.
- Для водяного знака и коллажа — посмотри результат (`look_at`/`read`), если инструмент доступен.
- Назови пользователю файлы и их размеры (px и КБ: `os.path.getsize(f) // 1024`).
