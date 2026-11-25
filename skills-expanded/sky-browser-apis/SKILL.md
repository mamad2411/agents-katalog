---
name: sky-browser-apis
description: >-
  Modern tarayıcı API'leri ile "native uygulama" hissi: Web Share (paylaş menüsü), Clipboard,
  Popover API ve <dialog>, View Transitions, Broadcast Channel (sekmeler arası), Page
  Visibility, Badging, Wake Lock, Vibration, File System Access, Web Workers, passkey
  (WebAuthn), Web Speech (sesle yazma) ve EyeDropper; özellik algılama ve fallback'ler.
  "Paylaş butonu", "kopyala", "sekmeler arası senkron", "passkey", "sesle yazma" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Tarayıcı API'leri

Kural: **özellik algıla, fallback ver.** Desteklemeyen tarayıcıda deneyim bozulmasın, sadeleşsin.

## Paylaş (Web Share)

```ts
async function share(data: { title: string; text?: string; url: string }) {
  if (navigator.share && navigator.canShare?.(data)) {
    try { await navigator.share(data); } catch { /* kullanıcı iptal etti */ }
  } else {
    await navigator.clipboard.writeText(data.url);
    toast("Bağlantı kopyalandı");
  }
}
```
Mobilde native paylaş sayfası (WhatsApp, Instagram…). Dosya paylaşımı: `files: [new File(...)]`.
Masaüstü fallback menüsü: WhatsApp (`https://wa.me/?text=`), X, LinkedIn, kopyala.

## Pano

- Metin: `navigator.clipboard.writeText` → butonda ✓ ikonu 1.5 sn ("Kopyalandı").
- Görsel: `navigator.clipboard.write([new ClipboardItem({ "image/png": blob })])`.
- Yapıştırmadan görsel al: `paste` olayında `e.clipboardData.files`.
- Kod blokları, davet bağlantıları, IBAN, kupon kodu → kopyala butonu her zaman.

## Popover ve dialog

```html
<button popovertarget="menu">Menü</button>
<div id="menu" popover>…</div>                 <!-- Esc ve dışarı tıklama ile kapanır -->
<dialog id="confirm"><form method="dialog">…<button value="ok">Sil</button></form></dialog>
```
`dialog.showModal()` odak tuzağı, `::backdrop`, Esc'i yerleşik verir. Anchor positioning ile popover'ı
tetikleyiciye bağla (bkz. `sky-css-modern`).

## View Transitions

```ts
document.startViewTransition(() => updateDOM());   // aynı sayfa
// çok sayfalı: @view-transition { navigation: auto; }
```
Paylaşılan öğe: iki sayfada aynı `view-transition-name` → küçük resim büyüyerek detaya dönüşür.
Reduced-motion'da kapat.

## Sekmeler arası: Broadcast Channel

```ts
const ch = new BroadcastChannel("auth");
ch.postMessage({ type: "logout" });                      // bir sekmede çıkış → hepsinde çıkış
ch.onmessage = (e) => e.data.type === "logout" && location.assign("/login");
```
Sepet sayısı, tema değişimi, "başka sekmede açık" uyarısı için de.

## Görünürlük, rozet, başlık

- `document.visibilityState` → arka planda polling/animasyon/video durdur.
- Sekme başlığında sayı: `document.title = "(3) Mesajlar"`; favicon rozeti (canvas).
- Kurulu PWA'da `navigator.setAppBadge(3)` — ana ekran ikonunda sayı.

## Wake Lock ve titreşim

- Tarif, egzersiz, bilet QR ekranı → `navigator.wakeLock.request("screen")`; sekme dönüşünde yeniden iste.
- `navigator.vibrate(10)` başarıda mikro geri bildirim (Android); kapatılabilir olsun.

## Dosya sistemi

- `showSaveFilePicker` (Chromium): aynı dosyaya tekrar kaydet — editör uygulamalarında harika.
  Fallback: `<a download>` ve `<input type=file>`.
- Büyük dosyayı stream ile oku (`file.stream()`).

## Web Workers

Ağır iş (CSV parse, görsel işleme, arama indeksi) → Worker. `comlink` ile fonksiyon çağırır gibi:
```ts
const api = wrap<typeof import("./parse.worker")>(new Worker(new URL("./parse.worker.ts", import.meta.url), { type: "module" }));
const rows = await api.parseCsv(file);
```

## Passkey (WebAuthn)

Parolasız giriş — kullanıcılar Face ID/parmak iziyle girmeyi sever. SimpleWebAuthn veya auth çözümünün
eklentisi. `autocomplete="username webauthn"` ile e-posta alanında otomatik passkey önerisi.
Kurtarma yolu (e-posta) her zaman olsun (bkz. `sky-auth`).

## Ses ve diğerleri

- **Web Speech** (`SpeechRecognition`, `lang = "tr-TR"`): arama/not alanında 🎤 ile sesle yazma; desteklenmiyorsa gizle.
- `speechSynthesis` ile sesli okuma.
- **EyeDropper** (Chromium): ekrandan renk seçme.
- **Contact Picker** (Android Chrome): davet ederken rehberden seç.
- `navigator.connection.saveData` → veri tasarrufu modunda ağır medyayı yükleme.

## Kontrol listesi

- [ ] Her API için özellik algılama + fallback
- [ ] İzin isteyen API'ler kullanıcı eylemiyle tetikleniyor
- [ ] HTTPS (güvenli bağlam)
- [ ] İptal/hata durumları akışı bozmuyor
