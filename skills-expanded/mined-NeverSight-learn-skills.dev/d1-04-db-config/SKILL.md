---
name: d1-04-db-config
description: "Configures the up-api .NET project's PostgreSQL connection (Npgsql, EF Core DbContext). No redeploy — config/code only. Use when the user asks for Day 1 step 4 of the CRUD drill, or asks to connect up-api to the database."
compatibility: "Requires the .NET 10 SDK, and an existing up-api project + running Postgres db (from earlier drill steps)."
---

# Day 1 · Step 4 — Configure the DB connection (no redeploy)

```Run bash
cd up-api
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
dotnet add package Microsoft.EntityFrameworkCore.Design
```

`appsettings.Development.json`:
```json
{
  "ConnectionStrings": {
    "Default": "Host=localhost;Port=5432;Database=up_db;Username=upadmin;Password=uppass"
  }
}
```
Use `localhost` here because EF CLI commands (next steps) run from the host. Inside the `up-api`
container the connection string instead uses the compose service name `db` — that's already set in the
container's environment from the docker-deploy step, don't change it.

`Data/AppDbContext.cs`:
```csharp
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    // DbSet<Entity> properties are added in the entity-migration step
}
```

`Program.cs`:
```csharp
builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseNpgsql(builder.Configuration.GetConnectionString("Default")));
```

This step is code + config only — do not redeploy.
