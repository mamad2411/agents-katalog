---
name: asset-review
description: "Bekleyen asset-browser upload'larini incele — her biri icin onay/red karari ver, onaylananlari post-process edip runtime asset dizinine tasi, commit+push. Triggers: asset review, asset incele, bekleyenleri incele, asset review workflow, waiting review."
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



# /asset-review — Bekleyen Asset'leri Incele

`asset-browser` kurulu bir projenin `waiting-for-review` listesini inceler. Her item icin:
1. Upload edilen ham dosyayi ceker (GitHub'dan)
2. Preview eder
3. Onayla / Reddet (sebep) / Atla karari verir
4. Onaylanirsa: post-process (animasyon ise strip + WebP), runtime dizine tasi, commit+push
5. Reddedilirse: `denyReason` ile status denied olur
6. Status'u `/api/review` ile günceller

## Kullanim

```
/asset-review                    # CWD projesi
/asset-review /path/to/project   # belirli proje
```

## Akis

### 1. Proje tespiti

`<project>/asset-browser/config.json` okunur. Yoksa hata.

### 2. Bekleyen listesi

GitHub'dan taze `missing.json` ceker:
```bash
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/contents/asset-browser/data/missing.json?ref=main" \
  | jq -r '.content' | base64 -d | jq '.items[] | select(.status=="waiting-for-review")'
```

### 3. Her bekleyen icin

1. **Dosya cek** (GitHub blobs API — >1MB destekli):
   ```bash
   node -e '... fetch blob by sha ...' > /tmp/review/<file>
   ```
2. **Preview**: `open /tmp/review/<file>` ve `magick identify`
3. **Karar**: kullaniciya sor (veya otomatik mod varsa kurallara gore karar ver):
   - Onayla → post-process + tasi
   - Reddet → sebep iste, /api/review deny
   - Atla → sonraki item

### 4a. Web-approved items (post-process eksik)

`/api/review approve` artik uploaded dosyayi **ham halde** runtime dir'e kopyaliyor. Ama bu animasyon icin DOGRU degil — post-process gerekli.

Bu durumu tespit et:
```bash
for name in $(curl -s ...missing.json | jq -r '.items[] | select(.status=="approved" and .type=="Animasyon") | .name'); do
  # runtime file dim kontrolu
  magick identify $PROJECT/game/public/assets/$name.webp
  # dim raw grid (1536x1024 / 2048x1024 / similar) ise = ham kopyalanmis, split gerekli
done
```

Ham bulunanlari listele → kullaniciya sor "bunlari post-process edip yenileyeyim mi?" → evetse magick pipeline ile:
1. Magenta transparent
2. Uygun split (6x1 horizontal / 3x2 grid / etc. isme gore `_6f` / `_8f`)
3. Trim + center + extent 256x256 per frame
4. Append horizontal strip
5. WebP q90, overwrite runtime
6. Commit + push

### 4b. Onay + post-process (tip bazli)

**Animasyon (type=="Animasyon")**: KABUL ETME.
- Sprite animasyonu bu yoldan gecmez. Magenta fonlu, kare kare
  cizdirilmis seritler oyunda oynatilamiyor: her kare bagimsiz
  uretildigi icin karakter kareler arasinda degisiyor.
- Yukleyene soyle: `/animate` ile kuyruga versin. Tek durağan
  gorselden video, videodan sheet cikiyor ve kimlik korunuyor.
- Bu maddenin eski hali (fuzz/crop/append ile kare bolme) kaldirildi;
  ajanlar onu gorup "demek ki burada animasyon uretiliyor" saniyordu.

**Resim (type=="Resim")**:
- Raw genelde buyuk PNG
- `magick IN -resize '512x512>'` → sinirla
- `cwebp -q 90 -alpha_q 100` → WebP
- Hedef runtime dizini

### 5. Status transition + commit

1. `/api/review` ile status approved yap:
   ```bash
   curl -X POST https://<alias>/api/review -d '{"name":"X","action":"approve"}'
   ```
2. Runtime dosyasini commit + push:
   ```bash
   cd <project> && git add <runtime_path> && git commit -m "feat: approve <name>" && git push
   ```

### 6. Reddet akisi

```bash
curl -X POST https://<alias>/api/review -d '{"name":"X","action":"deny","reason":"..."}'
```

### 7. Ozet

```
━━ Asset Review Complete ━━━━━━━━━━━━━━━━
  ✓ fire_loop_6f    — approved (6 frames 256x256 -> game/public/assets/fire_loop_6f.webp)
  ✗ cart_wheels_8f  — denied (Reason: proportions drift between frames)
  ⊘ smoke_rise_6f   — skipped (user undecided)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Runtime dizini tespiti

`config.json` sources'ta `"category": "In Game"` olan ilk entry'nin `dir`'i runtime dizini.

Yoksa: `game/public/assets` -> fallback.

## Kurallar

- Proje ayarlarindan (config.json / AGENT.md) style kurallarini oku
- Kalite sinirlari: frame count, transparency, edge style esleme (bkz. `feedback_asset_quality_rigor.md`)
- Dosya boyutu > 1MB icin GitHub blobs API kullan (contents API 1MB sinir)
- WebP 512px max, q90, alpha_q 100
- Ham PNG'yi de `01_assets/transparent_png/` varsa oraya sakla

## Alias

Vercel stable alias `config.json`'daki title'dan turetilir:
`asset-browser-<slug>.vercel.app` (slug = title lowercase + non-alnum -> dash)

## When NOT to Use
- Hic bekleyen yoksa — sessizce bitir
- asset-browser kurulu degilse

## Red Flags
- Upload dosyasi bozuk / cok kucuk / yanlis format
- Proje kurallariyla celisen asset

## Error Handling
- API 4xx/5xx → retry (1 kere) → kullaniciya sor
- Post-process fail → kullaniciya sebep goster, item'i atla
- Git push fail → rebase + retry
