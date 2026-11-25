---
name: sky-dotnet
description: >-
  C# ve .NET ile backend: ASP.NET Core Minimal API ve controller seçimi, DI yaşam süreleri,
  Options deseni, EF Core (AsNoTracking, Include, projeksiyon, N+1, migration, global filtre),
  FluentValidation, JWT/Identity, ProblemDetails ile hatalar, async/await kuralları, nullable
  reference types, xUnit + WebApplicationFactory + Testcontainers, OpenTelemetry ve dağıtım.
  .NET projesinde kullan.
disable-model-invocation: true
---

# Sky · .NET

## Proje

```bash
dotnet new webapi -n Acme.Api
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
dotnet add package Microsoft.EntityFrameworkCore.Design
```
csproj: `<Nullable>enable</Nullable>`, `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`.
Çözüm: `Acme.Api` (HTTP), `Acme.Domain` (varlık, kural), `Acme.Infrastructure` (EF, dış servisler), `Acme.Tests`.

## Minimal API

```csharp
var bookings = app.MapGroup("/api/bookings").RequireAuthorization().WithTags("Bookings");

bookings.MapPost("/", async (CreateBooking req, IValidator<CreateBooking> validator, BookingService svc,
                             ClaimsPrincipal user, CancellationToken ct) =>
{
    var result = await validator.ValidateAsync(req, ct);
    if (!result.IsValid) return Results.ValidationProblem(result.ToDictionary());
    var booking = await svc.CreateAsync(user.GetUserId(), req, ct);
    return Results.Created($"/api/bookings/{booking.Id}", BookingDto.From(booking));
});
```
Endpoint'leri alan bazlı statik sınıflara (`MapBookingEndpoints`) böl; controller'lar da geçerli.

## DI ve yapılandırma

- `AddScoped` (istek başına: DbContext, servisler), `AddSingleton` (durumsuz), `AddTransient`. Singleton içine scoped enjekte etme.
- Options: `AddOptions<SmsOptions>().BindConfiguration("Sms").ValidateDataAnnotations().ValidateOnStart();`
- Sırlar: geliştirmede User Secrets, prod'da env/Key Vault.

## EF Core

```csharp
public class AppDb(DbContextOptions<AppDb> options, ITenant tenant) : DbContext(options)
{
    public DbSet<Booking> Bookings => Set<Booking>();
    protected override void OnModelCreating(ModelBuilder b)
    {
        b.Entity<Booking>().HasIndex(x => new { x.OrgId, x.StartsAt });
        b.Entity<Booking>().HasQueryFilter(x => x.OrgId == tenant.OrgId);   // global kiracı filtresi
    }
}

var list = await db.Bookings.AsNoTracking()
    .Where(b => b.StartsAt >= now).OrderBy(b => b.StartsAt)
    .Select(b => new BookingDto(b.Id, b.StartsAt, b.Client.Name))
    .ToListAsync(ct);
```
- Okumada `AsNoTracking` + projeksiyon; döngüde navigasyon erişimi yok (N+1); kartezyen patlamada `AsSplitQuery()`.
- Migration: `dotnet ef migrations add AddBookings` → üretileni oku → prod'da migration bundle veya SQL script.
- `DateTimeOffset`, UTC; optimistic concurrency için satır sürümü.

## Hatalar ve auth

- `AddProblemDetails()` + `UseExceptionHandler()` + `IExceptionHandler` ile alan hatalarını durum kodlarına eşle.
- JWT: `AddAuthentication().AddJwtBearer(...)`; kullanıcı yönetimi Identity veya harici sağlayıcı.
- Politikalar `AddAuthorizationBuilder().AddPolicy(...)`; kaynak bazlı yetki serviste.

## async kuralları

Uçtan uca async; `.Result`/`.Wait()` yok. `CancellationToken`'ı endpoint'ten DB'ye geçir. `async void` yalnızca olay işleyicide.

## Test

```csharp
public class BookingTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    [Fact]
    public async Task Unauthorized_without_token()
    {
        var res = await factory.CreateClient().PostAsJsonAsync("/api/bookings", new { });
        Assert.Equal(HttpStatusCode.Unauthorized, res.StatusCode);
    }
}
```
`WebApplicationFactory<Program>` + Testcontainers; birim testlerde servisleri izole et.

## Gözlem ve dağıtım

OpenTelemetry (`AddOpenTelemetry().WithTracing(...).WithMetrics(...)`), `MapHealthChecks("/health")`, Serilog veya yerleşik JSON log.
`dotnet publish -c Release` → `mcr.microsoft.com/dotnet/aspnet` imajı veya `dotnet publish /t:PublishContainer`; Native AOT hızlı açılış için.
