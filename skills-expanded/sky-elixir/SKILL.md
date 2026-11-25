---
name: sky-elixir
description: >-
  Elixir ve Phoenix: OTP temelleri (süreçler, GenServer, Supervisor, "bırak çöksün"), pattern
  matching ve pipe ile idiomatik kod, Phoenix bağlamları (contexts) ve Ecto (şema, changeset,
  sorgular, migration), Phoenix LiveView ile JS'siz gerçek zamanlı arayüzler, PubSub ve
  Presence, Oban ile arka plan işleri, test (ExUnit), dağıtım (releases, Fly) ve ne zaman
  Elixir doğru seçim. Elixir/Phoenix projesinde kullan.
disable-model-invocation: true
---

# Sky · Elixir & Phoenix

## Ne zaman?

Çok sayıda eşzamanlı bağlantı (sohbet, canlı panolar, bildirim, IoT), hata toleransı, gerçek zamanlı özellikleri az JS ile isteyen ekipler. BEAM sanal makinesi milyonlarca hafif süreci rahatça çalıştırır.

## İdiomatik Elixir

```elixir
def create_booking(%User{} = user, attrs) do
  with {:ok, service} <- fetch_service(user.org_id, attrs["service_id"]),
       :ok <- ensure_slot_free(service, attrs["starts_at"]),
       {:ok, booking} <- %Booking{} |> Booking.changeset(Map.put(attrs, "org_id", user.org_id)) |> Repo.insert() do
    Phoenix.PubSub.broadcast(App.PubSub, "org:#{user.org_id}", {:booking_created, booking})
    {:ok, booking}
  end
end
```
`{:ok, x}` / `{:error, reason}` dönüşleri, `with` zincirleri, pattern matching ile dallanma, pipe `|>` ile dönüşümler; istisna yalnızca gerçekten istisnai durumda.

## OTP

- **GenServer**: durumlu süreç (önbellek, oran sınırlayıcı, oturum); **Supervisor**: çöken süreci yeniden başlatır ("let it crash" — savunmacı kod yerine temiz yeniden başlatma).
- `Task.async_stream` paralel iş (eşzamanlılık sınırıyla); `Registry` ile adlandırılmış süreçler.

## Phoenix + Ecto

- **Context** modülleri (`Bookings`, `Accounts`) iş mantığının kamusal API'si; controller/LiveView yalnızca bunları çağırır.
- Ecto **changeset**: doğrulama + dönüşüm (`cast`, `validate_required`, `unique_constraint`, `exclusion_constraint`); sorgular `from b in Booking, where: b.org_id == ^org_id, preload: [:client]` (N+1 için preload).
- Migration'lar `mix ecto.gen.migration`; kısıtlar DB'de.
- Auth: `mix phx.gen.auth` (güvenli, hazır).

## LiveView (insanların "JS yazmadan mı?" dediği)

```elixir
def mount(_params, _session, socket) do
  if connected?(socket), do: Phoenix.PubSub.subscribe(App.PubSub, "org:#{socket.assigns.current_user.org_id}")
  {:ok, stream(socket, :bookings, Bookings.upcoming(socket.assigns.current_user))}
end
def handle_info({:booking_created, b}, socket), do: {:noreply, stream_insert(socket, :bookings, b, at: 0)}
```
Sunucu durumlu, WebSocket üzerinden DOM farkları; formlar canlı doğrulama (`phx-change`), `streams` ile büyük listeler, JS hook'ları gerektiğinde. Presence ile kim çevrimiçi.

## İşler, test, dağıtım

**Oban** (Postgres tabanlı kalıcı kuyruk, cron, yeniden deneme — bkz. `sky-jobs`); ExUnit + `Ecto.Adapters.SQL.Sandbox` (paralel DB testleri), `Phoenix.LiveViewTest`; `mix format`, Credo, Dialyzer;
`mix release` + Docker, Fly.io (kümeleme kolay), `config/runtime.exs` ile env.
