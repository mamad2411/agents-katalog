---
name: clop-compress
description: Comprimir imagenes, videos, PDFs y audio con Clop (app macOS de lowtechguys) via su CLI. Usar cuando se pida comprimir, optimizar, reducir peso o "hacer mas ligeras" fotos/videos/PDFs, preparar assets para web, o vaciar espacio de una carpeta de medios. Incluye escalas de compresion medidas, encoders de video, recetas por caso de uso y las trampas del CLI.
---

# Clop: compresion de medios

Clop no comprime por si mismo: orquesta binarios CLI (jpegoptim, pngquant, cwebp, ffmpeg, gifski, ghostscript, libvips, exiftool). Su valor es la calibracion de esos encoders, no un algoritmo propio.

## Rutas

```
clop                                                    # CLI, ya en PATH (~/.local/bin/clop)
/Applications/Clop.app/Contents/SharedSupport/ClopCLI   # fuente del CLI, por si hay que reinstalar
~/Library/Application Scripts/com.lowtechguys.Clop/bin/arm64/   # ffmpeg, exiftool, jpegoptim...
```

Si `clop` desaparece tras una actualizacion de la app:
```bash
cp /Applications/Clop.app/Contents/SharedSupport/ClopCLI ~/.local/bin/clop && chmod +x ~/.local/bin/clop
```

## Regla 1: nunca sobre los originales

Clop modifica **in place** por defecto. El flujo seguro siempre es copiar primero y comprimir la copia:

```bash
cp -R origen/ destino/
clop optimise image --compression 50 -n -r destino/
```

Es mas fiable que `--output` porque evita las trampas de plantilla (abajo).

## Escala de compresion

`--compression` va de **5 (mejor calidad) a 100 (archivo mas chico)**. Es al reves de la escala de calidad JPEG de toda la vida: 80 aqui NO es "calidad 80", es compresion muy agresiva.

Medido sobre JPEG de camara de 18MP (Canon, 6.7 MB, calidad original 98):

| `--compression` | Resultado | Ahorro | Uso |
|---|---|---|---|
| `adaptive` | 1.2 MB | 82% | Deja que Clop elija formato y nivel por imagen |
| 20 | 2.4 MB | 65% | Archivo de alta fidelidad |
| 35 | 958 KB | 86% | Impresion / edicion posterior |
| 50 | 655 KB | 90% | **Default recomendado**, sin artefactos visibles |
| 64 | 500 KB | 93% | Web / compartir |
| 80 | 391 KB | 94% | Miniaturas, adjuntos de correo |

Arriba de 64 los artefactos empiezan a verse en cielos y degradados.

## Video

`--encoder` importa mas que `--compression`. Medido sobre 1080p29.97 H.264 de camara a 46 Mbps (20 s, 120 MB):

| `--encoder` | Resultado | Ahorro | Tiempo |
|---|---|---|---|
| `lossless` | 54 MB | 55% | 7 s |
| `software` | 24 MB | 80% | 6 s |
| `hardware` | 17 MB | 86% | 2 s |
| `adaptive` | 17 MB | 86% | 3 s |

`hardware` gano en tamano **y** en velocidad, contra lo que sugiere la ayuda del CLI ("software = archivos mas chicos"). Medir antes de asumir.

`lossless` no es matematicamente sin perdida: significa "sin perdida perceptible". Recomprimir video nunca es bit a bit identico.

## Recetas

```bash
# Web / assets de sitio
clop optimise image --compression 64 -n -r assets/

# Archivo fotografico (calidad alta, ahorro fuerte)
clop optimise image --compression 35 -n -r fotos/

# Dejar que Clop decida formato por imagen (puede sacar WebP/HEIC)
clop optimise image --compression adaptive -n -r mixto/

# Video para compartir
clop optimise video --encoder hardware -n -r videos/

# Video preservando calidad
clop optimise video --encoder lossless -n -r videos/

# PDF (dpi adaptive elige por documento)
clop optimise pdf --dpi adaptive -n -r docs/

# Audio
clop optimise audio --compression 50 -n -r audio/

# Redimensionar ademas de comprimir
clop optimise image --compression 50 --downscale-factor 0.5 -n foto.jpg
clop optimise image --compression 50 --crop 1200x630 -n og-image.jpg

# Tipos mezclados en una carpeta (imagen + video + PDF juntos)
clop optimise -n -r carpeta/
```

