---
name: optimizely-scheduled-job-migrator
version: 1.0.0
category: Migration/Build
description: Migrate or create Optimizely CMS 12 scheduled jobs using the correct ScheduledPlugIn attribute, Execute method signature, and stop/cancellation patterns. Covers breaking changes from CMS 11.
compatibility: Optimizely CMS 12, EPiServer.CMS.Core 12.x, .NET 6+
---

# Optimizely CMS 12 Scheduled Job Migrator

## Trigger On

- "create a scheduled job"
- "migrate scheduled job"
- "add background job to Optimizely"
- "implement ScheduledPlugIn"
- any task involving `IScheduledJob` or `ScheduledJobBase`

## Documentation

- [Scheduled Jobs CMS 12](https://docs.developers.optimizely.com/content-management-system/docs/scheduled-jobs)
- [Breaking Changes CMS 11 → 12](https://docs.developers.optimizely.com/content-management-system/docs/breaking-changes-in-content-cloud-cms-12)

## Breaking Changes from CMS 11

| CMS 11 | CMS 12 | Action |
|---|---|---|
| `PrincipalInfo.CurrentPrincipal` in job | Not available | Remove or use `IHttpContextAccessor` with caution |
| `HttpContext.Current` in job | Not available in ASP.NET Core | Remove entirely |
| `JobExecutionStatus` return type | Still valid | Keep |
| Constructor DI | Fully supported | Preferred approach |
| `IsStopSignaled` property | Still valid | Keep for cooperative cancellation |

## Standard Scheduled Job Pattern

```csharp
using EPiServer.PlugIn;
using EPiServer.Scheduler;

[ScheduledPlugIn(
    DisplayName = "My Custom Job",
    Description = "Does something useful on a schedule",
    GUID = "D4E5F6A7-B8C9-0123-DEFG-456789012345",
    SortIndex = 100)]
public class MyCustomScheduledJob : ScheduledJobBase
{
    private bool _stopSignaled;
    private readonly IContentRepository _contentRepository;
    private readonly ILogger<MyCustomScheduledJob> _logger;

    public MyCustomScheduledJob(
        IContentRepository contentRepository,
        ILogger<MyCustomScheduledJob> logger)
    {
        _contentRepository = contentRepository;
        _logger = logger;
        IsStoppable = true;
    }

    public override void Stop()
    {
        _stopSignaled = true;
    }

    public override string Execute()
    {
        OnStatusChanged("Starting...");
        var processed = 0;

        try
        {
            var items = _contentRepository.GetChildren<PageData>(ContentReference.RootPage);

            foreach (var item in items)
            {
                if (_stopSignaled)
                    return $"Stopped after processing {processed} items.";

                // do work
                processed++;
                OnStatusChanged($"Processed {processed} items...");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error in scheduled job");
            throw;
        }

        return $"Successfully processed {processed} items.";
    }
}
```

## Restartable Job Pattern

```csharp
[ScheduledPlugIn(
    DisplayName = "Restartable Import Job",
    GUID = "E5F6A7B8-C9D0-1234-EFGH-567890123456",
    Restartable = true)]  // resumes after app recycle/crash
public class RestartableImportJob : ScheduledJobBase
{
    private bool _stopSignaled;

    public RestartableImportJob()
    {
        IsStoppable = true;
    }

    public override string Execute()
    {
        // Must be idempotent - job may re-run from beginning after restart
        // Track progress externally (e.g. in DB) to resume correctly
        var lastProcessedId = GetLastProcessedId();

        foreach (var item in GetItemsSince(lastProcessedId))
        {
            if (_stopSignaled) return "Stopped by user.";
            Process(item);
            SaveLastProcessedId(item.Id);
        }

        return "Complete.";
    }

    public override void Stop() => _stopSignaled = true;
}
```

## Enabling Scheduled Jobs in Program.cs

```csharp
// In Program.cs / Startup
builder.Services.Configure<SchedulerOptions>(o =>
{
    o.Enabled = true;
});
```

## Anti-Patterns

```csharp
// WRONG - HttpContext.Current removed in CMS 12
public override string Execute()
{
    var user = HttpContext.Current.User; // will throw
}

// WRONG - PrincipalInfo.CurrentPrincipal not set from HTTP context in scheduled jobs
var principal = PrincipalInfo.CurrentPrincipal; // unreliable in CMS 12 jobs

// WRONG - Missing GUID (job loses schedule config on rename)
[ScheduledPlugIn(DisplayName = "My Job")]
public class MyJob : ScheduledJobBase { }

// WRONG - Not cooperative with stop signal
public override string Execute()
{
    foreach (var item in millionItems)
    {
        Process(item); // never checks _stopSignaled - job can't be stopped
    }
}
```
