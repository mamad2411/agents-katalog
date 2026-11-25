---
name: download-repos
description: "Git'ten repoları indir — DownloadEssentials, DownloadClaude, DownloadSDK, DownloadAll. Triggers: download, download_, /download, download repos, repo indir, repoları çek, clone repos, git clone all, indir, repoları indir."
argument-hint: "[DownloadEssentials|DownloadClaude|DownloadSDK|DownloadAll]"
user-invocable: true
---

# /download-repos — Repo İndirici

`projects.json` + GitHub MCP ile repoları `~/Projects/` altına clone'la veya pull yap.

## Argüman yoksa

Seçenekleri göster:

```
Hangi set indirilsin?

  DownloadEssentials  — Temel config + hub repoları
  DownloadClaude      — Claude ekosistemi repoları
  DownloadSDK         — SDK ve API repoları
  DownloadAll         — projects.json'daki tüm repolar
```

## Repo Setleri

### DownloadEssentials
Çalışmak için gereken minimum set:
- `SkyWalker2506/claude-config`
- `SkyWalker2506/ClaudeHQ`
- `SkyWalker2506/claude-secrets` → `~/.claude/secrets/` altına indir (private repo)

### DownloadClaude
Claude ekosistemi:
- `SkyWalker2506/claude-config`
- `SkyWalker2506/ClaudeHQ`
- `SkyWalker2506/claude-marketplace`

### DownloadSDK
SDK, API ve entegrasyon repoları:
- `SkyWalker2506/claude-marketplace`
- `SkyWalker2506/ar-research`

### DownloadAll
`projects.json` içindeki tüm `git` alanına sahip repolar.

`projects.json` arama sırası (ilk bulunan kullanılır):
1. `~/Projects/ClaudeHQ/projects.json`
2. `~/Projects/claude-config/projects.json`
3. Mevcut dizin (`$PWD/projects.json`)

Hiçbiri yoksa → DownloadEssentials setini çalıştır ve kullanıcıya bildir.

## Akış

### 1. GitHub login kontrol

```bash
gh auth status
```

- **Login yok** → Kullaniciya soyle:
  > `! gh auth login --web -p https` komutunu çalıştır, sonra tekrar dene.
  Dur, devam etme.

### 2. Kullanıcı adını al

```bash
GH_USER=$(gh api user -q .login)
```

### 3. projects.json bul (DownloadAll için)

```bash
PROJECTS_JSON=""
for candidate in \
  "$HOME/Projects/ClaudeHQ/projects.json" \
  "$HOME/Projects/claude-config/projects.json" \
  "$PWD/projects.json"; do
  [ -f "$candidate" ] && PROJECTS_JSON="$candidate" && break
done
```

Bulunamazsa → DownloadEssentials setini çalıştır, kullanıcıya bildir.

### 4. Her repo için — clone veya pull

```bash
PROJECTS="$HOME/Projects"
REPO="<org>/<repo-name>"
DEST="$PROJECTS/<repo-name>"

if [ -d "$DEST/.git" ]; then
  echo "↻ Pull: $REPO"
  git -C "$DEST" pull --ff-only
else
  echo "⬇ Clone: $REPO"
  gh repo clone "$REPO" "$DEST"
fi
```

Bash tool ile her repo için sırayla çalıştır. Paralel değil — çıktı takibi için sıralı.

### 4. Özet tablo göster

```
| Repo               | İşlem  | Durum |
|--------------------|--------|-------|
| claude-config      | clone  | ✅    |
| ClaudeHQ           | pull   | ✅    |
| claude-marketplace | clone  | ✅    |
```

### 5. DownloadAll sonrası install.sh öner

> `claude-config` reposu indirildi. `./install.sh` çalıştırıp config'i kurmak ister misin?

Evet → `cd ~/Projects/claude-config && ./install.sh`

## Kurallar

- `gh repo clone` kullan — SSH key gerekmez, token yeterli
- Hata olursa atla, listeye `❌ (hata mesajı)` yaz, devam et
- `claude-secrets` reposu **istisnası**: `~/Projects/` değil `~/.claude/secrets/` altına indir
- Secret değerlerini terminale yazma

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
