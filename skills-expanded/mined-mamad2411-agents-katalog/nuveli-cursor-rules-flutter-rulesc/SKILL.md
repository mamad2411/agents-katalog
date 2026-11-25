---
description: Flutter kod standartları — tüm .dart dosyaları
globs: ["**/*.dart"]
alwaysApply: true
---

# Flutter Kuralları

## Mimari
- Feature-based klasörleme: `lib/features/<feature_name>/`
- Her feature: `screens/`, `widgets/`, `providers/` (veya `bloc/`), `repository/`
- Shared widget'lar: `lib/shared/widgets/`
- Core (theme, routing, config): `lib/core/`

## State Yönetimi
- Riverpod tercih edilir. Bloc da kabul edilir.
- `setState` sadece izole local UI state için (checkbox, animation).
- Global state asla `setState` ile yönetilmez.

## Widget Kuralları
- Büyük widget'ları küçük const widget'lara böl.
- Her widget dosyası tek sorumluluk taşır.
- `AppScaffold`, `PrimaryButton`, `LoadingView`, `ErrorStateView` shared widget'larını kullan.

## Tema
- Renkler her zaman `AppColors`'dan alınır. Hard-coded hex yasak.
- Text style her zaman `AppTextStyles`'dan alınır.
- Dark premium tema zorunlu; açık tema MVP'de yok.

## Routing
- GoRouter kullanılır.
- Route isimler sabit string yerine `AppRoute` enum/const'u ile tanımlanır.

## Kod Kalitesi
- Her public method için dartdoc yorumu.
- `// TODO:` sadece bırakılıyor ise açıklamasıyla.
- `print()` production kodda yasak; `log()` veya logger kullan.
- Loading durumu ve error durumu her async widget'ta ele alınır.

## Yasaklı
- `dart:io` ile direkt HTTP isteği (Dio kullan).
- `BuildContext` async gap'ten sonra kullanımı.
- Widget içinde iş mantığı (service/repository katmanına taşı).
