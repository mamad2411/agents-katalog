---
name: push-all
description: "Tum projelerdeki commitlenmis degisiklikleri push et. Triggers: push all, pushAll, tum projeleri pushla, toplu push."
argument-hint: "[--dry-run] [--include-commit]"
---

# /push-all — Tum Projelerde Toplu Push

`~/Projects` altindaki tum git repolarini tarar, remote'un gerisinde olanlari push eder.

## Kullanim

```
/push-all                    # sadece push (onceden commitlenmis)
/push-all --include-commit   # once /commit-all calistir, sonra push
/push-all --dry-run          # sadece ne olacagini goster
```

## Akis

### 1. Tara

Her repo icin:
```bash
git -C <repo> rev-list --count @{u}..HEAD  # kac commit ahead
git -C <repo> status --porcelain            # uncommitted var mi
```

### 2. Kullaniciya goster

```
Push edilecek repolar (X):

  CoinHQ          — 2 commits ahead
  trading-bot     — 3 commits ahead
  flutter_sec_kit — 1 commit ahead
  ...

⚠ Uncommitted degisikligi olan repolar (Y):
  ArtLift         — 5 modified (once /commit-all calistir)
  demo-site       — 8 modified

Devam? (enter = evet, n = iptal)
```

`--dry-run` ise burada dur.

`--include-commit` ise once `/commit-all` calistir, sonra push'a gec.

### 3. Her repo icin push

```bash
git -C <repo> push
```

Paralel calisabilir (max 5 concurrent) — git push hafif islem.

### 4. Sonuc

```
/push-all tamamlandi:
  ✓ CoinHQ        — 2 commits pushed
  ✓ trading-bot   — 3 commits pushed
  ✓ flutter_sec   — 1 commit pushed
  ✗ demo-site     — push failed (no remote)
  
  ⚠ 2 repo'da uncommitted degisiklik var — /commit-all calistir
```

## Kurallar

- `--force` KULLANMA — asla
- Remote'u olmayan repo'lari atla, hata verme
- Protected branch'e push etme (main'de degilse uyar)
- Hata olan repo'yu atla, digerlerine devam et

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
