---
name: commit-all
description: "Tum projelerdeki degisiklikleri tara, her biri icin commit at. Triggers: commit all, commitAll, tum projeleri commitle, toplu commit."
argument-hint: "[--dry-run]"
---

# /commit-all — Tum Projelerde Toplu Commit

`~/Projects` altindaki tum git repolarini tarar, degisiklik olanlari commitler.

## Kullanim

```
/commit-all              # tara + commitle
/commit-all --dry-run    # sadece ne olacagini goster
```

## Akis

### 1. Tara

`~/Projects/*/` altindaki tum `.git` repolarini tara:
```bash
git -C <repo> status --porcelain
```

Her repo icin:
- Degisiklik varsa → listeye ekle
- Temizse → atla

### 2. Kullaniciya goster

```
Degisiklik olan repolar (X/Y):

  CoinHQ          — 3 modified, 1 untracked
  ArtLift         — 5 modified, 2 untracked, 1 deleted
  claude-config   — 1 untracked
  ...

Devam? (enter = evet, n = iptal)
```

`--dry-run` ise burada dur.

### 3. Her repo icin commit

Her degisiklik olan repo icin sirayla:

1. **Filtreleme:**
   - `.DS_Store`, `.dart_tool/`, `*.log` gibi gereksiz dosyalari EKLEME
   - `.env`, `secrets`, credentials iceren dosyalari EKLEME — uyar
   - Repo'nun `.gitignore`'una uy

2. **Stage:**
   - Modified dosyalari ekle: `git add <dosya>`
   - Untracked dosyalari goster, anlamli olanlari ekle
   - Toplu `git add .` KULLANMA — dosya dosya sec

3. **Commit mesaji:**
   - Degisiklikleri analiz et
   - Conventional commit formati
   - Kisa ve anlamli
   - Co-Authored-By ekleme (toplu commit'te gereksiz)

4. **Sonuc:**
   ```
   ✓ CoinHQ       — chore: update dependencies (3 files)
   ✓ ArtLift      — feat: add notification system (5 files)
   ✓ claude-config — chore: add processed report
   ⊘ demo-site    — skipped (only .DS_Store)
   ```

### 4. Ozet

```
/commit-all tamamlandi:
  ✓ 8 repo commitlendi
  ⊘ 3 repo atlandı (sadece gereksiz dosya)
  — 6 repo zaten temizdi

Push icin: /push-all
```

## Kurallar

- `.DS_Store`, `.dart_tool/`, `*.log`, `node_modules/` gibi dosyalari COMMIT'LEME
- Secret iceren dosyalari COMMIT'LEME — kullaniciya uyar
- Her repo icin ayri commit (tek buyuk commit degil)
- `git add .` veya `git add -A` KULLANMA
- Hata olan repo'yu atla, diger repolara devam et

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
