---
name: yolo-log
description: "Son /yolo calistirmasinin ne yaptigini goster. Sadece yapilan isler — atlananlar icin --all. Triggers: yolo-log, yolo log, ne yaptin, yolo rapor."
argument-hint: "[--all]"
---

# /yolo-log — YOLO Rapor

Son `/yolo` calistirmasinin **ne yaptigini** gosterir. Varsayilan: sadece yapilan isler. `--all` ile atlananlar da dahil.

## Akis

### 1. Log dosyalarini oku

```bash
cat .yolo/log.json 2>/dev/null
cat .yolo/skipped.json 2>/dev/null
```

Dosya yoksa:
> Henuz /yolo calistirilmamis veya log dosyasi bulunamadi.

### 2. Cikti formati

#### Varsayilan (arguman yok veya `--done`)

Sadece **yapilan isler**, kronolojik:

```
## /yolo Rapor

| # | Ne yapildi | Dosyalar | Commit |
|---|-----------|----------|--------|
| 1 | Next.js project scaffolded | package.json, app/layout.tsx | abc1234 |
| 2 | Auth middleware added | middleware.ts, lib/auth.ts | def5678 |
| 3 | Dashboard page created | app/dashboard/page.tsx | ghi9012 |

**Toplam:** 3 adim, 3 commit
```

#### `--all` argumani

Yapilan isler + atlananlar:

```
## /yolo Rapor

### Yapilan isler
| # | Ne yapildi | Dosyalar | Commit |
|---|-----------|----------|--------|
| 1 | ... | ... | ... |

### Atlananlar
| Ne | Neden | Workaround |
|----|-------|------------|
| Database setup | No credentials | In-memory SQLite |

**Toplam:** 3 adim, 3 commit, 2 skip
```

### 3. Git log cross-check

Log'daki commit hash'lerini `git log --oneline` ile dogrula. Eksik/yanlis hash varsa `(?)` ile isaretle.

## Kurallar

- Sadece oku ve raporla — dosya duzenleme
- `.yolo/log.json` yoksa net hata mesaji ver
- Turkce cikti

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
