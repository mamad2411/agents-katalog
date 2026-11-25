---
name: sky-go
description: >-
  Go geliştirme: modül ve proje düzeni (cmd/, internal/), hata yönetimi (wrap, errors.Is/As),
  context ile iptal ve zaman aşımı, goroutine/channel/errgroup kalıpları ve sızıntı önleme,
  net/http (Go 1.22+ yönlendirme) ile API, slog ile log, pgx/sqlc ile veritabanı, tablo
  tabanlı testler ve httptest, golangci-lint, generics ölçüsü, graceful shutdown ve dağıtım.
  Go kodu yazarken veya gözden geçirirken kullan.
disable-model-invocation: true
---

# Sky · Go

## Düzen

```
go.mod
cmd/api/main.go          # giriş: yapılandırma, bağımlılıkları kur, sunucuyu başlat
internal/booking/        # alan paketi: handler.go, service.go, store.go, booking.go
internal/platform/db/
internal/platform/httpx/ # middleware, yanıt yardımcıları
```
- `internal/` dışarıdan import edilemez — varsayılan olarak her şey orada.
- Paket adları kısa, tekil, alan odaklı (`booking`, `user`); `utils`, `common` yok.
- Arayüzleri **kullanan** tarafta tanımla, küçük tut ("accept interfaces, return structs").

## Hatalar

```go
var ErrNotFound = errors.New("not found")

func (s *Store) Get(ctx context.Context, id string) (Booking, error) {
	b, err := s.q.GetBooking(ctx, id)
	if errors.Is(err, pgx.ErrNoRows) {
		return Booking{}, ErrNotFound
	}
	if err != nil {
		return Booking{}, fmt.Errorf("get booking %s: %w", id, err)
	}
	return b, nil
}
```
- Her hatayı ya ele al ya bağlamla sarmala (`%w`); `_ = err` yok.
- `panic` yalnızca programcı hatası/başlangıç; kütüphane kodunda asla.
- Alan bilgisi gerekiyorsa özel hata tipi + `errors.As`.

## context

İlk parametre `ctx context.Context`; DB, HTTP, uzun işlere aktar. `context.WithTimeout(ctx, 3*time.Second)` + `defer cancel()`.
Context'e iş verisi koyma (yalnızca istek kapsamlı: request ID, kullanıcı).

## Eşzamanlılık

```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(8)
for _, id := range ids {
	g.Go(func() error { return process(ctx, id) })   // Go 1.22+: döngü değişkeni her yinelemede yeni
}
if err := g.Wait(); err != nil {
	return err
}
```
- Her goroutine'in **nasıl biteceği** belli olsun (context, kapanan channel) — yoksa sızıntı.
- Paylaşılan durum: `sync.Mutex` veya tek sahipli goroutine + channel. `go test -race` CI'da.
- Channel'ı gönderen kapatır; nil channel sonsuza bloklar.

## HTTP (standart kütüphane, Go 1.22+)

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /bookings/{id}", h.get)
mux.HandleFunc("POST /bookings", h.create)
srv := &http.Server{Addr: ":8080", Handler: logging(recoverer(mux)), ReadHeaderTimeout: 5 * time.Second}

func (h *Handler) get(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	b, err := h.svc.Get(r.Context(), currentUser(r), id)
	if err != nil {
		writeError(w, err)
		return
	}
	writeJSON(w, http.StatusOK, b)
}
```
Girdi: `http.MaxBytesReader` + `json.NewDecoder` + `DisallowUnknownFields` + doğrulama. chi/echo yalnızca ek ihtiyaçta.

## Graceful shutdown

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
go func() { _ = srv.ListenAndServe() }()
<-ctx.Done()
shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
_ = srv.Shutdown(shutdownCtx)
```

## Veri ve log

- **pgx** + **sqlc** (SQL'den tip güvenli Go kodu) — ORM'siz, hızlı, okunur. Migration: goose / golang-migrate / atlas.
- **slog**: `slog.New(slog.NewJSONHandler(os.Stdout, nil))`, `logger.InfoContext(ctx, "booking created", "id", id)`.
- Yapılandırma: env + struct (`caarlos0/env`), başlangıçta doğrula.

## Test

```go
func TestValidPhone(t *testing.T) {
	tests := []struct {
		name, in string
		want     bool
	}{
		{"geçerli", "+905321234567", true},
		{"kısa", "123", false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := ValidPhone(tt.in); got != tt.want {
				t.Errorf("ValidPhone(%q) = %v, want %v", tt.in, got, tt.want)
			}
		})
	}
}
```
`httptest.NewRecorder` / `NewServer`; testcontainers-go; `t.Parallel()`; `go test ./... -race -cover`.

## Araçlar ve dağıtım

`gofmt`/`goimports`, **golangci-lint** (errcheck, govet, staticcheck, gosec, revive), `govulncheck`.
Generics yalnızca gerçekten tip bağımsız tekrar eden mantıkta; arayüz yetiyorsa arayüz.
`CGO_ENABLED=0 go build -ldflags="-s -w"` → distroless/scratch imaj (~15MB).
