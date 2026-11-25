---
name: sky-mobile-app
description: >-
  Web projesinden mobil uygulamaya: PWA mı, Capacitor ile sarmalama mı, Expo (React Native)
  mı kararı; Expo Router, paylaşılan TypeScript/Zod/API katmanı ve monorepo, native hissi
  (jestler, haptik, safe area, bottom sheet), push bildirim, derin bağlantılar (universal links),
  EAS Build/Update ile yayın ve OTA güncelleme, App Store / Google Play reddi tuzakları.
  "Mobil uygulama da olsun", "App Store'a koy", "React Native" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Mobil Uygulama

## Karar

| Durum | Yol |
|---|---|
| İçerik/form ağırlıklı, mağaza şart değil | **PWA** (bkz. `sky-pwa`) |
| Mevcut web uygulaması mağazada olmalı, az native API | **Capacitor** |
| Native his, akıcı jestler, uzun vadeli mobil ürün | **Expo (React Native)** + Expo Router |

Capacitor ile sarılmış sıradan bir site "minimum işlevsellik" gerekçesiyle reddedilebilir: native değer ekle
(push, çevrimdışı, kamera, widget).

## Monorepo yapısı

```
apps/web       # Next.js
apps/mobile    # Expo (expo-router)
packages/api   # Zod şemaları, API istemcisi, tipler
packages/tokens# renk/boşluk token'ları (web CSS + RN StyleSheet)
packages/i18n  # tr.json, en.json ortak
```
- İş mantığı ve doğrulama paylaşılır; **UI paylaşılmaz** (gerekiyorsa NativeWind / Tamagui).
- Mobil auth: çerez yerine `expo-secure-store`'da token.

## Native hissi

- Expo Router native stack geçişleri, iOS'ta kenardan kaydırıp geri.
- **FlashList** (60fps uzun liste), çekip yenile.
- `react-native-gesture-handler` + `reanimated`: kaydırarak sil, `@gorhom/bottom-sheet`.
- **Haptik** (`expo-haptics`): başarıda `notificationAsync(Success)`, seçimde `selectionAsync()`.
- Safe area, klavye kaçınma (`react-native-keyboard-controller`).
- Sistem dark mode'u, dinamik yazı boyutu.
- Splash ve ikon: tek kaynak 1024 ikon; Android adaptive icon.

## Push bildirim

- `expo-notifications`: bağlamlı izin isteme, Expo push token sunucuda.
- Bildirime dokununca derin bağlantı ile doğru ekran.

## Derin bağlantılar

Universal Links (`apple-app-site-association`) + Android App Links (`assetlinks.json`) web alanında →
`site.com/randevu/123` uygulama yüklüyse uygulamada, değilse web'de açılır. Expo Router URL'lerini web
route'larıyla aynı tut.

## Yayın

- **EAS Build** (bulutta derleme), **EAS Submit** (mağazaya gönderim).
- **EAS Update**: JS değişikliklerini mağaza onayı beklemeden gönder; kanallar, kademeli açılış, geri alma.

## Mağaza kontrol listesi

- [ ] Gizlilik politikası; App Store gizlilik etiketi ve Play "Data safety" doğru
- [ ] Hesap oluşturma varsa **uygulama içinden hesap silme**
- [ ] Başka sosyal giriş varsa **Sign in with Apple** da
- [ ] Dijital içerik/abonelik → mağaza içi satın alma kuralları (RevenueCat); fiziksel hizmet (randevu, kargo) → normal ödeme
- [ ] İzin metinleri Türkçe ve nedenini açıklıyor
- [ ] İnceleme için demo hesabı
- [ ] Türkçe mağaza açıklaması ve ekran görüntüleri
- [ ] Çökme raporlama (Sentry React Native)
