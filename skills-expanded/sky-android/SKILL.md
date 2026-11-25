---
name: sky-android
description: >-
  Native Android (Kotlin): Jetpack Compose UI, tek yönlü veri akışı ve ViewModel + StateFlow,
  coroutines ve Flow, Room, Retrofit/Ktor ile ağ, Hilt ile DI, Navigation Compose tip güvenli
  rotalar, Material 3 ve dinamik renk, edge-to-edge, izinler, WorkManager, testler (Compose UI,
  Turbine, screenshot), R8 ve Play Console yayını. Android projesinde kullan.
disable-model-invocation: true
---

# Sky · Android

## Mimari

```
ui/      Composable ekranlar + ViewModel (UiState: StateFlow)
domain/  (isteğe bağlı) use case'ler
data/    Repository → Room (yerel) + API (uzak), tek gerçek kaynak = yerel DB
di/      Hilt modülleri
```
UDF: olaylar yukarı (ViewModel), durum aşağı (Composable). Composable'lar durumsuz ve önizlenebilir.

## ViewModel + StateFlow

```kotlin
data class BookingsUiState(val items: List<Booking> = emptyList(), val loading: Boolean = true, val error: String? = null)

@HiltViewModel
class BookingsViewModel @Inject constructor(private val repo: BookingRepository) : ViewModel() {
    val state: StateFlow<BookingsUiState> = repo.observeUpcoming()
        .map { BookingsUiState(items = it, loading = false) }
        .catch { emit(BookingsUiState(loading = false, error = it.message)) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), BookingsUiState())

    fun cancel(id: String) = viewModelScope.launch { repo.cancel(id) }
}

@Composable
fun BookingsScreen(vm: BookingsViewModel = hiltViewModel()) {
    val state by vm.state.collectAsStateWithLifecycle()
    BookingsContent(state, onCancel = vm::cancel)
}
```
`collectAsStateWithLifecycle` arka planda toplamayı durdurur.

## Compose ipuçları

- Kararlılık: değişmez koleksiyonlar (kotlinx.collections.immutable) veya `@Immutable` → gereksiz recomposition yok.
- `LazyColumn` öğelerinde `key = { it.id }`; ağır hesaplar `remember`/`derivedStateOf`.
- Material 3 dinamik renk (Android 12+), koyu tema, edge-to-edge ve `WindowInsets`.
- `@PreviewLightDark`, farklı font ölçekleri; erişilebilirlik: `contentDescription`, `semantics`, 48dp dokunma hedefi.

## Veri

- **Room**: `Flow<List<T>>` döndüren DAO'lar otomatik güncellenir; migration'lar.
- **Ağ**: Retrofit + kotlinx.serialization veya Ktor client; token interceptor; çevrimdışı önce yerele yaz, WorkManager ile senkron.
- **DataStore** tercihler için. `GlobalScope` yok.

## Navigasyon, arka plan, izinler

- Navigation Compose tip güvenli rotalar (`@Serializable data class BookingDetail(val id: String)`), App Links.
- WorkManager kısıtlı garanti işler; bildirim izni (Android 13+) bağlamlı; FCM push.

## Test ve yayın

JUnit + Turbine + MockK; Compose UI testleri; Robolectric; screenshot testleri (Roborazzi/Paparazzi); ktlint/detekt, Lint.
Version catalog, R8 (`isMinifyEnabled = true` + keep kuralları), Play App Signing, AAB, dahili → kapalı → üretim kademeli açılış, Data safety formu.