Sin subcomando ni `--compression`, Clop aplica su modo adaptativo: ~82% en foto de camara, ~88% en video. Es el atajo bueno cuando no hay un requisito de calidad concreto.

Flags utiles: `-n` (sin barra de progreso), `-r` (recursivo), `-j` (JSON), `-s` (ignora errores), `-g` (muestra la UI flotante), `--async` (fondo).

## EXIF: Clop siempre lo borra

Tanto la app como el CLI eliminan **todo** el EXIF: fecha de captura, camara, GPS, lente. En una fototeca esto rompe el orden por fecha en Fotos y Finder.

Restaurar despues de comprimir (cuesta ~21 KB por foto, 3%):

```bash
EXIFTOOL=~/Library/"Application Scripts"/com.lowtechguys.Clop/bin/arm64/exiftool
for f in destino/*.JPG; do
  "$EXIFTOOL" -q -overwrite_original -TagsFromFile "origen/$(basename "$f")" -all:all "$f"
done
```

Verificado: devuelve Model, DateTimeOriginal y GPS sin tocar los pixeles.

## Trampas del CLI

**`-o carpeta/` no escribe dentro de la carpeta.** Si `dest` es un directorio existente, `-o dest` crea un archivo llamado `dest.JPG` al lado. Usar plantilla: `-o "dest/%f"`.

**`%f` ya incluye la extension correcta.** `-o "dest/%f.jpg"` produce `IMG_001.jpg.JPG`. Escribir solo `-o "dest/%f"`.

**MOV se convierte a MP4 y deja el original.** Tras procesar videos quedan los dos archivos; hay que borrar los `.MOV` sobrantes a mano.

**No hay `ffprobe`** en el bundle de Clop, solo `ffmpeg`. Para leer duracion o codec: `ffmpeg -hide_banner -i archivo 2>&1 | grep Duration`. Un script que llame a `ffprobe` falla en silencio y devuelve campos vacios que parecen validos.

**Formatos que Clop se salta** segun la config del usuario: revisar `imageFormatsToSkip` y `videoFormatsToSkip` con `defaults read com.lowtechguys.Clop`.

## Verificar siempre

Comprimir es destructivo. Antes de dar el trabajo por bueno y antes de borrar originales:

```bash
FFMPEG=~/Library/"Application Scripts"/com.lowtechguys.Clop/bin/arm64/ffmpeg
# decodificacion completa: detecta truncamiento y corrupcion
for f in destino/*; do
  err=$("$FFMPEG" -v error -i "$f" -f null - 2>&1 | head -1)
  [ -n "$err" ] && echo "CORRUPTO: $f -> $err"
done
# conteo y resolucion
echo "origen $(/bin/ls origen | wc -l) vs destino $(/bin/ls destino | wc -l)"
```

Para video, comparar la duracion origen/destino: si no coincide, la codificacion se trunco.

## Pipelines

Clop guarda presets reutilizables, compartidos entre app y CLI:

```bash
clop pipeline list
clop pipeline show "to WebP"
clop pipeline run "to WebP" imagenes/*.png
clop pipeline add "web-assets" 'optimise() -> convert(to: webp)' --file-type image
```

Los pasos son argumento **posicional**, no un flag `--steps`. `pipeline run` acepta `-r`, `-j`, `-s` igual que `optimise`.

Sintaxis de pasos: `optimise()`, `downscale(factor:)`, `crop(width:)`, `convert(to:)`, `watermark(image:)`, `move(to:)`, `changeSpeed(factor:)`, `removeAudio`, `filterIf(regex:)`, encadenados con `->`.

## Config de la app

```bash
defaults read com.lowtechguys.Clop            # ver todo
defaults read com.lowtechguys.Clop imageDirs  # carpetas vigiladas
```

`imageDirs`/`videoDirs` son carpetas que Clop vigila para comprimir **automaticamente e in place** todo lo que caiga ahi. Potente pero destructivo: verificar que las rutas existan y que el usuario lo quiera antes de activarlo.

Los backups para "restaurar original" viven en `~/Library/Caches/Clop/backups` y crecen sin limite (llegan a GB). Revisar de vez en cuando.
