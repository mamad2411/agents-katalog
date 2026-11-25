---
name: sky-ios
description: >-
  Native iOS (Swift): SwiftUI, Observation (@Observable) ile durum, async/await ve Swift 6
  strict concurrency (Sendable, actor, @MainActor), URLSession + Codable, SwiftData, Keychain,
  NavigationStack, widget ve Live Activities, App Intents, Swift Testing, erişilebilirlik ve
  App Store yayını. iOS/Swift projesinde kullan.
disable-model-invocation: true
---

# Sky · iOS

## Durum: @Observable

```swift
@Observable @MainActor
final class BookingsModel {
    var bookings: [Booking] = []
    var isLoading = false
    var error: String?
    private let api: BookingAPI
    init(api: BookingAPI) { self.api = api }

    func load() async {
        isLoading = true
        defer { isLoading = false }
        do { bookings = try await api.upcoming() } catch { self.error = error.localizedDescription }
    }
}

struct BookingsView: View {
    @State private var model = BookingsModel(api: .live)
    var body: some View {
        List(model.bookings) { BookingRow(booking: $0) }
            .overlay { if model.isLoading { ProgressView() } }
            .task { await model.load() }
            .refreshable { await model.load() }
    }
}
```
- `@State` sahip olunan model, `@Bindable` iki yönlü bağlama, `.environment(model)` paylaşım.
- Observation (iOS 17+) yalnızca okunan özellik değişince yeniden çizer.

## Concurrency (Swift 6)

- UI `@MainActor`; paylaşılan değiştirilebilir durum `actor`; sınır geçen tipler `Sendable`.
- `async let` / `withTaskGroup` paralel; görünüm işleri `.task` ile (otomatik iptal).
- Uyarıları susturma; modeli düzelt.

## Ağ

```swift
struct BookingAPI {
    var upcoming: () async throws -> [Booking]
    static let live = BookingAPI(upcoming: {
        var req = URLRequest(url: URL(string: "https://api.site.com/bookings")!)
        req.setValue("Bearer \(try Keychain.token())", forHTTPHeaderField: "Authorization")
        let (data, resp) = try await URLSession.shared.data(for: req)
        guard (resp as? HTTPURLResponse)?.statusCode == 200 else { throw APIError.badStatus }
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return try decoder.decode([Booking].self, from: data)
    })
}
```
Closure tabanlı bağımlılık → testte sahte veri. Token **Keychain**'de.

## Veri ve navigasyon

- **SwiftData** (`@Model`, `@Query`) yerel kalıcılık; sunucu kaynaksa önbellek olarak.
- `NavigationStack(path:)` + `navigationDestination(for:)` → Universal Links ve durum geri yükleme kolay.
- Bottom sheet: `.presentationDetents([.medium, .large])`.

## İnsanların sevdiği platform özellikleri

- **Widget'lar** ve **Live Activities** (yaklaşan randevu kilit ekranında geri sayım).
- **App Intents**: Siri/Kestirmeler/Spotlight ("yarınki randevularım").
- `.sensoryFeedback(.success, trigger:)` haptik, SF Symbols, dinamik yazı boyutu, `ShareLink`.

## Test ve yayın

**Swift Testing** (`@Test`, `#expect`, parametreli) + XCTest UI testleri; `#Preview` ile çok durumlu önizleme.
SwiftLint/swift-format. Xcode Cloud / Fastlane; TestFlight; App Store kuralları için `sky-mobile-app`.
