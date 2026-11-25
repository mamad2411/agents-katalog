---
name: yolo
description: "Tam otonom gorev calistirici. Soru sormadan gidebildigi yere kadar gider, engelleri atlar, her onemli adimda commit atar. Triggers: yolo, otonom yap, salliyorum, full auto."
argument-hint: "<gorev aciklamasi>"
---

# /yolo — Full Autonomous Mode

> Model yonlendirmesi: global/model-routing.md

Verilen gorevi **sifir soru sorarak**, gidebildigi yere kadar uygular. Engeller atlanir, her milestone'da commit atilir, sonuc raporlanir.

## Temel ilkeler

1. **ASLA soru sorma** — ne kullaniciya ne de onay bekle
2. **Engeli atla, durma** — DB? Mock. Login? Skip. API key? Fake. Ucretli servis? Skip.
3. **Her onemli adimda commit** — kucuk, anlamli commit'ler
4. **Arka planda calis** — `run_in_background: true`
5. **Log tut** — ne yaptigini `.yolo/` altina yaz

---

## Akis

### 0. Git kontrolu

```
KONTROL: git rev-parse --is-inside-work-tree 2>/dev/null
```

| Durum | Aksiyon |
|-------|---------|
| Git var | Devam et |
| Git yok | `git init` + `gh repo create <klasor-adi> --private --source=. --push` ile private repo olustur. gh auth yoksa sadece `git init` + lokal commit |

### 1. Log klasoru olustur

```bash
mkdir -p .yolo
echo '[]' > .yolo/log.json  # her /yolo calistirmada sifirla
```

`.yolo/` klasorunu `.gitignore`'a ekle (yoksa olustur, varsa append).

### 2. Analiz (max 5 tool call)

Projeyi hizlica tara: dil, framework, yapiyi anla. Uzun exploration yapma.

### 3. Uygulama

Her adimda:

1. **Yap** — kodu yaz, dosyayi olustur, config'i ayarla
2. **Log'a yaz** — `.yolo/log.json`'a entry ekle (asagidaki format)
3. **Commit at** — anlamli conventional commit mesaji ile

#### Log formati (.yolo/log.json)

JSON array, her entry:

```json
{
  "step": 1,
  "action": "create",
  "what": "Next.js project scaffolded with App Router",
  "files": ["package.json", "app/layout.tsx", "app/page.tsx"],
  "commit": "abc1234",
  "ts": "2026-04-02T14:30:00Z"
}
```

- `action`: `create` | `modify` | `configure` | `scaffold` | `install` | `skip`
- `what`: ne yapildi (1 cumle, Ingilizce)
- `files`: degisen/olusan dosyalar
- `commit`: commit hash (yoksa `null`)

#### Skip log'u (.yolo/skipped.json)

Atlanan seyler ayri dosyaya:

```json
{
  "what": "Database setup",
  "reason": "No credentials, used mock data instead",
  "workaround": "In-memory SQLite with seed data"
}
```

### 4. Engel atlama stratejileri

| Engel | Strateji |
|-------|----------|
| **Veritabani** | SQLite in-memory veya JSON dosya, seed data ile |
| **Auth/Login** | Sahte auth middleware, hardcoded test user |
| **API key** | `.env.example` olustur, kodda `process.env.X \|\| "demo-key"` fallback |
| **Ucretli servis** | Atla veya free tier alternatif kullan |
| **Docker/Container** | Lokal calistir, Docker skip |
| **CI/CD** | Basit script yaz, platform entegrasyonu atla |
| **Test** | Basit happy-path test yaz, edge case atla |
| **Type error** | `as any` veya minimal type tanimla, ilerle |
| **Eksik dependency** | `npm install` / `pip install` / her neyse, calistir |
| **Permission** | Sudo gerektiriyorsa atla, log'a yaz |

### 5. Commit kurallari

- Her mantiksal adimda 1 commit (scaffold, feature, config, fix...)
- Conventional commit: `feat:`, `fix:`, `chore:`, `scaffold:`
- Commit mesaji Ingilizce, kisa, ne yapildigini anlat
- `git add` spesifik dosyalar (`.` kullanma)
- `.yolo/` klasorunu COMMIT'LEME

### 6. Bitiste

Son adimda:

1. `.yolo/log.json`'a son entry: `"action": "complete"`
2. Kullaniciya **kisa ozet** goster:
   ```
   /yolo tamamlandi.
   - X adim, Y commit
   - Atlamalar: Z (detay icin /yolo-log)
   ```

---

## Agent prompt sablonu

```
Agent(
  prompt="""
  YOLO MODE — Tam otonom gorev.

  GOREV: $ARGUMENTS

  KURALLAR:
  1. ASLA soru sorma. Engeli atla, ilerle.
  2. DB gerekiyorsa: SQLite/JSON mock. Login gerekiyorsa: sahte auth. API key: fallback.
  3. Her onemli adimda git commit at (conventional commit, Ingilizce).
  4. Log tut: .yolo/log.json (JSON array, her adim bir entry).
  5. Atlananlar: .yolo/skipped.json (JSON array).
  6. .yolo/ klasorunu gitignore'a ekle, commit'leme.
  7. Git yoksa: git init + gh repo create <klasor-adi> --private (basarisizsa sadece lokal).
  8. Bitiste: .yolo/log.json'a "complete" entry yaz.

  LOG ENTRY FORMAT:
  {"step": N, "action": "create|modify|configure|scaffold|install|skip", "what": "...", "files": [...], "commit": "hash|null", "ts": "ISO"}

  SKIP ENTRY FORMAT:
  {"what": "...", "reason": "...", "workaround": "..."}

  ENGEL ATLAMA: DB→mock, Auth→fake, API key→fallback, Ucretli→skip, Docker→skip, CI→basit script.

  WATCHDOG: Bu gorev long. Max 50 tool call. Her 5 call self-check.
  """,
  run_in_background=True,
  description="yolo: <gorev ozeti>"
)
```

Gorev **mekanikse** bunun yerine Bash'ten `agy` serittir — Claude'un `Agent`
tool'u Gemini kabul etmez:

```bash
~/Projects/ClaudeHQ/scripts/hq agy --file <prompt-dosyasi> --dir <proje> \
  --slug yolo-<gorev> --json &
```

Karar, mimari ve teshis gerektiren gorevler Opus'ta kalir.

---

## Kurallar

- Secret'lari KOD'a yazma — `.env.example` + fallback pattern kullan
- `.yolo/` klasoru git'e girmez
- Mevcut kodu bozma — yeni dosya olusturmak tercih edilir
- Projenin mevcut `CLAUDE.md` kurallarini yine de uygula (guvenlik, dosya sistemi)
- `rm -rf`, `git push --force`, repo silme gibi tehlikeli isler YASAK — yolo bile olsa

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
