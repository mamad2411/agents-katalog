---
name: sky-rust
description: >-
  Rust geliştirme: cargo ve workspace, sahiplik/ödünç alma kalıpları ve borrow checker ile
  barışık tasarım, hata yönetimi (Result, ?, thiserror kütüphanede, anyhow uygulamada),
  enum/pattern matching ile durum modelleme, async (tokio), axum ile web API, sqlx, serde,
  tracing, clippy ve rustfmt, testler, unsafe'den kaçınma ve release ayarları. Rust kodu
  yazarken veya "borrow checker hatası" alındığında kullan.
disable-model-invocation: true
---

# Sky · Rust

## Proje

```bash
cargo new myapi && cd myapi
cargo add axum
cargo add tokio --features full
cargo add serde --features derive
cargo add sqlx --features runtime-tokio,postgres,uuid,chrono,macros
cargo add thiserror anyhow tracing tracing-subscriber
```
Büyük projede workspace (`[workspace] members = ["crates/*"]`): `api`, `domain`, `db` — derleme süresi ve sınırlar.

## Borrow checker ile kavga etmeden

- Parametre: sahiplik gerekmiyorsa `&str`/`&[T]`/`&T`; saklayacaksan `String`/`Vec<T>` (veya `impl Into<String>`).
- Uzun ömürlü referanslı struct'lar (`struct X<'a>`) yerine çoğu zaman **sahip olunan veri** veya ID.
- Paylaşım: tek thread `Rc<RefCell<T>>`, çok thread `Arc<Mutex<T>>`/`Arc<RwLock<T>>`; tercihen mesajla ilet (channel).
- `.clone()` utanç değil; sıcak döngü dışında okunurluğu tercih et, sonra profille.
- Borrow hatasında: kapsamı daralt, önce oku sonra yaz, `std::mem::take`, indeks yerine iterator.

## Hata yönetimi

```rust
#[derive(Debug, thiserror::Error)]
pub enum BookingError {
    #[error("randevu bulunamadı")]
    NotFound,
    #[error("slot dolu")]
    Conflict,
    #[error(transparent)]
    Db(#[from] sqlx::Error),
}

pub async fn get(pool: &PgPool, id: Uuid) -> Result<Booking, BookingError> {
    sqlx::query_as!(Booking, "select * from bookings where id = $1", id)
        .fetch_optional(pool)
        .await?
        .ok_or(BookingError::NotFound)
}
```
- Kütüphane/alan: `thiserror`. Uygulama/`main`: `anyhow::Result` + `.context("…")`.
- `unwrap()` yalnızca testte; imkânsız durumda `expect("neden imkânsız")`.

## Durumu tiplerle modelle

```rust
enum Payment {
    Pending { created: DateTime<Utc> },
    Paid { at: DateTime<Utc>, provider_id: String },
    Refunded { amount_minor: i64 },
}
```
Newtype ile karışmayı önle: `struct UserId(Uuid);`. "Parse, don't validate": geçerli tip oluşturulduysa geçerlidir.

## axum ile API

```rust
#[derive(Clone)]
struct AppState { pool: PgPool }

async fn get_booking(State(st): State<AppState>, Path(id): Path<Uuid>, user: AuthUser)
    -> Result<Json<Booking>, ApiError> {
    Ok(Json(booking::get_for_user(&st.pool, &user, id).await?))
}

let app = Router::new()
    .route("/bookings/{id}", get(get_booking))
    .layer(TraceLayer::new_for_http())
    .with_state(AppState { pool });
let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
axum::serve(listener, app).with_graceful_shutdown(shutdown_signal()).await?;
```
- `ApiError` için `impl IntoResponse` → durum kodu + JSON. Auth için özel extractor (`FromRequestParts`).
- `tower-http`: CORS, timeout, sıkıştırma, gövde boyutu sınırı.

## async (tokio)

- Async içinde bloklayan iş → `tokio::task::spawn_blocking`.
- `.await` boyunca `std::sync::MutexGuard` tutma → kapsamı daralt veya `tokio::sync::Mutex`.
- Eşzamanlılık: `JoinSet`, `buffer_unordered(8)`; iptal: `tokio::select!` + `CancellationToken`.

## Veri ve gözlem

- **sqlx**: derleme zamanında kontrol edilen sorgular (`query!`; CI için `cargo sqlx prepare` ile offline), `sqlx migrate`.
- **serde**: `#[serde(rename_all = "camelCase")]`, dış girdide `#[serde(deny_unknown_fields)]`.
- **tracing**: `#[tracing::instrument(skip(pool))]`, prod'da JSON çıktı.

## Kalite

`cargo fmt`, `cargo clippy -- -D warnings`, `cargo test` / `cargo nextest`, `cargo audit` / `cargo deny`.
Testler: modül içi `#[cfg(test)]`, entegrasyon `tests/`, `#[tokio::test]`, özellik tabanlı `proptest`.
`unsafe` yok; gerekiyorsa küçük, `// SAFETY:` açıklamalı, test edilmiş blok.
Release: `[profile.release] lto = true`, `codegen-units = 1`, `strip = true`; Docker'da `cargo-chef` ile bağımlılık önbelleği.
