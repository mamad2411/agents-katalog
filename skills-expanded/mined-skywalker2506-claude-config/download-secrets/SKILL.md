---
name: download-secrets
description: "Download secrets from private GitHub repo. Login if needed, then clone/pull secrets. Triggers: download secrets, secrets indir, secrets cek, secret login."
user-invocable: true
---

# Download Secrets

Private secrets reposunu indir veya guncelle. Login yoksa once login yap.

## Akis

### 1. GitHub login kontrolu

```bash
gh auth status
```

- **Login var** → Adim 2'ye gec
- **Login yok** → Kullaniciya soyle:

> GitHub'a giris yapmak icin calistir:
> ```
> ! gh auth login --web -p https
> ```

Login tamamlaninca devam et.

### 2. Secrets repo kontrol

```bash
SECRETS_DIR="$HOME/.claude/secrets"
```

#### A) Repo zaten var → pull
```bash
cd ~/.claude/secrets && git pull
```

#### B) Repo yok → clone
Kullanicinin GitHub kullanici adini al:
```bash
GH_USER=$(gh api user -q .login)
```

Clone dene:
```bash
git clone "https://github.com/$GH_USER/claude-secrets.git" ~/.claude/secrets
```

Basarisizsa kullaniciya sor:
> Private secrets repo URL'niz nedir? (orn: https://github.com/USER/claude-secrets.git)

### 3. Dogrulama

```bash
ls -la ~/.claude/secrets/secrets.env
```

Dosya varsa:
> Secrets indirildi. Eksik key var mi kontrol ediliyor...

Zorunlu key kontrol:
```bash
grep "^GITHUB_TOKEN=" ~/.claude/secrets/secrets.env
```

### 4. install.sh calistir (opsiyonel)

> Secrets guncellendi. `./install.sh` calistirip config'e uygulamak ister misin?

Evet → `cd ~/Projects/claude-config && ./install.sh` calistir
Hayir → "Tamam, sonraki install.sh'da otomatik uygulanacak" de

## Onemli

- `gh auth login` interaktif — kullanici `!` ile calistirmali
- Secret degerlerini terminale yazma

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
