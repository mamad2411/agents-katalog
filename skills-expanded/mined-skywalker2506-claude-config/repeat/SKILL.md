---
name: repeat
description: "Herhangi bir skill/komutu N kez tekrarla. Her iterasyon bitince sonrakini baslat. Triggers: repeat, tekrarla, N kez yap."
argument-hint: "<N> <komut veya skill>"
---

# /repeat — Generic Command Repeater

Verilen komutu/skill'i N kez sirayla calistirir. Her iterasyon bitince sonraki baslar.

## Kullanim

```
/repeat 3 /forge                    # 3 kez forge
/repeat 5 /review                   # 5 kez review dongusu calistir
/repeat 2 /yolo fix all tests       # 2 kez yolo
/repeat 4 /fbf                      # 4 kez feedback fix
/repeat 3 "README guncelle"         # 3 kez serbest prompt
```

## Arguman cozumu

| Input | N | Komut |
|-------|---|-------|
| `/repeat 3 /forge` | 3 | `/forge` |
| `/repeat /forge` | **2** (varsayilan) | `/forge` |
| `/repeat 100 /yolo` | **20** (max cap) | `/yolo` |

- Ilk token sayi ise → N olarak al, geri kalan komut
- Ilk token sayi degilse → N=2, tumu komut
- Max N: 20

## Akis

### 1. Parse & Validate

```
N = ilk sayi argumani (default 2, max 20)
COMMAND = geri kalan argumanlar
```

Komut bossa hata ver:
```
/repeat neyi tekrarlayacagimi belirt. Ornek: /repeat 3 /forge
```

### 2. Iterasyon dongusu

Her iterasyon icin:

```
━━ Repeat [1/N] ━━━━━━━━━━━━━━━━━━━━
```

1. **Komutu calistir:**
   - `/` ile basliyorsa → Skill tool ile calistir
   - Degilse → serbest prompt olarak isle
2. **Bitmesini bekle** (foreground)
3. **Sonucu kaydet** — ozet olarak bir sonraki iterasyona context ver

```
━━ Repeat [1/N] Done ✓ ━━━━━━━━━━━━━
```

### 3. Iterasyonlar arasi context

Her iterasyonun kisa ozeti (max 3 satir) sonraki iterasyona beslenir:
```
[Onceki run ozeti: X dosya degisti, Y commit atildi, Z task tamamlandi]
```

`--no-context` flag'i ile kapatilabilir:
```
/repeat 3 --no-context /fbf
```

### 4. Hata yonetimi

| Durum | Davranis |
|-------|----------|
| Iterasyon basarili | Sonrakine gec |
| Iterasyon hata verdi | Log'a yaz, sonrakine gec |
| `--stop-on-fail` | Ilk hatada dur |

Varsayilan: hata olsa bile devam et.

### 5. Bitis raporu

```
/repeat tamamlandi (N/N):
  [1/3] ✓ — 4 commit, 2 dosya
  [2/3] ✓ — 3 commit, 5 dosya
  [3/3] ✗ — flutter analyze hatasi (devam edildi)
```

## Kurallar

- Her iterasyon sirayla calisir (paralel degil) — onceki bitmeden sonraki baslamaz
- Max 20 iterasyon — daha fazlasi icin kullaniciya uyari ver
- Secret'lari loglamaz
- Kullaniciya soru sormaz (tekrarlanan komut sorarsa, o komutun kurallarina uyar)

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
