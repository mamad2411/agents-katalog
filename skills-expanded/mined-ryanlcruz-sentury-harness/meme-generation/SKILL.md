---
name: meme-generation
# Como esta skill aparece para o usuario na lista do 'o que sei fazer'.
# Mora aqui, e nao no motor: o que a skill e e como ela se apresenta
# mudam juntos.
vitrine:
  grupo: 'Visuais'
  rotulo: 'meme com texto'
description: "Generate meme images with text overlays using Pillow."
version: 1.0.0
author: Sentury
license: MIT
platforms: [linux, macos, windows]
tags: [creative, memes, images, pillow]
category: creative
---

# Meme Generation Skill

## NO SENTURY: use o helper `generate_meme` (NÃO use import/Pillow direto)

Neste ambiente, gere o meme chamando a função **pré-carregada** `generate_meme(top_text, bottom_text="", filename="meme")` dentro de `executar_python`. Ela cria um card PNG (fundo escuro, texto branco com contorno) e o arquivo é **anexado automaticamente**. NÃO use `import`, `open` nem `Pillow` no código — o sandbox bloqueia.

```python
resultado = generate_meme("o build quebrou de novo", "ninguem surpreso", "meme_build")
```

Só afirme que gerou se `resultado` confirmar sucesso.

Use this skill to programmatically generate classic memes with custom text overlays, using the Pillow library in python.

## Setup

Requires `pillow`. Can be installed/run inside `executar_python`.

```python
import subprocess
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image, ImageDraw, ImageFont
```

## Procedimento

To create a meme (e.g. "This is Fine" or a colored square with text), write a python script to download a base image (or create a solid background), render white text with black borders, and save the image.

```python
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Let's generate a simple visual card with text or download a template
# e.g., create a solid 600x400 status card
img = Image.new("RGB", (600, 400), color="#1e293b")
draw = ImageDraw.Draw(img)

# Draw a warning box
draw.rectangle([50, 50, 550, 350], fill="#0f172a", outline="#ef4444", width=3)

# Add text
# (Uses default font fallback if special font file is not present)
draw.text((300, 150), "BUILD: 3 falhas seguidas", fill="#ef4444", anchor="mm", font_size=28)
draw.text((300, 220), "A meta era zero.", fill="#f8fafc", anchor="mm", font_size=18)
draw.text((300, 260), "Alguém chame quem fez o merge...", fill="#94a3b8", anchor="mm", font_size=16)

img.save("sentury_build_meme.png")
print("Meme / Card gerado com sucesso!")
```
