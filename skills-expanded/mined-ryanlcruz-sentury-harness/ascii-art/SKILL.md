---
name: ascii-art
# Como esta skill aparece para o usuario na lista do 'o que sei fazer'.
# Mora aqui, e nao no motor: o que a skill e e como ela se apresenta
# mudam juntos.
vitrine:
  grupo: 'Visuais'
  rotulo: 'banner ASCII'
description: "ASCII art banners using pyfiglet/cowsay."
version: 1.0.0
author: Sentury
license: MIT
platforms: [linux, macos, windows]
tags: [ascii, art, banners, creative, text-art]
category: creative
---

# ASCII Art Skill

## NO SENTURY: use o helper `ascii_banner` (NÃO use import)

Neste ambiente, gere o banner chamando a função **pré-carregada** `ascii_banner(text, font="standard")` dentro de `executar_python` e atribua a `resultado`. Fontes úteis: `standard`, `slant`, `big`, `banner3`, `block`. NÃO use `import pyfiglet` — o sandbox bloqueia.

```python
resultado = ascii_banner("DEPLOY OK", "slant")
```

Na resposta, mostre o resultado dentro de um bloco de código (```) para preservar o alinhamento.

Use this skill to generate beautiful ASCII art text banners or cowsay quotes. Perfect for adding a visual, classic hacker touch to reports or logs.

## Setup

Requires the `pyfiglet` pip package. Can be installed or run inside `executar_python`.

```python
import subprocess
import sys

# Install pyfiglet dynamically in the sandbox if not present
try:
    import pyfiglet
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet", "-q"])
    import pyfiglet
```

## Procedimento

To create a banner, write a python script to render text using pyfiglet and return it:

```python
import pyfiglet

# Render text banner using the "slant" font (modern look)
banner = pyfiglet.figlet_format("SENTURY", font="slant")
print(banner)
```

### Fonts Available:
- `slant` (Clean & modern - Recommended)
- `doom` (Bold & blocky)
- `big` (Big & readable)
- `small` (Compact)
