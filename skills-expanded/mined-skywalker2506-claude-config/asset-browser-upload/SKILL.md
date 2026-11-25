---
name: asset-browser-upload
description: "Lokal PNG'leri işleyip asset-browser runtime'a ekle — magenta/siyah kaldır, frame böl, WebP çevir, missing.json güncelle, commit+push. Triggers: asset upload, lokal dosya yükle, generated assets işle, asset-browser upload, png işle, asset ekle"
argument-hint: "[klasör_yolu]"
---

> ## ANIMASYON URETIMI BU SKILL'IN ISI DEGIL
>
> Karakter animasyonu **yalnizca** `/animate` ile uretilir: tek durağan
> gorselden Wan 2.2 I2V ile video, oradan sprite sheet. Baska bir yol yok.
>
> Goruntu modeline (Gemini, Imagen, SDXL...) kare kare sprite cizdirmeyin.
> Denendi ve tutmuyor: her kare bagimsiz uretildigi icin karakter kareler
> arasinda degisiyor, magenta fon temizlenince kenarlar yeniyor ve sonuc
> oyunda oynatilamiyor.
>
> Bu skill yalnizca **zaten var olan** dosyalari isler. Uretmek icin:
>
>     python -m animcreator.cli add-project --name "<oyun>"
>     python -m animcreator.cli add-character --project <oyun> --name "<ad>" --image <png>
>     python -m animcreator.cli queue --character <slug> --anim idle --anim walk.side
>
> Kuyruk GPU makinesinde isler, sonuc inceleme sitesinde belirir.



# /asset-browser-upload — Lokal PNG'leri İşle ve Ekle

Argümansız çağrılırsa proje dizinlerini tarar ve seçenekleri listeler.

## Kullanım

```
/asset-browser-upload                        # klasör seç (otomatik liste)
/asset-browser-upload 07_generated_assets    # belirli klasör
/asset-browser-upload /tam/yol/klasör        # tam yol
```

## Çalıştır

