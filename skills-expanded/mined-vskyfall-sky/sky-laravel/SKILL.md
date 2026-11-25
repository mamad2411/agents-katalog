---
name: sky-laravel
description: >-
  Laravel geliştirme: proje yapısı ve Artisan, Eloquent modelleri, ilişkiler ve N+1 önleme
  (with, preventLazyLoading), migration ve factory, Form Request doğrulama, Policy ile yetki,
  API Resource'lar, Sanctum, kuyruklar ve Horizon, zamanlanmış görevler, Pest testleri,
  Livewire/Inertia/Filament seçimi, Pint ve Larastan, güvenlik ve dağıtım. Laravel/PHP
  projesinde kullan.
disable-model-invocation: true
---

# Sky · Laravel

## Kurulum ve araçlar

```bash
composer create-project laravel/laravel app && cd app
php artisan install:api                 # Sanctum + routes/api.php
composer require --dev larastan/larastan pestphp/pest laravel/pint
```
Yerel: Laravel Herd veya Sail. Stil `./vendor/bin/pint`, analiz `phpstan` (Larastan, seviye 6+), test `./vendor/bin/pest`.

## Eloquent

```php
class Booking extends Model
{
    protected $fillable = ['client_id', 'service_id', 'starts_at', 'status'];

    protected function casts(): array
    {
        return ['starts_at' => 'immutable_datetime', 'status' => BookingStatus::class];
    }

    public function client(): BelongsTo
    {
        return $this->belongsTo(Client::class);
    }

    public function scopeUpcoming(Builder $q): void
    {
        $q->where('starts_at', '>=', now());
    }
}
```
- N+1: `Booking::with(['client', 'service'])->upcoming()->get()`; geliştirmede
  `Model::preventLazyLoading(! app()->isProduction());` (AppServiceProvider).
- Sayılar `withCount('bookings')`; büyük veri `chunkById(1000)`, `lazy()`.
- Atomik: `increment()`, `DB::transaction(fn () => …)`, `lockForUpdate()`.
- Kiracı izolasyonu: ilişki üzerinden sorgula (`$org->bookings()->findOrFail($id)`) veya global scope.

## Doğrulama: Form Request

```php
class StoreBookingRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Booking::class);
    }

    public function rules(): array
    {
        return [
            'service_id' => ['required', Rule::exists('services', 'id')->where('org_id', $this->user()->org_id)],
            'starts_at'  => ['required', 'date', 'after:now'],
            'phone'      => ['required', 'regex:/^\+905\d{9}$/'],
        ];
    }
}
```
Türkçe mesajlar: `laravel-lang` paketi + `APP_LOCALE=tr`.

## Yetki: Policy

```php
class BookingPolicy
{
    public function view(User $user, Booking $b): bool { return $user->org_id === $b->org_id; }
    public function cancel(User $user, Booking $b): bool { return $this->view($user, $b) && $b->starts_at->isFuture(); }
}
// controller: Gate::authorize('cancel', $booking);
```

## API

- `BookingResource` (`JsonResource`) ile çıktı — modeli doğrudan döndürme.
- Scoped route model binding (`->scopeBindings()`).
- Sanctum: SPA için çerez tabanlı, mobil/dış için kapsamlı token (`createToken('mobile', ['bookings:read'])`).
- Rate limit: `RateLimiter::for('api', …)`.

## Kuyruk ve zamanlama

- `ShouldQueue` job'lar: `$tries`, `backoff()`, `ShouldBeUnique`; Redis + **Horizon** paneli; commit sonrası `->afterCommit()`.
- `routes/console.php`: `Schedule::job(new SendReminders)->everyFiveMinutes()->withoutOverlapping();` + tek cron satırı.
- Bildirimler: `Notification` sınıfları (mail, database, SMS kanalı paketleri).

## Frontend

- **Livewire** (+ Flux/Volt): PHP içinde etkileşim, JS az, CRUD'da çok hızlı.
- **Inertia** (+ React/Vue): Laravel route'ları + modern SPA.
- **Filament**: dakikalar içinde güzel admin paneli — insanların en sevdiği Laravel aracı.

## Test (Pest)

```php
it('başka org randevusunu göremez', function () {
    $booking = Booking::factory()->create();
    $this->actingAs(User::factory()->create())
        ->getJson("/api/bookings/{$booking->id}")
        ->assertNotFound();
});
```
`RefreshDatabase`, factory'ler, `Http::fake()`, `Queue::fake()`, `Notification::fake()`, `$this->travelTo()`.

## Güvenlik ve dağıtım

`APP_DEBUG=false`, `APP_KEY` set, `$fillable`, Blade `{{ }}` kaçışlı (`{!! !!}` yalnızca güvenilir içerik), IDOR testleri.
Forge / Ploi / Vapor / Docker; `php artisan optimize`, `migrate --force`, Horizon/supervisor, `storage:link`.
