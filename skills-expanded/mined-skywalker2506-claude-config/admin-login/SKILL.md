---
name: admin-login
description: "GitHub authentication and account management. Login, switch accounts, check auth status. Triggers: login, gh auth, github login, admin login, hesap degistir."
user-invocable: true
---

# Admin Login

## Akis

### 1. Login kontrolu

```bash
gh auth status 2>&1
```

- **Zaten login** → "GitHub: [USER] olarak giris yapilmis." de, dur.
- **Login yok** → Adim 2

### 2. Secret'tan email kontrol

```bash
grep "^GITHUB_EMAIL=" ~/.claude/secrets/secrets.env 2>/dev/null
```

- **Email var** → Goster: "Kayitli email: X"
- **Email yok** → Sor: "GitHub email adresin?" → `GITHUB_EMAIL=cevap` olarak secrets.env'e ekle

### 3. Login

Kullaniciya:
> ```
> ! gh auth login --web -p https
> ```

Sonra:
```bash
gh auth setup-git
gh api user -q '.login'
```

### 4. Coklu hesap (istenirse)

```bash
gh auth switch --user <USER>
git remote set-url origin https://<USER>@github.com/<USER>/repo.git
```

## Kurallar

- Login varsa hicbir sey yapma
- `gh auth login` interaktif — `!` ile kullanici calistirir
- Sadece email kaydet, token/secret terminale yazma

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
