---
name: d1-01-dotnet-webapi-init
description: "Scaffolds the up-api .NET 10 Web API project from the default template. Adds CORS (allow all origins). CRUD drill Day 1 step 1. Trigger: 'day1 step1', 'create up-api'."
compatibility: "Requires the .NET 10 SDK."
---

# Day 1 · Step 1 — Create up-api

```Run bash
dotnet new webapi -n up-api
```

Default template only — no packages, no `dotnet run`. Verify/add to `Program.cs`:

```csharp
builder.Services.AddControllers();
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

app.UseCors();
app.MapControllers();
```
