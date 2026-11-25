---
name: pull-all
description: "Tum projelerdeki remote degisiklikleri cek. Triggers: pull all, pullAll, tum projeleri pulla, toplu pull."
---

# /pull-all — Tum Projelerde Toplu Pull

`~/Projects` altindaki tum git repolarini tarar, remote'un onunde olanlari pull eder.

## Kullanim

```
/pull-all              # normal pull (fast-forward)
/pull-all --rebase     # rebase modunda pull
/pull-all --dry-run    # sadece ne olacagini goster
```

## Akis

### 1. Tara

Her repo icin once `git fetch`, sonra:
```bash
git -C <repo> rev-list --count HEAD..@{u}  # kac commit behind
git -C <repo> status --porcelain            # uncommitted var mi
```

### 2. Kullaniciya goster

```
Pull edilecek repolar (X):

  CoinHQ          — 2 commits behind
  RefinUp         — 1 commit behind
  claude-config   — 3 commits behind

⚠ Uncommitted degisiklik + behind olan repolar (Y):
  ArtLift         — 5 modified, 2 behind (stash + pull + pop)
  demo-site       — 1 modified, 1 behind

Devam? (enter = evet, n = iptal)
```

`--dry-run` ise burada dur.

### 3. Her repo icin pull

Temiz repolar:
```bash
git -C <repo> pull [--rebase]
```

Uncommitted degisiklik varsa: **otomatik stash + pull + stash pop**:
```bash
git -C <repo> stash push -u -m "pull-all auto-stash"
git -C <repo> pull [--rebase]
git -C <repo> stash pop
```

Stash pop conflict olursa → uyar, repoyu atla, devam et.

Paralel calisabilir (max 5 concurrent).

### 4. Sonuc

```
/pull-all tamamlandi:
  ✓ CoinHQ        — 2 commits pulled
  ✓ RefinUp       — 1 commit pulled
  ✓ claude-config — 3 commits pulled
  ⚠ ArtLift       — stashed, pulled, popped (check git status)
  ✗ demo-site     — stash pop conflict, manual resolve gerekli
```

## Kurallar

- `--force` KULLANMA
- `pull --no-rebase` varsayilan (merge commit olusabilir)
- `--rebase` flag'i ile rebase modu
- Remote'u olmayan repo'lari atla
- Uncommitted varsa otomatik stash, pull sonrasi pop dene
- Conflict olursa dur, kullaniciya bildir, diger repolara devam et

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Aktif calisilan dal varsa dikkatli ol

## Red Flags
- Remote rewrite edilmis (history degismis) → dur, kullaniciya sor
- Birden fazla repo ayni dakikada conflict veriyor → sor

## Error Handling
- Remote yoksa → atla
- Auth hatasi → bir kere retry, yine olmazsa atla
- 3 basarisiz → daha uygun yaklasima yonlendir

## Verification
- [ ] Beklenen commit'ler geldi
- [ ] Uncommitted degisiklik korundu
- [ ] Conflict raporu acik
