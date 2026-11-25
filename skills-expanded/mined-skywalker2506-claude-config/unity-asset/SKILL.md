---
name: unity-asset
description: "Unity Asset Store'dan hesabındaki asset'leri bul ve 'Open in Unity' ile Editor'a gönder. Credentials secrets'tan otomatik okunur. Triggers: unity asset indir, unity asset bul, asset store, my assets."
argument-hint: "<asset-adı> [asset-adı2] ..."
---

# /unity-asset — Unity Asset Store Downloader

Unity hesabına giriş yap, istenen asset'leri My Assets'te bul, "Open in Unity" butonuna bas.

## Kullanım

```
/unity-asset SwishSwoosh
/unity-asset Dustyroom "Stylized Skybox"
/unity-asset SwishSwoosh Dustyroom Artkovski
```

## Ön Koşullar

- Unity Editor açık olmalı (deeplink'i yakalar)
- Credentials: `~/.claude/secrets/secrets.env` → `AUTH_UNITY_CLIENT_ID` + `AUTH_UNITY_CLIENT_SECRET`

## Execution Steps

### 1. Credentials Oku

```bash
source ~/.claude/secrets/secrets.env
echo $AUTH_UNITY_CLIENT_ID   # sadece kontrol, değeri loglama
```

Değerler comment'li (#) olabilir — grep + sed ile temizle:
```bash
UNITY_EMAIL=$(grep "AUTH_UNITY_CLIENT_ID" ~/.claude/secrets/secrets.env | sed 's/^#\s*//' | cut -d'=' -f2 | tr -d ' ')
UNITY_PASS=$(grep "AUTH_UNITY_CLIENT_SECRET" ~/.claude/secrets/secrets.env | sed 's/^#\s*//' | cut -d'=' -f2 | tr -d ' ')
```

**GÜVENLİK:** Email/şifreyi ASLA ekrana/loga yazma. Sadece Playwright fill'e geç.

### 2. Unity'ye Login Kontrol Et

`mcp__playwright__browser_navigate` ile `https://assetstore.unity.com/account/assets` aç.

Screenshot al. Eğer "My Assets" sayfası geliyorsa → zaten login, adım 3'e geç.

Eğer login sayfasına yönlendiriyorsa:
- `https://id.unity.com/en/login` git
- Email field'ı bul: `input[name="email"]` veya `input[type="email"]`
- Password field: `input[name="password"]` veya `input[type="password"]`
- `mcp__playwright__browser_evaluate` ile React-safe fill:
  ```js
  const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  const email = document.querySelector('input[type="email"]');
  nativeSetter.call(email, EMAIL);
  email.dispatchEvent(new Event('input', {bubbles: true}));
  // password için aynı
  ```
- Sign in butonuna tıkla
- Asset Store'a yönlendir

### 3. Her Asset için Arama + Open in Unity

Her asset adı için sırayla:

**3a. My Assets'te Ara**

```js
// React-safe input set
const inputs = document.querySelectorAll('input[placeholder="Search for my assets"]');
const input = inputs[0];
const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
nativeSetter.call(input, 'ASSET_ADI');
input.dispatchEvent(new Event('input', {bubbles: true}));
input.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13, bubbles: true}));
```

**3b. Sonucu Kontrol Et**

Screenshot al. "0 items" ise → asset hesapta yok, kullanıcıya bildir.

**3c. Open in Unity Bas**

```js
const btn = Array.from(document.querySelectorAll('a, button')).find(el => el.textContent.includes('Open in Unity'));
if (btn) btn.click();
```

veya snapshot'tan ref bul → `mcp__playwright__browser_click` ile bas.

**3d. Arama Temizle**

Sonraki asset için search input'u temizle, aynı adımı tekrarla.

### 4. Özet Rapor

Tüm asset'ler bittikten sonra:

```
✅ SwishSwoosh — Open in Unity tetiklendi (Unity Editor'da görünmeli)
✅ Dustyroom Casual SFX — Open in Unity tetiklendi
❌ Artkovski Illustrated Nature — My Assets'te bulunamadı
```

## Sınırlamalar

- Unity Editor **kapalıysa** deeplink çalışmaz — sadece buton basılır ama indirme başlamaz
- Web'den `.unitypackage` dosyası indirilemez — Unity'nin DRM kısıtlaması
- 2FA aktifse login otomatize edilemez — manuel giriş gerekir

## Red Flags

- Credentials secrets'ta yoksa → kullanıcıya sor, asla hardcode etme
- "Open in Unity" butonu yoksa → asset hesapta değil veya sayfa tam yüklenmedi, tekrar dene
- Login sonrası tekrar login sayfasına dönüyorsa → 2FA veya yanlış credentials
