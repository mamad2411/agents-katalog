---
name: darkbot-clean-arch
description: Clean Architecture DarkBot.Net — Core / Application (фасады + BotEngine) / Infrastructure / Presentation. Без MediatR. Образец Sample/Desktop.Application. Используй при новых фичах, сервисах, ViewModels, DI, рефакторинге слоёв.
alwaysApply: false
---

# DarkBot.Net — Clean Architecture

Desktop-бот DarkOrbit: **WPF** + **BepInEx Unity-bridge** + Unity client v1.1.103.

Образец Application-слоя: `Sample/Desktop/Desktop.Application` (фасады, DTOs, Mappers — **без MediatR**).

## Зависимости слоёв

```text
Presentation → Application.Contracts (I*AppService), Infrastructure (только DI)
Infrastructure → Application, Core
Application    → Core
Core           → (ничего)
```

Composition root: `DarkBot.Net.Presentation.Extensions.DependencyInjection.BuildDarkBotHost`.

```csharp
services.AddApplication();
services.AddInfrastructure(configuration);
services.AddPresentationUi();
```

---

## Core (`DarkBot.Net.Core`)

| Папка | Содержимое |
|-------|------------|
| `Interfaces/Game/`, `Interfaces/Auth/` | Порты: `IGameConnection`, `IGameStateProbe`, `ICredentialStore` |
| `Managers/` | **Интерфейсы** API бота: `IHeroApi`, `IMovementApi`, `IStatsApi` |
| `Game/` | Контракты сущностей: `IGameMap`, `IHealth`, `ILocationInfo` |
| `Models/Game/`, `Options/` | Value objects, options (`DarkBotUiOptions`) |

❌ Нет WPF, Frida, Serilog host, реализаций managers.

---

## Application (`DarkBot.Net.Application`)

### PUBLIC — видит Presentation

```text
Contracts/              I*AppService — единственный API для ViewModels
DTOs/
  Responses/{Feature}/    BotStatusSnapshot, MapStatusSnapshot, …
  Commands/{Feature}/     по мере необходимости (как Desktop)
  Queries/{Feature}/
Mappers/{Feature}/        managers/domain → DTO (BotStatusSnapshotMapper, …)
Services/{Feature}/       *AppService — orchestration, вызывает Mappers
Extensions/               AddApplication(), Scrutor *AppService
```

### INTERNAL — BotEngine (не для VM)

```text
BotEngine/
├── Loop/           BotLoopService, IBotController        (tick 10 Hz)
├── Install/        BotInstallerService                   (Frida addresses)
├── Runtime/        BotRuntime, BotModuleRunner
├── Modules/        DisconnectModule, …
├── Managers/       HeroManager, MapManager, MovementApi, StatsManager, …
├── State/          GameMapModel, TrackedHealth, …        (impl Core IGameMap/IHealth)
├── Addresses/      BotAddressRegistry                      (бывш. Memory/)
└── Statistics/     StatImpl                                (internal для StatsManager)
```

**Namespaces:** `DarkBot.Net.Application.BotEngine.{Loop|Managers|State|…}`

❌ Корневых `Bot/`, `Managers/`, `Entities/`, `Memory/`, `Models/` — только `BotEngine/`.
❌ MediatR, WPF, UiStrings, `Process.Start`.

### Фасад (паттерн)

```csharp
// Contracts/IBotStatusAppService.cs
public interface IBotStatusAppService
{
    BotStatusSnapshot Capture();
}

// Services/Bot/BotStatusAppService.cs — только orchestration
public sealed class BotStatusAppService(...) : IBotStatusAppService
{
    public BotStatusSnapshot Capture() =>
        BotStatusSnapshotMapper.Create(hero, map, entities, frida, stats, bot, movement);
}
```

Scrutor: `AddAppServices()` сканирует `*AppService`, anchor `ILoginAppService`.

### AppService-фасады

`ILoginAppService` · `IGameLaunchAppService` · `IBotControlAppService` · `IBotStatusAppService` ·
`IGameConnectionStatusAppService` · `IMovementAppService` · `IAppShellAppService` ·
`IGameShutdownAppService` · `IGameClientRestartAppService`

---

## Infrastructure (`DarkBot.Net.Infrastructure`)

| Папка | Содержимое |
|-------|------------|
| `Game/` | FridaGameApi, launcher, lifecycle, restart/shutdown |
| `Hosting/` | VerifierSidecarHostedService |
| `Logging/` | `DarkBotSerilogHostBuilderExtensions` |
| `Auth/` | Login, credentials |

Может ссылаться на `Application.BotEngine.Loop` / `Addresses` (shutdown, restart).
❌ ViewModels, XAML.

---

## Presentation (`DarkBot.Net.Presentation`)

```text
ViewModels/{Feature}/     только I*AppService + Ui/*
Views/, Controls/         WPF + ReactiveUI
Formatting/               enum → UiStrings
Ui/Config, Ui/Shell        окна, навигация
Controls/Main/MapCanvas/   render-only (MapRenderSettings, Skia)
Extensions/                composition root
Diagnostics/               ReactiveUI probe
```

```csharp
// ✅ VM
Snapshot = _botStatus.Capture();  // DTOs.Responses.Bot напрямую

// ❌
Snapshot = SomeMapper.ToUi(...);
_heroManager.Tick();
```

❌ `Services/`, `Models/`, `Mapping/`, `Configuration/`, `Logging/` (Serilog → Infrastructure).
❌ Дубли `Application.DTOs.*` в Presentation.

---

## Frida-only

- Managers/BotEngine читают `IGameStateProbe`, не ReadProcessMemory.
- Клиент: `C:\DarkOrbit_Version1.1.102`
- Bridge: `darkorbit-unity-bridge/agent/dist/agent.js`
- Игра запускается пользователем, не ботом.

---

## Куда класть новый код

| Задача | Куда |
|--------|------|
| Use case для UI | `Contracts/I*AppService` + `Services/*AppService` |
| Response для UI | `DTOs/Responses/{Feature}/` |
| Маппинг в DTO | `Mappers/{Feature}/` |
| Tick / hero / map logic | `BotEngine/Managers/` или `BotEngine/Modules/` |
| Impl `IGameMap` / `IHealth` | `BotEngine/State/` |
| Frida / process / HTTP | Infrastructure |
| UI строки / render flags | Presentation `Formatting/` или `MapCanvas/` |

---

## Антипаттерны

- MediatR / `IRequest` / CQRS handlers
- ViewModel → Infrastructure, `HeroManager`, `IMovementApi`, `FridaGameApi`
- Маппинг 100+ строк внутри `*AppService` (→ `Mappers/`)
- `Presentation/Models/` дублирующие Application DTO
- Presentation → `BotEngine.*`
- Корневые legacy-папки в Application вместо `BotEngine/`
