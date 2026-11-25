---
name: sky-react-native
description: >-
  React Native (Expo) ile uygulama geliştirme derinlemesine: Expo Router (sekme, stack, modal,
  derin bağlantı), stil ve NativeWind, liste performansı (FlashList), animasyon ve jestler
  (Reanimated, Gesture Handler), formlar ve klavye, durum ve veri (TanStack Query, Zustand,
  MMKV), kimlik doğrulama ve SecureStore, native modüller ve config plugin'leri, development
  build, hata ayıklama, test (Jest, Maestro) ve EAS ile yayın. Expo/React Native projesinde kullan.
disable-model-invocation: true
---

# Sky · React Native (Expo)

Platform kararı ve mağaza kuralları `sky-mobile-app`'te; burada günlük geliştirme.

## Yapı (Expo Router)

```
app/
  _layout.tsx              # kök Stack + provider'lar
  (tabs)/_layout.tsx       # Tabs
  (tabs)/index.tsx         # Ana sayfa
  (tabs)/bookings.tsx
  booking/[id].tsx         # detay (derin bağlantı: myapp://booking/123)
  (auth)/login.tsx
  +not-found.tsx
```
Auth koruması: kök layout'ta oturum durumuna göre `<Redirect href="/login" />` veya `Stack.Protected` (sürüme göre).

## Performans

- Listeler **FlashList** (`estimatedItemSize` sürümüne göre), `keyExtractor`, satır bileşeni `memo`.
- Animasyon **Reanimated** (UI thread'de, 60/120fps), jestler **Gesture Handler**; JS thread'i bloklayan ağır iş yok.
- Görseller `expo-image` (önbellek, blurhash yer tutucu).
- Yeni mimari (Fabric/TurboModules) varsayılan — kütüphane uyumluluğunu kontrol et.

## Stil

`StyleSheet.create` veya **NativeWind** (Tailwind sınıfları); token'lar web ile paylaşılabilir (bkz. `sky-design-system`); `useColorScheme` koyu tema; safe area (`react-native-safe-area-context`).

## Formlar ve klavye

React Hook Form + Zod (web ile aynı şema), `KeyboardAvoidingView` veya `react-native-keyboard-controller`, `returnKeyType="next"` + odak zinciri, `textContentType`/`autoComplete` (SMS kodu otomatik doldurma: `oneTimeCode`).

## Veri ve depolama

TanStack Query (çevrimdışı/yeniden bağlanınca tazeleme `onlineManager` ile), Zustand; hızlı anahtar-değer **MMKV**; token **expo-secure-store**; yerel DB `expo-sqlite` (+ Drizzle).

## Native özellikler

Expo SDK modülleri (kamera, konum, bildirim, haptik, dosya, biyometrik `expo-local-authentication`); eksik native kod → **config plugin** veya Expo Modules API ile kendi modülün; Expo Go yerine **development build** (`npx expo run:ios` / EAS development profili).

## Hata ayıklama ve test

React Native DevTools (Chrome DevTools tabanlı), Expo dev menüsü, Sentry React Native; birim/bileşen: Jest + `@testing-library/react-native`; E2E: **Maestro** (YAML akışlar, kolay) veya Detox.

## Yayın

EAS Build (profiller: development/preview/production), EAS Submit, **EAS Update** (OTA JS güncellemesi, kanallar, geri alma), `app.config.ts` ile ortam bazlı yapılandırma; sürüm/build numarası otomatik artırma (`autoIncrement`).
