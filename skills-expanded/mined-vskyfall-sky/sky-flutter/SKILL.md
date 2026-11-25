---
name: sky-flutter
description: >-
  Flutter ve Dart: feature-first proje yapısı, widget performansı (const, rebuild sınırları),
  durum yönetimi (Riverpod, Bloc), go_router, dio ve freezed/json_serializable, drift ve güvenli
  depolama, Material 3 tema, ARB ile yerelleştirme, platform kanalları (pigeon), widget/golden/
  integration testleri ve mağaza yayını. Flutter projesinde kullan.
disable-model-invocation: true
---

# Sky · Flutter

## Yapı

```
lib/
  main.dart
  app/        router.dart, theme.dart, l10n/
  core/       network/, storage/, errors/
  features/bookings/ data/ (repo, dto), domain/ (model), presentation/ (screens, widgets, controllers)
```

## Durum yönetimi

| Seçim | Ne zaman |
|---|---|
| **Riverpod** (varsayılan) | test edilebilir, async durum (`AsyncValue`) yerleşik |
| **Bloc/Cubit** | olay tabanlı, büyük ekip |
| setState / Provider | küçük uygulama |

```dart
@riverpod
Future<List<Booking>> upcomingBookings(Ref ref) => ref.watch(bookingRepoProvider).upcoming();

class BookingsScreen extends ConsumerWidget {
  const BookingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final bookings = ref.watch(upcomingBookingsProvider);
    return bookings.when(
      data: (items) => items.isEmpty ? const EmptyBookings() : BookingList(items: items),
      loading: () => const BookingListSkeleton(),
      error: (e, _) => ErrorView(onRetry: () => ref.invalidate(upcomingBookingsProvider)),
    );
  }
}
```

## Widget performansı

- `const` constructor her yerde.
- Büyük `build`'i yardımcı **metotlara** değil küçük widget **sınıflarına** böl (rebuild sınırı).
- `ListView.builder`; ağır iş `compute()`/isolate; görseller `cached_network_image`.
- DevTools: rebuild sayaçları, jank kareleri.

## Ağ, modeller, depolama

```dart
@freezed
class Booking with _$Booking {
  const factory Booking({required String id, required DateTime startsAt, required BookingStatus status}) = _Booking;
  factory Booking.fromJson(Map<String, dynamic> json) => _$BookingFromJson(json);
}
```
`dio` (interceptor: token, yeniden deneme) + `build_runner`; `go_router` (redirect ile auth koruması, `ShellRoute`);
`shared_preferences`, `flutter_secure_storage` (token), **drift** (tip güvenli SQLite).

## Tema ve yerelleştirme

`ColorScheme.fromSeed(seedColor: brand)`, koyu tema, `ThemeExtension` ile marka token'ları;
`flutter_localizations` + ARB (`app_tr.arb`), `intl` (`NumberFormat.currency(locale: "tr_TR", symbol: "₺")`).

## Platform ve test

- Hazır paketler (pub.dev "Flutter Favorite"), eksikse `pigeon` ile tip güvenli platform kanalı.
- Testler: birim, widget (`ProviderScope(overrides: …)`), **golden**, `integration_test`; `flutter analyze` + `very_good_analysis`.

## Yayın

Flavor'lar (dev/staging/prod), `--obfuscate --split-debug-info`, AAB + iOS archive; Codemagic/Fastlane/GitHub Actions; mağaza kuralları `sky-mobile-app`.