```bash
INPUT_DIR="${1:-}"

# Proje tespiti
if [ -f "asset-browser/config.json" ]; then
  PROJECT_DIR="$(pwd)"
elif [ -f "${HOME}/Projects/MedievalFactory/asset-browser/config.json" ]; then
  PROJECT_DIR="${HOME}/Projects/MedievalFactory"
elif [ -f "${HOME}/Projects/GameFactory/asset-browser/config.json" ]; then
  PROJECT_DIR="${HOME}/Projects/GameFactory"
else
  echo "ERROR: asset-browser/config.json bulunamadı."
  exit 1
fi

CONFIG="${PROJECT_DIR}/asset-browser/config.json"

# Runtime dizini
RUNTIME_DIR=$(python3 -c "
import json
c=json.load(open('${CONFIG}'))
src=next((s for s in c.get('sources',[]) if 'game' in s.get('category','').lower() or 'in' in s.get('category','').lower()), c.get('sources',[{}])[0])
print(src.get('dir','game/public/assets'))
" 2>/dev/null)
RUNTIME="${PROJECT_DIR}/${RUNTIME_DIR}"

# Vercel alias
TITLE=$(python3 -c "import json; c=json.load(open('${CONFIG}')); print(c['title'].lower())" 2>/dev/null)
SLUG=$(echo "$TITLE" | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
ALIAS="https://asset-browser-${SLUG}.vercel.app"

# Klasör tespiti
if [ -z "$INPUT_DIR" ]; then
  echo "Hangi klasörü işlemek istiyorsun?"
  echo ""
  IDX=1
  DIRS=()
  for D in \
    "${PROJECT_DIR}/07_generated_assets" \
    "${PROJECT_DIR}/01_assets/transparent_png" \
    "${HOME}/Downloads" \
    "${HOME}/Desktop"
  do
    if [ -d "$D" ]; then
      PNG_COUNT=$(find "$D" -maxdepth 1 -iname "*.png" 2>/dev/null | wc -l | tr -d ' ')
      [ "$PNG_COUNT" -gt 0 ] && echo "  $IDX) $D  ($PNG_COUNT PNG)" && DIRS+=("$D") && IDX=$((IDX+1))
    fi
  done
  echo ""
  echo "Kullanım: /asset-browser-upload <klasör_yolu>"
  echo "Örnek:    /asset-browser-upload ${PROJECT_DIR}/07_generated_assets"
  exit 0
fi

# Tam yol veya proje-relative
if [ "${INPUT_DIR:0:1}" != "/" ]; then
  UPLOAD_DIR="${PROJECT_DIR}/${INPUT_DIR}"
else
  UPLOAD_DIR="$INPUT_DIR"
fi

[ ! -d "$UPLOAD_DIR" ] && { echo "ERROR: klasör bulunamadı: $UPLOAD_DIR"; exit 1; }

PNG_LIST=()
while IFS= read -r f; do PNG_LIST+=("$f"); done < <(find "$UPLOAD_DIR" -maxdepth 1 -iname "*.png" 2>/dev/null | sort)
[ ${#PNG_LIST[@]} -eq 0 ] && { echo "PNG bulunamadı: $UPLOAD_DIR"; exit 0; }

echo "=== asset-browser-upload ==="
echo "Kaynak : $UPLOAD_DIR  (${#PNG_LIST[@]} PNG)"
echo "Hedef  : $RUNTIME"
echo ""

TMPDIR="/tmp/ab_upload_$$"
mkdir -p "$TMPDIR"
APPROVED=()
SKIPPED=()

for PNG in "${PNG_LIST[@]}"; do
  [ -f "$PNG" ] || continue
  BASENAME=$(basename "$PNG")
  NAME="${BASENAME%.*}"
  TMPFRAMES="$TMPDIR/frames_${NAME}"
  mkdir -p "$TMPFRAMES"

  # Frame sayısını isimden çıkar (_Nf)
  FRAMES=$(echo "$NAME" | grep -oE '_([0-9]+)f$' | grep -oE '[0-9]+' || true)

  if [ -n "$FRAMES" ]; then
    # ANIMASYON PIPELINE KALDIRILDI — sprite animasyonu /animate ile
    # uretilir. Asagisi yalnizca eski dosyalari kurtarmak icin durur;
    # YENI animasyon bu yoldan gecmemeli.
    # 1. Magenta dene
    magick "$PNG" -fuzz 35% -transparent magenta \
      -crop ${FRAMES}x1@ +repage \
      "$TMPFRAMES/f_%02d.png" 2>/dev/null

    FCOUNT=$(ls "$TMPFRAMES"/f_*.png 2>/dev/null | wc -l | tr -d ' ')

    # 2. Siyah bg fallback (smoke vb.)
    if [ "$FCOUNT" -eq 0 ] || [ "$FCOUNT" -lt "$FRAMES" ]; then
      rm -f "$TMPFRAMES"/f_*.png
      magick "$PNG" -fuzz 20% -transparent black \
        -crop ${FRAMES}x1@ +repage \
        "$TMPFRAMES/f_%02d.png" 2>/dev/null
      FCOUNT=$(ls "$TMPFRAMES"/f_*.png 2>/dev/null | wc -l | tr -d ' ')
    fi

    if [ "$FCOUNT" -eq 0 ]; then
      echo "SKIP $NAME — frame split başarısız"
      SKIPPED+=("$NAME")
      continue
    fi

    # Trim + center + extent 256x256
    for F in "$TMPFRAMES"/f_*.png; do
      magick "$F" -trim +repage \
        -background none -gravity center -extent 256x256 "$F" 2>/dev/null
    done

    # Yatay strip birleştir
    FLIST=()
    while IFS= read -r F; do FLIST+=("$F"); done < <(ls "$TMPFRAMES"/f_*.png | sort)
    magick "${FLIST[@]}" +append "$TMPDIR/${NAME}.png"
    DIMS=$(magick identify -format '%wx%h' "$TMPDIR/${NAME}.png" 2>/dev/null)
    echo "  anim: $NAME  $DIMS  (${FCOUNT}f)"
  else
    # Statik resim — max 512px
    magick "$PNG" -resize '512x512>' "$TMPDIR/${NAME}.png"
    DIMS=$(magick identify -format '%wx%h' "$TMPDIR/${NAME}.png" 2>/dev/null)
    echo "  resim: $NAME  $DIMS"
  fi

  # WebP
  cwebp -q 90 -alpha_q 100 "$TMPDIR/${NAME}.png" -o "$TMPDIR/${NAME}.webp" -quiet 2>/dev/null
  if [ ! -f "$TMPDIR/${NAME}.webp" ]; then
    echo "SKIP $NAME — webp dönüşüm başarısız"
    SKIPPED+=("$NAME")
    continue
  fi

  cp "$TMPDIR/${NAME}.webp" "$RUNTIME/${NAME}.webp"
  APPROVED+=("$NAME")
done

echo ""
echo "İşlendi: ${#APPROVED[@]}  Atlandı: ${#SKIPPED[@]}"

if [ ${#APPROVED[@]} -eq 0 ]; then
  rm -rf "$TMPDIR"
  exit 0
fi

# missing.json güncelle (todo olanları approved yap)
echo "missing.json güncelleniyor..."
for NAME in "${APPROVED[@]}"; do
  curl -s -X POST "$ALIAS/api/missing-patch" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$NAME\",\"patch\":{\"status\":\"approved\"}}" > /dev/null 2>&1
  sleep 0.2
done

# Git commit + push
echo "Commit + push..."
(cd "$PROJECT_DIR" && \
  git add "$RUNTIME_DIR"/ && \
  git diff --cached --quiet || \
  git commit -m "feat: approve $(echo ${#APPROVED[@]}) assets from local upload" && \
  git push)

rm -rf "$TMPDIR"

echo ""
echo "Tamamlandı!"
echo "  Eklenenler: ${APPROVED[*]}"
[ ${#SKIPPED[@]} -gt 0 ] && echo "  Atlananlar: ${SKIPPED[*]}"
echo "  Live: $ALIAS"
```
