# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Build
dotnet build AStar.Dev.Onedrive.Sync.Client.slnx --configuration Release

# Run all unit tests
dotnet test --filter "FullyQualifiedName!~Integration&FullyQualifiedName!~EndToEnd"

# Run a single test class
dotnet test --filter "FullyQualifiedName~ConflictResolverTests"

# Run the app
dotnet run --project src/AStar.Dev.OneDrive.Sync.Client/AStar.Dev.OneDrive.Sync.Client.csproj

# Add EF Core migration
dotnet ef migrations add <MigrationName> --project src/AStar.Dev.OneDrive.Sync.Client

# Watch tests
dotnet watch test
```

## Architecture

**.NET 10 / Avalonia 11 desktop app (MVVM).** No web server, no API — pure desktop with Microsoft Graph API for OneDrive access.

### Bootstrap

`App.axaml.cs` is the composition root. `BootstrapAsync` builds a `Microsoft.Extensions.DependencyInjection` `ServiceProvider` and resolves all services from it. Service registrations live in `Services/ServiceCollectionExtensions.cs` (`AddOneDriveSyncServices`).

Bootstrap order matters:
1. `SettingsService.LoadAsync()` — async factory, pre-loaded before container build and registered as a singleton instance
2. `ServiceCollection` built, `ServiceProvider` stored in `App._serviceProvider`
3. `ILocalizationService.InitialiseAsync` called
4. `IThemeService.Apply` called with saved theme
5. `AppDbContext` resolved, `MigrateAsync()` run
6. `MainWindowViewModel` resolved (transient), passed to `MainWindow.InitialiseAsync`
7. `SyncScheduler.Start` called with saved interval

`ServiceProvider` is disposed on app exit via `desktop.Exit`, which automatically disposes singleton `IAsyncDisposable` services (e.g., `SyncScheduler`).

**Lifetimes:** all services are `Singleton` except `MainWindowViewModel` which is `Transient`. No `Scoped` — there is no HTTP scope in a desktop app.

### Navigation

`MainWindowViewModel` owns five lazy-cached view instances (`DashboardView`, `FilesView`, `ActivityView`, `AccountsView`, `SettingsView`). Navigation is driven by the `NavSection` enum — setting `ActiveSection` property swaps the `ActiveView`.

### Sync Pipeline

```
SyncScheduler (timer)
  → SyncService.SyncAccountAsync
      → GraphService.GetDeltaAsync   (full enum on first sync, delta link after)
      → LocalChangeDetector          (detect local uploads)
      → ClassifyJobsAsync            (conflict detection, 5-second tolerance)
      → ParallelDownloadPipeline     (bounded channel, 8 workers)
          → DownloadWorker (×8)
              → HttpDownloader       (retry + exponential backoff on HTTP 429)
```

`ConflictResolver` is a static utility class that applies the per-account `ConflictPolicy` (Ignore / LocalWins / RemoteWins / KeepBoth / LastWriteWins).

### Data Layer

SQLite via EF Core. `DbContextFactory.Create()` resolves the platform-correct path:
- Windows: `%APPDATA%\AStar.Dev.OneDrive.Sync\onedrivesync.db`
- Linux: `~/.config/AStar.Dev.OneDrive.Sync/onedrivesync.db`
- macOS: `~/Library/Application Support/AStar.Dev.OneDrive.Sync/onedrivesync.db`

Migrations live in `src/.../Data/Migrations/`. The app runs `MigrateAsync()` at startup.

Repositories: `AccountRepository` (accounts + folder selections + delta links), `SyncRepository` (job queue + conflict tracking).

### Authentication

MSAL with file-backed token cache (`TokenCacheService`). Authority is `consumers` (personal accounts only). `AuthService` handles interactive sign-in via system browser + loopback redirect, and silent token refresh. `StartupService.RestoreAccountsAsync` validates cached tokens at startup and filters out stale accounts.

### Local Nuget Packages (referenced as ProjectReferences)

- `src/nuget-packages/AStar.Dev.Functional.Extensions` — `Result<T>`, `Option<T>`, `Try`, `Pattern` functional primitives
- `src/nuget-packages/AStar.Dev.Utilities` — String, Enum, Linq, Path, Encryption extensions
- `src/nuget-packages/AStar.Dev.Logging.Extensions` — Serilog configuration helpers

### Test Stack

xUnit v3, NSubstitute (mocking), Shouldly (assertions), WireMock.Net (HTTP mocking), EF Core In-Memory provider (repository tests). Tests mirror the `src` directory structure under `test/AStar.Dev.OneDrive.Sync.Client.Tests.Unit/`.

### Converters

Avalonia value converters in `src/.../Converters/`. `SyncState` enum drives badge colors in the dashboard. The `DepthToIndentConverter` drives folder tree indentation (16px per depth level).

### Localization

JSON-based; `en-GB.json` is the only locale. `LocalizationService` loads it as an embedded resource. Resolved via `ILocalizationService` from the DI container.

### Settings

`SettingsService` persists `AppSettings` (theme, locale, sync interval, default conflict policy) to JSON in the platform data directory. Loaded at startup before DB migration.
