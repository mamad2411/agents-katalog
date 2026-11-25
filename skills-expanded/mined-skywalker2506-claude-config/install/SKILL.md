---
name: install
description: "Run claude-config installer. Asks questions via Claude, then runs install.sh with correct flags. Triggers: install, kurulum, setup config."
user-invocable: true
---

# Install — claude-config Kurulum

Claude Code icinden install.sh'i calistir. Interaktif sorulari Claude sorar, sonra script'e arguman olarak gecirir.

## Akis

### 1. Platform ve durum kontrolu

```bash
uname -s
gh auth status 2>&1
ls ~/.claude/secrets/secrets.env 2>/dev/null
```

### 2. Kullaniciya sor

Sirasıyla sor (zaten ayarliysa atlama):

**A. Kurulum kapsamı:**
> Bu kurulum ne icin?
> 1. Global (tum projeler icin genel kurulum — ~/.claude/ + ~/Projects/)
> 2. Tek proje (sadece bu projeye ozel MCP/config)

- "Global" → normal install.sh akisi (adim B-E)
- "Tek proje" → sadece proje tespiti + proje bazli MCP kurulumu (adim D, install.sh calistirilmaz)

**B. Proje kok dizini** (sadece global):
> Proje kok dizinin nedir? (macOS varsayilan: ~/Projects, Windows: ~/Documents/GitHub)

**C. GitHub login** (gh auth status basarisizsa):
> GitHub'a login olmak ister misin? Login icin calistir:
> ```
> ! gh auth login --web -p https
> ```
> Login tamamlaninca "tamam" yaz.

Login istemezse → `--skip-login` flag kullan.

**D. Proje tipleri (stacks):**

Kullaniciya sormadan ONCE bulundugun dizini ve parent dizini otomatik tespit et:

```bash
# Bulundugun dizin (pwd) — SADECE bu dizini kontrol et, alt klasorlere bakma
CUR="$(pwd)"
echo "=== pwd: $CUR ==="

# Unity projesi mi? (Assets/ + ProjectSettings/ AYNI dizinde olmali)
ls -d "$CUR/Assets" "$CUR/ProjectSettings" 2>/dev/null

# Flutter projesi mi? (pubspec.yaml AYNI dizinde olmali)
ls "$CUR/pubspec.yaml" 2>/dev/null

# Web projesi mi? (package.json AYNI dizinde olmali)
ls "$CUR/package.json" 2>/dev/null

# Python projesi mi? (requirements.txt veya pyproject.toml AYNI dizinde olmali)
ls "$CUR/requirements.txt" "$CUR/pyproject.toml" 2>/dev/null
```

```bash
# Parent dizin (proje kok dizini) — ust dizindeki diger projeleri tara
PARENT="$(dirname "$CUR")"
echo "=== parent: $PARENT ==="
ls "$PARENT"/*/pubspec.yaml 2>/dev/null    # Flutter projeleri
ls -d "$PARENT"/*/Assets "$PARENT"/*/ProjectSettings 2>/dev/null  # Unity projeleri
ls "$PARENT"/*/package.json 2>/dev/null    # Web projeleri
ls "$PARENT"/*/requirements.txt "$PARENT"/*/pyproject.toml 2>/dev/null  # Python projeleri
```

Tespit sonucunu kullaniciya **goster ve onayla:**

> Tespit ettigim proje tipleri:
> - Bu dizin ($CUR): **Unity projesi** (Assets/ + ProjectSettings/ bulundu)
> - Parent dizininde ($PARENT): 3 Flutter, 1 Web projesi var
>
> Bu dogru mu? Eklemek/cikarmak istedigin var mi?
> Secenekler: flutter, unity, web, python, general

**ONEMLI:**
- **SADECE `$(pwd)` dizinini kontrol et** — alt klasorlere (subdirectory) girme
- Parent dizinde sadece dogrudan cocuk klasorleri tara (`$PARENT/*/`), toruna (nested) bakma
- Yanlis tespit riski varsa **kullaniciya sor, varsayimla ilerleme**
- Secimleri virgullu listeye cevir: `flutter,unity,web,python`
- Secim yapmadiysa → `--stacks general`

**E. Secrets** (secrets.env yoksa, sadece global):
> Private secrets repon var mi? Varsa URL'yi yaz, yoksa "yok" de.

- URL verdiyse → `--secrets-repo URL`
- "yok" dediyse → `--skip-secrets`

### 3. install.sh calistir (sadece global kapsam)

Topladığın cevaplardan komutu olustur:

```bash
cd ~/Projects/claude-config && bash ./install.sh --auto --root <CEVAP_B> --stacks <CEVAP_D> [--skip-login] [--skip-secrets] [--secrets-repo <URL>]
```

`--auto` her zaman ekle — script'in kendi read -p'leri calismaz, tum parametreler arguman olarak gecer.

### 4. Sonuc

Script ciktisini goster. Hata varsa yardimci ol.
Basarili ise: "Kurulum tamamlandi." de.

## Kurallar

- Script her zaman `--auto` ile calistirilir
- Kullanici bilgisi eksikse **Claude sorar**, script'e sormadan gecirir
- Zaten ayarli olan seyler (login var, secrets var) icin soru sorma
- Secret degerleri terminale yazma
- Proje tipi tespiti **sadece `$(pwd)` ve `$(pwd)/../*/`** — baska yere bakma

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
